-- Migration 0023 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-24
BEGIN;

-- ADD COLUMN on audit_logs
ALTER TABLE audit_logs
  ADD COLUMN status VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 23, applied_at = NOW() WHERE name = 'audit_logs';

COMMIT;
