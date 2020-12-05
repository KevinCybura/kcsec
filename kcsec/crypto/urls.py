from django.urls import path
from rest_framework.routers import SimpleRouter

from kcsec.crypto import views

router = SimpleRouter()

router.register("", views.TradeGenericViewSet, basename="chart-data")

urlpatterns = [
    path("", views.TradingView.as_view(), name="coin"),
]

urlpatterns += router.urls
