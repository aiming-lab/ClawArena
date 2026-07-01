# Migration Request — payments-split

**From:** Linda Wong, Platform Migration Team
**Date:** 2026-05-24
**Project:** payments-split

Hi team,

I'm opening the PR to split four services out of the payments monorepo:
- `services/payments` — core payment processing
- `services/billing` — invoicing and billing cycles
- `services/ledger` — transaction ledger (the most complex one)
- `services/reports` — reporting and analytics

The split covers ~180k tokens of code (Python, Go, YAML, Terraform, protobuf).
Shared infrastructure (lib, proto, configs) stays in `shared/`.

Key files to look at:
- `architecture/service_inventory.yaml` — lists all 4 services with metadata
- `architecture/shared_deps_audit.json` — 7 shared dependencies identified, one flagged high-risk
- `architecture/cross_service_rpc_diff.md` — one RPC schema incompatibility documented

Please complete the review by EOD 2026-05-26.

— Linda
