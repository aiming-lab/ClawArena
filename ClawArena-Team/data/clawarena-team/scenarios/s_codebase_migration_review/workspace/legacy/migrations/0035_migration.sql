-- Migration 0035 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-08
BEGIN;

-- CREATE INDEX on transactions
ALTER TABLE transactions
  CREATE INDEX batch_id ;

-- Update version
UPDATE schema_versions SET version = 35, applied_at = NOW() WHERE name = 'transactions';

COMMIT;
