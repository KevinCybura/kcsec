from itertools import cycle

import simplejson as json
from django.db.models import F
from django.http import HttpResponse
from django.views.generic import TemplateView

from kcsec.core.models import Portfolio


class ComplexEncoder(json.JSONEncoder):
    """Always return JSON primitive."""

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            if hasattr(obj, "pk"):
                return obj.pk
            return str(obj)


class PortfolioPieChartJSONView(TemplateView):
    colors = cycle(["#80002d", "#2b2b2b", "#999"])

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

        context["data"] = {"datasets": [{"data": data, "backgroundColor": colors}], "labels": labels}
        return context

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(json.dumps(context, cls=ComplexEncoder), content_type="application/json", **response_kwargs)
