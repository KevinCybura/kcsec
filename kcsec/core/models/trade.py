from django.db import models

from kcsec.core.base import BaseModel


class Trade(BaseModel):
    symbol = models.OneToOneField("securities.Symbol", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    size = models.DecimalField(max_digits=20, decimal_places=5)
    odd_lot = models.BooleanField()
    iso = models.BooleanField()
    out_side_regular_hours = models.BooleanField()
    single_price_cross = models.BooleanField()
    trade_through_exempt = models.BooleanField()

    class Meta:
        abstract = True
        verbose_name = None
        verbose_name_plural = None


class Order(BaseModel):
    class BidAsk(models.IntegerChoices):
        BID = 0, "bid"
        ASK = 1, "ask"

    symbol = models.OneToOneField("securities.Symbol", on_delete=models.DO_NOTHING)
    bid_ask = models.IntegerField(choices=BidAsk.choices)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    size = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        abstract = True
        verbose_name = None
        verbose_name_plural = None


class Ask(BaseModel):
    symbol = models.ForeignKey("securities.Symbol", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    size = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        unique_together = ("symbol", "price")
        verbose_name = "Order book ask"
        verbose_name_plural = "Order book asks"


class Bid(BaseModel):
    symbol = models.ForeignKey("securities.Symbol", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    size = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        unique_together = ("symbol", "price")
        verbose_name = "Order book bid"
        verbose_name_plural = "Order book bis"
