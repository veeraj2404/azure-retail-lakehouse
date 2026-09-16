IF OBJECT_ID('dbo.fact_sales','U') IS NOT NULL DROP TABLE dbo.fact_sales;
IF OBJECT_ID('dbo.dim_date','U') IS NOT NULL DROP TABLE dbo.dim_date;
IF OBJECT_ID('dbo.dim_customer','U') IS NOT NULL DROP TABLE dbo.dim_customer;
IF OBJECT_ID('dbo.dim_product','U') IS NOT NULL DROP TABLE dbo.dim_product;
IF OBJECT_ID('dbo.dim_store','U') IS NOT NULL DROP TABLE dbo.dim_store;

CREATE TABLE dbo.dim_customer(
 customer_id varchar(50) NOT NULL PRIMARY KEY,
 customer_name varchar(150), email varchar(200), city varchar(100), state varchar(100), created_date date
);
CREATE TABLE dbo.dim_product(
 product_id varchar(50) NOT NULL PRIMARY KEY,
 product_name varchar(150), category varchar(100), unit_price decimal(18,2)
);
CREATE TABLE dbo.dim_store(
 store_id varchar(50) NOT NULL PRIMARY KEY,
 store_name varchar(150), city varchar(100), state varchar(100), region varchar(100)
);
CREATE TABLE dbo.dim_date(
 date_key int NOT NULL PRIMARY KEY, full_date date NOT NULL,
 day_of_month int, month_number int, month_name varchar(20), quarter_number int, year_number int
);
CREATE TABLE dbo.fact_sales(
 order_id varchar(50) NOT NULL PRIMARY KEY,
 date_key int NOT NULL, customer_id varchar(50) NOT NULL, product_id varchar(50) NOT NULL, store_id varchar(50) NOT NULL,
 quantity int NOT NULL, unit_price decimal(18,2) NOT NULL, discount_pct decimal(9,4) NOT NULL,
 gross_amount decimal(18,2) NOT NULL, net_amount decimal(18,2) NOT NULL, last_modified_ts datetime2,
 CONSTRAINT FK_fact_date FOREIGN KEY(date_key) REFERENCES dbo.dim_date(date_key),
 CONSTRAINT FK_fact_customer FOREIGN KEY(customer_id) REFERENCES dbo.dim_customer(customer_id),
 CONSTRAINT FK_fact_product FOREIGN KEY(product_id) REFERENCES dbo.dim_product(product_id),
 CONSTRAINT FK_fact_store FOREIGN KEY(store_id) REFERENCES dbo.dim_store(store_id)
);
