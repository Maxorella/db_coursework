SELECT bcc.phone AS "Номер телефона", bcc.money_limit AS "Лимит в месяц"
FROM bcc
JOIN staff ON bcc.staff_id = staff.staff_id
WHERE staff.staff_id = $staff_id and bcc.status = 'active';