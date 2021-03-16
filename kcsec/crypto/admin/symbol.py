from django.contrib import admin

from kcsec.crypto.models import Symbol


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    pass
