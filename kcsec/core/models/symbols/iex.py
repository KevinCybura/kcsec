from django.db import models
from kcsec.core.base import BaseModel
from kcsec.core.models._meta import  core_entity

class IexSymbol(BaseModel):
    symbol = models.OneToOneField("core.Symbol", on_delete=models.DO_NOTHING, primary_key=True)
    date = models.DateField()
    is_enabled = models.BooleanField()

    class Meta:
        db_table = core_entity("iex_symbol")
        verbose_name = "Iex supported symbol"
        verbose_name_plural = "Iex supported symbols"
