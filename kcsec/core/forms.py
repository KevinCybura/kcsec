from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from kcsec.core.models import Portfolio


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="User name")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username", "first_name", "last_name")

    def save(self, commit=True):
        if not commit:
            raise ValueError("Must save user to db to create profile")
        user = super().save(commit=True)
        Portfolio.objects.create(user=user, balance=50000)
        return user
