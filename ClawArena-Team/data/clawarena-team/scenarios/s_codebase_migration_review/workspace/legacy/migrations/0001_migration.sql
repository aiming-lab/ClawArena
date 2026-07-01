-- Migration 0001 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-02-02
BEGIN;

-- ADD COLUMN on ledger_entries
ALTER TABLE ledger_entries
  ADD COLUMN checksum VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 1, applied_at = NOW() WHERE name = 'ledger_entries';

COMMIT;
