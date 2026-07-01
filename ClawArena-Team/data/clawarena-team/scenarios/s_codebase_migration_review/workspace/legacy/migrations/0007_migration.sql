-- Migration 0007 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-08
BEGIN;

-- CREATE INDEX on transactions
ALTER TABLE transactions
  CREATE INDEX service_id ;

-- Update version
UPDATE schema_versions SET version = 7, applied_at = NOW() WHERE name = 'transactions';

COMMIT;
