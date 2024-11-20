import json

from flask import Blueprint, request, render_template, flash, redirect, session, url_for, current_app
import os

from internal.auth.select import select_user
from internal.database.sql_provider import SQLProvider

from internal.database.DBcm import DBContextManager

auth_blueprint = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
    static_folder=''
)

@auth_blueprint.route('/', methods=['GET', 'POST'])
def auth_handler():
    conf = current_app.config['db_config']
    provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

    if request.method == 'GET': # если пользователь уже зареган - редирект на меню
        if 'user_id' in session:
            return redirect(url_for('', ))

        message = request.args.get('message') # если не зареган - страничка авторизации
        if message is None:
            message = 'Войдите в аккаунт.'

        return render_template('input_login.html', message=message)

    elif request.method == 'POST':
        login = request.form.get('login', '') # логин с формы
        password = request.form.get('password', '') # пароль с формы

        sql = provider.get('select_user.sql', login=login, password=password) # запрос (sql)

        result, schema, error = select_user(conf, sql) # модель

        if error == "Cursor not created":
            return redirect(url_for('auth_bp.auth_handler', message="Произошла внутренняя ошибка!"))
        if error == "Error executing SQL query":
            return redirect(url_for('auth_bp.auth_handler', message="Ошибка при выполнении запроса!"))

        if result:
            session['user_id'] = result[0][0]
            session['login'] = result[0][1]
            session['password'] = result[0][2]
            session['user_group'] = result[0][3]
            session.permanent = True
            return redirect(url_for('main_menu_handler', message = f"Вы ${session.get('user_group')}"))
        else:
            return redirect(url_for('auth_bp.auth_handler', message="Неправильный логин или пароль!"))