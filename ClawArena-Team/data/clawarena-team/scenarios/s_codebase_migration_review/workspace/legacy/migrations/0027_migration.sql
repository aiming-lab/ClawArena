-- Migration 0027 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-28
BEGIN;

-- DROP INDEX on reconciliation_jobs
ALTER TABLE reconciliation_jobs
  DROP INDEX checksum ;

-- Update version
UPDATE schema_versions SET version = 27, applied_at = NOW() WHERE name = 'reconciliation_jobs';

COMMIT;
