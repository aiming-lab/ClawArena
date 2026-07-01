-- Migration 0002 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-03
BEGIN;

-- ADD COLUMN on payments
ALTER TABLE payments
  ADD COLUMN created_at VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 2, applied_at = NOW() WHERE name = 'payments';

COMMIT;
