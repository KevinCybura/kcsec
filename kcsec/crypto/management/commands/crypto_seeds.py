import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from kcsec.crypto.seeds import crypto_seed

logger = logging.Logger(__name__)


class Command(BaseCommand):
    help = "Connect to websocket"
    crypto_currencies = ["BTC", "ETH", "LTC"]

    def handle(self, *args, **options) -> None:
        print("Running crypto_seeds")
        try:
            crypto_seed(self.crypto_currencies)
        except IntegrityError:
            print("Seeds already run")
        print("Finished crypto_seeds")
