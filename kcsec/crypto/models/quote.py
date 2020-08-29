from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Quote(BaseModel):
    symbol_id = models.ForeignKey("crypto.Symbol", on_delete=models.DO_NOTHING)
    time_exchange = models.DateTimeField()
    time_coin_api = models.DateTimeField()
    ask_price = models.DecimalField(decimal_places=5, max_digits=50)
    ask_size = models.IntegerField()
    bid_price = models.DecimalField(decimal_places=5, max_digits=50)
    bid_size = models.IntegerField()

    class Meta:
        db_table = crypto_entity("quote")
        verbose_name = "Crypto currency quote"
        verbose_name_plural = "Crypto currency quotes"
