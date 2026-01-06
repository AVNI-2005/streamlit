ROLLBACK;
CREATE TABLE department1(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employe (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department_id INT REFERENCES departments(id),
    email VARCHAR(255),
    salary DECIMAL(10,2)
);

CREATE TABLE product1 (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2)
   
);

CREATE TABLE orders1 (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    employee_id INT REFERENCES employees(id),
    order_total DECIMAL(10,2),
    order_date DATE
);
INSERT INTO department1 (name)
VALUES ('HR'), ('Engineering'), ('Sales');

INSERT INTO employe(name, department_id, email, salary) VALUES
('Akansha', 1, 'akansha@company.com', 50000),
('Annu', 2, 'annu@company.com', 70000),
('Ravi', 3, 'ravi@company.com', 60000),
('Kiran', 4, 'kiran@company.com', 55000);


INSERT INTO product1 (name, price)
VALUES
('Laptop', 800),
('Wireless Mouse', 20),
('Keyboard', 30),
('Monitor', 200),



INSERT INTO orders1 (customer_name, employee_id, order_total, order_date)
VALUES
('Jiya ', 1, 820, '2015-01-01'),
('Davi', 2, 20, '2014-01-02'),
('Amit', 3, 230, '2016-02-10');


select * from employe;
select * from department1;
