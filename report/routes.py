from flask import Blueprint, request, render_template, current_app, redirect, url_for
import os
from database.sql_provider import SQLProvider
from access import group_required
from report.model_route import route_get_report, route_create_report
from utils import month_to_string

report_blueprint = Blueprint(
    'report_bp',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@report_blueprint.route('/create_report', methods=['GET', 'POST'])
@group_required
def create_report_handler():
    conf = current_app.config['db_config']
    report_conf = current_app.config['report']

    if request.method == 'GET':
        message = request.args.get('message')
        return render_template('report_choice.html', reports=report_conf, message=message)

    if request.method == 'POST':
        report_type = int(request.form.get('report_type'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))

        error = route_create_report(month, year, conf, provider, report_conf[report_type])
        if error == '':
            return render_template('success.html')
        else:
            return redirect(url_for('report_bp.create_report_handler', message=error))

@report_blueprint.route('/get_report', methods=['GET', 'POST'])
@group_required
def get_report_handler():
    conf = current_app.config['db_config']
    report_conf = current_app.config['report']

    if request.method == 'GET':
        message = request.args.get('message')
        return render_template('report_show_choice.html', reports=report_conf, message=message)

    if request.method == 'POST':
        report_type = int(request.form.get('report_type'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))

        result, schema, error = route_get_report(month, year, conf, provider, report_conf[report_type])
        if error != '':
            return redirect(url_for('report_bp.get_report_handler', message=error))
        else:
            return render_template('staff_exceed_table.html', report_type=report_conf[report_type],
                                   month=month_to_string(month), year=year, report_list_list=result, schema_list=schema)