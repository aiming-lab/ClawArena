-- V0235__add_lock_timeout_guard.sql
-- Hotfix applied after 2026-05-12 incident
-- Adds lock_timeout advisory to migration session configuration

-- This is now the TEMPLATE for all future DDL migrations:
-- SET lock_timeout = '30s'; must appear before any DDL.

BEGIN;
SET lock_timeout = '30s';

-- Example safe migration pattern:
ALTER TABLE billing_transactions
  ADD COLUMN IF NOT EXISTS migration_safe_example_col BOOLEAN DEFAULT FALSE;

COMMENT ON COLUMN billing_transactions.migration_safe_example_col
  IS 'Added as part of incident remediation V0235 to demonstrate lock_timeout usage.';

COMMIT;
