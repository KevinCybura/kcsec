import logging
from typing import TYPE_CHECKING

import simplejson as json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from kcsec.crypto.models import CryptoShare

if TYPE_CHECKING:
    from typing import Union

    from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class SymbolConsumer(AsyncJsonWebsocketConsumer):
    groups = ["gemini"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currency_symbol: str = ""
        self.symbols: list[str] = []
        self.heartbeat_count: int = 0
        self.user: "Union[User, AnonymousUser]" = AnonymousUser()

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)

    async def connect(self):
        self.user = self.scope.get("user")
        await self.accept()

    async def receive_json(self, content, **kwargs):
        self.currency_symbol = content.get("currency_symbol", "USD")
        self.symbols = content.get("symbols", [])

    async def update_data(self, event):
        message = event["message"]

        logger.info(message)
        if not message["symbol"].endswith(self.currency_symbol):
            return

        if message["symbol"] not in self.symbols:
            return

        to_send = {
            message["symbol"]: {
                "ohlcv": message["changes"],
                "updated_share": await self.get_updated_share(message["symbol"]),
            }
        }

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

    @database_sync_to_async
    def get_updated_share(self, symbol: str) -> dict:
        if self.user.is_authenticated:
            share = CryptoShare.objects.filter(crypto_symbol=symbol, portfolio__user=self.user)
            if share.exists():
                return {"percent_change": share[0].percent_change}
        return {}
