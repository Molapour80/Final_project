CREATE TABLE students (
        student_id INT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        class_id INT,
        registration_date DATE
    );

CREATE TABLE teachers (
        teacher_id INT PRIMARY KEY,
        name VARCHAR(100),
        subject VARCHAR(100)
    );

CREATE TABLE classes (
        class_id INT PRIMARY KEY,
        class_name VARCHAR(100)
    );

CREATE TABLE courses (
        course_id INT PRIMARY KEY,
        course_name VARCHAR(100),
        teacher_id INT,
        class_id INT
    );