from psqlextra.manager import PostgresManager

from kcsec.crypto.models.querysets.ohlcv import OhlcvQuerySet
from kcsec.crypto.models.querysets.symbol import SymbolQuerySet


class OhlcvManager(PostgresManager.from_queryset(OhlcvQuerySet)):
    def get_queryset(self):
        return OhlcvQuerySet(self.model, using=self.db)


class SymbolManager(PostgresManager.from_queryset(SymbolQuerySet)):
    def get_queryset(self):
        return SymbolQuerySet(self.model, using=self.db)
