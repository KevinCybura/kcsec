import datetime
import locale
from decimal import Decimal

import pytest

from kcsec.crypto.models import Ohlcv
from kcsec.crypto.models.factories.ohlcv import OhlcvFactory
from kcsec.crypto.views import TradeView


class TestTradeView:
    def test_get_success_url(self, trade_view_request):
        view = TradeView(request=trade_view_request)
        assert view.get_success_url() == "/crypto/?symbol=BTCUSD"

        trade_view_request.POST.pop("symbol")
        assert view.get_success_url() == "/crypto/"

    @pytest.mark.django_db
    def test_portfolio_data(self, trade_view_request_authenticated):
        locale.setlocale(locale.LC_ALL, "")
        portfolio = trade_view_request_authenticated.user.portfolio
        view = TradeView(request=trade_view_request_authenticated)
        result = view.get_context_data(symbols=["BTCUSD"])
        assert result["symbols"] == ["BTCUSD"]
        assert result["navs"] == ["BTCUSD", "ETHUSD", "LTCUSD"]
        assert result["current_nav"] == "BTCUSD"
        assert len(result["symbol_data"]) == 1
        data = result["symbol_data"][0]
        assert data["form"].initial == {
            "portfolio": portfolio,
            "price": round(Ohlcv.objects.filter(symbol="BTCUSD").latest().close, ndigits=2),
            "symbol": "BTCUSD",
        }
        assert len(data["order_data"]) == 5
        order_data = portfolio.cryptoorder_set.filter(symbol="BTCUSD").values(
            "created_at", "order_type", "price", "shares", "symbol_id", "trade_type"
        )
        assert sorted(data["order_data"], key=lambda o: o["created_at"]) == sorted(
            list(order_data), key=lambda o: o["created_at"]
        )

        share = portfolio.cryptoshare_set.get(symbol="BTCUSD")
        assert data["share_data"]["average_price"] == locale.currency(share.average_price, grouping=True)
        assert data["share_data"]["shares"] == share.shares
        assert data["share_data"]["symbol"] == share.symbol.id
        assert data["share_data"]["id"] == share.id
        assert data["share_data"]["portfolio"] == portfolio.id
        assert isinstance(data["share_data"]["todays_percent"], Decimal)
        assert data["share_data"]["todays_percent"] != Decimal("Nan")
        assert isinstance(data["share_data"]["todays_price"], str)
        assert data["share_data"]["todays_price"] != "Nan"
        assert isinstance(data["share_data"]["total_percent"], Decimal)
        assert data["share_data"]["total_percent"] != Decimal("Nan")
        assert isinstance(data["share_data"]["total_price"], str)
        assert data["share_data"]["total_price"] != "Nan"

    @pytest.mark.django_db
    def test_portfolio_data_no_user(self, trade_view_request, crypto_seeds):
        view = TradeView(request=trade_view_request)
        result = view.get_context_data(symbols=["BTCUSD"])
        assert result["symbols"] == ["BTCUSD"]
        assert result["navs"] == ["BTCUSD", "ETHUSD", "LTCUSD"]
        assert result["current_nav"] == "BTCUSD"
        assert result["form"] == None
        assert len(result["symbol_data"]) == 1
        data = result["symbol_data"][0]
        assert data["order_data"] == {}
        assert data["share_data"] == {}
        assert data["symbol"] == "BTCUSD"
        assert list(data.keys()) == [
            "symbol",
            "price",
            "formatted_price",
            "midnight_price",
            "percent_change",
            "price_change",
            "share_data",
            "order_data",
            "form",
        ]

        assert data["form"].initial == {
            "portfolio": None,
            "price": round(Ohlcv.objects.filter(symbol="BTCUSD").latest().close, ndigits=2),
            "symbol": "BTCUSD",
        }


@pytest.mark.django_db
def test_latest_symbol_price(crypto_seeds):
    symbol = crypto_seeds.symbols[0]
    ohlcv = OhlcvFactory(
        symbol=symbol,
        asset_id_base=symbol.asset_id_base,
        asset_id_quote=symbol.asset_id_quote,
        time_open=datetime.datetime.now() + datetime.timedelta(minutes=1),
        exchange=crypto_seeds.exchange,
        time_frame="1m",
    )
    price = Ohlcv.objects.filter(symbol=symbol, exchange="gemini", time_frame="1m").latest()
    assert price.close == ohlcv.close
