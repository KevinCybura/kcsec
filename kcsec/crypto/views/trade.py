import logging
from typing import TYPE_CHECKING

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView

from kcsec.crypto.forms import OrderForm
from kcsec.crypto.models import Ohlcv

if TYPE_CHECKING:
    from kcsec.core.models import Portfolio

logger = logging.getLogger(__name__)


class TradeView(FormView):
    template_name = "crypto/index.html"
    SYMBOLS = ["BTCUSD", "ETHUSD", "LTCUSD"]
    form_class = OrderForm
    success_url = reverse_lazy("crypto")

    def get_success_url(self):
        if symbol := self.get_form().data.get("crypto_symbol"):
            return self.success_url + f"?symbol={symbol}"
        return self.success_url

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
        context["symbol_data"] = self.symbol_data(symbols)

        return context

    def symbol_data(self, symbols: list[str]) -> list[dict]:
        portfolio_data = []
        for symbol in symbols:
            base = symbol[:3]
            quote = symbol[3:]

            data = {
                "symbol": symbol,
                "share_data": None,
                "order_data": None,
                **self.get_price_info(base, quote, "gemini", Ohlcv.TimeFrame.ONE_MINUTE),
            }

            if self.request.user.is_authenticated:
                data = self.portfolio_data(data, symbol, self.request.user.portfolio)

            data["form"] = self.form_class(
                initial={
                    "portfolio": getattr(self.request.user, "portfolio", None),
                    "crypto_symbol": symbol,
                    "price": round(Ohlcv.objects.latest_price(base, quote, "gemini", "1m")[0], 2),
                },
                auto_id=f"id_{symbol}_%s",
            )

            portfolio_data.append(data)

        return portfolio_data

    @staticmethod
    def portfolio_data(data: dict, symbol: str, portfolio: "Portfolio") -> dict:
        data["order_data"] = (
            portfolio.cryptoorder_set.filter(crypto_symbol_id=symbol)
            .order_by("-created_at")
            .values("crypto_symbol_id", "shares", "price", "order_type", "trade_type", "created_at")
        )[:5]

        share_data = portfolio.cryptoshare_set.filter(crypto_symbol_id=symbol)

        if share_data.exists():
            data["share_data"] = share_data[0]

        return data

    @staticmethod
    def get_price_info(base: str, quote: str, exchange: str, time_frame: "Ohlcv.TimeFrame"):
        one_day_price_diff = Ohlcv.objects.get_24_hour_difference(base, quote, exchange, time_frame)

        return {
            "price": Ohlcv.objects.latest_price(base, quote, exchange, time_frame)[0],
            "percent_change": one_day_price_diff.percent_change,
            "price_change": one_day_price_diff.price_change,
        }
