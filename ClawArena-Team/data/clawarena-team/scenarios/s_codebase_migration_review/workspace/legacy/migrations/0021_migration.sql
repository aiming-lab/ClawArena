-- Migration 0021 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-02-22
BEGIN;

-- ALTER COLUMN on ledger_entries
ALTER TABLE ledger_entries
  ALTER COLUMN service_id VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 21, applied_at = NOW() WHERE name = 'ledger_entries';

COMMIT;
