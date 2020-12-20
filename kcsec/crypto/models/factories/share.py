import factory
from factory.django import DjangoModelFactory

from kcsec.crypto.models import CryptoShare


class CryptoShareFactory(DjangoModelFactory):
    portfolio = factory.SubFactory("kcsec.core.models.factories.portfolio.PortfolioFactory")
    crypto_symbol = factory.SubFactory("kcsec.crypto.models.factories.symbol.SymbolFactory")
    shares = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    average_price = factory.LazyAttribute(lambda o: o.crypto_symbol.price)
    percent_change = 0.0

    class Meta:
        model = CryptoShare
