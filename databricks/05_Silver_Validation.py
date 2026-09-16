# Databricks notebook source
# MAGIC %run ./00_Config
from pyspark.sql.functions import col

orders=spark.read.format("delta").load(PATHS["silver_orders"])
customers=spark.read.format("delta").load(PATHS["silver_customers"])
products=spark.read.format("delta").load(PATHS["silver_products"])
stores=spark.read.format("delta").load(PATHS["silver_stores"])

def duplicate_count(df,key):
    return df.groupBy(key).count().filter(col("count")>1).count()

assert duplicate_count(orders,"order_id")==0, "Duplicate order_id found"
assert duplicate_count(customers,"customer_id")==0, "Duplicate customer_id found"
assert duplicate_count(products,"product_id")==0, "Duplicate product_id found"
assert duplicate_count(stores,"store_id")==0, "Duplicate store_id found"

missing_customer=orders.join(customers,"customer_id","left_anti").count()
missing_product=orders.join(products,"product_id","left_anti").count()
missing_store=orders.join(stores,"store_id","left_anti").count()

print("Silver counts:", orders.count(), customers.count(), products.count(), stores.count())
print("Unmatched FK counts:", missing_customer, missing_product, missing_store)
assert missing_customer==0 and missing_product==0 and missing_store==0, "Silver referential integrity failed"
print("Silver validation passed.")
