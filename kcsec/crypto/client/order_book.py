import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    from typing import TypedDict
    from typing import Union

    Change = list[Literal["buy", "sell"], float, float]

    class L2Update(TypedDict):
        type: Literal["l2_update"]
        symbol: str
        changes: list[Change]

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

    L2Initial = dict[L2Update, L2Auction, list[L2Trade]]
    L2Message = Union[L2Trade, L2Auction, L2Update, L2Initial]

logger = logging.getLogger(__name__)


class OrderBook:
    def __init__(self, symbol):
        self.symbol: str = symbol
        self.asks = {}
        self.bids = {}
        self.best_bid = None
        self.best_ask = None

    async def handle_message(self, message: "L2Message"):
        updates = {"buy": {}, "sell": {}}
        for change in message["changes"]:

            updates[change[0]] = (change[1], change[2])

            if change[0] == "buy":
                self.best_bid = max(self.best_bid, change[1]) if self.best_bid else change[1]
            elif change[0] == "sell":
                self.best_ask = min(self.best_ask, change[1]) if self.best_ask else change[1]

            # await self.store_order_book(message["symbol"], change)

        self.asks.update(**updates["sell"])
        self.bids.update(**updates["buy"])
        return updates

    # @database_sync_to_async
    # async def store_order_book(self, symbol, change):
    #     BidAsk.objects.update_or_create(
    #         symbol=symbol, exchange="gemini", order_type=change[0], price=change[1], quantity=change[2]
    #     )

    # @database_sync_to_async
    # async def update_order_book(self, symbol, updates):
    #     buys_sells = []
    #     for order_type, (price, quantity) in updates:
    #         buys_sells.append(
    #             dict(
    #                 symbol__asset_base_id=symbol,
    #                 symbol__exchange_id="gemini",
    #                 order_type=order_type,
    #                 price=price,
    #                 quantity=quantity,
    #             )
    #         )
    # BidAsk.objects.bulk_upsert(
    #     conflict_target=["symbol__asset_base_id", "symbol__exchange_", "price"],
    #     rows=buys_sells,
    # )

    @property
    def order_book(self) -> dict:
        return {"asks": self.asks, "bids": self.bids, "ask": self.best_ask, "bid": self.best_bid}

    # def __init__(self, symbol):
    #     self.symbol: str = symbol
    #     self.asks = {}
    #     self.bids = {}
    #     self.best_bid = None
    #     self.best_ask = None
    #     self.ohlcv = []
    #     self.high = None
    #     self.low = None
    #     self.open = None
    #     self.close = None
    #     self.volume = 0
    #     self.last_time = None
    #     self.lock = Lock()
    #     self.trades_made = 0
    #     self.minute = 0
    #
    # async def handle_message(self, message: "L2Message"):
    # if message["type"] == "l2_updates" and message.get("trades"):
    #     await self.l2_update(message)
    #     for trade in message["trades"]:
    #         await self.l2_trade(trade)
    #
    #     for event in message["auction_events"]:
    #         await self.l2_auction(event)
    #
    # elif message["type"] == "l2_updates":
    #     await self.l2_update(message)
    # elif message["type"] == "trade":
    #     await self.l2_trade(message)
    # elif message["type"] == "auction":
    #     await self.l2_auction(message)
    #
    # async def l2_update(self, event: "L2Update"):
    #     async with self.lock:
    #         for change in event["changes"]:
    #             if change[0] == "buy":
    #                 self.bids[change[1]] = change[2]
    #                 self.best_bid = max(self.best_bid, change[1]) if self.best_bid else change[1]
    #             elif change[0] == "sell":
    #                 self.asks[change[1]] = change[2]
    #                 self.best_ask = min(self.best_ask, change[1]) if self.best_ask else change[1]
    #
    # async def l2_trade(self, event: "L2Trade"):
    #     async with self.lock:
    #         price = float(event["price"])
    #         self.last_time = time.time()
    #         self.minute = self.last_time % (1000 * 60)
    #         if self.last_time % 1000 < self.minute:
    #             self.open = price
    #             self.high = price
    #             self.low = price
    #             self.volume = abs(float(event["quantity"]))
    #             self.trades_made = 1
    #         else:
    #             self.high = max(self.high, price) if self.high else price
    #             self.low = min(self.low, price) if self.low else price
    #             self.volume += abs(float(event["quantity"]))
    #             self.trades_made += 1
    #
    #             if not self.open:
    #                 self.open = price
    #
    #         self.close = price
    #
    # async def l2_auction(self, event: "L2Auction"):
    #     # Handle auction events Here.
    #     pass

    # @property
    # def ohlc(self) -> dict:
    #     return {
    #         "open": self.open,
    #         "high": self.high,
    #         "low": self.low,
    #         "close": self.close,
    #         "volume": self.volume,
    #         "time": int(self.last_time),
    #         "value": (self.open + self.close) / 2,
    #     }
