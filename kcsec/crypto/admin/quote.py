from django.contrib import admin

from kcsec.crypto.models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    pass
