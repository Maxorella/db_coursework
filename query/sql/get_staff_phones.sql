SELECT bcc.phone, bcc.money_limit
FROM bcc
JOIN staff ON bcc.staff_id = staff.staff_id
WHERE staff.staff_id = $staff_id;