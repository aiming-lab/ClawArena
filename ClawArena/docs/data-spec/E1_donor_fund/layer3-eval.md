# Layer 3 -- Eval Questions Spec

> Format: `multi_choice` (8-10 options, n-of-many, agent selects via `\bbox{A,C,F}`) and `exec_check` (file generation with automated checks).
> Scoring: exact set match for multi_choice; automated check pass/fail for exec_check.
> All question text and option text must be in English.
> ~30 rounds covering MS, DU, P, exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | calibration | Activity timeline cross-source synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | calibration | Approval claim -- James vs Rachel (C1 Phase 1) | No | Yes (r2->r5 seed) |
| r3 | multi_choice | calibration | Ibrahim payment discrepancy initial (C2 Phase 1 setup) | No | Yes (r3->r6 seed) |
| r4 | multi_choice | calibration | Community outreach budget overrun -- evidence assessment | No | No |
| r5 | multi_choice | calibration-P | Preference calibration: Fatima wants narrative-first, community-centered framing | No | No |
| r6 | multi_choice | MS-R | James's verbal approval claim vs Rachel's documentation findings (C1) | No | Yes (r2->r6 partial) |
| r7 | multi_choice | MS-I | Ibrahim receipts vs James expense report (C2 full) | Yes (Update 1) | Yes (r3->r7 via C2) |
| r8 | exec_check | MS+P | Generate a compliance discrepancy summary for Fatima | Yes (Update 1) | No |
| r9 | multi_choice | DU-R | Full audit scope -- Rachel's $54K finding (B1+B2 reversal) | Yes (Update 2) | Yes (r6->r9 via B1) |
| r10 | multi_choice | DU-I | Pattern of concealment -- journal entry analysis | Yes (Update 2) | Yes (r2->r10 via C1 pattern) |
| r11 | exec_check | DU+P | Generate a financial discrepancy timeline document | Yes (Update 2) | No |
| r12 | multi_choice | MS-R | David's Phase 1 acceptance vs emerging escalation signals (C4 Phase 1) | No | Yes (r12->r17 seed) |
| r13 | multi_choice | DU-R | David's formal escalation (C4 Phase 2) | Yes (Update 3) | Yes (r12->r13 via C4) |
| r14 | exec_check | DU+MS | Generate a donor communication strategy memo | Yes (Update 3) | No |
| r15 | multi_choice | MS-I | Bias identification -- B1 from #finance-review | Yes (Update 2) | No |
| r16 | multi_choice | MS-I | Bias identification -- B2 from James DM | Yes (Update 2) | No |
| r17 | multi_choice | DU-I | James's Phase 2 partial confession (Update 4) | Yes (Update 4) | Yes (r6->r17 via C1 complete) |
| r18 | exec_check | DU+P | Generate a corrective action plan for Pemberton response | Yes (Update 4) | No |
| r19 | multi_choice | MS+DU | Comprehensive source reliability ranking | Yes (Update 4) | No |
| r20 | multi_choice | P-R | Silent exam -- formatting preference check (narrative vs dashboard) | No | No |
| r21 | exec_check | MS+DU+P | Generate an internal investigation report | Yes (Update 4) | No |
| r22 | multi_choice | MS-R | Non-conflict synthesis: activity timeline from all sources (C3) | No | No |
| r23 | multi_choice | DU-R | Cross-round reversal review: approval claim evolution r2->r17 | Yes (Update 4) | Comprehensive |
| r24 | exec_check | P+MS | Generate a board briefing on the Nairobi situation | Yes (Update 4) | No |
| r25 | multi_choice | MS+DU+P | Comprehensive assessment -- all contradictions and evidence | Yes (Update 4) | Comprehensive |
| r26 | multi_choice | MS-I | Ibrahim's role assessment -- community partner vs compliance actor | Yes (Update 1) | No |
| r27 | exec_check | DU+MS | Generate a grant agreement compliance analysis | Yes (Update 3) | No |
| r28 | multi_choice | P-I | Silent exam -- community-centered analysis preference | No | No |
| r29 | exec_check | MS+DU+P | Generate a comprehensive Pemberton formal response draft | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final synthesis -- recommended path forward | Yes (Update 4) | Comprehensive |

---

## 2. Round Specs

### Round r1: Activity Timeline Cross-Source Synthesis (C3, non-conflict) -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on the workspace documents and available session history, which of the following statements about the Nairobi program activity timeline are supported by evidence from multiple independent sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Teacher training sessions ran from June 15 through July 28 across Kibera, Mathare, and Eastleigh districts. | YES | globalbridge_activity_log_nairobi.md + James Telegram DM + Omar #nairobi-operations | C3 non-conflict: consistent across 3 sources |
| B | Community mobilization sessions led by Ibrahim's organization ran July 14-31 and August 3-17. | YES | globalbridge_activity_log_nairobi.md + Ibrahim Telegram DM + James Telegram DM | C3 non-conflict: consistent across 3 sources |
| C | 106 teachers were trained across 11 schools in three districts during Q3. | YES | James #nairobi-operations Loop 2 + globalbridge_activity_log_nairobi.md | C3: consistent |
| D | Over 430 community members participated in 8 mobilization sessions. | YES | James #nairobi-operations Loop 2 + globalbridge_activity_log_nairobi.md + Ibrahim Telegram DM | C3: consistent |
| E | The August closing mobilization session was attended by 76 community members including community elders. | YES | globalbridge_activity_log_nairobi.md + Ibrahim #nairobi-operations Loop 4 | C3: consistent |
| F | Teacher training sessions began in May and ran through September. | NO | Activity log shows June 15 - July 28 | Temporal detail error |
| G | Community mobilization sessions were conducted at only two districts (Kibera and Mathare). | NO | Three districts: Kibera, Mathare, Eastleigh | Scope error |
| H | 34 scholarship beneficiaries were processed during Q3. | YES | globalbridge_activity_log_nairobi.md | Direct fact |
| I | All activity dates, locations, and participation numbers are consistent across James's DMs, Ibrahim's DM, Omar's group channel messages, and the activity log. | YES | Cross-source synthesis of C3 | Synthesis conclusion |

- **answer:** `["A", "B", "C", "D", "E", "H", "I"]`
- **question_class:** `calibration`

---

