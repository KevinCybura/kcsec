from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Exchange(BaseModel):
    exchange = models.CharField(max_length=30, primary_key=True)
    website = models.URLField()
    name = models.CharField(max_length=30)
    data_start = models.DateField()
    data_end = models.DateField()
    data_quote_start = models.DateTimeField()
    data_quote_end = models.DateTimeField()
    data_orderbook_start = models.DateTimeField()
    data_orderbook_end = models.DateTimeField()
    data_trade_start = models.DateTimeField()
    data_trade_end = models.DateTimeField()
    data_symbols_count = models.IntegerField()
    volume_1hrs_usd = models.FloatField()
    volume_1day_usd = models.FloatField()
    volume_1mth_usd = models.FloatField()

    class Meta:
        db_table = crypto_entity("exchange")
        verbose_name = "Crypto currency exchange"
        verbose_name_plural = "Crypto currency exchanges"
