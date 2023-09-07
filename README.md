# pos365-analysis

Analyze data from pos365.vn

## What is this?

pos365.vn is a Point-of-Sale (POS) provider in Vietnam. My friend has two restaurants and the built-in analysis tools
are lacking, so I'm writing this to help them out. This basically finds newly added CSV files, parses them, and enters
them into SQLite3 for further analysis which is done by other scripts.

## Techstack

**warning** I haven't used Python on a regular basis since f strings came out (python 3.6) so it's been about 6 years?
So this might not be the most pythonic code.

SQLite is in vogue now, and what's more in vogue is not using ORMs. I first started
using ORMs in 2015 with SQLAlchemy, and for this project I've decided to directly
use the `sqlite3` python lib to practice my SQL skills.

## Setup

You can have as many stores as you need, and the CSV files should be called `HangHoaBanRaChiTiet.csv` when you download it from pos365. Go to #!/SalesReport and select this setting, then download the data as CSV.

<img width="438" alt="image" src="https://github.com/JCharante/pos365-analysis/assets/13973198/41ba297d-417d-4b41-9426-619e1ee178e8">

You can call the files whatever, the script will ignore duplicate transactions (this assumes transactions have unique names, which seems to be the case)

Folder structure:

/data
  - /store1
    - CSV files
  - /store2
    - CSV files

## Usage

You'll need to install the python3 dependencies in requirements.txt

Goal: none of these scripts will delete your data in the /data folder. If you delete the database, 
you can re-initialize it and add the same stores again, and then run the load script again.

Use `python3 init.py` to initialize the SQLite3 database and data folder. (suggestion: install SQLite DB Browser to view the database)

Use `python3 add_store.py <storename>` to add a store to the database & data folder. This will create a folder in the data folder with the store name.

Use `python3 load.py` to check the data folder for new CSV files and load them into the database.

It takes about 5 seconds to load about 50,000 transactions into the database. There are
calls that could be optimized, but this is fast enough for our operations.

Use `python3 sum_product_sales.py` to generate the sum_product_sales table.
**This is semi-destructive.** It will drop the table and recreate it on every run.

This is useful for mapping product_ids to items and categories, because it calculates
the total sales for each product_id, so you can map the most important items first.

Use `python3 gen_report_time.py <start_hour> <end_hour> <minute_interval>` to generate reports in the /reports folder.

- Example invocation: `python3 gen_report_time.py 10 21 10`

- This will generate a report for each store.

- Reports are generated in the /reports folder with the name convention `sales-by-time-<storename>-interval-<minute_interval>.csv` and will overwrite existing files.

Use `python3 init_categories.py` to initialize the items and categories JSON5 file.

- There are multiple product_id's for the same item, so this JSON5 file
maps the item info to the product_id (which is unique to each store).

- Then in the categories JSON5 file, you can map items to a category.

- This uses JSON5 rather than JSON so that there can be comments in the file.

- There are example values in the generated files.

- This is a non-destructive command. If the files already exit they won't be overwritten. 

Use `python3 gen_report_cats.py` to generate reports for categories

- There are several reports generated, they are all in the /reports folder and overwrite a previous report.

- `category-<category_name>-sales-<store_name>-daily.csv` 
This includes the total sales by item in the category, grouped by date.

- `category-<category_name>-sales-<store_name>-weekly.csv` 
This includes the total sales by item in the category, grouped by week.

- `category-<category_name>-sales-<store_name>-biweekly.csv` 
This includes the total sales by item in the category, grouped bi-weekly.

- `category-<category_name>-sales-<store_name>-monthly.csv` 
This includes the total sales by item in the category, grouped by month.

- **Advice** Use the script `python3 remaining_items.py` to generate a list of product_ids that are already mapped, 
then use NOT IN to filter out those items when looking up the sum_product_sales table.

Use `python3 remaining_items.py` to generate a list of product_ids that are
mapped in the items.json5 file. It will print them out by store,
then you can run a query like

```sql
SELECT * 
FROM sum_product_sales 
WHERE product_id NOT IN ("HH-0001") 
AND store_name = "store1"
ORDER BY sales DESC;
```


## Pitfalls

- If a transaction has a percentage discount then the discount amount will not be stored in the DB.

# Case Study

## Opening Hours

Using the reports from `gen_report_time.py`, we were able to make a data-driven decision about
when to open the restaurant. We found that the restaurant was not profitable until 11AM, so
we moved the opening time from 10AM to 11AM. This was done by looking at lifetime sales between
10AM and 11AM and then calculating labor costs. We had a hunch that this might be the case,
but presenting this graph to the owner made it an instant decision.
