from types import SimpleNamespace

import pytest

from kcsec.core.models.factories.portfolio import PortfolioFactory
from kcsec.crypto.models.factories.order import CryptoOrderFactory
from kcsec.crypto.models.factories.share import CryptoShareFactory
from kcsec.crypto.seeds import crypto_seed


@pytest.fixture
def crypto_seeds():
    currency = crypto_seed(["BTC", "ETH", "LTC"], create_ohlcv=True)
    return currency


@pytest.fixture
def portfolio(crypto_seeds):
    portfolio = PortfolioFactory()
    share = CryptoShareFactory(portfolio=portfolio, shares=50.0, crypto_symbol=crypto_seeds.symbols[0])
    orders = [
        CryptoOrderFactory(share=share, shares=10.0, portfolio=portfolio, crypto_symbol=crypto_seeds.symbols[0])
        for _ in range(5)
    ]
    return SimpleNamespace(portfolio=portfolio, share=share, order=orders)


@pytest.fixture
def trade_view_request():
    return SimpleNamespace(
        method="POST", POST={"crypto_symbol": "BTCUSD"}, FILES={}, user=SimpleNamespace(is_authenticated=False)
    )


@pytest.fixture
def trade_view_request_authenticated(portfolio):
    return SimpleNamespace(
        method="POST",
        POST={"crypto_symbol": "BTCUSD"},
        FILES={},
        user=SimpleNamespace(is_authenticated=True, portfolio=portfolio.portfolio),
    )
