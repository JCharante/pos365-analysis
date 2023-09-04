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

Use `python3 init.py` to initialize the SQLite3 database and data folder. (suggestion: install SQLite DB Browser to view the database)

Use `python3 add_store.py <storename>` to add a store to the database & data folder. This will create a folder in the data folder with the store name.

Use `python3 load.py` to check the data folder for new CSV files and load them into the database.

## Pitfalls

- If a transaction has a percentage discount then the discount amount will not be stored in the DB.
