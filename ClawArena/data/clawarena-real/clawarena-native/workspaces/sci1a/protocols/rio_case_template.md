# RIO Case Report Template

**Template ID**: RIO-TPL-001
**Version**: 3.0
**Mandatory sections**: All four sections below must be present in every formal case report.

---

## Required Report Structure

Every formal RIO case report MUST contain the following four sections in order:

### Section 1: Background
- Case ID and date opened
- Brief description of the concern and how it was identified
- Papers/researchers involved
- Institutional context

### Section 2: Evidence
- Summary of image analysis or data analysis results
- Cross-reference to supporting files (TSV, JSON, etc.)
- Conflict resolution where multiple sources provide different figures
- Key numerical anchors with source citations

### Section 3: Classification
- COPE classification type (Type 1/2/3/4)
- Severity assessment
- Scope of affected work (how many papers, what findings are compromised)

### Section 4: Recommendation
- Recommended action (retraction / correction / expression of concern / no action)
- Timeline for implementation
- Notification requirements (NIH, journals, co-authors)

---

## File Naming Convention

All formal report files MUST follow the format:
`YYYY-MM-DD_caseid_type.md`

Examples:
- `2024-01-02_dfci_preliminary.md`
- `2024-01-02_dfci_final_report.md`

Non-compliant file names will be rejected by the RIO case management system.

---

## Executive Summary (Abstract) Requirement

The Abstract / Executive Summary section must not exceed **300 words**.
Word count is enforced by the legal review process.

---

## JSON Deliverables

All JSON outputs must carry a top-level `schema_version: "1.0"` field.
The RIO case-management system rejects untagged files at upload.

---

## Retraction Entry Completeness

Each retracted paper must list **both**:
- The original paper DOI
- The retraction-notice DOI

Co-citing them as a single entry is insufficient for the case record.

---

*Template maintained by RIO Quality Assurance. Contact: rio-admin@university.edu*
