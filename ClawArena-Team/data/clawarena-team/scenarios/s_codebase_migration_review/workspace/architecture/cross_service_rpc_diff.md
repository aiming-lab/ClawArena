# Cross-Service RPC Schema Diff — payments-split migration

**Source:** architecture team review
**Date:** 2026-05-25

## Incompatibility Found

One RPC schema incompatibility was identified between the billing service
and the ledger client during the migration review:

### Billing proto (source of truth)

File: `services/billing/proto/v3.proto` **line 42**

```protobuf
service BillingService {
  // ProcessCharge uses int64 amount_cents
  rpc ProcessCharge(ChargeRequest) returns (ChargeResponse);
  ...
}
```

The `ChargeRequest.amount_cents` field is typed as `int64` (cent-level precision).

### Ledger client (consumer — incompatible)

File: `services/ledger/go/client.go` **line 117**

```go
// FIX REQUIRED BEFORE MERGE: update ChargeEntry.Amount to int64, rename to AmountCents
```

The ledger `ChargeEntry.Amount` field is typed as `float64`, which does not
match the billing proto's `int64`. This will cause silent precision loss in
reconciliation amounts.

## Impact

- **Services affected**: billing, ledger
- **Risk**: financial reconciliation amounts may silently lose precision at the
  float64/int64 boundary (e.g. $1.99 → $1 in some rounding modes)
- **Fix**: update `ChargeEntry.Amount` to `int64`, rename to `AmountCents`

## Resolution required before merge

The billing proto v3.proto:42 and the ledger client.go:117 must be aligned
before this PR can be merged. This is a hard blocker.
