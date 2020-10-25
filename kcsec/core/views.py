from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView

from kcsec.core.forms import RegisterForm

# Create your views here.


def home(request):
    count = User.objects.count()
    return render(request, "core/home.html", {"count": count})


class UserAuthView(CreateView):
    form_class = RegisterForm
    initial = {}
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")


@login_required
def secret_page(request):
    return render(request, "core/secret_page.html")


class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = "core/secret_page.html"
