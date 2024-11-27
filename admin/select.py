from database.DBcm import DBContextManager

def save_report(db_config: dict, _sql: str):
    result, schema, err = '', '', ''

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            err = "Cursor not created"
            raise ValueError(err)
        try:
            cursor.execute(_sql)
        except Exception as e:
            err = "Error executing SQL query"
            result = ''
            schema = ''

    return result, schema, err


def create_exceed_report(db_config: dict, _sql: str):
    result, schema, err = '', '', ''

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            err = "Cursor not created"
            raise ValueError(err)
        try:
            cursor.execute(_sql)
        except Exception as e:
            err = "Error executing SQL query"
            result = ''
            schema = ''

    return result, schema, err