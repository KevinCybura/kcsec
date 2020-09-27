from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Ohlcv(BaseModel):
    exchange = models.ForeignKey("crypto.Exchange", on_delete=models.DO_NOTHING)
    asset_id_base = models.ForeignKey("crypto.Asset", related_name="ohlcv_base", on_delete=models.DO_NOTHING)
    asset_id_quote = models.ForeignKey("crypto.Asset", related_name="ohlcv_quote", on_delete=models.DO_NOTHING)
    time_period_start = models.DateTimeField(null=True)
    time_period_end = models.DateTimeField(null=True)
    time_open = models.DateTimeField()
    time_close = models.DateTimeField(null=True)
    open = models.DecimalField(decimal_places=10, max_digits=25)
    high = models.DecimalField(decimal_places=10, max_digits=25)
    low = models.DecimalField(decimal_places=10, max_digits=25)
    close = models.DecimalField(decimal_places=10, max_digits=25)
    volume = models.DecimalField(decimal_places=10, max_digits=25)
    trades_count = models.IntegerField(null=True)

    class Meta:
        db_table = crypto_entity("ohlcv")
        verbose_name = "Open High Low Close Volume"
        verbose_name_plural = "Open High Low Close Volume"
        unique_together = ("exchange_id", "asset_id_base", "asset_id_quote", "time_open")
