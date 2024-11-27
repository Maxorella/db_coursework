from database.select import select_list

def fetch_staff(db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('get_staff.sql')
    result, _, err = select_list(db_config, _sql) # ([staff_id, surname, position],[staff_id, surname, position])
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, err


def fetch_staff_exceed(staff_id, db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('get_staff_exceed.sql', staff_id=staff_id)
    result, _, err = select_list(db_config, _sql)
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