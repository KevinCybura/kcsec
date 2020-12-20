import factory
from factory.django import DjangoModelFactory

from kcsec.core.models import Portfolio


class PortfolioFactory(DjangoModelFactory):
    user = factory.SubFactory("kcsec.core.models.factories.user.UserFactory")
    balance = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)
    margin = factory.Faker("pydecimal", left_digits=10, right_digits=4, positive=True, min_value=0.0)

    class Meta:
        model = Portfolio
