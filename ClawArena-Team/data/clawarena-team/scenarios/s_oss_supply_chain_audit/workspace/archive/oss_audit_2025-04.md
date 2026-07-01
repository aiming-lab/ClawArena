# OSS Supply Chain Audit Report — 2025-04 (SUPERSEDED)
**Status: SUPERSEDED 2025-04**
**This document is from the prior fiscal year audit cycle (April 2025).**
**DO NOT use findings from this report for the current 2026 audit.**

---

## Executive Summary (2025-04 — PRIOR YEAR)

Audit period: 2025-02-01 to 2025-04-30.
Project: Mercator Autonomous Simulation Engine v0.7.x (internal, pre-release).

**Key finding at the time**: lib-tinypath@1.3.8 was identified as having a
moderate severity issue (CVSS 4.2 MEDIUM — CVE-2025-11203) related to path
normalisation. This was remediated by upgrading to 1.3.9.

**IMPORTANT**: The 2025-04 audit finding for lib-tinypath relates to v1.3.8
and CVE-2025-11203 (MEDIUM). The current 2026 audit is concerned with
lib-tinypath@1.4.2 and CVE-2026-21847 (8.7 HIGH) — a completely different
vulnerability in a different version. Do NOT cite the 2025-04 CVE status
as evidence for the 2026 audit.

## CVE Status as of 2025-04 (SUPERSEDED — DO NOT USE)

| Package | CVE | Severity | Status (2025-04) |
|---|---|---|---|
| lib-tinypath@1.3.8 | CVE-2025-11203 | MEDIUM (4.2) | REMEDIATED — upgraded to 1.3.9 |
| colorz@1.9.0 | — | — | Flagged as potential typosquat; under review |

**This table is SUPERSEDED.** Versions, CVEs, and statuses have all changed
since April 2025. Use current SBOM and CVE database exports only.

## Test Coverage (2025-04 — PRIOR YEAR)

At the time of this report, lib-tinypath test coverage was 81% (v1.3.x).
This figure does NOT apply to lib-tinypath v1.4.x used in the current audit.

## Status

SUPERSEDED 2025-04. Retained for compliance archive purposes only.
Refer to the 2026 audit materials for current findings.
