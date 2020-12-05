from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class CryptoOrder(BaseModel):
    class OrderType(models.Choices):
        BUY = "buy"
        SELL = "sell"

    crypto_symbol = models.ForeignKey("crypto.Symbol", on_delete=models.DO_NOTHING)
    share = models.ForeignKey("crypto.CryptoShare", on_delete=models.DO_NOTHING, null=True)
    portfolio = models.ForeignKey("core.Portfolio", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    shares = models.DecimalField(max_digits=15, decimal_places=5)
    filled = models.BooleanField(default=False)
    order_type = models.CharField(choices=OrderType.choices, max_length=5)

    class Meta:
        db_table = crypto_entity("order")
        verbose_name = "Crypto currency order"
        verbose_name_plural = "Crypto currency order"
