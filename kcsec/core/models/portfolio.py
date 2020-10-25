from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import core_entity


class Portfolio(BaseModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)

    class Meta:
        db_table = core_entity("portfolio")
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"
