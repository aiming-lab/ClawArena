-- Migration 0039 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-05-12
BEGIN;

-- DROP INDEX on reports
ALTER TABLE reports
  DROP INDEX service_id ;

-- Update version
UPDATE schema_versions SET version = 39, applied_at = NOW() WHERE name = 'reports';

COMMIT;
