import datetime

from database.select import select_list
from database.update import update
def exceed_update(phone, month, year, date, db_config, sql_provider):
    err_mes=''
    _sql = sql_provider.get('update_exceed.sql', phone=phone, month=month, year=year, date=date)
    ok = update(db_config, _sql)
    if ok:
        return ''
    else:
        return 'Ошибка во время выполнения запроса!'

def pay_exceed_route(phone, month, year, db_config, sql_provider):
    date = datetime.datetime.now().strftime('%Y-%m-%d')  # Форматируем дату в 'YYYY-MM-DD'

    err_mes = exceed_update(phone, month, year, date, db_config, sql_provider)
    if err_mes != '':
        return "Ошибка при обновлении статуса задолженности!"
    return ''