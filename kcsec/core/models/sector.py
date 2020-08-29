from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import core_entity


class Sector(BaseModel):
    name = models.CharField(primary_key=True, max_length=255)

    class Meta:
        db_table = core_entity("sector")
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
