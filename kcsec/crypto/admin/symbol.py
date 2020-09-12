from django.contrib import admin

from kcsec.crypto.models import Symbol


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Symbol._meta.get_fields()]
