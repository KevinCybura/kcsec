from django.contrib import admin

from kcsec.crypto.models import CryptoShare


@admin.register(CryptoShare)
class CryptoShareAdmin(admin.ModelAdmin):
    pass
