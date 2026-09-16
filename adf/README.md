# Azure Data Factory

ADF is used for orchestration and the Gold -> Azure SQL serving load.

Pipelines:
- `PL_Bronze_To_Silver`
- `PL_Silver_To_Gold`
- `PL_Gold_To_AzureSQL`
- `PL_Retail_Lakehouse_Orchestration`

The orchestration pipeline loads dimensions before `fact_sales` so Azure SQL foreign keys can be satisfied.

These JSON files are project templates. Replace workspace/server/storage placeholders and validate against your live ADF export format before publishing.
