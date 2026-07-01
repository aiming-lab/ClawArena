# Payments Service — payments-split migration

## Overview

This directory contains the split-out `payments` service from the payments monorepo.
The migration PR (`payments-split`) extracts this service along with `billing`,
`ledger`, and `reports` into independent deployable units.

## Coverage

Current test coverage: **87.4%**
✅  Meets the 80% threshold.

## Structure

- `src/` — Python business logic modules
- `go/` — Go RPC handlers
- `k8s/` — Kubernetes deployment manifests
- `terraform/` — IaC (Google Cloud Run)
- `proto/` — Protobuf service definitions
- `tests/` — Pytest regression suite

## Migration status

Extracted from `monorepo/services/payments/` at commit `ref/payments-split-2026-05-20`.
Owner: Linda Wong (platform-migration team).
