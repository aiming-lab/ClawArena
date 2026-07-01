-- Migration 0037 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-10
BEGIN;

-- ADD COLUMN on invoices
ALTER TABLE invoices
  ADD COLUMN batch_id VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 37, applied_at = NOW() WHERE name = 'invoices';

COMMIT;
