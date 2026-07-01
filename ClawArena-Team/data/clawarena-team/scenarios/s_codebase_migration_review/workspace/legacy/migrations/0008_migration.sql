-- Migration 0008 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-09
BEGIN;

-- DROP INDEX on reports
ALTER TABLE reports
  DROP INDEX service_id ;

-- Update version
UPDATE schema_versions SET version = 8, applied_at = NOW() WHERE name = 'reports';

COMMIT;
