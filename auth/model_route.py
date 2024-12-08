from auth.select import select_user


def auth_route(request, provider, conf):
    login = request.form.get('login', '')  # логин с формы
    password = request.form.get('password', '')  # пароль с формы

    sql = provider.get('select_user.sql', login=login, password=password)  # запрос (sql)

    result, _, error = select_user(conf, sql)  # модель
    return result, error
