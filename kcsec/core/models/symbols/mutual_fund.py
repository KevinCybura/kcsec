from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import  core_entity

TYPE_CHOICES = [("oef", "oef"), ("cef", "cef")]


class MutualFundSymbol(BaseModel):
    symbol = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=255)
    date = models.DateField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=4)
    region = models.CharField(max_length=20)
    currency = models.ForeignKey("core.Currency", on_delete=models.CASCADE)
    iex_id = models.CharField(max_length=25)

    class Meta:
        db_table = core_entity("mutual_fund_symbol")
        verbose_name = "Mutual Fund Symbol"
        verbose_name_plural = "Mutual Fund Symbols"
