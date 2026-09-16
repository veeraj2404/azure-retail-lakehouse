# Reconciliation Tests

- Silver Orders business keys are unique.
- Silver Orders references exist in Customer/Product/Store Silver datasets.
- Gold fact row count equals publishable Silver Orders row count.
- Gold fact foreign keys resolve to all dimensions.
- Azure SQL row counts match Gold table row counts after serving load.
- Power BI totals reconcile to Azure SQL aggregate queries.
