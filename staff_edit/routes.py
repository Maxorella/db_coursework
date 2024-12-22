from flask import Blueprint, request, render_template, current_app, redirect, url_for
import os
from database.sql_provider import SQLProvider
from access import group_required
from report.model_route import route_get_report, route_create_report
from staff_edit.model_route import route_get_active_staff, route_get_staff_by_id, route_get_phones_by_staff_id, \
    route_delete_phone, route_add_phone
from utils import month_to_string

editor_blueprint = Blueprint(
    'editor_bp',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@editor_blueprint.route('/staff_menu', methods=['GET', 'POST'])
@group_required
def staff_menu_editor_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':
        staff, schema, error = route_get_active_staff(provider, conf)
        if error != '': #TODO
            return redirect(url_for('main_menu_handler', message=error))

        return render_template('staff_menu.html',schema_list=schema, staff_list_list=staff)
    if request.method == 'POST':
        pass
        # Создать сотрудника

@editor_blueprint.route('/edit_staff', methods=['GET', 'POST'])
@group_required
def staff_editor_handler():
    conf = current_app.config['db_config']
    if request.method == 'GET':
        staff_id = int(request.args.get('staff_id'))
        staff_info, schema_staff, error = route_get_staff_by_id(provider, conf, staff_id)
        if error != '': #TODO
            return redirect(url_for('main_menu_handler', message=error))

        phones_list, schema_phone, error = route_get_phones_by_staff_id(provider, conf, staff_id)
        if error != '': #TODO
            return redirect(url_for('main_menu_handler', message=error))

        return render_template('staff_and_phone_editor.html',
                               schema_staff_list=schema_staff, staff_list_info=staff_info,
                               schema_phones_list=schema_phone, phones_list_list=phones_list)
    if request.method == 'POST':
        pass
        # Редактировать сотрудника

@editor_blueprint.route('/delete_phone', methods=['POST'])
@group_required
def delete_phone_handler():
    conf = current_app.config['db_config']

    if request.method == 'POST':
        staff_id = int(request.args.get('staff_id'))
        phone = int(request.args.get('phone'))
        error = route_delete_phone(provider, conf, phone)
        if error != '': #TODO
            return redirect(url_for('main_menu_handler', message=error))

        return redirect(url_for('editor_bp.staff_editor_handler', staff_id=staff_id))  # TODO message

@editor_blueprint.route('/add_phone', methods=['POST'])
@group_required
def add_phone_handler():
    conf = current_app.config['db_config']

    if request.method == 'POST':
        staff_id = int(request.args.get('staff_id'))
        phone = int(request.form.get('phone'))
        money_limit = int(request.form.get('money_limit'))
        error = route_add_phone(provider, conf, staff_id, phone, money_limit)

        if error != '': #TODO
            return redirect(url_for('main_menu_handler', message=error))

        return redirect(url_for('editor_bp.staff_editor_handler', staff_id=staff_id))  # TODO message
