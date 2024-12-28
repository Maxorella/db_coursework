from flask import Blueprint, request, render_template, current_app, redirect, url_for
import os
from database.sql_provider import SQLProvider
from access import group_required
from report.model_route import route_get_report, route_create_report
from staff_edit.model_route import route_get_active_staff, route_get_staff_by_id, route_get_phones_by_staff_id, \
    route_delete_phone, route_add_phone, route_edit_staff, route_delete_staff, route_add_staff
from utils import month_to_string

editor_blueprint = Blueprint(
    'editor_bp',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@editor_blueprint.route('/staff_menu', methods=['GET'])
@group_required
def staff_menu_editor_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':
        staff, schema, error = route_get_active_staff(provider, conf)
        if error != '':
            return redirect(url_for('main_menu_handler', message=error))

        message = request.args.get('message')
        if message:
            return render_template('staff_menu.html',schema_list=schema, staff_list_list=staff, message=message)
        else:
            return render_template('staff_menu.html',schema_list=schema, staff_list_list=staff)


@editor_blueprint.route('/staff_phone_menu', methods=['GET'])
@group_required
def staff_editor_handler():
    conf = current_app.config['db_config']
    if request.method == 'GET':
        staff_id = int(request.args.get('staff_id'))
        staff_info, schema_staff, error = route_get_staff_by_id(provider, conf, staff_id)
        if error != '':
            return redirect(url_for('editor_bp.staff_menu_editor_handler', message=error))

        phones_list, schema_phone, error = route_get_phones_by_staff_id(provider, conf, staff_id)
        if error != '':
            return redirect(url_for('editor_bp.staff_menu_editor_handler', message=error))

        message = request.args.get('message')
        return render_template('staff_and_phone_editor.html',
                               schema_staff_list=schema_staff, staff_list_info=staff_info,
                               schema_phones_list=schema_phone, phones_list_list=phones_list, message=message)

@editor_blueprint.route('/delete_phone', methods=['POST'])
@group_required
def delete_phone_handler():
    conf = current_app.config['db_config']

    if request.method == 'POST':
        staff_id = int(request.args.get('staff_id'))
        phone = int(request.args.get('phone'))
        error = route_delete_phone(provider, conf, phone)
        if error != '':
            return redirect(url_for('editor_bp.staff_editor_handler', staff_id=staff_id, message=error))

        return redirect(url_for('editor_bp.staff_editor_handler', staff_id=staff_id, message='Телефон удален'))

@editor_blueprint.route('/add_phone', methods=['POST'])
@group_required
def add_phone_handler():
    conf = current_app.config['db_config']

    if request.method == 'POST':
        staff_id = int(request.args.get('staff_id'))
        phone = int(request.form.get('phone'))
        money_limit = int(request.form.get('money_limit'))
        error = route_add_phone(provider, conf, staff_id, phone, money_limit)

        if error != '':
            return redirect(url_for('editor_bp.staff_editor_handler', staff_id=staff_id, message=error))

        return redirect(url_for('editor_bp.staff_editor_handler', staff_id=staff_id, message='Телефон создан!'))


@editor_blueprint.route('/edit_staff', methods=['POST'])
@group_required
def edit_staff_handler():
    conf = current_app.config['db_config']

    surname = request.form.get('surname')
    address = request.form.get('address')
    birthday = request.form.get('birthday')
    position = request.form.get('position')
    hire_date = request.form.get('hire_date')
    department_id = request.form.get('department_id')

    staff_id = int(request.args.get('staff_id'))
    error = route_edit_staff(provider, conf, staff_id, surname, address,
                                 birthday, position, hire_date, department_id)

    if error != '':
        return redirect(url_for('editor_bp.staff_editor_handler', message=error))

    return redirect(url_for('editor_bp.staff_editor_handler', staff_id=staff_id, message='Сотрудник отредактирован!'))


@editor_blueprint.route('/delete_staff', methods=['GET', 'POST'])
@group_required
def delete_staff_handler():
    conf = current_app.config['db_config']

    staff_id = int(request.args.get('staff_id'))
    error = route_delete_staff(provider, conf, staff_id)

    if error != '':
        return redirect(url_for('editor_bp.staff_menu_editor_handler', message=error))

    return redirect(url_for('editor_bp.staff_menu_editor_handler', message='Сотрудник удален!'))


@editor_blueprint.route('/create_staff', methods=['POST'])
@group_required
def create_staff_handler():
    conf = current_app.config['db_config']
    login = request.form.get('login')
    password = request.form.get('password')
    user_group = request.form.get('user_group')
    surname = request.form.get('surname')
    address = request.form.get('address')
    birthday = request.form.get('birthday')
    position = request.form.get('position')
    hire_date = request.form.get('hire_date')
    department_id = int(request.form.get('department_id'))

    error = route_add_staff(provider, conf, login, password, user_group, surname, address, birthday, position,
                            hire_date, department_id)

    if error != '':
        return redirect(url_for('editor_bp.staff_menu_editor_handler', message=error))

    return redirect(url_for('editor_bp.staff_menu_editor_handler', message='Сотрудник создан!'))