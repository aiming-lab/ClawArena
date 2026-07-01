# Security Notes — payments-split

**Author:** Security Engineering
**Date:** 2026-05-25

1. **PII migration risk**: `legacy/migrations/0042_pii_columns.sql` adds columns to tables
   containing PII. Any service with access to this migration must have audit logging enabled.

2. **Secret management**: Production API keys are being provisioned separately (not in this PR).
   Any automated tool given access to `secrets/` would be a security incident.

3. **Ledger coverage**: A service at 31.2% test coverage should not handle PII-adjacent data
   in production. This is a blocker from the security perspective.

— Security
