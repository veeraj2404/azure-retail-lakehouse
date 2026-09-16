# Databricks notebook source
# MAGIC %run ./00_Config
from pyspark.sql.functions import col

fact=spark.read.format("delta").load(PATHS["gold_fact_sales"])
dc=spark.read.format("delta").load(PATHS["gold_dim_customer"])
dp=spark.read.format("delta").load(PATHS["gold_dim_product"])
ds=spark.read.format("delta").load(PATHS["gold_dim_store"])
dd=spark.read.format("delta").load(PATHS["gold_dim_date"])

assert fact.groupBy("order_id").count().filter(col("count")>1).count()==0
assert fact.join(dc,"customer_id","left_anti").count()==0
assert fact.join(dp,"product_id","left_anti").count()==0
assert fact.join(ds,"store_id","left_anti").count()==0
assert fact.join(dd,"date_key","left_anti").count()==0

print("Gold counts:", fact.count(), dc.count(), dp.count(), ds.count(), dd.count())
print("Gold validation passed.")
