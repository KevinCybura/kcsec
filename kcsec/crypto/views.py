import logging
from typing import List
from typing import Optional

from django.db.models.expressions import F
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView
from psqlextra.expressions import DateTimeEpoch
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from kcsec.crypto.forms import OrderForm
from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import ChartDataSerializer

logger = logging.getLogger(__name__)


class TradingView(FormView):
    template_name = "crypto/index.html"
    SYMBOLS = ["BTC", "ETH", "LTC"]
    form_class = OrderForm
    success_url = reverse_lazy("coin")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        context_data = self.get_context_data(form=form)
        return self.render_to_response(context_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        symbol = self.request.GET.get("symbol")

        if symbol and symbol not in self.SYMBOLS:
            raise Http404(f"Symbol does not exist {symbol}")

        symbols = [symbol] if symbol else self.SYMBOLS

        context["navs"] = self.SYMBOLS
        context["current_nav"] = symbol or "Crypto"
        context["symbol_data"] = self.symbol_data(symbols, kwargs.get("form"))

        return context

    def symbol_data(self, symbols: List[str], form: Optional[OrderForm] = None) -> List[dict]:

        if self.request.user.is_authenticated:
            portfolio = self.request.user.portfolio
        else:
            portfolio = None

        context = []
        for symbol in symbols:
            data = {"symbol": symbol, "share_data": None, "order_data": None}

            if form and form.cleaned_data["crypto_symbol"].asset_id_base_id == symbol:
                data["form"] = form
            else:
                data["form"] = self.form_class(initial={"portfolio": portfolio, "crypto_symbol": symbol})

            if portfolio:
                data["order_data"] = (
                    portfolio.cryptoorder_set.filter(crypto_symbol_id=symbol)
                    .order_by("-created_at")
                    .values("crypto_symbol_id", "shares", "price", "order_type", "created_at")
                )
                try:
                    data["share_data"] = portfolio.cryptoshare_set.get(crypto_symbol_id=symbol)
                except CryptoShare.DoesNotExist:
                    data["share_data"] = None
            context.append(data)

        return context


class TradeGenericViewSet(GenericViewSet):
    serializer_class = ChartDataSerializer

    @action(detail=False, methods=["post"])
    def chart_data(self, request):
        """Gets Open high low close data for charts"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(self._get_ohlc(serializer.validated_data["symbol"], "gemini"), many=True)

        return Response(serializer.data)

    @classmethod
    def _get_ohlc(cls, asset, exchange_id):
        """Queries Open high low close data for charts"""
        ret = list(
            Ohlcv.objects.filter(asset_id_base=asset, exchange_id=exchange_id)
            .annotate(time=DateTimeEpoch("time_open"))
            .annotate(value=((F("high") + F("low")) / 2))
            .order_by(
                F("time").desc(),
            )[:1441]
            .values("open", "high", "low", "close", "volume", "value", "time")
        )
        ret.reverse()
        return ret
