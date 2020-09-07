from django.contrib import admin

from kcsec.crypto.models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    pass
