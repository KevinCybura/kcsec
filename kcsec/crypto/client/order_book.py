import logging
import time
from asyncio import Lock
from dataclasses import asdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict
    from typing import List
    from typing import Literal
    from typing import TypedDict
    from typing import Union

    Change = List[Literal["buy", "sell"], float, float]

    class L2Update(TypedDict):
        type: Literal["l2_update"]
        symbol: str
        changes: List[Change]

    class L2Trade(TypedDict):
        type: Literal["trade"]
        symbol: str
        event_id: int
        timestamp: int
        price: float
        quantity: float
        side: Literal["buy", "sell"]

    class L2Auction(TypedDict):
        type: Literal["auction_result", "auction_indicative"]
        symbol: str
        time_ms: int
        result: Literal["success", "failure"]
        highest_bid_price: float
        highest_ask_price: float
        collar_price: float
        auction_price: float
        auction_quantity: float

    L2Initial = Dict[L2Update, L2Auction, List[L2Trade]]
    L2Message = Union[L2Trade, L2Auction, L2Update, L2Initial]

logger = logging.getLogger(__name__)


class OrderBook:
    @dataclass
    class _Ohlc:
        open: float
        high: float
        low: float
        close: float
        volume: int
        time: float
        value: float = None

        def __post_init__(self):
            self.value = (self.high + self.low) / 2

    def __init__(self, symbol):
        self.symbol: str = symbol
        self.asks = {}
        self.bids = {}
        self.best_bid = None
        self.best_ask = None
        self.ohlcv = []
        self.high = None
        self.low = None
        self.open = None
        self.close = None
        self.volume = 0
        self.last_time = None
        self.lock = Lock()
        self.trades_made = 0
        self.minute = 0

    async def handle_message(self, message: "L2Message"):
        if message["type"] == "l2_updates" and message.get("trades"):
            await self.l2_update(message)
            for trade in message["trades"]:
                await self.l2_trade(trade)

            for event in message["auction_events"]:
                await self.l2_auction(event)

        elif message["type"] == "l2_updates":
            await self.l2_update(message)
        elif message["type"] == "trade":
            await self.l2_trade(message)
        elif message["type"] == "auction":
            await self.l2_auction(message)

    async def l2_update(self, event: "L2Update"):
        async with self.lock:
            for change in event["changes"]:
                if change[0] == "buy":
                    self.bids[change[1]] = change[2]
                    self.best_bid = max(self.best_bid, change[1]) if self.best_bid else change[1]
                elif change[0] == "sell":
                    self.asks[change[1]] = change[2]
                    self.best_ask = min(self.best_ask, change[1]) if self.best_ask else change[1]

    async def l2_trade(self, event: "L2Trade"):
        async with self.lock:
            price = float(event["price"])
            self.last_time = time.time()
            self.minute = self.last_time % (1000 * 60)
            if self.last_time % 1000 < self.minute:
                self.open = price
                self.high = price
                self.low = price
                self.volume = abs(float(event["quantity"]))
                self.trades_made = 1
            else:
                self.high = max(self.high, price) if self.high else price
                self.low = min(self.low, price) if self.low else price
                self.volume += abs(float(event["quantity"]))
                self.trades_made += 1

                if not self.open:
                    self.open = price

            self.close = price

    async def l2_auction(self, event: "L2Auction"):
        # Handle auction events Here.
        pass

    @property
    def ohlc(self) -> "_Ohlc.__dict__":
        return asdict(self._Ohlc(self.open, self.high, self.low, self.close, self.volume, int(self.last_time)))
