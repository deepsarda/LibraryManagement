import os
import mysql.connector
from mysql.connector import Error

#Load .env file manually to load env secerts
if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

# Check if secrets are loaded
if not os.environ.get('DB_HOST') or not os.environ.get('DB_USER') or not os.environ.get('DB_PASSWORD'):
    raise Exception("Missing environment variables. Please add .env file with DB_HOST, DB_USER, and DB_PASSWORD. Example: DB_HOST=127.0.0.1\nDB_USER=root\nDB_PASSWORD=password")

def create_connection():
    """
    Creates a connection to the MySQL database using environment variables.

    The connection is configured to the 'library_management' database if no
    'DB_NAME' environment variable is set.

    Returns the connection object if successful, otherwise None.
    """
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME') or 'library_management',
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
