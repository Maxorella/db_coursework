from flask import Blueprint, request, render_template, redirect, session, url_for, current_app
import os

from auth.model_route import auth_route
from auth.select import select_user
from database.sql_provider import SQLProvider

auth_blueprint = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
)



@auth_blueprint.route('/', methods=['GET', 'POST'])
def auth_handler():
    conf = current_app.config['db_config']
    provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
    if request.method == 'GET':  # если пользователь уже зареган - редирект на меню
        if 'user_id' in session:
            return redirect(url_for('main_menu_handler', hello_sign=f'Вы уже авторизованы, как {session.get("user_group")}' ))

        message = 'Войдите в аккаунт.'

        return render_template('login.html', message=message)

    elif request.method == 'POST':
        result, err = auth_route(request, provider, conf)

        if err == "Cursor not created":
            return redirect(url_for('auth_bp.auth_handler', message="Произошла ошибка при подключении к базе данных!"))
        if err == "Error executing SQL query":
            return redirect(url_for('auth_bp.auth_handler', message="Ошибка при выполнении запроса!"))

        if result:
            session['user_id'] = result[0][0]
            session['login'] = result[0][1]
            session['password'] = result[0][2]
            session['user_group'] = result[0][3]
            session.permanent = True
            return redirect(url_for('main_menu_handler'))
        else:
            return redirect(url_for('auth_bp.auth_handler', message="Неправильный логин или пароль!"))