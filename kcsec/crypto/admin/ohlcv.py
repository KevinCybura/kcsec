from django.contrib import admin

from kcsec.crypto.models import Ohlcv


@admin.register(Ohlcv)
class OhlcvAdmin(admin.ModelAdmin):
    pass