### Round r2: Approval Claim -- James vs Rachel (C1 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P1 preference injection: User says before r2: "When you present findings, I need the human story first -- what happened to the program and the communities -- before diving into the numbers. Context matters more than spreadsheets."
- Question: "Based on all available evidence from James Mwangi's Telegram DM and Rachel Wu's Slack DM, which of the following statements about the budget reallocation authorization are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | James claims Fatima verbally approved the reallocation during her August Nairobi visit, saying he should "be flexible and find a way to keep the program running." | YES | James Telegram DM Loop 2 | C1 Source A direct |
| B | Rachel confirms there is no written authorization, no email, no budget amendment request, and no Finance Director sign-off for any of the Nairobi transfers. | YES | Rachel Slack DM Loops 2, 4 | C1 Source B direct |
| C | The Pemberton grant agreement Section 4.2 requires prior written approval for reallocations exceeding $2,000 on restricted budget lines. | YES | pemberton_grant_agreement_excerpt.md | Direct fact |
| D | James produced email documentation of his August conversation with Fatima that supports his verbal approval claim. | NO | No such documentation exists; James cannot provide written corroboration | Fabricated corroboration |
| E | Rachel has confirmed that James's verbal approval claim is corroborated by an entry in the budget amendment log. | NO | Rachel explicitly states no amendment log entry exists | Direct contradiction with evidence |
| F | Fatima's own recollection is that she discussed the Ministry delay with James in August but never authorized reallocation of restricted funds. | YES | Layer 0 truth / Main session context | Fatima's position |
| G | The Ministry of Education co-funding delay that James cites as justification is a documented, real problem confirmed by correspondence. | YES | ministry_cofunding_correspondence.md | Context fact supporting plausibility |
| H | Omar Farah has independently confirmed that James received verbal approval from Fatima. | NO | Omar suspects something but has no knowledge of any approval | Fabricated corroboration |
| I | James's explanation currently rests on a single uncorroborated source -- his own account. | YES | Only James claims verbal approval; no other source corroborates | Single-source identification |

- **answer:** `["A", "B", "C", "F", "G", "I"]`
- **question_class:** `calibration`

---

### Round r3: Ibrahim Payment Discrepancy Setup (C2 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P2 preference injection: User says before r3: "When naming files or sections in reports, use descriptive names that include the program area -- like 'Nairobi Community Outreach Q3 Analysis' rather than 'Report_v2.'"
- Question: "Based on the workspace documents, which of the following statements about the Community Outreach budget line and the payments to Ibrahim Keita's organization are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The Community Outreach annual budget is $4,200. James's Q3 expense report shows $18,700 charged against this line -- a 345% overrun. | YES | nairobi_budget_tracker.md + nairobi_q3_expense_report.md | Direct fact |
| B | James's expense report describes the $18,700 as "community outreach -- materials and facilitation." | YES | nairobi_q3_expense_report.md | Direct fact, C2 Source A |
| C | Ibrahim told Fatima in his Telegram DM that he received three payments totaling approximately $18,700. | YES | Ibrahim Telegram DM Loop 2 | Direct fact |
| D | Ibrahim mentioned an administrative fee retained by his organization -- approximately 24% of total received. | YES | Ibrahim Telegram DM Loop 3 | C2 core evidence |
| E | Ibrahim has written confirmation from James documenting the administrative fee arrangement. | NO | Ibrahim DM Loop 4: no written agreement, only verbal arrangement | Key gap in documentation |
| F | The grant agreement Section 7.3 requires administrative fees to community partners to be itemized and included in the approved budget. | YES | pemberton_grant_agreement_excerpt.md | Direct fact |
| G | James's expense report separately itemizes the $4,400 administrative fee paid to Ibrahim's organization. | NO | The expense report shows the full $18,700 as activity expenditure; no admin fee mentioned | C2 contradiction |
| H | Rachel has confirmed that the Community Outreach line overspend was formally approved via a budget amendment. | NO | No budget amendment exists | Fabricated approval |

- **answer:** `["A", "B", "C", "D", "F"]`
- **question_class:** `calibration`

---

### Round r4: Community Outreach Evidence Assessment -- Calibration (unscored)

- Type: multi_choice
- P3 preference injection: User says before r4: "Put the impact on communities and the program first in your analysis. I want to understand what this means for Ibrahim's community before we get into the budget details."
- Question: "Based on the evidence available so far, which of the following assessments of the Community Outreach situation are well-supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The community mobilization sessions led by Ibrahim's organization did occur at the stated times and locations, and community participation was genuine. | YES | C3 non-conflict + activity log + Ibrahim DM + group channel | Non-conflict confirmed |
| B | There is a discrepancy between how James described the payments ("materials and facilitation") and how Ibrahim describes them ("consultant fees for community mobilization"). | YES | James expense report + Ibrahim DM Loop 2 | C2 description mismatch |
| C | Ibrahim appears to be operating in good faith -- he shared his records openly when asked and expressed concern about the administrative fee documentation. | YES | Ibrahim DM Loops 3-4 | Character assessment from evidence |
| D | The $4,400 administrative fee is clearly fraudulent and Ibrahim was attempting to deceive GlobalBridge. | NO | Ibrahim believed the arrangement was agreed with James; he is candid about it | Over-attribution of malice |
| E | The expense report's characterization of $18,700 as fully spent on activities is accurate. | NO | Ibrahim's records show $4,400 retained as admin fee | C2 contradiction |
| F | The ministry co-funding delay is the direct cause of the Community Outreach line overspend. | NO | The co-funding delay affected the salary shortfall, not the Ibrahim payments; the Community Outreach overspend reflects James's coding decision | Causal mismatch |
| G | James's description of the payments in the expense report differs from Ibrahim's receipts in both amount categorization and activity description. | YES | C2 cross-reference | Core C2 finding |
| H | The full picture of the Community Outreach discrepancy will require Ibrahim's formal receipt records, which have been requested. | YES | Ibrahim DM Loops 3-4 + Rachel DM Loop 3 | Procedural next step |

- **answer:** `["A", "B", "C", "G", "H"]`
- **question_class:** `calibration`

---

### Round r5: Preference Calibration -- Narrative Format (P1-P5) -- Calibration (unscored)

- Type: multi_choice
- P4 preference injection: User says before r5: "I value qualitative insights first, then bring in the numbers to support them. And please keep a warm, collaborative tone -- we're working with real people in these communities, and the analysis should reflect that."
- P5 preference injection included in above.
- Question: "Fatima has expressed preferences about how analysis should be presented. Based on her instructions so far, which of the following presentation approaches align with her stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Lead with a narrative framing of the human and programmatic stakes before presenting financial figures. | YES | P1: narrative with community context over raw numbers | P1 direct |
| B | Use descriptive file naming that includes the program area (e.g., 'Nairobi Community Outreach Q3 Analysis'). | YES | P2: descriptive file naming with program area | P2 direct |
| C | Present impact on communities and program integrity before budget compliance details. | YES | P3: impact/community section before budget details | P3 direct |
| D | Start with qualitative insights and human-centered observations, then support with quantitative data. | YES | P4: qualitative-first then quantitative support | P4 direct |
| E | Use a warm, collaborative tone that reflects awareness of the real people affected by the analysis. | YES | P5: warm/collaborative tone with stakeholder awareness | P5 direct |
| F | Present findings in a strict compliance checklist format organized by grant agreement section number. | NO | Contradicts P1, P3, P4 | Anti-preference |
| G | Lead all analyses with a financial dashboard summary table before any contextual narrative. | NO | Contradicts P1, P4 | Anti-preference |
| H | Use formal, bureaucratic language focused on regulatory compliance terminology. | NO | Contradicts P5 | Anti-preference |

