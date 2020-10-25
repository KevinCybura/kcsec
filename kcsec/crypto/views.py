import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.expressions import F
from django.http import Http404
from django.views.generic import TemplateView
from psqlextra.expressions import DateTimeEpoch
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from kcsec.core.models import Portfolio
from kcsec.crypto.models import CryptoOrder
from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import ChartDataSerializer

logger = logging.getLogger(__name__)


class SymbolView(LoginRequiredMixin, TemplateView):
    template_name = "crypto/index.html"
    SYMBOLS = ["BTCUSD", "ETHUSD", "LTCUSD"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        symbol = self.request.GET.get("symbol")

        if symbol and symbol not in self.SYMBOLS:
            raise Http404(f"Symbol does not exist {symbol}")

        context["navs"] = self.SYMBOLS
        context["current_nav"] = symbol or "Crypto"
        context["symbols"] = [symbol] if symbol else self.SYMBOLS

        return context


class TradeGenericViewSet(LoginRequiredMixin, GenericViewSet):
    serializer_class = ChartDataSerializer

    @action(detail=False, methods=["post"])
    def chart_data(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(self._get_ohlcv(serializer.validated_data["symbol"], "gemini"), many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def make_trade(self, request):
        portfolio = Portfolio.objects.get(user__username=request.user)
        return Response({})

    def _get_ohlcv(self, asset, exchange_id):
        base = asset[:3]
        quote = asset[3:]

        ret = list(
            Ohlcv.objects.filter(asset_id_base=base, asset_id_quote=quote, exchange_id=exchange_id)
            .annotate(time=DateTimeEpoch("time_open"))
            .annotate(value=((F("high") + F("low")) / 2))
            .order_by(
                F("time").desc(),
            )[:1441]
            .values("open", "high", "low", "close", "volume", "value", "time")
        )
        ret.reverse()
        return ret
