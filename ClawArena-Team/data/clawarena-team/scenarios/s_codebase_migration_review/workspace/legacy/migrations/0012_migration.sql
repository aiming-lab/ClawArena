-- Migration 0012 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-13
BEGIN;

-- DROP INDEX on reconciliation_jobs
ALTER TABLE reconciliation_jobs
  DROP INDEX batch_id ;

-- Update version
UPDATE schema_versions SET version = 12, applied_at = NOW() WHERE name = 'reconciliation_jobs';

COMMIT;
