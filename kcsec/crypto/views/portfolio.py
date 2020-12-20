import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = "crypto/portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shares"] = self.request.user.portfolio.cryptoshare_set.all()

        return context
