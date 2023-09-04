import sqlite3

import os


def database_exists(db_path):
    return os.path.isfile(db_path)


def initialize_database(db_path = "database.db"):
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect(db_path)

        # Create a new SQLite cursor
        cursor = conn.cursor()

        # Create a new table named 'stores'
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stores (
                        store_name TEXT PRIMARY KEY
                    )
                """)

        # Create a new table named 'parsed_files'
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS parsed_files (
                        store TEXT,
                        filename TEXT,
                        PRIMARY KEY(store, filename),
                        FOREIGN KEY(store) REFERENCES stores(store_name)
                    )
                """)

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()

        print(f"Database initialized successfully at {db_path}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Initialize the database at the specified path
    if not database_exists('database.db'):
        initialize_database('database.db')
    else:
        print("Database already exists")