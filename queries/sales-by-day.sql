SELECT (substr(transaction_date, 7, 4) || '-' || substr(transaction_date, 4, 2) || '-' || substr(transaction_date, 1, 2)) as yyyymmdd,
       SUM(transaction_total)
FROM (
    -- authors note: I didn't know SQL had sub-queries!
    SELECT transaction_id, transaction_total, transaction_date
                                    FROM raw_sales
                                    WHERE store = "hanoi"
                                    GROUP BY transaction_date, transaction_id
    ) GROUP BY transaction_date
ORDER BY yyyymmdd ASC