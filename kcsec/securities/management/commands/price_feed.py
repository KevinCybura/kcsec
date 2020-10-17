import asyncio
import json
import logging
from datetime import datetime
from typing import Dict
from typing import List
from urllib.parse import urlencode

import websockets
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from websockets.exceptions import InvalidMessage

from kcsec.crypto.models import Ohlcv

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Connect to websocket"
    candle_stick_url = "wss://api.gemini.com/v2/marketdata"

    def handle(self, *args, **options) -> None:
        params = {}

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect(self.candle_stick_url, params))
        loop.run_forever()

    async def connect(self, url: str, params: dict = None) -> None:
        async with websockets.connect(url) as ws:
            if params is not None:
                params = json.dumps(params)
                await ws.send(params)

            async for message in ws:
                await self.handle_message(message)

    async def handle_message(self, message: str) -> None:
        message_dict = json.loads(message)

        logger.info(message)
        if message_dict.get("result") == "error":
            raise InvalidMessage(message)

        if message_dict["type"] == "heartbeat":
            return

        message_dict["changes"] = self._convert(message_dict["changes"])

        await self._store_ohlcv(message_dict, exchange_id="gemini")

        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "securities", {"type": "securities_chart_data", "message": json.dumps(message_dict)}
        )

    @classmethod
    def _convert(cls, changes: List[List[float]]) -> List[Dict]:
        pass

    @database_sync_to_async
    def _store_ohlcv(self, message: Dict[str, dict], exchange_id: str = "gemini") -> None:
        pass
