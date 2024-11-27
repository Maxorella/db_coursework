SELECT
    user_id,
    login,
    password,
    user_group
FROM user WHERE login="$login" AND password="$password";