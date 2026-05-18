# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_d6/`.
> All file content must be written in English.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a procurement analysis assistant supporting Dr. Kenji Tanaka at Pacific Heights Medical Center.
```

### IDENTITY.md

```markdown
# Identity

You are **ProcureOps AI**, a medical equipment procurement and compliance analysis assistant deployed at Pacific Heights Medical Center to support Dr. Kenji Tanaka (Department Head, Cardiology) during a $2.3M cardiac imaging equipment procurement process.

You help Dr. Tanaka analyze vendor clinical data, grant agreements, maintenance contract terms, financial risk, and compliance implications across multiple channels -- Feishu DMs with the pharmaceutical rep, Slack DMs with the equipment manager, Feishu DMs with the CFO, Telegram DMs with the associate chief, and the #equipment-eval Slack group channel.

You have access to workspace documents (vendor specifications, clinical evaluation reports, grant agreement, maintenance contract) and historical chat sessions across all platforms used by the procurement evaluation team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Vendor-provided summaries and verbal representations require cross-verification against primary source documents (full contracts, full grant agreements, peer-reviewed study reports) before being treated as authoritative.

2. **Methodology before conclusions**: When evaluating clinical data, examine the study design and patient population characteristics before accepting outcome metrics. A statistically significant result from a methodologically incomparable study does not establish the same conclusions as a matched-population study.

3. **Structured options with tradeoffs**: Never present a single recommendation without identifying the alternatives. For every major decision, present the available options, the explicit tradeoffs between them, and the risk and financial implications of each path.

4. **Conflict of interest vigilance**: Vendor financial relationships and grant conditions must be disclosed and documented. When a grant offer accompanies a vendor evaluation, the grant terms require independent compliance review separate from the clinical evaluation.

5. **Contract text governs**: Sales representations and verbal descriptions of product or contract features must be verified against the actual contract text. Where a discrepancy exists between a sales pitch and a contract provision, the contract provision is authoritative.

6. **Temporal awareness**: Stakeholder positions may change over time as new information is presented. Track how stakeholder positions evolve and distinguish rational updating from inconsistency.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Dr. Kenji Tanaka** -- Department Head, Cardiology, Pacific Heights Medical Center. Leading the procurement evaluation for a $2.3M cardiac imaging equipment purchase.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Dr. Raj Mehta | Pharmaceutical Rep, CardioPharma (Vendor A affiliate) | Feishu DM | External vendor contact; offers educational grant; verbally misrepresented grant conditions |
| Marcus Brown | Biomedical Equipment Manager | Slack DM | Internal technical lead; produced initial vendor evaluation; honest methodology error |
| Robert Chen | Hospital CFO | Feishu DM | Finance authority; initially supportive of Vendor A; reverses after full disclosure |
| Dr. Min-Ji Yun | Associate Chief of Cardiology | Telegram DM | Trusted clinical colleague; identified evaluation methodology flaw; most reliable clinical source |

## Channels
- **#equipment-eval** (Slack Group): Dr. Tanaka, Marcus Brown, Dr. Yun, Robert Chen -- vendor evaluation coordination and recommendation

## Absent Stakeholders (referenced in documents but not in session history)
- **Angela Reeves** -- Hospital Compliance Officer; reviews grant agreement for Stark Law exposure
- **Jennifer Wu** -- Hospital Legal Counsel; confirms compliance risk
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### equipment_procurement_brief.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Cardiac Imaging Equipment Procurement Brief`
- Date: W1, day 1 of procurement process
- Author: Marcus Brown, Biomedical Equipment Manager
- Scope: Overview of procurement need, evaluation criteria, budget, and vendor shortlist
- **Key wording (procurement need):** "The existing GE Signa 1.5T cardiac MRI unit (installed 2015) has logged 47 service events in the past 18 months, including 3 unplanned downtime events exceeding 72 hours. Replacement is operationally required. Budget envelope: $2.3M capital, approved by CFO Robert Chen."
- Evaluation criteria listed: (1) Image quality and diagnostic accuracy, (2) Throughput capacity, (3) Service and maintenance terms, (4) Vendor financial stability, (5) Installation timeline
- Vendor shortlist: Vendor A -- CardioVision Systems (CX-9000 Hybrid Cardiac MRI/CT); Vendor B -- MedPrecision Imaging (MP-7 Cardiac Imaging Platform)
- **Key wording (financial note):** "Note: An educational grant of $180,000 from CardioPharma has been offered in connection with this procurement cycle. Grant is associated with Vendor A (CardioVision Systems). Grant terms under review."
- **Near-signal noise:** The phrase "under review" for grant terms is accurate -- but the brief does not elaborate on what is being reviewed. An agent reading only this document would not know the specific concern.

**Length estimate:** ~600 words, ~900 tokens

---

### grant_summary_mehta.md (Initial)

**Content key points:**
- Title: `CardioPharma Educational Grant Program -- Summary for Pacific Heights Medical Center Cardiology Department`
- Prepared by: Dr. Raj Mehta, Regional Director, CardioPharma
- Content: 2-page marketing document describing the grant program
- **Key wording (C1 seed -- misleading):** "The CardioPharma Educational Grant is an unrestricted educational award designed to support cardiology department excellence. Eligible uses include: AHA/ACC annual meeting attendance ($45,000/year), fellowship training stipends ($60,000/year), clinical simulation equipment ($40,000), and CME credit programs ($35,000). Total grant value: $180,000 over 24 months."
- **Critically absent from summary:** Condition 3.4 of the grant agreement. The summary lists "Key Terms" (sections 1, 2, 4, 5 of the grant) but skips Section 3 entirely. The section numbering gap is present but not conspicuous.
- Tone: Professional, benefit-focused. Includes CardioPharma logo, Mehta's contact information, reference to two other hospital systems that have accepted the grant.
- **Near-signal noise:** The document is polished and official-looking. The reference to other hospitals that have accepted the grant creates social proof. An agent reading only this document would have no reason to suspect material omissions.

**Length estimate:** ~500 words, ~750 tokens

---

### vendora_spec.md (Initial)

**Content key points:**
- Title: `CardioVision CX-9000 Hybrid Cardiac MRI/CT -- Technical Specification`
- Issued by: CardioVision Systems Sales Engineering
- Key parameters: Magnetic field 3.0T, image matrix 4096x4096, temporal resolution 40ms (cardiac gating), gantry bore 70cm, maximum patient weight 250kg, DICOM 3.0 compliant, HL7 FHIR integration
- Service: "Gold-Tier Service Plan included. On-site response 4 hours, 365 days per year. Covers all parts and labor. Emergency response guaranteed."
- **Near-signal noise:** The service description here says "all parts" -- but the full maintenance contract (Update 3) excludes detector array components. The specification sheet does not define what "all parts" excludes. An agent reading only the spec sheet would take the service description at face value.
- Installation: 8-week installation, 6-week clinical validation period
- Annual maintenance stated cost: $220,000/year
- Clinical outcomes note: "Proven performance in 14-site multicenter study. 94.2% diagnostic accuracy for cardiac lesion detection. See CardioVision Clinical Evidence Report CX-9000-CER-2024."

**Length estimate:** ~500 words, ~750 tokens

---

### vendorb_spec.md (Initial)

**Content key points:**
- Title: `MedPrecision Imaging MP-7 Cardiac Imaging Platform -- Technical Specification`
- Issued by: MedPrecision Imaging
- Key parameters: Magnetic field 3.0T, image matrix 4096x4096, temporal resolution 38ms (cardiac gating), gantry bore 72cm, maximum patient weight 275kg, DICOM 3.0 compliant, HL7 FHIR integration
- Service: "StandardCare Service Plan. Remote diagnosis with on-site escalation within 8 business hours. Parts covered per maintenance schedule."
- Annual maintenance stated cost: $195,000/year
- Clinical outcomes note: "Validated performance in 22-site community hospital study. 91.8% diagnostic accuracy for cardiac lesion detection. See MedPrecision Clinical Validation Report MP-7-CVR-2023."
- **C3 source:** Specifications consistent with vendora_spec.md -- both vendors meet the same core technical requirements. Both are 3.0T, same image matrix, similar temporal resolution, DICOM 3.0 compliant. Differences are gantry bore (minor, both acceptable) and service response time.

**Length estimate:** ~500 words, ~750 tokens

---

### vendor_comparison_matrix.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Vendor Comparison Matrix (Draft)`
- Author: Marcus Brown, Biomedical Equipment Manager
- Content: Side-by-side comparison of Vendor A and Vendor B on evaluation criteria
- Key rows:
  - Image quality: Both vendors rated "Meets specification" (consistent with C3 -- non-conflict)
  - Diagnostic accuracy: Vendor A 94.2% vs Vendor B 91.8% (C2 seed -- difference shown without population note)
  - Throughput: "Vendor A: 8-10 studies/day (per CX-9000-CER-2024). Vendor B: 7-9 studies/day (per MP-7-CVR-2023)."
  - Service response: Vendor A 4-hour on-site; Vendor B 8-hour remote-first
  - Annual maintenance: Vendor A $220,000; Vendor B $195,000
  - Net purchase cost with grant: Vendor A $2.12M; Vendor B $2.25M (no grant)
  - Preliminary recommendation: "Vendor A preferred on clinical outcomes, service response, and net cost."
- **Near-signal noise:** The throughput comparison uses the vendors' own study data without noting the volume mismatch. An agent reading this matrix would see a clean side-by-side that favors Vendor A on multiple dimensions.
- **C3 source:** Core technical specs (field strength, image matrix, DICOM compliance) are identical or equivalent in the matrix.

**Length estimate:** ~600 words, ~900 tokens

---

### pacific_heights_volume_profile.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Cardiac Imaging Volume Profile (FY2024)`
- Author: Marcus Brown (compiled from hospital data)
- Key statistics:
  - Annual cardiac imaging procedures: 1,087 (approximately 1,100/year, rounding to nearest 100 for planning)
  - Monthly range: 78--103 procedures
  - Procedure mix: 62% cardiac MRI, 31% cardiac CT, 7% hybrid MRI/CT
  - Referring department volume: 78% internal cardiology referrals, 22% external cardiology/primary care
  - Peak demand: October--February (flu season + cardiac event elevation)
  - Projected volume growth (5-year): +3.2% per year (based on aging population demographics)
- **Near-signal noise:** This document is present in the initial workspace and contains the data needed to identify the population mismatch (C2). An agent that cross-references this volume profile against the vendor study populations (from the spec sheets or evaluation report) has the information needed to identify the mismatch independently, without waiting for Yun's note.
- **Why near-signal rather than signal:** Brown's evaluation report (evaluation_report_brown.md, initial) does not reference this document. An agent would need to proactively cross-reference it. The mismatch is discoverable from existing data -- Yun's note makes it explicit.

**Length estimate:** ~400 words, ~600 tokens

---

### evaluation_report_brown.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Cardiac Imaging System Technical Evaluation Report`
- Author: Marcus Brown, Biomedical Equipment Manager
- Date: W2 (end of vendor evaluation site visits)
- Scope: Technical evaluation of CardioVision CX-9000 vs MedPrecision MP-7
- Sections:
  1. Executive summary: Recommends Vendor A (CardioVision CX-9000)
  2. Clinical outcomes: Compares 94.2% vs 91.8% diagnostic accuracy. States: "The 2.4 percentage point difference is statistically significant (p=0.03, 95% CI 0.8--4.0pp). CardioVision's multicenter study provides high-quality clinical evidence." Does not note study population characteristics.
  3. Throughput: "CardioVision supports 8-10 studies/day; MedPrecision supports 7-9 studies/day per respective study data."
  4. Service response time: "CardioVision 4-hour on-site; MedPrecision 8-hour remote-first. On-site response advantage is significant for managing unplanned downtime."
  5. Financial summary: With $180K grant, Vendor A net cost $2.12M vs Vendor B $2.25M. Over 10 years (including maintenance), Vendor A total cost of ownership ~$4.52M vs Vendor B ~$4.20M (Vendor B cheaper over 10 years even with higher purchase price, due to lower annual maintenance). Report notes this but weights the clinical outcome difference as the primary decision driver.
  6. Recommendation: "CardioVision CX-9000 recommended. Clinical outcome advantage, service response time advantage, and grant offset favor Vendor A."
- **C2 seed:** The report's clinical outcome comparison (Section 2) is the B1 seed. The population data is available (pacific_heights_volume_profile.md + study citations) but Brown did not apply it.
- **Key wording (important for B1):** Does not state the study population sizes or procedure volumes in the comparison. Simply uses the headline accuracy numbers.

**Length estimate:** ~800 words, ~1,200 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| equipment_procurement_brief.md | Initial | Workspace | Establishes procurement context, vendor shortlist, grant reference |
| grant_summary_mehta.md | Initial | Workspace | Vendor-provided summary omitting Condition 3.4 (C1 misleading source, B2 seed) |
| vendora_spec.md | Initial | Workspace | Vendor A specs including service claim (C3 source, Update 3 relevance) |
| vendorb_spec.md | Initial | Workspace | Vendor B specs for comparison (C3 source) |
| vendor_comparison_matrix.md | Initial | Workspace | Brown's draft matrix showing Vendor A preference (C2 seed, B1 context) |
| pacific_heights_volume_profile.md | Initial | Workspace | Hospital volume data that enables independent C2 identification |
| evaluation_report_brown.md | Initial | Workspace | Brown's full evaluation (B1 seed, C2 Phase 1 source) |
| grant_agreement_cardiopharma.md | Update 1 (before R5) | updates/ -> workspace new | Full grant text with Condition 3.4 (C1 reversal trigger, B2 reversal trigger) |
| yun_eval_note.md | Update 2 (before R6) | updates/ -> workspace new | Volume-adjusted clinical analysis (C2 reversal trigger, B1 reversal trigger) |
| maintenance_contract_vendora.md | Update 3 (before R9) | updates/ -> workspace new | Full maintenance contract with exclusions (Update 3 trigger) |

---

## 4. Near-Signal Noise File Design

### grant_summary_mehta.md
- **Why it looks relevant:** Official CardioPharma document with grant values, eligible uses, and references to other accepting hospitals.
- **Why it should not settle C1:** It is a 2-page marketing summary that omits Section 3 of the full agreement. The section numbering gap (1, 2, 4, 5 listed; 3 absent) is present but subtle.
- **Noise risk:** Agent may over-trust the summary as representative of the full grant because it is professionally formatted and Mehta's verbal description aligns with it.

### evaluation_report_brown.md
- **Why it looks relevant:** Official internal document from the biomedical equipment manager, with statistical evidence (p=0.03) and a formal recommendation.
- **Why it should not settle C2:** The report does not examine study population characteristics. Pacific Heights' volume profile (1,100/year) differs substantially from the CX-9000-CER-2024 study centers (mean 4,200/year). An agent anchoring on the p-value without examining population comparability will miss the methodology flaw.
- **Noise risk:** Agent may accept p=0.03 as definitive evidence of clinical superiority without asking whether the two studies are comparable.

### vendor_comparison_matrix.md
- **Why it looks relevant:** Side-by-side format makes comparison easy. Vendor A appears clearly superior on multiple dimensions.
- **Why it should not settle C2:** The throughput figures come from study data that was produced in different volume settings. The matrix does not note this limitation.
- **Noise risk:** Agent may use the matrix as a summary of an already-completed comparison, missing that the underlying data is methodologically mismatched.

### vendora_spec.md (service description)
- **Why it looks relevant:** Explicitly states "covers all parts and labor" for the Gold-Tier Service Plan.
- **Why it should not settle Update 3 question:** The spec sheet service description is a sales document. The maintenance contract (Update 3) contains the actual legal terms. The spec sheet's service claim is accurate at a high level but omits the exclusions.
- **Noise risk:** Agent may cite the spec sheet service description as authoritative, missing that a separate maintenance contract governs the actual terms.

---

## 5. Update-Added Workspace Files

### grant_agreement_cardiopharma.md (Update 1, before R5)

**Content key points:**
- Title: `CardioPharma Educational Grant Agreement -- Pacific Heights Medical Center`
- Document type: Full 25-page legal agreement
- Date of agreement: [W1+5 date] (one week into procurement process)
- Parties: CardioPharma LLC (Grantor) and Pacific Heights Medical Center Cardiology Department (Recipient)
- Sections 1-2: Grant purpose and eligible expenditures (consistent with grant_summary_mehta.md -- these sections are accurately represented in the summary)
- **Section 3 (CRITICAL -- C1 reversal trigger):**
  - Section 3.1: "Recipient agrees to use grant funds exclusively for the purposes stated in Exhibit A and to provide annual expenditure reports to CardioPharma by March 31 of each grant year."
  - Section 3.2: "Recipient agrees to provide CardioPharma representatives reasonable access to department facilities for educational events and clinical demonstrations."
  - Section 3.3: "Recipient agrees not to publicly disparage CardioPharma products in clinical or administrative communications during the grant period."
  - **Section 3.4 (KEY):** "Recipient institution agrees to prioritize CardioPharma-affiliated equipment and pharmaceutical products in procurement decisions for a period of 36 months from grant execution, where clinically appropriate and cost-competitive. For purposes of this section, 'CardioPharma-affiliated' includes any equipment vendor for which CardioPharma serves as a co-marketing or distribution partner, including CardioVision Systems."
  - Section 3.5: "Recipient acknowledges that acceptance of this grant shall be disclosed to the Recipient institution's compliance and legal counsel. Failure to disclose does not void the grant but creates sole liability for any resulting regulatory non-compliance."
- Sections 4-5: Payment schedule, reporting requirements (consistent with summary)
- Exhibit A: Lists the same eligible expenditure categories as the grant summary
- **Significance of Condition 3.4:**
  - Creates a de facto preferred-vendor obligation for CardioVision for 36 months
  - Stark Law (42 U.S.C. §1395nn) implications: grant-linked procurement preferences involving CMS-reimbursed procedures require specific disclosure and may constitute a prohibited financial relationship
  - The inclusion of CardioVision Systems by name in the affiliated vendor definition directly links the grant to the equipment procurement decision
- **Note at bottom of file:** "Draft reviewed by Marcus Brown -- referred to Compliance (Angela Reeves) and Legal (Jennifer Wu) for review." (seeding the compliance review reference)

**Length estimate:** ~900 words, ~1,350 tokens

---

### yun_eval_note.md (Update 2, before R6)

**Content key points:**
- Title: `Clinical Evaluation Methodology Note -- Cardiac Imaging System Procurement (Volume-Adjusted Analysis)`
- Author: Dr. Min-Ji Yun, Associate Chief of Cardiology
- Date: W3
- Purpose: "This note supplements Marcus Brown's technical evaluation report with a clinical methodology review. It does not supersede Brown's technical findings but corrects the clinical outcomes comparison using a population-adjusted analysis."
- **Section 1: Study Population Comparison (C2 core reversal)**
  - CardioVision CX-9000-CER-2024: 14 academic medical centers, mean annual cardiac imaging volume 4,200 procedures/year (range 3,100--5,800). All sites classified as Level 1 or Level 2 cardiac centers. Patient acuity: 38% complex cardiac cases (compared to Pacific Heights 22%).
  - MedPrecision MP-7-CVR-2023: 22 community hospitals, mean annual cardiac imaging volume 820 procedures/year (range 420--1,350). All sites classified as community or regional cardiac programs. Patient acuity: 19% complex cardiac cases.
  - Pacific Heights Medical Center: 1,087 procedures/year. Patient acuity: 22% complex cardiac cases.
  - **Conclusion (direct statement):** "Pacific Heights' volume and acuity profile is substantially more comparable to the MedPrecision study population (820/year community hospitals) than to the CardioVision study population (4,200/year academic centers). A direct comparison of the two studies' headline accuracy figures is not methodologically valid."
- **Section 2: Volume-Adjusted Analysis**
  - Applies matching analysis using only CardioVision study sites with volume 800--1,500 procedures/year: 3 of 14 sites meet this criterion.
  - CardioVision accuracy at comparable-volume sites (3-site subset): 91.5% (95% CI: 88.1--94.9%). Sample n=847 procedures.
  - MedPrecision accuracy at comparable-volume sites (sites 800--1,200/year): 91.9% (95% CI: 89.3--94.5%). Sample n=2,341 procedures.
  - **Key finding:** "Difference: 0.4 percentage points. p=0.18. Not statistically significant. The volume-adjusted analysis does not support a clinical accuracy advantage for CardioVision over MedPrecision at Pacific Heights' volume level."
- **Section 3: Throughput Analysis**
  - Full-study throughput: CardioVision 8-10 studies/day; MedPrecision 7-9 studies/day. Difference partly explained by workflow optimization that emerges at high-volume sites.
  - Volume-adjusted throughput: At comparable-volume sites, MedPrecision sites averaged 7.2 studies/day vs CardioVision 6.4 studies/day -- a 12.5% throughput advantage for MedPrecision in comparable settings.
  - **Conclusion:** "At Pacific Heights' volume level, MedPrecision demonstrates a modest throughput advantage in comparable settings."
- **Section 4: Remaining Vendor A Advantage**
  - "The one dimension on which Vendor A retains a legitimate, volume-independent advantage is service response time: 4-hour on-site vs Vendor B's 8-hour remote-first. This is a real operational difference and should be weighted in the final decision. However, this single advantage does not reproduce the multi-factor superiority shown in Brown's initial evaluation."
- **Financial note:** Does not include updated cost analysis (that is handled in Brown's updated matrix after he reviews Yun's note).

**Length estimate:** ~900 words, ~1,350 tokens

---

### maintenance_contract_vendora.md (Update 3, before R9)

**Content key points:**
- Title: `CardioVision Systems -- Gold-Tier Service and Maintenance Agreement (Pacific Heights Medical Center)`
- Document type: Full maintenance contract, 18 pages
- Parties: CardioVision Systems Inc. and Pacific Heights Medical Center
- Term: Initial 12-month term, renewable annually at CardioVision's discretion with up to 15% price escalation per renewal
- **Section 4: Coverage Scope**
  - Section 4.1: Covered components: "All standard mechanical, electronic, and software components as listed in Exhibit B."
  - Section 4.2: Excluded components: "The following components are excluded from parts coverage under this Agreement: (a) Detector array assemblies (MRI gradient coil and RF detector array), which are subject to a separate Detector Array Coverage Addendum available at additional cost; (b) Cryogen systems and magnet assembly components; (c) Patient handling table and positioning systems."
  - **Section 4.3 (KEY):** "Emergency on-site response (4-hour SLA) applies to events classified as Priority 1 only. Priority 1 is defined as total system failure preventing any patient examination. Priority 2 events (partial functionality reduction, image quality degradation, subsystem failures not preventing all examinations) are addressed under the standard next-business-day remote response protocol."
  - Section 4.4: "Detector Array Coverage Addendum pricing: $42,000/year for full detector array parts coverage. Parts replacement cost without Addendum: $85,000--$120,000 per detector array unit per replacement event."
- **Section 7: Renewal Terms**
  - Section 7.1: "This Agreement renews annually unless cancelled by either party with 90 days' notice. CardioVision reserves the right to adjust the annual maintenance fee by up to 15% at each renewal. Price adjustments are at CardioVision's sole discretion and are not subject to negotiation once the renewal option is exercised."
- **Sales pitch discrepancies (C-Update 3):**
  - Sales pitch at W1 site visit: "Our gold-tier service plan covers all parts, labor, and emergency on-site response within 4 hours, 365 days a year." Contract Section 4.2 excludes detector arrays. Contract Section 4.3 limits 4-hour response to Priority 1 (total failure) only.
  - Sales pitch: "The plan covers everything." Contract Section 4.2 explicitly lists excluded categories.
  - Sales pitch: "Fixed pricing for the contract term." Contract Section 7.1 allows up to 15% annual price escalation at CardioVision's discretion.
- **Financial impact note at bottom of document:**
  - "Without the Detector Array Coverage Addendum ($42,000/year additional), detector array failure events are fully out-of-pocket. Industry data from CardioVision installed base: average time to first detector array replacement at 1,000--1,500 procedure/year volume sites: 5.2 years. Two replacements over a 10-year contract at $100,000 average: $200,000 additional unbudgeted exposure."
  - "15% annual escalation on $220,000/year maintenance: Year 5 maintenance cost estimate $389,000. Year 10 estimate $689,000. (Compounding 15% annually from base $220,000.)"

**Length estimate:** ~900 words, ~1,350 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (7 files) | equipment_procurement_brief.md, grant_summary_mehta.md, vendora_spec.md, vendorb_spec.md, vendor_comparison_matrix.md, pacific_heights_volume_profile.md, evaluation_report_brown.md | ~6,100 tokens |
| Update 1 files (1 file) | grant_agreement_cardiopharma.md | ~1,350 tokens |
| Update 2 files (1 file) | yun_eval_note.md | ~1,350 tokens |
| Update 3 files (1 file) | maintenance_contract_vendora.md | ~1,350 tokens |
| **Total workspace** | **15 files** | **~12,150 tokens** |

Remaining token budget for sessions: ~350K - 12.2K = ~337.8K tokens across 5 history sessions + 1 main session.
