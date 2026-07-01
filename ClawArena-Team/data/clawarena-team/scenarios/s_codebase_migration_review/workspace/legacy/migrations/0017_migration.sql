-- Migration 0017 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-18
BEGIN;

-- DROP INDEX on settlements
ALTER TABLE settlements
  DROP INDEX batch_id ;

-- Update version
UPDATE schema_versions SET version = 17, applied_at = NOW() WHERE name = 'settlements';

COMMIT;
