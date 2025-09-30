create database HospitalDB;
use HospitalDB;

create table Patients (
patient_id INT PRIMARY KEY,
name VARCHAR(50),
age INT,
gender CHAR(1),
city VARCHAR(50)
);

create table Doctors(
doctor_id INT PRIMARY KEY,
name VARCHAR(50),
specialization VARCHAR(50),
experience INT
);

create table Appointments (
appointment_id INT PRIMARY KEY,
patient_id INT ,
doctor_id INT ,
appointment_date DATE,
status VARCHAR(20),
FOREIGN KEY (patient_id) references Patients(patient_id),
FOREIGN KEY (doctor_id) references Doctors(doctor_id)
);

create table MedicalRecords (
record_id INT PRIMARY KEY,
patient_id INT ,
doctor_id INT ,
diagnosis VARCHAR(100),
treatment VARCHAR(100),
date DATE,
FOREIGN KEY (patient_id) references Patients(patient_id),
FOREIGN KEY (doctor_id)references Doctors(doctor_id)
);

create table Billing(
bill_id INT PRIMARY KEY,
patient_id INT ,
amount DECIMAL(10,2),
bill_date DATE,
status VARCHAR(20),
FOREIGN KEY (patient_id) references Patients(patient_id)
);


INSERT INTO Patients VALUES
(1, 'Raj', 35, 'M', 'Mumbai'),
(2, 'Sneha', 29, 'F', 'Pune'),
(3, 'Karan', 40, 'M', 'Delhi'),
(4, 'Meera', 33, 'F', 'Mumbai'),
(5, 'Aditya', 27, 'M', 'Chennai'),
(6, 'Riya', 24, 'F', 'Pune'),
(7, 'Manav', 50, 'M', 'Delhi'),
(8, 'Isha', 38, 'F', 'Bengaluru'),
(9, 'Tanya', 31, 'F', 'Bengaluru'),
(10, 'Rohit', 45, 'M', 'Chennai');

INSERT INTO Doctors VALUES
(1, 'Dr. Aarti Mehra', 'Cardiology', 15),
(2, 'Dr. Rajeev Nair', 'Orthopedics', 12),
(3, 'Dr. Sneha Kapoor', 'Pediatrics', 9),
(4, 'Dr. Arjun Sinha', 'Neurology', 18),
(5, 'Dr. Priya Das', 'Dermatology', 7);


INSERT INTO Appointments VALUES
(1, 1, 1, '2025-10-01', 'Scheduled'),
(2, 2, 3, '2025-10-02', 'Completed'),
(3, 3, 2, '2025-10-05', 'Cancelled'),
(4, 4, 1, '2025-10-07', 'Scheduled'),
(5, 5, 5, '2025-10-10', 'Completed'),
(6, 6, 4, '2025-10-12', 'Scheduled'),
(7, 7, 2, '2025-10-15', 'Completed'),
(8, 8, 3, '2025-10-18', 'Scheduled'),
(9, 9, 5, '2025-10-20', 'Cancelled'),
(10, 10, 4, '2025-10-22', 'Completed');


INSERT INTO MedicalRecords VALUES
(1, 1, 1, 'Hypertension', 'Medication and lifestyle changes', '2025-09-15'),
(2, 2, 3, 'Asthma', 'Inhaler therapy', '2025-09-20'),
(3, 3, 2, 'Fractured arm', 'Cast application', '2025-09-25'),
(4, 4, 1, 'High cholesterol', 'Statins prescription', '2025-09-27'),
(5, 5, 5, 'Skin rash', 'Topical corticosteroids', '2025-09-30'),
(6, 6, 4, 'Migraine', 'Pain management', '2025-10-02'),
(7, 7, 2, 'Knee pain', 'Physiotherapy', '2025-10-04'),
(8, 8, 3, 'Allergic reaction', 'Antihistamines', '2025-10-06'),
(9, 9, 5, 'Eczema', 'Moisturizers and steroids', '2025-10-08'),
(10, 10, 4, 'Seizures', 'Antiepileptic drugs', '2025-10-10');

INSERT INTO Billing  VALUES
(1, 1, 1500.00, '2025-10-05', 'Paid'),
(2, 2, 2000.50, '2025-10-06', 'Unpaid'),
(3, 3, 3500.00, '2025-10-07', 'Paid'),
(4, 4, 1200.75, '2025-10-08', 'Unpaid'),
(5, 5, 1800.00, '2025-10-09', 'Paid'),
(6, 6, 2200.00, '2025-10-10', 'Unpaid'),
(7, 7, 3000.00, '2025-10-11', 'Paid'),
(8, 8, 1750.25, '2025-10-12', 'Paid'),
(9, 9, 2100.00, '2025-10-13', 'Unpaid'),
(10, 10, 4000.00, '2025-10-14', 'Paid');



TASK 1 List all patients assigned to a cardiologist.


SELECT p.patient_id, p.name, p.age, p.gender, p.city
FROM Patients p
JOIN Appointments a ON p.patient_id = a.patient_id
JOIN Doctors d ON a.doctor_id = d.doctor_id
WHERE d.specialization = 'Cardiology';

TASK 2 Find all appointments for a given doctor.

select d.doctor_id, d.name, group_concat(a.appointment_id SEPARATOR ',') as appointment_ids,
group_concat(p.patient_id SEPARATOR ',') as patient_ids,
group_concat( a.appointment_date SEPARATOR ',') as appointment_dates,
group_concat( a.status SEPARATOR ',') as status
from Appointments a
join Doctors d on a.doctor_id = d.doctor_id
join Patients p on a.patient_id = p.patient_id
group by d.doctor_id;


TASK 3 Show unpaid bills of patients.


SELECT b.bill_id , b.patient_id ,b.amount ,b.bill_date,b.status 
FROM Patients p
JOIN billing b ON b.patient_id = p.patient_id
WHERE b.status = 'Unpaid';


TASK 4 Procedure: GetPatientHistory(patient_id) → returns all visits, diagnoses, 
and treatments for a patient.

DELIMITER $$ 
create procedure GetPatientHistory(in p_id int)
BEGIN
select date, diagnosis, treatment
from MedicalRecords 
where patient_id = p_id;
END $$
DELIMITER ;

call GetPatientHistory(2);


TASK 5 Procedure: GetDoctorAppointments(doctor_id) → returns all appointments for a doctor.
DELIMITER $$ 
create procedure GetDoctorAppointments(in d_id int)
BEGIN
select doctor_id , appointment_id, patient_id , appointment_date ,status
from Appointments 
where doctor_id = d_id;
END $$
DELIMITER ;

call GetDoctorAppointments(1);
