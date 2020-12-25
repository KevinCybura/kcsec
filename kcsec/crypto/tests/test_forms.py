import datetime
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from kcsec.crypto.forms import OrderForm
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.models.factories.ohlcv import OhlcvFactory


class TestOrderForm:
    @pytest.mark.django_db
    def test_clean_trade_type(self, portfolio):
        share = portfolio.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio.portfolio,
                "shares": share.shares,
                "order_type": "market_order",
                "trade_type": "sell",
                "price": Decimal(100.0),
            }
        )
        form.full_clean()
        assert form.clean_trade_type() == "sell"

    @pytest.mark.django_db
    def test_clean_trade_type_error(self, portfolio):
        share = portfolio.portfolio.cryptoshare_set.get(symbol="BTCUSD")
        form = OrderForm(
            data={
                "symbol": "BTCUSD",
                "portfolio": portfolio.portfolio,
                "shares": share.shares + Decimal(1),
                "order_type": "market_order",
                "trade_type": "sell",
                "price": Decimal(100.0),
            }
        )
        form.full_clean()
        assert form.errors == {"trade_type": ["Not enough shares to sell."]}
