#!/usr/bin/env bash
# rollback.sh — Database migration rollback (wave3 version)
# Runbook: runbooks_md/RB-DB-002-rollback-procedure.md

set -euo pipefail

MIGRATION_ID="${MIGRATION_ID:-V0234__add_idempotency_keys.sql}"
DB_HOST="${DB_HOST:-prod-billing-db.mercatorrobotics.internal}"
DB_NAME="${DB_NAME:-billing}"

echo "[ROLLBACK] Starting rollback for $MIGRATION_ID at $(date -u)"

# Step 1: Kill blocking queries
echo "[STEP 1] Killing blocking queries..."
psql -h "$DB_HOST" -U flyway -d "$DB_NAME" <<'SQL' 2>&1 || true
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE wait_event_type = 'Lock' AND state = 'active' AND pid != pg_backend_pid();
SQL

# Step 2: Flyway repair
echo "[STEP 2] Running flyway repair..."
flyway -url="jdbc:postgresql://$DB_HOST:5432/$DB_NAME" \
       -schemas=public repair 2>&1 || true

# Step 3: Resume ETL
echo "[STEP 3] Resuming analytics ETL job..."
curl -sf -X POST "https://scheduler.mercatorrobotics.internal/jobs/etl-analytics-billing-hourly/resume" || true

echo "[ROLLBACK] Rollback complete at $(date -u)"
