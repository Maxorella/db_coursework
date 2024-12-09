from database.call import call
from database.select import select_list

def route_create_report(month, year, conf, provider, report_conf):
    month = int(month)
    year = int(year)
    _sql = provider.get(report_conf[2], year=year, month=month)
    print(_sql)
    ok = call(conf, _sql)
    err_mes=''
    if not ok:
        err_mes = 'Ошибка во время выполнения запроса!'
    return err_mes

def route_get_report(month, year, conf, provider, report_conf):

    month = int(month)
    year = int(year)
    _sql = provider.get(report_conf[3], year=year, month=month)
    print(_sql)
    result, schema, err = select_list(conf, _sql)
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    return result, schema, err
