from django.urls import path

from kcsec.crypto import views

urlpatterns = [
    path("", views.CoinView.as_view(), name="coin"),
    path("<str:coin>", views.CoinView.as_view(), name="coin"),
]
