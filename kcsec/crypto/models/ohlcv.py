from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._managers import OhlcvManager
from kcsec.crypto.models._meta import crypto_entity
from kcsec.crypto.types import TimeFrame


class Ohlcv(BaseModel):
    symbol = models.ForeignKey("crypto.Symbol", on_delete=models.DO_NOTHING)
    asset_id_base = models.ForeignKey("crypto.Asset", related_name="ohlcv_base", on_delete=models.DO_NOTHING)
    asset_id_quote = models.ForeignKey("crypto.Asset", related_name="ohlcv_quote", on_delete=models.DO_NOTHING)
    exchange = models.ForeignKey("crypto.Exchange", on_delete=models.DO_NOTHING)
    time_open = models.DateTimeField()
    time_close = models.DateTimeField(null=True)
    time_frame = models.CharField(choices=TimeFrame.choices, max_length=3)
    open = models.DecimalField(decimal_places=10, max_digits=25)
    high = models.DecimalField(decimal_places=10, max_digits=25)
    low = models.DecimalField(decimal_places=10, max_digits=25)
    close = models.DecimalField(decimal_places=10, max_digits=25)
    volume = models.DecimalField(decimal_places=10, max_digits=25)
    trades_count = models.IntegerField(null=True)

    objects = OhlcvManager()

    class Meta:
        db_table = crypto_entity("ohlcv")
        verbose_name = "Open High Low Close Volume"
        verbose_name_plural = "Open High Low Close Volume"
        unique_together = ("symbol", "exchange", "time_open", "time_frame")
        ordering = ["time_open"]
        get_latest_by = ["time_open"]
