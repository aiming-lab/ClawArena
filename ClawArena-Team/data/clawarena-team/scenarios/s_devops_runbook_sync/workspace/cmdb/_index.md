# cmdb/ — CMDB operations database

## Files

| File | Description |
|---|---|
| ops_db.sqlite | **B-dimension**: SQLite database — must query with `sqlite3`. Contains `migration_events` and `approval_records` tables. |

## Query example

```sql
SELECT migration_id, status, phase, failure_reason
FROM migration_events WHERE status = 'FAILED';
```

The `migration_events` table has the authoritative record of the failing migration including phase and failure reason.
