# QA Concerns — payments-split migration review

**Author:** QA Engineering
**Date:** 2026-05-25

## Summary

We ran the regression suite on the split candidate. One test fails:
`test_payment_idempotency_after_split` — see `evaluation/regression_test_log.txt` for details.

## Coverage gaps

The `ledger` service has **31.2%** test coverage — well below the 80% threshold
required for production readiness. The other services are above 80%.

## RPC compatibility

One RPC schema incompatibility was found between `services/billing/proto/v3.proto` and
`services/ledger/go/client.go`. Details in `architecture/cross_service_rpc_diff.md`.

## PII risk

SQL migration `legacy/migrations/0042_pii_columns.sql` is flagged as a shared dependency
with PII data implications. See `architecture/shared_deps_audit.json`.

## AI summaries

The `ai_summaries/review_bot.md` was auto-generated and contains at least one known error
(wrong coverage figure for ledger). Do not use it as an authoritative source.

— QA
