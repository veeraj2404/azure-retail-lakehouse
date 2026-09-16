# Delta MERGE Tests

- Insert a new `order_id`: Silver row count should increase by one.
- Re-submit same `order_id` with an older timestamp: Silver should not change.
- Re-submit same `order_id` with a newer timestamp and changed values: Silver should update.
- Re-run unchanged Bronze input: Silver should remain logically idempotent.
