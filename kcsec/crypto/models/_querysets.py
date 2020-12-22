from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import F
from django.utils.timezone import utc
from psqlextra.expressions import DateTimeEpoch
from psqlextra.manager import PostgresQuerySet

if TYPE_CHECKING:
    from typing import Optional
    from typing import Tuple

    from kcsec.crypto.models import CryptoOrder
    from kcsec.crypto.models import CryptoShare
    from kcsec.crypto.models import Exchange
    from kcsec.crypto.models import Ohlcv
    from kcsec.crypto.models import Symbol
    from kcsec.crypto.types import CandleMessage
    from kcsec.crypto.types import TimeFrame


class OhlcvQuerySet(PostgresQuerySet):
    def filter_trade_view_chart(
        self, symbol: "Symbol", exchange: "Exchange", time_frame: "TimeFrame", limit: int = None
    ) -> "OhlcvQuerySet":
        """
            Filter data for TradeView light weight charts.
        :param symbol: `Symbol` which to get data for.
        :param exchange: the `Exchange` the symbol is traded on.
        :param time_frame: the `TimeFrame` to filter on.
        :param limit: optionally limit the amount of data to return.
        :return: OhlcvQuerySet which contains data used for TradeView light weight charts.
        """
        if limit is None:
            limit = time_frame.one_day_index

        filtered_qs = self.filter(symbol=symbol, exchange=exchange, time_frame=time_frame)
        return (
            filtered_qs.annotate_time()
            .annotate_value()
            .order_by("-time")[:limit]
            .values("time", "open", "high", "low", "close", "volume", "value")
        )

    def annotate_time(self) -> "OhlcvQuerySet":
        return self.annotate(time=DateTimeEpoch("time_open"))

    def annotate_value(self) -> "OhlcvQuerySet":
        return self.annotate(value=(F("high") + F("low")) / 2)

    def latest_price(self, symbol: "Symbol", exchange: "Exchange", time_frame: "TimeFrame") -> "Decimal":
        """
            Get latest_price of a symbol.
        :param symbol: the symbol the price is for.
        :param exchange: the exchange the symbol is on.
        :param time_frame: time frame of latest price.
        :return:
        """
        # return self.filter(symbol=symbol, time_frame=time_frame).order_by("-time_open").values_list("close")[0]
        return self.filter(symbol=symbol, exchange=exchange, time_frame=time_frame).latest().close

    def one_day_difference(
        self, symbol: "Symbol", exchange: "Exchange", time_frame: "TimeFrame", price: "Optional[Decimal]" = None
    ) -> "Tuple[Decimal, Decimal]":
        """
            Gets the one day price and percent change for a symbol.
        :param symbol: the symbol the difference is for
        :param exchange: exchange the symbol is traded on
        :param time_frame: time for 24h difference see "types.TimeFrame"
        :param price: Optionally  pass in the current price or get latest price
        :return: Tuple[Decimal, Decimal] that is percent_change and price_change
        """
        if not price:
            price = self.latest_price(symbol=symbol, exchange=exchange, time_frame=time_frame)

        qs = (
            self.filter(symbol=symbol, exchange=exchange, time_frame=time_frame)
            .order_by("-time_open")
            .annotate(percent_change=(F("close") / price) - Decimal(1.0), price_change=(F("close") - price))
        )
        try:
            obj = qs[time_frame.one_day_index]
        except IndexError:
            obj = qs[qs.count() - 1]

        ret = obj.percent_change, obj.price_change
        return ret

    def bulk_create_from_message(self, message: "CandleMessage", exchange: "Exchange") -> "Ohlcv":
        obj = [
            self.model(
                symbol_id=message["symbol"],
                asset_id_base_id=message["symbol"][:3],
                asset_id_quote_id=message["symbol"][3:],
                exchange_id=exchange,
                time_open=datetime.fromtimestamp(change["time"], tz=utc),
                open=change["open"],
                high=change["high"],
                low=change["low"],
                close=change["close"],
                volume=change["volume"],
                time_frame=message["time_frame"],
            )
            for change in message["changes"]
        ]
        return self.bulk_create(obj, ignore_conflicts=True)


class CryptoShareQuerySet(PostgresQuerySet):
    def update_shares(self, price: float) -> int:
        return self.update(percent_change=(price / F("average_price") - Decimal(1.0)) * 100)

    def execute_order(self, order: "CryptoOrder") -> "Tuple[CryptoShare, bool]":
        """
            Execute a order and update a `CryptoShare` row. Creates or updates a `CryptoShare` row.
        :param order: `CryptoOrder` that is used to update the a `CryptoShare` row.
        :return: `Tuple[CryptoShare, bool]`  (share, created)
        """
        with transaction.atomic(using=self.db):
            try:
                share: "CryptoShare" = self.select_for_update().get(
                    portfolio_id=order.portfolio_id, crypto_symbol_id=order.crypto_symbol_id
                )
            except self.model.DoesNotExist:
                share: "CryptoShare" = self.create(
                    portfolio_id=order.portfolio_id,
                    crypto_symbol_id=order.crypto_symbol_id,
                    shares=order.shares,
                    average_price=order.price,
                    percent_change=0.0,
                )
                return share, True

            # If its a sell set quantity to a negative value.
            if order.trade_type == order.TradeType.SELL:
                order.shares *= -1

            total = (share.average_price * share.shares) + (order.price * order.shares)

            share.average_price = total / (order.shares + share.shares)

            share.shares += order.shares

            share.percent_change = share.average_price / order.crypto_symbol.price - Decimal(1.0)

            share.save()

        return share, False


class SymbolQuerySet(PostgresQuerySet):
    def update_price_and_shares(self, symbol: str, exchange: "Exchange", price: float) -> int:
        """
            Update price of a symbol and all shares of that symbol.
        :param symbol: Symbol id to update
        :param exchange: Exchange the symbol is traded on.
        :param price: new price of symbol
        :return: int: the number of shares updated
        """
        symbol: "Symbol" = self.get(pk=symbol, exchange=exchange)
        symbol.price = price
        num_updated = symbol.cryptoshare_set.update_shares(price)
        symbol.save()
        return num_updated
