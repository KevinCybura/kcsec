from django.urls import path

from kcsec.crypto.views import index

urlpatterns = [path("", index, name="index")]
