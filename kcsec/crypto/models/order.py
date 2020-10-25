from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class CryptoOrder(BaseModel):
    share = models.ForeignKey("crypto.CryptoShare", on_delete=models.CASCADE)
    user = models.ForeignKey("core.Portfolio", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    filled = models.BooleanField()

    class Meta:
        db_table = crypto_entity("order")
        verbose_name = "Crypto currency order"
        verbose_name_plural = "Crypto currency order"
