from typing import TYPE_CHECKING

from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity
from kcsec.crypto.models.querysets.share import CryptoShareQuerySet

if TYPE_CHECKING:
    from decimal import Decimal


class CryptoShare(BaseModel):
    portfolio = models.ForeignKey("core.Portfolio", on_delete=models.CASCADE)
    symbol = models.ForeignKey("crypto.Symbol", on_delete=models.DO_NOTHING)
    shares = models.DecimalField(max_digits=15, decimal_places=5)
    average_price = models.DecimalField(max_digits=15, decimal_places=5)

    objects = CryptoShareQuerySet.as_manager()

    class Meta:
        db_table = crypto_entity("share")
        verbose_name = "Crypto currency share"
        verbose_name_plural = "Crypto currency shares"
        unique_together = ("portfolio", "symbol")

    def average_percent_change(self, price: "Decimal"):
        return self.percent_change(price, self.average_price)

    @classmethod
    def percent_change(cls, new_price: "Decimal", original_price: "Decimal"):
        """
        Percent change is calculated the following way.

        if Decrease
            Decrease = Original Number - New Number
            % Decrease = Decrease ÷ Original Number × 100

        if Increase
            Increase = New Number - Original Number
            % increase = Increase ÷ Original Number × 100.
        :param new_price:
        :param original_price:
        :return:
        """
        if new_price > original_price:
            ret = (new_price - original_price) / original_price * 100
            return ret

        ret = (original_price - new_price) / original_price * -100
        return ret
