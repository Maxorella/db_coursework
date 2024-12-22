from database.select import select_list, select_dict


def auth_route(provider, conf, login, password):

    sql = provider.get('select_user.sql', login=login, password=password)
    result, error = select_dict(conf, sql)

    if error == "Cursor not created":
        return dict(), "Произошла ошибка при подключении к базе данных!"

    if error.startswith("Error executing SQL query:"):
        return dict(), "Возникла ошибка при выполнении запроса!"

    if len(result) == 0 and error == '':
        return result, "Неправильный логин или пароль!"

    if error != '':
        return dict(), error

    return result, error
