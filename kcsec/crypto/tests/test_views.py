import datetime

import pytest

from kcsec.crypto.models.factories.ohlcv import OhlcvFactory
from kcsec.crypto.models.ohlcv import Ohlcv
from kcsec.crypto.views import TradeView


class TestTradeView:
    def test_get_success_url(self, trade_view_request):
        view = TradeView(request=trade_view_request)
        assert view.get_success_url() == "/crypto/?symbol=BTCUSD"

        trade_view_request.POST.pop("crypto_symbol")
        assert view.get_success_url() == "/crypto/"

    @pytest.mark.django_db
    def test_portfolio_data(self, trade_view_request_authenticated):
        view = TradeView(request=trade_view_request_authenticated)
        result = view.symbol_data(["BTCUSD"])
        assert result[0]["symbol"] == "BTCUSD"
        assert result[0]["share_data"] is not None
        assert len(result[0]["order_data"]) == 5
        assert sorted(list(result[0]["form"].fields.keys())) == [
            "crypto_symbol",
            "order_type",
            "portfolio",
            "price",
            "shares",
            "trade_type",
        ]

    @pytest.mark.django_db
    def test_portfolio_data_no_user(self, trade_view_request_authenticated, crypto_seeds):
        trade_view_request_authenticated.user.is_authenticated = False
        view = TradeView(request=trade_view_request_authenticated)
        result = view.symbol_data(["BTCUSD"])
        assert result[0]["symbol"] == "BTCUSD"
        assert result[0]["share_data"] is None
        assert result[0]["order_data"] is None
        assert sorted(list(result[0]["form"].fields.keys())) == [
            "crypto_symbol",
            "order_type",
            "portfolio",
            "price",
            "shares",
            "trade_type",
        ]


@pytest.mark.django_db
def test_latest_symbol_price(crypto_seeds):
    symbol = crypto_seeds.symbols[0]
    ohlcv = OhlcvFactory(
        asset_id_base=symbol.asset_id_base,
        asset_id_quote=symbol.asset_id_quote,
        time_open=datetime.datetime.now() + datetime.timedelta(minutes=1),
        exchange=crypto_seeds.exchange,
    )

    assert (
        Ohlcv.objects.latest_price(
            asset_id_base=symbol.asset_id_base, asset_id_quote=symbol.asset_id_quote, exchange="gemini"
        )[0]
        == ohlcv.close
    )
