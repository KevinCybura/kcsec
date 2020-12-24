import datetime
import logging
from decimal import Decimal
from typing import TYPE_CHECKING

import simplejson as json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import CryptoTemplateContext
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
        def default(o):
            if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()

        return json.dumps(content, default=default)

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

        data = await self.get_updated_share(message)
        to_send = {"symbol": message["symbol"], "ohlcv": message["changes"], **data}

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
    def get_updated_share(self, message: "CandleMessage") -> CryptoTemplateContext.data:
        midnight_price = Ohlcv.objects.filter_after_midnight(
            message["symbol"], exchange="gemini", time_frame="1m", delta=datetime.timedelta(hours=5)
        ).earliest()

        return CryptoTemplateContext(
            instance=dict(
                symbol=message["symbol"],
                user=self.user,
                price=Decimal(message["changes"][-1]["close"]),
                midnight_price=midnight_price.open,
                update=True,
            )
        ).data
