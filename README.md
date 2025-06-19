Python : Library Management System

Introduction

This project is a console-based Library Management System implemented in Python, utilizing mysql.connector for database interactions and prettytable for formatted output. The system allows both administrators and students to manage library operations, including viewing, adding, deleting, issuing, and returning books. It provides a structured interface for common library tasks, ensuring proper record-keeping and book availability.

Objective
The primary objectives of this Library Management System are:

To provide a robust and user-friendly console interface for library administration.

To manage book inventory, including adding new books, deleting existing ones, and updating stock.

To facilitate book borrowing and returning processes for students, tracking issue and return dates.

To maintain separate login functionalities for administrators and students, ensuring role-based access to features.

To integrate with a MySQL database for persistent storage of library, admin, student, and borrow details.

Implementation Steps
The Library.py script implements the system through the following classes and functionalities:

Connection Class:

Handles the establishment and termination of the MySQL database connection.

Connects to a local MySQL instance with specified credentials (host="localhost", user="root", password="pranjal28").

Selects the library_managment database.

Includes error handling for connection issues.

Admin_Function Class (inherits from Connection):

Provides an admin_menu with options for administrators.

show_booksAdmin(): Fetches and displays all books from the library table in a PrettyTable format, showing Book ID, Title, Author, Publish Date, and Copies.

Add_book(): Prompts for Book Title, Author Name, Publish Date (YYYY-MM-DD), and Available Copies, then inserts the new book into the library table.

Delete_book(): Prompts for a Book ID and deletes the corresponding book from the library table.

borrow_details(): Fetches and displays all borrowing records from the borrow_details table in a PrettyTable, showing issue_id, book_id, student_id, issue_date, and return_date.

Student_Function Class (inherits from Connection):

Provides a student_menu with options for students.

show_booksStu(): Similar to the admin function, displays all available books.

issue(): Prompts for Book ID, Student ID, and Issue Date. It checks for book availability (copies > 0) in the library table, inserts a new record into borrow_details, and decrements the Copies count in the library table.

return_books(): Prompts for Book ID, Student ID, and Return Date. It updates the return_date in borrow_details for the specified book and student, and increments the Copies count in the library table. Includes checks to ensure the book was previously issued and not already returned.

issue_details(): Prompts for Student ID and displays the Book_id, Issue_date, and Return_date for all books borrowed by that student.

LibraryManagment Class (inherits from Admin_Function and Student_Function):

The main class that initializes the database connection.

main_menu(): The entry point of the application, allowing users to choose between Admin, Student, or Exit roles.

admin_login(): Authenticates admin users against admin table using userid and password. If successful, grants access to the admin_menu.

student_login(): Authenticates student users against student table using Student_Id and password. If successful, grants access to the student_menu.

Requirements
Python 3.x

mysql.connector library (pip install mysql-connector-python)

prettytable library (pip install prettytable)

A running MySQL server.

A MySQL database named library_managment with the following tables (and necessary data for admin and student for login):

library: Book_id (PK, auto-increment), Title, Author_Name, Publish_Date, Copies

borrow_details: issue_id (PK, auto-increment), Book_id, Student_id, Issue_date, Return_date

admin: userid, password

student: Student_Id, password

Usage
Ensure MySQL is running and the library_managment database with the required tables is set up.

Update the MySQL connection details (user, password) in Library.py if different from the default (root, pranjal28).

Run the script: python Library.py

Follow the console prompts to interact with the system as an Admin or Student.

Contact Information
For any questions, discussions, or potential collaborations on this project, please feel free to connect:

Name: Pranjal Joshi

Email: pranjaljoshi2811@gmail.com

GitHub: https://github.com/pranjal2811

LinkedIn: https://www.linkedin.com/in/pranjaljoshi2811
