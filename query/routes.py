from flask import Blueprint, request, render_template, redirect, session, url_for, current_app
import os

from auth.select import select_user
from database.sql_provider import SQLProvider
from access import group_required
from query.model_route import fetch_staff, staff_exceed_route

query_blueprint = Blueprint(
    'query_bp',
    __name__,
    template_folder='templates',
    static_folder=''
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_blueprint.route('/', methods=['GET'])
@group_required
def staff_query_handler():
    response, err_mes = fetch_staff(current_app.config['db_config'], provider)
    if err_mes != '':
        return render_template("input_staff.html", message=err_mes)
    else:
        return render_template("input_staff.html", staff_list=response) # [staff_id, surname, position]

@query_blueprint.route('/staff_exceed', methods=['GET'])
@group_required
def staff_query_result_handler():
    staff_id = request.args.get('staff_id')


    staff_info, staff_exceed, err_mes = staff_exceed_route(staff_id, current_app.config['db_config'], provider)
    print(staff_info)

    print(staff_exceed)
    # staff_info ([staff_id, user_group, surname, position, hire_date, department_id])
    # staff_exceed ([phone, exceed_amount, exceed_month, exceed_year, repayment_date(always NULL) ], ...)
    if err_mes != '':
        return render_template("exceed_staff.html", message=err_mes)
    else:
        return render_template("exceed_staff.html", staff_info=staff_info[0], staff_exceed=staff_exceed)