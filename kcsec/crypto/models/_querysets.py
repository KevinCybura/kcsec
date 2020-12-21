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
    from kcsec.crypto.models import Ohlcv
    from kcsec.crypto.models import Symbol
    from kcsec.crypto.types import CandleMessage


class OhlcvQuerySet(PostgresQuerySet):
    def trade_view_chart_filter(
        self, base: str, quote: str, exchange: str, time_frame: "Ohlcv.TimeFrame", limit: int = 1441
    ) -> "OhlcvQuerySet":
        filtered_qs = self.filter(asset_id_base=base, asset_id_quote=quote, exchange=exchange, time_frame=time_frame)
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

    def latest_price(self, base: str, quote: str, exchange: str, time_frame: "Ohlcv.TimeFrame") -> "OhlcvQuerySet":
        return (
            self.filter(asset_id_base=base, asset_id_quote=quote, exchange=exchange, time_frame=time_frame)
            .order_by("-time_open")
            .values_list("close")[0]
        )

    def get_24_hour_difference(
        self, base: str, quote: str, exchange: str, time_frame: "Ohlcv.TimeFrame", price: "Optional[Decimal]" = None
    ) -> "Ohlcv":
        if not price:
            price = self.latest_price(base, quote, exchange, time_frame)

        qs = (
            self.filter(asset_id_base=base, asset_id_quote=quote, exchange_id=exchange, time_frame=time_frame)
            .order_by("-time_open")
            .annotate(percent_change=(F("close") / price) - Decimal(1.0))
            .annotate(price_change=(F("close") - price))
        )

        try:
            obj = qs[1441]
        except IndexError:
            obj = qs[0]

        return obj

    def bulk_create_from_message(self, message: "CandleMessage", exchange: str) -> "Ohlcv":
        obj = [
            self.model(
                exchange_id=exchange,
                asset_id_base_id=message["symbol"][:3],
                asset_id_quote_id=message["symbol"][3:],
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
    def execute_order(self, order: "CryptoOrder") -> "Tuple[CryptoShare, bool]":
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
    def update_price_and_shares(self, symbol: Decimal, price: float) -> int:
        symbol: "Symbol" = self.get(pk=symbol)
        symbol.price = price
        num_updated = symbol.cryptoshare_set.filter().update(
            percent_change=(price / F("average_price") - Decimal(1.0)) * 100
        )
        symbol.save()
        return num_updated
