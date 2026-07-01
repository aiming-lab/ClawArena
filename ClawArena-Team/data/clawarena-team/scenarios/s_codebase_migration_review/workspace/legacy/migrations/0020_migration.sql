-- Migration 0020 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-21
BEGIN;

-- DROP INDEX on ledger_entries
ALTER TABLE ledger_entries
  DROP INDEX created_at ;

-- Update version
UPDATE schema_versions SET version = 20, applied_at = NOW() WHERE name = 'ledger_entries';

COMMIT;
