from asyncio import Lock
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    from typing import TypedDict

    class ChangeEvent(TypedDict):
        type: Literal["change", "trade", "auction", "block_trade"]
        price: float
        side: Literal["bid", "ask"]
        reason: Literal["place", "trade", "cancel", "initial"]
        remaining: float
        delta: float


class OrderBook:
    def __init__(self, symbol):
        self.symbol = symbol
        self.asks = {}
        self.bids = {}
        self.ohlcv = []
        self.lock = Lock()
        self.high = None
        self.low = None
        self.open = None
        self.close = None
        self.volume = 0
        self.last_time = None

    async def handle_message(self, message: dict) -> None:
        async for event in message["events"]:
            if event["type"] == "change":
                await self.update(event)

    async def update(self, event: "ChangeEvent") -> None:
        async with self.lock:
            self.open = max(self.open, event["price"]) if self.open else event["price"]
            self.low = min(self.low, event["price"]) if self.low else event["price"]
            self.volume += abs(event["delta"])


class Ask:
    pass


class Bid:
    pass


@dataclass
class Ohlc:
    open: float
    high: float
    low: float
    close: float
    volume: int
