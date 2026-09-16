# Databricks notebook source
# MAGIC %run ./00_Config

from pyspark.sql.functions import (
    col, trim, to_date, to_timestamp, when, lit, concat_ws,
    current_timestamp, round as spark_round, row_number
)
from pyspark.sql.window import Window
from delta.tables import DeltaTable

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(PATHS["bronze_orders"])
)

clean = (
    df
    .withColumn("order_id", trim(col("order_id")).cast("string"))
    .withColumn("customer_id", trim(col("customer_id")).cast("string"))
    .withColumn("product_id", trim(col("product_id")).cast("string"))
    .withColumn("store_id", trim(col("store_id")).cast("string"))
    .withColumn("order_date", to_date(col("order_date")))
    .withColumn("quantity", col("quantity").cast("int"))
    .withColumn("unit_price", col("unit_price").cast("decimal(18,2)"))
    .withColumn("discount_pct", col("discount_pct").cast("decimal(9,4)"))
    .withColumn("last_modified_ts", to_timestamp(col("last_modified_ts")))
)

# Keep the latest source version for each order in the incoming Bronze data.
w = Window.partitionBy("order_id").orderBy(col("last_modified_ts").desc_nulls_last())
dedup = clean.withColumn("_rn", row_number().over(w)).filter(col("_rn") == 1).drop("_rn")

dq = (
    dedup
    .withColumn("dq_order_id", when(col("order_id").isNull() | (col("order_id") == ""), "Missing order_id"))
    .withColumn("dq_order_date", when(col("order_date").isNull(), "Invalid or missing order_date"))
    .withColumn("dq_customer_id", when(col("customer_id").isNull() | (col("customer_id") == ""), "Missing customer_id"))
    .withColumn("dq_product_id", when(col("product_id").isNull() | (col("product_id") == ""), "Missing product_id"))
    .withColumn("dq_store_id", when(col("store_id").isNull() | (col("store_id") == ""), "Missing store_id"))
    .withColumn("dq_quantity", when(col("quantity").isNull() | (col("quantity") <= 0), "Invalid quantity"))
    .withColumn("dq_unit_price", when(col("unit_price").isNull() | (col("unit_price") < 0), "Invalid unit_price"))
    .withColumn("dq_discount", when(col("discount_pct").isNull() | (col("discount_pct") < 0) | (col("discount_pct") > 1), "Invalid discount_pct"))
    .withColumn("dq_modified", when(col("last_modified_ts").isNull(), "Invalid or missing last_modified_ts"))
)

dq_cols = ["dq_order_id","dq_order_date","dq_customer_id","dq_product_id","dq_store_id",
           "dq_quantity","dq_unit_price","dq_discount","dq_modified"]

dq = dq.withColumn("rejection_reason", concat_ws("; ", *[col(c) for c in dq_cols]))

valid = (
    dq.filter(col("rejection_reason") == "")
    .drop(*(dq_cols + ["rejection_reason"]))
    .withColumn("gross_amount", spark_round(col("quantity") * col("unit_price"), 2))
    .withColumn("net_amount", spark_round(col("quantity") * col("unit_price") * (lit(1) - col("discount_pct")), 2))
)

invalid = (
    dq.filter(col("rejection_reason") != "")
    .drop(*dq_cols)
    .withColumn("quarantine_timestamp", current_timestamp())
    .withColumn("source_entity", lit("orders"))
)

if invalid.limit(1).count() > 0:
    invalid.write.format("delta").mode("append").save(PATHS["quarantine_orders"])

if not DeltaTable.isDeltaTable(spark, PATHS["silver_orders"]):
    valid.write.format("delta").mode("overwrite").save(PATHS["silver_orders"])
else:
    target = DeltaTable.forPath(spark, PATHS["silver_orders"])
    (
        target.alias("t")
        .merge(valid.alias("s"), "t.order_id = s.order_id")
        .whenMatchedUpdateAll(condition="s.last_modified_ts > t.last_modified_ts")
        .whenNotMatchedInsertAll()
        .execute()
    )

print("Orders Bronze -> Silver completed.")
