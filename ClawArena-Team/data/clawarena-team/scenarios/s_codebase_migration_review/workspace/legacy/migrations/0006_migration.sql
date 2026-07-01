-- Migration 0006 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-02-07
BEGIN;

-- ALTER COLUMN on invoices
ALTER TABLE invoices
  ALTER COLUMN checksum VARCHAR(255);

-- Update version
UPDATE schema_versions SET version = 6, applied_at = NOW() WHERE name = 'invoices';

COMMIT;
