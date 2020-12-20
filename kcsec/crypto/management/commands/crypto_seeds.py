from django.core.management.base import BaseCommand

from kcsec.crypto.management.seeds import crypto_seed


class Command(BaseCommand):
    help = "Connect to websocket"
    crypto_currencies = ["BTC", "ETH", "LTC"]

    def handle(self, *args, **options) -> None:
        crypto_seed(self.crypto_currencies)
