from types import SimpleNamespace

import pytest
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from kcsec.core.models.factories.portfolio import PortfolioFactory
from kcsec.crypto.models.factories.order import CryptoOrderFactory
from kcsec.crypto.models.factories.share import CryptoShareFactory
from kcsec.crypto.seeds import crypto_seed


@pytest.fixture
def crypto_seeds():
    currency = crypto_seed(["BTC", "ETH", "LTC"], create_ohlcv=True)
    return currency


@pytest.fixture
def portfolio_namespace(crypto_seeds):
    portfolio = PortfolioFactory(balance=50000)
    share = CryptoShareFactory(portfolio=portfolio, shares=50.0, symbol=crypto_seeds.symbols[0])
    orders = [
        CryptoOrderFactory(share=share, shares=10.0, portfolio=portfolio, symbol=crypto_seeds.symbols[0])
        for _ in range(5)
    ]
    return SimpleNamespace(portfolio=portfolio, share=share, order=orders)


@pytest.fixture
def seed_namespace():
    seeds = crypto_seed(["BTC", "ETH", "LTC"], create_ohlcv=True)
    portfolio = PortfolioFactory(balance=50000)
    share = CryptoShareFactory(portfolio=portfolio, shares=50.0, symbol=seeds.symbols[0])
    orders = [
        CryptoOrderFactory(share=share, shares=10.0, portfolio=portfolio, symbol=seeds.symbols[0]) for _ in range(5)
    ]
    return SimpleNamespace(portfolio=portfolio, share=share, order=orders, seeds=seeds)


@pytest.fixture
def trade_view_request():
    return SimpleNamespace(
        method="POST",
        GET={"symbol": "BTCUSD"},
        POST={"symbol": "BTCUSD"},
        FILES={},
        user=AnonymousUser(),
    )


@pytest.fixture
def trade_view_request_authenticated(portfolio_namespace):
    return SimpleNamespace(
        method="POST",
        GET={"symbol": "BTCUSD"},
        POST={"symbol": "BTCUSD"},
        FILES={},
        user=SimpleNamespace(is_authenticated=True, portfolio=portfolio_namespace.portfolio),
    )
