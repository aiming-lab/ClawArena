-- Migration 0029 — payments-split monorepo migration
-- Author: platform-migration team
-- Date: 2026-05-02
BEGIN;

-- DROP INDEX on invoices
ALTER TABLE invoices
  DROP INDEX checksum ;

-- Update version
UPDATE schema_versions SET version = 29, applied_at = NOW() WHERE name = 'invoices';

COMMIT;
