# Databricks notebook source
# MAGIC %run ./00_Config

from pyspark.sql.functions import col, trim, when, concat_ws, current_timestamp, lit

df=spark.read.option("header",True).option("inferSchema",True).csv(PATHS["bronze_products"])
clean=(df.withColumn("product_id",trim(col("product_id")).cast("string"))
         .withColumn("product_name",trim(col("product_name")).cast("string"))
         .withColumn("category",trim(col("category")).cast("string"))
         .withColumn("unit_price",col("unit_price").cast("decimal(18,2)"))
         .dropDuplicates(["product_id"]))
dq=(clean.withColumn("dq_id",when(col("product_id").isNull()|(col("product_id")==""),"Missing product_id"))
         .withColumn("dq_name",when(col("product_name").isNull()|(col("product_name")==""),"Missing product_name"))
         .withColumn("dq_price",when(col("unit_price").isNull()|(col("unit_price")<0),"Invalid unit_price")))
cols=["dq_id","dq_name","dq_price"]
dq=dq.withColumn("rejection_reason",concat_ws("; ",*[col(c) for c in cols]))
valid=dq.filter(col("rejection_reason")=="").drop(*(cols+["rejection_reason"]))
invalid=(dq.filter(col("rejection_reason")!="").drop(*cols)
         .withColumn("quarantine_timestamp",current_timestamp()).withColumn("source_entity",lit("products")))
valid.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(PATHS["silver_products"])
if invalid.limit(1).count()>0: invalid.write.format("delta").mode("append").save(PATHS["quarantine_products"])
print("Products Bronze -> Silver completed.")
