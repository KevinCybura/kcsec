from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Exchange(BaseModel):
    exchange_id = models.CharField(max_length=60, unique=True, primary_key=True)
    website = models.URLField()
    name = models.CharField(max_length=60)
    data_start = models.DateField(null=True)
    data_end = models.DateField(null=True)
    data_quote_start = models.DateTimeField(null=True)
    data_quote_end = models.DateTimeField(null=True)
    data_orderbook_start = models.DateTimeField(null=True)
    data_orderbook_end = models.DateTimeField(null=True)
    data_trade_start = models.DateTimeField(null=True)
    data_trade_end = models.DateTimeField(null=True)
    data_symbols_count = models.IntegerField(null=True)
    volume_1hrs_usd = models.FloatField(null=True)
    volume_1day_usd = models.FloatField(null=True)
    volume_1mth_usd = models.FloatField(null=True)

    class Meta:
        db_table = crypto_entity("exchange")
        verbose_name = "Crypto currency exchange"
        verbose_name_plural = "Crypto currency exchanges"
