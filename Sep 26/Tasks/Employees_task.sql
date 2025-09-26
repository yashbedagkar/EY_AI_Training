CREATE TABLE Employees(
	id int auto_increment primary key,
    name VARCHAR(50) NOT NULL,
    age int,
    department VARCHAR(50),
    salary decimal (10,2)
    );
    
insert into Employees(name,age,department,salary)
values('Ayush',24,'Tax',600000);

insert into Employees(name,age,department,salary)
values
('Yash',22,'AI',350000),
('Om',23,'HR',400000),
('Rahul',24,'Consulting',800000);

select * from Employees;

select name,salary from Employees;

select * from Employees WHERE salary > 500000;

UPDATE Employees
SET department = 'Data',salary = '450000'
where id = 2;

DELETE from Students where id =4;