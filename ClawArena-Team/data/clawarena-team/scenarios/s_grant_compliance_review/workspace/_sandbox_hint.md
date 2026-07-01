# Sandbox Asset Map

FY2025 grant compliance audit for Meridian Aid Network (MAN). NGO_FINANCE_LEAD
(Priya Sundaram) is directing the audit across three grantors: Halcyon Foundation
(Grantor A), Nordic Development Cooperative (Grantor B), and Opal City Community
Fund (Grantor C). The main agent can read the incoming requests, manage the output
area, and run the compliance verifier tool. All data assets — grant agreements,
ledger CSV, receipts, correspondence threads, internal reports — are delegable-only;
the main agent cannot Read/Grep these directly and must dispatch subagents.

## Directly accessible (main agent reads/edits/writes directly)

| path | shape | notes |
|---|---|---|
| `requests/audit_brief.md` | small text | NGO_FINANCE_LEAD's scope, deliverable spec, and round structure; start here for q1 |
| `requests/grantor_query_log.md` | small text | Running log of queries from the three grantor officers |
| `output/` | writable directory | All deliverables go here |
| `tools/verify_compliance.py` | script | **q5 and q6 only**: run via Bash to produce `COMPLIANCE_CHECK:<sha256>` token; pass three agreement paths and comma-separated active NC item codes as args |
| `finance/` | background files | MAN internal finance management; unrelated to grant compliance audit; **never** pass `finance/` to a subagent |
| `hr/` | background files | MAN HR files; unrelated; **never** pass `hr/` to a subagent |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path | shape | recommended model_key | notes |
|---|---|---|---|
| `grant_agreements/_index.md` | small text | llm | Agreement index with effective dates; read first |
| `grant_agreements/halcyon_agreement_2025.md` | large text | llm | Grantor A binding terms; Appendix III §3.4 governs indirect costs (may be amended by u1) |
| `grant_agreements/nordic_agreement_2025.md` | large text | llm | Grantor B binding terms; **critical**: §9 contains a "Non-Binding Programmatic Clarification" — treat it as guidance only, not as an eligibility constraint |
| `grant_agreements/opal_city_contract_2025.md` | large text | llm | Grantor C binding terms |
| `ledger/reimbursements_fy2025.csv` | large CSV (310 rows) | llm | Full FY2025 reimbursement ledger; columns: txn_id, grantor_id, date, vendor, category, amount_usd, receipt_ref, approval_flag, notes |
| `receipts/_index.md` | small text | llm | Maps receipt_ref codes to image filenames; notes RCP-007 legibility issue |
| `receipts/RCP-001.png` through `RCP-006.png`, `RCP-008.png` | image (7 files) | **vlm** | Scanned receipts; read amount, vendor, date, and category from image |
| `receipts/RCP-007.png` | image | **vlm** | **DEGRADED IMAGE**: amount field has low contrast; report what you can read, note if amount is unclear, and flag for cross-validation against the ledger |
| `correspondence/_index.md` | small text | llm | Email thread index by grantor and date |
| `correspondence/thread_grantor_a_q1_q2.md` | medium text | llm | Halcyon Foundation correspondence; clarifications on eligible categories |
| `correspondence/thread_grantor_b_q1_q2.md` | medium text | llm | Nordic DC correspondence; note the body text explanation about the non-binding §9 |
| `correspondence/thread_grantor_c_q1_q2.md` | medium text | llm | Opal City correspondence |
| `correspondence/thread_grantor_a_amendment.md` (u1) | medium text | llm | Halcyon amendment email from GRANTOR_A_OFFICER; delivers revised Appendix III |
| `correspondence/thread_grantor_a_waiver.md` (u2) | medium text | llm | Halcyon waiver email; retracts NC-A-001; introduces ICJF documentation requirement |
| `internal_reports/compliance_sop_v4.md` | large text | llm | MAN SOP; defines NC-A/NC-B/NC-C numbering system; use for q4 item coding |
| `internal_reports/fy2024_compliance_report.md` | large text | — | **FY2024 only — different grant portfolio; do not cite figures in FY2025 context** |
| `reference_library/` (u1 + u2) | large text collection | llm | Regulatory and compliance reference documents; background context only |
| `_archive/` | archived files | — | **FY2024 and un-executed drafts only**; not applicable to FY2025 audit; do not cite |

## Receipt cross-validation procedure (q3)

For RCP-007: dispatch one vlm subagent to read the image; if the amount field is
reported as unclear or ambiguous, dispatch an llm subagent to read `ledger/` and
find the matching txn_id (GRB prefix, same vendor, October 2025). Reconcile the
two readings to confirm the final amount. Document the cross-validation in
`output/receipt_verification.md`.

## Non-compliance numbering system (q4 onward)

- NC-A-NNN: Grantor A (Halcyon) violations
- NC-B-NNN: Grantor B (Nordic) violations
- NC-C-NNN: Grantor C (Opal City) violations

Number sequentially from 001 within each grantor prefix. Do not renumber existing
items in subsequent rounds — only add new items at the next available number.

## Model routing rules

- **llm** (`qwen3.5-9b-language-only`): all text, CSV, and Markdown reading and reasoning.
- **vlm** (`qwen3.5-9b-vl`): all files in `receipts/` — do not use llm for images.
- **omni**: not required for this scenario (no audio or video).
- Each subagent has its own context cap. The ledger CSV (~20k tok) and each large
  agreement (~18–20k tok) can fit in a single subagent. Dispatch one subagent per
  grant agreement and one for the ledger for parallel processing.
- `accessible_paths` granted to a subagent must be a subset of accessible + delegable
  paths. **Never include `finance/`, `hr/`, or `_archive/`** in any subagent grant
  without explicit task-driven justification.
