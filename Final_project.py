
import mysql.connector
class Connection1:

    Connection_ = None

    @staticmethod
    def get_connection():

        if Connection1.Connection_ is None:
            Connection1._connection = mysql.connector.connect(
                host='localhost',
                user='admin',
                password='2001',
                database='school'
            )
        return Connection1.Connection_
    
class Student:
    def __init__(self, student_id, name, email, class_id):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.class_id = class_id


class Student_M:
    @staticmethod
    def add_student(student):
       
        connection = Connection1.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (student_id, name, email, class_id) VALUES (%s, %s, %s, %s)", 
                       (student.student_id, student.name, student.email, student.class_id))
        connection.commit()
        cursor.close()

    @staticmethod
    def delete_student(student_id):
        
        connection = Connection1.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        connection.commit()
        cursor.close()

    @staticmethod
    def update_student(student):
        
        connection = Connection1.get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, email = %s WHERE student_id = %s", 
                       (student.name, student.email, student.student_id))
        connection.commit()
        cursor.close()

    @staticmethod
    def search_student(student_id=None, name=None):
       
        connection = Connection1.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM students WHERE 1=1"
        params = []

        if student_id:
            query += " AND student_id = %s"
            params.append(student_id)
        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")

        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results

class ReportGenerator:
    

    @staticmethod
    def generate_student_report():
       
        connection = Connection1.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.close()
        
        report = "Student Report:\n"
        for student in students:
            report += f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}, Class ID: {student[3]}\n"
        return report


new_student = Student(student_id=1, name="Ali", email="ali@example.com", class_id=101)
Student_M.add_student(new_student)

found_students =Student_M.search_student(name="Ali")
print(found_students)

report = ReportGenerator.generate_student_report()
print(report)

new_student.name = "Ali Reza"
Student_M.update_student(new_student)

Student_M.delete_student(1)