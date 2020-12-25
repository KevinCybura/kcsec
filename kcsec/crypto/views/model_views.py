from django_filters import rest_framework as rf
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from kcsec.crypto.filter_sets import OhlcvFilter
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import OhlcvSerializer
from kcsec.crypto.types import TimeFrame


class ChartDataViewSet(GenericViewSet):
    serializer_class = OhlcvSerializer

    @action(detail=False, methods=["post"])
    def chart_data(self, request):
        """Gets Open high low close data for charts"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(self.get_ohlc(serializer.validated_data["symbol"], "gemini"), many=True)

        return Response(serializer.data)

    @classmethod
    def get_ohlc(cls, symbol: str, exchange: str) -> list[Ohlcv]:
        """Queries Open high low close data for charts"""
        return list(
            reversed(
                Ohlcv.objects.filter_trade_view_chart(symbol, exchange, TimeFrame.ONE_MINUTE)[:1441].values(
                    "time", "open", "high", "low", "close", "volume", "value"
                )
            )
        )

    @action(detail=False, methods=["post"])
    def latest_price(self, request):
        symbol = self.request.data["symbol"]
        return Response(
            Ohlcv.objects.filter(symbol=symbol, exchange="gemini", time_frame=TimeFrame.ONE_MINUTE).latest().close
        )


# Not using this DELETE?
class OhlcvViewSet(ReadOnlyModelViewSet):
    serializer_class = OhlcvSerializer
    queryset = Ohlcv.objects.all()
    filterset_class = OhlcvFilter
    filter_backends = [rf.DjangoFilterBackend]
