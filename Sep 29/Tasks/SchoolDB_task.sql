CREATE database School;
USE School;
    
create table Subjects (
	subject_id int auto_increment primary key,
    subject_name VARCHAR(50)
    );
    
create table Teachers (
	teacher_id int auto_increment primary key,
	name VARCHAR(50),
    subject_id int,
    foreign key (subject_id) references Subjects(subject_id)
    );
    
INSERT INTO Subjects (subject_name) VALUES
('Mathematics'),   -- id = 1
('Science'),       -- id = 2
('English'),       -- id = 3
('History'),       -- id = 4
('Geography');     -- id = 5 (no teacher yet)

INSERT INTO Teachers (name, subject_id) VALUES
('Rahul Sir', 1),   -- Mathematics
('Priya Madam', 2), -- Science
('Arjun Sir', NULL),-- No subject assigned
('Neha Madam', 3);  -- English

select * from Subjects;
select * from Teachers;

-- INNER JOIN
select s.subject_id,s.subject_name,t.teacher_id, t.name
from Subjects s 
INNER JOIN Teachers t
on s.subject_id = t.subject_id;

-- LEFT JOIN
select s.subject_id,s.subject_name,t.teacher_id, t.name
from Subjects s 
LEFT JOIN Teachers t
on s.subject_id = t.subject_id;

-- RIGHT JOIN
select s.subject_id,s.subject_name,t.teacher_id, t.name
from Subjects s 
RIGHT JOIN Teachers t
on s.subject_id = t.subject_id;

-- FULL JOIN
select s.subject_id,s.subject_name,t.teacher_id, t.name
from Subjects s 
LEFT JOIN Teachers t
on s.subject_id = t.subject_id
UNION
select s.subject_id,s.subject_name,t.teacher_id, t.name
from Subjects s 
RIGHT JOIN Teachers t
on s.subject_id = t.subject_id;