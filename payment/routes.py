from flask import Blueprint, request, render_template, redirect, session, url_for, current_app
import os

from database.sql_provider import SQLProvider
from access import group_required
from payment.model_route import pay_exceed_route
from query.model_route import staff_exceed_route

payment_blueprint = Blueprint(
    'payment_bp',
    __name__,
    template_folder='templates',
    static_folder=''
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@payment_blueprint.route('/', methods=['GET'])
@group_required
def staff_debt_check_handler():
    message = request.args.get('message')

    staff_id = session.get('user_id',"")
    if not staff_id:
        return render_template('check_exceed.html', message="Ошибка определения пользователя!")
    staff_info, staff_exceed, err_mes = staff_exceed_route(staff_id, current_app.config['db_config'], provider)

    # staff_info ([staff_id, user_group, surname, position, hire_date, department_id])
    # staff_exceed ([phone, exceed_amount, exceed_month, exceed_year, repayment_date(always NULL) ], ...)

    if err_mes != '':
        return render_template("check_exceed.html", message=err_mes)
    else:
        if message is not None:
            return render_template("check_exceed.html", staff_info=staff_info[0], staff_exceed=staff_exceed, message=message)
        return render_template("check_exceed.html", staff_info=staff_info[0], staff_exceed=staff_exceed)

@payment_blueprint.route('/pay_exceed', methods=['POST'])
@group_required
def staff_pay_handler():
    selected_exceed = request.form.get('selected_exceed')

    if selected_exceed:
        phone, month, year = selected_exceed.split('|')
        month = int(month)
        year = int(year)
    else:
        return redirect(url_for('payment_bp.staff_debt_check_handler', message="Не выбрана задолженность для погашения!"))

    err_mes = pay_exceed_route(phone, month, year, current_app.config['db_config'], provider)

    if err_mes != '':
        return redirect(url_for('payment_bp.staff_debt_check_handler', message="message!"))
    else:
        return render_template("success_pay.html")