from typing import TYPE_CHECKING

from django.db import transaction
from psqlextra.manager import PostgresQuerySet

if TYPE_CHECKING:
    from kcsec.crypto.models import CryptoOrder
    from kcsec.crypto.models import CryptoShare


class CryptoShareQuerySet(PostgresQuerySet):
    def execute_order(self, order: "CryptoOrder") -> ("CryptoShare", bool):
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
                )
                return share, True

            # If its a sell set quantity to a negative value.
            if order.trade_type == order.TradeType.SELL:
                order.shares = -1 * order.shares

            total = (share.average_price * share.shares) + (order.price * order.shares)

            share.average_price = total / (order.shares + share.shares)

            share.shares += order.shares

            share.save()

        return share, False
