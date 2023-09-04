import sqlite3
import os
import csv


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


def entry_exists(cursor, store_name, transaction_id):
    try:
        cursor.execute("""
            SELECT EXISTS(
                SELECT 1 
                FROM raw_sales 
                WHERE store = ? AND transaction_id = ?
            )
        """, (store_name, transaction_id))

        # fetchone() retrieves the first record from the query result (which will be a single record here)
        result = cursor.fetchone()

        if result[0]:
            return True
        else:
            return False

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def parse_csv_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            rows = [row for row in csv_reader]
            # format check
            if len(rows[0]) != 42:
                raise Exception(f"Invalid file format: {file_path}")
            indexes = {
                'product_id': 30,
                'product_name': 36,
                'qty_product_sold': 28,
                'product_price': 38,
                'product_prices': 40,
                'transaction_id': 33,
                'transaction_datetime': 37,
                'discount_amount': 39,  # this may be a number or a percentage like 29%
                'transaction_total': 40
            }
            # dev: this statement helps decode the format of the csv file
            # print('\n'.join([f"{i}: {val}" for i, val in enumerate(rows[1])]))
            # commentary: I've missed good ol' list comprehension
            entries = [
            {
                idx_name: row[idx_val]
                for idx_name, idx_val in indexes.items()
            }
            for row in rows[1:]]
            # Now we bucket them by transaction_id
            transactions = {}
            for entry in entries:
                if entry['transaction_id'] not in transactions:
                    transactions[entry['transaction_id']] = []
                transactions[entry['transaction_id']].append(entry)
            return transactions
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def add_transaction_to_db(cursor, transaction_id, entries, store):
    print(f"Adding {transaction_id} to database...")
    pass


if __name__ == '__main__':
    db_path = 'database.db'
    data_folder = 'data'

    conn, cursor = connect_to_database(db_path)
    if conn is None or cursor is None:
        exit(1)

    try:
        parsed_files = get_parsed_files(cursor)
        all_csv_files = get_all_csv_files(data_folder)

        unread_files = all_csv_files - parsed_files

        for store, filename in unread_files:
            print(f"Unread file: {store}/{filename}")

        for store, filename in unread_files:
            transactions = parse_csv_file(f"{data_folder}/{store}/{filename}")
            for transaction_id, entries in transactions.items():
                if entry_exists(cursor, store, transaction_id):
                    print(f"Entry for transaction {transaction_id} already exists. Skipping...")
                    continue
                else:
                    add_transaction_to_db(cursor, transaction_id, entries, store)

        conn.close()
    except Exception as e:
        conn.close()
        print("Exception occurred. Connection to database closed.")
