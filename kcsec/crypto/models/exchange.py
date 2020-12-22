from django.db import models

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class Exchange(BaseModel):
    exchange_id = models.CharField(max_length=60, unique=True, primary_key=True)
    website = models.URLField()
    name = models.CharField(max_length=60)
    data_start = models.DateField(null=True)
    exchange_icon = models.ImageField(upload_to="images/crypto/", height_field=48, width_field=48, null=True)

    class Meta:
        db_table = crypto_entity("exchange")
        verbose_name = "Crypto currency exchange"
        verbose_name_plural = "Crypto currency exchanges"
