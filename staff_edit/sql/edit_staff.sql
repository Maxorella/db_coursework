UPDATE staff
SET surname = '$surname', address = '$address', birthday = '$birthday',
position = '$position', hire_date = '$hire_date', department_id = $department_id
WHERE staff_id = $staff_id;