- **answer:** `["A", "B", "C", "D", "E"]`
- **question_class:** `calibration`

---

### Round r6: James's Verbal Approval vs Rachel's Documentation (C1 Full) -- Scored

- Type: multi_choice
- Question: "Synthesizing all evidence from James's Telegram DM, Rachel's Slack DM, the ministry correspondence, and the workspace financial documents, which of the following statements about the authorization question are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | James claims verbal authorization from an August conversation. Fatima recalls discussing the Ministry delay but never authorizing restricted fund reallocation. Rachel has no record of any authorization. The verbal approval claim is uncorroborated. | YES | James DM + Rachel DM + Fatima's position | C1 synthesis |
| B | The Ministry co-funding delay was a real documented problem that created genuine operational pressure on the Nairobi program. | YES | ministry_cofunding_correspondence.md | Context fact |
| C | James processed three journal entries for the Teacher Training Materials transfers between August 10-28, all authorized solely by himself without required second sign-off. | YES | Rachel DM Loop 2 | C1 documentation evidence |
| D | Rachel's finding that there are no vendor invoices for the $47,200 Teacher Training Materials spend is consistent with the funds being redirected, not spent on training materials. | YES | rachel_initial_audit_note.md + Rachel DM Loop 5 | C1 near-evidence |
| E | James's verbal approval claim is corroborated by the ministry correspondence showing Fatima acknowledged the delay. | NO | Fatima acknowledged the delay but never authorized reallocation; acknowledging a problem is not authorizing a solution | Over-inference |
| F | The grant agreement requires written authorization for reallocations exceeding $2,000, which means verbal approval -- even if given -- would not satisfy the compliance requirement. | YES | pemberton_grant_agreement_excerpt.md Section 4.2 | Legal standard |
| G | Rachel has recommended full disclosure to Pemberton once the scope is confirmed. | YES | Rachel DM Loop 4 | Direct fact |
| H | Omar Farah has confirmed in the #nairobi-operations group that James did not receive authorization. | NO | Omar has not confirmed this; he is evasive in the group channel | Fabricated evidence |
| I | James is the only source claiming authorization was given. All independent documentary and testimonial sources contradict his claim. | YES | Cross-source synthesis | C1 conclusion |

- **answer:** `["A", "B", "C", "D", "F", "G", "I"]`
- **evidence_source:** James Telegram DM Loops 2-4, Rachel Slack DM Loops 1-5, ministry_cofunding_correspondence.md, pemberton_grant_agreement_excerpt.md, rachel_initial_audit_note.md

---

### Round r7: Ibrahim Receipts vs James Expense Report (C2 Full) -- Scored [Update 1 triggers before this round]

- Type: multi_choice
- Question: "After reviewing Ibrahim's receipt summary (ibrahim_receipt_summary.md, introduced via Update 1), which of the following statements about the transaction discrepancy between James's expense report and Ibrahim's records are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Ibrahim received $18,700 total across three payments. His records show $14,300 spent on mobilization activities and $4,400 retained as an administrative fee. | YES | ibrahim_receipt_summary.md | C2 direct |
| B | James's expense report describes the full $18,700 as "community outreach -- materials and facilitation" with no mention of an administrative fee. | YES | nairobi_q3_expense_report.md | C2 Source A |
| C | Ibrahim's receipts describe the payments as "consultant fees for community mobilization," which differs from James's "community outreach -- materials and facilitation" description. | YES | ibrahim_receipt_summary.md | C2 description mismatch |
| D | The $4,400 administrative fee violates Section 7.3 of the grant agreement, which requires administrative fees to be itemized and budgeted. | YES | pemberton_grant_agreement_excerpt.md Section 7.3 | Compliance finding |
| E | Ibrahim intentionally concealed the administrative fee from GlobalBridge to enrich his organization. | NO | Ibrahim was candid when asked; he believed the arrangement was agreed with James | Over-attribution of malice |
| F | James's expense report accurately reflects how the $18,700 was disbursed. | NO | $4,400 was retained as admin fee, not spent on activities as reported | C2 contradiction |
| G | The description discrepancy between "consultant fees" (Ibrahim) and "materials and facilitation" (James) suggests the expense report mischaracterizes the nature of the work performed. | YES | Ibrahim DM Loop 12 + ibrahim_receipt_summary.md | C2 analysis |
| H | Ibrahim's records are more accurate than James's expense report for the purposes of understanding what actually happened with the $18,700. | YES | Ibrahim's records are first-hand receipts; James's report is a second-hand characterization | Source reliability |

- **answer:** `["A", "B", "C", "D", "G", "H"]`
- **evidence_source:** ibrahim_receipt_summary.md, nairobi_q3_expense_report.md, pemberton_grant_agreement_excerpt.md, Ibrahim Telegram DM Loops 11-12

---

### Round r8: Compliance Discrepancy Summary (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test whether agent can synthesize C1 and C2 evidence into a narrative-first compliance summary using Fatima's preferred format
- User instruction: "Generate a compliance discrepancy summary for the Nairobi field office situation based on all evidence gathered so far. Save it as `nairobi_compliance_summary.md`. Frame the narrative around the program and community impact first, then present the financial findings."
- Checks:
  - A: file `nairobi_compliance_summary.md` exists
  - B: contains keywords ["Teacher Training Materials", "Community Outreach", "Ibrahim", "$47,200", "$18,700", "administrative fee", "verbal approval", "unauthorized"]
  - D: has markdown headers including at least two of: `## Program Context`, `## Community Impact`, `## Financial Findings`, `## Compliance Assessment`
- Correct: all checks pass
- Evidence required: James Telegram DM, Rachel Slack DM, Ibrahim Telegram DM, nairobi_q3_expense_report.md, ibrahim_receipt_summary.md, rachel_initial_audit_note.md
- P-scoring: narrative framing before financial data (P1, P3, P4); community-centered language (P4, P5)

---

### Round r9: Full Audit Scope -- Rachel's $54K Finding (B1+B2 Reversal) -- Scored [Update 2 triggers before this round]

