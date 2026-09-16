# Databricks notebook source
# MAGIC %run ./00_Config

from pyspark.sql.functions import col, trim, lower, to_date, when, concat_ws, current_timestamp, lit

df = spark.read.option("header", True).option("inferSchema", True).csv(PATHS["bronze_customers"])

clean = (
    df.withColumn("customer_id", trim(col("customer_id")).cast("string"))
      .withColumn("customer_name", trim(col("customer_name")).cast("string"))
      .withColumn("email", lower(trim(col("email"))).cast("string"))
      .withColumn("city", trim(col("city")).cast("string"))
      .withColumn("state", trim(col("state")).cast("string"))
      .withColumn("created_date", to_date(col("created_date")))
      .dropDuplicates(["customer_id"])
)

dq = (
    clean
    .withColumn("dq_id", when(col("customer_id").isNull() | (col("customer_id") == ""), "Missing customer_id"))
    .withColumn("dq_name", when(col("customer_name").isNull() | (col("customer_name") == ""), "Missing customer_name"))
    .withColumn("dq_date", when(col("created_date").isNull(), "Invalid or missing created_date"))
)
dq_cols=["dq_id","dq_name","dq_date"]
dq=dq.withColumn("rejection_reason",concat_ws("; ",*[col(c) for c in dq_cols]))
valid=dq.filter(col("rejection_reason")=="").drop(*(dq_cols+["rejection_reason"]))
invalid=(dq.filter(col("rejection_reason")!="").drop(*dq_cols)
         .withColumn("quarantine_timestamp",current_timestamp()).withColumn("source_entity",lit("customers")))

valid.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(PATHS["silver_customers"])
if invalid.limit(1).count()>0:
    invalid.write.format("delta").mode("append").save(PATHS["quarantine_customers"])
print("Customers Bronze -> Silver completed.")
