-- Migration 0040 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-13
BEGIN;

-- ADD COLUMN on reconciliation_jobs
ALTER TABLE reconciliation_jobs
  ADD COLUMN version VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 40, applied_at = NOW() WHERE name = 'reconciliation_jobs';

COMMIT;
