from database.DBcm import DBContextManager

def select_user(db_config: dict, _sql: str):
    result, schema, err = '', '', ''

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            err = "Cursor not created"
            raise ValueError(err)
        try:
            cursor.execute(_sql)
            result = cursor.fetchall()
            schema = [item[0] for item in cursor.description]
        except Exception as e:
            err = "Error executing SQL query"
            result = ''
            schema = ''

    return result, schema, err
