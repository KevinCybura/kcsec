import json
import logging
from typing import TYPE_CHECKING

import websockets
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.db.models import Q
from websockets.exceptions import InvalidMessage

from kcsec.crypto.client import Consumer
from kcsec.crypto.client.order_book import OrderBook
from kcsec.crypto.models import CryptoOrder
from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.models import Symbol
from kcsec.crypto.types import TimeFrame

if TYPE_CHECKING:
    from typing import Awaitable

    from kcsec.crypto.client.order_book import L2Message
    from kcsec.crypto.types import CandleMessage
    from kcsec.crypto.types import Change
    from kcsec.crypto.types import MessageChanges

logger = logging.getLogger(__name__)


class GeminiConsumer(Consumer):
    crypto_currencies = ["BTCUSD", "ETHUSD", "LTCUSD"]
    gemini_subscriptions = [
        {"name": "candles_1m", "symbols": crypto_currencies},
        # {"name": "candles_5m", "symbols": crypto_currencies},
        # {"name": "candles_15m", "symbols": crypto_currencies},
        # {"name": "candles_30m", "symbols": crypto_currencies},
        # {"name": "candles_1h", "symbols": crypto_currencies},
        # {"name": "candles_6h", "symbols": crypto_currencies},
        # {"name": "candles_1d", "symbols": crypto_currencies},
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
            logger.error(message)
            raise InvalidMessage(message)

        if message["type"] == "heartbeat":
            await self.channel_layer.group_send("crypto", {"type": "heartbeat", "message": message})

        # type = "candle_<time_frame>_updates.
        if "candles" == message["type"].split("_")[0]:
            await self.handle_candle_updates(message)
        elif message["type"] == "l2_updates":
            await self.handle_l2_updates(message)

    async def handle_candle_updates(self, message: "CandleMessage"):
        message["changes"] = self.convert(message["changes"])

        message["time_frame"] = TimeFrame(message["type"].split("_")[1])
        await self.store_ohlcv(message)

        if message["time_frame"] == TimeFrame.ONE_MINUTE:
            await self.update_symbol(message)

        logger.info(message)
        await self.fill_orders(message)
        logger.info("Attempt to fill unfilled orders.")
        await self.channel_layer.group_send("crypto", {"type": "update_data", "message": message})

    async def handle_l2_updates(self, message: "L2Message"):
        if not self.order_book.get(message["symbol"]):
            self.order_book[message["symbol"]] = OrderBook(message["symbol"])

        if not message["type"] == "l2_updates":
            order_book = self.order_book.get(message["symbol"])

            await order_book.handle_message(message)

            await self.channel_layer.group_send(
                "crypto", {"type": "update.order_book", "message": order_book.order_book}
            )

    @database_sync_to_async
    def fill_orders(self, message: "CandleMessage"):
        price = message["changes"][-1]["close"]
        filter_not_ready_orders = (Q(trade_type=CryptoOrder.TradeType.BUY) & Q(price__gte=price)) | (
            Q(trade_type=CryptoOrder.TradeType.SELL) & Q(price__lte=price)
        )
        unfilled_orders = CryptoOrder.objects.filter(filter_not_ready_orders, symbol=message["symbol"], filled=False)

        shares = []
        for order in unfilled_orders:
            order.price = price
            order.filled = True
            if order.share:
                share, _ = CryptoShare.objects.execute_order(order, save=False)
                share.price = price
                share.cryptoorder_set.add(order)
                shares.append(share)

            else:
                # TODO: when an order is created create a empty share for the user so we dont have to handle this case.
                share, _ = CryptoShare.objects.execute_order(order)
                order.share = share

        CryptoShare.objects.bulk_update(shares, ["average_price", "shares"])
        CryptoOrder.objects.bulk_update(unfilled_orders, ["share", "filled"])

    @classmethod
    def convert(cls, changes: "MessageChanges") -> list["Change"]:
        def map_changes(change: list[float]):
            change[0] /= 1000
            change.append((change[2] + change[3]) / 2)
            return change

        keys = ["time", "open", "high", "low", "close", "volume", "value"]
        return [{k: v for k, v in zip(keys, change)} for change in map(map_changes, changes)]

    @database_sync_to_async
    def store_ohlcv(self, message: "CandleMessage", exchange: str = "gemini") -> "Awaitable[int]":
        return Ohlcv.objects.bulk_create_from_message(message, exchange)

    @database_sync_to_async
    def update_symbol(self, message: "CandleMessage", exchange: str = "gemini"):
        symbol = Symbol.objects.get(pk=message["symbol"], exchange=exchange)
        symbol.price = message["changes"][-1]["close"]
        symbol.save()
