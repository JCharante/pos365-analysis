import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
                DROP TABLE IF EXISTS sum_product_sales;
    """)
    cursor.execute("""
                CREATE TABLE sum_product_sales (
                    store TEXT,
                    product_id TEXT,
                    product_name TEXT,
                    qty_product_sold REAL,
                    sales INTEGER
                )
    """)
    data = cursor.execute("""
                SELECT store, product_id, product_name, SUM(qty_product_sold) AS qty_product_sold, SUM(product_prices) AS sales
                FROM raw_sales
                GROUP BY store, product_id;

    """)
    data_for_entry = []
    for datum in data.fetchall():
        data_for_entry.append(datum)

    insert_query = """
        INSERT INTO sum_product_sales (
            store, product_id, product_name, qty_product_sold, sales
        ) VALUES (?, ?, ?, ?, ?)
    """

    cursor.executemany(insert_query, data_for_entry)
    conn.commit()
    print("Added sum_product_sales to database.")
    conn.close()
