from django.urls import path
from rest_framework.routers import SimpleRouter

from kcsec.crypto.views import ChartDataViewSet
from kcsec.crypto.views import PortfolioView
from kcsec.crypto.views import TradeView

router = SimpleRouter()

router.register("", ChartDataViewSet, basename="chart-data")

urlpatterns = [
    path("", TradeView.as_view(), name="coin"),
    path("portfolio/<int:pk>", PortfolioView.as_view(), name="crypto_portfolio"),
]

urlpatterns += router.urls
