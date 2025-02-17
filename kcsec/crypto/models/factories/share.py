import factory
from factory.django import DjangoModelFactory

from kcsec.crypto.models import CryptoShare


class CryptoShareFactory(DjangoModelFactory):
    portfolio = factory.SubFactory("kcsec.core.models.factories.portfolio.PortfolioFactory")
    symbol = factory.SubFactory("kcsec.crypto.models.factories.symbol.SymbolFactory")
    shares = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    average_price = factory.LazyAttribute(lambda o: o.symbol.price)

    class Meta:
        model = CryptoShare
