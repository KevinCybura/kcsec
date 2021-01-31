from decimal import Decimal

import pytest

from kcsec.crypto.forms import OrderForm
from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.models.factories.share import CryptoShareFactory


class TestOrderForm:
    @pytest.mark.django_db
    def test_save_limit_order(self, portfolio_namespace):
        Ohlcv.objects.filter(symbol="BTCUSD", time_frame="1m").update(close=100)
        share = portfolio_namespace.share
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": 1,
                "order_type": "limit_order",
                "trade_type": "sell",
                "price": 100,
            }
        )
        form.fields["price"].disabled = False
        form.full_clean()
        assert form.instance.portfolio.balance == 50000
        assert share.shares == 50
        assert share.average_price == 1

        order = form.save()
        share = portfolio_namespace.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        assert not order.filled
        assert order.portfolio.balance == 50000
        assert share.shares == 50
        assert share.average_price == 1

    @pytest.mark.django_db
    def test_save_sell(self, portfolio_namespace):
        Ohlcv.objects.filter(symbol="BTCUSD", time_frame="1m").update(close=100)
        share = portfolio_namespace.share
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": 1,
                "order_type": "market_order",
                "trade_type": "sell",
            }
        )
        form.full_clean()
        assert form.instance.portfolio.balance == 50000
        assert share.shares == 50
        assert share.average_price == 1

        order = form.save()
        share = portfolio_namespace.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        assert order.filled
        assert order.portfolio.balance == 50100
        assert share.shares == 49
        assert share.average_price == 1

    @pytest.mark.django_db
    def test_save_buy(self, portfolio_namespace):
        Ohlcv.objects.filter(symbol="BTCUSD", time_frame="1m").update(close=100)
        share = portfolio_namespace.share
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": 1,
                "order_type": "market_order",
                "trade_type": "buy",
            }
        )
        form.full_clean()
        assert form.instance.portfolio.balance == 50000
        assert share.shares == 50
        assert share.average_price == 1

        order = form.save()
        share = portfolio_namespace.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        assert order.filled
        assert order.portfolio.balance == 49900
        assert share.shares == 51
        assert share.average_price == Decimal("2.94118")

    @pytest.mark.django_db
    def test_save_buy(self, portfolio_namespace):
        Ohlcv.objects.filter(symbol="BTCUSD", time_frame="1m").update(close=100)
        share = portfolio_namespace.share
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": 1,
                "order_type": "market_order",
                "trade_type": "buy",
            }
        )
        form.full_clean()
        assert form.instance.portfolio.balance == 50000
        assert share.shares == 50
        assert share.average_price == 1

        order = form.save()
        share = portfolio_namespace.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        assert order.filled
        assert order.portfolio.balance == 49900
        assert share.shares == 51
        assert share.average_price == Decimal("2.94118")

    @pytest.mark.django_db
    def test_save_delete_share(self, portfolio_namespace):
        Ohlcv.objects.filter(symbol="ETHUSD", time_frame="1m").update(close=100)
        share = CryptoShareFactory(
            average_price=1, portfolio=portfolio_namespace.portfolio, shares=50.0, symbol_id="ETHUSD"
        )
        form = OrderForm(
            data={
                "symbol": "ETHUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": 50,
                "order_type": "market_order",
                "trade_type": "sell",
            }
        )
        form.full_clean()
        assert form.instance.portfolio.balance == 50000
        assert share.shares == 50
        assert share.average_price == 1

        order = form.save()
        assert order.filled
        assert order.portfolio.balance == 55000

        with pytest.raises(CryptoShare.DoesNotExist):
            portfolio_namespace.portfolio.cryptoshare_set.get(symbol="ETHUSD")

    @pytest.mark.django_db
    def test_clean_shares(self, portfolio_namespace):
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": 0.01,
                "order_type": "market_order",
                "trade_type": "sell",
            }
        )
        form.full_clean()
        assert form.clean_shares() == Decimal("0.01")
        assert form.errors == {}

        form.cleaned_data["shares"] = 0.001
        assert form.clean_shares() == 0.001
        assert form.errors == {"shares": ["Fractional shares cant be lower than 0.01"]}

    @pytest.mark.django_db
    def test_clean_cost_error(self, portfolio_namespace):
        share = portfolio_namespace.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        Ohlcv.objects.filter(symbol="BTCUSD", time_frame="1m").update(close=10000)
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": share.shares,
                "order_type": "market_order",
                "trade_type": "sell",
            }
        )
        form.full_clean()
        assert form.errors == {
            "cost": ["Not enough cash in account balance to fulfill order try using a limit order."],
        }

    @pytest.mark.django_db
    def test_clean_shares_error(self, portfolio_namespace):
        share = portfolio_namespace.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        Ohlcv.objects.filter(symbol="BTCUSD", time_frame="1m").update(close=1)
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": share.shares + Decimal(1),
                "order_type": "market_order",
                "trade_type": "sell",
            }
        )
        form.full_clean()
        assert form.errors == {
            "shares": ["Not enough shares to sell."],
        }

    @pytest.mark.django_db
    def test_clean(self, portfolio_namespace):
        share = portfolio_namespace.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        Ohlcv.objects.filter(symbol="BTCUSD", time_frame="1m").update(close=100000)
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio_namespace.portfolio,
                "shares": share.shares + Decimal(1),
                "order_type": "market_order",
                "trade_type": "sell",
            }
        )
        form.full_clean()
        assert form.errors == {
            "cost": ["Not enough cash in account balance to fulfill order try using a limit order."],
            "shares": ["Not enough shares to sell."],
        }
