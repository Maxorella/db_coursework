from flask import Blueprint, request, render_template, current_app, redirect, url_for
import os

from database.sql_provider import SQLProvider
from access import group_required
from query.model_route import fetch_staff, staff_exceed_route
from report.model_route import route_create_exceed_report

report_blueprint = Blueprint(
    'report_bp',
    __name__,
    template_folder='templates',
    static_folder=''
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@report_blueprint.route('/', methods=['GET', 'POST'])
@group_required
def report_handler():
    if request.method == 'GET':
        message = request.args.get('message')

        return render_template('report_choice.html', message=message) # [staff_id, surname, position]
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        month = request.form.get('month')
        year = request.form.get('year')

        if report_type == '1':
            #TODO
            ok = route_create_exceed_report(month,year, current_app.config['db_config'], provider)
            if not ok:
                return render_template('success.html')
            else:
                return redirect(url_for('report_bp.report_handler', message='Ошибка при создании отчета!'))
        return redirect(url_for('report_bp.report_handler', message='Ошибка в выборе отчета!'))
