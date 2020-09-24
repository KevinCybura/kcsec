import json
import logging
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class CoinConsumer(AsyncJsonWebsocketConsumer):
    coin_cache = [
        "BTCUSD",
        "ETHUSD",
        "LTCUSD",
    ]
    groups = ["crypto"]

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        message = content

        # TODO cache messages in redis.
        coins = {}
        for coin in self.coin_cache:
            if coin in message["coins"]:
                coins[coin] = {}

        await self.send(json.dumps({"message": coins}))

    async def crypto_update(self, event):
        message = json.loads(event["message"])

        if message["type"] == "heartbeat":
            return
        ohlcv = [
            {
                "time": datetime.fromtimestamp(change[0] / 1000).timestamp(),
                "open": change[1],
                "high": change[2],
                "low": change[3],
                "close": change[4],
                "volume": change[5],
                "value": (change[2] + change[3]) / 2,
            }
            for change in message["changes"]
        ]
        ohlcv.reverse()

        to_send = {message["symbol"]: {"ohlcv": ohlcv}}

        await self.send_json({"message": to_send})
