from django.db import models

from kcsec.core.base import BaseModel
from kcsec.securities.models._meta import securities_entity

TYPE_CHOICES = [
    ("ad", "ad"),
    ("re", "re"),
    ("ce", "ce"),
    ("si", "si"),
    ("lp", "lp"),
    ("cs", "cs"),
    ("et", "et"),
    ("wt", "wt"),
]


class Otc(BaseModel):
    symbol = models.OneToOneField("securities.Symbol", on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=3)
    region = models.CharField(max_length=25)
    currency = models.ForeignKey("securities.Currency", on_delete=models.CASCADE)
    iex_id = models.CharField(max_length=20)

    class Meta:
        db_table = securities_entity("otc")
        verbose_name = "OTC symbol"
        verbose_name_plural = "OTC symbols"
