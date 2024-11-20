from flask import request, session
'''
def auth_user(request, provider):
    login = request.form.get('login', '')
    password = request.form.get('password', '')
    sql = provider.get(
        'add_session.sql',
        {
            'login': login,
            'password': password
        }
    )
    user = find_user(sql, {})
    session['user_id'] = user['user_id']
    session['password'] = user['password']
    session.permanent = True
    return {
        'status': 'OK',
        'message': 'Successful'
    }


def find_user(provider):

    sql = provider.get(
        'add_session.sql',
        {
            'login': login,
            'password': password
        }
    )

    return{
        'user_id': 1,
        'user_group': 'typical',
        'password': ,
    }
'''