# Orders Source Contract

| Column | Expected Type | Rule |
|---|---|---|
| order_id | string | Required; business key |
| order_date | date | Required and parseable |
| customer_id | string | Required |
| product_id | string | Required |
| store_id | string | Required |
| quantity | integer | > 0 |
| unit_price | decimal(18,2) | >= 0 |
| discount_pct | decimal(9,4) | Between 0 and 1 |
| last_modified_ts | timestamp | Required for deterministic merge/update handling |
