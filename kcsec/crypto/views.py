import logging

import simplejson as json
from django.db.models.expressions import F
from django.http import Http404
from django.views.generic import TemplateView
from psqlextra.expressions import DateTimeEpoch

from kcsec.crypto.models import Ohlcv

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

        context["preloaded_coins"] = {}
        for asset in context["coins"]:
            context["preloaded_coins"][asset] = self._get_ohlcv(asset, exchange_id="gemini")

        return context

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
        print(len(ret))
        return ret
