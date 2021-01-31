import logging
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from kcsec.crypto.models import Ohlcv
from kcsec.crypto.serializers import CryptoTemplateContext

logger = logging.getLogger(__name__)


class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = "crypto/portfolio.html"
    serializer_class = CryptoTemplateContext

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        symbols = self.request.user.portfolio_namespace.cryptoshare_set.all().values_list("symbol_id", flat=True)

        def current_price(sym):
            return Ohlcv.objects.filter(symbol=sym, exchange="gemini", time_frame="1m").latest().close

        def midnight_price(sym):
            return Ohlcv.objects.filter_after_midnight(sym, "gemini", "1m", timedelta(hours=5)).earliest().open

        context["data"] = [
            self.serializer_class(
                instance=dict(
                    symbol=symbol,
                    user=self.request.user,
                    price=current_price(symbol),
                    midnight_price=midnight_price(symbol),
                ),
            ).data
            for symbol in symbols
        ]

        return context
