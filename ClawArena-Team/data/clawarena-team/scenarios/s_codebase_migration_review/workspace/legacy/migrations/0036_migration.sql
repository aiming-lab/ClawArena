-- Migration 0036 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-02-09
BEGIN;

-- ADD COLUMN on transactions
ALTER TABLE transactions
  ADD COLUMN status VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 36, applied_at = NOW() WHERE name = 'transactions';

COMMIT;
