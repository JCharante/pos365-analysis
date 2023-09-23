--On launch day, it appears the restaurant entered prices in implied units of 1,000 VND
--and later that day, they realized their mistake.
--so they updated their prices from (for example) 89 to 89000
--so this script just fixes that manually
UPDATE raw_sales
SET product_price = product_price * 1000,
    product_prices = product_prices * 1000,
    transaction_total = transaction_total * 1000
WHERE transaction_date = '20/04/2021' AND store = 'hanoi' AND product_price < 1000 AND product_price > 0
