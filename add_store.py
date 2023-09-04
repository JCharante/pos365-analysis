import sqlite3
import os
import sys


# Function to add a new store to the database and create a folder in the data folder
def add_store(db_path, store_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO stores (store_name) VALUES (?)", (store_name,))
        conn.commit()
        conn.close()

        os.makedirs(f"data/{store_name}", exist_ok=True)
        print(f"Store '{store_name}' added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 add_store.py <storename>")
        sys.exit(1)

    db_path = 'database.db'
    store_name = sys.argv[1]

    add_store(db_path, store_name)
