from Final_project import *


def import_or_update_students_from_csv(db_student, db_class, file_path):
    """Import or update students from a CSV file into the database."""
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                email = row['email']
                class_id = int(row['class_id'])

                # Check if class exists before adding or updating student
                if db_class.get_class(class_id):
                    # Check if student already exists
                    existing_student = db_student.get_student_by_email(email)
                    if existing_student:
                        # Update existing student
                        existing_student.name = name
                        existing_student.class_id = class_id
                        db_student.update_student(existing_student)
                        print(f"Updated student: {name}")
                    else:
                        # Add new student
                        student = Student(student_id=None, name=name, email=email, class_id=class_id)
                        db_student.add_student(student)
                        print(f"Added student: {name}")
                else:
                    print(f"Class ID {class_id} does not exist. Skipping student: {name}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_report(db_student, db_class):
    """Generate a report of students and their classes."""
    students = db_student.get_all_students()
    report_data = []

    for student in students:
        class_name = db_class.get_class(student[3])[1]  
        report_data.append(f"Student ID: {student[0]}, Name: {student[1]}, Email: {student[2]}, Class: {class_name}")

    with open("student_report.txt", "w") as report_file:
        for line in report_data:
            report_file.write(line + "\n")
    print("Report generated: student_report.txt")

def main():
    connection_ = DatabaseConnection.get_connection()
    if connection_ is None:
        print("Failed to connect to the database.")
        return

    db_student = DatabaseStudent(connection_)
    db_teacher = DatabaseTeacher(connection_)
    db_class = DatabaseClass(connection_)
    db_course = DatabaseCourse(connection_)

    while True:
        print("Welcome to Sys school")
        print("\nSelect an operation:")
        print("1. Database Student")
        print("2. Database Teacher")
        print("3. Database Classes")
        print("4. Database Courses")
        print("5. Export Data to CSV") 
        print("6. Visualize Student Count")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            database_student(db_student, db_class)

        elif choice == "2":
            database_teacher(db_teacher,db_course)

        elif choice == "3":
            database_class(db_class, db_teacher)  

        elif choice == "4":
            database_courses(db_course)

        elif choice == "5":
            export_data_to_csv(db_student, db_teacher, db_class, db_course)  

        elif choice == "6":
            DataVisualization.plot_student_count_by_class()

        elif choice == "7":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice! Please try again.")

    connection_.close()

def export_data_to_csv(db_student, db_teacher, db_class, db_course):
    """Export information to CSV files."""
    try:
        # Export students
        with open('students.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student ID", "Name", "Email", "Class ID"])
            for student in db_student.get_all_students():
                writer.writerow(student)

        # Export teachers
        with open('teachers.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Teacher ID", "Name", "Email", "Course ID"])
            for teacher in db_teacher.get_all_teachers():
                writer.writerow(teacher)

        # Export classes
        with open('classes.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Class ID", "Name", "Teacher ID"])
            for class_ in db_class.get_all_classes():
                writer.writerow(class_)

        # Export courses
        with open('courses.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Course ID", "Name"])
            for course in db_course.get_all_courses():
                writer.writerow(course)

        print("Data exported to CSV files successfully.")
    except Exception as e:
        logging.error("Error exporting data to CSV: %s", e)
        print("Failed to export data to CSV. Please check the file permissions and try again.")

def database_student(db_student, db_class):
    while True:
        print("\nStudent Operations:")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. View Student")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter student name: ")
                email = input("Enter student email: ")
                class_id = int(input("Enter class ID: "))
                
                # Check if class exists before adding student
                if db_class.get_class(class_id):
                    student = Student(student_id=None, name=name, email=email, class_id=class_id)
                    db_student.add_student(student)
                    print("Student added successfully.")
                else:
                    print(f"Class ID {class_id} does not exist.")
            except ValueError:
                print("Invalid input for class ID. Please enter an integer.")
            except Exception as e:
                print(f"Error adding student: {e}")

        elif choice == "2":
            try:
                student_id = int(input("Enter student ID to update: "))
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
                        student.class_id = int(class_id)
                    db_student.update_student(student)
                    print("Student updated successfully.")
                else:
                    print("Student not found.")
            except ValueError:
                print("Invalid input. Please enter a valid student ID or class ID.")
            except Exception as e:
                print(f"Error updating student: {e}")

        elif choice == "3":
            try:
                student_id = int(input("Enter student ID to delete: "))
                db_student.delete_student(student_id)
                print("Student deleted successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid student ID.")
            except Exception as e:
                print(f"Error deleting student: {e}")

        elif choice == "4":
            try:
                student_id = int(input("Enter student ID to view: "))
                student = db_student.get_student(student_id)
                if student:
                    print(f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}, Class ID: {student[3]}")
                else:
                    print("Student not found.")
            except ValueError:
                print("Invalid input. Please enter a valid student ID.")

        elif choice == "5":
            break

        else:
            print("Invalid choice! Please try again.")

def database_teacher(db_teacher, db_course):
    while True:
        print("\nTeacher Operations:")
        print("1. Add Teacher")
        print("2. Update Teacher")
        print("3. Delete Teacher")
        print("4. View Teacher")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter teacher name: ")
                email = input("Enter teacher email: ")
                course_id = int(input("Enter course ID: "))

                
                if not db_course.get_course(course_id):
                    print(f"Course ID {course_id} does not exist.")
                    continue
                
                teacher = Teacher(teacher_id=None, name=name, email=email, course_id=course_id)
                db_teacher.add_teacher(teacher)
                print("Teacher added successfully.")
            except ValueError:
                print("Invalid input for course ID. Please enter an integer.")
            except Exception as e:
                print(f"Error adding teacher: {e}")

        elif choice == "2":
            try:
                teacher_id = int(input("Enter teacher ID to update: "))
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
                        teacher.course_id = int(course_id)
                    db_teacher.update_teacher(teacher)
                    print("Teacher updated successfully.")
                else:
                    print("Teacher not found.")
            except ValueError:
                print("Invalid input. Please enter a valid teacher ID or course ID.")
            except Exception as e:
                print(f"Error updating teacher: {e}")

        elif choice == "3":
            try:
                teacher_id = int(input("Enter teacher ID to delete: "))
                db_teacher.delete_teacher(teacher_id)
                print("Teacher deleted successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid teacher ID.")
            except Exception as e:
                print(f"Error deleting teacher: {e}")

        elif choice == "4":
            try:
                teacher_id = int(input("Enter teacher ID to view: "))
                teacher = db_teacher.get_teacher(teacher_id)
                if teacher:
                    print(f"ID: {teacher[0]}, Name: {teacher[1]}, Email: {teacher[2]}, Course ID: {teacher[3]}")
                else:
                    print("Teacher not found.")
            except ValueError:
                print("Invalid input. Please enter a valid teacher ID.")

        elif choice == "5":
            break

        else:
            print("Invalid choice! Please try again.")

def database_class(db_class, db_teacher):
    while True:
        print("\nClass Operations:")
        print("1. Add Class")
        print("2. Update Class")
        print("3. Delete Class")
        print("4. View Class")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter class name: ")
                teacher_id = int(input("Enter teacher ID: "))

                
                if not db_teacher.get_teacher(teacher_id):
                    print(f"Teacher ID {teacher_id} does not exist.")
                    continue
                
                class_ = Class(class_id=None, name=name, teacher_id=teacher_id)
                db_class.add_class(class_)
                print("Class added successfully.")
            except ValueError:
                print("Invalid input for teacher ID. Please enter an integer.")
            except Exception as e:
                print(f"Error adding class: {e}")

        elif choice == "2":
            try:
                class_id = int(input("Enter class ID to update: "))
                class_ = db_class.get_class(class_id)
                if class_:
                    name = input("Enter new name (leave blank to keep current): ")
                    teacher_id = input("Enter new teacher ID (leave blank to keep current): ")
                    if name:
                        class_.name = name
                    if teacher_id:
                        class_.teacher_id = int(teacher_id)
                    db_class.update_class(class_)
                    print("Class updated successfully.")
                else:
                    print("Class not found.")
            except ValueError:
                print("Invalid input. Please enter a valid class ID or teacher ID.")
            except Exception as e:
                print(f"Error updating class: {e}")

        elif choice == "3":
            try:
                class_id = int(input("Enter class ID to delete: "))
                db_class.delete_class(class_id)
                print("Class deleted successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid class ID.")
            except Exception as e:
                print(f"Error deleting class: {e}")

        elif choice == "4":
            try:
                class_id = int(input("Enter class ID to view: "))
                class_ = db_class.get_class(class_id)
                if class_:
                    print(f"ID: {class_[0]}, Name: {class_[1]}, Teacher ID: {class_[2]}")
                else:
                    print("Class not found.")
            except ValueError:
                print("Invalid input. Please enter a valid class ID.")

        elif choice == "5":
            break

        else:
            print("Invalid choice! Please try again.")

def database_courses(db_course):
    while True:
        print("\nCourse Operations:")
        print("1. Add Course")
        print("2. Update Course")
        print("3. Delete Course")
        print("4. View Course")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter course name: ")  
                course = Course(course_id=None, name=name)
                db_course.add_course(course)
                print("Course added successfully.")
            except Exception as e:
                print(f"Error adding course: {e}")

        elif choice == "2":
            try:
                course_id = int(input("Enter course ID to update: "))
                course = db_course.get_course(course_id)
                if course:
                    name = input("Enter new name (leave blank to keep current): ")
                    if name:
                        course.name = name
                    db_course.update_course(course)
                    print("Course updated successfully.")
                else:
                    print("Course not found.")
            except ValueError:
                print("Invalid input. Please enter a valid course ID.")
            except Exception as e:
                print(f"Error updating course: {e}")

        elif choice == "3":
            try:
                course_id = int(input("Enter course ID to delete: "))
                db_course.delete_course(course_id)
                print("Course deleted successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid course ID.")
            except Exception as e:
                print(f"Error deleting course: {e}")

        elif choice == "4":
            try:
                course_id = int(input("Enter course ID to view: "))
                course = db_course.get_course(course_id)
                if course:
                    print(f"ID: {course[0]}, Name: {course[1]}")
                else:
                    print("Course not found.")
            except ValueError:
                print("Invalid input. Please enter a valid course ID.")

        elif choice == "5":
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
    