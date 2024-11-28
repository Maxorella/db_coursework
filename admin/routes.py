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

@admin_blueprint.route('/create_report', methods=['GET', 'POST'])
@group_required
def admin_report_handler():
    conf = current_app.config['db_config']
    provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

    if request.method == 'GET':
        # Выводим страницу с формой для добавления данных
        message = request.args.get('message')
        return render_template('add_number_summ.html', message=message)

    if request.method == 'POST':
        # Получаем данные с формы
        report_year = request.form.get('report_year')
        report_month = request.form.get('report_month')
        phone_number = request.form.get('phone_number')
        amount = request.form.get('amount')

        # Преобразуем сумму в число с плавающей точкой
        try:
            amount = float(amount)
        except ValueError:
            flash("Неверный формат суммы!")
            return redirect(url_for('admin_bp.admin_report_handler', message='Неверный формат суммы!'))

        # Проверим, что все поля заполнены корректно
        if not phone_number or not amount or not report_year or not report_month:
            flash("Пожалуйста, заполните все поля!")
            return redirect(url_for('admin_bp.admin_report_handler', message='Пожалуйста, заполните все поля!'))

        sql = provider.get('add_phone_summ.sql', phone=phone_number, amount=amount, year=report_year, month=report_month) # запрос (sql)

        schema, result, err = save_report(conf, sql)
        if err != '':
            return redirect(url_for('admin_bp.admin_report_handler', message='Произошла ошибка при добавлении!'))
        print(f"Ошибка: {err}")
        flash(f"Данные для телефона {phone_number} на сумму {amount} успешно добавлены за {report_month}/{report_year}!")
        return redirect(url_for('admin_bp.admin_report_handler', message=f'данные о телефоне {phone_number} за {report_month}/{report_year} добавлены'))




@admin_blueprint.route('/generate_report', methods=['POST'])
def generate_report_handler():
    conf = current_app.config['db_config']
    provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

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