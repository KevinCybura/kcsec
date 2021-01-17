from django.contrib import admin

from kcsec.crypto.models import CryptoOrder


@admin.register(CryptoOrder)
class CryptoOrderAdmin(admin.ModelAdmin):
    pass