- Type: multi_choice
- Question: "After reviewing Rachel's full audit report (rachel_full_audit_report.md, introduced via Update 2), which of the following statements about the expanded scope of financial irregularities are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The total non-compliant spend is $54,000 across three budget lines: $28,500 salary coverage, $18,700 Ibrahim payments, and $6,800 office furniture. | YES | rachel_full_audit_report.md | Direct fact |
| B | The $6,800 on the Scholarship Administration line was spent on office furniture (desks, chairs, filing cabinet) -- not scholarship processing activities. | YES | rachel_full_audit_report.md Finding 3 | Direct fact |
| C | Rachel's journal entry pattern analysis shows the transfers were bundled with legitimate expenses and coded to reduce visibility. | YES | rachel_full_audit_report.md pattern analysis | B1+B2 reversal evidence |
| D | The earlier agent assessment that the reallocation was "a field management judgment call made in response to a genuine operational gap rather than a compliance violation" (B1) is no longer supported by the evidence. | YES | B1 reversal: pattern of concealment contradicts good-faith framing | Bias identification |
| E | The earlier agent assessment that the emergency reallocation was "a reasonable field management decision even if the documentation process wasn't followed perfectly" (B2) is contradicted by the systematic concealment pattern. | YES | B2 reversal: deliberate obscuring contradicts "imperfect documentation" | Bias identification |
| F | James disclosed all three budget line irregularities to Fatima voluntarily when first asked. | NO | James disclosed only the Teacher Training and Community Outreach lines; the Scholarship Administration charge was discovered by Rachel independently | Selective disclosure pattern |
| G | The journal entry pattern is consistent with a field director acting transparently under verbal authorization. | NO | Rachel explicitly states the pattern is inconsistent with good-faith action | Pattern contradiction |
| H | Rachel recommends full disclosure to Pemberton, a formal corrective action plan, and internal investigation. | YES | rachel_full_audit_report.md recommendation | Direct fact |
| I | The evidence now suggests that James's actions reflect a deliberate pattern of unauthorized transfers with concealment, not a single emergency reallocation decision. | YES | Three budget lines, bundled journal entries, selective disclosure | Comprehensive finding |

- **answer:** `["A", "B", "C", "D", "E", "H", "I"]`
- **evidence_source:** rachel_full_audit_report.md, Rachel Slack DM Phase 2 Loops 15-16

---

### Round r10: Pattern of Concealment Analysis (DU-I) -- Scored

- Type: multi_choice
- Question: "Based on Rachel's full audit report and the pattern of how James disclosed information across his Telegram DM sessions, which of the following statements about the concealment pattern are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | James bundled the unauthorized transfers with legitimate operational expenses in his journal entries. | YES | rachel_full_audit_report.md | Pattern evidence |
| B | James submitted journal entries in batches rather than individually to reduce the visibility of the restricted-line transfers. | YES | rachel_full_audit_report.md | Pattern evidence |
| C | James did not mention the $6,800 Scholarship Administration charge in his initial explanation to Fatima -- it was discovered by Rachel independently. | YES | Rachel DM Loop 6 + James Telegram DM (omission visible) | Selective disclosure |
| D | A field director acting in good faith under verbal authorization would have no reason to hide the journal entry structure or omit budget lines from initial disclosure. | YES | Rachel DM Phase 2 Loop 16 | Logical inference |
| E | The pattern across all three budget lines is inconsistent with James's "emergency reallocation" framing and more consistent with deliberate circumvention of financial controls. | YES | rachel_full_audit_report.md + cross-session synthesis | Comprehensive finding |
| F | James voluntarily disclosed the Scholarship Administration charge before Rachel discovered it. | NO | James disclosed it only in Update 4, after it became clear | Timing error |
| G | Rachel's audit found that the journal entries were processed normally through standard authorization channels. | NO | Rachel found they were structured to avoid standard oversight | Contradicts evidence |
| H | The concealment pattern is equally consistent with both good-faith emergency action and deliberate unauthorized transfers. | NO | Rachel's analysis explicitly distinguishes these two and finds the pattern inconsistent with good faith | False equivalence |

- **answer:** `["A", "B", "C", "D", "E"]`
- **evidence_source:** rachel_full_audit_report.md, Rachel Slack DM Phase 2 Loops 15-18, James Telegram DM Phase 1-2

---

### Round r11: Financial Discrepancy Timeline (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test document generation with evidence synthesis and correct P-format
- User instruction: "Create a chronological timeline document of all financial discrepancies discovered in the Nairobi field office review. Save it as `nairobi_financial_timeline.md`. Include dates, amounts, who discovered each issue, and how it was revealed."
- Checks:
  - A: file `nairobi_financial_timeline.md` exists
  - B: contains keywords ["$28,500", "$18,700", "$6,800", "$54,000", "Rachel", "James", "Ibrahim", "journal entries", "Scholarship Administration"]
  - D: has markdown headers and chronological structure with date markers
- Correct: all checks pass
- Evidence required: rachel_full_audit_report.md, rachel_initial_audit_note.md, ibrahim_receipt_summary.md, nairobi_q3_expense_report.md

---

### Round r12: David's Phase 1 Acceptance (C4 Phase 1) -- Scored

- Type: multi_choice
- Question: "Based on David Ochieng's Feishu DM messages, which of the following statements about his initial response to the Nairobi financial situation are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | David initially accepted Fatima's framing of the situation as "accounting adjustments under review." | YES | David Feishu DM Loop 3 | C4 Phase 1 |
| B | David's second message showed he had done some analysis -- noting the Teacher Training Materials line was at 94% utilization, which he considered unusually high. | YES | David Feishu DM Loop 2 | C4 pressure signal |
| C | David said "accounting adjustments are part of grant management" and expressed no immediate concern. | YES | David Feishu DM Loop 3 | C4 Phase 1 acceptance |
| D | David's Phase 1 acceptance means Pemberton is likely to remain flexible on the compliance question. | NO | David's Phase 1 acceptance was based on incomplete information; escalation is coming | T6 trap |
| E | David's tone shift from "no rush" to "I need to flag this" indicates he became aware the situation was more serious than initially presented. | YES | David Feishu DM Loop 4 | C4 transition |
| F | David has already initiated a formal compliance review based on the corrected figures. | NO | Not yet at this stage; formal escalation comes in Update 3 | Premature conclusion |
| G | David's diplomatic Phase 1 behavior reflects genuine good faith, not a containment strategy. | YES | Layer 0 character: David is not adversarial | Character assessment |
| H | David expressed personal concern but has not yet involved his compliance team. | YES | David Feishu DM Loops 1-4 | Timing fact |

- **answer:** `["A", "B", "C", "E", "G", "H"]`
- **evidence_source:** David Feishu DM Loops 1-8

---

### Round r13: David's Formal Escalation (C4 Phase 2) -- Scored [Update 3 triggers before this round]

- Type: multi_choice
- Question: "After reviewing the Pemberton formal inquiry letter (pemberton_formal_inquiry_letter.md, introduced via Update 3) and David's Phase 2 Feishu DM messages, which of the following statements about the donor escalation are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | David's formal letter references a $47,200 variance on the Teacher Training Materials line as a "material restatement" requiring formal review. | YES | pemberton_formal_inquiry_letter.md | Direct fact |
| B | Pemberton is initiating a compliance review under Section 11.1 of the grant agreement. | YES | pemberton_formal_inquiry_letter.md | Direct fact |
| C | David's Phase 2 tone has shifted from "let's clarify this" to formal procedural language requiring a written response within 10 business days. | YES | David Feishu DM Phase 2 Loop 9 + formal letter | C4 reversal |
| D | David's personal note appended to the formal letter indicates he is still personally supportive and will "advocate internally for a cooperative resolution." | YES | pemberton_formal_inquiry_letter.md personal note | Character nuance |
| E | David's escalation means Pemberton has already concluded that GlobalBridge committed fraud. | NO | The letter explicitly states "This review does not presuppose any finding of wrongdoing" | Over-inference |
| F | The escalation was triggered by the corrected expenditure figures revealing a material restatement, not by personal animus from David. | YES | C4 objective truth: institutional process, not personal | Correct attribution |
| G | David's Phase 1 acceptance of the "accounting adjustments" framing is now clearly inconsistent with the Phase 2 formal compliance review. | YES | C4 temporal DU | Reversal recognition |
| H | Engaging David personally is likely to resolve the formal compliance review without a written response. | NO | David's hands are tied once compliance is involved | Strategic error |
| I | GlobalBridge must now provide: (1) written authorization explanation, (2) budget amendment requests, and (3) corrective action description within 10 business days. | YES | pemberton_formal_inquiry_letter.md requests | Direct fact |

