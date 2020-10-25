from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class CryptoShare(BaseModel):
    user = models.ForeignKey("core.Portfolio", on_delete=models.CASCADE)
    crypto_asset = models.ForeignKey("crypto.Symbol", on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=15, decimal_places=5)
    average_price = models.DecimalField(max_digits=15, decimal_places=5)
    percent_gain = models.FloatField()

    class Meta:
        db_table = crypto_entity("share")
        verbose_name = "Crypto currency share"
        verbose_name_plural = "Crypto currency shares"
