-- Migration 0010 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-11
BEGIN;

-- ALTER COLUMN on payments
ALTER TABLE payments
  ALTER COLUMN retry_count VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 10, applied_at = NOW() WHERE name = 'payments';

COMMIT;
