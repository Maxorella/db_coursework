from database.call import call
from database.select import select_list, select_dict, delete_insert


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


def route_delete_phone(provider, conf, phone):
    sql = provider.get('delete_phone.sql', phone=phone)
    error = delete_insert(conf, sql)

    if error == "Cursor not created":
        return "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return "Возникла ошибка при выполнении запроса!"

    if error != '':
        return error

    return ''


def route_add_phone(provider, conf, staff_id, phone, money_limit):
    sql = provider.get('check_phone.sql', phone=phone)
    result, schema, error = select_list(conf, sql)

    if error == "Cursor not created":
        return "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return "Возникла ошибка при выполнении запроса!"

    if error != '':
        return error

    if len(result) != 0:
        return "Такой телефон уже занят!"

    sql = provider.get('add_phone.sql', phone=phone, staff_id=staff_id, money_limit=money_limit)
    error = delete_insert(conf, sql)

    if error == "Cursor not created":
        return "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return "Возникла ошибка при выполнении запроса!"

    if error != '':
        return error

    return ''


def route_edit_staff(provider, conf, staff_id, surname, address, birthday, position, hire_date, department_id):
    sql = provider.get('edit_staff.sql', staff_id=staff_id, surname=surname, address=address, birthday=birthday,
                       position=position, hire_date=hire_date, department_id=department_id)
    error = delete_insert(conf, sql)

    if error == "Cursor not created":
        return "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return "Возникла ошибка при выполнении запроса!"

    if error != '':
        return error

    return ''


def route_delete_staff(provider, conf, staff_id):
    sql = provider.get('delete_staff.sql', staff_id=staff_id)
    error = delete_insert(conf, sql)

    if error == "Cursor not created":
        return "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return "Возникла ошибка при выполнении запроса!"

    if error != '':
        return error

    return ''


def route_add_staff(provider, conf, login, password, user_group, surname, address, birthday, position,
                    hire_date, department_id):
    sql = provider.get('add_staff.sql', login=login, password=password, user_group=user_group,
                       surname=surname, address=address, birthday=birthday, position=position,
                       hire_date=hire_date, department_id=department_id)
    ok = call(conf, sql)
    if not ok:
        return "Произошла ошибка при создании сотрудника!"

    return ''