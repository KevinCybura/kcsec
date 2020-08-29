from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import core_entity


class Currency(BaseModel):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = core_entity("currency")
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class CurrencyPair(BaseModel):
    symbol = models.CharField(primary_key=True, max_length=10)
    from_currency = models.ForeignKey(Currency, related_name="from_currency", on_delete=models.CASCADE, max_length=10)
    to_currency = models.ForeignKey(Currency, related_name="to_currency", on_delete=models.CASCADE, max_length=10)

    class Meta:
        db_table = core_entity("currency_pair")
        verbose_name = "Currency Pair"
        verbose_name_plural = "Currency Pairs"
