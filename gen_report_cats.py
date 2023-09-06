import os
import sqlite3
import json5


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
        with open(f'reports/{store}.json5', 'w') as file:
            json5.dump(data, file, indent=4)
    pass


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