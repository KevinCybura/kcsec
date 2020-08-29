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

    symbol_id = models.CharField(max_length=150, unique=True)
    exchange = models.ForeignKey("crypto.Exchange", on_delete=models.DO_NOTHING)
    symbol_type = models.CharField(max_length=10, choices=SymbolTypeChoices.choices)
    asset_id_base = models.ForeignKey("crypto.Asset", related_name="base", on_delete=models.DO_NOTHING)
    asset_id_quote = models.ForeignKey("crypto.Asset", related_name="quote", on_delete=models.DO_NOTHING)
    asset_id_unit = models.ForeignKey("crypto.Asset", related_name="unit", on_delete=models.DO_NOTHING)
    data_start = models.DateField()
    data_end = models.DateField()
    data_quote_start = models.DateTimeField()
    data_quote_end = models.DateTimeField()
    data_orderbook_start = models.DateTimeField()
    data_orderbook_end = models.DateTimeField()
    data_trade_start = models.DateTimeField()
    data_trade_end = models.DateTimeField()
    volume_1hrs = models.FloatField()
    volume_1day = models.FloatField()
    volume_1mth = models.FloatField()
    volume_1hrs_usd = models.FloatField()
    volume_1day_usd = models.FloatField()
    volume_1mth_usd = models.FloatField()
    price = models.DecimalField(decimal_places=5, max_digits=50)

    class Meta:
        db_table = crypto_entity("symbol")
        verbose_name = "Symbol"
        verbose_name_plural = "Symbols"
