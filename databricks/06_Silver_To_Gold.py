# Databricks notebook source
# MAGIC %run ./00_Config
from pyspark.sql.functions import (
    col, min as spark_min, max as spark_max, sequence, explode,
    date_format, dayofmonth, month, quarter, year
)

orders=spark.read.format("delta").load(PATHS["silver_orders"])
customers=spark.read.format("delta").load(PATHS["silver_customers"])
products=spark.read.format("delta").load(PATHS["silver_products"])
stores=spark.read.format("delta").load(PATHS["silver_stores"])

dim_customer=customers.select("customer_id","customer_name","email","city","state","created_date").dropDuplicates(["customer_id"])
dim_product=products.select("product_id","product_name","category","unit_price").dropDuplicates(["product_id"])
dim_store=stores.select("store_id","store_name","city","state","region").dropDuplicates(["store_id"])

bounds=orders.agg(spark_min("order_date").alias("min_date"),spark_max("order_date").alias("max_date")).first()
date_df=(spark.createDataFrame([(bounds["min_date"],bounds["max_date"])],["min_date","max_date"])
         .select(explode(sequence(col("min_date"),col("max_date"))).alias("full_date")))
dim_date=(date_df.withColumn("date_key",date_format("full_date","yyyyMMdd").cast("int"))
         .withColumn("day_of_month",dayofmonth("full_date"))
         .withColumn("month_number",month("full_date"))
         .withColumn("month_name",date_format("full_date","MMMM"))
         .withColumn("quarter_number",quarter("full_date"))
         .withColumn("year_number",year("full_date"))
         .select("date_key","full_date","day_of_month","month_number","month_name","quarter_number","year_number"))

fact_sales=(orders.withColumn("date_key",date_format("order_date","yyyyMMdd").cast("int"))
            .select("order_id","date_key","customer_id","product_id","store_id","quantity",
                    "unit_price","discount_pct","gross_amount","net_amount","last_modified_ts"))

for df,path in [
    (dim_customer,PATHS["gold_dim_customer"]),(dim_product,PATHS["gold_dim_product"]),
    (dim_store,PATHS["gold_dim_store"]),(dim_date,PATHS["gold_dim_date"]),
    (fact_sales,PATHS["gold_fact_sales"])
]:
    df.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(path)

print("Gold star schema created.")
