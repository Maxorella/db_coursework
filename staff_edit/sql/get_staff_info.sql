SELECT
    user.user_id AS "user_id",
    user.login AS "Логин",
    user.password AS "Пароль",
    staff.surname AS "Фамилия",
    staff.address AS "Адрес",
    staff.birthday AS "День рождения",
    staff.position AS "Должность",
    staff.hire_date AS "Дата найма",
    staff.department_id AS "Номер отдела"
FROM
    user
LEFT JOIN
    staff
ON
    user.user_id = staff.staff_id
WHERE
    user.status = 'active' AND user.user_id = $staff_id
ORDER BY
    staff.department_id;