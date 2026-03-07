-- MariaDB Dummy Data: HR System
USE hr_db;

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(150) UNIQUE,
    hire_date DATE,
    salary DECIMAL(10, 2),
    FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE leave_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    start_date DATE,
    end_date DATE,
    reason VARCHAR(255),
    status ENUM(
        'PENDING',
        'APPROVED',
        'REJECTED'
    ) DEFAULT 'PENDING',
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);

-- Departments
INSERT INTO
    departments (name)
VALUES ('Engineering'),
    ('Marketing'),
    ('Finance'),
    ('HR'),
    ('Operations');

-- Employees
INSERT INTO
    employees (
        department_id,
        first_name,
        last_name,
        email,
        hire_date,
        salary
    )
VALUES (
        1,
        'Omar',
        'Hassan',
        'omar.h@company.com',
        '2021-03-15',
        85000.00
    ),
    (
        1,
        'Sara',
        'Ahmed',
        'sara.a@company.com',
        '2020-07-01',
        92000.00
    ),
    (
        2,
        'Khaled',
        'Mansour',
        'khaled.m@company.com',
        '2022-01-10',
        67000.00
    ),
    (
        3,
        'Nour',
        'Ibrahim',
        'nour.i@company.com',
        '2019-11-20',
        75000.00
    ),
    (
        4,
        'Aya',
        'Mohamed',
        'aya.mo@company.com',
        '2023-06-05',
        60000.00
    ),
    (
        5,
        'Youssef',
        'Gamal',
        'youssef.g@company.com',
        '2018-09-30',
        55000.00
    );

-- Leave Requests
INSERT INTO
    leave_requests (
        employee_id,
        start_date,
        end_date,
        reason,
        status
    )
VALUES (
        1,
        '2026-04-01',
        '2026-04-05',
        'Annual leave',
        'APPROVED'
    ),
    (
        2,
        '2026-03-20',
        '2026-03-21',
        'Medical',
        'PENDING'
    ),
    (
        3,
        '2026-05-10',
        '2026-05-15',
        'Family occasion',
        'APPROVED'
    ),
    (
        4,
        '2026-03-25',
        '2026-03-26',
        'Personal',
        'REJECTED'
    );

SELECT 'MariaDB: hr_db loaded ✅' AS status;