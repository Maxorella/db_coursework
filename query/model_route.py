from database.select import select_dict


# Поиск телефонов по фамилии и отделу сотрудника
def model_route_query_staff_phone(conf, provider, surname, department_id):
    _sql = provider.get('get_staff_by_surname_department.sql', surname=surname, department_id=department_id)
    staff, error = select_dict(conf, _sql)

    if error == "Cursor not created":
        return None, None, "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return None, None, "Возникла ошибка при выполнении запроса!"

    if len(staff) == 0 and error == '':
        return None, None, "Такой сотрудник не найден!"

    if error != '':
        return None, None, error

    _sql = provider.get('get_staff_phones.sql', surname=surname, department_id=department_id)
    phones_dict_list, error = select_dict(conf, _sql)

    if error == "Cursor not created":
        return None, None, "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return None, None, "Возникла ошибка при выполнении запроса!"

    if error != '':
        return None, None, error

    return staff, phones_dict_list, error


# Превышения по телефону
def model_route_query_phone_exceed(db_config, sql_provider, phone):
    _sql = sql_provider.get('get_phone_exceed.sql', phone=phone)
    result, err = select_dict(db_config, _sql)
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err


# Превышения по всем телефонам сотруднику
def model_route_query_staff_exceed(conf, provider, surname, department_id):
    _sql = provider.get('get_staff_by_surname_department.sql', surname=surname, department_id=department_id)
    staff_info, error = select_dict(conf, _sql)
    if error == "Cursor not created":
        return None, None, "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return None, None, "Возникла ошибка при выполнении запроса!"

    if len(staff_info) == 0 and error == '':
        return None, None, "Такой сотрудник не найден!"

    if error != '':
        return None, None, error

    staff_info = staff_info[0]
    _sql = provider.get('get_staff_exceed.sql', staff_id=staff_info['staff_id'])
    result, error = select_dict(conf, _sql)

    if error == "Cursor not created":
        return None, None, "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return None, None, "Возникла ошибка при выполнении запроса!"

    if error != '':
        return None, None, error

    return staff_info, result, error
