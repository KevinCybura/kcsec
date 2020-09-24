import asyncio
import json
import logging

import websockets
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django_redis import get_redis_connection
from websockets.exceptions import InvalidMessage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Connect to websocket"
    crypto_currencies = ["BTCUSD", "ETHUSD", "LTCUSD"]
    gemini_url = "wss://api.gemini.com/v2/marketdata"
    binance_base = "wss://stream.binance.com:9443/ws/btcusdc@ticker/ws/"
    binance_endpoints = ["btcusdc@ticker"]

    def handle(self, *args, **options) -> None:
        params = {
            "type": "subscribe",
            "subscriptions": [
                {"name": "candles_1m", "symbols": self.crypto_currencies},
                # {"name": "candles_5m", "symbols": self.crypto_currencies},
            ],
        }

        self.redis = get_redis_connection("default")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect(self.gemini_url, params))
        loop.run_forever()

    async def connect(self, url: str, params: dict) -> None:
        async with websockets.connect(url) as ws:
            params = json.dumps(params)
            await ws.send(params)

            async for message in ws:
                await self.handle_message(message)

    async def handle_message(self, message: str) -> None:
        message_dict = json.loads(message)

        if message_dict.get("result") == "error":
            raise InvalidMessage(message)

        logger.info(message)

        channel_layer = get_channel_layer()
        # self.redis.
        await channel_layer.group_send("crypto", {"type": "crypto_update", "message": message})
