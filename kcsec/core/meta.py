def get_db_table_name(schema: str, entity: str, provider: str = None) -> str:
    return f'{schema}"."{entity}'
