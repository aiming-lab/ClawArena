-- Migration 0032 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-03-05
BEGIN;

-- CREATE INDEX on invoices
ALTER TABLE invoices
  CREATE INDEX updated_at ;

-- Update version
UPDATE schema_versions SET version = 32, applied_at = NOW() WHERE name = 'invoices';

COMMIT;
