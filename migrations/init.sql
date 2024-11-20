CREATE DATABASE sot_svyaz;
USE sot_svyaz;


DROP  TABLE IF EXISTS stuff;
DROP  TABLE IF EXISTS bcc;
DROP  TABLE IF EXISTS invoice;
DROP  TABLE IF EXISTS invoice_line;
DROP  TABLE IF EXISTS payment;
DROP  TABLE IF EXISTS payment_line;
DROP  TABLE IF EXISTS user;


CREATE TABLE IF NOT EXISTS user (
    user_id INT NOT NULL AUTO_INCREMENT,
    login VARCHAR(255) NOT NULL UNIQUE,
    user_group ENUM('сотрудник', 'руководство', 'админ', 'оператор', 'сотрудник банка') NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);


CREATE TABLE IF NOT EXISTS stuff (
    stuff_id INT NOT NULL AUTO_INCREMENT,
    surname VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    birthday DATE,
    position VARCHAR(100),
    hire_date DATE,
    department_id INT,
    PRIMARY KEY (stuff_id),
    FOREIGN KEY (stuff_id) REFERENCES user(user_id)
);


CREATE TABLE IF NOT EXISTS bcc (
    phone BIGINT NOT NULL,
    money_limit DECIMAL(15,2) NOT NULL,
    stuff_id INT,
    PRIMARY KEY (phone),
    FOREIGN KEY (stuff_id) REFERENCES stuff(stuff_id)
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

CREATE TABLE IF NOT EXISTS report_info (
    report_id INT NOT NULL,
    report_month INT NOT NULL,
    report_year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS exceed_report (
    report_id INT NOT NULL,
    stuff_id INT NOT NULL,
    total_exceed_amount DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (stuff_id, report_id),
    FOREIGN KEY (stuff_id) REFERENCES stuff(stuff_id),
    FOREIGN KEY (report_id) REFERENCES report_info(report_id)
);


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
    INSERT INTO exceed_report (report_id, stuff_id, total_exceed_amount)
    SELECT
        v_report_id,
        s.stuff_id,
        SUM(le.exceed_amount) AS total_exceed_amount
    FROM
        limit_exceed le
    JOIN bcc b ON le.phone = b.phone
    JOIN stuff s ON b.stuff_id = s.stuff_id
    WHERE le.exceed_month = p_month AND le.exceed_year = p_year
    GROUP BY s.stuff_id;
END $$

DELIMITER ;

/*
CREATE TABLE IF NOT EXISTS invoice (
    invoice_number INT NOT NULL AUTO_INCREMENT,
    issue_date DATE NOT NULL,
    invoice_month INT NOT NULL,
    invoice_year INT NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (invoice_number)
);

CREATE TABLE IF NOT EXISTS invoice_line (
    phone BIGINT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    invoice_number INT NOT NULL,
    PRIMARY KEY (phone, invoice_number),
    FOREIGN KEY (phone) REFERENCES bcc(phone),
    FOREIGN KEY (invoice_number) REFERENCES invoice(invoice_number)
);

 */


DELIMITER $$

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
END $$

DELIMITER ;
/*
CREATE TABLE IF NOT EXISTS payment (
    payment_number INT NOT NULL AUTO_INCREMENT,
    creation_date DATE NOT NULL,
    PRIMARY KEY (payment_number)
);

CREATE TABLE IF NOT EXISTS payment_line (
    phone INT NOT NULL,
    received_amount DECIMAL(15,2) NOT NULL,
    payment_number INT NOT NULL,
    payment_month INT NOT NULL,
    payment_year INT NOT NULL,
    PRIMARY KEY (phone, payment_number, payment_month, payment_year),
    FOREIGN KEY (payment_number) REFERENCES payment(payment_number)
);
*/


-- CREATE TABLE IF NOT EXISTS report (
-- );

INSERT INTO user (login, user_group, password) VALUES
    ('management1', 'руководство', 'password1'),
    ('management2', 'руководство', 'password2'),
    ('admin1', 'админ', 'password1'),
    ('admin2', 'админ', 'password2');
-- ('operator1', 'оператор', 'password1'),
-- ('operator2', 'оператор', 'password2'),
-- ('bank1', 'сотрудник банка', 'password1'),
-- ('bank2', 'сотрудник банка', 'password2');



-- Вставка пользователей для сотрудников из первого отдела (6 сотрудников)
INSERT INTO user (login, user_group, password)
VALUES
    ('login1', 'сотрудник', 'password1'), -- Иванов
    ('login2', 'сотрудник', 'password2'), -- Петров
    ('login3', 'сотрудник', 'password3'), -- Сидоров
    ('login4', 'сотрудник', 'password4'), -- Алексеев
    ('login5', 'сотрудник', 'password5'), -- Николаев
    ('login6', 'сотрудник', 'password6'); -- Захаров

-- Вставка пользователей для сотрудников из второго отдела (4 сотрудника)
INSERT INTO user (login, user_group, password)
VALUES
    ('login7', 'сотрудник', 'password7'), -- Кузнецов
    ('login8', 'сотрудник', 'password8'), -- Морозов
    ('login9', 'сотрудник', 'password9'), -- Дмитриев
    ('login10', 'сотрудник', 'password10'); -- Егорова


-- Вставка 6 сотрудников в первый отдел (department_id = 1)
INSERT INTO stuff (surname, address, birthday, position, hire_date, department_id)
VALUES
    ('Иванов', 'ул. Ленина, 1', '1985-06-15', 'Менеджер', '2023-01-10', 1),
    ('Петров', 'ул. Мира, 5', '1990-04-22', 'Инженер', '2022-11-14', 1),
    ('Сидоров', 'ул. Победы, 3', '1982-11-05', 'Директор', '2021-03-01', 1),
    ('Алексеев', 'ул. Московская, 10', '1987-07-30', 'Оперативник', '2022-06-20', 1),
    ('Николаев', 'ул. Куйбышева, 7', '1993-02-12', 'Бухгалтер', '2023-05-01', 1),
    ('Захаров', 'ул. Тверская, 13', '1989-08-14', 'Маркетолог', '2021-09-10', 1);

-- Вставка 4 сотрудников во второй отдел (department_id = 2)
INSERT INTO stuff (surname, address, birthday, position, hire_date, department_id)
VALUES
    ('Кузнецов', 'ул. Чапаева, 15', '1988-01-25', 'Аналитик', '2022-02-15', 2),
    ('Морозов', 'ул. Октябрьская, 2', '1995-10-30', 'Программист', '2023-08-05', 2),
    ('Дмитриев', 'ул. Строителей, 8', '1992-12-10', 'Менеджер', '2023-04-18', 2),
    ('Егорова', 'ул. Розы, 6', '1986-09-11', 'Юрист', '2021-12-15', 2);

-- Вставка телефонов для сотрудников из первого отдела
INSERT INTO bcc (phone, money_limit, stuff_id)
VALUES
    (89051544123, 500.00, 1),
    (89051544124, 600.00, 1),
    (89051544125, 400.00, 2),
    (89051544126, 300.00, 2),
    (89051544127, 700.00, 3),
    (89051544128, 850.00, 3),
    (89051544129, 900.00, 4),
    (89051544130, 500.00, 4),
    (89051544131, 650.00, 5),
    (89051544132, 750.00, 5),
    (89051544133, 950.00, 6),
    (89051544134, 550.00, 6);

-- Вставка телефонов для сотрудников из второго отдела
INSERT INTO bcc (phone, money_limit, stuff_id)
VALUES
    (89051544135, 200.00, 7),
    (89051544136, 300.00, 7),
    (89051544137, 400.00, 8),
    (89051544138, 500.00, 8),
    (89051544139, 600.00, 9),
    (89051544140, 700.00, 9),
    (89051544141, 800.00, 10),
    (89051544142, 900.00, 10);