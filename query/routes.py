from flask import Blueprint, request, render_template, current_app, url_for, redirect
import os

from database.sql_provider import SQLProvider
from access import group_required
from query.model_route import model_route_query_staff_phone, model_route_query_phone_exceed, model_route_query_staff_exceed

query_blueprint = Blueprint(
    'query_bp',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_blueprint.route('/', methods=['GET'])
@group_required
def query_menu_handler():
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
        staff_info, result, err_mes = model_route_query_staff_phone(conf, provider, surname, department_id)
        if err_mes != '':
            return redirect(url_for('query_bp.query_menu_handler', message=err_mes))
        else:
            return render_template("query_staff_phone_result.html", staff_info=staff_info, result=result)


@query_blueprint.route('/query_phone_exceed', methods=['GET', 'POST'])
@group_required
def query_phone_exceed_handler():
    conf = current_app.config['db_config']
    if request.method == 'GET':
        return render_template("query_phone_exceed.html")
    if request.method == 'POST':
        phone = request.form.get('phone')
        result, err_mes = model_route_query_phone_exceed(conf, provider, phone)
        if err_mes != '':
            return redirect(url_for('query_bp.query_menu_handler', message=err_mes))
        else:
            return render_template("query_phone_exceed_result.html", phone=phone, phone_exceed=result, result=result)


@query_blueprint.route('/query_staff_exceed', methods=['GET', 'POST'])
@group_required
def query_staff_exceed_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':
        return render_template("query_staff_exceed.html")
    if request.method == 'POST':
        surname = request.form.get('surname')
        department_id = request.form.get('department_id')
        user_input = (surname, department_id)
        staff_info, result, err_mes = model_route_query_staff_exceed(conf, provider, user_input)
        if err_mes != '':
            return redirect(url_for('query_bp.query_staff_exceed_handler', message=err_mes))
        else:
            return render_template("query_staff_exceed_result.html", staff=staff_info, staff_exceed=result, result=result)