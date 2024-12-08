from database.select import select_list, select_dict


def fetch_all_staff(db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('get_all_staff.sql')
    result, err = select_dict(db_config, _sql) # ([staff_id, surname, position, department_id],[staff_id, surname, position, department_id])
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err

def fetch_all_phones(db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('get_all_phones.sql')
    result, err = select_dict(db_config, _sql)
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err


def fetch_id_phone(db_config, sql_provider, staff_id):
    error_message = ''
    _sql = sql_provider.get('get_staff_phones.sql', staff_id=staff_id)
    result, err = select_dict(db_config, _sql)  # ([])
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err

def fetch_id_staff(db_config, sql_provider, staff_id):
    error_message = ''
    _sql = sql_provider.get('get_staff_by_id.sql', staff_id=staff_id)
    result, err = select_dict(db_config, _sql)
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
        return None, err
    return result[0], err


def fetch_phone_exceed(db_config, sql_provider, phone):
    error_message = ''
    _sql = sql_provider.get('get_phone_exceed.sql', phone=phone)
    result, err = select_dict(db_config, _sql)
    # ([phone, exceed_amount, exceed_month, exceed_year, repayment_date(always NULL) ], ...)

    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err


def fetch_staff_exceed(db_config, sql_provider,staff_id):
    error_message = ''
    _sql = sql_provider.get('get_staff_exceed.sql', staff_id=staff_id)
    result, err = select_dict(db_config, _sql)
    # ([phone, exceed_amount, exceed_month, exceed_year, repayment_date(always NULL) ], ...)

    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err


def fetch_staff_info(staff_id, db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('get_staff_info.sql', staff_id=staff_id)

    result, _, err = select_list(db_config, _sql) # ([staff_id, user_group, surname, position, hire_date, department_id])
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err

def staff_exceed_route(staff_id, db_config, sql_provider):

    if not staff_id:
        return None, None, "Не выбран сотрудник!"

    staff_info, err_mes = fetch_staff_info(staff_id, db_config, sql_provider)
    if err_mes != '':
        return None, None, "Ошибка во время получения информации о сотруднике!"

    staff_exceed, err_mes = fetch_staff_exceed(staff_id, db_config, sql_provider)
    if err_mes != '':
        return None, None, "Ошибка во время получения информации о задолженностях сотрудника!"
    return staff_info, staff_exceed, err_mes