-- Migration 0005 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-06
BEGIN;

-- DROP INDEX on audit_logs
ALTER TABLE audit_logs
  DROP INDEX status ;

-- Update version
UPDATE schema_versions SET version = 5, applied_at = NOW() WHERE name = 'audit_logs';

COMMIT;
