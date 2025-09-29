CREATE DATABASE CompanyDB;
USE CompanyDB;

create table Departments(
	dept_id INT auto_increment primary key,
    dept_name VARCHAR(50) not null
    );

create table Employees(
	emp_id int auto_increment primary key,
    name VARCHAR(50),
    age int ,
    salary decimal(10,2),
    dept_id int,
    foreign key (dept_id) references Departments(dept_id)
    );
    
insert into Departments (dept_name) values
('IT'),
('HR'),
('Finance'),
('Sales');

INSERT INTO Employees (name, age, salary, dept_id) VALUES
('Rahul', 28, 55000, 1),   -- IT
('Priya', 32, 60000, 2),   -- HR
('Arjun', 25, 48000, 3),   -- Finance
('Neha', 30, 70000, 1),    -- IT
('Vikram', 35, 65000, 4);  -- Sales


truncate table Employees;
ALTER TABLE Employees DROP FOREIGN KEY employees_ibfk_1;
truncate table Departments;

INSERT INTO Employees (name, age, salary, dept_id) VALUES
('Rahul', 28, 55000, 1),   -- IT
('Priya', 32, 60000, 2),   -- HR
('Arjun', 25, 48000, NULL),-- 
('Neha', 30, 70000, 1),    -- IT
('Vikram', 35, 65000, 4);  -- Sales

select * from Employees;
select * from Departments;
 
select e.name, e.salary, d.dept_name
from Employees e
INNER JOIN Departments d
on e.dept_id = d.dept_id;

select e.name, e.salary, d.dept_name
from Employees e
LEFT JOIN Departments d
on e.dept_id = d.dept_id;

select e.name, e.salary, d.dept_name
from Employees e
RIGHT JOIN Departments d
on e.dept_id = d.dept_id;

select e.name, e.salary, d.dept_name
from Employees e
LEFT JOIN Departments d
on e.dept_id = d.dept_id
UNION
select e.name, e.salary, d.dept_name
from Employees e
RIGHT JOIN Departments d
on e.dept_id = d.dept_id;