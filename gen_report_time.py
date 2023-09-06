import os
import sqlite3
from datetime import datetime
import sys

def get_store_sales(cursor, store_name):
    cursor.execute("""
        SELECT transaction_time, transaction_total
        FROM raw_sales
        WHERE store = ?
        GROUP BY transaction_id
    """, (store_name,))

    return cursor.fetchall()


# given a start hour, end hour, and interval, return a list of timeslots
# example: start hour = 10, end hour = 11, interval = 10
# returns: { '10:00': 0, '10:10': 0, '10:20': 0, '10:30': 0, '10:40': 0, '10:50': 0 }
# author: chatgpt4
def timeslot_factory(start_hour, end_hour, interval):
    timeslots = {}
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, interval):
            timeslot = f"{hour:02d}:{minute:02d}"
            timeslots[timeslot] = 0
    return timeslots


# given a list of timeslots (e.g. ['10:00', '10:10', '10:20', '10:30', '10:40', '10:50'])
# this reads the transaction_time and returns the timeslot that the transaction_time falls into
# not the most efficient way, but this took 1 minute to prompt chatgpt to write
# and test that it works. so it's good enough until it becomes a bottleneck.
def find_timeslot(transaction_time, timeslots, interval):
    transaction_dt = datetime.strptime(transaction_time, '%H:%M')
    transaction_minutes = transaction_dt.hour * 60 + transaction_dt.minute

    for timeslot in timeslots:
        timeslot_dt = datetime.strptime(timeslot, '%H:%M')
        timeslot_start_minutes = timeslot_dt.hour * 60 + timeslot_dt.minute
        if timeslot_start_minutes + interval > transaction_minutes >= timeslot_start_minutes:
            return timeslot
    return None


def generate_report(cursor, store_name, start_hour, end_hour, interval):
    all_sales = get_store_sales(cursor, store_name)
    timeslot_dict = timeslot_factory(start_hour, end_hour, interval)
    timeslots = list(timeslot_dict.keys())
    for transaction in all_sales:
        transaction_time = transaction[0]
        transaction_total = transaction[1]
        timeslot = find_timeslot(transaction_time, timeslots, interval)
        if timeslot is None:
            print(f"Error: timeslot is None for transaction_time {transaction_time}")
            print("Error resolution: transaction will not be included in the report.")
            continue
            # raise Exception("Error: timeslot is None for transaction_time {transaction_time}")
        timeslot_dict[timeslot] += transaction_total
    # write report to csv
    with open(f"reports/sales-by-time-{store_name}-interval-{interval}.csv", 'w') as f:
        f.write("timeslot,total_sales\n")
        for timeslot in timeslots:
            f.write(f"{timeslot},{timeslot_dict[timeslot]}\n")
    # print success message
    print(f"Report generated for {store_name}.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 gen_report_time.py <start_hour> <end_hour> <interval>")
        sys.exit(1)
    start_hour = int(sys.argv[1])
    end_hour = int(sys.argv[2])
    interval = int(sys.argv[3])

    # create reports folder if not exist
    if not os.path.exists('reports'):
        os.mkdir('reports')

    # connect to database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if conn is None or cursor is None:
        exit(1)

    try:
        # get all stores
        cursor.execute("""
            SELECT store_name FROM stores
        """)

        stores = cursor.fetchall()

        # generate report for each store
        for store in stores:
            generate_report(cursor, store[0])

        # close connection
        conn.close()
    except Exception as e:
        conn.close()
        print(f"An error occurred: {e}")
        exit(1)