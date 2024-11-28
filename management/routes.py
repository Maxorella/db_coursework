from flask import Blueprint, request, render_template, current_app, redirect, url_for
import os

from database.sql_provider import SQLProvider
from access import group_required
from management.model_route import route_get_exceed_report

management_blueprint = Blueprint(
    'management_bp',
    __name__,
    template_folder='templates',
    static_folder=''
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@management_blueprint.route('/', methods=['GET', 'POST'])
@group_required
def management_handler():
    if request.method == 'GET':
        message = request.args.get('message')

        return render_template('report_show_choice.html', message=message)
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        month = request.form.get('month')
        year = request.form.get('year')
        # ([staff_id, surname, position, total_exceed_amount, report_month, report_year ], ...)

        if report_type == '1':
            #TODO
            result, schema, error_message = route_get_exceed_report(month, year, current_app.config['db_config'], provider)
            if error_message!='':
                return redirect(url_for('report_bp.report_handler', message='Ошибка при получении отчета!'))
            else:
                return render_template('stuff_exceed_table.html', exceed_report=result)

        return redirect(url_for('report_bp.report_handler', message='Ошибка в выборе отчета для просмотра!'))