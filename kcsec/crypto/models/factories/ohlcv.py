from datetime import datetime
from datetime import timedelta

import factory
from factory.django import DjangoModelFactory

from kcsec.crypto.models import Ohlcv


class OhlcvFactory(DjangoModelFactory):
    exchange = factory.SubFactory("kcsec.crypto.models.factories.exchange.ExchangeFactory")
    asset_id_base = factory.SubFactory("kcsec.crypto.models.factories.asset.AssetFactory")
    asset_id_quote = factory.SubFactory("kcsec.crypto.models.factories.asset.AssetFactory")
    open = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    high = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    low = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    close = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    volume = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    trades_count = factory.Faker("pyint")

    class Meta:
        model = Ohlcv

    @factory.sequence
    def time_open(n):
        try:
            return Ohlcv.objects.latest("time_open").time_open + timedelta(minutes=float(n))
        except Ohlcv.DoesNotExist:
            return datetime.now()
