import sqlite3
import os


# Function to connect to the database and return the connection and cursor
def connect_to_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None, None


# Function to get the list of parsed files from the database
def get_parsed_files(cursor):
    try:
        cursor.execute("SELECT store, filename FROM parsed_files")
        return set(cursor.fetchall())
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return set()


# Function to get the list of all CSV files in the data folder
def get_all_csv_files(data_folder):
    csv_files = []
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith('.csv'):
                store = os.path.relpath(root, data_folder)
                csv_files.append((store, file))
    return set(csv_files)


if __name__ == '__main__':
    db_path = 'database.db'
    data_folder = 'data'

    conn, cursor = connect_to_database(db_path)
    if conn is None or cursor is None:
        exit(1)

    parsed_files = get_parsed_files(cursor)
    all_csv_files = get_all_csv_files(data_folder)

    unread_files = all_csv_files - parsed_files

    for store, filename in unread_files:
        print(f"Unread file: {store}/{filename}")



    conn.close()
