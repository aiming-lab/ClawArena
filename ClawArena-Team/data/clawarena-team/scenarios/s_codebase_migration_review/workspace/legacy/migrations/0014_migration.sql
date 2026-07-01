-- Migration 0014 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-05-15
BEGIN;

-- CREATE INDEX on invoices
ALTER TABLE invoices
  CREATE INDEX checksum ;

-- Update version
UPDATE schema_versions SET version = 14, applied_at = NOW() WHERE name = 'invoices';

COMMIT;
