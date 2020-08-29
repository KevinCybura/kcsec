from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Asset(BaseModel):
    asset = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=30)
    type_is_crypto = models.BooleanField()
    data_quote_start = models.DateTimeField()
    data_quote_end = models.DateTimeField()
    data_orderbook_start = models.DateTimeField()
    data_orderbook_end = models.DateTimeField()
    data_trade_start = models.DateTimeField()
    data_trade_end = models.DateTimeField()
    data_quote_count = models.IntegerField()
    data_trade_count = models.IntegerField()
    data_symbols_count = models.IntegerField()
    volume_1hrs_usd = models.FloatField()
    volume_1day_usd = models.FloatField()
    volume_1mth_usd = models.FloatField()
    price_usd = models.DecimalField(decimal_places=5, max_digits=50)

    class Meta:
        db_table = crypto_entity("asset")
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
