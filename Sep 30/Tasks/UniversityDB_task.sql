CREATE DATABASE UniversityDB;
USE UniversityDB;
-- Students Table
CREATE TABLE Students (
student_id INT PRIMARY KEY,
name VARCHAR(50),
city VARCHAR(50)
);
-- Courses Table
CREATE TABLE Courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(50),
credits INT
);
-- Enrollments Table
CREATE TABLE Enrollments (
enroll_id INT PRIMARY KEY,
student_id INT,
course_id INT,
grade CHAR(2),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
-- Insert Students
INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');
-- Insert Courses
INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);
-- Insert Enrollments
INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),
(5, 4, 102, 'B'),
(6, 5, 104, 'A');

Level 1: Single Table
1. Create a stored procedure to list all students.
2. Create a stored procedure to list all courses.
3. Create a stored procedure to find all students from a given city (take city as input).

DELIMITER $$
create procedure list_of_students()
BEGIN
	select name from Students;
END $$
DELIMITER ;

call list_of_students();

DELIMITER $$
create procedure list_of_courses()
BEGIN
	select course_name from Courses;
END $$
DELIMITER ;

call list_of_courses();

DELIMITER $$
create procedure students_from_a_city(IN student_city varchar(15))
BEGIN
	select name from Students
    where city = student_city;
END $$
DELIMITER ;

call students_from_a_city('Mumbai');


Level 2: Two-Table Joins
4. Create a stored procedure to list students with their enrolled courses.
5. Create a stored procedure to list all students enrolled in a given course (take
course_id as input).
6. Create a stored procedure to count the number of students in each course.

DELIMITER $$
create procedure students_and_courses()
BEGIN
select s.name as student_name ,c.course_name
    from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on c.course_id = e.course_id  ;
END $$
DELIMITER ;

call students_and_courses();

DELIMITER $$
create procedure students_in_a_course(IN course_id int)
BEGIN
select s.name as student_name
from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on c.course_id = e.course_id  
    where c.course_id = course_id;
END $$
DELIMITER ;

call students_in_a_course(101);
   
DELIMITER $$
create procedure count_of_stu_per_course()
BEGIN
select c.course_name,count(s.student_id) as count_of_students
from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on c.course_id = e.course_id  
    group by c.course_name;
END $$
DELIMITER ;

call count_of_stu_per_course();

 Level 3: Three-Table Joins
7. Create a stored procedure to list students with course names and grades.
8. Create a stored procedure to show all courses taken by a given student (take
student_id as input).
9. Create a stored procedure to show average grade per course


DELIMITER $$
create procedure stu_with_course_grades()
BEGIN
select s.name as student_name, c.course_name,e.grade
from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on c.course_id = e.course_id  ;
END $$
DELIMITER ;

call stu_with_course_grades();

DELIMITER $$
create procedure all_courses_by_a_student(IN student_id int )
BEGIN
select s.name, group_concat(c.course_name SEPARATOR ',') as courses
from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on c.course_id = e.course_id  
    group by s.student_id;
END $$
DELIMITER ; 

call all_courses_by_a_student(1);

DELIMITER $$
create procedure avg_grade_per_course( )
BEGIN
select c.course_name,count(e.grade) as count
from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on c.course_id = e.course_id  
    group by c.course_name;
END $$
DELIMITER ; 

