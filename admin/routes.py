from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
import os

from admin.select import save_report, create_exceed_report
from database.sql_provider import SQLProvider

from access import group_required

admin_blueprint = Blueprint(
    'admin_bp',
    __name__,
    template_folder='templates',
    static_folder=''
)


@admin_blueprint.route('/generate_report', methods=['POST'])
def generate_report_handler():
    provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
    conf = current_app.config['db_config']
    report_type = request.form.get('report_type')
    report_year = int(request.form.get('report_year'))
    report_month = int(request.form.get('report_month'))

    # Вызов соответствующего метода для генерации отчета
    if report_type == 'exceed_report':
        # Логика для общего отчета о превышениях
        sql = provider.get('exceed_report.sql', year=report_year, month=report_month) # запрос (sql)
    elif report_type == 'paid_exceed_report':
        # Логика для отчета об оплаченных превышениях
        sql = provider.get('paid_exceed_report.sql', year=report_year, month=report_month) # запрос (sql)
    else:
        flash('Неизвестный тип отчета!', 'error')


    schema, result, err = create_exceed_report(conf, sql)
    if err != '':
        return redirect(url_for('admin_bp.choose_report', message='Произошла ошибка!'))

    return redirect(url_for('admin_bp.choose_report'))

@admin_blueprint.route('/choose_report')
def choose_report_handler():
    return render_template('choose_report.html')