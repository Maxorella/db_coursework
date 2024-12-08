CREATE DATABASE sot_svyaz;
USE sot_svyaz;
SET foreign_key_checks = 0;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS bcc;
DROP TABLE IF EXISTS limit_exceed;
DROP TABLE IF EXISTS exceed_report;

-- пользователи
CREATE TABLE IF NOT EXISTS user (
    user_id INT NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    user_group ENUM('сотрудник', 'руководство', 'админ') NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

-- сведенья о сотрудниках
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT NOT NULL,
    surname VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    birthday DATE,
    position VARCHAR(100),
    hire_date DATE,
    department_id INT,
    PRIMARY KEY (staff_id),
    FOREIGN KEY (staff_id) REFERENCES user(user_id)
);

-- служебная сотовая связь
CREATE TABLE IF NOT EXISTS bcc (
    phone VARCHAR(32) NOT NULL,
    money_limit DECIMAL(15,2) NOT NULL,
    staff_id INT,
    PRIMARY KEY (phone),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

-- счет
CREATE TABLE IF NOT EXISTS invoice (
    invoice_id INT,
    creation_date DATETIME,
    invoice_month INT,
    invoice_year INT,
    total_sum INT,
    PRIMARY KEY (invoice_id)
);

-- строка счета
CREATE TABLE IF NOT EXISTS invoice_line (
    invoice_id INT,
    phone VARCHAR(32),
    sum_to_pay DECIMAL(15, 2),
    PRIMARY KEY (invoice_id, phone),
    FOREIGN KEY (invoice_id) REFERENCES invoice(invoice_id)

);

-- превышение лимита
CREATE TABLE IF NOT EXISTS limit_exceed (
    phone VARCHAR(32) NOT NULL,
    exceed_amount DECIMAL(15,2) NOT NULL,
    exceed_month INT NOT NULL,
    exceed_year INT NOT NULL,
    repayment_date DATE,
    PRIMARY KEY (phone, exceed_month, exceed_year),
    FOREIGN KEY (phone) REFERENCES bcc(phone)
);

-- платежка
CREATE TABLE IF NOT EXISTS payment (
  payment_number INT,
  creation_date DATETIME NOT NULL,
  PRIMARY KEY (payment_number)
);


-- строка платежки
CREATE TABLE IF NOT EXISTS payment_line (
  payment_number INT,
  phone VARCHAR(32) NOT NULL,
  got_sum INT NOT NULL,
  payment_month INT,
  payment_year INT,
  PRIMARY KEY (payment_number, phone),
  FOREIGN KEY (phone) REFERENCES bcc(phone),
  FOREIGN KEY (payment_number) REFERENCES payment(payment_number)
);

-- отчет по неоплаченным превышениям
CREATE TABLE IF NOT EXISTS exceed_report (
    staff_id INT NOT NULL,
    total_exceed_amount DECIMAL(15,2) NOT NULL,
    report_month INT NOT NULL,
    report_year INT NOT NULL,
    PRIMARY KEY (staff_id, report_month, report_year),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);


-- Вставка пользователей для администраторов
INSERT INTO user (user_id, login, user_group, password)
VALUES
    (1, 'admin1', 'админ', 'password1'),
    (2, 'admin2', 'админ', 'password2');

-- Вставка пользователей для руководителей
INSERT INTO user (user_id, login, user_group, password)
VALUES
    (3, 'management1', 'руководство', 'password1'),
    (4, 'management2', 'руководство', 'password2');

-- Вставка пользователей для сотрудников
INSERT INTO user (user_id, login, user_group, password)
VALUES
    (5, 'employee1', 'сотрудник', 'password1'),
    (6, 'employee2', 'сотрудник', 'password2'),
    (7, 'employee3', 'сотрудник', 'password3'),
    (8, 'employee4', 'сотрудник', 'password4'),
    (9, 'employee5', 'сотрудник', 'password5'),
    (10, 'employee6', 'сотрудник', 'password6'),
    (11, 'employee7', 'сотрудник', 'password7'),
    (12, 'employee8', 'сотрудник', 'password8'),
    (13, 'employee9', 'сотрудник', 'password9'),
    (14, 'employee10', 'сотрудник', 'password10');

-- Вставка сотрудников в таблицу staff для администраторов
INSERT INTO staff (staff_id, surname, address, birthday, position, hire_date, department_id)
VALUES
    (1, 'Admin1', 'ул. Центральная, 1', '1980-05-10', 'Системный администратор', '2021-01-01', 1),
    (2, 'Admin2', 'ул. Ленина, 2', '1975-03-22', 'Главный администратор', '2020-06-15', 2);

-- Вставка сотрудников в таблицу staff для руководителей
INSERT INTO staff (staff_id, surname, address, birthday, position, hire_date, department_id)
VALUES
    (3, 'Management1', 'ул. Советская, 3', '1984-11-15', 'Руководитель отдела 1', '2022-07-10', 1),
    (4, 'Management2', 'ул. Октябрьская, 4', '1990-02-20', 'Руководитель отдела 2', '2023-03-01', 2);

-- Вставка сотрудников в таблицу staff для сотрудников
INSERT INTO staff (staff_id, surname, address, birthday, position, hire_date, department_id)
VALUES
    (5, 'Employee1', 'ул. Ленина, 5', '1992-06-17', 'Менеджер', '2023-01-10', 1),
    (6, 'Employee2', 'ул. Мира, 6', '1990-04-22', 'Инженер', '2022-11-14', 1),
    (7, 'Employee3', 'ул. Победы, 7', '1985-11-05', 'Директор', '2021-03-01', 1),
    (8, 'Employee4', 'ул. Московская, 8', '1987-07-30', 'Оперативник', '2022-06-20', 2),
    (9, 'Employee5', 'ул. Куйбышева, 9', '1993-02-12', 'Бухгалтер', '2023-05-01', 2),
    (10, 'Employee6', 'ул. Тверская, 10', '1989-08-14', 'Маркетолог', '2021-09-10', 2),
    (11, 'Employee7', 'ул. Чапаева, 11', '1988-01-25', 'Аналитик', '2022-02-15', 3),
    (12, 'Employee8', 'ул. Октябрьская, 12', '1995-10-30', 'Программист', '2023-08-05', 3),
    (13, 'Employee9', 'ул. Строителей, 13', '1992-12-10', 'Менеджер', '2023-04-18', 3),
    (14, 'Employee10', 'ул. Розы, 14', '1986-09-11', 'Юрист', '2021-12-15', 3);

-- Вставка телефонов для администраторов
INSERT INTO bcc (phone, money_limit, staff_id)
VALUES
    ('89051544123', 1500.00, 1),  -- телефон администратора 1
    ('89051544124', 2000.00, 1);  -- телефон администратора 2

-- Вставка телефонов для руководителей
INSERT INTO bcc (phone, money_limit, staff_id)
VALUES
    ('89051544125', 1000.00, 3),  -- телефон руководителя 1
    ('89051544126', 1200.00, 4);  -- телефон руководителя 2

-- Вставка телефонов для сотрудников
INSERT INTO bcc (phone, money_limit, staff_id)
VALUES
    ('89051544127', 500.00, 5),  -- телефон сотрудника 1
    ('89051544128', 600.00, 6),  -- телефон сотрудника 2
    ('89051544129', 700.00, 7),  -- телефон сотрудника 3
    ('89051544130', 800.00, 8),  -- телефон сотрудника 4
    ('89051544131', 650.00, 9),  -- телефон сотрудника 5
    ('89051544132', 750.00, 10), -- телефон сотрудника 6
    ('89051544133', 950.00, 11), -- телефон сотрудника 7
    ('89051544134', 850.00, 12), -- телефон сотрудника 8
    ('89051544135', 1200.00, 13), -- телефон сотрудника 9
    ('89051544136', 1100.00, 14); -- телефон сотрудника 10

-- Вставка превышений лимита для администраторов
INSERT INTO limit_exceed (phone, exceed_amount, exceed_month, exceed_year)
VALUES
    ('89051544123', 200.00, 10, 2024),  -- превышение для администратора 1
    ('89051544124', 400.00, 10, 2024);  -- превышение для администратора 2

-- Вставка превышений лимита для руководителей
INSERT INTO limit_exceed (phone, exceed_amount, exceed_month, exceed_year)
VALUES
    ('89051544125', 100.00, 10, 2024),  -- превышение для руководителя 1
    ('89051544126', 300.00, 10, 2024);  -- превышение для руководителя 2

-- Вставка превышений лимита для сотрудников
INSERT INTO limit_exceed (phone, exceed_amount, exceed_month, exceed_year)
VALUES
    ('89051544127', 50.00, 10, 2024),   -- превышение для сотрудника 1
    ('89051544128', 100.00, 10, 2024),  -- превышение для сотрудника 2
    ('89051544129', 150.00, 10, 2024),  -- превышение для сотрудника 3
    ('89051544130', 200.00, 10, 2024),  -- превышение для сотрудника 4
    ('89051544131', 50.00, 10, 2024),   -- превышение для сотрудника 5
    ('89051544132', 100.00, 10, 2024),  -- превышение для сотрудника 6
    ('89051544133', 300.00, 10, 2024),  -- превышение для сотрудника 7
    ('89051544134', 400.00, 10, 2024),  -- превышение для сотрудника 8
    ('89051544135', 150.00, 10, 2024),  -- превышение для сотрудника 9
    ('89051544136', 200.00, 10, 2024);  -- превышение для сотрудника 10

SET foreign_key_checks = 1;


DELIMITER $$

CREATE PROCEDURE create_or_update_exceed_report(
    IN p_month INT,
    IN p_year INT
)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_staff_id INT;
    DECLARE v_total_exceed_amount DECIMAL(15, 2);
    DECLARE report_cursor CURSOR FOR
        SELECT s.staff_id, SUM(le.exceed_amount) AS total_exceed_amount
        FROM limit_exceed le
        JOIN bcc b ON le.phone = b.phone
        JOIN staff s ON b.staff_id = s.staff_id
        WHERE le.exceed_month = p_month AND le.exceed_year = p_year
        GROUP BY s.staff_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Открываем курсор для обработки данных
    OPEN report_cursor;

    read_loop: LOOP
        FETCH report_cursor INTO v_staff_id, v_total_exceed_amount;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Обновляем запись, если она существует
        IF EXISTS (
            SELECT 1 FROM exceed_report
            WHERE staff_id = v_staff_id
              AND report_month = p_month
              AND report_year = p_year
        ) THEN
            UPDATE exceed_report
            SET total_exceed_amount = v_total_exceed_amount
            WHERE staff_id = v_staff_id
              AND report_month = p_month
              AND report_year = p_year;
        ELSE
            -- Вставляем новую запись, если она не существует
            INSERT INTO exceed_report (staff_id, total_exceed_amount, report_month, report_year)
            VALUES (v_staff_id, v_total_exceed_amount, p_month, p_year);
        END IF;
    END LOOP;

    -- Закрываем курсор
    CLOSE report_cursor;
END$$

DELIMITER ;
