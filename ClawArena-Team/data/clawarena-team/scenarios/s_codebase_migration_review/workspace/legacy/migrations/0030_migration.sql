-- Migration 0030 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-03
BEGIN;

-- ADD COLUMN on audit_logs
ALTER TABLE audit_logs
  ADD COLUMN version VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 30, applied_at = NOW() WHERE name = 'audit_logs';

COMMIT;
