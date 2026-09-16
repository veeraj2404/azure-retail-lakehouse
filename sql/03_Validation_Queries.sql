SELECT COUNT(*) AS fact_sales_rows FROM dbo.fact_sales;
SELECT COUNT(*) AS dim_customer_rows FROM dbo.dim_customer;
SELECT COUNT(*) AS dim_product_rows FROM dbo.dim_product;
SELECT COUNT(*) AS dim_store_rows FROM dbo.dim_store;
SELECT COUNT(*) AS dim_date_rows FROM dbo.dim_date;

SELECT order_id, COUNT(*) cnt FROM dbo.fact_sales GROUP BY order_id HAVING COUNT(*) > 1;

SELECT COUNT(*) AS missing_customers
FROM dbo.fact_sales f LEFT JOIN dbo.dim_customer d ON f.customer_id=d.customer_id
WHERE d.customer_id IS NULL;
