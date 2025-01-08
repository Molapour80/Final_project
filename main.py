from Final_project import *

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
        print("8. Search in Student")
        print("9. Search by Teacher")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter teacher name: ")
            email = input("Enter teacher email: ")
            course_id = int(input("Enter course ID: "))
            new_teacher = Teacher(teacher_id=None, name=name, email=email, course_id=course_id)
            db_teacher.add_teacher(new_teacher)
            print("Added teacher:", new_teacher.name)

        elif choice == "2":
            name = input("Enter student name: ")
            email = input("Enter student email: ")
            class_id = input("Enter class ID: ")
            new_student = Student(student_id=None, name=name, email=email, class_id=class_id)
            db_student.add_student(new_student)
            print("Added student:", new_student.name)

        elif choice == '3':
            teacher_id = input("Enter teacher ID to retrieve: ")
            teacher = db_teacher.get_teacher(teacher_id)
            if teacher:
                print("Retrieved Teacher:", teacher)
            else:
                print("Teacher not found.")

        elif choice == '4':
            student_id = input("Enter student ID to retrieve: ")
            student = db_student.get_student(student_id)
            if student:
                print("Retrieved Student:", student)
            else:
                print("Student not found.")

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
            search = input("Search by (student_id, name, class_id): ").lower()
            if search == "student_id":
                student_id = input("Enter student ID: ")
                student = db_student.search_by_student_id(student_id)
                print("Search Result:", student if student else "No results found.")
            elif search == "name":
                name = input("Enter name to search: ")
                results = db_student.search_by_name(name)
                print("Search Results:", results if results else "No results found.")
            elif search == "class_id":
                class_id = input("Enter class ID: ")
                results = db_student.search_by_class_id(class_id)
                print("Search Results:", results if results else "No results found.")
            else:
                print("Invalid search criteria.")

        elif choice == "9":
            teacher_id = input("Enter teacher ID to search: ")
            teacher = db_teacher.get_teacher(teacher_id)
            print("Search Result:", teacher if teacher else "No results found.")

        elif choice == "10":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice! Please try again.")

    connection_.close()

if __name__ == "__main__":
    main()
    