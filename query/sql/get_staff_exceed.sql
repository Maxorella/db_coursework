SELECT
    le.phone AS phone_number,
    le.exceed_amount AS debt_amount,
    le.exceed_month AS debt_month,
    le.exceed_year AS debt_year,
    le.repayment_date AS repayment_date
FROM
    limit_exceed le
JOIN
    bcc b ON le.phone = b.phone
WHERE
    b.staff_id = $staff_id
  AND
    le.repayment_date IS NULL
ORDER BY
    le.exceed_year DESC,
    le.exceed_month DESC;