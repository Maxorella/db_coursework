# функции связанные с выполнением запроса в базу данных
from database.DBcm import DBContextManager


def select_list(db_config: dict, _sql: str):
    result, schema, err = '', '', ''
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            err = 'Cursor not created'
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
                result = cursor.fetchall()
                schema = [item[0] for item in cursor.description]
            except Exception as e:
                err = f"Error executing SQL query: {e}"
                result = ''
                schema = ''

    return result, schema, err


def select_dict(db_config: dict, _sql: str):
    result, schema, err = select_list(db_config, _sql)
    if err != '':
        return None, err
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict, ''


def delete_insert(db_config: dict, _sql: str):
    err = ''
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            err = 'Cursor not created'
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
                cursor.connection.commit()
            except Exception as e:
                err = f"Error executing SQL query: {e}"
                cursor.connection.rollback()
                return err
    return ''
