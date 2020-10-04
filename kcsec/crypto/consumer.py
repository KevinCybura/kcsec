import logging

import simplejson as json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class CoinConsumer(AsyncJsonWebsocketConsumer):
    coin_cache = [
        "BTCUSD",
        "ETHUSD",
        "LTCUSD",
    ]
    groups = ["crypto"]

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)

    async def connect(self):
        await self.accept()

    async def crypto_update(self, event):
        message = json.loads(event["message"])

        if message["type"] == "heartbeat":
            return

        to_send = {message["symbol"]: {"ohlcv": message["changes"]}}

        await self.send_json({"message": to_send})
