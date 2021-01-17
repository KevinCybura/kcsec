from types import SimpleNamespace

from kcsec.crypto.models import Asset
from kcsec.crypto.models import Exchange
from kcsec.crypto.models import Symbol


def crypto_seed(
    crypto_currencies: list[str], asset: str = "USD", exchange: str = "gemini", create_ohlcv: bool = False
) -> SimpleNamespace:
    quote = Asset.objects.create(asset_id=asset)
    exchange = Exchange.objects.create(exchange_id=exchange)
    seeds = SimpleNamespace(exchange=exchange, asset=asset, symbols=[])
    for currency in crypto_currencies:
        base = Asset.objects.create(asset_id=currency)
        symbol = Symbol.objects.create(
            id=base.pk + quote.pk, asset_id_base=base, asset_id_quote=quote, exchange=exchange, price=1.0
        )
        if create_ohlcv:
            from kcsec.crypto.models.factories.ohlcv import OhlcvFactory

            OhlcvFactory(symbol=symbol, exchange=exchange, asset_id_base=base, asset_id_quote=quote, time_frame="1m")

        seeds.symbols.append(symbol)

    return seeds
