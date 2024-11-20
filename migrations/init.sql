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
    phone INT NOT NULL,
    money_limit DECIMAL(15,2) NOT NULL,
    stuff_id INT,
    PRIMARY KEY (phone),
    FOREIGN KEY (stuff_id) REFERENCES stuff(stuff_id)
);

CREATE TABLE IF NOT EXISTS limit_exceed (
    phone INT NOT NULL,
    exceed_amount DECIMAL(15,2) NOT NULL,
    exceed_month INT NOT NULL,
    exceed_year INT NOT NULL,
    repayment_date DATE,
    PRIMARY KEY (phone, exceed_month, exceed_year)
);

CREATE TABLE IF NOT EXISTS invoice (
    invoice_number INT NOT NULL AUTO_INCREMENT,
    issue_date DATE NOT NULL,
    invoice_month INT NOT NULL,
    invoice_year INT NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (invoice_number)
);

CREATE TABLE IF NOT EXISTS invoice_line (
    phone INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    invoice_number INT NOT NULL,
    PRIMARY KEY (phone, invoice_number),
    FOREIGN KEY (phone) REFERENCES bcc(phone),
    FOREIGN KEY (invoice_number) REFERENCES invoice(invoice_number)
);


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



-- CREATE TABLE IF NOT EXISTS report (
-- );

INSERT INTO user (login, user_group, password) VALUES
    ('пользователь1', 'сотрудник', 'password1'),
    ('employee2', 'сотрудник', 'password2'),
    ('management1', 'руководство', 'password1'),
    ('management2', 'руководство', 'password2'),
    ('admin1', 'админ', 'password1'),
    ('admin2', 'админ', 'password2'),
    ('operator1', 'оператор', 'password1'),
    ('operator2', 'оператор', 'password2'),
    ('bank1', 'сотрудник банка', 'password1'),
    ('bank2', 'сотрудник банка', 'password2');