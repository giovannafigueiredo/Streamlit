import pymysql
import sqlalchemy
# Database connection details
host = '192.168.0.107'
user = 'admin'
password = 'admin'
database = 'f1db'

try:
    # Establish a connection
    connection = pymysql.connect(
        host = host,
        user=user,
        password=password,
        database=database
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a sample query
    cursor.execute("SELECT VERSION()")

    # Fetch the result
    db_version = cursor.fetchone()

    print(f"Connected to MySQL Server. Server version: {db_version[0]}")

except pymysql.Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor:
        cursor.close()

    if 'connection' in locals() and connection:
        connection.close()
