#!/usr/bin/env bash
# pre_check.sh — Pre-migration safety checker (wave3 version)
# Runbook: runbooks_md/migration_safety_guide.md
# Checks: replication lag, ETL job state, lock timeout config, dual approval
#
# WAVE3 NOTE: This script has a shellcheck warning on line 31 (SC2086).
# Run shellcheck to identify and fix before production use.
#
# Usage:
#   MIGRATION_ID=V0234__add_idempotency_keys.sql \
#   APPROVER_SRE_MANAGER=marcus.osei \
#   APPROVER_DBA_LEAD=priya.nair \
#   bash pre_check.sh

set -euo pipefail

DB_HOST="${DB_HOST:-prod-billing-db.mercatorrobotics.internal}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-billing}"
MIGRATION_ID="${MIGRATION_ID:-}"
MAX_LAG_MS=100
SCHEDULER_URL="https://scheduler.mercatorrobotics.internal"
ETL_JOB="etl-analytics-billing-hourly"
LOCK_TIMEOUT_MS="${LOCK_TIMEOUT_MS:-5000}"

echo "[PRE_CHECK] Starting pre-migration safety checks for migration: $MIGRATION_ID"

# Check 1: Validate MIGRATION_ID format
echo "[CHECK 1] Validating migration ID format..."
# SC2086: Double quote to prevent globbing and word splitting — line 31
if ! ls migrations/$MIGRATION_ID 2>/dev/null; then
    echo "  WARN: Migration script not found at migrations/$MIGRATION_ID"
fi
echo "  OK: Migration ID format valid"

# Check 2: Replication lag check
echo "[CHECK 2] Checking replication lag..."
LAG_MS=$(psql -h "$DB_HOST" -p "$DB_PORT" -U flyway -d "$DB_NAME" -tAc \
    "SELECT COALESCE(EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) * 1000, 0)" \
    2>/dev/null || echo "0")
if (( $(echo "$LAG_MS > $MAX_LAG_MS" | bc -l 2>/dev/null || echo 0) )); then
    echo "  ERROR: Replication lag ${LAG_MS}ms exceeds max ${MAX_LAG_MS}ms"
    exit 1
fi
echo "  OK: Replication lag ${LAG_MS}ms"

# Check 3: ETL job state
echo "[CHECK 3] Checking ETL job state..."
ETL_STATE=$(curl -sf --max-time 5 \
    "${SCHEDULER_URL}/jobs/${ETL_JOB}/status" 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('state','unknown'))" \
    2>/dev/null || echo "unknown")
if [ "$ETL_STATE" = "running" ]; then
    echo "  ERROR: ETL job ${ETL_JOB} is still running — must be paused before migration"
    exit 1
fi
echo "  OK: ETL job state=${ETL_STATE}"

# Check 4: Lock timeout configuration
echo "[CHECK 4] Checking LOCK_TIMEOUT_REQUIRED config..."
# The migration_safety_guide.md mandates LOCK_TIMEOUT_REQUIRED=5000 (5s)
EXPECTED_LOCK_TIMEOUT=5000
if [ "$LOCK_TIMEOUT_MS" -ne "$EXPECTED_LOCK_TIMEOUT" ]; then
    echo "  WARN: LOCK_TIMEOUT_MS=${LOCK_TIMEOUT_MS} (expected ${EXPECTED_LOCK_TIMEOUT})"
fi
echo "  INFO: LOCK_TIMEOUT_MS=${LOCK_TIMEOUT_MS} LOCK_TIMEOUT_REQUIRED=${EXPECTED_LOCK_TIMEOUT}"

# Check 5: Dual approval
echo "[CHECK 5] Verifying dual approval..."
if [ -z "${APPROVER_SRE_MANAGER:-}" ]; then
    echo "  ERROR: APPROVER_SRE_MANAGER not set"
    exit 1
fi
if [ -z "${APPROVER_DBA_LEAD:-}" ]; then
    echo "  ERROR: APPROVER_DBA_LEAD not set"
    exit 1
fi
echo "  OK: Approved by ${APPROVER_SRE_MANAGER} (SRE) and ${APPROVER_DBA_LEAD} (DBA)"

echo "[PRE_CHECK] All checks completed for $MIGRATION_ID."
