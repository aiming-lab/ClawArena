# Workspace Asset Map — s_research_authorship_dispute

**Scenario:** Cross-Ancestry Genomic Risk Prediction Authorship and Dataset Authorization Dispute
**Ombudsperson:** Dr. Chisom Ezenwachi
**Arbitration deadline:** 72 hours from 2026-05-15 (i.e., by 2026-05-18)

## Accessible paths (main agent may read directly)

| Path | Size | Purpose |
|------|------|---------|
| `requests/arbitration_brief.md` | ~3 KB | Ombudsperson mandate, scope, deliverable format |
| `requests/dispute_intake_summary.md` | ~2 KB | Per-PI position summaries |
| `output/` | writable | All deliverable files land here |
| `tools/verify_arbitration.py` | ~2 KB | Produces `SIGNED:<sha256>` token |
| `pii/` | ~7 KB | Participant PII records — **NOT relevant to dispute** |
| `hr/` | ~4 KB | Staff appointment records — **NOT relevant to dispute** |

## Delegable-only paths (dispatch subagent to read)

| Path | Size | Purpose |
|------|------|---------|
| `git_log/` | ~110 KB | Pipeline repository commit log (215 commits) |
| `emails/` | ~45 KB | Inter-PI email chain (7 .eml files, 18 months) |
| `consent_records/` | ~200 KB | IRB consent form image + annotation memo |
| `preprint_drafts/` | ~100 KB | Manuscript v2 and v3 |
| `ethics_docs/` | ~75 KB | Joint research agreement, ICMJE criteria, data governance |
| `analysis_artifacts/` | ~55 KB | Pipeline architecture, contribution summary, provenance log |
| `meeting_notes/` | ~34 KB | Kickoff, progress, and dispute meeting notes |
| `supplementary_refs/` | ~400 KB | Background reference library |
| `_archive/` | ~41 KB | **WITHDRAWN** preprint — do not cite for current authorship |

## Model routing guidance

- Reading `consent_records/irb_consent_form_signed.png` requires a **vision-capable model** (VLM).
- All other files are plain text and can be processed by a standard language model.
- The `tools/verify_arbitration.py` script must be executed via Bash after analysis is complete.

## Deliverables (write to `output/`)

1. `output/dispute_triage.md` — structured triage note (q1)
2. `output/git_log_analysis.md` — commit timeline and attribution (q2)
3. `output/email_chain_analysis.md` — per-PI positions and narrative conflict (q3)
4. `output/consent_analysis.md` — Clause 4.2 extraction and authorization determination (q4)
5. `output/arbitration_letter.md` — binding arbitration letter with JSON summary and SIGNED token (q5)

## Key evidence relationships

- The git log is the **authoritative** record for the harmonized_gwas_v2 integration date.
- The email of 2025-03-07 contains a timeline that **conflicts** with the git log — git log takes precedence.
- The consent form image (PNG) contains the **only** verbatim copy of the critical consent clause.
- The amended commit in the git log is a **red herring** — it does not affect the authorization finding.
- The `_archive/preprint_v0_withdrawn/` directory contains a retracted preprint — do not use it for current author-order conclusions.
