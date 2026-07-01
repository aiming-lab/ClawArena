-- Migration 0004 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-05-05
BEGIN;

-- DROP INDEX on reports
ALTER TABLE reports
  DROP INDEX created_at ;

-- Update version
UPDATE schema_versions SET version = 4, applied_at = NOW() WHERE name = 'reports';

COMMIT;
