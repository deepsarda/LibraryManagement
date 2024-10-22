# user_management.py
from db_config import create_connection
import mysql.connector
import hashlib
from tkinter import messagebox
def hash_password(password):
    """
    Hashes a password using SHA-256.

    Parameters:
    password (str): The password to hash.

    Returns:
    str: The SHA-256 hash of the password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def register_member(username, password, role, full_name, email, phone, membership_category):
    """
    Registers a new member in the database.

    Parameters:
    username (str): The username chosen by the member.
    password (str): The password chosen by the member.
    role (str): The role assigned to the member.
    full_name (str): The full name of the member.
    email (str): The email address of the member.
    phone (str): The phone number of the member.
    membership_category (str): The membership category of the member.

    Returns:
    None
    """
    
    connection = create_connection()
    success = False
    
    cursor = connection.cursor()
    hashed_password = hash_password(password)
    query = """INSERT INTO users (username, password, role, full_name, email, phone, membership_category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    values = (username.lower(), hashed_password, role, full_name, email, phone, membership_category)

    try:
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", "Member registered successfully.")
        success = True
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"{err}")

    finally:
        cursor.close()
        connection.close()
    
    return success
            
def authenticate_user(username, password):
    """
    Authenticates a user.

    Parameters:
    username (str): The username.
    password (str): The password.

    Returns:
    dict or None: The user dictionary if authenticated, None otherwise.
    """
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    hashed_password = hash_password(password)
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username.lower(), hashed_password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

def get_user_id(username):
    """
    Returns the user ID of a user.

    Parameters:
    username (str): The username.

    Returns:
    int: The user ID.
    """
    connection = create_connection()
   
    cursor = connection.cursor()
    query = "SELECT user_id FROM users WHERE username = %s"
    cursor.execute(query, (username.lower(),))  
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    return None

def get_user_fine(user_id):
    """
    Returns the fine amount of a user.

    Parameters:
    user_id (int): The user ID.

    Returns:
    int: The fine amount.
    """
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT fines FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    return 0

def update_user_fine(user_id, fine_amount):
    """
    Updates the fine amount of a user.

    Parameters:
    user_id (int): The user ID.
    fine_amount (int): The new fine amount.

    Returns:
    None
    """
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET fines = %s WHERE user_id = %s"
    cursor.execute(query, (fine_amount, user_id))
    connection.commit()
    cursor.close()
    connection.close() 
