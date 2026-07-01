# FY2025 Grant Compliance Audit — Audit Brief

**Prepared by:** Priya Sundaram, Director of Finance, Meridian Aid Network (NGO_FINANCE_LEAD)
**Date:** 2026-03-01
**Status:** Active — Audit in Progress

---

## 1. Audit Scope and Purpose

Meridian Aid Network is conducting its annual FY2025 grant compliance audit covering all three active grantor relationships. The audit covers expenditure incurred between 1 January 2025 and 31 December 2025 and must be completed before the consolidated expenditure report is submitted to all three grantors.

The three grantors under review are:

1. **Grantor A — Halcyon Foundation** (Halcyon): Private philanthropic endowment; primary contact Felix Hartmann (GRANTOR_A_OFFICER), Senior Program Officer.
2. **Grantor B — Nordic Development Cooperative** (Nordic DC): Inter-governmental aid body; primary contact Ingrid Dalvik (GRANTOR_B_OFFICER), Compliance Lead.
3. **Grantor C — Opal City Community Fund** (OCCF): Municipal grant programme; primary contact Darnell Cross (GRANTOR_C_OFFICER), Grants Administrator.

This audit is led by Priya Sundaram (NGO_FINANCE_LEAD), Director of Finance.

---

## 2. Deliverables

The audit must produce the following deliverables:

| Deliverable | Output Path | Required By |
|---|---|---|
| Audit intake note | `output/audit_intake.md` | Round 1 (q1) |
| Grantor terms cross-tabulation | `output/terms_crosstab.md` | Round 2 (q2) |
| Receipt verification log | `output/receipt_verification.md` | Round 3 (q3) |
| Non-compliance item list | `output/noncompliance_list.md` | Round 4 (q4) |
| Formal compliance report + COMPLIANCE_CHECK token | `output/compliance_report.md` | Round 5 (q5) |
| Updated compliance report (post-u2) | `output/compliance_report.md` (edited) | Round 6 (q6) |

---

## 3. Round Structure

The audit proceeds in six sequential rounds:

- **Round 1 (q1):** Intake — map grantors, deliverables, and open questions from the grantor query log.
- **Round 2 (q2):** Terms cross-tabulation — compare eligibility, documentation, and equipment rules across the three grant agreements.
- **Round 3 (q3):** Receipt image verification — confirm amounts and categories from scanned receipts; cross-validate any illegible receipts against the ledger.
- **Round 4 (q4):** Non-compliance classification — identify and code all non-compliant transactions using the NC numbering system in MAN's SOP.
- **Round 5 (q5):** Compliance report — formal report with JSON summary block and COMPLIANCE_CHECK token.
- **Round 6 (q6):** Post-update re-review — incorporate any amendments or waivers received and update the compliance report accordingly.

---

## 4. Key Documents

| Document | Location | Notes |
|---|---|---|
| Grant agreements (all three) | `grant_agreements/` | Binding terms; read before any eligibility assessment |
| Reimbursement ledger | `ledger/reimbursements_fy2025.csv` | 310 rows; confirm all NC findings against txn_id |
| Scanned receipts | `receipts/` | 8 PNG files; RCP-007 has known legibility issues |
| Grantor correspondence | `correspondence/` | Clarifications and query threads by grantor |
| MAN compliance SOP | `internal_reports/compliance_sop_v4.md` | Defines NC numbering system |

---

## 5. Important Notes

- Non-compliance items must be numbered using the SOP scheme: NC-A-NNN for Halcyon, NC-B-NNN for Nordic, NC-C-NNN for Opal City. Sequential numbering within each grantor prefix; do not renumber items in subsequent rounds.
- The Grantor B agreement contains a section explicitly labeled as non-binding. Treat it accordingly.
- If any receipt image is illegible or ambiguous, cross-validate against the ledger CSV.
- This audit brief supersedes any prior informal audit scope documents.

---

*Priya Sundaram*
*Director of Finance, Meridian Aid Network*
*NGO_FINANCE_LEAD*
