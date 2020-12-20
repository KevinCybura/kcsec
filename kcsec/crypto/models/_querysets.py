from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import F
from psqlextra.expressions import DateTimeEpoch
from psqlextra.manager import PostgresQuerySet

if TYPE_CHECKING:
    from typing import Tuple

    from kcsec.crypto.models import CryptoOrder
    from kcsec.crypto.models import CryptoShare


class OhlcvQuerySet(PostgresQuerySet):
    def trade_view_chart_filter(
        self, asset_id_base: str, asset_id_quote: str, exchange: str, limit: int = 1441
    ) -> "OhlcvQuerySet":
        return (
            self.filter(asset_id_base=asset_id_base, asset_id_quote=asset_id_quote, exchange=exchange)
            .annotate_time()
            .annotate_value()
            .order_by("-time")[:limit]
            .values("time", "open", "high", "low", "close", "volume", "value")
        )

    def annotate_time(self) -> "OhlcvQuerySet":
        return self.annotate(time=DateTimeEpoch("time_open"))

    def annotate_value(self) -> "OhlcvQuerySet":
        return self.annotate(value=(F("high") + F("low")) / 2)

    def latest_price(self, asset_id_base: str, asset_id_quote: str, exchange: str) -> "OhlcvQuerySet":
        return (
            self.filter(asset_id_base=asset_id_base, asset_id_quote=asset_id_quote, exchange=exchange)
            .order_by("-time_open")
            .values_list("close")[0]
        )

    def bulk_create_from_message(self, message: dict[str, dict], exchange: str):
        pass

        # obj = [
        #     Ohlcv(
        #         exchange=exchange,
        #         asset_id_base_id=message["symbol"][:3],
        #         asset_id_quote_id=message["symbol"][3:],
        #         time_open=datetime.fromtimestamp(change["time"], tz=utc),
        #         open=change["open"],
        #         high=change["high"],
        #         low=change["low"],
        #         close=change["close"],
        #         volume=change["volume"],
        #     )
        #     for change in message["changes"]
        # ]


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
                order.shares = -1 * order.shares

            total = (share.average_price * share.shares) + (order.price * order.shares)

            share.average_price = total / (order.shares + share.shares)

            share.shares += order.shares

            share.percent_change = share.average_price / order.crypto_symbol.price - Decimal(1.0)

            share.save()

        return share, False


class SymbolQuerySet(PostgresQuerySet):
    def update_price_and_shares(self, symbol: Decimal, price: float):
        symbol = self.get(pk=symbol)
        symbol.price = price
        symbol.cryptoshare_set.filter().update(percent_change=(price / F("average_price") - Decimal(1.0)) * 100)
        symbol.save()
