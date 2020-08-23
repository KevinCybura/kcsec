from django.contrib.postgres.fields import ArrayField
from django.db import models

from kcsec.core.models._meta import  core_entity
from kcsec.core.base import BaseModel


class Option(BaseModel):
    symbol = models.OneToOneField("core.Symbol", on_delete=models.CASCADE, primary_key=True)
    dates = ArrayField(models.DateField())

    class Meta:
        db_table = core_entity("option")
        verbose_name = "Option"
        verbose_name_plural = "Options"
