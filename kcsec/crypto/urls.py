from django.urls import path
from rest_framework.routers import SimpleRouter

from kcsec.crypto.views import ChartDataViewSet
from kcsec.crypto.views import PortfolioPieChartJSONView
from kcsec.crypto.views import PortfolioView
from kcsec.crypto.views import TradeView

router = SimpleRouter()

router.register("", ChartDataViewSet, basename="chart-data")

urlpatterns = [
    path("", TradeView.as_view(), name="crypto"),
    path("portfolio/", PortfolioView.as_view(), name="crypto_portfolio"),
    path("chart", PortfolioPieChartJSONView.as_view(), name="line_chart_json"),
]

urlpatterns += router.urls
