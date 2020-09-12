from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Ohlcv(BaseModel):
    asset_id_base = models.ForeignKey("crypto.Asset", related_name="ohlcv_base", on_delete=models.DO_NOTHING)
    asset_id_quote = models.ForeignKey("crypto.Asset", related_name="ohlcv_quote", on_delete=models.DO_NOTHING)
    time_period_start = models.DateTimeField()
    time_period_end = models.DateTimeField()
    time_open = models.DateTimeField()
    time_close = models.DateTimeField()
    price_open = models.DecimalField(decimal_places=10, max_digits=25)
    price_high = models.DecimalField(decimal_places=10, max_digits=25)
    price_low = models.DecimalField(decimal_places=10, max_digits=25)
    price_close = models.DecimalField(decimal_places=10, max_digits=25)
    volume_traded = models.DecimalField(decimal_places=10, max_digits=25)
    trades_count = models.IntegerField()

    class Meta:
        db_table = crypto_entity("ohlcv")
        verbose_name = "Open High Low Close Volume"
        verbose_name_plural = "Open High Low Close Volume"
        unique_together = ("time_period_start", "time_period_end")
