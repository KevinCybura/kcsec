import factory
from factory.django import DjangoModelFactory

from kcsec.crypto.models import CryptoOrder


class CryptoOrderFactory(DjangoModelFactory):
    symbol = factory.SubFactory("kcsec.crypto.models.factories.symbol.SymbolFactory")
    share = factory.SubFactory("kcsec.crypto.models.factories.share.CryptoShare")
    portfolio = factory.SubFactory("kcsec.core.models.factories.portfolio.PortfolioFactory")
    price = factory.LazyAttribute(lambda o: o.symbol.price)
    shares = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    filled = True
    trade_type = "buy"
    order_type = "market_order"

    class Meta:
        model = CryptoOrder
