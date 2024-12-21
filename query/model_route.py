from database.select import select_dict, select_list


def model_route_query_staff_phone(conf, provider, surname, department_id):
    _sql = provider.get('get_staff_by_surname_department.sql', surname=surname, department_id=department_id)
    staff, error = select_dict(conf, _sql)

    if error == "Cursor not created":
        return None, None, "Произошла ошибка при подключении к базе данных!"
    if error.startswith("Error executing SQL query:"):
        return None, None, "Возникла ошибка при выполнении запроса!"

    _sql = provider.get('get_staff_phones.sql', surname=surname, department_id=department_id)
    phones_dict_list, error = select_dict(conf, _sql)

    if error == "Cursor not created":
        return None, None, "Произошла ошибка при подключении к базе данных!"
    if error.startswith("Error executing SQL query:"):
        return None, None, "Возникла ошибка при выполнении запроса!"

    return staff, phones_dict_list, error


def model_route_query_phone_exceed(db_config, sql_provider, phone):
    _sql = sql_provider.get('get_phone_exceed.sql', phone=phone)
    result, err = select_dict(db_config, _sql)
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err


def model_route_query_staff_exceed(conf, provider, surname, department_id):
    _sql = provider.get('get_staff_by_surname_department.sql', surname=surname, department_id=department_id)
    staff_info, err = select_dict(conf, _sql)
    staff_info = staff_info[0]
    if err != '':
        return None, None, 'Во время поиска сотрудника произошла ошибка!'
    _sql = provider.get('get_staff_exceed.sql', staff_id=staff_info['staff_id'])
    result, err = select_dict(conf, _sql)
    if err != '':
        return None, None, 'Во время поиска телефона сотрудника произошла ошибка!'
    return staff_info, result, err
