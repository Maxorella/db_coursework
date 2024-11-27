SELECT
    s.staff_id,
    u.user_group,
    s.surname,
    s.position,
    s.hire_date,
    s.department_id
FROM
    staff s
JOIN
    user u ON s.staff_id = u.user_id
WHERE
    s.staff_id = $staff_id;
