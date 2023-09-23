SELECT (substr(transaction_date, 7, 4) || '-' || substr(transaction_date, 4, 2) || '-' || substr(transaction_date, 1, 2)) as yyyymmdd,
       * FROM raw_sales
ORDER BY yyyymmdd ASC, transaction_time ASC
LIMIT 1;