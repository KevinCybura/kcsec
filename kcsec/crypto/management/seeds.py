from types import SimpleNamespace

from kcsec.crypto.models.factories.asset import AssetFactory
from kcsec.crypto.models.factories.exchange import ExchangeFactory
from kcsec.crypto.models.factories.ohlcv import OhlcvFactory
from kcsec.crypto.models.factories.symbol import SymbolFactory


def crypto_seed(
    crypto_currencies: list[str], asset: str = "USD", exchange: str = "gemini", create_ohlcv: bool = False
) -> SimpleNamespace:
    quote = AssetFactory(asset_id=asset)
    exchange = ExchangeFactory(exchange_id=exchange)
    seeds = SimpleNamespace(exchange=exchange, asset=asset, symbols=[])
    for currency in crypto_currencies:
        base = AssetFactory(asset_id=currency)
        symbol = SymbolFactory(
            symbol_id=base.pk + quote.pk,
            asset_id_base=base,
            asset_id_quote=quote,
            exchange=exchange,
        )
        if create_ohlcv:
            OhlcvFactory(exchange=exchange, asset_id_base=base, asset_id_quote=quote)

        seeds.symbols.append(symbol)

    return seeds
