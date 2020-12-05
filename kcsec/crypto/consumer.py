import logging

import simplejson as json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class SymbolConsumer(AsyncJsonWebsocketConsumer):
    groups = ["crypto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbols = []

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        self.symbols = content.get("symbols", [])

    async def update_data(self, event):
        message = event["message"]

        if message["symbol"] not in self.symbols:
            return

        to_send = {message["symbol"]: {"ohlcv": message["changes"]}}

        await self.send_json({"message": to_send, "event": "chart"})

    async def update_order_book(self, event):
        message = event["message"]

        if message["symbol"] not in self.symbols:
            return

        to_send = {}

        await self.send_json({"message": to_send, "event": "order_book"})
