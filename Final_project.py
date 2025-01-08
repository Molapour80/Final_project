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

class DatabaseTeacher:  
    def __init__(self, db_connection):  
        self.connection = db_connection  

    def add_teacher(self, teacher):  
        cursor = self.connection.cursor()  
        cursor.execute(  
            "INSERT INTO teachers (teacher_id, name, email, course_id) VALUES (%s, %s, %s, %s)",  
            (teacher.teacher_id, teacher.name, teacher.email, teacher.course_id)  
        )  
        self.connection.commit()  

    def get_teacher(self, teacher_id):  
        cursor = self.connection.cursor()  
        cursor.execute("SELECT * FROM teachers WHERE teacher_id = %s", (teacher_id,))  
        return cursor.fetchone()  

    def delete_teacher(self, teacher_id):  
        cursor = self.connection.cursor()  
        cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))  
        self.connection.commit()

def main():
    connection_ = DatabaseConnection.get_connection()
    if connection_ is None:
        print("Failed to connect to the database.")
        return

    db_student = DatabaseStudent(connection_)
    db_teacher = DatabaseTeacher(connection_)

    while True:
        print("\nSelect an operation:")
        print("1. Add Teacher")
        print("2. Add Student")
        print("3. Get Teacher")
        print("4. Get Student")
        print("5. Update Student")
        print("6. Delete Teacher")
        print("7. Delete Student")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            teacher_id = input("Enter teacher ID: ")
            name = input("Enter teacher name: ")
            email = input("Enter teacher email: ")
            course_id = input("Enter course ID: ")
            new_teacher = Teacher(teacher_id, name, email, course_id)
            db_teacher.add_teacher(new_teacher)
            print("Added teacher:", new_teacher.name)

        elif choice == "2":
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            email = input("Enter student email: ")
            class_id = input("Enter class ID: ")
            new_student = Student(student_id, name, email, class_id)
            db_student.add_student(new_student)
            print("Added student:", new_student.name)

        elif choice == '3':
            teacher_id = input("Enter teacher ID to retrieve: ")
            teacher = db_teacher.get_teacher(teacher_id)
            print("Retrieved Teacher:", teacher)

        elif choice == '4':
            student_id = input("Enter student ID to retrieve: ")
            student = db_student.get_student(student_id)
            print("Retrieved Student:", student)

        elif choice == '5':
            student_id = input("Enter student ID to update: ")
            student = db_student.get_student(student_id)
            if student:
                print("Current Name:", student[1])
                student_name = input("Enter new name: ")
                student_email = input("Enter new email: ")
                student_class_id = input("Enter new class ID: ")
                updated_student = Student(student_id, student_name, student_email, student_class_id)
                db_student.update_student(updated_student)
                print("Updated student:", student_name)
            else:
                print("Student not found.")

        elif choice == '6':
            teacher_id = input("Enter teacher ID to delete: ")
            db_teacher.delete_teacher(teacher_id)
            print("Deleted teacher with ID:", teacher_id)

        elif choice == '7':
            student_id = input("Enter student ID to delete: ")
            db_student.delete_student(student_id)
            print("Deleted student with ID:", student_id)

        elif choice == '8':
            break

        else:
            print("Invalid choice! Please try again.")

    connection_.close()

if __name__ == "__main__":
    main()