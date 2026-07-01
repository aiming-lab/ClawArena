-- Migration 0028 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-04-01
BEGIN;

-- CREATE INDEX on invoices
ALTER TABLE invoices
  CREATE INDEX updated_at ;

-- Update version
UPDATE schema_versions SET version = 28, applied_at = NOW() WHERE name = 'invoices';

COMMIT;
