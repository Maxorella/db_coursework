from functools import wraps
from flask import session, request, redirect, url_for, current_app
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.auth_handler', message='Для продолжения войдите в аккаунт!'))
        return f(*args, **kwargs)
    return decorated_function


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            user_role = session.get('user_group')
            user_request = request.endpoint
            print('request_endpoint=', user_request)
            user_bp = user_request.split('.')[0]
            access = current_app.config['db_access']
            if user_role in access and user_bp in access[user_role]:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('no_access_handler'))
        else:
            return redirect(url_for('main_menu_handler'))
    return wrapper