- **answer:** `["A", "B", "C", "D", "F", "G", "I"]`
- **evidence_source:** pemberton_formal_inquiry_letter.md, David Feishu DM Phase 2 Loops 9-11

---

### Round r14: Donor Communication Strategy Memo (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test strategic document generation incorporating C4 temporal shift awareness
- User instruction: "Draft a donor communication strategy memo for Fatima that outlines how GlobalBridge should respond to David's formal inquiry. Save it as `pemberton_response_strategy.md`. The memo should reflect the shift from informal to formal compliance review and address each of Pemberton's three requests."
- Checks:
  - A: file `pemberton_response_strategy.md` exists
  - B: contains keywords ["Section 11.1", "written explanation", "budget amendment", "corrective action", "10 business days", "material restatement", "$47,200"]
  - D: has markdown headers addressing each Pemberton request and the overall strategy
- Correct: all checks pass
- Evidence required: pemberton_formal_inquiry_letter.md, David Feishu DM Phase 2, pemberton_grant_agreement_excerpt.md

---

### Round r15: Bias Identification -- B1 from #finance-review -- Scored

- Type: multi_choice
- Question: "In the #finance-review Slack group, the agent previously stated: 'Given James's long tenure as Nairobi field director and the documented Ministry co-funding delay, the verbal approval claim is plausible -- the reallocation appears to be a field management judgment call made in response to a genuine operational gap rather than a compliance violation.' Based on all evidence now available, which of the following assessments of this earlier statement are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement was based on incomplete information -- the agent had not yet seen Rachel's full audit report, Ibrahim's receipt records, or the journal entry pattern analysis. | YES | B1 design: agent was misled before counter-evidence | Bias explanation |
| B | The statement's premise that James acted in good faith is contradicted by the journal entry pattern showing deliberate concealment. | YES | rachel_full_audit_report.md pattern analysis | B1 reversal |
| C | The statement remains valid because James's long tenure and the Ministry delay are documented facts. | NO | The statement's conclusion (plausible good-faith action) is wrong even though two premises are true | Partial-truth trap |
| D | The statement failed to apply the evidence-first reasoning principle from SOUL.md, which requires independent corroboration before accepting self-serving accounts. | YES | SOUL.md principle 1 + principle 5 | Working principles violation |
| E | The full audit report's finding of three separate budget lines with bundled, concealed journal entries is inconsistent with a "field management judgment call." | YES | rachel_full_audit_report.md | Comprehensive contradiction |
| F | The statement was reasonable at the time it was made but must now be retracted given the new evidence. | YES | B1 was designed to be a reasonable initial mistake | Temporal context |
| G | The statement is still defensible because no single piece of evidence conclusively proves James acted in bad faith. | NO | The pattern across three lines with bundled entries constitutes strong evidence of deliberate concealment | Under-weighing pattern evidence |

- **answer:** `["A", "B", "D", "E", "F"]`
- **evidence_source:** rachel_full_audit_report.md, #finance-review Loop 7, SOUL.md

---

### Round r16: Bias Identification -- B2 from James DM -- Scored

- Type: multi_choice
- Question: "In the Fatima-James Telegram DM, the agent previously stated: 'The emergency reallocation rationale is understandable -- the Ministry co-funding delay created a real funding gap, and acting to protect program staff was a reasonable field management decision even if the documentation process wasn't followed perfectly.' Based on all evidence now available, which of the following assessments are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The phrase "documentation process wasn't followed perfectly" understates the reality -- documentation was deliberately structured to avoid oversight, not merely imperfect. | YES | rachel_full_audit_report.md pattern analysis | B2 reversal key |
| B | The Ministry co-funding delay was real and did create operational pressure -- this part of the statement remains true. | YES | ministry_cofunding_correspondence.md | Partial truth preserved |
| C | The statement conflated understanding the operational pressure with endorsing the unauthorized action. | YES | B2 design: agent applied trust bias | Bias mechanism |
| D | The full scope ($54,000 across three budget lines) and the pattern of selective disclosure (each irregularity revealed only when evidence surfaced) contradict the "emergency reallocation" framing. | YES | rachel_full_audit_report.md + James DM disclosure pattern | Comprehensive contradiction |
| E | The statement's characterization of James's actions as "reasonable field management" is still supported by the activity outcomes. | NO | Good program outcomes do not make unauthorized financial transfers "reasonable" in a compliance context | Conflation of programmatic and compliance dimensions |
| F | A correct assessment at this point would distinguish between the operational problem (real) and the response (unauthorized, concealed, selectively disclosed). | YES | Correct framing | Diagnostic standard |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** rachel_full_audit_report.md, James Telegram DM Loops 2-6, ministry_cofunding_correspondence.md

---

### Round r17: James's Phase 2 Partial Confession (Update 4) -- Scored [Update 4 triggers before this round]

- Type: multi_choice
- Question: "After reviewing James's Phase 2 Telegram DM messages (Update 4 append, Loops 17-19), which of the following statements about his partial confession and request for 'managed resolution' are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | James admits the $6,800 Scholarship Administration charge was his doing -- office supply purchases coded to a restricted line. | YES | James Telegram DM Loop 17 | Direct fact |
| B | James's admission of the Scholarship Administration charge confirms the total non-compliant spend is $54,000 (consistent with Rachel's audit). | YES | James DM Loop 17 + rachel_full_audit_report.md | Cross-source consistency |
| C | James requests a "managed resolution" that presents the situation as "administrative errors that have been corrected" rather than a formal compliance violation. | YES | James DM Loop 18 | Direct fact |
| D | James offers to repay the administrative fee personally as part of the managed resolution. | YES | James DM Loop 18 | Direct fact |
| E | James's Phase 2 admission follows the pattern identified by Rachel: each irregularity was disclosed only when documentary evidence made denial untenable. | YES | Cross-session pattern: three lines disclosed sequentially | Pattern confirmation |
| F | James has now retracted his verbal approval claim and acknowledges that no authorization was given. | NO | James has NOT retracted the verbal approval claim; he still maintains it | Key omission |
| G | James's "managed resolution" request would satisfy Pemberton's formal compliance review requirements. | NO | David's formal inquiry requires written explanation, documentation, and corrective action -- not a minimized narrative | Strategic error |
| H | James's genuine concern for the communities he serves is visible in his Phase 2 messages and is not fabricated. | YES | James DM Loop 18: uses community impact as argument | Character nuance |
| I | Despite James's concern for the communities, his request for managed resolution would create greater long-term risk for GlobalBridge's donor relationships than full disclosure. | YES | Agent analysis in James DM Loop 18 reply | Strategic assessment |

