import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from kcsec.crypto.models import Ohlcv
from kcsec.crypto.types import TimeFrame

logger = logging.getLogger(__name__)


class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = "crypto/portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shares"] = [
            {**self.get_price_info(share["crypto_symbol_id"], "gemini", TimeFrame.ONE_MINUTE), **share}
            for share in self.request.user.portfolio.cryptoshare_set.all().values()
        ]

        return context

    @staticmethod
    def get_price_info(symbol: str, exchange: str, time_frame: "TimeFrame"):
        percent_change, price_change = Ohlcv.objects.one_day_difference(symbol, exchange, time_frame)

        return {
            "price": Ohlcv.objects.latest_price(symbol, exchange, time_frame),
            "percent_change": percent_change,
            "price_change": price_change,
        }
