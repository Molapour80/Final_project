#https://github.com/Molapour80/Final_project
from Final_project import *

# Set up logging
logging.basicConfig(
    filename='Sys_school.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
#search_by name in teacher
def search_teachers_by_name(db_teacher):
    """Search for teachers by name."""
    name = input("Enter the name of the teacher to search for: ").strip().lower()
    teachers = db_teacher.get_all_teachers() 
    found_teachers = [teacher for teacher in teachers if name in teacher.name.lower()]
    
    if found_teachers:
        print("\nSearch Results:")
        for teacher in found_teachers:
            print(f"ID: {teacher.teacher_id}, Name: {teacher.name}, Email: {teacher.email}, Course ID: {teacher.course_id}")
    else:
        print("No teachers found with that name.")

#create the table
def save_table_structure_to_txt(file_path):
    """Save table structures and SQL commands to a text file."""
    table_structure = """
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
    """

    try:
        with open(file_path, mode='w') as file:
            file.write(table_structure)
        print(f"Table structure saved successfully at {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the table structure: {e}")

#show the information about the students ,email ,name , class_id 
def import_or_update_students_from_csv(db_student, db_class, file_path):
    """Import or update students from a CSV file into the database."""
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            required_columns = ['name', 'email', 'class_id']
            
            # Check for required columns in the CSV
            if not all(column in reader.fieldnames for column in required_columns):
                print(f"Error: The CSV file must contain the following columns: {', '.join(required_columns)}")
                return
            
            for row in reader:
                name = row['name']
                email = row['email']

                try:
                    class_id = int(row['class_id'])
                except ValueError:
                    print(f"Error: Class ID '{row['class_id']}' is not a valid integer for student '{name}'. Skipping.")
                    continue

                # Check if class exists before adding or updating student
                if db_class.get_class(class_id):
                    existing_student = db_student.get_student_by_email(email)
                    
                    if existing_student:
                        # Update existing student
                        existing_student.name = name
                        existing_student.class_id = class_id
                        db_student.update_student(existing_student)
                        logging.info(f"Updated student: {name}")
                        print(f"Updated student: {name}")
                    else:
                        # Add new student
                        student = Student(student_id=None, name=name, email=email, class_id=class_id)
                        db_student.add_student(student)
                        logging.info(f"Added student: {name}")
                        print(f"Added student: {name}")
                else:
                    print(f"Class ID {class_id} does not exist. Skipping student: {name}")
    
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_simple_valid_email(email):
    """Check if the provided email has a simple valid format."""
    if "@" not in email or "." not in email:
        return False
    username, domain = email.split("@")
    if len(username) < 1 or len(domain) < 3:
        return False
    return True


"""First the main option"""
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
        print("\nWelcome to Sys school")
        print("\nSelect an operation:")
        print("1. Database Student")
        print("2. Database Teacher")
        print("3. Database Classes")
        print("4. Database Courses")
        print("5. Export Data to CSV") 
        print("6. Visualize Student Count")
        print("7. Generate CSV Report")
        print("8. Save Table Structure to TXT")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            database_student(db_student, db_class)

        elif choice == "2":
            database_teacher(db_teacher, db_course)

        elif choice == "3":
            database_class(db_class, db_teacher)  

        elif choice == "4":
            database_courses(db_course)

        elif choice == "5":
            export_data_to_csv(db_student, db_teacher, db_class, db_course)

        elif choice == "6":
            DataVisualization.plot_student_count_by_class()

        elif choice == "7":
            selected_fields = select_fields_for_csv_report()
            if selected_fields:
                file_path = input("Enter your the name file to save the report(.csv): ")
                generate_csv_report(db_student, file_path, selected_fields)

        elif choice == "8":
            file_path = input("Enter the path to save the table structure (e.g., tables.txt): ")
            save_table_structure_to_txt(file_path)

        elif choice == "9":
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
                writer.writerow([student.student_id, student.name, student.email, student.class_id])

        # Export teachers
        with open('teachers.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Teacher ID", "Name", "Email", "Course ID"])
            for teacher in db_teacher.get_all_teachers():
                writer.writerow([teacher.teacher_id, teacher.name, teacher.email, teacher.course_id])

        # Export classes
        with open('classes.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Class ID", "Name", "Teacher ID"])
            for class_ in db_class.get_all_classes():
                writer.writerow([class_.class_id, class_.name, class_.teacher_id])

        # Export courses
        with open('courses.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Course ID", "Name"])
            for course in db_course.get_all_courses():
                writer.writerow([course.course_id, course.name])

        print("Data exported to CSV files successfully.")
    except Exception as e:
        logging.error("Error exporting data to CSV: %s", e)
        print("Failed to export data to CSV. Please check the file permissions and try again.")

# main student database
def database_student(db_student, db_class):
    while True:
        print("\nStudent Operations:")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4.search by name")
        print("5. View Student by ID")
        print("6. View All Students")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter student name: ")
                email = input("Enter student email: ")
                if not is_simple_valid_email(email):
                    print(f"Error: Invalid email format for {name}.")
                    continue
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
                    if email and not is_simple_valid_email(email):
                        print(f"Error: Invalid email format. Keeping current email.")
                        email = student.email
                    class_id = input("Enter new class ID (leave blank to keep current): ")

                    if name:
                        student.name = name
                    if email:
                        student.email = email
                    if class_id:
                        if db_class.get_class(int(class_id)):
                            student.class_id = int(class_id) 
                        else:
                            print(f"Class ID {class_id} does not exist. Keeping current class ID.")

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
            search_students_by_name(db_student) 

        elif choice == "5":
            try:
                student_id = int(input("Enter student ID to view: "))
                student = db_student.get_student(student_id)
                if student:
                    print(f"ID: {student.student_id}, Name: {student.name}, Email: {student.email}, Class ID: {student.class_id}")
                else:
                    print("Student not found.")
            except ValueError:
                print("Invalid input. Please enter a valid student ID.")

        elif choice == "6":
            try:
                students = db_student.get_all_students()  # Make sure to implement this method
                if students:
                    for student in students:
                        print(f"ID: {student.student_id}, Name: {student.name}, Email: {student.email}, Class ID: {student.class_id}")
                else:
                    print("No students found.")
            except Exception as e:
                print(f"Error retrieving students: {e}")

        elif choice == "7":
            break

        else:
            print("Invalid choice! Please try again.")

def database_teacher(db_teacher, db_course):
    while True:
        print("\nTeacher Operations:")
        print("1. Add Teacher")
        print("2. Update Teacher")
        print("3. Delete Teacher")
        print("4. Search Teachers by Name")
        print("5. View All Teachers")
        print("6. View Teacher by ID")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter teacher name: ")
                email = input("Enter teacher email: ")
                if not is_simple_valid_email(email):
                    print(f"Error: Invalid email format for {name}.")
                    continue
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
                        if db_course.get_course(int(course_id)):
                            teacher.course_id = int(course_id)
                        else:
                            print(f"Course ID {course_id} does not exist. Keeping current course ID.")

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
            search_teachers_by_name(db_teacher)

        elif choice == "5":
            try:
                teachers = db_teacher.get_all_teachers()  # Make sure to implement this method
                if teachers:
                    for teacher in teachers:
                        print(f"ID: {teacher.teacher_id}, Name: {teacher.name}, Email: {teacher.email}, Course ID: {teacher.course_id}")
                else:
                    print("No teachers found.")
            except Exception as e:
                print(f"Error retrieving teachers: {e}")

        elif choice == "6":
            try:
                teacher_id = int(input("Enter teacher ID to view: "))
                teacher = db_teacher.get_teacher(teacher_id)
                if teacher:
                    print(f"ID: {teacher.teacher_id}, Name: {teacher.name}, Email: {teacher.email}, Course ID: {teacher.course_id}")
                else:
                    print("Teacher not found.")
            except ValueError:
                print("Invalid input. Please enter a valid teacher ID.")

        elif choice == "7":
            break

        else:
            print("Invalid choice! Please try again.")

def database_class(db_class, db_teacher):
    while True:
        print("\nClass Operations:")
        print("1. Add Class")
        print("2. Update Class")
        print("3. Delete Class")
        print("4. View Class by ID")
        print("5. View All Classes")
        print("6. Back to Main Menu")

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
                        if db_teacher.get_teacher(int(teacher_id)):
                            class_.teacher_id = int(teacher_id)
                        else:
                            print(f"Teacher ID {teacher_id} does not exist. Keeping current teacher ID.")

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
                    print(f"ID: {class_.class_id}, Name: {class_.name}, Teacher ID: {class_.teacher_id}")
                else:
                    print("Class not found.")
            except ValueError:
                print("Invalid input. Please enter a valid class ID.")

        elif choice == "5":
            try:
                classes = db_class.get_all_classes() 
                if classes:
                    for class_ in classes:
                        print(f"ID: {class_.class_id}, Name: {class_.name}, Teacher ID: {class_.teacher_id}")
                else:
                    print("No classes found.")
            except Exception as e:
                print(f"Error retrieving classes: {e}")

        elif choice == "6":
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
            
            courses = db_course.get_all_courses()
            for course in courses:
                print(f"ID: {course.course_id}, Name: {course.name}") 

        elif choice == "5":
            break

        else:
            print("Invalid choice! Please try again.")


def format_student_data(student):
    """Format student data for CSV output."""
    return {
        'student_id': student.student_id,
        'name': student.name.title(),  # Capitalize name
        'email': student.email.lower(),  # Lowercase email
        'class_id': student.class_id,
        'registration_date': student.registration_date.strftime('%Y-%m-%d')  # Format date
    }

def generate_csv_report(db_student, file_path, selected_fields):
    """Generate or append to a CSV report based on selected fields."""
    if os.path.exists(file_path):
        mode = 'a'  # Append mode
    else:
        mode = 'w'  # Write mode (create new file)

    try:
        with open(file_path, mode=mode, newline='') as file:
            writer = csv.DictWriter(file, fieldnames=selected_fields)
            
            # If creating a new file, write the header
            if mode == 'w':
                writer.writeheader()

            students = db_student.get_all_students()
            
            for student in students:
                # Format data before writing
                formatted_data = format_student_data(student)
                writer.writerow({field: formatted_data[field] for field in selected_fields})
        
        print(f"Report generated successfully at {file_path}")
        logging.info(f"Report generated successfully at {file_path}")
    except Exception as e:
        print(f"An error occurred while generating the report: {e}")
def select_fields_for_csv_report():
    """Allow the user to select fields for the CSV report."""
    print("Select fields for the report (comma-separated):")
    print("Available fields: student_id, name, email, class_id")
    
    selected_fields = input("Enter fields: ").split(',')
    selected_fields = [field.strip() for field in selected_fields]

    valid_fields = ['student_id', 'name', 'email', 'class_id']
    if not all(field in valid_fields for field in selected_fields):
        print("Error: One or more selected fields are invalid.")
        return None
    
    return selected_fields

if __name__ == "__main__":
    main()
      
    