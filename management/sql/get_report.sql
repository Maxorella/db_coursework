SELECT
    s.staff_id,
    s.surname,
    s.position,
    er.total_exceed_amount,
    er.report_month,
    er.report_year
FROM
    exceed_report er
JOIN
    staff s ON er.staff_id = s.staff_id
WHERE
    er.report_month = $month
    AND er.report_year = $year;
