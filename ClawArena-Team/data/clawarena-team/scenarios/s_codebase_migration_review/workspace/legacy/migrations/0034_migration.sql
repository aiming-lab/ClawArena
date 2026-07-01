-- Migration 0034 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-05-07
BEGIN;

-- ADD COLUMN on transactions
ALTER TABLE transactions
  ADD COLUMN version VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 34, applied_at = NOW() WHERE name = 'transactions';

COMMIT;
