import mysql.connector
from mysql.connector import Error

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
                    print("Connected to the database")
                    DatabaseConnection.create_tables()
                else:
                    print("Not connected")
            except Error as e:
                print("Error connecting to the server:", e)
                DatabaseConnection._connection = None  
        return DatabaseConnection._connection

    @staticmethod
    def create_tables():
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        
        # Create teachers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            course_id INT
        )
        """)

        # Create students table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            class_id INT
        )
        """)

        # Create classes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            class_id INT PRIMARY KEY,
            name VARCHAR(255),
            teacher_id INT
        )
        """)

        # Create courses table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT PRIMARY KEY,
            name VARCHAR(255),
            teacher_id INT
        )
        """)

        connection.commit()
        print("Tables created successfully.")

class Student:
    def __init__(self, student_id, name, email, class_id):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.class_id = class_id

class Teacher:
    def __init__(self, teacher_id, name, email, course_id):
        self.teacher_id = teacher_id
        self.name = name
        self.email = email
        self.course_id = course_id

class DatabaseStudent:
    def __init__(self, db_connection):
        self.connection = db_connection

    def add_student(self, student):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO students (student_id, name, email, class_id) VALUES (%s, %s, %s, %s)",
            (student.student_id, student.name, student.email, student.class_id)
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



