from django.urls import re_path

from kcsec.crypto.consumer import SymbolConsumer

websocket_urlpatterns = [re_path(r"ws/crypto/", SymbolConsumer)]
