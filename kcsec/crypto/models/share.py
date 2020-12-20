from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity
from kcsec.crypto.models._querysets import CryptoShareQuerySet


class CryptoShare(BaseModel):
    portfolio = models.ForeignKey("core.Portfolio", on_delete=models.CASCADE)
    crypto_symbol = models.ForeignKey("crypto.Symbol", on_delete=models.DO_NOTHING)
    shares = models.DecimalField(max_digits=15, decimal_places=5)
    average_price = models.DecimalField(max_digits=15, decimal_places=5)
    percent_change = models.DecimalField(max_digits=7, decimal_places=2)

    objects = CryptoShareQuerySet.as_manager()

    class Meta:
        db_table = crypto_entity("share")
        verbose_name = "Crypto currency share"
        verbose_name_plural = "Crypto currency shares"
        unique_together = ("portfolio", "crypto_symbol")
