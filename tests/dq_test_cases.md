# DQ Test Cases

1. Null `customer_id` in Orders -> Quarantine.
2. `quantity <= 0` -> Quarantine.
3. Negative `unit_price` -> Quarantine.
4. `discount_pct < 0` or `> 1` -> Quarantine.
5. Invalid `order_date` -> Quarantine.
6. Missing `last_modified_ts` -> Quarantine.
7. Duplicate `order_id` versions -> latest timestamp retained for merge.
8. Missing master-data business key -> corresponding Quarantine.
9. Valid rows -> Silver only.
10. Each quarantined row contains `rejection_reason`, `source_entity`, `quarantine_timestamp`.
