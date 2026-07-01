-- Migration 0013 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-14
BEGIN;

-- DROP INDEX on audit_logs
ALTER TABLE audit_logs
  DROP INDEX updated_at ;

-- Update version
UPDATE schema_versions SET version = 13, applied_at = NOW() WHERE name = 'audit_logs';

COMMIT;
