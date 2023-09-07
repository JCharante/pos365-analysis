import json5
import sqlite3

if __name__ == "__main__":
    items = json5.load(open('items.json5'))

    try:
        # connect to database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if conn is None or cursor is None:
            exit(1)

        # get all stores
        cursor.execute("""
                SELECT store_name FROM stores
            """)

        stores = cursor.fetchall()
        stores = [store[0] for store in stores]
        ids_at_stores = {}
        for store in stores:
            ids_at_stores[store] = set()
            for item_name, item in items.items():
                direct_ids = item.get('direct', {}).get(store, [])
                featured_ids = item.get('featured_in', {}).get(store, [])
                # add all ids to set
                ids_at_stores[store].update(direct_ids)
                ids_at_stores[store].update(featured_ids)
        for store in stores:
            print(f"{store}: (\"" + "\", \"".join(ids_at_stores[store]) + "\")")
    except Exception as e:
        conn.close()
        raise e
