# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_e1/`.
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

You are a grant compliance and program management assistant supporting Fatima Al-Hassan at GlobalBridge Foundation.
```

### IDENTITY.md

```markdown
# Identity

You are **ProgramOps AI**, a grant compliance and program management assistant deployed at GlobalBridge Foundation to support Fatima Al-Hassan (Program Director) during a donor fund compliance review.

You help Fatima analyze financial records, review correspondence with field staff and community partners, assess compliance with restricted grant requirements, and prepare documentation for donor communications -- across Telegram DMs with field directors and community partners, Slack DMs with HQ Finance and M&E colleagues, Feishu DMs with the donor contact, the #nairobi-operations Telegram group, and the #finance-review Slack group.

You have access to workspace documents (expense reports, budget trackers, grant agreements, activity logs, Ibrahim's receipt summary) and historical chat sessions across all platforms used by the GlobalBridge program management team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Field director self-reports require cross-verification against financial records, partner receipts, and independent documentation before being treated as authoritative. Self-serving accounts (especially post-hoc approval claims) require independent corroboration.

2. **Narrative before data**: When presenting findings to Fatima, always open with a contextual narrative framing that explains the human and programmatic stakes before presenting financial figures. Fatima is a program director who thinks in stories, not spreadsheets. Lead with what happened to the communities, then to the program, then to the finances.

3. **Qualitative-quantitative integration**: Financial compliance findings must be analyzed alongside program impact. A compliance violation that also harmed program beneficiaries is different from one that redirected funds within the program's mission. Both dimensions must be present in every analysis.

4. **Community-centered analysis**: When assessing the impact of financial decisions, always include the effect on community partners and program beneficiaries -- not only on the organization's compliance posture. Ibrahim Keita and the communities GlobalBridge serves are stakeholders whose interests matter in every analysis.

5. **Cautious attribution**: When field director claims and financial documentation conflict, present both with their sources, flag the discrepancy explicitly, and identify which source has higher verification credibility. Financial records with independent corroboration outweigh verbal self-reports, especially when the self-report involves a retroactive approval claim.

6. **Donor relationship sensitivity**: GlobalBridge's relationship with Pemberton Foundation is an organizational asset. Communications strategy should preserve the relationship while ensuring full compliance. Do not recommend strategies that achieve short-term donor appeasement at the cost of long-term credibility. When donor escalation occurs, treat it as an institutional process requiring substantive response, not a negotiation.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Fatima Al-Hassan** -- Program Director, GlobalBridge Foundation. Managing a $7.2M active grant portfolio across 4 countries. Currently investigating a financial compliance issue in the Nairobi field office.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| James Mwangi | Nairobi Field Director | Telegram DM | Senior field staff; long-tenured; claims verbal approval for budget reallocation; initially persuasive, evidence pattern undermines his account |
| David Ochieng | Donor Relations Manager, Pemberton Foundation | Feishu DM | Key donor contact; initially diplomatic, escalates to formal compliance inquiry when corrected figures reveal material restatement |
| Rachel Wu | Finance Director, HQ | Slack DM | Trusted financial colleague; most reliable financial source; urges full disclosure; audit documentation is accurate |
| Ibrahim Keita | Community Leader, Nairobi Partner | Telegram DM | Community partner; receipts show different amounts/descriptions from James's expense reports; candid when asked; not a bad actor |
| Omar Farah | Program Officer, Nairobi | #nairobi-operations (Telegram Group) | Junior field staff; knows about salary shortfall; evasive in group channel; no dedicated DM |
| Sophie Laurent | M&E Director, HQ | #finance-review (Slack Group) | Metrics framework designer; participates in finance review discussions |

## Channels
- **#nairobi-operations** (Telegram Group): Fatima, James, Omar Farah, Ibrahim Keita -- field operations and program coordination
- **#finance-review** (Slack Group): Fatima, Rachel Wu, Sophie Laurent, James Mwangi (remote) -- financial review and compliance discussions
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

### nairobi_q3_expense_report.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Nairobi Field Office Q3 Expense Report (Pemberton Grant #PF-2024-EDU-017)`
- Author: James Mwangi, Nairobi Field Director
- Reporting period: July 1 -- September 30
- Submitted: October 3 (W0+3 relative to Fatima's review starting W1)
- **Key budget lines (C1/C2 baseline):**
  - Teacher Training Materials (restricted line): Budget $50,400. Reported spend: $47,200. Activities listed: "Training materials procurement, facilitator fees, school-based workshop supplies for Q3 teacher training cycle."
  - Community Outreach (restricted line): Budget $4,200. Reported spend: $18,700. Activities listed: "Community mobilization sessions July 14-31 and August 3-17. All funds disbursed to Ibrahim Keita (community coordinator) for facilitation and materials."
  - Scholarship Administration (restricted line): Budget $12,500. Reported spend: $11,400. Activities listed: "Scholarship processing, beneficiary verification, coordination with school administration."
  - Personnel -- Program Officers (co-funded, HQ-managed): Budget $82,000. Reported spend: $53,500 (short of budget -- reflecting the unfilled Ministry co-funding gap).
- **Notable omission:** No mention of the $4,400 administrative fee retained by Ibrahim's organization. The $18,700 community outreach figure is presented as fully spent on activities.
- **Notable omission:** No note in the report about internal budget transfers or reallocations. The Teacher Training Materials and Scholarship Administration overspends are not flagged as requiring approval.
- **C2 seed:** Community Outreach line shows $18,700 against a $4,200 budget -- a 345% overspend -- without any budget amendment or explanatory note.

**Length estimate:** ~700 words, ~1,050 tokens

### pemberton_grant_agreement_excerpt.md (Initial)

**Content key points:**
- Title: `Pemberton Foundation -- Grant Agreement #PF-2024-EDU-017 (GlobalBridge Foundation), Relevant Provisions (Excerpt)`
- Excerpted by: Rachel Wu, Finance Director
- Key grant provisions:
  - Section 4.2: Restricted budget lines. "Funds designated to specific budget lines in Annex B may not be reallocated to other budget lines or purposes without prior written approval from the Pemberton Foundation Program Officer. Reallocations exceeding $2,000 require a formal budget amendment request."
  - Section 5.1: Expenditure documentation. "All expenditures must be supported by original receipts, purchase orders, or approved disbursement forms. Cash advances to partner organizations require a signed advance agreement and final accounting within 30 days."
  - Section 7.3: Partner sub-grants. "Payments to community partner organizations must reference an executed partnership agreement. Administrative fees paid to community partners must be itemized separately and included in the approved budget."
  - Section 9.2: Financial reporting. "Grantee shall submit quarterly expenditure reports within 15 days of quarter-end. Material corrections to submitted reports must be accompanied by a written explanation."
  - Section 11.1: Compliance investigation. "The Foundation reserves the right to initiate a compliance review if reported expenditures cannot be reconciled with supporting documentation. In the event of confirmed non-compliant expenditure, the Foundation may require repayment, withhold future tranches, or terminate the grant."
- **Key wording (C1/U3 relevance):** Section 4.2's "prior written approval" requirement is the definitive standard against which James's "verbal approval" claim must be measured. No verbal approval can satisfy this clause.
- **Key wording (C2 relevance):** Section 7.3 establishes that administrative fees to community partners must be itemized and budgeted -- the $4,400 admin fee to Ibrahim is non-compliant under this section regardless of whether James authorized it.

**Length estimate:** ~600 words, ~900 tokens

### nairobi_budget_tracker.md (Initial)

**Content key points:**
- Title: `Nairobi Field Office -- Pemberton Grant Budget Tracker (Active)`
- Author: Rachel Wu, Finance Director (compiled from accounting system)
- Content: Budget vs actual spend by line for the full grant period (January -- December)
- **Key records:**
  - Teacher Training Materials: Annual budget $50,400. Q1-Q2 spend: $3,200 (training materials only). Q3 spend per expense report: $47,200. Year-to-date: $50,400 (100% of annual budget, with Q4 remaining).
  - Community Outreach: Annual budget $4,200. Q1-Q2 spend: $0. Q3 spend per expense report: $18,700. Year-to-date: $18,700 (445% of annual budget).
  - Scholarship Administration: Annual budget $12,500. Q1-Q2 spend: $2,400. Q3 spend per expense report: $6,800 (office supplies line). Year-to-date: $9,200 (74% of annual budget -- note: this figure does not yet reflect the full Q3 report; Rachel's reconciliation is in progress).
  - Personnel -- Program Officers: Annual budget $164,000 (designed as 50% GlobalBridge / 50% Ministry co-funding). Ministry co-funding of $82,000 has not been received. Q3 actual spend: $53,500 (GlobalBridge portion only).
- **Rachel's note:** "The Teacher Training Materials line has exhausted 100% of its annual budget in Q3 alone. This is statistically implausible given Q1-Q2 spend of $3,200. The Community Outreach line shows 445% budget utilization. Both lines require immediate explanation and documentation review."
- **C3 source:** Activity dates implied by spending patterns are consistent with the program activity log -- the spending concentration in Q3 aligns with the July-August activity period.

**Length estimate:** ~600 words, ~900 tokens

### ministry_cofunding_correspondence.md (Initial)

**Content key points:**
- Title: `Correspondence: Kenyan Ministry of Education Co-Funding Delay -- Nairobi Program`
- Period: May -- October (current year)
- Content: Email chain between James Mwangi, Samuel Kipchoge (Ministry liaison), and Fatima Al-Hassan
- **Key correspondence:**
  - May 15: Ministry letter to GlobalBridge confirming approved co-funding of KSH 10,660,000 (~$82,000) for program officer positions. Payment subject to Ministry budget approval.
  - June 3: Samuel Kipchoge to James: "The budget allocation has been delayed due to the national supplementary budget process. We expect release of funds in September or October. Please proceed with the program on your current budget."
  - August 12: Fatima to Samuel (CC James): "We note the continued delay on the co-funding. Our program officers are in place and delivering. We hope to receive resolution soon. Please advise on the timeline."
  - August 12: James to Fatima (separate message, same day): "Fatima, I spoke with Samuel again. He says October at the earliest. We are managing but it's getting tight. I may need to find a solution."
  - September 28: Samuel to James: "The FY budget has now closed without the GlobalBridge allocation. The co-funding will need to be resubmitted for next year's budget cycle. I apologize for the delay."
- **B2 seed:** This correspondence establishes the Ministry delay as a real, documented problem -- the same problem James uses to justify the reallocation. The August 12 message ("I may need to find a solution") is the closest thing in the documentary record to a warning from James, but it does not request or receive approval for a specific reallocation.
- **C1 context:** Fatima's August 12 reply does not authorize any reallocation. Her response ("we hope to receive resolution soon") is not a directive to James to act on the restricted budget.

**Length estimate:** ~500 words, ~750 tokens

### globalbridge_activity_log_nairobi.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Nairobi Program Activity Log (Pemberton Grant #PF-2024-EDU-017, Q2-Q3)`
- Author: Omar Farah, Program Officer (Nairobi), compiled quarterly
- Content: All program activities, dates, locations, participation counts
- **Key records (C3 source):**
  - Teacher Training sessions: June 15-21 (Kibera primary schools, 4 schools, 23 teachers), June 24-30 (Mathare, 3 schools, 18 teachers), July 7-14 (Eastleigh, 4 schools, 24 teachers), July 21-28 (follow-up all districts, 11 schools, 41 teachers).
  - Community Mobilization sessions (led by Ibrahim Keita's organization): July 14 (Kibera, 45 community members), July 17 (Mathare, 38 community members), July 21 (Eastleigh, 52 community members), July 28-31 (multi-district joint session, 89 community members), August 3 (Kibera, 41 community members), August 7 (Mathare, 44 community members), August 10 (Eastleigh, 49 community members), August 17 (closing session, all districts, 76 community members).
  - Scholarship administration: quarterly processing of 34 scholarship beneficiaries (ongoing).
- **C3 confirmation:** All activity dates, locations, and participation numbers are internally consistent with what James reports in his Telegram DMs, what Ibrahim describes in his DM, and what Omar posts in #nairobi-operations. No source disputes the activities occurred. The contradiction is about financial recording, not program execution.
- **Near-signal noise:** The activity log shows a busy and effective program. An agent reading only the activity log would see a successful quarter. The financial irregularities are invisible in this document.

**Length estimate:** ~700 words, ~1,050 tokens

### rachel_initial_audit_note.md (Initial)

**Content key points:**
- Title: `Finance Review Note -- Nairobi Q3 Expense Report Discrepancies`
- Author: Rachel Wu, Finance Director
- Date: W1 (the document that triggers the investigation)
- Content: Rachel's initial reconciliation findings
- **Key findings (C1 baseline):**
  - Teacher Training Materials ($47,200): "No purchase orders or delivery receipts on file for this expenditure. Internal accounting shows the amount was processed via three journal entries by James Mwangi between August 10-28. Normal procurement for training materials involves vendor invoices from approved suppliers -- no vendor invoices are recorded for this period."
  - Community Outreach ($18,700): "The approved budget for this line is $4,200 for the full grant year. The Q3 report shows $18,700 against this line -- a $14,500 overrun against annual budget. No budget amendment has been submitted or approved."
  - **Key absence:** No written authorization for either amount in the budget amendment log. No email from Fatima approving either reallocation. No sign-off from the Finance Director on any budget transfer.
  - Rachel's conclusion: "These transactions require explanation and supporting documentation before I can certify this report. I am flagging this to the Program Director immediately."
- **B1 seed:** This document establishes the factual baseline but does not yet reveal the full picture (the Scholarship Administration line charge is not yet identified).
- **C1 reversal trigger (partial):** Rachel's finding that there are no vendor invoices for the Teacher Training Materials spend is the first signal that the $47,200 was not actually spent on training materials.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| nairobi_q3_expense_report.md | Initial | Workspace | Establishes the reported figures (C1/C2 baseline, B1/B2 seed) |
| pemberton_grant_agreement_excerpt.md | Initial | Workspace | Grant terms defining what is compliant (C1 standard, C2 relevance) |
| nairobi_budget_tracker.md | Initial | Workspace | Budget vs actual comparison (C1/C2 scope indicator) |
| ministry_cofunding_correspondence.md | Initial | Workspace | Documents the real Ministry delay (B2 seed, C1 context) |
| globalbridge_activity_log_nairobi.md | Initial | Workspace | Program activities (C3 non-conflict source) |
| rachel_initial_audit_note.md | Initial | Workspace | Rachel's first findings (C1 baseline, B1 seed) |
| ibrahim_receipt_summary.md | Update 1 (before R4) | updates/ -> workspace new | Ibrahim's records vs James's expense report (C2 reversal trigger, B1 partial reversal) |
| rachel_full_audit_report.md | Update 2 (before R6) | updates/ -> workspace new | Full $54K scope, three budget lines, journal entry pattern (B1+B2 full reversal) |
| pemberton_formal_inquiry_letter.md | Update 3 (before R8) | updates/ -> workspace new | David's formal escalation letter (C4 temporal reversal trigger) |

---

## 4. Near-Signal Noise File Design

### nairobi_q3_expense_report.md
- **Why it looks plausible:** Formally structured quarterly report. Budget lines, activity descriptions, and amounts all appear professional. The community outreach overspend could be rationalized as a program expansion. James's name appears as the authorized signatory, which is appropriate for his role.
- **Why it should not settle C2:** The community outreach line shows 445% budget utilization with no budget amendment note. The Teacher Training Materials line shows 100% utilization in one quarter when Q1-Q2 spend was $3,200. Both patterns are implausible without explanation. The administrative fee is omitted entirely.
- **Noise risk:** Agent may accept the formally structured report as evidence of legitimate process, missing the absence of vendor invoices and the impossible spending patterns.

### ministry_cofunding_correspondence.md
- **Why it looks relevant:** The co-funding delay is real, documented, and significant. James's August 12 message ("I may need to find a solution") could be read as foreshadowing a reallocation.
- **Why it should not settle C1:** The correspondence establishes the problem (Ministry delay) but contains no authorization for any specific reallocation. Fatima's replies do not approve any budget action. The document establishes operational pressure, not authorization.
- **Noise risk:** Agent may over-weight the Ministry delay as justification for the reallocation, applying B2 logic (emergency reallocation is understandable) without noting that understanding the problem is not the same as authorizing a non-compliant solution.

### globalbridge_activity_log_nairobi.md
- **Why it looks relevant:** Shows a busy, successful program quarter. Activities match the dates James reports. Community engagement is high.
- **Why it should not settle C1 or C2:** The activity log confirms what happened programmatically but says nothing about how it was funded. The community mobilization sessions were led by Ibrahim's organization and did occur -- the question is whether the $18,700 was properly recorded and whether the admin fee was disclosed. The log is irrelevant to the financial compliance question.
- **Noise risk:** Agent may cite the activity log as evidence that the money was well-spent and therefore the reallocation is acceptable. This conflates programmatic effectiveness with financial compliance.

### rachel_initial_audit_note.md
- **Why it looks relevant:** Official finance review note by the Finance Director, specifically documenting the discrepancies.
- **Why it shows only part of the picture:** Rachel's initial note covers only two budget lines (Teacher Training Materials and Community Outreach). The Scholarship Administration charge ($6,800) is not yet identified. The full pattern of journal entry manipulation is not yet documented.
- **Noise risk:** Agent may treat Rachel's initial note as a complete picture, failing to anticipate additional findings.

---

## 5. Update-Added Workspace Files

### ibrahim_receipt_summary.md (Update 1, before R4)

**Content key points:**
- Title: `Ibrahim Keita Community Organization -- Payment Receipt Summary (GlobalBridge Nairobi, Q2-Q3)`
- Author: Ibrahim Keita (provided to Fatima verbally summarized in Telegram DM; Rachel requests and receives formal copy)
- Date: Prepared W2, covering July-August payment period
- **Key evidence (C2 reversal):**
  - Payment 1 (July 5): KSH 650,000 (~$5,000) received from GlobalBridge Nairobi. Description on receipt: "Consultant fees -- community mobilization preparation." Actual disbursement: KSH 595,000 ($4,580) to facilitators; KSH 55,000 ($420) retained as admin fee.
  - Payment 2 (July 22): KSH 850,000 (~$6,540) received. Description: "Consultant fees -- community mobilization July." Actual disbursement: KSH 788,000 ($6,060) to facilitators; KSH 62,000 ($480) retained as admin fee.
  - Payment 3 (August 19): KSH 906,600 (~$6,970) retained as admin fee. Description: "Consultant fees -- community mobilization August." Actual disbursement: KSH 689,000 ($5,300) on activities; KSH 535,000 ($4,115) retained... [Note: Ibrahim's record shows KSH 438,100 retained as admin fee across all three payments combined = $3,370 at KSH 130/$1]
  - **Totals:** Total received: ~$18,510 (approximately $18,700 with exchange rate variation). Total spent on activities: ~$14,340 (~$14,300). Admin fee retained: ~$4,370 (~$4,400).
  - Ibrahim's annotation: "The admin fee arrangement was discussed with James Mwangi. James told me this was the standard arrangement for community organizations working with GlobalBridge. I did not have written confirmation. I now understand this may not have been formally approved."
- **Description discrepancy (C2 core):** Ibrahim's receipts describe payments as "consultant fees for community mobilization." James's expense report describes the same payments as "community outreach -- materials and facilitation." These are different descriptions for the same transactions. Ibrahim's description is more accurate (his organization provided coordination, not materials).
- **What this proves:** The $18,700 was not fully spent on activities. $4,400 was retained as an admin fee that does not appear in James's expense report and is not in the approved budget per Section 7.3 of the grant agreement. The expense report description ("materials and facilitation") mischaracterizes a consultant fee arrangement.

**Length estimate:** ~700 words, ~1,050 tokens

### rachel_full_audit_report.md (Update 2, before R6)

**Content key points:**
- Title: `GlobalBridge Foundation -- Internal Audit Report: Nairobi Field Office Q3 Financial Review`
- Author: Rachel Wu, Finance Director
- Date: W2-W3 (approximately 2-3 weeks into investigation)
- **Full scope findings (B1+B2 reversal triggers):**
  - Finding 1: Teacher Training Materials line ($47,200). Detailed journal entry analysis shows the $47,200 breaks down as: $28,500 processed as internal transfers to the Personnel -- Program Officers line (coded as "Q3 personnel cost adjustment"), and $18,700 processed as cash disbursement to Ibrahim Keita's organization (coded as "community facilitation"). Both amounts required budget amendment approval per Section 4.2. Neither was submitted for approval. James Mwangi authorized all three journal entries himself.
  - Finding 2: Community Outreach line ($18,700). The $18,700 is double-counted: it appears as an outflow from Teacher Training Materials ($18,700 to Ibrahim) and also appears as the Community Outreach line spend. James coded the Ibrahim payments under Community Outreach to make the Teacher Training Materials line appear to be spent on legitimate activities. The budget for Community Outreach was $4,200 -- the actual use of this line was $0 since the $18,700 is a recoded entry from Teacher Training Materials, not new activity spend. This means the Community Outreach budget of $4,200 is effectively unspent.
  - Finding 3: Scholarship Administration line ($6,800). A separate set of journal entries shows $6,800 processed as "office supplies -- program administration" charged to the Scholarship Administration line. Supporting documentation: three receipts for office furniture (two desks, four chairs, filing cabinet) purchased for the Nairobi office. The Scholarship Administration line is restricted to scholarship processing activities, not general office purchases.
  - Total non-compliant spend: $28,500 (salary coverage from restricted line) + $18,700 (Ibrahim payments with $4,400 admin fee not disclosed) + $6,800 (office furniture charged to scholarship line) = $54,000.
- **Journal entry pattern analysis (B1+B2 reversal):** "The three sets of journal entries share a pattern: each was processed as a bundle with legitimate operational expenses, each was submitted in batches rather than individually (reducing visibility), and each used secondary budget codes that require supervisor sign-off but were submitted in a way that obscured the primary restricted line being charged. This pattern is inconsistent with a good-faith operational adjustment made under verbal authorization. A field director who believed he had authorization would have no reason to obscure the transfers."
- **Rachel's recommendation:** "Full disclosure to Pemberton Foundation. Formal corrective action plan. Internal investigation of the authorization pattern."

**Length estimate:** ~900 words, ~1,350 tokens

### pemberton_formal_inquiry_letter.md (Update 3, before R8)

**Content key points:**
- Title: `Pemberton Foundation -- Formal Compliance Inquiry: Grant #PF-2024-EDU-017 (GlobalBridge Foundation)`
- Author: David Ochieng, Donor Relations Manager, Pemberton Foundation (on behalf of Compliance Department)
- Date: W4 (approximately 4 weeks into investigation)
- **Content (C4 reversal):**
  - Reference line: "RE: Corrected Q3 Expenditure Report -- Material Restatement Notification"
  - Paragraph 1 (factual): "Pemberton Foundation has received GlobalBridge Foundation's corrected Q3 expenditure report for Grant #PF-2024-EDU-017. The corrected report shows a variance of $47,200 on the Teacher Training Materials restricted line compared to the originally submitted report. Under our grant management policy, variances of this magnitude constitute a material restatement requiring formal review."
  - Paragraph 2 (process): "Pemberton Foundation's compliance team has been notified. We are initiating a formal grant compliance review under Section 11.1 of the Grant Agreement. This review does not presuppose any finding of wrongdoing. We are requesting: (1) A written explanation of how the original Teacher Training Materials expenditure was authorized, with supporting documentation; (2) Copies of all budget amendment requests submitted in relation to the Nairobi field office for Grant Year 2024; (3) A description of the corrective actions GlobalBridge has taken or plans to take."
  - Paragraph 3 (tone/relationship): "GlobalBridge Foundation has been a valued Pemberton partner, and we want to resolve this matter in a way that protects both organizations. We are available to discuss this by video call. However, a written formal response is required within 10 business days under our grant agreement."
  - David's personal note appended informally: "Fatima -- I'm sorry this has become formal. My hands are tied once the compliance team is involved. Please put together the strongest possible written response. I will advocate internally for a cooperative resolution process."
- **C4 temporal marker:** David's formal letter vs his Phase 1 Feishu DMs shows the shift from "let's clarify this" to institutional compliance process.
- **What this establishes:** A formal Pemberton compliance review is now underway. The 10-day response deadline creates urgency. David's personal note shows he is still a potential ally, but the formal process is not under his control.

**Length estimate:** ~600 words, ~900 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | nairobi_q3_expense_report.md, pemberton_grant_agreement_excerpt.md, nairobi_budget_tracker.md, ministry_cofunding_correspondence.md, globalbridge_activity_log_nairobi.md, rachel_initial_audit_note.md | ~5,400 tokens |
| Update 1 files (1 file) | ibrahim_receipt_summary.md | ~1,050 tokens |
| Update 2 files (1 file) | rachel_full_audit_report.md | ~1,350 tokens |
| Update 3 files (1 file) | pemberton_formal_inquiry_letter.md | ~900 tokens |
| **Total workspace** | **14 files** | **~10,700 tokens** |

Remaining token budget for sessions: ~400K - 10.7K = ~389.3K tokens across 6 history sessions + 1 main session.
