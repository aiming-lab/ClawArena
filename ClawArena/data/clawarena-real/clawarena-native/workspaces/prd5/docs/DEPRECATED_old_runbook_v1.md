# A/B Testing Runbook — DEPRECATED VERSION (v1)

⚠️ ⚠️ ⚠️ THIS DOCUMENT IS DEPRECATED AND SHOULD NOT BE USED ⚠️ ⚠️ ⚠️

This runbook has been superseded by docs/ab_testing_runbook.md (v2).
The parameters in this document contain known errors and do not reflect current company policy.

DEPRECATED DATE: 2023-10-15
REASON: Incorrect z-values; missing Bonferroni correction guidance; outdated SRM threshold

---

# OLD Runbook (DO NOT USE)

## Quick Reference (WRONG VALUES — DO NOT USE)

| Parameter | Value | NOTE |
|-----------|-------|------|
| Alpha | 0.05 | |
| Power | 0.80 | |
| z_alpha/2 | **2.33** | ❌ WRONG — should be 1.96 |
| z_beta | **1.04** | ❌ WRONG — should be 0.84 |
| SRM threshold | p < 0.05 | ❌ WRONG — should be p < 0.01 (Statsig) |
| CUPED window | **14 days** | ❌ WRONG — should be 7 days (Statsig) |
| Multiple testing | None (not specified) | ❌ MISSING |

## OLD Sample Size Formula (INCORRECT)

n = z_alpha^2 × [2 × p(1-p)] / MDE^2

(This formula uses incorrect z-values and a simplified variance formula)

Example (WRONG): p1=0.10, p2=0.12 → n ≈ 3400 per group (overcalculated due to wrong z=2.33)
Correct answer should be ~1764 (using z_alpha=1.96, z_beta=0.84)

---

This document is retained for historical reference only. All active experiments
must use the current runbook v2 (docs/ab_testing_runbook.md).
