from factory.django import DjangoModelFactory
from factory.faker import Faker

from kcsec.crypto.models import Asset


class AssetFactory(DjangoModelFactory):
    asset_id = Faker("pystr")

    class Meta:
        model = Asset
