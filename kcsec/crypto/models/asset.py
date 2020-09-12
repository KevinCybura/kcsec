from django.db import models
from django.utils.html import mark_safe

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Asset(BaseModel):
    asset_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=50, null=True)
    type_is_crypto = models.BooleanField(null=True)
    data_start = models.DateTimeField(null=True)
    data_end = models.DateTimeField(null=True)
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
    price_usd = models.DecimalField(decimal_places=5, max_digits=50, null=True)
    asset_icon = models.ImageField(upload_to="images/crypto/", null=True)

    class Meta:
        db_table = crypto_entity("asset")
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    @property
    def icon(self):
        if self.asset_icon:
            return mark_safe('<img src="{}" width="16" height="16" />'.format(self.asset_icon.url))
        return ""
