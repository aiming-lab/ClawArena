-- scripts/find_slow_queries.sql
-- Identify top-20 slowest queries from pg_stat_statements
-- Reference: https://www.postgresql.org/docs/current/pgstatstatements.html

SELECT
    queryid,
    calls,
    ROUND(mean_exec_time::numeric, 2)  AS mean_exec_time_ms,
    ROUND(total_exec_time::numeric, 2) AS total_exec_time_ms,
    ROUND(stddev_exec_time::numeric, 2) AS stddev_ms,
    rows,
    ROUND(shared_blks_read::numeric / GREATEST(calls, 1), 0) AS avg_blks_read,
    LEFT(query, 120) AS query_preview
FROM pg_stat_statements
WHERE mean_exec_time > 500          -- threshold: 500ms
  AND toplevel = TRUE
ORDER BY mean_exec_time DESC
LIMIT 20;

-- To reset statistics (use with caution in production):
-- SELECT pg_stat_statements_reset();
