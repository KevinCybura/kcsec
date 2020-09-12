from django.contrib import admin
from django.utils.html import mark_safe

from kcsec.crypto.models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ["asset_id", "icon", "price_usd"]
    search_fields = ["asset_id"]
    readonly_fields = ["icon"]
