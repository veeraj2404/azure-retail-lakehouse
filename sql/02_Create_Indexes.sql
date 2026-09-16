CREATE INDEX IX_fact_sales_date ON dbo.fact_sales(date_key);
CREATE INDEX IX_fact_sales_customer ON dbo.fact_sales(customer_id);
CREATE INDEX IX_fact_sales_product ON dbo.fact_sales(product_id);
CREATE INDEX IX_fact_sales_store ON dbo.fact_sales(store_id);
