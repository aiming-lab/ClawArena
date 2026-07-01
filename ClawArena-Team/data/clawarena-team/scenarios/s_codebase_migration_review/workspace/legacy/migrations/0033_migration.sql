-- Migration 0033 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-06
BEGIN;

-- CREATE INDEX on ledger_entries
ALTER TABLE ledger_entries
  CREATE INDEX checksum ;

-- Update version
UPDATE schema_versions SET version = 33, applied_at = NOW() WHERE name = 'ledger_entries';

COMMIT;
