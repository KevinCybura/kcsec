from django.contrib import admin

from kcsec.crypto.models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass
