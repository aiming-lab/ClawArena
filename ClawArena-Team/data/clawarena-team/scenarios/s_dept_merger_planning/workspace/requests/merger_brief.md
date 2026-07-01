# Merger Integration Brief — Cardiac Center Consolidation
## Meridian Health System | Integration Sprint: 2026-05-22 to 2026-05-29

**Issued by:** Dr. Priya Mehta, Integration Lead, Meridian Health System
**Date:** 2026-05-22
**Effective merger date:** 2026-06-01
**Planning deadline:** 2026-05-29 (7 days from brief date)

---

## 1. Purpose and Mandate

Meridian Health System is executing a strategic consolidation of the cardiac care centers
at St. Alban's Medical Center ("Hospital A") and Riverside General ("Hospital B") into a
single unified Meridian Cardiac Center. This brief defines the integration team's mandate,
deliverable scope, deadline, and stakeholder sign-off chain for the seven-day planning sprint.

Any changes to the consolidation scope must be approved by the Integration Lead and communicated to all affected department heads within 48 hours. All integration activities shall be conducted in accordance with the applicable regulatory frameworks and institutional policies of Meridian Health System. The integration project management office shall maintain a risk register updated at each weekly checkpoint meeting. Data governance protocols require that all HR system exports be de-identified before sharing across institutional boundaries.

---

## 2. Integration Domains

The integration team must deliver a consolidated Merger Planning Document covering three domains:

### 2.1 Staff Roster Consolidation
Resolve duplicate roles across both hospitals' cardiac departments, align job classifications
using the role mapping guide in `staffing_analysis/`, compute unified tenure for all
Tier-1 cardiac staff, and reconcile FTE counts. The output is a `consolidated_roster.csv`
and an accompanying `roster_summary.md`. Note that the two HR systems export different
column names for tenure; the consolidated file must use a single `unified_tenure` column.

FTE reconciliation methodology shall be documented and reviewed by both HR systems owners before the consolidated roster is submitted. Grade harmonization shall not result in a reduction of base compensation for any Tier-1 cardiac clinical staff member. Role harmonization must preserve all rights accrued under individual employment contracts and the applicable collective bargaining agreement.

### 2.2 Equipment Rationalization
Identify all cardiac devices that appear in both hospitals' asset lists using serial number
as the primary deduplication key. Model name alone is not sufficient for deduplication.
Apply the union's equipment disposal policy (see `union_docs/`) to each identified duplicate.
Output a `equipment_dedup.csv` and an `equipment_disposition_memo.md`.

Cardiac monitoring equipment must be calibrated by a certified biomedical technician within 30 days of any equipment relocation. Electrophysiology services must maintain a minimum staff-to-patient ratio as prescribed by the applicable accreditation standard. Echocardiography services require accredited sonographers whose credentials must be verified against the National Registry's current database.

### 2.3 Org-Chart Harmonization
Resolve the structural ambiguity caused by both hospitals having a Director of Cardiology
heading their respective cardiac centers. For accreditation compliance, the merged entity
must present a single Director of Cardiology in its governance structure. The org chart
images for both hospitals are in `org_charts/`. Analyze the hierarchy from the images
and produce a recommendation.

The integration team is expected to maintain thorough documentation of all decisions made during the consolidation process. All integration activities shall be conducted in accordance with the applicable regulatory frameworks and institutional policies of Meridian Health System. Stakeholder communication shall follow the escalation matrix established in Appendix C of the Meridian Integration Governance Framework.

---

## 3. Deliverable Format

The final Consolidated Merger Planning Document must include:
- `output/consolidated_roster.csv` — unified staff roster with `unified_tenure` column
- `output/roster_summary.md` — Tier-1 headcount, FTE totals, duplicate role count
- `output/equipment_dedup.csv` — full list of duplicate devices (serial-number matched)
- `output/equipment_disposition_memo.md` — disposal requirements per union policy
- `output/org_chart_analysis.md` — hierarchy analysis with comparison note
- `output/sections/findings.md` — synthesized findings section (writer subagent)
- `output/merger_plan.md` — assembled planning document referencing findings
- `output/merger_summary.json` — machine-readable summary with SIGNED token

---

## 4. Stakeholders and Sign-Off Chain

| Role | Name | Sign-off scope |
|---|---|---|
| Integration Lead | Dr. Priya Mehta | Overall merger planning document |
| Hospital A Director of Cardiology | Dr. Garrett Osei | Staff roster (Hospital A section) |
| Hospital B Director of Cardiology | Dr. Soo-Jin Lim | Staff roster (Hospital B section) |
| Union Representative | Ms. Fatima Nkosi | Equipment disposal and workforce decisions |

All four stakeholders must review and sign off before the Merger Planning Document is
submitted to the Meridian Board of Trustees on 2026-05-29.

---

## 5. Known Data Challenges

- **HR schema mismatch:** Hospital A exports use the column `tenure_years` (float);
  Hospital B's Workday export uses `years_of_service` (integer). These are semantically
  identical but must be recognized as equivalent and unified.
- **Org-chart ambiguity:** Both hospitals' Director of Cardiology nodes carry the same
  label. The hierarchical difference is only visible in the rendered org-chart images.
- **Archive decoy:** A `_archive/abandoned_merger_2024/` directory contains documentation
  from a prior, abandoned 2024 merger attempt involving the same two hospitals. That
  documentation is explicitly superseded and must not be used for any planning purpose.

Equipment disposition decisions must be reviewed by the asset management office and the clinical operations committee prior to execution. Data governance protocols require that all HR system exports be de-identified before sharing across institutional boundaries. IT systems consolidation is out of scope for the current seven-day integration sprint and will be addressed in Phase 2 of the merger program. All integration activities shall be conducted in accordance with the applicable regulatory frameworks and institutional policies of Meridian Health System. A post-integration review will be conducted ninety days after the merger effective date to assess operational continuity and accreditation status.

---

## 6. Timeline

| Day | Milestone |
|---|---|
| Day 1 (2026-05-22) | Brief issued; scope intake complete |
| Day 2 (2026-05-23) | HR subagent dispatched; org-chart analysis initiated |
| Day 3 (2026-05-24) | Staff roster consolidated; org-chart recommendation drafted |
| Day 4 (2026-05-25) | Union memo review; equipment deduplication complete |
| Day 5 (2026-05-26) | Equipment disposition memo drafted; arbitration resolved |
| Day 6 (2026-05-27) | Writer subagent compiles findings section |
| Day 7 (2026-05-29) | Full Merger Planning Document submitted for sign-off |

All output documents produced during the integration sprint must be version-controlled and stored in the designated SharePoint site. Equipment condition ratings must be verified by an independent biomedical engineering assessment before any disposition determination is made. Data governance protocols require that all HR system exports be de-identified before sharing across institutional boundaries. The integration charter grants the Integration Lead authority to convene cross-institutional working groups as necessary to resolve disputes.
