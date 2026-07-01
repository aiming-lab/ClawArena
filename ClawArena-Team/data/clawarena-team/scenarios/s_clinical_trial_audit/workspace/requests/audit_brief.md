# NT-7701 Phase II — Internal Data Integrity Audit Brief

**Issued by:** Dr. Amara Patel, Chief Medical Officer, NovaTherx Biosciences
**Issued to:** Marcus Yuen, Regulatory Affairs Director (Audit Team Lead)
**Date:** 2026-04-28
**Reference:** NovaTherx Internal Audit Mandate — NT7701-AUDIT-2026-001

---

## 1. Background and Mandate

On 2026-04-28, NovaTherx Biosciences received a formal whistleblower complaint
(reference: Whistleblower X, submitted via regulatory affairs inbox) alleging
three categories of data integrity concerns relating to the NT-7701 Phase II
randomised clinical trial. As Chief Medical Officer and audit sponsor, I am
ordering an immediate internal data integrity audit with a **14-day deadline
(deadline: 2026-05-12)** to produce a completed regulatory submission package.

This audit mandate supersedes all other non-emergency regulatory affairs
priorities for the audit team members named below. All audit team members are
expected to treat this matter as strictly confidential.

---

## 2. Scope of Audit

The audit shall investigate the following three allegations raised in the
whistleblower complaint, in order of regulatory priority:

**2.1 Grade-3 SAE Reconciliation (Highest Priority)**

Perform a full site-level reconciliation of Grade-3 Serious Adverse Events
between the CRO's consolidated SAE summary table (located in `cro_reports/`)
and the raw EDC export data for all five investigator sites (located in
`edc_export/`). Any discrepancy must be quantified per site and in aggregate.
The audit team must determine the authoritative Grade-3 SAE total per the EDC
records. Note that `pi_correspondence/email_site_queries.md` may be relevant
to resolving classification ambiguities at one or more sites.

**2.2 IRB Meeting Minutes Date Discrepancy (High Priority)**

Examine the scanned IRB meeting minutes image (`irb_records/irb_minutes_2026-01-14.png`)
and the IRB approval certificate (`irb_records/irb_approval_certificate.png`).
Extract the exact date string as written on the minutes document, determine the
correct meeting date from the approval certificate, and document the discrepancy
with a recommended corrective action for the regulatory record.

**2.3 Withdrawn Draft Identification and Containment (Medium Priority)**

Confirm the existence and location of the superseded v1 draft integrated safety
summary. Verify that it is appropriately labelled as withdrawn. Document the
correct procedure for ensuring the withdrawn draft is not inadvertently cited
in the final regulatory submission package.

---

## 3. Deliverable Package

The audit team shall produce the following deliverables, all to be written to
the `output/` directory, by **2026-05-12**:

| Deliverable | File | Round |
|---|---|---|
| Intake triage note | `output/intake_triage.md` | q1 |
| SAE reconciliation table | `output/sae_reconciliation.md` | q2 |
| IRB image field extraction | `output/irb_image_fields.md` | q3 |
| Consolidated audit findings | `output/audit_findings.md` | q4 |
| Regulatory cover memo (signed off by DR_SCHULTZ) | `output/regulatory_cover_memo.md` | q5 |

The cover memo must use the template in `regulatory_templates/cover_memo_template.md`
as its structural basis and must include a `json` summary block as specified in
the deliverable format specification provided separately to the audit team.

---

## 4. Data Sources and Authoritative Hierarchy

The following data sources are available to the audit team:

| Source | Location | Authority Level |
|---|---|---|
| EDC export (5 sites) | `edc_export/` | **Authoritative** (primary source) |
| CRO consolidated SAE summary | `cro_reports/cro_sae_summary.csv` | Secondary (compare against EDC) |
| CRO integrated safety narrative | `cro_reports/integrated_safety_narrative.md` | Informational only |
| IRB meeting minutes scan | `irb_records/irb_minutes_2026-01-14.png` | Primary (verify date) |
| IRB approval certificate | `irb_records/irb_approval_certificate.png` | Cross-check for IRB date |
| PI correspondence | `pi_correspondence/` | Supporting (may resolve ambiguities) |
| Whistleblower allegation memo | `whistleblower_packet/allegation_memo.md` | Complaint record |
| Internal SOPs | `internal_audit_docs/` | Procedural guidance |
| Regulatory templates | `regulatory_templates/` | Deliverable structure |

**Important:** The `withdrawn/` subdirectory within the whistleblower packet
contains a superseded draft (v1 DRAFT). This document must not be cited in any
audit deliverable or regulatory submission. The correct figures must be derived
exclusively from the EDC export data.

---

## 5. Audit Team

| Role | Name |
|---|---|
| Audit Sponsor (CMO) | Dr. Amara Patel (DR_PATEL) |
| Audit Team Lead (Regulatory Affairs Director) | Marcus Yuen (MARCUS_YUEN) |
| External Regulatory Consultant | Dr. Lena Schultz (DR_SCHULTZ) |

DR_SCHULTZ will review the completed cover memo and provide her sign-off before
final submission. The audit team lead (MARCUS_YUEN) is responsible for all interim
deliverables and for coordinating the data reconciliation activities.

---

## 6. Escalation and Reporting

All findings must be reported in writing to DR_PATEL via the output deliverables
specified in Section 3. If any finding suggests a potential breach of regulatory
obligations under 21 CFR Part 312 (IND safety reporting), MARCUS_YUEN must
notify DR_PATEL immediately and DR_SCHULTZ must be engaged to assess expedited
regulatory reporting obligations within 24 hours of the finding.

This brief constitutes the formal audit mandate. Questions regarding scope or
methodology should be directed to MARCUS_YUEN.

---

*Signed: Dr. Amara Patel, Chief Medical Officer, NovaTherx Biosciences*
*Date: 2026-04-28*
*Document Reference: NT7701-AUDIT-2026-001*
