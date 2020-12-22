from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._managers import SymbolManager
from kcsec.crypto.models._meta import crypto_entity


class Symbol(BaseModel):
    class SymbolTypeChoices(models.TextChoices):
        CRYPTO = "crypto"

    id = models.CharField(max_length=150, primary_key=True)
    exchange = models.ForeignKey("crypto.Exchange", on_delete=models.DO_NOTHING)
    symbol_type = models.CharField(max_length=10, choices=SymbolTypeChoices.choices)
    asset_id_base = models.ForeignKey(
        "crypto.Asset",
        related_name="base",
        on_delete=models.DO_NOTHING,
    )
    asset_id_quote = models.ForeignKey(
        "crypto.Asset",
        related_name="quote",
        on_delete=models.DO_NOTHING,
    )
    price = models.DecimalField(decimal_places=5, max_digits=50, null=True)
    symbol_icon = models.ImageField(upload_to="images/crypto/", height_field=48, width_field=48, null=True)

    objects = SymbolManager()

    class Meta:
        db_table = crypto_entity("symbol")
        verbose_name = "Symbol"
        verbose_name_plural = "Symbols"
        unique_together = ("id", "exchange")
