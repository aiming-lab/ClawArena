-- Migration 0024 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-05-25
BEGIN;

-- CREATE INDEX on settlements
ALTER TABLE settlements
  CREATE INDEX version ;

-- Update version
UPDATE schema_versions SET version = 24, applied_at = NOW() WHERE name = 'settlements';

COMMIT;
