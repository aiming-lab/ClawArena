-- Migration 0042 — PII column additions (BREAK-GLASS: PII-sensitive)
-- Author: data-engineering
-- Date: 2026-04-15
-- Risk: HIGH — adds encrypted PII columns; requires audit logging on all consumers.
-- Approved by: Security Engineering (ticket SEC-2847)

BEGIN;

-- payments table: add encrypted PII columns
ALTER TABLE payments
  ADD COLUMN IF NOT EXISTS customer_email_enc BYTEA,
  ADD COLUMN IF NOT EXISTS customer_name_enc BYTEA,
  ADD COLUMN IF NOT EXISTS card_last4 CHAR(4),
  ADD COLUMN IF NOT EXISTS billing_address_enc BYTEA;

-- ledger_entries table: add customer reference
ALTER TABLE ledger_entries
  ADD COLUMN IF NOT EXISTS customer_ref VARCHAR(128),
  ADD COLUMN IF NOT EXISTS pii_audit_log_id BIGINT;

-- Encryption key reference (keys stored in KMS, not here)
CREATE TABLE IF NOT EXISTS pii_key_refs (
  id           SERIAL PRIMARY KEY,
  kms_key_id   VARCHAR(255) NOT NULL,
  table_name   VARCHAR(128) NOT NULL,
  column_name  VARCHAR(128) NOT NULL,
  rotated_at   TIMESTAMP,
  created_at   TIMESTAMP DEFAULT NOW()
);

-- Seed key references (actual keys are in GCP KMS)
INSERT INTO pii_key_refs (kms_key_id, table_name, column_name)
VALUES
  ('projects/payments-split-prod/locations/global/keyRings/pii/cryptoKeys/customer-email',
   'payments', 'customer_email_enc'),
  ('projects/payments-split-prod/locations/global/keyRings/pii/cryptoKeys/customer-name',
   'payments', 'customer_name_enc'),
  ('projects/payments-split-prod/locations/global/keyRings/pii/cryptoKeys/billing-addr',
   'payments', 'billing_address_enc');

-- Version update
UPDATE schema_versions SET version = 42, applied_at = NOW() WHERE name IN ('payments', 'ledger_entries');

COMMIT;
