-- Migration 0019 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-05-20
BEGIN;

-- ADD COLUMN on payments
ALTER TABLE payments
  ADD COLUMN version VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 19, applied_at = NOW() WHERE name = 'payments';

COMMIT;
