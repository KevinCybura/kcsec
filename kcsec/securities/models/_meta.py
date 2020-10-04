from kcsec.core.meta import get_db_table_name

SCHEMA = "securities"


def securities_entity(entity: str) -> str:
    return get_db_table_name(SCHEMA, entity)


SYMBOL_TYPE_CHOICES = [
    ("ad", "ad"),
    ("re", "re"),
    ("ce", "ce"),
    ("si", "si"),
    ("lp", "lp"),
    ("cs", "cs"),
    ("et", "et"),
    ("wt", "wt"),
    ("oef", "oef"),
    ("cef", "cef"),
    ("ps", "ps"),
    ("ut", "ut"),
    ("temp", "temp"),
]
