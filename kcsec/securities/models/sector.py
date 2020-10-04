from django.db import models

from kcsec.core.base import BaseModel
from kcsec.securities.models._meta import securities_entity


class Sector(BaseModel):
    name = models.CharField(primary_key=True, max_length=255)

    class Meta:
        db_table = securities_entity("sector")
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
