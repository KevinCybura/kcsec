import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    username = factory.Faker("user_name")
    email = factory.Faker("last_name")

    class Meta:
        model = User
