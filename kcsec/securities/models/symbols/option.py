from django.contrib.postgres.fields import ArrayField
from django.db import models

from kcsec.core.base import BaseModel
from kcsec.securities.models._meta import securities_entity


class Option(BaseModel):
    symbol = models.OneToOneField("securities.Symbol", on_delete=models.CASCADE, primary_key=True)
    dates = ArrayField(models.DateField())

    class Meta:
        db_table = securities_entity("option")
        verbose_name = "Option"
        verbose_name_plural = "Options"
