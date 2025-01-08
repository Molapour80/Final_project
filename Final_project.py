import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(
    filename='app.log',         
    filemode='a',              
    level=logging.INFO,        
    format='%(asctime)s - %(levelname)s - %(message)s'  
)

class DatabaseConnection:
    _connection = None

    @staticmethod
    def get_connection():
        if DatabaseConnection._connection is None:
            try:
                DatabaseConnection._connection = mysql.connector.connect(
                    host='localhost',
                    user='admin',
                    password='2001',
                    database='school'
                )
                if DatabaseConnection._connection.is_connected():
                    logging.info("Connected to the database")
                    DatabaseConnection.create_tables()
                else:
                    logging.error("Not connected")
            except Error as e:
                logging.error("Error connecting to the server: %s", e)
                DatabaseConnection._connection = None  
        return DatabaseConnection._connection

    @staticmethod
    def create_tables():
        """Creates tables in the database if they do not already exist."""
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Drop tables in reverse order of dependencies
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("DROP TABLE IF EXISTS classes")
        cursor.execute("DROP TABLE IF EXISTS teachers")
        cursor.execute("DROP TABLE IF EXISTS courses")

        # Create courses table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255),
            PRIMARY KEY(course_id)
        )
        """)

        # Create teachers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255),
            email VARCHAR(255),
            course_id INT,
            PRIMARY KEY (teacher_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
        )
        """)

        # Create classes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            class_id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255),
            teacher_id INT,
            PRIMARY KEY (class_id),
            FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
        )
        """)

        # Create students table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255),
            email VARCHAR(255),
            class_id INT,
            PRIMARY KEY (student_id),
            FOREIGN KEY (class_id) REFERENCES classes (class_id)
        )
        """)

        connection.commit()
        logging.info("Tables created successfully.")

# Class definitions
class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Student(Person):
    def __init__(self, student_id, name, email, class_id):
        super().__init__(name, email)
        self.student_id = student_id
        self.class_id = class_id

class Teacher(Person):
    def __init__(self, teacher_id, name, email, course_id):
        super().__init__(name, email)
        self.teacher_id = teacher_id
        self.course_id = course_id

class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name

class Class:
    def __init__(self, class_id, name, teacher_id):
        self.class_id = class_id
        self.name = name
        self.teacher_id = teacher_id

# Database operations for Students
class DatabaseStudent:
    def __init__(self, connection):
        self.connection = connection

    def add_student(self, student):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, class_id) VALUES (%s, %s, %s)",
            (student.name, student.email, student.class_id)
        )
        self.connection.commit()

    def get_student(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        return cursor.fetchone()

    def update_student(self, student):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE students SET name = %s, email = %s, class_id = %s WHERE student_id = %s",
            (student.name, student.email, student.class_id, student.student_id)
        )
        self.connection.commit()

    def delete_student(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        self.connection.commit()

    def search_by_student_id(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        return cursor.fetchone()

    def search_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name LIKE %s", ('%' + name + '%',))
        return cursor.fetchall()

    def search_by_class_id(self, class_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE class_id = %s", (class_id,))
        return cursor.fetchall()

# Database operations for Teachers
class DatabaseTeacher:
    def __init__(self, connection):
        self.connection = connection

    def add_teacher(self, teacher):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO teachers (name, email, course_id) VALUES (%s, %s, %s)",
            (teacher.name, teacher.email, teacher.course_id)
        )
        self.connection.commit()

    def get_teacher(self, teacher_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM teachers WHERE teacher_id = %s", (teacher_id,))
        return cursor.fetchone()

    def update_teacher(self, teacher):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE teachers SET name = %s, email = %s, course_id = %s WHERE teacher_id = %s",
            (teacher.name, teacher.email, teacher.course_id, teacher.teacher_id)
        )
        self.connection.commit()

    def delete_teacher(self, teacher_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
        self.connection.commit()

# Database operations for Courses
class DatabaseCourse:
    def __init__(self, connection):
        self.connection = connection

    def add_course(self, course):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO courses (name) VALUES (%s)",
            (course.name,)
        )
        self.connection.commit()

    def get_course(self, course_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        return cursor.fetchone()

    def update_course(self, course):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE courses SET name = %s WHERE course_id = %s",
            (course.name, course.course_id)
        )
        self.connection.commit()

    def delete_course(self, course_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        self.connection.commit()

# Database operations for Classes
class DatabaseClass:
    def __init__(self, connection):
        self.connection = connection

    def add_class(self, class_):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO classes (name, teacher_id) VALUES (%s, %s)",
            (class_.name, class_.teacher_id)
        )
        self.connection.commit()

    def get_class(self, class_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM classes WHERE class_id = %s", (class_id,))
        return cursor.fetchone()

    def update_class(self, class_):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE classes SET name = %s, teacher_id = %s WHERE class_id = %s",
            (class_.name, class_.teacher_id, class_.class_id)
        )
        self.connection.commit()

    def delete_class(self, class_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM classes WHERE class_id = %s", (class_id,))
        self.connection.commit()

