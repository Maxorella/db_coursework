from flask import Blueprint, request, render_template, redirect, session, url_for, current_app
import os
from auth.model_route import auth_route
from database.sql_provider import SQLProvider

auth_blueprint = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_blueprint.route('/', methods=['GET', 'POST'])
def auth_handler():
    conf = current_app.config['db_config']

    if request.method == 'GET':  # если пользователь уже авторизован - редирект на главное меню
        if 'user_group' in session:
            return redirect(
                url_for('main_menu_handler', message=f'Вы уже авторизованы, как {session.get("user_group")}')
            )

        message = request.args.get('message')

        return render_template('login.html', message=message)

    elif request.method == 'POST':

        result, err = auth_route(provider, conf, request.form.get('login', ''), request.form.get('password', ''))

        if result and err == '':
            session['user_id'] = result[0]['user_id']
            session['login'] = result[0]['login']
            session['password'] = result[0]['password']
            session['user_group'] = result[0]['user_group']
            session.permanent = True
            return redirect(url_for('main_menu_handler'))
        else:
            return redirect(url_for('auth_bp.auth_handler', message=err))
