from database.call import call
from database.select import select_dict, select_list


def route_create_report(month, year, conf, provider, report_conf):
    result, _, err = route_get_report(month, year, conf, provider, report_conf)

    if err == '' and len(result) > 0:
        return 'Такой отчет уже существует'
    if err != '':
        return err

    _sql = provider.get(report_conf[2], year=year, month=month)
    ok = call(conf, _sql)
    err = ''
    if not ok:
        err = 'Ошибка во время выполнения запроса!'
    return err


def route_get_report(month, year, conf, provider, report_conf):
    _sql = provider.get(report_conf[3], year=year, month=month)
    result, schema, err = select_list(conf, _sql)
    if err != '':
        err = 'Ошибка во время выполнения запроса!'
    if len(result) == 0:
        return result, list(), 'Такого отчета нет!'
    return result, schema, err
