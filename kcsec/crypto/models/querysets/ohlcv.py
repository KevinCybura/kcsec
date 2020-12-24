from datetime import datetime
from datetime import timedelta
from typing import TYPE_CHECKING

from django.db.models import F
from django.utils.timezone import utc
from psqlextra.expressions import DateTimeEpoch
from psqlextra.manager import PostgresQuerySet

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from kcsec.crypto.models import Exchange
    from kcsec.crypto.models import Ohlcv
    from kcsec.crypto.models import Symbol
    from kcsec.crypto.types import CandleMessage
    from kcsec.crypto.types import TimeFrame


class OhlcvQuerySet(PostgresQuerySet):
    def filter_trade_view_chart(
        self, symbol: "Symbol", exchange: "Exchange", time_frame: "TimeFrame"
    ) -> "OhlcvQuerySet":
        """
            Filter data for TradeView light weight charts.
        :param symbol: `Symbol` which to get data for.
        :param exchange: the `Exchange` the symbol is traded on.
        :param time_frame: the `TimeFrame` to filter on.
        :return: OhlcvQuerySet which contains data used for TradeView light weight charts.
        """
        return (
            self.filter(symbol=symbol, exchange=exchange, time_frame=time_frame)
            .annotate_time()
            .annotate_value()
            .order_by("-time")
        )

    def annotate_time(self) -> "OhlcvQuerySet":
        return self.annotate(time=DateTimeEpoch("time_open"))

    def annotate_value(self) -> "OhlcvQuerySet":
        return self.annotate(value=(F("high") + F("low")) / 2)

    def filter_after_midnight(
        self, symbol: "Symbol", exchange: "Exchange", time_frame: "TimeFrame", delta: timedelta
    ) -> "QuerySet":
        return self.filter(
            symbol=symbol,
            exchange=exchange,
            time_frame=time_frame,
            time_open__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - delta,
        )

    def bulk_create_from_message(self, message: "CandleMessage", exchange: "Exchange") -> "Ohlcv":
        obj = [
            self.model(
                symbol_id=message["symbol"],
                asset_id_base_id=message["symbol"][:3],
                asset_id_quote_id=message["symbol"][3:],
                exchange_id=exchange,
                time_open=datetime.fromtimestamp(change["time"], tz=utc),
                open=change["open"],
                high=change["high"],
                low=change["low"],
                close=change["close"],
                volume=change["volume"],
                time_frame=message["time_frame"],
            )
            for change in message["changes"]
        ]
        return self.bulk_create(obj, ignore_conflicts=True)
