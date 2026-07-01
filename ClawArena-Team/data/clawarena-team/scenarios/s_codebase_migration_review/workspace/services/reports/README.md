# Reports Service — payments-split migration

## Overview

This directory contains the split-out `reports` service from the payments monorepo.
The migration PR (`payments-split`) extracts this service along with `billing`,
`ledger`, and `reports` into independent deployable units.

## Coverage

Current test coverage: **76.8%**
⚠️  Below the 80% threshold required for merge approval.

## Structure

- `src/` — Python business logic modules
- `go/` — Go RPC handlers
- `k8s/` — Kubernetes deployment manifests
- `terraform/` — IaC (Google Cloud Run)
- `proto/` — Protobuf service definitions
- `tests/` — Pytest regression suite

## Migration status

Extracted from `monorepo/services/reports/` at commit `ref/reports-split-2026-05-20`.
Owner: Linda Wong (platform-migration team).
