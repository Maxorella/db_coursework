SELECT
    le.phone,
    le.exceed_amount,
    le.exceed_month,
    le.exceed_year,
    le.repayment_date
FROM
    limit_exceed le
WHERE
    le.phone = '$phone'
  AND
    le.repayment_date IS NULL
ORDER BY
    le.exceed_year DESC,
    le.exceed_month DESC;