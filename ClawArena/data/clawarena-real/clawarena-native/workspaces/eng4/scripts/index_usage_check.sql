-- scripts/index_usage_check.sql
-- Check index usage rates and identify unused / redundant indexes
-- Reference: https://www.postgresql.org/docs/current/monitoring-stats.html

-- 1. Indexes with low usage (candidates for removal)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC
LIMIT 20;

-- 2. Tables with high seq_scan ratio (missing index candidates)
SELECT
    relname AS table_name,
    seq_scan,
    idx_scan,
    CASE WHEN seq_scan + idx_scan > 0
         THEN ROUND(100.0 * seq_scan / (seq_scan + idx_scan), 2)
         ELSE 0 END AS seq_scan_pct,
    n_live_tup,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY seq_scan DESC
LIMIT 20;

-- 3. Foreign keys without supporting indexes (Stormatics pattern)
SELECT
    conrelid::regclass AS table_name,
    a.attname AS column_name,
    conname AS constraint_name
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
      SELECT 1 FROM pg_index i
      WHERE i.indrelid = c.conrelid
        AND a.attnum = ANY(i.indkey)
  )
ORDER BY table_name;
