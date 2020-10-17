import asyncio
import logging

from django.core.management.base import BaseCommand

from kcsec.crypto.client import Consumer
from kcsec.crypto.client import connections

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Connect to websocket"

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(*[self.connect(uri, consumer) for uri, consumer in connections]))
        except Exception as e:
            logger.error(f"Stopping event loop received error {e}")
            loop.stop()

    @staticmethod
    async def connect(url: str, consumer: Consumer.__class__):
        async with await consumer.connect(url) as consumer:
            async for message in consumer.ws:
                await consumer.handle_message(message)
