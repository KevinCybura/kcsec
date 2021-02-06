import pytest

from kcsec.crypto.client.gemini import GeminiConsumer
from kcsec.crypto.models.factories.order import CryptoOrderFactory
from kcsec.crypto.models.factories.share import CryptoShareFactory


# For each test run `make db` then run the test to see if it pass. There will be one pass and failure if which means it
# passed otherwise they will both fail and the test fails. If both pass then this skip can be removed
@pytest.mark.skip("test fail because no support for clean up")
class TestGeminiConsumer:
    @pytest.mark.django_db(transaction=True)
    def test_fill_buy_orders(self, seed_namespace, event_loop):
        limit_order = CryptoOrderFactory(
            symbol=seed_namespace.seeds.symbols[-1],
            portfolio=seed_namespace.portfolio,
            share=None,
            price=50.0,
            shares=1,
            filled=False,
            trade_type="buy",
            order_type="limit_order",
        )

        candle_message = {"symbol": "LTCUSD", "changes": [{"close": 49}]}
        consumer = GeminiConsumer(None)

        event_loop.run_until_complete(consumer.fill_orders(candle_message))
        limit_order.refresh_from_db()

        assert limit_order.filled
        assert limit_order.share is not None

    @pytest.mark.django_db(transaction=True)
    def test_fill_buy_orders_share_exists(self, seed_namespace, event_loop):
        share = CryptoShareFactory(
            symbol=seed_namespace.seeds.symbols[-1], portfolio=seed_namespace.portfolio, shares=1, average_price=1.0
        )
        limit_order = CryptoOrderFactory(
            symbol=seed_namespace.seeds.symbols[-1],
            portfolio=seed_namespace.portfolio,
            share=share,
            price=50.0,
            shares=1,
            filled=False,
            trade_type="buy",
            order_type="limit_order",
        )

        candle_message = {"symbol": "LTCUSD", "changes": [{"close": 49}]}
        consumer = GeminiConsumer(None)

        event_loop.run_until_complete(consumer.fill_orders(candle_message))
        limit_order.refresh_from_db()
        share.refresh_from_db()

        assert limit_order.filled
        assert share.shares == 2
        assert share.average_price == 25.00

    @pytest.mark.django_db(transaction=True)
    def test_fill_sell_orders(self, seed_namespace, event_loop):
        limit_order = CryptoOrderFactory(
            symbol=seed_namespace.seeds.symbols[-1],
            portfolio=seed_namespace.portfolio,
            share=None,
            price=50.0,
            shares=1,
            filled=False,
            trade_type="sell",
            order_type="limit_order",
        )

        candle_message = {"symbol": "LTCUSD", "changes": [{"close": 51}]}
        consumer = GeminiConsumer(None)

        event_loop.run_until_complete(consumer.fill_orders(candle_message))
        limit_order.refresh_from_db()
        assert limit_order.filled
        assert limit_order.share is not None
