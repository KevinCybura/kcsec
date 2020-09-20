import json
import logging
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class CoinConsumer(AsyncJsonWebsocketConsumer):
    coin_cache = {
        "BTCUSD": {"messages": []},
        "ETHUSD": {"messages": []},
        "LTCUSD": {"messages": []},
    }
    groups = ["crypto"]

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        message = content
        # logger.info(content)

        coins = {}
        logger.info("HERE")
        for coin, data in self.coin_cache.items():
            if coin in message["coins"]:
                coins[coin] = data.get("ohlcv", [])

        await self.send(json.dumps({"message": coins}))

    async def crypto_update(self, event):
        message = json.loads(event["message"])

        # logger.info(message)
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

        if isinstance(ohlcv, list):
            self.coin_cache[message["symbol"]]["ohlcv"] = ohlcv
        else:
            self.coin_cache[message["symbol"]]["ohlcv"].append(ohlcv)
        self.coin_cache[message["symbol"]]["messages"].append(message)

        # ohlcv =  [{'time': 1600550160, 'open': 11087, 'high': 11087, 'low': 11087, 'close': 11087, 'volume': 0}]
        to_send = {message["symbol"]: {"ohlcv": ohlcv}}
        print(to_send)

        await self.send_json({"message": to_send})
