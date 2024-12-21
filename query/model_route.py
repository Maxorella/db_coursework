from database.select import select_dict

def model_route_query_phone_exceed(db_config, sql_provider, phone):
    _sql = sql_provider.get('get_phone_exceed.sql', phone=phone)
    result, err = select_dict(db_config, _sql)
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err

def model_route_query_staff_exceed(conf, provider, user_input):
    _sql = provider.get('get_staff_by_surname_department.sql', surname=user_input[0], department_id=user_input[1])
    staff_info, err = select_dict(conf, _sql)
    staff_info = staff_info[0]
    if err!='':
        return None, None, 'Во время поиска сотрудника произошла ошибка!'
    _sql = provider.get('get_staff_exceed.sql', staff_id=staff_info['staff_id'])
    result, err = select_dict(conf, _sql)
    if err!='':
        return None, None, 'Во время поиска телефона сотрудника произошла ошибка!'
    return staff_info, result, err

def model_route_query_staff_phone(conf, provider, surname, department_id):
    _sql = provider.get('get_staff_by_surname_department.sql', surname=surname, department_id=department_id)
    staff, err = select_dict(conf, _sql)
    if err != '':
        return None, None, 'Ошибка во время поиска сотрудника!'

    _sql = provider.get('get_staff_phones.sql', surname=surname, department_id=department_id)
    phones_dict_list, err = select_dict(conf, _sql)
    if err != '':
        return None, None, 'Ошибка во время выполнения запроса!'
    return staff, phones_dict_list, err