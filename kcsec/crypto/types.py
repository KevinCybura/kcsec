from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    from typing import Optional
    from typing import TypedDict
    from typing import Union

    from kcsec.crypto.models import Ohlcv

    MessageChanges = list[list[float]]

    class Change(TypedDict):
        time: float
        open: float
        high: float
        low: float
        close: float
        volume: int
        value: float

    class CandleMessage(TypedDict):
        symbol: str
        type: Literal[
            "l2",
            "candles_1m_updates",
            "candles_5m_updates",
            "candles_15m_updates",
            "candles_30m_updates",
            "candles_1h_updates",
            "candles_6h_updates",
            "candles_1d_updates",
        ]
        changes: Union[list[Change], MessageChanges]
        time_frame: Optional[Ohlcv.TimeFrame]
