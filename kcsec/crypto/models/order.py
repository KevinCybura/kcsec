from django.db import models
from django.utils.translation import gettext_lazy as _

from kcsec.core.base import BaseModel
from kcsec.crypto.models._meta import crypto_entity


class CryptoOrder(BaseModel):
    class TradeType(models.TextChoices):
        BUY = "buy"
        SELL = "sell"

    class OrderType(models.TextChoices):
        MARKET = "market_order", _("Market Order")
        LIMIT = "limit_order", _("Limit Order")

    crypto_symbol = models.ForeignKey("crypto.Symbol", on_delete=models.DO_NOTHING)
    share = models.ForeignKey("crypto.CryptoShare", on_delete=models.DO_NOTHING, null=True)
    portfolio = models.ForeignKey("core.Portfolio", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    shares = models.DecimalField(max_digits=15, decimal_places=5)
    filled = models.BooleanField(default=False)
    trade_type = models.CharField(choices=TradeType.choices, max_length=5, default=TradeType.BUY)
    order_type = models.CharField(choices=OrderType.choices, max_length=20, default=OrderType.MARKET)

    class Meta:
        db_table = crypto_entity("order")
        verbose_name = "Crypto currency order"
        verbose_name_plural = "Crypto currency order"
