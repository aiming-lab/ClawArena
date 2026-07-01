-- Migration 0015 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-16
BEGIN;

-- ADD COLUMN on reports
ALTER TABLE reports
  ADD COLUMN status VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 15, applied_at = NOW() WHERE name = 'reports';

COMMIT;
