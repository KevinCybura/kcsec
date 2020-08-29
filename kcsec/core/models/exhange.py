from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import core_entity


class InternationalExchange(BaseModel):
    exchange = models.CharField(primary_key=True, max_length=20)
    region = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    mic = models.CharField(max_length=10)
    exchange_suffix = models.CharField(max_length=10)

    class Meta:
        db_table = core_entity("international_exchange")
        verbose_name = "International Exchange"
        verbose_name_plural = "International Exchanges"


class UsExchange(BaseModel):
    name = models.CharField(primary_key=True, max_length=20)
    long_name = models.CharField(max_length=255)
    mic = models.CharField(max_length=10)
    tape_id = models.CharField(max_length=10)
    oats_id = models.CharField(max_length=10)
    ref_id = models.CharField(max_length=10)
    type = models.CharField(max_length=10)

    class Meta:
        db_table = core_entity("us_exchange")
        verbose_name = "US Exchange"
        verbose_name_plural = "US Exchanges"
