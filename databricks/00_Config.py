# Databricks notebook source
# Environment-safe project configuration. Do not store secrets here.

STORAGE_ACCOUNT = "<storage-account-name>"

BRONZE = f"abfss://bronze@{STORAGE_ACCOUNT}.dfs.core.windows.net"
SILVER = f"abfss://silver@{STORAGE_ACCOUNT}.dfs.core.windows.net"
GOLD = f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net"
QUARANTINE = f"abfss://quarantine@{STORAGE_ACCOUNT}.dfs.core.windows.net"

PATHS = {
    "bronze_orders": f"{BRONZE}/orders/",
    "bronze_customers": f"{BRONZE}/customers/customers.csv",
    "bronze_products": f"{BRONZE}/products/products.csv",
    "bronze_stores": f"{BRONZE}/stores/stores.csv",
    "silver_orders": f"{SILVER}/orders/",
    "silver_customers": f"{SILVER}/customers/",
    "silver_products": f"{SILVER}/products/",
    "silver_stores": f"{SILVER}/stores/",
    "quarantine_orders": f"{QUARANTINE}/orders/",
    "quarantine_customers": f"{QUARANTINE}/customers/",
    "quarantine_products": f"{QUARANTINE}/products/",
    "quarantine_stores": f"{QUARANTINE}/stores/",
    "gold_fact_sales": f"{GOLD}/fact_sales/",
    "gold_dim_customer": f"{GOLD}/dim_customer/",
    "gold_dim_product": f"{GOLD}/dim_product/",
    "gold_dim_store": f"{GOLD}/dim_store/",
    "gold_dim_date": f"{GOLD}/dim_date/",
}
