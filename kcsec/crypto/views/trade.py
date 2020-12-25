import logging
from datetime import timedelta

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView

from kcsec.crypto.forms import OrderForm
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import CryptoTemplateContext

logger = logging.getLogger(__name__)


class TradeView(FormView):
    template_name = "crypto/index.html"
    SYMBOLS = ["BTCUSD", "ETHUSD", "LTCUSD"]
    form_class = OrderForm
    success_url = reverse_lazy("crypto")
    serializer_class = CryptoTemplateContext

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if symbol := self.get_form().data.get("symbol"):
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
        context = super().get_context_data(form=None, **kwargs)
        symbol = self.request.GET.get("symbol")

        if symbol and symbol not in self.SYMBOLS:
            raise Http404(f"Symbol does not exist {symbol}")

        symbols = [symbol] if symbol else self.SYMBOLS

        context["navs"] = self.SYMBOLS

        context["current_nav"] = symbol or "Crypto"

        def current_price(sym):
            return Ohlcv.objects.filter(symbol=sym, exchange="gemini", time_frame="1m").latest().close

        def midnight_price(sym):
            return Ohlcv.objects.filter_after_midnight(sym, "gemini", "1m", timedelta(hours=5)).earliest().open

        context["symbol_data"] = [
            self.serializer_class(
                instance=dict(
                    symbol=symbol,
                    user=self.request.user,
                    form_class=self.form_class,
                    price=current_price(symbol),
                    midnight_price=midnight_price(symbol),
                ),
            ).data
            for symbol in symbols
        ]

        return context
