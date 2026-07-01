-- Migration 0043 — payments-split safety patch for 0042_pii_columns.sql
-- Author: DevOps / Platform Team
-- Date: 2026-05-26
-- Context: Follow-up to 0042_pii_columns.sql (PII column additions)
--          This patch adds audit triggers and row-level security policies.

BEGIN;

-- Audit trigger for PII column access
CREATE OR REPLACE FUNCTION audit_pii_access()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (
    table_name, operation, user_id, accessed_at, row_id
  ) VALUES (
    TG_TABLE_NAME, TG_OP, current_user, NOW(), NEW.id
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to tables modified by 0042
CREATE TRIGGER trg_audit_payments_pii
  AFTER INSERT OR UPDATE OR SELECT ON payments
  FOR EACH ROW EXECUTE FUNCTION audit_pii_access();

CREATE TRIGGER trg_audit_ledger_pii
  AFTER INSERT OR UPDATE OR SELECT ON ledger_entries
  FOR EACH ROW EXECUTE FUNCTION audit_pii_access();

-- Row-level security: only the owning service SA can read PII columns
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE ledger_entries ENABLE ROW LEVEL SECURITY;

CREATE POLICY payments_rls ON payments
  FOR ALL TO payments_service_role
  USING (service_owner = 'payments');

CREATE POLICY ledger_rls ON ledger_entries
  FOR ALL TO ledger_service_role
  USING (service_owner = 'ledger');

UPDATE schema_versions
  SET version = 43, applied_at = NOW()
  WHERE name IN ('payments', 'ledger_entries');

COMMIT;
