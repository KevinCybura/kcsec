import logging
from typing import TYPE_CHECKING

import simplejson as json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.types import TimeFrame

if TYPE_CHECKING:
    from typing import Union

    from django.contrib.auth.models import User

    from kcsec.crypto.types import CandleMessage

logger = logging.getLogger(__name__)


class SymbolConsumer(AsyncJsonWebsocketConsumer):
    groups = ["crypto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.symbols = content.get("symbols", [])

    async def update_data(self, event):
        message: "CandleMessage" = event["message"]

        logger.info(message)

        if message["symbol"] not in self.symbols or message["time_frame"] != TimeFrame.ONE_MINUTE:
            return

        updated_shares = await self.get_updated_share(message["symbol"])
        change = await self.get_24_hour_difference(message)
        to_send = {
            message["symbol"]: {
                "ohlcv": message["changes"],
                "updated_share": updated_shares,
                "24h_change": {"time_frame": message["time_frame"], **change},
            }
        }

        await self.send_json({"message": to_send, "event": "chart"})

    async def update_order_book(self, event):
        message: "CandleMessage" = event["message"]

        if message["symbol"] not in self.symbols or message["time_frame"] != "1m":
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
                return {"total_percent_change": share[0].percent_change}
        return {}

    @database_sync_to_async
    def get_24_hour_difference(self, message: "CandleMessage") -> dict:
        percent_change, price_change = Ohlcv.objects.one_day_difference(
            message["symbol"],
            "gemini",
            TimeFrame.ONE_MINUTE,
            message["changes"][-1]["close"],
        )
        return {"percent_change": percent_change, "price_change": price_change}
