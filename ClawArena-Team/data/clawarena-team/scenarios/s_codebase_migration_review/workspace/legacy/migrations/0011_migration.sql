-- Migration 0011 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-02-12
BEGIN;

-- ALTER COLUMN on reconciliation_jobs
ALTER TABLE reconciliation_jobs
  ALTER COLUMN retry_count VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 11, applied_at = NOW() WHERE name = 'reconciliation_jobs';

COMMIT;
