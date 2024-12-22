from functools import wraps
from flask import session, request, redirect, url_for, current_app


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            user_role = session.get('user_group')  # группа пользователя
            user_request = request.endpoint  # Полное имя функции (например, 'auth_bp.auth_func')
            access = current_app.config['db_access']  # Конфигурация доступа из json

            # Проверяем, есть ли роль в access и разрешена ли указанная функция
            if user_role in access and user_request in access[user_role]:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('no_access_handler'))  # доступа нет
        else:
            return redirect(url_for('no_access_handler'))  # доступа нет

    return wrapper
