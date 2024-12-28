SELECT
    s.surname AS "Фамилия сотрудника",
    s.position AS "Должность",
    s.department_id AS "Отдел",
    per.total_paid_amount AS "Оплаченная сумма",
    per.report_month AS "Месяц превышения",
    per.report_year AS "Год превышения"
FROM
    paid_exceed_report per
JOIN
    staff s ON per.staff_id = s.staff_id
WHERE
    per.report_month = $month
    AND per.report_year = $year;