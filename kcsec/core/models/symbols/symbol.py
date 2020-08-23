from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import  core_entity

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


class Symbol(BaseModel):
    symbol = models.CharField(primary_key=True, max_length=10)
    exchange = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    date = models.DateField()
    is_enabled = models.BooleanField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=5)
    region = models.CharField(max_length=25)
    currency = models.ForeignKey("core.Currency", on_delete=models.DO_NOTHING)
    iex_id = models.CharField(max_length=20)
    figi = models.CharField(max_length=25)
    cik = models.CharField(max_length=20)

    class Meta:
        db_table = core_entity("symbol")
        verbose_name = "Symbol"
        verbose_name_plural = "Symbols"
