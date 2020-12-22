from typing import TYPE_CHECKING

from django_filters import rest_framework as rf
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import OhlcvFilter
from kcsec.crypto.serializers import OhlcvSerializer
from kcsec.crypto.types import TimeFrame

if TYPE_CHECKING:
    from kcsec.crypto.models import Exchange
    from kcsec.crypto.models import Symbol


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
    def get_ohlc(cls, symbol: "Symbol.symbol_id", exchange: "Exchange.exchange_id") -> list[Ohlcv]:
        """Queries Open high low close data for charts"""
        return list(reversed(Ohlcv.objects.filter_trade_view_chart(symbol, exchange, TimeFrame.ONE_MINUTE)))

    @action(detail=False, methods=["post"])
    def latest_price(self, request):
        symbol = self.request.data["symbol"]
        return Response(Ohlcv.objects.latest_price(symbol, "gemini", TimeFrame.ONE_MINUTE))


class OhlcvViewSet(ReadOnlyModelViewSet):
    serializer_class = OhlcvSerializer
    queryset = Ohlcv.objects.all()
    filterset_class = OhlcvFilter
    filter_backends = [rf.DjangoFilterBackend]
