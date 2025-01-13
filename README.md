# 🎓 School Management System 🏫

 💡 This project is a database management system for a school that allows you to manage students and teachers. The system includes features for adding, editing, deleting, and viewing information about students and teachers.

## 🚀 Features

- **Manage Students**: Add, update, delete, and view student information.
- **Manage Teachers**: Handle teacher records seamlessly.
- **Manage Classes and Courses**: Organize classes and courses efficiently.
- **Data Export**: Export information to CSV files for reporting.
- **Search Functionality**: Quickly find students or teachers by name.
- **Data Visualization**: Visualize student counts by class.

## Prerequisites ⚙️

To run this project, you need the following:

- **Python 3.x** 🐍
- **MySQL Server** 🗄️
- **MongoDB** 🌐 *(for NoSQL storage)*
- Required libraries:
  - `mysql-connector-python` 📦
  - `csv` (included with Python)
  - `logging` (included with Python)
  - `os` (included with Python)

#  Sys_mongodb 
- this file create wite the mongodb

#  📚 Usage:
python main.py

# 📜 Error Logging and Reporting
The system utilizes the logging module to record errors and significant events. All logs are stored in the Sys_school.log file for your review.

# 🗄️ MongoDB Integration
Write the sys_mongodb.py with mongodb.

# Table 
- Class Student 
| id | name | email | clases_id|
| :---: | :---: | :---: | :---: |

- Class Teacher
| id | name | email | course_id|
| :---: | :---: | :---: | :---: |

- class course
| id | name |
| :---: | :---: | 

- class clases
| id | name |teacher_id|
| :---: | :---: | :---: | :---: |

| Name | Last Name | Age |
| :---: | :---: | :---: |


