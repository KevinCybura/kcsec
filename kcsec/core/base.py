from django.db import models
from psqlextra.manager import PostgresManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)

    objects = PostgresManager()

    class Meta:
        abstract = True

