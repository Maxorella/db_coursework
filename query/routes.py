from flask import Blueprint, request, render_template, current_app, url_for, redirect
import os
from database.sql_provider import SQLProvider
from access import group_required
from query.model_route import (model_route_query_staff_phone,
                               model_route_query_phone_exceed, model_route_query_staff_exceed)

query_blueprint = Blueprint(
    'query_bp',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_blueprint.route('/', methods=['GET'])
@group_required
def query_menu_handler():
    message = request.args.get('message')
    if message:
        return render_template("query_menu.html", message=message)
    else:
        return render_template("query_menu.html")


@query_blueprint.route('/query_staff_phone', methods=['GET', 'POST'])
@group_required
def query_staff_phone_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':
        return render_template("query_staff_phone.html")

    if request.method == 'POST':
        surname = request.form.get('surname')
        department_id = request.form.get('department_id')
        # staff_info например
        # {'department_id': 1, 'position': 'Системный администратор', 'staff_id': 1, 'surname': 'Admin1'}

        # result например
        # [{'money_limit': Decimal('1500.00'), 'phone': '89051544123'}]
        staff_info, result, error = model_route_query_staff_phone(conf, provider, surname, department_id)
        if error != '':
            return redirect(url_for('query_bp.query_menu_handler', message=error))
        else:
            return render_template("query_staff_phone_result.html", staff_info=staff_info[0], result=result)


@query_blueprint.route('/query_phone_exceed', methods=['GET', 'POST'])
@group_required
def query_phone_exceed_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':
        return render_template("query_phone_exceed.html")

    if request.method == 'POST':
        phone = request.form.get('phone')
        # phone_exceed
        # [{'exceed_amount': Decimal('100.00'), 'exceed_month': 10, 'exceed_year': 2024,
        # 'phone': '89051544125', 'repayment_date': None}]
        phone_exceed, error = model_route_query_phone_exceed(conf, provider, phone)
        if error != '':
            return redirect(url_for('query_bp.query_menu_handler', message=error))
        else:
            return render_template("query_phone_exceed_result.html", phone=phone, phone_exceed=phone_exceed)


@query_blueprint.route('/query_staff_exceed', methods=['GET', 'POST'])
@group_required
def query_staff_exceed_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':
        return render_template("query_staff_exceed.html")

    if request.method == 'POST':
        surname = request.form.get('surname')
        department_id = request.form.get('department_id')
        # staff_info
        # {'department_id': 1, 'position': 'Системный администратор', 'staff_id': 1, 'surname': 'Admin1'}
        # result
        # [{'exceed_amount': Decimal('200.00'), 'exceed_month': 10, 'exceed_year': 2024,
        # 'phone': '89051544123', 'repayment_date': None}]

        staff_info, result, error = model_route_query_staff_exceed(conf, provider, surname, department_id)

        if error != '':
            return redirect(url_for('query_bp.query_menu_handler', message=error))
        else:
            return render_template("query_staff_exceed_result.html",
                                   staff=staff_info, staff_exceed=result, result=result)
