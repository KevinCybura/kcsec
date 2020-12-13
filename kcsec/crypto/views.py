import logging
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
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import ChartDataSerializer

logger = logging.getLogger(__name__)


class TradingView(FormView):
    template_name = "crypto/index.html"
    SYMBOLS = ["BTC", "ETH", "LTC"]
    form_class = OrderForm
    success_url = reverse_lazy("coin")

    def get_success_url(self):
        symbol = self.get_form().data["crypto_symbol"]
        return self.success_url + f"?symbol={symbol}"

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
        context["symbol_data"] = self.portfolio_data(symbols)
        context["order_types"] = ["Market Order", "Limit Order"]

        return context

    def portfolio_data(self, symbols: list[str]) -> list[dict]:

        if self.request.user.is_authenticated:
            portfolio = self.request.user.portfolio
        else:
            portfolio = None

        portfolio_data = []
        for symbol in symbols:

            data = {"symbol": symbol, "share_data": None, "order_data": None}

            if portfolio:
                data["order_data"] = (
                    portfolio.cryptoorder_set.filter(crypto_symbol_id=symbol)
                    .order_by("-created_at")
                    .values("crypto_symbol_id", "shares", "price", "order_type", "created_at")
                )
                data["share_data"] = portfolio.cryptoshare_set.filter(crypto_symbol_id=symbol)

                if data["share_data"].exists():
                    data["share_data"] = data["share_data"][0]

            data["form"] = self.form_class(
                initial={
                    "portfolio": portfolio,
                    "crypto_symbol": symbol,
                    "price": round(self.latest_symbol_price(symbol)[0], 2),
                },
                auto_id=f"id_{symbol}_%s",
            )

            portfolio_data.append(data)

        return portfolio_data

    @classmethod
    def latest_symbol_price(cls, symbol: str) -> dict:
        return Ohlcv.objects.filter(asset_id_base_id=symbol, exchange_id="gemini").values_list("close")[0]


class TradeGenericViewSet(GenericViewSet):
    serializer_class = ChartDataSerializer

    @action(detail=False, methods=["post"])
    def chart_data(self, request):
        """Gets Open high low close data for charts"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(self.get_ohlc(serializer.validated_data["symbol"], "gemini"), many=True)

        return Response(serializer.data)

    @classmethod
    def get_ohlc(cls, asset, exchange_id):
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
