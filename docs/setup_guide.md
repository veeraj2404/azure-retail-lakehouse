# Setup Guide

Required Azure services:
- ADLS Gen2
- Azure Databricks
- Azure SQL Database
- Azure Data Factory
- Power BI Desktop / Service

Create ADLS containers: bronze, silver, gold, quarantine.
Configure Databricks access using your approved managed identity/access connector and Unity Catalog/external-location approach.
Do not place secrets in notebooks or Git.
