import json
import os

from flask import Flask

from auth.routes import auth_blueprint
from query.routes import query_blueprint
from report.routes import report_blueprint

from flask import request, render_template, session

app = Flask(__name__)
app.secret_key = 'super secret key'

with open("./data/dbconfig.json") as f:
    app.config['db_config'] = json.load(f)
with open('./data/db_access.json') as f:
    app.config['db_access'] = json.load(f)
with open('./data/report.json') as f:
    app.config['report'] = json.load(f)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(query_blueprint, url_prefix='/query')
app.register_blueprint(report_blueprint, url_prefix='/report')

@app.route('/')
def main_menu_handler():
    hello_sign = 'Авторизуйтесь, чтобы продолжить!'
    if 'user_group' in session:
        user_role = session.get('user_group')
        hello_sign = f'Вы авторизованы как {user_role}'
    return render_template('main_menu.html', hello_sign=hello_sign)



@app.route('/exit')
def exit_handler():
    session.clear()
    return render_template('exit.html')

@app.route('/no_access')
def no_access_handler():
    return render_template('no_access.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)
