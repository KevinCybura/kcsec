from django.urls import re_path

from kcsec.crypto.channels.gemini import SymbolConsumer

websocket_urlpatterns = [re_path(r"ws/crypto/", SymbolConsumer.as_asgi())]
