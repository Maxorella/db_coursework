SELECT
    s.surname AS "Фамилия сотрудника",
    s.department_id AS "Отдел",
    s.position AS "Должность",
    er.total_exceed_amount AS "Сумма превышения",
    er.report_month AS "Месяц превышения",
    er.report_year AS "Год превышения"
FROM
    exceed_report er
JOIN
    staff s ON er.staff_id = s.staff_id
WHERE
    er.report_month = $month
    AND er.report_year = $year;