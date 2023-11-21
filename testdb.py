import streamlit as st
import pandas as pd
import pymysql

# Function to connect to MySQL database and retrieve tables
def fetch_data(host, user, password, database, table_name):
    try:
        # Connect to the MySQL database
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Get a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Example: Get list of tables
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        table_exists = cursor.fetchone()

        if not table_exists:
            st.error(f"Table '{table_name}' not found in the database.")
            return None

        # Fetch columns for the specified table
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [column[0] for column in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return pd.DataFrame(columns, columns=["Columns"])

    except Exception as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

# Streamlit app
def main():
    st.title("Streamlit MySQL App")

    # Database connection details
    host = st.text_input("Enter MySQL Host:", "localhost")
    user = st.text_input("Enter MySQL User:", "your_username")
    password = st.text_input("Enter MySQL Password:", "", type="password")
    database = st.text_input("Enter MySQL Database:", "your_database")
    table_name = st.text_input("Enter Table Name:", "your_table")

    # Button to fetch columns for a table
    if st.button("Fetch Columns"):
        # Fetch columns from MySQL database
        columns_df = fetch_data(host, user, password, database, table_name)

        # Display columns as a DataFrame
        if columns_df is not None:
            st.success(f"Columns for table '{table_name}' fetched successfully!")
            st.write("Columns in the table:")
            st.write(columns_df)

# Run the Streamlit app
if __name__ == "__main__":
    main()