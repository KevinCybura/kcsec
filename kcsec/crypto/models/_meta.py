from kcsec.core.meta import get_db_table_name

SCHEMA = "crypto"


def crypto_entity(entity: str) -> str:
    return get_db_table_name(SCHEMA, entity)
