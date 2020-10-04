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
    crypto_currencies = ["BTCUSD", "ETHUSD", "LTCUSD"]
    l1_data = "wss://api.gemini.com/{version}/marketdata/{symbol}"
    candle_stick_url = "wss://api.gemini.com/v2/marketdata"

    def handle(self, *args, **options) -> None:
        params = {
            "type": "subscribe",
            "subscriptions": [
                {"name": "candles_1m", "symbols": self.crypto_currencies},
                # {"name": "candles_5m", "symbols": self.crypto_currencies},
            ],
        }

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
        await channel_layer.group_send("crypto", {"type": "crypto_update", "message": json.dumps(message_dict)})

    @classmethod
    def _convert(cls, changes: List[List[float]]) -> List[Dict]:
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
    def _store_ohlcv(self, message: Dict[str, dict], exchange_id: str = "gemini") -> None:
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

