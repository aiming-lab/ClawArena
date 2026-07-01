#!/bin/bash
# scripts/vacuum_analyze_report.sh
# Report last_autovacuum and n_dead_tup for all public tables
# Used to identify tables needing manual ANALYZE after bulk operations

set -euo pipefail

PGCONN="${PGCONN:-postgres://localhost:5432/finedge_prod}"

psql "$PGCONN" <<'SQL'
SELECT
    relname AS table_name,
    n_live_tup,
    n_dead_tup,
    ROUND(100.0 * n_dead_tup / GREATEST(n_live_tup + n_dead_tup, 1), 2) AS dead_pct,
    last_autovacuum,
    last_autoanalyze,
    CASE
        WHEN last_autovacuum < NOW() - INTERVAL '3 days' THEN 'STALE — consider VACUUM ANALYZE'
        WHEN n_dead_tup > n_live_tup * 0.1 THEN 'HIGH BLOAT — VACUUM recommended'
        ELSE 'OK'
    END AS status
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_dead_tup DESC;
SQL
