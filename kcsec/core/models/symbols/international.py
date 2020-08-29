from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import core_entity

TYPE_CHOICES = [
    ("ad", "ad"),
    ("re", "re"),
    ("ce", "ce"),
    ("si", "si"),
    ("lp", "lp"),
    ("cs", "cs"),
    ("et", "et"),
    ("wt", "wt"),
    ("oef", "oef"),
    ("cef", "cef"),
    ("ps", "ps"),
    ("ut", "ut"),
    ("temp", "temp"),
]


class InternationalSymbol(BaseModel):
    symbol = models.CharField(primary_key=True, max_length=10)
    exchange = models.ForeignKey("core.InternationalExchange", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    is_enabled = models.BooleanField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=5)
    region = models.CharField(max_length=20)
    currency = models.ForeignKey("core.Currency", on_delete=models.CASCADE)
    iex_id = models.CharField(max_length=25)

    class Meta:
        db_table = core_entity("international_symbol")
        verbose_name = "International Symbol"
        verbose_name_plural = "International Symbols"
