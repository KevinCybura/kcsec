from typing import TYPE_CHECKING

from django.db import transaction
from psqlextra.manager import PostgresQuerySet

if TYPE_CHECKING:
    from typing import Tuple

    from kcsec.crypto.models import CryptoOrder
    from kcsec.crypto.models import CryptoShare


class CryptoShareQuerySet(PostgresQuerySet):
    def execute_order(self, order: "CryptoOrder") -> "Tuple[CryptoShare, bool]":
        """
            Execute a order and update a `CryptoShare` row. Creates or updates a `CryptoShare` row.
            If shares falls to 0 the row is deleted.
        :param order: `CryptoOrder` that is used to update the a `CryptoShare` row.
        :return: `Tuple[CryptoShare, bool]`  (share, created)
        """
        with transaction.atomic(using=self.db):
            try:
                share: "CryptoShare" = self.select_for_update().get(
                    portfolio_id=order.portfolio_id, symbol_id=order.symbol_id
                )
            except self.model.DoesNotExist:
                share: "CryptoShare" = self.create(
                    portfolio_id=order.portfolio_id,
                    symbol_id=order.symbol_id,
                    shares=order.shares,
                    average_price=order.price,
                )
                return share, True

            shares_traded = order.shares
            # If its a buy add shares and update average_price.
            if order.trade_type == order.TradeType.BUY:
                total = (share.average_price * share.shares) + (order.price * shares_traded)

                share.average_price = total / (shares_traded + share.shares)

                share.shares += shares_traded
            # If its a sell subtract the shares
            else:
                share.shares -= shares_traded

            share.save()

        return share, False
