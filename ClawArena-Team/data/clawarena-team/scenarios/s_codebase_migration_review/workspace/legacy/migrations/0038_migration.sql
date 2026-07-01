-- Migration 0038 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-11
BEGIN;

-- ALTER COLUMN on settlements
ALTER TABLE settlements
  ALTER COLUMN created_at VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 38, applied_at = NOW() WHERE name = 'settlements';

COMMIT;
