import logging

from django.core.management.base import BaseCommand

from kcsec.crypto.models.factories.asset import AssetFactory
from kcsec.crypto.models.factories.exchange import ExchangeFactory
from kcsec.crypto.models.factories.symbol import SymbolFactory

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Connect to websocket"
    crypto_currencies = ["BTC", "ETH", "LTC"]

    def handle(self, *args, **options) -> None:
        exchange = ExchangeFactory(exchange_id="gemini")
        usd = AssetFactory(asset_id="USD")
        for coin in self.crypto_currencies:
            SymbolFactory(
                symbol_id=coin, asset_id_base=AssetFactory(asset_id=coin), asset_id_quote=usd, exchange=exchange
            )
