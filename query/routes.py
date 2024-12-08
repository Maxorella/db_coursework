from flask import Blueprint, request, render_template, current_app, url_for, redirect
import os

from database.sql_provider import SQLProvider
from access import group_required
from query.model_route import staff_exceed_route, fetch_id_phone, fetch_all_staff, fetch_id_staff

query_blueprint = Blueprint(
    'query_bp',
    __name__,
    template_folder='templates',
    static_folder=''
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_blueprint.route('/', methods=['GET'])
@group_required
def query_menu_handler():
    message = request.args.get('message')
    return render_template("query_menu.html", message=message)


@query_blueprint.route('/query_staff_phone', methods=['GET','POST'])
@group_required
def query_staff_phone_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':
        response, err_mes = fetch_all_staff(conf, provider)
        if err_mes != '':
            return render_template("query_staff_phone.html", message=err_mes)
        else:
            return render_template("query_staff_phone.html", staff_list=response)
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        staff_info, err_mes = fetch_id_staff(conf, provider, staff_id)  # [id surname position department_id]
        if err_mes != '':
            return redirect(url_for('query_bp.query_menu_handler', message='err_mes'))
        result, err_mes = fetch_id_phone(conf, provider, staff_info['staff_id'])
        if err_mes != '':
            return redirect(url_for('query_bp.query_menu_handler', message='err_mes'))
        else:
            return render_template("query_staff_phone_result.html", staff_info=staff_info, result=result)


@query_blueprint.route('/query_phone_exceed', methods=['GET','POST'])
@group_required
def query_phone_exceed_handler():
    conf = current_app.config['db_config']

    response, err_mes = fetch_all_staff(conf, provider)
    if err_mes != '':
        return render_template("query_staff_phone.html", message=err_mes)
    else:
        return render_template("query_staff_phone.html", staff_list=response)  # [staff_id, surname, position, department_id]



@query_blueprint.route('/query_phone_payment', methods=['GET','POST'])
@group_required
def query_phone_payment_handler():
    response, err_mes = fetch_all_staff(current_app.config['db_config'], provider)
    if err_mes != '':
        return render_template("query_staff_phone.html", message=err_mes)
    else:
        return render_template("query_staff_phone.html", staff_list=response) # [staff_id, surname, position, department_id]