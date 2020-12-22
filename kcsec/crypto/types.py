from itertools import takewhile
from typing import TYPE_CHECKING

from django.db.models import TextChoices

if TYPE_CHECKING:
    from typing import Literal
    from typing import Optional
    from typing import TypedDict
    from typing import Union

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
        time_frame: Optional["TimeFrame"]


class TimeFrame(TextChoices):
    ONE_MINUTE = "1m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    ONE_HOUR = "1h"
    SIX_HOUR = "6h"
    ONE_DAY = "1d"

    @property
    def one_day_index(self) -> int:
        return int(1440 / int("".join(takewhile(str.isdigit, self))))
