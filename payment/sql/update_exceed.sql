UPDATE limit_exceed
SET repayment_date = STR_TO_DATE("$date", '%Y-%m-%d')
WHERE phone = $phone
  AND exceed_month = $month
  AND exceed_year = $year;