# Power BI Semantic Model

Source: Azure SQL serving database.

Relationships:
- dim_customer[customer_id] 1 -> * fact_sales[customer_id]
- dim_product[product_id] 1 -> * fact_sales[product_id]
- dim_store[store_id] 1 -> * fact_sales[store_id]
- dim_date[date_key] 1 -> * fact_sales[date_key]

Use single-direction filters from dimensions to fact. Mark `dim_date[full_date]` as the date table date column.
