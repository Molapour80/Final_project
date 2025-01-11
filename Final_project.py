import mysql.connector
import logging
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import csv
from main import is_simple_valid_email

# Set up logging
logging.basicConfig(filename='Sys_school.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                logging.info("Connected to the database")
            except mysql.connector.Error as e:
                logging.error("Error connecting to the database: %s", e)
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
        cursor.close()  
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
        if not is_simple_valid_email(student.email):
            logging.error(f"Invalid email format for student: {student.name}")
            print(f"Error: Invalid email format for {student.name}.")
            return
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, class_id) VALUES (%s, %s, %s)",
            (student.name, student.email, student.class_id)
        )
        self.connection.commit()
        cursor.close()
        logging.info(f"Added student: {student.name}")

    def get_student(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        cursor.close()  # Close cursor
        return student

    def get_student_by_email(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        student = cursor.fetchone()
        cursor.close()  # Close cursor
        return student

    def update_student(self, student):
        if not is_simple_valid_email(student.email):
            logging.error(f"Invalid email format for student: {student.name}")
            print(f"Error: Invalid email format for {student.name}.")
            return
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE students SET name = %s, email = %s, class_id = %s WHERE student_id = %s",
            (student.name, student.email, student.class_id, student.student_id)
        )
        self.connection.commit()
        cursor.close()
        logging.info(f"Updated student: {student.name}")

    def delete_student(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        self.connection.commit()
        cursor.close()  # Close cursor
        logging.info(f"Deleted student ID: {student_id}")

    def get_all_students(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students")
        results = cursor.fetchall()
        cursor.close()
        return [Student(student_id=row[0], name=row[1], email=row[2], class_id=row[3]) for row in results]

# Database operations for Teachers
class DatabaseTeacher:
    def __init__(self, connection):
        self.connection = connection

    def add_teacher(self, teacher):
        if not is_simple_valid_email(teacher.email):
            logging.error(f"Invalid email format for teacher: {teacher.name}")
            print(f"Error: Invalid email format for {teacher.name}.")
            return
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO teachers (name, email, course_id) VALUES (%s, %s, %s)",
            (teacher.name, teacher.email, teacher.course_id)
        )
        self.connection.commit()
        cursor.close()
        logging.info(f"Added teacher: {teacher.name}")
    def get_teacher(self, teacher_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM teachers WHERE teacher_id = %s", (teacher_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Teacher(teacher_id=result[0], name=result[1], email=result[2], course_id=result[3])
        return None

    def update_teacher(self, teacher):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE teachers SET name = %s, email = %s, course_id = %s WHERE teacher_id = %s",
            (teacher.name, teacher.email, teacher.course_id, teacher.teacher_id)
        )
        self.connection.commit()
        cursor.close()
        logging.info(f"Updated teacher: {teacher.name}")

    def delete_teacher(self, teacher_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
        self.connection.commit()
        cursor.close()
        logging.info(f"Deleted teacher ID: {teacher_id}")

    def get_all_teachers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM teachers")
        results = cursor.fetchall()
        cursor.close()
        return [Teacher(teacher_id=row[0], name=row[1], email=row[2], course_id=row[3]) for row in results]
# Database operations for Courses
class DatabaseCourse:
    def __init__(self, connection):
        self.connection = connection

    def add_course(self, course):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO courses (name) VALUES (%s)", (course.name,))
        self.connection.commit()
        cursor.close()  # Close cursor
        logging.info(f"Added course: {course.name}")

    def get_course(self, course_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None  

    def update_course(self, course):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE courses SET name = %s WHERE course_id = %s", (course.name, course.course_id))
        self.connection.commit()
        cursor.close()  # Close cursor
        logging.info(f"Updated course: {course.name}")

    def delete_course(self, course_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        self.connection.commit()
        cursor.close()  # Close cursor
        logging.info(f"Deleted course ID: {course_id}")

    def get_all_courses(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM courses")
        results = cursor.fetchall()
        cursor.close()  # Close cursor
        return [Course(course_id=row[0], name=row[1]) for row in results]
        

# Database operations for Classes
class DatabaseClass:
    def __init__(self, connection):
        self.connection = connection

    def add_class(self, class_):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO classes (name, teacher_id) VALUES (%s, %s)", 
                       (class_.name, class_.teacher_id))
        self.connection.commit()
        cursor.close()
        logging.info(f"Added class: {class_.name}")

    def get_class(self, class_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM classes WHERE class_id = %s", (class_id,))
        class_ = cursor.fetchone()
        cursor.close()
        return class_

    def update_class(self, class_):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE classes SET name = %s, teacher_id = %s WHERE class_id = %s",
                       (class_.name, class_.teacher_id, class_.class_id))
        self.connection.commit()
        cursor.close()
        logging.info(f"Updated class: {class_.name}")

    def delete_class(self, class_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM classes WHERE class_id = %s", (class_id,))
        self.connection.commit()
        cursor.close()
        logging.info(f"Deleted class ID: {class_id}")

    def get_all_classes(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM classes")
        results = cursor.fetchall()
        cursor.close()
        return [Class(class_id=row[0], name=row[1], teacher_id=row[2]) for row in results]


class DataVisualization:
    @staticmethod
    def plot_student_count_by_class():
        query = """
        SELECT classes.name AS class_name, COUNT(students.student_id) AS student_count
        FROM classes
        LEFT JOIN students ON classes.class_id = students.class_id
        GROUP BY classes.class_id
        """
        connection = DatabaseConnection.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Convert results to DataFrame
                df = pd.DataFrame(results, columns=['class_name', 'student_count'])
                
                plt.figure(figsize=(10, 6))
                plt.bar(df['class_name'], df['student_count'], color='skyblue')
                plt.title('Number of Students by Class')
                plt.xlabel('Class Name')
                plt.ylabel('Student Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            except Exception as e:
                logging.error("Error while plotting data: %s", e)
            finally:
                cursor.close()
