-- Migration 0003 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-04
BEGIN;

-- CREATE INDEX on reports
ALTER TABLE reports
  CREATE INDEX batch_id ;

-- Update version
UPDATE schema_versions SET version = 3, applied_at = NOW() WHERE name = 'reports';

COMMIT;
