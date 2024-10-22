from db_config import create_connection
import mysql.connector
from datetime import datetime, timedelta
from tkinter import messagebox

def get_transactions(user_id):
    """
    Returns the list of books borrowed by a user.

    Parameters:
    user_id (int): The user ID.

    Returns:
    list: The list of books borrowed by the user.
    """
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM transactions WHERE user_id = %s AND return_date IS NULL"
    cursor.execute(query, (user_id,))
    books = cursor.fetchall()   
    cursor.close()
    connection.close()
    return books

def issue_book(user_id, book_id):
    """
    Issues a book to a user.

    :param user_id: The ID of the user
    :param book_id: The ID of the book
    :return: None
    """
    
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        # Make sure user has no fines
        cursor.execute("SELECT fines FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            messagebox.showerror("Error", "User has outstanding fines.")
            return
        # Check availability
        cursor.execute("SELECT available_copies FROM books WHERE book_id = %s", (book_id,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            due_date = datetime.now().date() + timedelta(days=14)  # 2 weeks loan period
            query = """INSERT INTO transactions (user_id, book_id, issue_date, due_date)
                       VALUES (%s, %s, %s, %s)"""
            values = (user_id, book_id, datetime.now().date(), due_date)
            try:
                cursor.execute(query, values)
                # Decrement available copies
                cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s", (book_id,))
                connection.commit()
                messagebox.showinfo("Success", "Book issued successfully.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            messagebox.showerror("Error","Book is not available.")
        cursor.close()
        connection.close()

def return_book(transaction_id):
    """
    Returns a book given its transaction_id.

    :param transaction_id: The unique id of the transaction.
    :return: None
    """

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        # Get book_id from transaction
        cursor.execute("SELECT book_id, due_date FROM transactions WHERE transaction_id = %s AND return_date IS NULL", (transaction_id,))
        result = cursor.fetchone()
        if result:
            book_id, due_date = result
            return_date = datetime.now().date()
            # Update transaction
            cursor.execute("UPDATE transactions SET return_date = %s WHERE transaction_id = %s", (return_date, transaction_id))
            # Increment available copies
            cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s", (book_id,))
            # Get user membership
            cursor.execute("SELECT membership FROM users WHERE user_id = (SELECT user_id FROM transactions WHERE transaction_id = %s)", (transaction_id,))
            membership = cursor.fetchone()[0]
            # Calculate fines if any and if user membership is not staff
            if return_date > due_date and membership != 'staff':
                days_over = (return_date - due_date).days
                fine = days_over * (10 if membership == 'public' else 5)  # Assume 10 rupees per day for public 5 rupees for student
                cursor.execute("SELECT user_id FROM transactions WHERE transaction_id = %s", (transaction_id,))
                user_id = cursor.fetchone()[0]
                cursor.execute("UPDATE users SET fines = fines + %s WHERE user_id = %s", (fine, user_id))
                messagebox.showinfo("Success", f"Book returned with a fine of ${fine}.")
            else:
                messagebox.showinfo("Success", "Book returned on time.")
            connection.commit()
        else:
            messagebox.showerror("Error","Transaction not found or book already returned.")
        cursor.close()
        connection.close()
