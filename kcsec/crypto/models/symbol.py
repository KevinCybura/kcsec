from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Symbol(BaseModel):
    class SymbolTypeChoices(models.TextChoices):
        SPOT = "SPOT"
        FUTURES = "FUTURES"
        OPTION = "OPTION"
        PERPETUAL = "PERPETUAL"
        INDEX = "INDEX"
        CREDIT = "CREDIT"

    symbol_id = models.CharField(max_length=150, unique=True, primary_key=True)
    exchange = models.ForeignKey("crypto.Exchange", on_delete=models.DO_NOTHING, null=True, default="")
    symbol_type = models.CharField(max_length=10, choices=SymbolTypeChoices.choices)
    asset_id_base = models.ForeignKey(
        "crypto.Asset", related_name="base", on_delete=models.DO_NOTHING, null=True, default=""
    )
    asset_id_quote = models.ForeignKey(
        "crypto.Asset", related_name="quote", on_delete=models.DO_NOTHING, null=True, default=""
    )
    asset_id_unit = models.ForeignKey(
        "crypto.Asset", related_name="unit", on_delete=models.DO_NOTHING, null=True, default=""
    )
    data_start = models.DateField(null=True)
    data_end = models.DateField(null=True)
    data_quote_start = models.DateTimeField(null=True)
    data_quote_end = models.DateTimeField(null=True)
    data_orderbook_start = models.DateTimeField(null=True)
    data_orderbook_end = models.DateTimeField(null=True)
    data_trade_start = models.DateTimeField(null=True)
    data_trade_end = models.DateTimeField(null=True)
    volume_1hrs = models.FloatField(null=True)
    volume_1day = models.FloatField(null=True)
    volume_1mth = models.FloatField(null=True)
    volume_1hrs_usd = models.FloatField(null=True)
    volume_1day_usd = models.FloatField(null=True)
    volume_1mth_usd = models.FloatField(null=True)
    price = models.DecimalField(decimal_places=5, max_digits=50, null=True)
    symbol_icon = models.ImageField(upload_to="images/crypto/", height_field=48, width_field=48, null=True)

    class Meta:
        db_table = crypto_entity("symbol")
        verbose_name = "Symbol"
        verbose_name_plural = "Symbols"
