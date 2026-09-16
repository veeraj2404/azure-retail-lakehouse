# Data Flow

Client raw files -> Bronze.

Bronze Orders -> Orders Silver / Orders Quarantine.
Bronze Customers -> Customers Silver / Customers Quarantine.
Bronze Products -> Products Silver / Products Quarantine.
Bronze Stores -> Stores Silver / Stores Quarantine.

Silver Orders + Customers + Products + Stores -> Gold star schema.

Gold dimensions are loaded into Azure SQL first; `fact_sales` is loaded after dimensions.

Power BI consumes Azure SQL only.
