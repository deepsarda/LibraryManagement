from db_config import create_connection
import mysql.connector

def add_book(title, author, isbn, publisher, edition, genre, language, publication_year, dewey_decimal, subject_tags, total_copies):
    """
    Add a book to the catalog.

    Parameters:
    title (str): Book title
    author (str): Book author
    isbn (str): Book ISBN
    publisher (str): Book publisher
    edition (str): Book edition
    genre (str): Book genre
    language (str): Book language
    publication_year (int): Book publication year
    dewey_decimal (str): Book Dewey Decimal classification
    subject_tags (str): Book subject tags
    total_copies (int): Total number of copies of the book

    Returns:
    None
    """
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO books 
                   (title, author, isbn, publisher, edition, genre, language, publication_year, dewey_decimal, subject_tags, total_copies, available_copies)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (title, author, isbn, publisher, edition, genre, language, publication_year, dewey_decimal, subject_tags, total_copies, total_copies)
        try:
            cursor.execute(query, values)
            connection.commit()
            print("Book added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

def search_books(keyword):
    """
    Search for books in the catalog by keyword.

    Parameters:
    keyword (str): Keyword to search for

    Returns:
    list: List of dictionaries containing the book details, or an empty list if there are no results
    """
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """SELECT * FROM books WHERE 
                   title LIKE %s OR 
                   author LIKE %s OR 
                   isbn LIKE %s OR 
                   genre LIKE %s OR 
                   language LIKE %s OR 
                   publication_year LIKE %s"""
        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword, like_keyword, like_keyword, like_keyword, like_keyword))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    return []


def get_book_by_id(book_id):
    """
    Get a book from the catalog by its ID.

    Parameters:
    book_id (int): ID of the book

    Returns:
    dict: Dictionary containing the book details, or None if the book is not found
    """
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM books WHERE book_id = %s"
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    return None