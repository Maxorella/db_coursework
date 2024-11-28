from database.call import call


def create_report_exceed(month, year, db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('create_report.sql', year=year, month=month)

    ok = call(db_config, _sql)
    if not ok:
        error_message = 'Ошибка во время выполнения запроса!'
    return error_message

def route_create_exceed_report(month, year, db_config, sql_provider):

    month = int(month)
    year = int(year)

    err_mes = create_report_exceed(month, year, db_config, sql_provider)
    return err_mes