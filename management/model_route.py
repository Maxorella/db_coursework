from database.select import select_list


def get_report_exceed(month, year, db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('get_report.sql', year=year, month=month)
    result, schema, err = select_list(db_config, _sql)
    if err!='':
        error_message = 'Ошибка во время выполнения запроса!'


    return result, schema, error_message


def route_get_exceed_report(month, year, db_config, sql_provider):

    month = int(month)
    year = int(year)

    result, schema, error_message = get_report_exceed(month, year, db_config, sql_provider)
    return result, schema, error_message
