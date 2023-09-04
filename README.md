# pos365-analysis

Analyze data from pos365.vn

You can have as many stores as you need, and the CSV files should be called `HangHoaBanRaChiTiet.csv` when you download it from pos365. Go to #!/SalesReport and select this setting, then download the data as CSV.

<img width="438" alt="image" src="https://github.com/JCharante/pos365-analysis/assets/13973198/41ba297d-417d-4b41-9426-619e1ee178e8">

You can call the files whatever, the script will ignore duplicate transactions (this assumes transactions have unique names, which seems to be the case)

Folder structure:

/data
  - /store1
    - CSV files
  - /store2
    - CSV files
