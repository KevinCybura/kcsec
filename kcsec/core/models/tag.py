from django.db import models

from kcsec.core.models._meta import  core_entity
from kcsec.core.base import BaseModel


class Tag(BaseModel):
    name = models.CharField(primary_key=True, max_length=255)

    class Meta:
        db_table = core_entity("tag")
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
