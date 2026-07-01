-- Migration 0022 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-23
BEGIN;

-- CREATE INDEX on ledger_entries
ALTER TABLE ledger_entries
  CREATE INDEX status ;

-- Update version
UPDATE schema_versions SET version = 22, applied_at = NOW() WHERE name = 'ledger_entries';

COMMIT;
