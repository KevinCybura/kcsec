import logging

from django.http import Http404
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class CoinView(TemplateView):
    template_name = "crypto/index.html"

    COINS = {"btc": "BTCUSD", "eth": "ETHUSD", "ltc": "LTCUSD"}

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        coin = kwargs.get("coin")
        if coin == None:
            context["coins"] = self.COINS.values()
        else:
            try:
                context["coins"] = [self.COINS[coin.lower()]]
            except KeyError as e:
                logger.error(e)
                return Http404(f"Coin does not exist {coin}")
        return context


# # Create your views here.
# def index(request):
#     return render(request, "crypto/index.html", {"coins": COINS})
