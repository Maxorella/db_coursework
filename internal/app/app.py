import json
import os
from functools import wraps

from flask import Flask, render_template, request
from internal.database.sql_provider import SQLProvider
# from internal.dashboard.routes import dashboard_blueprint
from internal.database.select import select_catergory
from model_route import model_route
from internal.auth.routes import auth_blueprint
from flask import Blueprint, request, render_template, flash, redirect, session, url_for

from internal.utils.access import login_required

app = Flask(__name__)
app.secret_key = 'super secret key'

with open("./data/dbconfig.json") as f:
    app.config['db_config'] = json.load(f)
with open('./data/db_access.json') as f:
    app.config['db_access'] = json.load(f)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

app.register_blueprint(auth_blueprint, url_prefix='/auth')
# app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')


@app.route('/')
def main_menu_handler():
    if 'user_group' in session:
        user_role = session.get('user_group')
        hello_sign = f'Вы авторизованы как {user_role}'
    else:
        hello_sign = 'Вам необходимо авторизоваться'
    return render_template('main_menu.html', hello_sign=hello_sign)



@app.route('/exit')
def exit_handler():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)
