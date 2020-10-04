from django.db import models

from kcsec.core.base import BaseModel
from kcsec.securities.models._meta import SYMBOL_TYPE_CHOICES
from kcsec.securities.models._meta import securities_entity


class InternationalSymbol(BaseModel):
    symbol = models.CharField(primary_key=True, max_length=10)
    exchange = models.ForeignKey("securities.InternationalExchange", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    is_enabled = models.BooleanField()
    type = models.CharField(choices=SYMBOL_TYPE_CHOICES, max_length=5)
    region = models.CharField(max_length=20)
    currency = models.ForeignKey("securities.Currency", on_delete=models.CASCADE)
    iex_id = models.CharField(max_length=25)

    class Meta:
        db_table = securities_entity("international_symbol")
        verbose_name = "International Symbol"
        verbose_name_plural = "International Symbols"
