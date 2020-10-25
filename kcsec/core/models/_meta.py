from kcsec.core.meta import get_db_table_name

SCHEMA = "core"


def core_entity(entity: str) -> str:
    return get_db_table_name(SCHEMA, entity)
