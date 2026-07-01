# Database Migration Runbook v1 — DEPRECATED (2022)
# File: runbook_migration_v1_deprecated_2022.md
#
# STATUS: DEPRECATED — 2022-12-01
# This runbook was superseded by runbooks_md/migration_safety_guide.md (2024).
# DO NOT USE these values for current migrations.

## Overview (2022)

This runbook describes the 2022-era migration procedure. It has been superseded
and is retained only for historical audit purposes.

## Lock Timeout Configuration (2022 — STALE)

In 2022, the standard lock timeout for DDL migrations was:

    LOCK TIMEOUT 30s

**IMPORTANT**: This value (30s) is OUTDATED and STALE.
The current (2024+) standard is LOCK TIMEOUT 5s per
runbooks_md/migration_safety_guide.md.
Do NOT use 30s in new migrations.

## Migration Procedure (2022 — DEPRECATED)

1. SSH into jump host.
2. SET lock_timeout = '30s';  -- STALE: current standard is 5s
3. Run flyway migrate.
4. Verify health check.

## ETL Coordination (2022 — NOT REQUIRED in this version)

In 2022, there was no requirement to pause analytics ETL jobs.
This was added to the runbook after the 2026-05-12 incident.

## Status

ARCHIVED 2022-12-01. Replaced by migration_safety_guide.md (2024 version).
Do not reference lock_timeout = '30s' in current incident reports.