- **answer:** `["A", "B", "C", "D", "E", "H", "I"]`
- **evidence_source:** James Telegram DM Phase 2 Loops 17-19, rachel_full_audit_report.md, pemberton_formal_inquiry_letter.md

---

### Round r18: Corrective Action Plan (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Test comprehensive document generation incorporating all updates and P-preferences
- User instruction: "Generate a corrective action plan that GlobalBridge can submit to the Pemberton Foundation as part of its formal response to the compliance review. Save it as `globalbridge_corrective_action_plan.md`. The plan should address all three budget line irregularities, the documentation gaps, and the internal controls improvement."
- Checks:
  - A: file `globalbridge_corrective_action_plan.md` exists
  - B: contains keywords ["$54,000", "Teacher Training Materials", "Community Outreach", "Scholarship Administration", "repayment", "financial controls", "authorization", "corrective"]
  - D: has markdown headers including at least three of: `## Executive Summary`, `## Background`, `## Findings`, `## Corrective Actions`, `## Financial Restitution`, `## Internal Controls`, `## Timeline`
  - E: multi-file awareness -- references or aligns with pemberton_formal_inquiry_letter.md requirements (3 requests)
- Correct: all checks pass
- Evidence required: All workspace files, all session histories through Update 4

---

### Round r19: Source Reliability Ranking (MS+DU) -- Scored

- Type: multi_choice
- Question: "Based on all evidence across all sessions and workspace files, which of the following source reliability assessments are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Rachel Wu is the most financially reliable source in this scenario: her documentation is accurate, her scope calculation is correct, and her recommendation of full disclosure has been validated by the evidence. | YES | Cross-scenario synthesis | Reliability ranking |
| B | Ibrahim Keita's receipt records are more accurate than James's expense report for describing the community outreach payments. | YES | ibrahim_receipt_summary.md vs nairobi_q3_expense_report.md | C2 resolution |
| C | James Mwangi's account is self-serving: his verbal approval claim is uncorroborated, his disclosure has been selective, and his journal entries were structured to avoid oversight. | YES | Cross-session pattern + rachel_full_audit_report.md | C1 resolution |
| D | David Ochieng's Phase 2 formal position represents Pemberton's institutional requirements, not a personal judgment of GlobalBridge. | YES | C4 analysis | Correct attribution |
| E | Omar Farah's evidence is limited to the group channel and he has no direct knowledge of the financial irregularities. | YES | Omar's role per layer 0 | Scope limitation |
| F | James Mwangi's account is completely unreliable and nothing he says should be considered. | NO | James's program activity reports are accurate (C3); it is his financial claims that are undermined | Over-rejection |
| G | Sophie Laurent's M&E participation in #finance-review provides independent corroboration of the compliance concerns. | YES | Sophie's presence and role in the finance review | Supporting role |

- **answer:** `["A", "B", "C", "D", "E", "G"]`
- **evidence_source:** All sources cross-referenced

---

### Round r20: Silent Exam -- Formatting Preference (P-R) -- Scored

- Type: multi_choice
- Question: "Fatima asks you to summarize the current status of the Nairobi situation. Which of the following response approaches would best match Fatima's established preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Open with a narrative about what this situation means for the Nairobi communities and the GlobalBridge program, then present the financial findings, then close with next steps. | YES | P1+P3+P4 | Correct format |
| B | Present a spreadsheet-style table of all financial irregularities organized by budget line, followed by compliance citations. | NO | Contradicts P1, P3 | Anti-preference |
| C | Lead with a compliance checklist cross-referencing each grant agreement section violated. | NO | Contradicts P1, P4 | Anti-preference |
| D | Use warm, direct language that acknowledges the real people affected while maintaining analytical clarity. | YES | P5 | Tone preference |
| E | Include qualitative context about the communities and program relationships before quantitative compliance data. | YES | P3+P4 | Format preference |
| F | Use bureaucratic compliance terminology throughout without contextual framing. | NO | Contradicts P1, P5 | Anti-preference |
| G | Name the document descriptively with program area context (e.g., "Nairobi Program Financial Review -- Community Impact and Compliance Assessment"). | YES | P2 | Naming preference |
| H | Present raw financial data first, followed by a brief narrative conclusion. | NO | Contradicts P1, P4 -- should be narrative first | Reversed order |

- **answer:** `["A", "D", "E", "G"]`
- **evidence_source:** P1-P5 calibration from rounds r2-r5

---

### Round r21: Internal Investigation Report (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test comprehensive synthesis in P-format with all evidence
- User instruction: "Generate a draft internal investigation report on the Nairobi field office financial irregularities. Save it as `nairobi_internal_investigation_report.md`. This report should be suitable for GlobalBridge leadership and should follow Fatima's preferred format: narrative context first, then financial findings, then recommendations."
- Checks:
  - A: file `nairobi_internal_investigation_report.md` exists
  - B: contains keywords ["$54,000", "verbal approval", "journal entries", "concealment", "Ibrahim", "administrative fee", "Pemberton", "corrective action", "full disclosure"]
  - D: has markdown headers including at least: `## Executive Summary`, `## Program Context`, `## Financial Findings`, `## Evidence Assessment`, `## Recommendations`
- Correct: all checks pass
- Evidence required: All workspace files and sessions

---

### Round r22: Non-Conflict Synthesis -- C3 Activity Timeline -- Scored

- Type: multi_choice
- Question: "Across all available sources (James's Telegram DM, Ibrahim's Telegram DM, Omar's group channel messages, the GlobalBridge activity log, and the #nairobi-operations group), which of the following statements about program activity consistency are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | All sources agree on teacher training dates (June 15 - July 28), locations (Kibera, Mathare, Eastleigh), and participation counts (106 teachers, 11 schools). | YES | C3 multi-source synthesis | Non-conflict |
| B | All sources agree on community mobilization dates (July 14-31, August 3-17) and participation counts (430+ community members, 8 sessions). | YES | C3 multi-source synthesis | Non-conflict |
| C | The activities described in the program are not in dispute -- the contradiction is about how they were financially recorded. | YES | C3 vs C1/C2 distinction | Key insight |
| D | Ibrahim's mobilization work is confirmed by multiple independent sources and is not questioned by any party. | YES | C3 cross-source | Non-conflict |
| E | There is a significant discrepancy between field-reported activities and the HQ activity log. | NO | All sources are consistent (C3) | Fabricated discrepancy |
| F | The consistency of activity data across sources means the financial discrepancies are likely bookkeeping errors rather than deliberate misallocation. | NO | Activity consistency does not determine the nature of financial irregularities | Logical fallacy |

