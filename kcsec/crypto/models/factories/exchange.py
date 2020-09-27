from factory.django import DjangoModelFactory
from factory.faker import Faker

from kcsec.crypto.models import Exchange


class ExchangeFactory(DjangoModelFactory):
    exchange_id = Faker("pystr")
    website = Faker("url")
    name = Faker("name")

    class Meta:
        model = Exchange
