from psqlextra.manager import PostgresManager

from kcsec.crypto.models._querysets import OhlcvQuerySet


class OhlcvManager(PostgresManager.from_queryset(OhlcvQuerySet)):
    def get_queryset(self):
        return OhlcvQuerySet(self.model, using=self.db)
