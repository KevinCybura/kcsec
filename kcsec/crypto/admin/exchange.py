from django.contrib import admin

from kcsec.crypto.models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Exchange._meta.get_fields()]
