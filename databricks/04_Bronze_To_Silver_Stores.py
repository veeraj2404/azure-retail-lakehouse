# Databricks notebook source
# MAGIC %run ./00_Config

from pyspark.sql.functions import col, trim, when, concat_ws, current_timestamp, lit

df=spark.read.option("header",True).option("inferSchema",True).csv(PATHS["bronze_stores"])
clean=(df.withColumn("store_id",trim(col("store_id")).cast("string"))
         .withColumn("store_name",trim(col("store_name")).cast("string"))
         .withColumn("city",trim(col("city")).cast("string"))
         .withColumn("state",trim(col("state")).cast("string"))
         .withColumn("region",trim(col("region")).cast("string"))
         .dropDuplicates(["store_id"]))
dq=(clean.withColumn("dq_id",when(col("store_id").isNull()|(col("store_id")==""),"Missing store_id"))
         .withColumn("dq_name",when(col("store_name").isNull()|(col("store_name")==""),"Missing store_name")))
cols=["dq_id","dq_name"]
dq=dq.withColumn("rejection_reason",concat_ws("; ",*[col(c) for c in cols]))
valid=dq.filter(col("rejection_reason")=="").drop(*(cols+["rejection_reason"]))
invalid=(dq.filter(col("rejection_reason")!="").drop(*cols)
         .withColumn("quarantine_timestamp",current_timestamp()).withColumn("source_entity",lit("stores")))
valid.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(PATHS["silver_stores"])
if invalid.limit(1).count()>0: invalid.write.format("delta").mode("append").save(PATHS["quarantine_stores"])
print("Stores Bronze -> Silver completed.")