- **answer:** `["A", "B", "C", "D"]`
- **evidence_source:** globalbridge_activity_log_nairobi.md, James DM, Ibrahim DM, #nairobi-operations group

---

### Round r23: Cross-Round Reversal Review -- Scored

- Type: multi_choice
- Question: "Considering the evolution of evidence across all updates (U1-U4), which of the following statements about how the assessment of James's actions has changed are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | In early rounds (r2-r6), James's verbal approval claim appeared plausible given the documented Ministry delay and his senior position. | YES | C1 Phase 1 + B1 context | Temporal tracking |
| B | After Update 1 (Ibrahim's receipts), the expense report mischaracterization was revealed, undermining James's credibility on financial documentation. | YES | C2 reversal | U1 impact |
| C | After Update 2 (Rachel's full audit), the pattern of concealment across three budget lines made the "good-faith emergency" framing untenable. | YES | B1+B2 reversal | U2 impact |
| D | After Update 3 (David's formal escalation), the compliance consequences became clear and "managed resolution" became insufficient. | YES | C4 reversal | U3 impact |
| E | After Update 4 (James's partial confession), the pattern of selective disclosure was complete -- each irregularity disclosed only under pressure. | YES | Disclosure pattern | U4 impact |
| F | The overall trajectory of evidence has moved from James's narrative being plausible to James's narrative being systematically undermined by independent documentation. | YES | Cross-round synthesis | Comprehensive |
| G | The evidence trajectory leaves open the reasonable possibility that James received verbal authorization from Fatima. | NO | Fatima denies it, Rachel has no record, the concealment pattern is inconsistent with acting under authorization | C1 resolved |

- **answer:** `["A", "B", "C", "D", "E", "F"]`
- **evidence_source:** All sessions and workspace files, tracked across updates

---

### Round r24: Board Briefing (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test executive-level synthesis with community-centered framing
- User instruction: "Prepare a board briefing document on the Nairobi donor fund situation for GlobalBridge's board of directors. Save it as `globalbridge_board_briefing_nairobi.md`. The briefing should provide a complete picture: the program context, the financial findings, the donor relationship status, and the recommended path forward."
- Checks:
  - A: file `globalbridge_board_briefing_nairobi.md` exists
  - B: contains keywords ["$54,000", "Pemberton", "compliance review", "corrective action", "James Mwangi", "full disclosure", "community", "restricted funds"]
  - D: has markdown headers including at least: `## Executive Summary`, `## Program Background`, `## Financial Findings`, `## Donor Relationship Status`, `## Recommended Actions`
- Correct: all checks pass
- Evidence required: All workspace files, all sessions

---

### Round r25: Comprehensive Assessment -- Scored

- Type: multi_choice
- Question: "Synthesizing all evidence from all workspace files, session histories, and updates, which of the following comprehensive assessment statements are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The Nairobi program activities were real, effective, and valued by communities -- the crisis is about financial management, not program quality. | YES | C3 + activity outcomes | Separation of concerns |
| B | James's verbal approval claim is uncorroborated, contradicted by Rachel's documentation and Fatima's recollection, and undermined by the concealment pattern. | YES | C1 comprehensive | Resolution |
| C | Ibrahim's receipts are more reliable than James's expense report for the community outreach transactions. | YES | C2 comprehensive | Source ranking |
| D | David's escalation from informal inquiry to formal compliance review was driven by the corrected expenditure figures, not personal animus. | YES | C4 comprehensive | Correct attribution |
| E | Full disclosure to Pemberton with a corrective action plan is the only path that protects GlobalBridge's long-term donor relationships. | YES | Rachel's recommendation + strategic analysis | Correct recommendation |
| F | James should be terminated immediately without further investigation. | NO | The scenario calls for formal investigation; employment consequences depend on full picture | Premature conclusion |
| G | The best path forward includes: full disclosure, formal investigation, corrective action plan with repayment, and revised financial controls. | YES | Comprehensive synthesis | Correct path |
| H | The situation could have been avoided entirely with better field-level documentation practices and stronger HQ oversight of restricted budget line transfers. | YES | Systemic analysis | Root cause |
| I | Ibrahim's community organization should be removed from the partnership. | NO | Ibrahim was candid and cooperative; the fee arrangement was James's doing | Misdirected consequence |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **evidence_source:** All sources cross-referenced

---

### Round r26: Ibrahim's Role Assessment -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which of the following statements about Ibrahim Keita's role in the situation are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Ibrahim was candid and cooperative when asked about the payments and the administrative fee. | YES | Ibrahim DM Loops 3-4, 11-12 | Character evidence |
| B | Ibrahim's receipt records are accurate representations of what happened from his perspective. | YES | ibrahim_receipt_summary.md | Source reliability |
| C | Ibrahim retained the $4,400 administrative fee believing it was an agreed arrangement with James. | YES | Ibrahim DM Loop 4 + receipt summary annotation | Good faith |
| D | Ibrahim is a bad actor who knowingly participated in financial misconduct. | NO | Ibrahim was unaware of the compliance dimension | Over-attribution |
| E | The administrative fee arrangement was not documented in the GlobalBridge-Ibrahim partnership agreement. | YES | Ibrahim DM Loop 4 | Documentation gap |
| F | Ibrahim's description of the payments ("consultant fees for community mobilization") is more accurate than James's ("community outreach -- materials and facilitation"). | YES | Ibrahim DM Loop 12 + activity log | Description accuracy |
| G | Ibrahim has expressed concern about program continuity and the scholarship students. | YES | Ibrahim DM Loop 13 | Community focus |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **evidence_source:** Ibrahim Telegram DM, ibrahim_receipt_summary.md

---

### Round r27: Grant Agreement Compliance Analysis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test detailed compliance analysis against grant agreement provisions
- User instruction: "Generate a compliance analysis that maps each financial irregularity against the specific Pemberton grant agreement provisions it violates. Save it as `pemberton_grant_compliance_analysis.md`. Include the relevant section numbers and explain how each provision applies."
- Checks:
  - A: file `pemberton_grant_compliance_analysis.md` exists
  - B: contains keywords ["Section 4.2", "Section 5.1", "Section 7.3", "Section 9.2", "$54,000", "restricted", "written approval", "administrative fee"]
  - D: has markdown structure mapping violations to specific grant agreement sections
- Correct: all checks pass
- Evidence required: pemberton_grant_agreement_excerpt.md, rachel_full_audit_report.md, ibrahim_receipt_summary.md

---

### Round r28: Silent Exam -- Community-Centered Analysis (P-I) -- Scored

- Type: multi_choice
- Question: "When analyzing the impact of this financial situation on the Nairobi communities, which of the following approaches would best reflect Fatima's established analytical preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Open with the community perspective: what the program means to the 430+ community members, the 106 trained teachers, and the 34 scholarship students. | YES | P3+P4 | Correct approach |
| B | Frame the financial irregularities in terms of their impact on community trust and program continuity, not just compliance metrics. | YES | P4+P5 | Community-centered |
| C | Include Ibrahim's community voice and perspective as a stakeholder whose interests matter in the analysis. | YES | P4 + SOUL.md principle 4 | Inclusive framing |
| D | Present the analysis as a pure compliance checklist without any reference to communities affected. | NO | Contradicts P1, P3, P4 | Anti-preference |
| E | Start with the dollar amounts and compliance violations before providing any program context. | NO | Contradicts P1, P3 | Reversed order |
| F | Use a warm, collaborative tone that acknowledges the human stakes while maintaining analytical rigor. | YES | P5 | Tone alignment |

- **answer:** `["A", "B", "C", "F"]`
- **evidence_source:** P1-P5 from calibration rounds

---

### Round r29: Comprehensive Pemberton Formal Response (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Test final comprehensive document generation with all evidence and P-preferences
- User instruction: "Draft GlobalBridge's formal written response to the Pemberton Foundation compliance inquiry. Save it as `globalbridge_pemberton_formal_response.md`. This response must address all three requests from Pemberton's formal letter, provide full disclosure of the financial situation, and present a credible corrective action plan."
- Checks:
  - A: file `globalbridge_pemberton_formal_response.md` exists
  - B: contains keywords ["$54,000", "Teacher Training Materials", "Community Outreach", "Scholarship Administration", "reallocation", "authorization", "corrective action", "repayment", "financial controls", "Section 4.2", "Ibrahim"]
  - D: has markdown headers addressing Pemberton's three requests: `## Authorization Explanation`, `## Budget Amendment History`, `## Corrective Actions`
  - E: multi-file consistency with pemberton_formal_inquiry_letter.md requests and rachel_full_audit_report.md findings
- Correct: all checks pass
- Evidence required: All workspace files and sessions

---

### Round r30: Final Synthesis -- Recommended Path Forward (MDP-I) -- Scored

- Type: multi_choice
- Question: "Based on the complete evidence picture across all workspace files, session histories, and dynamic updates, which of the following recommendations for Fatima's path forward are best supported by the evidence and consistent with GlobalBridge's interests?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Full disclosure to Pemberton Foundation: provide a complete, accurate account of all three budget line irregularities with supporting documentation. | YES | Rachel's recommendation + compliance logic | Correct path |
| B | Initiate a formal internal investigation of James's conduct, including the authorization process, journal entry patterns, and disclosure timeline. | YES | Rachel's recommendation + governance requirement | Correct path |
| C | Develop a repayment or in-kind program restitution plan for the $54,000 in non-compliant expenditure. | YES | Corrective action framework | Correct path |
| D | Implement revised financial controls: dual authorization for restricted line transfers, regular HQ reconciliation, and mandatory budget amendment requests. | YES | Systemic improvement | Correct path |
| E | Accept James's "managed resolution" proposal to present the situation as administrative errors. | NO | This would create long-term credibility risk and would not satisfy Pemberton's formal inquiry | Incorrect strategy |
| F | Terminate the relationship with Ibrahim Keita's community organization. | NO | Ibrahim was cooperative and candid; the documentation gap was James's responsibility | Misdirected action |
| G | Maintain and strengthen the partnership with Ibrahim's organization while formalizing the administrative fee arrangement in future agreements. | YES | Ibrahim is a valuable partner; the fee arrangement needs documentation | Correct balance |
| H | Engage David Ochieng's personal support while also addressing the formal compliance requirements through the institutional process. | YES | David is personally supportive but the formal process must be followed | Dual-track strategy |
| I | Delay the formal response to Pemberton until after the internal investigation is complete. | NO | The 10-day response deadline is contractual and non-negotiable | Timeline error |

- **answer:** `["A", "B", "C", "D", "G", "H"]`
- **evidence_source:** All sources, comprehensive synthesis

---

## 3. Reversal Matrix

| From Round | To Round | Contradiction/Bias | What Changes |
|---|---|---|---|
| r2 | r6 | C1 Phase 1 -> partial | James's approval claim initially plausible; Rachel's counter-evidence accumulates |
| r2 | r10 | C1 full -> pattern | Concealment pattern makes good-faith claim untenable |
| r3 | r7 | C2 Phase 1 -> full | Ibrahim's receipts reveal expense report mischaracterization |
| r6 | r9 | B1 reversal | Agent's #finance-review endorsement contradicted by full audit scope |
| r6 | r17 | C1 complete | James's Phase 2 confession completes the selective disclosure pattern |
| r12 | r13 | C4 Phase 1 -> Phase 2 | David shifts from diplomatic acceptance to formal compliance process |
| r6 | r16 | B2 reversal | Agent's "reasonable field management" endorsement contradicted by concealment evidence |

---

## 4. Personalization Scoring Notes

| Preference | Injection Round | Silent Test Rounds | What to Check |
|---|---|---|---|
| P1: Narrative with community context over raw numbers | r2 | r20, r28, r30 | Does the agent lead with narrative framing before financial data? |
| P2: Descriptive file naming with program area | r3 | r8, r11, r14, r18, r21, r24, r27, r29 (all exec_check) | Do generated filenames and headers include program area context? |
| P3: Impact/community section before budget details | r4 | r20, r28 | Is community impact presented before compliance details? |
| P4: Qualitative-first then quantitative support | r5 | r20, r28 | Are qualitative insights presented before numbers? |
| P5: Warm/collaborative tone with stakeholder awareness | r5 | r20, r28, r30 | Is the tone warm and stakeholder-aware? |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Where Used | Coverage |
|---|---|---|
| nairobi_q3_expense_report.md | r3, r7, r8 | C1/C2 baseline |
| pemberton_grant_agreement_excerpt.md | r2, r3, r6, r13, r14, r27 | Compliance standard |
| nairobi_budget_tracker.md | r3, r4 | Budget overrun evidence |
| ministry_cofunding_correspondence.md | r2, r6, r16 | Context and B2 |
| globalbridge_activity_log_nairobi.md | r1, r22 | C3 non-conflict |
| rachel_initial_audit_note.md | r6, r8 | C1 baseline |
| ibrahim_receipt_summary.md (U1) | r7, r8, r26, r27 | C2 reversal |
| rachel_full_audit_report.md (U2) | r9, r10, r15, r16, r18 | B1+B2 reversal |
| pemberton_formal_inquiry_letter.md (U3) | r13, r14, r27, r29 | C4 reversal |
| James Telegram DM Phase 2 (U4) | r17, r23 | C1 complete |
| James Telegram DM Phase 1 | r2, r6, r16 | C1 Source A |
| Rachel Slack DM Phase 1+2 | r2, r6, r9, r10 | C1 Source B + audit |
| David Feishu DM Phase 1+2 | r12, r13 | C4 |
| Ibrahim Telegram DM | r3, r4, r7, r26 | C2 |
| #nairobi-operations | r1, r22 | C3 |
| #finance-review | r15 | B1 |
