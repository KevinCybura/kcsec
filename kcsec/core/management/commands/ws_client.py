import asyncio
import logging
from typing import TYPE_CHECKING

from django.core.management.base import BaseCommand

from kcsec.crypto.client import connections

if TYPE_CHECKING:
    from kcsec.crypto.client import Consumer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Connect to websocket"

    def handle(self, *args, **options):
        try:
            asyncio.run(self.main())
        except BaseException as e:
            logger.error(f"Received error {e}")

    @staticmethod
    async def connect(url: str, consumer: "Consumer.__class__"):
        async with await consumer.connect(url) as consumer:
            async for message in consumer.conn:
                await consumer.handle_message(message)

    async def main(self):
        return await asyncio.gather(*[self.connect(*conn) for conn in connections])
