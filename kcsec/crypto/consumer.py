import logging

import simplejson as json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class SymbolConsumer(AsyncJsonWebsocketConsumer):
    groups = ["gemini"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currency_symbol = ""
        self.symbols = []
        self.heartbeat_count = 0

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        self.currency_symbol = content.get("currency_symbol", "USD")
        self.symbols = content.get("symbols", [])

    async def update_data(self, event):
        message = event["message"]

        logger.info(message)
        if not message["symbol"].endswith(self.currency_symbol):
            return

        symbol = message["symbol"].replace(self.currency_symbol, "")
        if symbol not in self.symbols:
            return

        to_send = {symbol: {"ohlcv": message["changes"]}}

        await self.send_json({"message": to_send, "event": "chart"})

    async def update_order_book(self, event):
        message = event["message"]

        if message["symbol"] not in self.symbols:
            return

        to_send = {}

        await self.send_json({"message": to_send, "event": "order_book"})

    async def heartbeat(self, event):
        logger.info(event["message"], extra={"heartbeat_count": self.heartbeat_count})
        self.heartbeat_count += 1
