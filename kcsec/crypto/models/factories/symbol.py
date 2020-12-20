from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker

from kcsec.crypto.models import Symbol
from kcsec.crypto.models.factories.asset import AssetFactory
from kcsec.crypto.models.factories.exchange import ExchangeFactory


class SymbolFactory(DjangoModelFactory):
    symbol_id = Faker("pystr")
    asset_id_base = SubFactory(AssetFactory)
    asset_id_quote = SubFactory(AssetFactory)
    exchange = SubFactory(ExchangeFactory)
    price = Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)

    class Meta:
        model = Symbol
