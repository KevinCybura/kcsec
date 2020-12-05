from django.db import models

from kcsec.core.base import BaseModel
from kcsec.core.models._meta import core_entity


class Portfolio(BaseModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=4, null=True)
    margin = models.DecimalField(max_digits=15, decimal_places=4, null=True)

    class Meta:
        db_table = core_entity("portfolio")
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"
