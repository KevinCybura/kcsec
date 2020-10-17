import logging

from django.db.models.expressions import F
from django.http import Http404
from django.views.generic import TemplateView
from psqlextra.expressions import DateTimeEpoch
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import ChartDataSerializer

logger = logging.getLogger(__name__)


class CoinView(TemplateView):
    template_name = "crypto/index.html"
    COINS = ["BTCUSD", "ETHUSD", "LTCUSD"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coin = kwargs.get("coin")

        if coin and coin not in self.COINS:
            raise Http404(f"Coin does not exist {coin}")

        context["navs"] = self.COINS
        context["current_nav"] = coin or "Home"
        context["coins"] = [coin] if coin else self.COINS

        return context


class TradeGenericViewSet(GenericViewSet):
    serializer_class = ChartDataSerializer

    @action(detail=False, methods=["post"])
    def chart_data(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer = self.get_serializer(self._get_ohlcv(serializer.validated_data["symbol"], "gemini"), many=True)

        return Response(serializer.data)

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
