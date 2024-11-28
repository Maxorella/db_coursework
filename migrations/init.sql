CREATE DATABASE sot_svyaz;
USE sot_svyaz;
SET foreign_key_checks = 0;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS bcc;
DROP TABLE IF EXISTS limit_exceed;
DROP TABLE IF EXISTS talk_sum;
DROP TABLE IF EXISTS exceed_report;

CREATE TABLE IF NOT EXISTS user (
    user_id INT NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    user_group ENUM('сотрудник', 'руководство', 'админ') NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

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

CREATE TABLE IF NOT EXISTS bcc (
    phone BIGINT NOT NULL,
    money_limit DECIMAL(15,2) NOT NULL,
    staff_id INT,
    PRIMARY KEY (phone),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

CREATE TABLE IF NOT EXISTS limit_exceed (
    phone BIGINT NOT NULL,
    exceed_amount DECIMAL(15,2) NOT NULL,
    exceed_month INT NOT NULL,
    exceed_year INT NOT NULL,
    repayment_date DATE,
    PRIMARY KEY (phone, exceed_month, exceed_year),
    FOREIGN KEY (phone) REFERENCES bcc(phone)
);

CREATE TABLE IF NOT EXISTS talk_sum (
    phone BIGINT NOT NULL,
    talk_summ DECIMAL(15,2) NOT NULL,
    summ_month INT NOT NULL,
    summ_year INT NOT NULL,
    PRIMARY KEY (phone, summ_month, summ_year),
    FOREIGN KEY (phone) REFERENCES bcc(phone)
);

CREATE TABLE IF NOT EXISTS exceed_report (
    report_id INT NOT NULL,
    staff_id INT NOT NULL,
    total_exceed_amount DECIMAL(15,2) NOT NULL,
    report_month INT NOT NULL,
    report_year INT NOT NULL,
    PRIMARY KEY (staff_id, report_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

delimiter $$

CREATE PROCEDURE add_phone_summ(
    IN p_phone BIGINT,
    IN p_amount DECIMAL(15,2),
    IN p_year INT,
    IN p_month INT
)
BEGIN
    DECLARE v_money_limit DECIMAL(15,2);

    -- Получаем лимит по телефону из таблицы bcc
    SELECT money_limit INTO v_money_limit
    FROM bcc
    WHERE phone = p_phone;

    -- Если телефон найден и лимит установлен
    IF v_money_limit IS NOT NULL THEN
        -- Вставляем данные о разговоре в таблицу talk_sum
        INSERT INTO talk_sum (phone, talk_summ, summ_month, summ_year)
        VALUES (p_phone, p_amount, p_month, p_year);

        -- Если сумма разговора превышает лимит, добавляем запись в limit_exceed
        IF p_amount > v_money_limit THEN
            INSERT INTO limit_exceed (phone, exceed_amount, exceed_month, exceed_year)
            VALUES (p_phone, p_amount - v_money_limit, p_month, p_year);
        END IF;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Телефон не найден в таблице bcc';
    END IF;
END; $$

delimiter ;
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
    (89051544123, 1500.00, 1),  -- телефон администратора 1
    (89051544124, 2000.00, 2);  -- телефон администратора 2

-- Вставка телефонов для руководителей
INSERT INTO bcc (phone, money_limit, staff_id)
VALUES
    (89051544125, 1000.00, 3),  -- телефон руководителя 1
    (89051544126, 1200.00, 4);  -- телефон руководителя 2

-- Вставка телефонов для сотрудников
INSERT INTO bcc (phone, money_limit, staff_id)
VALUES
    (89051544127, 500.00, 5),  -- телефон сотрудника 1
    (89051544128, 600.00, 6),  -- телефон сотрудника 2
    (89051544129, 700.00, 7),  -- телефон сотрудника 3
    (89051544130, 800.00, 8),  -- телефон сотрудника 4
    (89051544131, 650.00, 9),  -- телефон сотрудника 5
    (89051544132, 750.00, 10), -- телефон сотрудника 6
    (89051544133, 950.00, 11), -- телефон сотрудника 7
    (89051544134, 850.00, 12), -- телефон сотрудника 8
    (89051544135, 1200.00, 13), -- телефон сотрудника 9
    (89051544136, 1100.00, 14); -- телефон сотрудника 10

-- Вставка превышений лимита для администраторов
INSERT INTO limit_exceed (phone, exceed_amount, exceed_month, exceed_year)
VALUES
    (89051544123, 200.00, 10, 2024),  -- превышение для администратора 1
    (89051544124, 400.00, 10, 2024);  -- превышение для администратора 2

-- Вставка превышений лимита для руководителей
INSERT INTO limit_exceed (phone, exceed_amount, exceed_month, exceed_year)
VALUES
    (89051544125, 100.00, 10, 2024),  -- превышение для руководителя 1
    (89051544126, 300.00, 10, 2024);  -- превышение для руководителя 2

-- Вставка превышений лимита для сотрудников
INSERT INTO limit_exceed (phone, exceed_amount, exceed_month, exceed_year)
VALUES
    (89051544127, 50.00, 10, 2024),   -- превышение для сотрудника 1
    (89051544128, 100.00, 10, 2024),  -- превышение для сотрудника 2
    (89051544129, 150.00, 10, 2024),  -- превышение для сотрудника 3
    (89051544130, 200.00, 10, 2024),  -- превышение для сотрудника 4
    (89051544131, 50.00, 10, 2024),   -- превышение для сотрудника 5
    (89051544132, 100.00, 10, 2024),  -- превышение для сотрудника 6
    (89051544133, 300.00, 10, 2024),  -- превышение для сотрудника 7
    (89051544134, 400.00, 10, 2024),  -- превышение для сотрудника 8
    (89051544135, 150.00, 10, 2024),  -- превышение для сотрудника 9
    (89051544136, 200.00, 10, 2024);  -- превышение для сотрудника 10

SET foreign_key_checks = 1;


/*
DELIMITER $$

CREATE PROCEDURE create_exceed_report_by_employee(
    IN p_month INT,
    IN p_year INT
)
BEGIN
    DECLARE v_report_id INT;

    -- Проверяем, существует ли запись в report_info
    SELECT report_id INTO v_report_id
    FROM report_info
    WHERE report_month = p_month AND report_year = p_year;

    -- Если запись не существует, добавляем новую
    IF v_report_id IS NULL THEN
        INSERT INTO report_info (report_month, report_year)
        VALUES (p_month, p_year);

        -- Получаем ID только что добавленной записи
        SELECT LAST_INSERT_ID() INTO v_report_id;
    END IF;

    -- Вставляем агрегированные данные по сотрудникам в таблицу exceed_report
    INSERT INTO exceed_report (report_id, staff_id, total_exceed_amount)
    SELECT
        v_report_id,
        s.staff_id,
        SUM(le.exceed_amount) AS total_exceed_amount
    FROM
        limit_exceed le
    JOIN bcc b ON le.phone = b.phone
    JOIN staff s ON b.staff_id = s.staff_id
    WHERE le.exceed_month = p_month AND le.exceed_year = p_year
    GROUP BY s.staff_id;
END $$

DELIMITER ;
*/
