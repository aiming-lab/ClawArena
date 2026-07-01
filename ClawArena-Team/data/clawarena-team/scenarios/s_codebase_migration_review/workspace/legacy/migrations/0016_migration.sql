-- Migration 0016 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-02-17
BEGIN;

-- ALTER COLUMN on transactions
ALTER TABLE transactions
  ALTER COLUMN retry_count VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 16, applied_at = NOW() WHERE name = 'transactions';

COMMIT;
