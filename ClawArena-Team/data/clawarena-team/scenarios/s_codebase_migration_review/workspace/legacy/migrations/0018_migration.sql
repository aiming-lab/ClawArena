-- Migration 0018 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-19
BEGIN;

-- ADD COLUMN on ledger_entries
ALTER TABLE ledger_entries
  ADD COLUMN retry_count VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 18, applied_at = NOW() WHERE name = 'ledger_entries';

COMMIT;
