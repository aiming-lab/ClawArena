-- Migration 0031 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-02-04
BEGIN;

-- ALTER COLUMN on payments
ALTER TABLE payments
  ALTER COLUMN created_at VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 31, applied_at = NOW() WHERE name = 'payments';

COMMIT;
