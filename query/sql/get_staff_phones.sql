SELECT bcc.phone, bcc.money_limit
FROM bcc
JOIN staff ON bcc.staff_id = staff.staff_id
WHERE staff.surname = '$surname' AND staff.department_id = $department_id;
