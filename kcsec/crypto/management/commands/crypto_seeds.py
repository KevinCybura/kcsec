import logging

from django.core.management.base import BaseCommand

from kcsec.crypto.models.factories.asset import AssetFactory
from kcsec.crypto.models.factories.exchange import ExchangeFactory
from kcsec.crypto.views import CoinView

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Connect to websocket"
    crypto_currencies = ["BTC", "ETH", "LTC"]

    def handle(self, *args, **options) -> None:
        ExchangeFactory(exchange_id="gemini")
        AssetFactory(asset_id="USD")
        for coin in self.crypto_currencies:
            AssetFactory(asset_id=coin)
