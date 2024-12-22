from database.select import select_list, select_dict


def route_get_active_staff(provider, conf):

    sql = provider.get('get_all_active_staff.sql')
    result, schema, error = select_list(conf, sql)

    if error == "Cursor not created":
        return list(), list(), "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return list(), list(), "Возникла ошибка при выполнении запроса!"

    if len(result) == 0 and error == '':
        return list(), list(), "Не было найдено сотрудников!"

    if error != '':
        return list(), list(), error

    return result, schema, error


def route_get_staff_by_id(provider, conf, staff_id):

    sql = provider.get('get_staff_info.sql', staff_id=staff_id)
    result, schema, error = select_list(conf, sql)

    if error == "Cursor not created":
        return list(), list(), "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return list(), list(), "Возникла ошибка при выполнении запроса!"

    if len(result) == 0 and error == '':
        return list(), list(), "Сотрудник не найден!"

    if error != '':
        return list(), list(), error

    return result, schema, error


def route_get_phones_by_staff_id(provider, conf, staff_id):

    sql = provider.get('get_staff_phones.sql', staff_id=staff_id)
    result, schema, error = select_list(conf, sql)

    if error == "Cursor not created":
        return list(), list(), "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return list(), list(), "Возникла ошибка при выполнении запроса!"

    if error != '':
        return list(), list(), error

    return result, schema, error
