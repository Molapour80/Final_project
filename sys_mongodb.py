import logging
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import csv
from pymongo import MongoClient

# logging
logging.basicConfig(filename='Sys_school.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseConnection:
    _client = None
    _db = None

    @staticmethod
    def get_connection():
        if DatabaseConnection._client is None:
            try:
                DatabaseConnection._client = MongoClient('mongodb://localhost:27017/')
                DatabaseConnection._db = DatabaseConnection._client['school']
                logging.info("Connected to the database")
            except Exception as e:
                logging.error("Error connecting to the database: %s", e)
                DatabaseConnection._client = None
        return DatabaseConnection._db

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

#class class
class Class:
    def __init__(self, class_id, name, teacher_id):
        self.class_id = class_id
        self.name = name
        self.teacher_id = teacher_id

# Database operations for Students
class DatabaseStudent:
    def __init__(self, db):
        self.collection = db['students']

    def add_student(self, student):
        if not is_simple_valid_email(student.email):
            logging.error(f"Invalid email format for student: {student.name}")
            print(f"Error: Invalid email format for {student.name}.")
            return
        self.collection.insert_one({
            'name': student.name,
            'email': student.email,
            'class_id': student.class_id
        })
        logging.info(f"Added student: {student.name}")

    def get_student(self, student_id):
        return self.collection.find_one({'_id': student_id})

    def get_student_by_email(self, email):
        return self.collection.find_one({'email': email})

    def update_student(self, student):
        if not is_simple_valid_email(student.email):
            logging.error(f"Invalid email format for student: {student.name}")
            print(f"Error: Invalid email format for {student.name}.")
            return
        self.collection.update_one(
            {'_id': student.student_id},
            {'$set': {'name': student.name, 'email': student.email, 'class_id': student.class_id}}
        )
        logging.info(f"Updated student: {student.name}")

    def delete_student(self, student_id):
        self.collection.delete_one({'_id': student_id})
        logging.info(f"Deleted student ID: {student_id}")

    def get_all_students(self):
        return [
            Student(
                student_id=str(student['_id']),
                name=student.get('name', 'Unknown'),
                email=student.get('email', 'No Email'),
                class_id=student.get('class_id', 'Unknown')
            ) for student in self.collection.find()
        ]
    
# Database operations for Teachers
class DatabaseTeacher:
    def __init__(self, db):
        self.collection = db['teachers']

    def add_teacher(self, teacher):
        if not is_simple_valid_email(teacher.email):
            logging.error(f"Invalid email format for teacher: {teacher.name}")
            print(f"Error: Invalid email format for {teacher.name}.")
            return
        self.collection.insert_one({
            'name': teacher.name,
            'email': teacher.email,
            'course_id': teacher.course_id
        })
        logging.info(f"Added teacher: {teacher.name}")

    def get_teacher(self, teacher_id):
        return self.collection.find_one({'_id': teacher_id})

    def update_teacher(self, teacher):
        if not is_simple_valid_email(teacher.email):
            logging.error(f"Invalid email format for teacher: {teacher.name}")
            print(f"Error: Invalid email format for {teacher.name}.")
            return
        self.collection.update_one(
            {'_id': teacher.teacher_id},
            {'$set': {'name': teacher.name, 'email': teacher.email, 'course_id': teacher.course_id}}
        )
        logging.info(f"Updated teacher: {teacher.name}")
    def delete_teacher(self, teacher_id):
        self.collection.delete_one({'_id': teacher_id})
        logging.info(f"Deleted teacher ID: {teacher_id}")

    def get_all_teachers(self):
        return [Teacher(teacher_id=str(teacher['_id']), name=teacher['name'], email=teacher['email'], course_id=teacher['course_id']) for teacher in self.collection.find()]

# Database operations for Courses
class DatabaseCourse:
    def __init__(self, db):
        self.collection = db['courses']

    def add_course(self, course):
        self.collection.insert_one({'name': course.name})
        logging.info(f"Added course: {course.name}")

    def get_course(self, course_id):
        return self.collection.find_one({'_id': course_id})

    def update_course(self, course):
        self.collection.update_one(
            {'_id': course.course_id},
            {'$set': {'name': course.name}}
        )
        logging.info(f"Updated course: {course.name}")

    def delete_course(self, course_id):
        self.collection.delete_one({'_id': course_id})
        logging.info(f"Deleted course ID: {course_id}")

    def get_all_courses(self):
        return [Course(course_id=str(course['_id']), name=course['name']) for course in self.collection.find()]

# Database operations for Classes
class DatabaseClass:
    def __init__(self, db):
        self.collection = db['classes']

    def add_class(self, class_):
        self.collection.insert_one({'name': class_.name, 'teacher_id': class_.teacher_id})
        logging.info(f"Added class: {class_.name}")

    def get_class(self, class_id):
        return self.collection.find_one({'_id': class_id})

    def update_class(self, class_):
        self.collection.update_one(
            {'_id': class_.class_id},
            {'$set': {'name': class_.name, 'teacher_id': class_.teacher_id}}
        )
        logging.info(f"Updated class: {class_.name}")

    def delete_class(self, class_id):
        self.collection.delete_one({'_id': class_id})
        logging.info(f"Deleted class ID: {class_id}")

    def get_all_classes(self):
        return [Class(class_id=str(class_['_id']), name=class_['name'], teacher_id=class_['teacher_id']) for class_ in self.collection.find()]

class DataVisualization:
    @staticmethod
    def plot_student_count_by_class():
        # Similar to your previous implementation, but adapted for MongoDB
        pipeline = [
            {
                '$lookup': {
                    'from': 'students',
                    'localField': '_id',
                    'foreignField': 'class_id',
                    'as': 'students'
                }
            },
            {
                '$project': {
                    'class_name': '$name',
                    'student_count': {'$size': '$students'}
                }
            }
        ]
        results = DatabaseConnection.get_connection()['classes'].aggregate(pipeline)

        df = pd.DataFrame(results)
        plt.figure(figsize=(10, 6))
        plt.bar(df['class_name'], df['student_count'], color='skyblue')
        plt.title('Number of Students by Class')
        plt.xlabel('Class Name')
        plt.ylabel('Student Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def is_simple_valid_email(email):
    """Check if the provided email has a simple valid format."""
    if "@" not in email or "." not in email:
        return False
    username, domain = email.split("@")
    if len(username) < 1 or len(domain) < 3:
        return False
    return True

def main():
    db = DatabaseConnection.get_connection()
    if db is None:
        print("Failed to connect to the database.")
        return

    db_student = DatabaseStudent(db)
    db_teacher = DatabaseTeacher(db)
    db_class = DatabaseClass(db)
    db_course = DatabaseCourse(db)

    while True:
        print("\nMenu:")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. View All Students")
        print("5. Add Teacher")
        print("6. Update Teacher")
        print("7. Delete Teacher")
        print("8. View All Teachers")
        print("9. Add Class")
        print("10. Update Class")
        print("11. Delete Class")
        print("12. View All Classes")
        print("13. Add Course")
        print("14. Update Course")
        print("15. Delete Course")
        print("16. View All Courses")
        print("17. Visualize Student Count by Class")
        print("18. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter student name: ")
            email = input("Enter student email: ")
            class_id = input("Enter class ID: ")
            student = Student(student_id=None, name=name, email=email, class_id=class_id)
            db_student.add_student(student)

        elif choice == "2":
            student_id = input("Enter student ID to update: ")
            student = db_student.get_student(student_id)
            if student:
                name = input("Enter new name (leave blank to keep current): ")
                email = input("Enter new email (leave blank to keep current): ")
                class_id = input("Enter new class ID (leave blank to keep current): ")
                if name:
                    student.name = name
                if email:
                    student.email = email
                if class_id:
                    student.class_id = class_id
                db_student.update_student(student)

        elif choice == "3":
            student_id = input("Enter student ID to delete: ")
            db_student.delete_student(student_id)

        elif choice == "4":
            students = db_student.get_all_students()
            for student in students:
                print(f"ID: {student.student_id}, Name: {student.name}, Email: {student.email}, Class ID: {student.class_id}")

        elif choice == "5":
            name = input("Enter teacher name: ")
            email = input("Enter teacher email: ")
            course_id = input("Enter course ID: ")
            teacher = Teacher(teacher_id=None, name=name, email=email, course_id=course_id)
            db_teacher.add_teacher(teacher)

        elif choice == "6":
            teacher_id = input("Enter teacher ID to update: ")
            teacher = db_teacher.get_teacher(teacher_id)
            if teacher:
                name = input("Enter new name (leave blank to keep current): ")
                email = input("Enter new email (leave blank to keep current): ")
                course_id = input("Enter new course ID (leave blank to keep current): ")
                if name:
                    teacher.name = name
                if email:
                    teacher.email = email
                if course_id:
                    teacher.course_id = course_id
                db_teacher.update_teacher(teacher)

        elif choice == "7":
            teacher_id = input("Enter teacher ID to delete: ")
            db_teacher.delete_teacher(teacher_id)

        elif choice == "8":
            teachers = db_teacher.get_all_teachers()
            for teacher in teachers:
                print(f"ID: {teacher.teacher_id}, Name: {teacher.name}, Email: {teacher.email}, Course ID: {teacher.course_id}")

        elif choice == "9":
            class_name = input("Enter class name: ")
            teacher_id = input("Enter teacher ID for this class: ")
            class_ = Class(class_id=None, name=class_name, teacher_id=teacher_id)
            db_class.add_class(class_)

        elif choice == "10":
            class_id = input("Enter class ID to update: ")
            class_ = db_class.get_class(class_id)
            if class_:
                name = input("Enter new name (leave blank to keep current): ")
                teacher_id = input("Enter new teacher ID (leave blank to keep current): ")
                if name:
                    class_.name = name
                if teacher_id:
                    class_.teacher_id = teacher_id
                db_class.update_class(class_)

        elif choice == "11":
            class_id = input("Enter class ID to delete: ")
            db_class.delete_class(class_id)

        elif choice == "12":
            classes = db_class.get_all_classes()
            for class_ in classes:
                print(f"ID: {class_.class_id}, Name: {class_.name}, Teacher ID: {class_.teacher_id}")

        elif choice == "13":
            course_name = input("Enter course name: ")
            course = Course(course_id=None, name=course_name)
            db_course.add_course(course)

        elif choice == "14":
            course_id = input("Enter course ID to update: ")
            course = db_course.get_course(course_id)
            if course:
                name = input("Enter new name (leave blank to keep current): ")
                if name:
                    course.name = name
                db_course.update_course(course)

        elif choice == "15":
            course_id = input("Enter course ID to delete: ")
            db_course.delete_course(course_id)

        elif choice == "16":
            courses = db_course.get_all_courses()
            for course in courses:
                print(f"ID: {course.course_id}, Name: {course.name}")

        elif choice == "17":
            DataVisualization.plot_student_count_by_class()

        elif choice == "18":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()