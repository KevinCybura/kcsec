from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from kcsec.core.forms import RegisterForm

# Create your views here.


def home(request):
    return redirect(reverse_lazy("crypto"))


class UserAuthView(CreateView):
    form_class = RegisterForm
    initial = {}
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
