import json
import logging
from datetime import datetime

import websockets
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.utils.timezone import utc
from websockets.exceptions import InvalidMessage

from kcsec.crypto.client import Consumer
from kcsec.crypto.client.order_book import OrderBook
from kcsec.crypto.models import Ohlcv

logger = logging.getLogger(__name__)


class GeminiConsumer(Consumer):
    crypto_currencies = ["BTCUSD", "ETHUSD", "LTCUSD"]
    gemini_subscriptions = [
        {"name": "candles_1m", "symbols": crypto_currencies},
        {"name": "l2", "symbols": crypto_currencies},
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_layer = get_channel_layer()
        self.order_book: dict[str, OrderBook] = {}

    @classmethod
    async def connect(cls, url: str) -> Consumer:
        ws = await websockets.connect(url)
        return cls(ws)

    async def unsubscribe(self):
        logger.info("Unsubscribing from gemini")
        try:
            await self.conn.send(json.dumps({"type": "unsubscribe", "subscriptions": self.gemini_subscriptions}))
        except websockets.ConnectionClosedError as e:
            if e.code == 1006:
                logger.info("Received connection closed error, successfully unsubscribed from gemini")
            else:
                raise e

    async def subscribe(self, *args, **kwargs):
        logger.info("Subscribing to gemini")
        await self.conn.send(json.dumps({"type": "subscribe", "subscriptions": self.gemini_subscriptions}))

    async def handle_message(self, message: str):
        message = json.loads(message)

        if message.get("result") == "error":
            raise InvalidMessage(message)

        if message["type"] == "heartbeat":
            await self.channel_layer.group_send("gemini", {"type": "heartbeat", "message": message})

        if message["type"] == "candles_1m_updates":
            await self.handle_candle_data(message)
        elif message["type"] == "l2_updates":
            await self.handle_l2_updates(message)

    async def handle_candle_data(self, message: dict):
        message["changes"] = self.convert(message["changes"])

        await self.store_ohlcv(message, exchange_id="gemini")

        logger.info(message)
        await self.channel_layer.group_send("gemini", {"type": "update_data", "message": message})

    async def handle_l2_updates(self, message: dict):
        if not self.order_book.get(message["symbol"]):
            self.order_book[message["symbol"]] = OrderBook(message["symbol"])

        if not message["type"] == "l2_updates":
            order_book = self.order_book.get(message["symbol"])

            await order_book.handle_message(message)

            await self.channel_layer.group_send(
                "gemini", {"type": "update.order_book", "message": order_book.order_book}
            )

    @classmethod
    def convert(cls, changes: list[list[float]]) -> list[dict]:
        return [
            {
                "time": change[0] / 1000,
                "open": change[1],
                "high": change[2],
                "low": change[3],
                "close": change[4],
                "volume": change[5],
                "value": (change[2] + change[3]) / 2,
            }
            for change in changes[::-1]
        ]

    @database_sync_to_async
    def store_ohlcv(self, message: dict[str, dict], exchange_id: str = "gemini"):
        objs = [
            Ohlcv(
                exchange_id=exchange_id,
                asset_id_base_id=message["symbol"][:3],
                asset_id_quote_id=message["symbol"][3:],
                time_open=datetime.fromtimestamp(change["time"], tz=utc),
                open=change["open"],
                high=change["high"],
                low=change["low"],
                close=change["close"],
                volume=change["volume"],
            )
            for change in message["changes"]
        ]
        Ohlcv.objects.bulk_create(objs, ignore_conflicts=True)
