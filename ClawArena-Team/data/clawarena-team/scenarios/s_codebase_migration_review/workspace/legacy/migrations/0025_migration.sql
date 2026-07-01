-- Migration 0025 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-01-26
BEGIN;

-- ADD COLUMN on settlements
ALTER TABLE settlements
  ADD COLUMN version VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 25, applied_at = NOW() WHERE name = 'settlements';

COMMIT;
