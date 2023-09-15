import os
import sqlite3
import json5
from datetime import datetime
import csv


def sort_dates(date_list):
    return sorted(date_list, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))


def date_to_week(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    return date_obj.strftime('%Y-%U')


def date_to_biweek(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    week_number = int(date_obj.strftime('%U'))
    biweek_number = week_number // 2
    year = date_obj.strftime('%Y')
    return f"{year}-{biweek_number:02d}"


def date_to_month(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    return date_obj.strftime('%Y-%m')


# author: ChatGPT4
def json5_to_csv(json5_data, store_name, include_qty):
    sorted_keys = sort_dates(json5_data.keys())

    # Identify unique categories
    unique_categories = set()
    for date in json5_data:
        unique_categories.update(json5_data[date].keys())

    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Daily
    for category in unique_categories:
        # Identify unique items in this category
        unique_items = set()
        for date in json5_data:
            unique_items.update(json5_data[date].get(category, {}).keys())
        unique_items = list(unique_items)

        # Preparing the CSV headers
        headers = ["Date"]
        for item in unique_items:
            if include_qty:
                headers.append(f"{item} QTY")
            headers.append(f"{item} Revenue")

        # Writing to CSV
        with open(f'reports/category-{category}-sales-{store_name}-daily.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            for date in sorted_keys:
                row = [date]
                for item in unique_items:
                    item_data = json5_data.get(date, {}).get(category, {}).get(item, {})
                    if include_qty:
                        row.append(item_data.get('qty_sold_daily', 0))
                    row.append(item_data.get('product_revenue_daily', 0))
                writer.writerow(row)

    # Weekly
    for category in unique_categories:
        # Identify unique items in this category
        unique_items = set()
        for date in json5_data:
            unique_items.update(json5_data[date].get(category, {}).keys())
        unique_items = list(unique_items)

        # Preparing the CSV headers
        headers = ["Week"]
        for item in unique_items:
            if include_qty:
                headers.append(f"{item} QTY")
            headers.append(f"{item} Revenue")

        # Aggregate data by weeks
        weekly_data = {}
        for date in sorted_keys:
            week_number = date_to_week(date)
            if week_number not in weekly_data:
                weekly_data[week_number] = {item: {'qty_sold_daily': 0, 'product_revenue_daily': 0} for item in
                                            unique_items}

            for item in unique_items:
                item_data = json5_data[date].get(category, {}).get(item, {})
                weekly_data[week_number][item]['qty_sold_daily'] += item_data.get('qty_sold_daily', 0)
                weekly_data[week_number][item]['product_revenue_daily'] += item_data.get('product_revenue_daily', 0)

        # Writing to CSV
        with open(f'reports/category-{category}-sales-{store_name}-weekly.csv', 'w', newline='',
                  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            for week_number in sorted(weekly_data.keys()):
                row = [week_number]
                for item in unique_items:
                    if include_qty:
                        row.append(weekly_data[week_number][item]['qty_sold_daily'])
                    row.append(weekly_data[week_number][item]['product_revenue_daily'])
                writer.writerow(row)

    # bi-weekly
    for category in unique_categories:
        # Identify unique items in this category
        unique_items = set()
        for date in json5_data:
            unique_items.update(json5_data[date].get(category, {}).keys())
        unique_items = list(unique_items)

        # Preparing the CSV headers
        headers = ["Bi-Week"]
        for item in unique_items:
            if include_qty:
                headers.append(f"{item} QTY")
            headers.append(f"{item} Revenue")

        # Aggregate data by bi-weeks
        biweekly_data = {}
        for date in sorted_keys:
            biweek_number = date_to_biweek(date)
            if biweek_number not in biweekly_data:
                biweekly_data[biweek_number] = {item: {'qty_sold_daily': 0, 'product_revenue_daily': 0} for item in
                                                unique_items}

            for item in unique_items:
                item_data = json5_data[date].get(category, {}).get(item, {})
                biweekly_data[biweek_number][item]['qty_sold_daily'] += item_data.get('qty_sold_daily', 0)
                biweekly_data[biweek_number][item]['product_revenue_daily'] += item_data.get('product_revenue_daily', 0)

        # Writing to CSV
        with open(f'reports/category-{category}-sales-{store_name}-biweekly.csv', 'w', newline='',
                  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            for biweek_number in sorted(biweekly_data.keys()):
                row = [biweek_number]
                for item in unique_items:
                    if include_qty:
                        row.append(biweekly_data[biweek_number][item]['qty_sold_daily'])
                    row.append(biweekly_data[biweek_number][item]['product_revenue_daily'])
                writer.writerow(row)

    # Monthly reports
    for category in unique_categories:
        # Identify unique items in this category
        unique_items = set()
        for date in json5_data:
            unique_items.update(json5_data[date].get(category, {}).keys())
        unique_items = list(unique_items)

        # Preparing the CSV headers
        headers = ["Month"]
        for item in unique_items:
            if include_qty:
                headers.append(f"{item} QTY")
            headers.append(f"{item} Revenue")

        # Aggregate data by months
        monthly_data = {}
        for date in sorted_keys:
            month = date_to_month(date)
            if month not in monthly_data:
                monthly_data[month] = {item: {'qty_sold_daily': 0, 'product_revenue_daily': 0} for item in unique_items}

            for item in unique_items:
                item_data = json5_data[date].get(category, {}).get(item, {})
                monthly_data[month][item]['qty_sold_daily'] += item_data.get('qty_sold_daily', 0)
                monthly_data[month][item]['product_revenue_daily'] += item_data.get('product_revenue_daily', 0)

        # Writing to CSV
        with open(f'reports/category-{category}-sales-{store_name}-monthly.csv', 'w', newline='',
                  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            for month in sorted(monthly_data.keys()):
                row = [month]
                for item in unique_items:
                    if include_qty:
                        row.append(monthly_data[month][item]['qty_sold_daily'])
                    row.append(monthly_data[month][item]['product_revenue_daily'])
                writer.writerow(row)


def DDMMYYYY_to_YYYYMMDD(date_string):
    chunks = date_string.split('/')
    return f"{chunks[2]}-{chunks[1]}-{chunks[0]}"


# input in format of YYYY-MM-DD
def get_day_of_week(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%A')


def data_to_db(json5_data, store, cursor: sqlite3.Cursor, conn):
    sorted_keys = sort_dates(json5_data.keys())

    # Identify unique categories
    unique_categories = set()
    for date in json5_data:
        unique_categories.update(json5_data[date].keys())
    print(unique_categories)

    # delete previous answers
    cursor.execute("""
                DELETE FROM item_cat_sales WHERE store = ?
            """, [store])

    for category in unique_categories:
        # Identify unique items in this category
        unique_items = set()
        for date in json5_data:
            unique_items.update(json5_data[date].get(category, {}).keys())
        unique_items = list(unique_items)

        daily_info = []
        weekly_data = {}
        biweekly_data = {}
        monthly_data = {}

        for date in sorted_keys:
            week_number = date_to_week(date)
            if week_number not in weekly_data:
                weekly_data[week_number] = {item: {'qty_sold_daily': 0, 'product_revenue_daily': 0} for item in
                                            unique_items}

            biweek_number = date_to_biweek(date)
            if biweek_number not in biweekly_data:
                biweekly_data[biweek_number] = {item: {'qty_sold_daily': 0, 'product_revenue_daily': 0} for item in
                                                unique_items}

            month = date_to_month(date)
            if month not in monthly_data:
                monthly_data[month] = {item: {'qty_sold_daily': 0, 'product_revenue_daily': 0} for item in
                                       unique_items}

            for item in unique_items:
                item_data = json5_data.get(date, {}).get(category, {}).get(item, {})
                formatted_date = DDMMYYYY_to_YYYYMMDD(date)
                daily_info.append(
                    (store,
                     category,
                     formatted_date,
                     get_day_of_week(formatted_date),
                     "daily",
                     item_data.get('qty_sold_daily', 0),
                     item_data.get('product_revenue_daily', 0),
                     item)
                )
                weekly_data[week_number][item]['qty_sold_daily'] += item_data.get('qty_sold_daily', 0)
                weekly_data[week_number][item]['product_revenue_daily'] += item_data.get('product_revenue_daily', 0)
                biweekly_data[biweek_number][item]['qty_sold_daily'] += item_data.get('qty_sold_daily', 0)
                biweekly_data[biweek_number][item]['product_revenue_daily'] += item_data.get('product_revenue_daily', 0)
                monthly_data[month][item]['qty_sold_daily'] += item_data.get('qty_sold_daily', 0)
                monthly_data[month][item]['product_revenue_daily'] += item_data.get('product_revenue_daily', 0)


        statement = """
                    INSERT INTO item_cat_sales(
                        store, category, time_bucket, time_bucket_extra, type,
                        qty_product_sold, revenue, item
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
        conn.commit()
        cursor.executemany(statement, daily_info)
        # weekly_tuples = []
        # for week_number, items in weekly_data.items():
        #     for item_name, item in items.items():
        #         weekly_tuples.append((
        #             store, category, week_number, "weekly", item.get('qty_sold_daily', 0.0),
        #             item.get('product_revenue_daily', 0.0), item_name
        #         ))
        for time_bucket_type, time_bucket_data in [
            ("weekly", weekly_data),
            ("biweekly", biweekly_data),
            ("monthly", monthly_data),
        ]:
            tuples = []
            for time_bucket, items in time_bucket_data.items():
                for item_name, item in items.items():
                    tuples.append((
                        store, category, time_bucket, None, time_bucket_type, item.get('qty_sold_daily', 0.0),
                        item.get('product_revenue_daily', 0.0), item_name
                    ))
            cursor.executemany(statement, tuples)
        conn.commit()

    
def generate_report(cursor, stores, items, categories):
    # get all sales for store
    item_names = list(items.keys())
    category_names = list(categories.keys())
    for store in stores:
        data = {}  # {date: { category: { item_name: {qty_sold_daily, product_revenue_daily}}}
        for category_name in category_names:
            item_names_in_cat = categories[category_name]
            for item_name in item_names_in_cat:
                direct_ids = items[item_name].get('direct', {}).get(store, [])
                featured_in_ids = items[item_name].get('featured_in', {}).get(store, [])

                placeholders = ', '.join('?' for _ in direct_ids)
                cursor.execute(f"""
                SELECT transaction_date, SUM(qty_product_sold) as qty_sold_daily, SUM(product_prices) as product_revenue_daily
                FROM raw_sales
                WHERE product_id IN ({placeholders}) AND store = ?
                GROUP BY transaction_date
                """, direct_ids + [store])
                direct_sales = cursor.fetchall()

                placeholders = ', '.join('?' for _ in direct_ids)
                cursor.execute(f"""
                SELECT AVG(product_price) FROM raw_sales
                WHERE product_id IN ({placeholders}) AND store = ?
                """, direct_ids + [store])
                direct_avg_price = cursor.fetchone()[0]

                if direct_avg_price is None:
                    placeholders = ', '.join('?' for _ in featured_in_ids)
                    cursor.execute(f"""
                                    SELECT AVG(product_price) FROM raw_sales
                                    WHERE product_id IN ({placeholders}) AND store = ?
                                    """, featured_in_ids + [store])
                    direct_avg_price = cursor.fetchone()[0]
                    if direct_avg_price is None:
                        print(f"Error: {item_name} has no price in {store}. Skipping item.")
                        continue

                # we fetch the avg price to estimate the contribution of revenue
                # from indirect sales (combos)
                placeholders = ', '.join('?' for _ in featured_in_ids)
                cursor.execute(f"""
                                SELECT transaction_date, SUM(qty_product_sold) as qty_sold_daily
                                FROM raw_sales
                                WHERE product_id IN ({placeholders}) AND store = ?
                                GROUP BY transaction_date
                """, featured_in_ids + [store])

                featured_in_sales = cursor.fetchall()
                for transaction_date, qty_sold_daily, product_revenue_daily in direct_sales:
                    if transaction_date not in data:
                        data[transaction_date] = {}
                    if category_name not in data[transaction_date]:
                        data[transaction_date][category_name] = {}
                    data[transaction_date][category_name][item_name] = {
                        'qty_sold_daily': qty_sold_daily,
                        'product_revenue_daily': product_revenue_daily
                    }
                for transaction_date, qty_sold_daily in featured_in_sales:
                    if transaction_date not in data:
                        data[transaction_date] = {}
                    if category_name not in data[transaction_date]:
                        data[transaction_date][category_name] = {}
                    if item_name not in data[transaction_date][category_name]:
                        data[transaction_date][category_name][item_name] = {
                            'qty_sold_daily': 0,
                            'product_revenue_daily': 0
                        }
                    data[transaction_date][category_name][item_name]['qty_sold_daily'] += qty_sold_daily
                    data[transaction_date][category_name][item_name]['product_revenue_daily'] += qty_sold_daily * direct_avg_price
        # print(data)
        json5_to_csv(data, store, False)
        data_to_db(data, store, cursor, conn)
        # with open(f'reports/{store}.json5', 'w') as file:
        #     json5.dump(data, file, indent=4)
    pass


def delete_item_cat_sales(cursor: sqlite3.Cursor):
    cursor.execute("""
        DELETE FROM item_cat_sales;
    """)


if __name__ == "__main__":
    # create reports folder if not exist
    if not os.path.exists('reports'):
        os.mkdir('reports')

    # connect to database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if conn is None or cursor is None:
        exit(1)

    # read json5 config fies
    items = json5.load(open('items.json5'))
    categories = json5.load(open('categories.json5'))

    # delete item_cat_sales table
    delete_item_cat_sales(cursor)

    try:
        # get all stores
        cursor.execute("""
            SELECT store_name FROM stores
        """)

        stores = cursor.fetchall()
        stores = [store[0] for store in stores]

        # generate report for each store
        generate_report(cursor, stores, items, categories)

        # close connection
        conn.close()
    except Exception as e:
        conn.close()
        print(f"An error occurred: {e}")
        raise e