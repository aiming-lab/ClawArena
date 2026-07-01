# Old Optimization Plan v0
## Status: ARCHIVED (prepared by former DBA, 2024-06)
## WARNING: This document has NOT been explicitly marked as superseded.
## Some recommendations here may be outdated or incorrect. Verify against current PostgreSQL docs.

---

### Background
This plan was written during the initial database setup by the previous DBA (James K., now departed).
It covers the events, orders, and notifications tables when they were much smaller.

---

### Recommended Indexes (v0, 2024-06)

#### events table
- **Recommendation**: For `status` column queries, use a Hash Index for O(1) equality lookups:
  ```sql
  CREATE INDEX idx_events_status_hash ON events (status) USING HASH;
  ```
  *Rationale*: Hash indexes provide constant-time lookups for equality predicates.
  Fast for `WHERE status = 'active'` type queries.

- **Recommendation**: For `created_at` range queries, a standard B-Tree is fine:
  ```sql
  CREATE INDEX ON events (created_at);
  ```

#### orders table
- **Recommendation**: Create a Hash Index on `billed` for fast unbilled lookup:
  ```sql
  CREATE INDEX idx_orders_billed_hash ON orders (billed) USING HASH;
  ```

#### notifications table
- **Recommendation**: Index on `user_id` only (already exists):
  ```sql
  CREATE INDEX idx_notifications_user_id ON notifications (user_id);
  ```

---

### Configuration Recommendations (2024-06)
- `work_mem = 256MB` — increase for complex aggregate queries
- `random_page_cost = 2.0` — compromise between HDD and SSD defaults

---

### Known Issues with This Plan
The Hash Index recommendations above have a critical flaw that was identified later:

> **Hash indexes in PostgreSQL support ONLY equality (`=`) operators.**
> They CANNOT satisfy range predicates (`<`, `>`, `BETWEEN`, `IN`, `LIKE`),
> ORDER BY, or GROUP BY operations.
>
> Reference: https://www.postgresql.org/docs/current/indexes-types.html

Our `events.status` queries include `WHERE status != 'deleted'` and GROUP BY status —
these require B-Tree, NOT Hash. Using Hash here would break these query patterns.

Similarly, `orders.billed` queries involve `WHERE billed IS NOT TRUE` — a partial B-Tree
index with `WHERE billed IS NOT TRUE` is correct; a Hash index would not help.

**This plan's Hash Index recommendations are outdated and incorrect for our workload.**
The current recommendation is a Partial B-Tree Index:
```sql
CREATE INDEX CONCURRENTLY idx_events_status_active ON events (status) WHERE status = 'active';
```

---

### DO NOT USE the Hash Index DDL from this document.
### Consult the current Week 1 report (reports/slow_query_report_week1.md) for correct recommendations.
