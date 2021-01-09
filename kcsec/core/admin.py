from django.contrib import admin

from kcsec.core.models import Portfolio

# Register your models here.


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass
