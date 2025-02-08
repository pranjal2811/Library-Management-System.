import mysql.connector
from prettytable import PrettyTable

class Connection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def access_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pranjal28",
                use_pure=True
            )

            if self.connection.is_connected():
                print("Connected to MySQL database")
                self.cursor = self.connection.cursor()
                use_db_query = "USE library_managment"
                self.cursor.execute(use_db_query)
                print("Switched to database")

        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("SQL connection closed.")



class Admin_Function(Connection):
    def __init__(self):
        super().__init__()
        
        
    def admin_menu(self):
        while True:     
            print("1. View Books ")
            print("2. Add Book ")
            print("3. Delete Book ")
            print("4. Borrow Details")
            print("5. Back to main menu ")
            choice1= input("Make your choice: ")



            if choice1 == "1":
                self.show_booksAdmin()
            elif choice1== "2":
                self.Add_book()
            elif choice1 == "3":
                self.Delete_book()
            elif choice1 == "4":
                self.borrow_details()
            elif choice1 == "5":
                break
            else:
                print("Incorrect choice try again")

    def show_booksAdmin(self):
        query1= "select * from library"
        self.cursor.execute(query1)
        books = self.cursor.fetchall()

        table = PrettyTable(["Book ID", "Title", "Author", "Publish Date", "Copies"])
        for book in books:
            table.add_row(book)

        print("\nBooks Available in the Library:")
        print(table)

    def Add_book(self):
        print("Add your Book")
        
        B_title= input("Enter Book Title: ")
        B_author= input("Enter Author Name: ")
        B_publish= input("Enter Punlish Date (YYYY-MM-DD): ")
        B_count= int(input("Enter Available copys: "))
        Add_book_query = "insert into library (Title,Author_Name,Publish_Date,Copies) values (%s,%s,%s,%s);"
        self.cursor.execute(Add_book_query,(B_title,B_author,B_publish,B_count))
        self.connection.commit()
        print("Book added")

    def Delete_book(self):
        print("Delete your Book")
        B_Delete= int(input("Enter Book ID: "))
        Delete_book_query = f"delete from library where Book_id = {B_Delete};"
        self.cursor.execute(Delete_book_query)
        self.connection.commit()
        print("Book Deleted")


    def borrow_details(self):
        B_query= "select * from borrow_details"
        self.cursor.execute(B_query)
        Bdetails = self.cursor.fetchall()


        Btable = PrettyTable(["issue_id", "book_id", "student_id", "issue_date", "return_date"])
        for i in Bdetails:
            Btable.add_row(i)

        print("\nIssue Details:")
        print(Btable)


class Student_Function(Connection):
    def __init__(self):
        super().__init__()
        
    def student_menu(self):
        while True:
            print("\n login succesful")
            print("1. View Books ")
            print("2. Issue Book ")
            print("3. Return Book ")
            print("4. Show Details ")
            print("5. Back to main menu")
            choice2= input("Make your choice: ")



            if choice2 == "1":
                self.show_booksStu()
            elif choice2== "2":
                self.issue()
            elif choice2 == "3":
                self.return_books()
            elif choice2 == "4":
                self.issue_details()
            elif choice2 == "5":
                break
            else:
                print("Incorrect choice try again")
    
    def show_booksStu(self):
        query1= "select * from library"
        self.cursor.execute(query1)
        books = self.cursor.fetchall()

        table = PrettyTable(["Book ID", "Title", "Author", "Publish Date", "Copies"])
        for book in books:
            table.add_row(book)

        print("\nBooks Available in the Library:")
        print(table)

    
    def issue(self):
        while True:
            book_id = int(input("Enter Book ID to Issue: "))
            student_id = int(input("Enter Student ID: "))
            issue_date = input("Enter Issue Date (YYYY-MM-DD): ")
            


            query = "SELECT Copies FROM library WHERE Book_id = %s"
            self.cursor.execute(query, (book_id,))
            library = self.cursor.fetchone()

            if library and library[0] > 0:  # Ensure copies are available
        # Insert issue details into borrow_details
                query = "INSERT INTO borrow_details (Book_id, Student_id, Issue_date) VALUES (%s, %s, %s)"
                self.cursor.execute(query, (book_id, student_id, issue_date))

        # Update the number of copies in the library
                query = "UPDATE library SET Copies = Copies - 1 WHERE Book_id = %s"
                self.cursor.execute(query, (book_id,))

        # Commit the transaction
                self.connection.commit()
                print("Book issued successfully!")
                break
            else:
                print("Book not available!")


    def return_books(self):
        while True:
            R_book_id = int(input("Enter Book ID to Return: "))
            R_student_id = int(input("Enter Student ID: "))
            return_date = input("Enter Return Date (YYYY-MM-DD): ")


            self.cursor.reset()
    
            r_query = "SELECT * from borrow_details WHERE Book_id = %s and Student_id =%s and Return_date is Null"
            self.cursor.execute(r_query, (R_book_id,R_student_id))
            borrow_details = self.cursor.fetchall()
            

            if borrow_details:  
                update_query = "UPDATE borrow_details SET return_date = %s WHERE book_id = %s AND Student_Id = %s"
                self.cursor.execute(update_query, (return_date, R_book_id, R_student_id))
                restore_query = "UPDATE library SET Copies = Copies + 1 WHERE Book_id = %s"
                self.cursor.execute(restore_query, (R_book_id,))
                self.connection.commit()
                print("Book returned successfully!")
                break
                
            else:
                print("No record found for this Book ID and Student ID, or the book is already returned.")

    def issue_details(self):
        
        print("Enter Student Id")
        std_id= int(input("Enter here: "))
    
        query="Select Book_id,Issue_date,Return_date from borrow_details where Student_id=%s"
        self.cursor.execute(query,(std_id,))
        details=self.cursor.fetchall()

        if details:
            print("Borrow Details:")
            for row in details:
                print(f"Book ID: {row[0]}, Issue Date: {row[1]}, Return Date: {row[2]}")
        else:
            print("No borrow details found for this Student ID.")


class LibraryManagment(Admin_Function,Student_Function):
    def __init__(self):
        super().__init__()
        self.access_connection()

        

    def main_menu(self):
        while True:
            print("Welcome to Library")
            print("Enter your role")
            print("1. Admin")
            print("2. Student")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.student_login()
            elif choice == "3":
                self.close_connection()
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_login(self):
        try:
            user_id = int(input("Enter Admin ID: "))
            user_pass = input("Enter Admin Password: ")
            query = "SELECT * FROM admin WHERE userid = %s AND password = %s"
            self.cursor.execute(query, (user_id, user_pass))
            admin = self.cursor.fetchone()
            if admin:
                print("Admin login successful!")
                # Admin functionalities can go here
                if admin:
                    self.admin_menu()
            else:
                print("Invalid Admin ID or Password.")
                

        except Exception as e:
            print(f"Error during admin login: {e}")

    def student_login(self):
        try:
            student_id = int(input("Enter Student ID: "))
            student_pass = input("Enter Student Password: ")
            query1 = "SELECT * FROM student WHERE Student_Id = %s AND password = %s"
            self.cursor.execute(query1, (student_id, student_pass))
            student = self.cursor.fetchone()
            if student:
                print("Student login successful!")
                # Student functionalities can go here
            else:
                print("Invalid Student ID or Password.")
            if student:
                self.student_menu()

        except Exception as e:
            print(f"Error during student login: {e}")




# Run the program
if __name__ == "__main__":
    library = LibraryManagment()
    library.main_menu()



























    