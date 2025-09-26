CREATE DATABASE SchoolDB;
USE SchoolDB;

create table Students (
	id INT auto_increment primary key,
    name varchar(50),
    age INT, 
    course VARCHAR(50),
    marks int
);

insert into Students(name,age,course,marks)
values('Rahul',24,'Data Science',90);


insert into Students(name,age,course,marks)
values
('Ayush',22,'DSA',85),
('Yash',22,'AI',91);

select * from Students;

select name,marks from Students;

select * from Students WHERE marks > 85;

UPDATE Students
SET marks = 95,course = 'Advanced AI'
where id = 3;

-- UPDATE Students SET course = 'AI'; this will update the course for all records;

DELETE from Students where id =3;