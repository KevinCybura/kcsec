from datetime import datetime
from itertools import cycle

import simplejson as json
from django.db.models import F
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import ContextMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from kcsec.core.models import Portfolio
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import OhlcvSerializer
from kcsec.crypto.types import TimeFrame


class ComplexEncoder(json.JSONEncoder):
    """Always return JSON primitive."""

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            if hasattr(obj, "pk"):
                return obj.pk
            return str(obj)


class PortfolioPieChartJSONView(ContextMixin, View):
    colors = cycle(["#80002d", "#2b2b2b", "#999"])

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {}

        portfolio = Portfolio.objects.get(pk=self.request.GET["user_id"])

        shares = (
            portfolio.cryptoshare_set.all()
            .annotate(equity=F("symbol__price") * F("shares"))
            .values("equity", "symbol_id")
        )

        data = [share["equity"] for share in shares]
        labels = [share["symbol_id"] for share in shares]
        colors = [next(self.colors) for _ in data]

        data.append(portfolio.balance)
        labels.append("cash")
        colors.append(next(self.colors))

        context["data"] = {"datasets": [{"data": data, "backgroundColor": colors}], "labels": labels}
        return context

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(json.dumps(context, cls=ComplexEncoder), content_type="application/json", **response_kwargs)


class ChartDataViewSet(GenericViewSet):
    serializer_class = OhlcvSerializer
    queryset = Ohlcv.objects.all()

    @action(detail=False, methods=["post"])
    def chart_data(self, request):
        """Gets Open high low close data for charts"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(self.get_ohlc(serializer.validated_data["symbol"], "gemini"), many=True)

        return Response(serializer.data)

    def get_ohlc(self, symbol: str, exchange: str) -> list[Ohlcv]:
        """Queries Open high low close data for charts"""
        return list(
            reversed(
                self.queryset.filter(
                    time_open__gte=datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                )
                .filter_trade_view_chart(symbol, exchange, TimeFrame.ONE_MINUTE)
                .values("time", "open", "high", "low", "close", "volume", "value")
            )
        )
