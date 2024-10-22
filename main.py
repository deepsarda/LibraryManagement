# main.py
import tkinter as tk
from tkinter import messagebox
from user_management import get_user_fine, get_user_id, register_member, authenticate_user, update_user_fine
from circulation import issue_book, get_transactions
from catalog_management import search_books, get_book_by_id

def show_login_window():
    """
    Displays a window for logging in to the library management system. The user is asked to enter their username and password. If the username and password are valid, the window will be destroyed, and the main window will be displayed. If the username and password are invalid, an error message box will be displayed.

    :return: None
    """

    login_window = tk.Tk()
    login_window.title("Library Management System - Login")

    tk.Label(login_window, text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_window, text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        user = authenticate_user(username, password)
        if user:
            messagebox.showinfo("Login Success", f"Welcome {user['full_name']}!")
            login_window.destroy()
            show_main_window(user)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    tk.Button(login_window, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(login_window, text="Register", command=lambda: [login_window.destroy(), show_register_window()]).grid(row=3, column=0, columnspan=2, pady=5)
    
    login_window.mainloop()

def show_register_window():
    """
    A window for registering a new user. The user is asked to fill out a form with their username, password, full name, email, phone, and membership category. If the user is a student or staff, they must then confirm their registration with an admin/librarian username and password. After confirming their registration, the window will be destroyed, and the user will be logged in and shown the main window.
    """
    register_window = tk.Tk()
    register_window.title("Register New Member")

    labels = ["Username", "Password", "Full Name", "Email", "Phone", "Membership Category: (student/public/staff)"]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(register_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
        entry = tk.Entry(register_window)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[label] = entry

    def register():
        """
        Registers a new member in the database. The user is asked to fill out a form with their username, password, full name, email, phone, and membership category. If the user is a student or staff, they must then confirm their registration with an admin/librarian username and password. After confirming their registration, the window will be destroyed, and the user will be logged in and shown the main window.
        """
        username = entries["Username"].get()
        password = entries["Password"].get()
        full_name = entries["Full Name"].get()
        email = entries["Email"].get()
        phone = entries["Phone"].get()
        membership_category = entries["Membership Category: (student/public/staff)"].get()
        
        register_window.destroy()

        if not all([username, password, full_name, email, phone, membership_category]):
            messagebox.showerror("Error", "All fields are required.")
            return
        
         # Ask for an admin/librarian confimermation to confirm registration for students and staff
        if membership_category in ["student", "staff"]:

            staff_register_window = tk.Tk()
            staff_register_window.title("Confirm Registration")

            tk.Label(staff_register_window, text="Staff Username").grid(row=0, column=0, padx=10, pady=5)
            staff_username_entry = tk.Entry(staff_register_window)
            staff_username_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(staff_register_window, text="Staff Password").grid(row=1, column=0, padx=10, pady=5)
            staff_password_entry = tk.Entry(staff_register_window, show="*")
            staff_password_entry.grid(row=1, column=1, padx=10, pady=5)

            def authenticate_staff():
                """
                Authenticates the staff member for confirming registration. If the staff credentials are valid, the registration is confirmed, and the user is logged in and shown the main window. Otherwise, an error message is shown.
                """
                staff_username = staff_username_entry.get()
                staff_password = staff_password_entry.get()

                staff = authenticate_user(staff_username, staff_password)
                if staff and staff['role'] in ['admin', 'librarian']:
                    messagebox.showinfo("Success", "Registration confirmed.")
                    register_window.destroy()
                    success = register_member(username, password, 'borrower', full_name, email, phone, membership_category)

                    if not success:
                        messagebox.showerror("Error", "Registration failed.")
                    else:
                        messagebox.showinfo("Success", "Registration successful.")
        
                    staff_register_window.destroy()
                    show_login_window()
                else:
                    messagebox.showerror("Error", "Invalid staff credentials.")

            tk.Button(staff_register_window, text="Confirm Registration", command=authenticate_staff).grid(row=len(labels)+2, column=0, columnspan=2, pady=10)
        else:
            
            success = register_member(username, password, 'borrower', full_name, email, phone, membership_category)

            if not success:
                messagebox.showerror("Error", "Registration failed.")
            else:
                messagebox.showinfo("Success", "Registration successful.")
            
            show_login_window()

    tk.Button(register_window, text="Register", command=register).grid(row=len(labels), column=0, columnspan=2, pady=10)
    register_window.mainloop()

def show_main_window(user):
    """
    Shows the main window of the application, depending on the user's role.

    If the user is an admin or librarian, they can add books and pay fines.
    All users can search for books.
    """

    main_window = tk.Tk()
    main_window.title("Library Management System")

    tk.Label(main_window, text=f"Welcome, {user['full_name']}!", font=("Helvetica", 16)).pack(pady=20)
    tk.Label(main_window, text=f"Username: {user['username']}. Role: {user['role']}. Membership: {user['membership_category']}").pack(pady=10)
    # Get list of borrowed books
    transactions = get_transactions(user['user_id'])

    if transactions:
        tk.Label(main_window, text="Your borrowed books:").pack(pady=30)
        for transaction in transactions:
            # Get book by id
            book = get_book_by_id(transaction['book_id'])
            tk.Label(main_window, text=f"{book['title']} by {book['author']} ({book['isbn']}) - Due: {transaction['due_date']}").pack(pady=5)
    tk.Label(main_window, text="What would you like to do?").pack(pady=50)
    # Depending on user role, show different functionalities
    if user['role'] in ['admin', 'librarian']:
        tk.Button(main_window, text="Add Book", command=show_add_book_window).pack(pady=10)
        tk.Button(main_window, text="Pay Fine", command=show_pay_fine_window).pack(pady=10)

    tk.Button(main_window, text="Search/Borrow Books", command=lambda: show_search_books_window(user)).pack(pady=10)
    tk.Button(main_window, text="Logout", command=main_window.destroy).pack(pady=10)

    
    main_window.mainloop()

def show_add_book_window():
    """
    Opens a window to add a new book to the catalog.

    The window will have input fields for each of the book's attributes, and a button
    to add the book to the catalog. When the book is added successfully, a success
    message will be shown, and the window will be closed. If there is an error, an
    error message will be shown.
    """
    
    add_book_window = tk.Tk()
    add_book_window.title("Add New Book")

    labels = ["Title", "Author", "ISBN", "Publisher", "Edition", "Genre", "Language", "Publication Year", "Dewey Decimal", "Subject Tags", "Total Copies"]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(add_book_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
        entry = tk.Entry(add_book_window)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[label] = entry

    from catalog_management import add_book

    def add_book_to_db():
        try:
            data = {
                "title": entries["Title"].get(),
                "author": entries["Author"].get(),
                "isbn": entries["ISBN"].get(),
                "publisher": entries["Publisher"].get(),
                "edition": entries["Edition"].get(),
                "genre": entries["Genre"].get(),
                "language": entries["Language"].get(),
                "publication_year": int(entries["Publication Year"].get()),
                "dewey_decimal": entries["Dewey Decimal"].get(),
                "subject_tags": entries["Subject Tags"].get(),
                "total_copies": int(entries["Total Copies"].get())
            }
            add_book(**data)
            messagebox.showinfo("Success", "Book added successfully.")
            add_book_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data.")

    tk.Button(add_book_window, text="Add Book", command=add_book_to_db).grid(row=len(labels), column=0, columnspan=2, pady=10)
    add_book_window.mainloop()

def show_search_books_window(user):
  
    """
    Displays a window for searching books in the library catalog.

    The user can enter a keyword to search for books by title, author, ISBN, genre, language, or publication year.
    The search results, if any, are displayed in a new window, where each result is shown as a button with the
    book's title and author. Clicking on a result button shows more details about the book. If no results are found,
    a message is displayed.

    :param user: The user performing the search, used for accessing user-specific functionalities.
    """
    search_window = tk.Tk()
    search_window.title("Search Books")

    tk.Label(search_window, text="Enter keyword:").grid(row=0, column=0, padx=10, pady=10)
    keyword_entry = tk.Entry(search_window)
    keyword_entry.grid(row=0, column=1, padx=10, pady=10)


    def search():
        keyword = keyword_entry.get()
        results = search_books(keyword)
        results_window = tk.Toplevel(search_window)
        results_window.title("Search Results")
        #Add searchbar for another query
        tk.Label(search_window, text="Enter keyword:").grid(row=0, column=0, padx=10, pady=10)
        keyword = tk.Entry(search_window)
        tk.Label(results_window, text=f"Search results for '{keyword}':").grid(row=2, column=0, padx=10, pady=10)

        for idx, book in enumerate(results):
            tk.Button(results_window, text=f"{book['title']} by {book['author']}", command=lambda book=book: show_book_details_window(book, user, results_window)).grid(row=idx+4, column=0, padx=10, pady=5)

        # If no results are found, show a message
        if len(results) == 0:
            tk.Label(results_window, text="No results found.").grid(row=5, column=0, padx=10, pady=10)
            
        tk.Button(results_window, text="Close", command=results_window.destroy).grid(row=len(results)+5, column=0, padx=10, pady=10)
    tk.Button(search_window, text="Search", command=search).grid(row=3, column=0, columnspan=2, pady=10)
    search_window.mainloop()

def show_book_details_window(book, user ,results_window):
    """
    Opens a window to view more details about a book in the catalog.

    The window will have labels for each of the book's attributes, and a button
    to borrow the book. When the book is borrowed successfully, a success message
    will be shown, and the window will be closed. If there is an error, an error
    message will be shown.

    """
    book_details_window = tk.Tk()
    book_details_window.title("Book Details")

    tk.Label(book_details_window, text=f"Title: {book['title']}").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Author: {book['author']}").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"ISBN: {book['isbn']}").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Publisher: {book['publisher']}").grid(row=3, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Edition: {book['edition']}").grid(row=4, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Genre: {book['genre']}").grid(row=5, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Language: {book['language']}").grid(row=6, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Publication Year: {book['publication_year']}").grid(row=7, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Dewey Decimal: {book['dewey_decimal']}").grid(row=8, column=0, padx=10, pady=5)
    tk.Label(book_details_window, text=f"Subject Tags: {book['subject_tags']}").grid(row=9, column=0, padx=10, pady=5)


    def borrow():
        issue_book(user['user_id'], book['book_id'])
        messagebox.showinfo("Success", "Book borrowed successfully.")
        book_details_window.destroy()
        results_window.destroy()

    if book["available_copies"] == 0:
        tk.Button(book_details_window, text="Borrow", state="disabled", command=borrow).grid(row=10, column=0, columnspan=2, pady=10)
        tk.Label(book_details_window, text="No copies available.").grid(row=11, column=0, columnspan=2, pady=10)
    else:
        tk.Button(book_details_window, text="Borrow", command=borrow).grid(row=10, column=0, columnspan=2, pady=10)
    book_details_window.mainloop()
def show_pay_fine_window():
    """
    Displays a window to pay a fine.

    The window allows the user to enter their name and find their user ID to pay the fine.
    If the user is found, the fine payment process is initiated.
    If the user is not found, an error message is shown.

    """
    pay_fine_window = tk.Tk()
    pay_fine_window.title("Pay Fine")

    #Get user name
    tk.Label(pay_fine_window, text="Enter user name:").grid(row=0, column=0, padx=10, pady=10)
    user_name_entry = tk.Entry(pay_fine_window)
    user_name_entry.grid(row=0, column=1, padx=10, pady=10)

    def get_user_name():
        user_name = user_name_entry.get()
        
        user_id = get_user_id(user_name)
        if user_id:
            pay_fine_window.destroy()
            pay_fine(user_id)
        else:
            messagebox.showerror("Error", "User not found.")

    tk.Button(pay_fine_window, text="Find User", command=get_user_name).grid(row=1, column=0, columnspan=2, pady=10)
    pay_fine_window.mainloop()

def pay_fine(user_id):
    """
    Initiates the process of paying a fine for a user.

    This function checks the fine amount for the specified user ID. If the user has an outstanding fine, 
    it displays a window allowing the user to pay the fine. The user can enter the amount they wish to pay. 
    If the entered amount is valid, the fine is updated, and a success message is displayed. Otherwise, 
    an error message is shown.

    :param user_id: The unique identifier of the user whose fine is to be paid.
    """
    # Get fine amount
    
    fine_amount = get_user_fine(user_id)
    
    if fine_amount > 0:
        pay_fine_window = tk.Tk()
        tk.Label(pay_fine_window, text="Enter fine amount:").grid(row=0, column=0, padx=10, pady=10)
        fine_amount_entry = tk.Entry(pay_fine_window)
        fine_amount_entry.grid(row=0, column=1, padx=10, pady=10)

        def pay_fine():
            fine_amount_being_paid = fine_amount_entry.get()
            fine_amount_being_paid = int(fine_amount)
            if (fine_amount-fine_amount_being_paid) >= 0:
                update_user_fine(user_id, fine_amount-fine_amount_being_paid)
                messagebox.showinfo("Success", "Fine paid successfully.")
                pay_fine_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid fine amount.")

        tk.Button(pay_fine_window, text="Pay Fine", command=pay_fine).grid(row=1, column=0, columnspan=2, pady=10)
        pay_fine_window.mainloop()
    else:
        messagebox.showerror("Error", "No fine to pay.")

if __name__ == "__main__":
    while True:
        show_login_window()
