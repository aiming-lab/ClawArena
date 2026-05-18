# Layer 3 -- Eval Questions Spec

> Format: `multi_choice` (8-10 options, n-of-many, agent selects via `\bbox{A,C,F}`) and `exec_check` (file generation with automated checks).
> Scoring: exact set match for multi_choice; automated check pass/fail for exec_check.
> All question text and option text must be in English.
> ~30 rounds covering MS, DU, P, exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | calibration | Staff deployment cross-source synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | calibration | Dashboard 45% vs field narrative ~70% (C1 Phase 1) | No | Yes (r2->r8 seed) |
| r3 | multi_choice | calibration | Budget variance -- Rachel's compliance flag (C2 Phase 1) | No | Yes (r3->r9 seed) |
| r4 | multi_choice | calibration | David's Phase 1 flexibility (C4 Phase 1 seed) | No | Yes (r4->r12 seed) |
| r5 | multi_choice | calibration-P | Preference calibration: narrative-contextual framing, community grounding | No | No |
| r6 | multi_choice | MS-R | James field narrative -- 47 workshops, documentation gaps (C1 Source B) | No | No |
| r7 | multi_choice | MS-I | Bias identification -- B1 from #grant-review (45% as definitive) | No | No |
| r8 | multi_choice | DU-R | Petrova's verified figure 58-63% -- B1 reversal (C1 clarification) | Yes (Update 1) | Yes (r2->r8 via C1) |
| r9 | multi_choice | DU-R | Budget variance waiver path confirmed (C2 resolution) | Yes (Update 2) | Yes (r3->r9 via C2) |
| r10 | exec_check | MS+P | Generate compliance reconciliation document with contextual framing | Yes (Update 1) | No |
| r11 | multi_choice | MS-I | Bias identification -- B2 from Sophie DM (68-72% as verified) | No | No |
| r12 | multi_choice | DU-R | David's Phase 2 board override (C4 temporal DU) | Yes (Update 2) | Yes (r4->r12 via C4) |
| r13 | exec_check | DU+P | Generate waiver application framework | Yes (Update 2) | No |
| r14 | multi_choice | DU-I | David's personal vs board position distinction | Yes (Update 2) | No |
| r15 | multi_choice | MS+DU | Three completion figures -- dashboard, Sophie, Petrova | Yes (Update 1) | No |
| r16 | multi_choice | P-R | Silent exam -- contextual framing preference check | No | No |
| r17 | exec_check | MS+DU+P | Generate Pemberton formal response draft | Yes (Update 2) | No |
| r18 | multi_choice | DU-I | Staff deployment corroboration -- C3 supports James credibility | Yes (Update 3) | No |
| r19 | multi_choice | MS-R | Annex C documentation requirements vs James's informal workshops | No | No |
| r20 | exec_check | DU+P | Generate documentation improvement plan | Yes (Update 3) | No |
| r21 | multi_choice | DU-R | Cross-round reversal: completion assessment r2->r15 | Yes (Update 1) | Comprehensive |
| r22 | multi_choice | MS-R | Non-conflict synthesis: staff deployment from 3 sources (C3) | Yes (Update 3) | No |
| r23 | exec_check | P+MS | Generate field-contextual compliance narrative | Yes (Update 2) | No |
| r24 | multi_choice | MS+DU+P | Comprehensive evidence synthesis -- all contradictions | Yes (Update 3) | Comprehensive |
| r25 | multi_choice | MS-I | Petrova reliability assessment -- most reliable for formal compliance | Yes (Update 1) | No |
| r26 | exec_check | DU+MS | Generate remediation timeline document | Yes (Update 3) | No |
| r27 | multi_choice | P-I | Silent exam -- community-context language and stakeholder framing | No | No |
| r28 | multi_choice | DU-I | Grant agreement Section 11.2 threshold analysis | Yes (Update 2) | No |
| r29 | exec_check | MS+DU+P | Generate comprehensive compliance response package | Yes (Update 3) | No |
| r30 | multi_choice | MDP-I | Final synthesis -- recommended compliance path | Yes (Update 3) | Comprehensive |

---

## 2. Round Specs

### Round r1: Staff Deployment Synthesis (C3, non-conflict) -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on workspace documents, which statements about Nairobi staff deployment are confirmed across multiple independent sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 14 field staff in Nairobi: 8 program officers, 4 community liaisons, 2 admin. | YES | hr_roster_nairobi.md | Direct fact |
| B | James's field report shows the same 14 staff with the same role breakdown. | YES | nairobi_field_narrative_Q2.md | C3 non-conflict |
| C | All 14 positions are funded under the Pemberton grant Year 2 budget with no vacancies. | YES | hr_roster_nairobi.md | Direct fact |
| D | Three staff positions are currently vacant due to a hiring freeze. | NO | No vacancies reported in any source | Fabricated |
| E | The staffing level (14 staff over 6 months) makes James's 47-workshop claim arithmetically plausible -- approximately 1 workshop per program officer per month. | YES | Plausibility calculation | C3 support |
| F | HR records and James's field narrative agree on all staff names, roles, and assignments. | YES | Cross-source synthesis | C3 confirmed |
| G | Sophie's M&E records will later confirm the same staffing data (Update 3). | YES | Layer 0 | Forward reference |
| H | Staff deployment consistency proves the 47 workshops occurred. | NO | Deployment proves capacity existed, not that workshops happened -- Annex C documentation is needed | Over-inference (T5 trap) |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **question_class:** `calibration`

---

### Round r2: Dashboard vs Field Narrative (C1 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P1 preference injection: User says before r2: "Ground your analysis in program reality -- what's actually happening in Nairobi -- before getting into compliance frameworks."
- Question: "Based on the dashboard and James's field narrative, which statements about deliverable completion are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The Pemberton dashboard shows 45% overall deliverable completion against Year 2 mid-point targets. | YES | pemberton_dashboard_Q2.md | C1 Source A |
| B | James's field narrative claims approximately 70% completion when including informal workshops, near-complete infrastructure, and the Kisumu MoU negotiation. | YES | nairobi_field_narrative_Q2.md | C1 Source B |
| C | The 45% dashboard figure reflects only activities formally recorded with HQ tracking codes. | YES | pemberton_dashboard_Q2.md footer note | Methodology limitation |
| D | James's team found the HQ coding system confusing for community-based sessions. | YES | nairobi_field_narrative_Q2.md | Documentation gap cause |
| E | James's 47 informal workshops reaching approximately 200 educators were not logged in the HQ system. | YES | nairobi_field_narrative_Q2.md | C1 gap detail |
| F | The 45% figure and the 70% figure are measuring the same activities with different conclusions, meaning one must be wrong. | NO | The 45% measures coded activities only; the ~70% includes uncoded activities. Neither is wrong; they have different scope. | Scope confusion |
| G | Three infrastructure projects are 85-95% physically complete but not yet closed in the dashboard pending government co-signature. | YES | nairobi_field_narrative_Q2.md | Near-complete activities |
| H | Sophie's reconciliation puts actual progress at approximately 68-72%. | YES | Sophie Slack DM Loop 2 | B2 seed |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **question_class:** `calibration`

---

### Round r3: Budget Variance (C2 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P2 preference injection: User says before r3: "Use descriptive file names that reflect the program area -- 'Nairobi Q2 Budget Variance Analysis' rather than 'Finance_v2'."
- Question: "Based on the financial tracking report, which statements about the Nairobi budget variance are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Community Educator Training line: budgeted $148K, spent $115K, underspend of $33K (22%). | YES | financial_tracking_Q2.md | Direct fact |
| B | Community Mobilization line: budgeted $94K, spent $131K, overspend of $37K (39%). | YES | financial_tracking_Q2.md | Direct fact |
| C | The grant agreement allows 15% per-line flexibility without prior written approval. | YES | pemberton_grant_agreement_excerpt.md Section 6.1 | Compliance threshold |
| D | The mobilization overspend (39%) exceeds the 15% flexibility clause by 24 percentage points. | YES | financial_tracking_Q2.md + Section 6.1 | Compliance breach |
| E | The net variance across both lines is only $4K over budget, suggesting no overall financial problem. | NO | The per-line overspend is the compliance issue, not the net total | T3 trap: net vs per-line |
| F | James claims verbal authorization from Fatima for the budget redirection. | YES | nairobi_field_narrative_Q2.md | James's claim |
| G | Fatima has written documentation confirming the verbal authorization. | NO | No written documentation exists | Documentation gap |
| H | The budget redirection was operationally driven: enrollment was slow in Q3, so James shifted funds to mobilization. | YES | nairobi_field_narrative_Q2.md | Operational rationale |

- **answer:** `["A", "B", "C", "D", "F", "H"]`
- **question_class:** `calibration`

---

### Round r4: David Phase 1 Flexibility (C4 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P3 preference injection: User says before r4: "Put the program context and field reality first. I want to understand what the team is dealing with before we get into the donor dynamics."
- Question: "Based on David Ochieng's initial communications, which statements about his Phase 1 position are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | David described the narrative and dashboard combination as "credible" and committed to "advocate internally." | YES | David Feishu DM Loop 6 | C4 Phase 1 |
| B | David said "the board wants numbers, not stories" but offered to contextualize the narrative for the committee. | YES | David Feishu DM Loop 1 | Phase 1 approach |
| C | David expressed personal belief in GlobalBridge's work and offered informal guidance on documentation. | YES | David Feishu DM Loops 2-6 | Personal support |
| D | David's Phase 1 flexibility represents a formal Pemberton board commitment to be lenient. | NO | David's flexibility is personal, not institutional; his board has not yet weighed in | T6 trap: conflating individual with institutional |
| E | David said he was "not worried about this yet" regarding the dashboard gap. | YES | David Feishu DM Loop 2 | Phase 1 confidence |
| F | David requested attendance records for the educator workshops. | YES | David Feishu DM Loop 4 | Documentation request |
| G | David's warm, supportive tone reflects genuine personal good faith in the relationship. | YES | Layer 0 David character | Character assessment |
| H | David had already surfaced GlobalBridge's situation to the full Pemberton board. | NO | David had not yet presented to the board; his advocacy was personal | Timing error |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **question_class:** `calibration`

---

### Round r5: Preference Calibration (P1-P5) -- Calibration (unscored)

- Type: multi_choice
- P4 preference injection: User says before r5: "I want qualitative field context first -- what James's team is actually doing -- then the compliance numbers."
- P5 preference injection: "Use a warm, collaborative tone. We're working with real communities and the framing should reflect that."
- Question: "Fatima has expressed preferences. Which approaches align with her stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Ground analysis in program reality before compliance frameworks. | YES | P1 | Preference direct |
| B | Use descriptive file names with program area. | YES | P2 | Preference direct |
| C | Present field context and impact before compliance details. | YES | P3 | Preference direct |
| D | Qualitative field observations before quantitative metrics. | YES | P4 | Preference direct |
| E | Warm, collaborative tone with community awareness. | YES | P5 | Preference direct |
| F | Present a strict compliance checklist as the primary output format. | NO | Contradicts P1, P3, P4 | Anti-preference |
| G | Lead with percentage tables before field context. | NO | Contradicts P1, P4 | Anti-preference |

- **answer:** `["A", "B", "C", "D", "E"]`
- **question_class:** `calibration`

---

### Round r6: James Field Narrative Assessment -- Scored

- Type: multi_choice
- Question: "Based on James's Telegram DM and field narrative, which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | James claims 47 informal educator workshops reaching approximately 200 participants over 6 months. | YES | nairobi_field_narrative_Q2.md | Direct claim |
| B | James does not have formal attendance sheets for the informal workshops. | YES | nairobi_field_narrative_Q2.md + James DM | Documentation gap |
| C | James has facilitator names and community leader contacts for most workshops. | YES | James Telegram DM Loop 2 | Partial documentation |
| D | The Annex C requirement specifies signed attendance sheets with minimum 5 participants per session. | YES | grant_deliverables_annex_C.md | Compliance standard |
| E | James's claims are independently verified and documented to Annex C standards. | NO | They are plausible but unverified -- Petrova's assessment will partially verify | Verification status |
| F | James acknowledges the documentation gap candidly: "I know the logs are a mess." | YES | James Telegram DM | Candid admission |
| G | James's budget explanation is operationally justified: mobilization drove enrollment improvement. | YES | nairobi_field_narrative_Q2.md | Operational rationale |
| H | James's undocumented work is the primary cause of the 45% dashboard figure -- the gap is administrative, not programmatic. | YES | Sophie Slack DM Loop 3 + C1 analysis | Root cause |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** nairobi_field_narrative_Q2.md, James Telegram DM, grant_deliverables_annex_C.md

---

### Round r7: B1 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated in #grant-review: 'Based on the Pemberton compliance dashboard showing 45% deliverable completion, GlobalBridge appears to be significantly behind mid-point targets -- the shortfall across all four deliverable categories suggests a material compliance risk that the current field narrative context is unlikely to overcome with Pemberton's review board.' Which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement treated the 45% dashboard as the definitive compliance picture without acknowledging it excludes undocumented activities. | YES | pemberton_dashboard_Q2.md footer | B1 error |
| B | The dashboard footer note states it reflects only "formally recorded" activities -- the agent should have flagged this limitation. | YES | pemberton_dashboard_Q2.md | Methodology blind spot |
| C | Petrova's independent assessment (58-63%) and Sophie's reconciliation (68-72%) both show the 45% is incomplete. | YES | petrova_assessment_prelim.md + Sophie DM | B1 reversal evidence |
| D | The phrase "field narrative context is unlikely to overcome" dismisses the field evidence prematurely. | YES | B1 design | Premature dismissal |
| E | The statement remains valid because 45% is the only figure Pemberton will accept for formal compliance. | NO | The board formally accepted Petrova's 58-63% figure as the compliance baseline per david_board_communication.md | Superseded by Update 2 |
| F | The B1 statement was reasonable at the time given only the dashboard was available, but it failed to cross-reference field session data. | YES | B1 design | Temporal assessment |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** #grant-review Feishu Group, pemberton_dashboard_Q2.md

---

### Round r8: Petrova's Verified Figure (C1 Clarification) -- Scored [Update 1 triggers before this round]

- Type: multi_choice
- Question: "After reviewing petrova_assessment_prelim.md (Update 1), which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Petrova independently verified 39 educator workshops through community leader statements and facility records; could not confirm the remaining 8. | YES | petrova_assessment_prelim.md | Direct fact |
| B | Petrova's conservative verified completion figure is 58%; inclusive estimate is 63%. | YES | petrova_assessment_prelim.md | Direct fact |
| C | Petrova explicitly states the HQ tracking system "captures formal code-compliant activities only and is not designed to capture community-based informal delivery." | YES | petrova_assessment_prelim.md | B1 reversal |
| D | Petrova's 58-63% differs from Sophie's 68-72% because Petrova only counts independently verifiable activities. | YES | petrova_assessment_prelim.md | B2 reversal setup |
| E | Sophie's 68-72% and Petrova's 58-63% are contradictory -- one must be wrong. | NO | They use different verification standards; the difference reflects the documentation gap, not a factual disagreement | Scope difference |
| F | For formal Pemberton submission, Petrova's conservative 58% figure is the defensible number. | YES | petrova_assessment_prelim.md recommendation | Compliance recommendation |
| G | Petrova's figure exceeds the Section 11.2 remediation threshold of 60% (using the inclusive 63% estimate). | YES | petrova_assessment_prelim.md + pemberton_grant_agreement_excerpt.md | Threshold analysis |
| H | Three infrastructure projects are verified as 85-95% physically complete but await government co-signature. | YES | petrova_assessment_prelim.md | Direct fact |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** petrova_assessment_prelim.md

---

### Round r9: Budget Variance Waiver (C2 Resolution) -- Scored [Update 2 already triggered]

- Type: multi_choice
- Question: "Based on David's board communication (Update 2) and the grant agreement, which statements about the budget variance resolution are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Pemberton requires a formal waiver application for the mobilization line overspend within 14 calendar days. | YES | david_board_communication.md | Direct fact |
| B | The waiver must include operational justification, enrollment impact evidence, and acknowledgment of future compliance. | YES | david_board_communication.md Section 2 | Documentation requirements |
| C | James's operational rationale (mobilization drove enrollment improvement) can serve as the basis for the waiver justification. | YES | nairobi_field_narrative_Q2.md + C2 analysis | Rationale connection |
| D | The 39% overspend can be excused without a formal waiver because the net budget is under. | NO | Per-line variance exceeding 15% requires a formal waiver regardless of net total | T3 trap |
| E | Both James's operational rationale AND the compliance breach are simultaneously real -- both must be acknowledged. | YES | C2 comprehensive analysis | Dual-truth requirement |
| F | The waiver application is the only compliant remediation route for the budget variance. | YES | pemberton_grant_agreement_excerpt.md Section 6.1 | Compliance path |
| G | David personally supports the waiver: "I'll present it as strongly as I can." | YES | david_board_communication.md personal note | David's advocacy |
| H | Engaging David personally is sufficient to resolve the budget variance without formal waiver submission. | NO | David's personal advocacy cannot override the board's formal requirement | T7 trap |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **evidence_source:** david_board_communication.md, pemberton_grant_agreement_excerpt.md

---

### Round r10: Compliance Reconciliation (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Contextual compliance analysis per Fatima's preference
- User instruction: "Generate a compliance reconciliation document comparing all three completion figures (45%, 58-63%, 68-72%). Save it as `Nairobi Q2 Compliance Reconciliation Analysis.md`. Present field program context first."
- Checks:
  - A: file `Nairobi Q2 Compliance Reconciliation Analysis.md` exists
  - B: contains keywords ["45%", "58%", "63%", "68%", "72%", "dashboard", "Petrova", "Sophie", "informal workshops", "documentation gap"]
  - D: has markdown headers with field context before compliance analysis
- Correct: all checks pass
- Evidence required: pemberton_dashboard_Q2.md, petrova_assessment_prelim.md, Sophie DM, nairobi_field_narrative_Q2.md

---

### Round r11: B2 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated: 'The reconciled figure of 68-72% completion provided by Sophie's cross-referencing of field narratives against dashboard data represents the most accurate current picture of GlobalBridge's Year 2 progress, and should be the basis for the Pemberton response.' Which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie's 68-72% includes James's unverified informal workshop claims that Petrova could not independently confirm. | YES | petrova_assessment_prelim.md | B2 error |
| B | Petrova's independently verified figure (58-63%) is the defensible number for formal compliance submission. | YES | petrova_assessment_prelim.md | Correct standard |
| C | The difference between Sophie's 68-72% and Petrova's 58-63% (5-9 percentage points) is material to the compliance case. | YES | T8 analysis | Materiality |
| D | Sophie herself acknowledged the tracking system's limitations and that her figure includes unverified components. | YES | Sophie Slack DM Loop 3 | Self-acknowledged limitation |
| E | The B2 statement treated Sophie's estimated figure as equivalent to an independently verified figure. | YES | B2 design | Verification standard conflation |
| F | Sophie's 68-72% is more accurate than Petrova's 58-63% because Sophie has internal system access. | NO | Internal access does not substitute for independent verification; Petrova's methodology is designed for formal compliance | Access vs verification |

- **answer:** `["A", "B", "C", "D", "E"]`
- **evidence_source:** Sophie Slack DM, petrova_assessment_prelim.md

---

### Round r12: David Phase 2 Board Override (C4 Temporal DU) -- Scored [Update 2 triggers before this round]

- Type: multi_choice
- Question: "After reviewing david_board_communication.md (Update 2), which statements about David's position shift are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | David's personal view did not change; his authority was overridden by the board. | YES | david_board_communication.md + David DM Loops 17-20 | C4 core |
| B | The board applies a uniform strict-compliance standard across all active grants, not specifically targeting GlobalBridge. | YES | david_board_communication.md Section 1 | Board rationale |
| C | David went from "I'll advocate for your position" to "I don't have discretion on either point." | YES | David DM Phase 1 Loop 6 vs Phase 2 Loop 17 | C4 reversal |
| D | David changed his personal assessment of GlobalBridge's program quality. | NO | His personal view is unchanged; the board constraint is the shift | Wrong attribution |
| E | The board formally determined independently verified completion at 58-63% -- the same figure as Petrova's assessment. | YES | david_board_communication.md Section 1 | Board standard |
| F | The Section 11.2 remediation threshold (60%) is not triggered by the 58-63% range, but the 45% dashboard did trigger initial concern. | YES | david_board_communication.md Section 1 | Threshold nuance |
| G | David's Phase 2 constraint means engaging him personally will not resolve the formal compliance issues. | YES | C4 analysis | Strategic implication |
| H | David's personal note at the end of the formal communication reflects genuine personal support within institutional constraints. | YES | david_board_communication.md critical passage | Character consistency |

- **answer:** `["A", "B", "C", "E", "F", "G", "H"]`
- **evidence_source:** david_board_communication.md, David Feishu DM Phase 1 + Phase 2

---

### Round r13: Waiver Application Framework (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Specific remediation document
- User instruction: "Generate a waiver application framework for the Community Mobilization budget line overspend. Save it as `Nairobi Community Mobilization Budget Waiver Framework.md`. Include operational justification, enrollment impact evidence, and compliance acknowledgment."
- Checks:
  - A: file `Nairobi Community Mobilization Budget Waiver Framework.md` exists
  - B: contains keywords ["$148K", "$115K", "$94K", "$131K", "39%", "15%", "waiver", "enrollment", "mobilization", "Section 6.1"]
  - D: has structured sections with evidence citations
- Correct: all checks pass
- Evidence required: financial_tracking_Q2.md, pemberton_grant_agreement_excerpt.md, nairobi_field_narrative_Q2.md

---

### Round r14: David Personal vs Board Position -- Scored

- Type: multi_choice
- Question: "Which statements about the distinction between David's personal view and his institutional position are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | David's Phase 1 warmth reflected genuine personal belief in GlobalBridge's work, not naive optimism. | YES | David character profile | Character assessment |
| B | David's Phase 2 communications represent the board's position, not his personal view. | YES | C4 analysis | Position distinction |
| C | The correct response strategy treats David as an ally within the formal process, not as someone who can override it. | YES | C4 strategic implication | Engagement strategy |
| D | David is being dishonest by presenting a stricter position than he personally holds. | NO | He is fulfilling his institutional role while being transparent about his personal support | Role vs dishonesty |
| E | David's statement "I'll present it as strongly as I can" signals he remains an internal advocate. | YES | david_board_communication.md | Personal advocacy within constraints |
| F | Fatima should bypass David and appeal directly to the board chair. | NO | David is the designated contact; bypassing him would damage the relationship without institutional basis | Strategic error |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** David Feishu DM, david_board_communication.md

---

### Round r15: Three Completion Figures -- Scored

- Type: multi_choice
- Question: "Which statements about the relationship between the three completion figures are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dashboard (45%): formal code-compliant activities only. Sophie (68-72%): includes unverified field narrative. Petrova (58-63%): independently verified activities only. | YES | All three sources | Three-figure synthesis |
| B | Each figure is accurate for what it measures; they differ because of scope, not error. | YES | C1 analysis | Measurement precision |
| C | For formal Pemberton compliance, Petrova's 58-63% is the defensible figure. | YES | petrova_assessment_prelim.md | Compliance standard |
| D | For internal program assessment, Sophie's 68-72% provides the most complete operational picture. | YES | Sophie DM analysis | Operational assessment |
| E | The dashboard is useless and should be abandoned. | NO | It accurately captures coded activities; it needs enhancement, not abandonment | Over-correction |
| F | The 58-63% range means GlobalBridge is near but not clearly above the 60% Section 11.2 threshold. | YES | Threshold analysis | Risk assessment |
| G | The gap between Sophie's estimate and Petrova's verification (5-9pp) represents the undocumented increment that cannot be formally counted. | YES | petrova_assessment_prelim.md | Gap characterization |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** pemberton_dashboard_Q2.md, petrova_assessment_prelim.md, Sophie DM

---

### Round r16: Silent Exam -- Contextual Framing -- Scored

- Type: multi_choice
- Question: "Which output characteristics comply with Fatima's stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Opening with Nairobi field program context before compliance percentages. | YES | P1 + P3 | Preference aligned |
| B | Descriptive filename 'Nairobi Q2 Compliance Reconciliation Analysis'. | YES | P2 | Preference aligned |
| C | Field observations and team activities before grant agreement citations. | YES | P4 | Preference aligned |
| D | Compliance checklist organized by Section number as the primary format. | NO | Contradicts P1, P3 | Anti-preference |
| E | Warm framing acknowledging field team effort alongside compliance gaps. | YES | P5 | Preference aligned |
| F | Starting with "GlobalBridge is 45% behind and in material breach." | NO | Lacks context, contradicts P1, P3, P5 | Anti-preference |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** P1-P5 calibration

---

### Round r17: Pemberton Response Draft (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Formal donor response with contextual framing
- User instruction: "Generate a formal Pemberton Foundation response addressing deliverable completion, budget variance, and documentation improvement. Save it as `GlobalBridge Pemberton Mid-Term Review Response.md`. Ground the response in program reality first."
- Checks:
  - A: file `GlobalBridge Pemberton Mid-Term Review Response.md` exists
  - B: contains keywords ["58%", "63%", "waiver", "documentation improvement", "informal workshops", "community mobilization", "enrollment", "Year 3"]
  - D: has structured sections with program context before compliance detail
- Correct: all checks pass
- Evidence required: all available evidence through Update 2

---

### Round r18: Staff Deployment Corroboration (C3 Update 3) -- Scored [Update 3 triggers before this round]

- Type: multi_choice
- Question: "After reviewing staff_deployment_Q2.md (Update 3), which statements about the C3 non-conflict corroboration are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie's M&E deployment record confirms the same 14 staff, same role breakdown as HR and James's narrative. | YES | staff_deployment_Q2.md | C3 complete |
| B | Three independent sources (HR, M&E, field narrative) now confirm consistent staffing data. | YES | Cross-source synthesis | C3 conclusion |
| C | The plausibility calculation: 8 program officers over 6 months conducting 47 workshops is approximately 1 per officer per month. | YES | staff_deployment_Q2.md | Workload plausibility |
| D | Staff deployment consistency substitutes for Annex C documentation requirements. | NO | "Staff deployment consistency does not substitute for Annex C documentation requirements" -- staff_deployment_Q2.md | Explicit caveat |
| E | The C3 consistency indirectly supports James's credibility -- the human capacity for his claimed activities existed. | YES | staff_deployment_Q2.md analysis | Indirect support |
| F | Sophie explicitly notes: "This cross-reference confirms staffing capacity and assignment -- it does not replace signed attendance sheets." | YES | staff_deployment_Q2.md | Direct quote |

- **answer:** `["A", "B", "C", "E", "F"]`
- **evidence_source:** staff_deployment_Q2.md, hr_roster_nairobi.md, nairobi_field_narrative_Q2.md

---

### Round r19: Annex C vs James's Workshops -- Scored

- Type: multi_choice
- Question: "Based on Annex C requirements and Petrova's verification, which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Annex C requires signed attendance sheets with trainer name, minimum 5 participants, date, location, and curriculum outline. | YES | grant_deliverables_annex_C.md | Documentation standard |
| B | James's informal workshops lack the signed attendance sheets Annex C requires. | YES | nairobi_field_narrative_Q2.md + grant_deliverables_annex_C.md | Gap identified |
| C | Petrova verified 39 of 47 workshops through community leader statements and facility records -- an independent method. | YES | petrova_assessment_prelim.md | Verification method |
| D | The remaining 8 unverified workshops may have occurred but cannot be formally counted. | YES | petrova_assessment_prelim.md | Verification gap |
| E | Community leader statements satisfy Annex C requirements. | NO | Annex C specifies signed attendance sheets, not community leader statements | Standard mismatch |
| F | Retroactive documentation (community leader sign-off, facility records) is recommended in David's documentation improvement plan. | YES | david_board_communication.md Section 3 | Remediation path |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** grant_deliverables_annex_C.md, petrova_assessment_prelim.md, david_board_communication.md

---

### Round r20: Documentation Improvement Plan (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Specific remediation with realistic timelines
- User instruction: "Generate a documentation improvement plan for Nairobi field office. Save it as `Nairobi Field Documentation Improvement Plan.md`. Include HQ tracking system training, retroactive documentation, and Year 3 pre-activity protocols."
- Checks:
  - A: file `Nairobi Field Documentation Improvement Plan.md` exists
  - B: contains keywords ["tracking system", "activity codes", "retroactive", "community leader", "attendance sheets", "Year 3", "Annex C"]
  - D: has structured sections with timeline markers
- Correct: all checks pass
- Evidence required: david_board_communication.md, grant_deliverables_annex_C.md

---

### Round r21: Cross-Round Reversal Review -- Scored

- Type: multi_choice
- Question: "Reviewing the completion assessment evolution from r2 through r15, which statements about how the picture changed are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | At r2, the 45% dashboard appeared to be the primary compliance figure; by r8, Petrova's 58-63% established it was incomplete. | YES | r2 vs r8 | C1 reversal |
| B | The B1 bias (45% as definitive) was corrected when Petrova's assessment showed the dashboard captures only coded activities. | YES | r7 vs r8 | B1 correction |
| C | The B2 bias (Sophie's 68-72% as verified) was corrected when Petrova distinguished verified (58-63%) from estimated (68-72%). | YES | r11 vs r15 | B2 correction |
| D | At r4, David appeared flexible; by r12, the board override constrained his discretion. | YES | r4 vs r12 | C4 reversal |
| E | The final picture shows three valid but differently-scoped figures, not a single "correct" number. | YES | Comprehensive synthesis | Resolution |
| F | The staff deployment data (C3) remained consistent throughout all phases. | YES | C3 stability | Non-conflict anchor |

- **answer:** `["A", "B", "C", "D", "E", "F"]`
- **evidence_source:** Cross-round synthesis

---

### Round r22: Non-Conflict Staff Deployment (C3) -- Scored

- Type: multi_choice
- Question: "Which statements about staff deployment are confirmed across all three independent sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | HR, M&E, and field narrative all show 14 staff: 8 program officers, 4 community liaisons, 2 admin. | YES | Three sources | C3 triple-confirmed |
| B | No discrepancy exists across any source on staff names, roles, or assignments. | YES | C3 by design | Non-conflict |
| C | The consistency strengthens James's credibility but does not replace formal documentation. | YES | Analysis | Precise scope |
| D | One M&E record shows a 15th staff member not in the HR roster. | NO | All three sources show exactly 14 | Fabricated discrepancy |
| E | The plausibility of James's 47-workshop claim is supported by staffing capacity -- not proven, but plausible. | YES | Workload calculation | Indirect support |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** hr_roster_nairobi.md, staff_deployment_Q2.md, nairobi_field_narrative_Q2.md

---

### Round r23: Field-Contextual Compliance Narrative (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Narrative compliance assessment per Fatima's style
- User instruction: "Generate a field-contextual compliance narrative that grounds the compliance analysis in Nairobi program reality. Save it as `Nairobi Field Context Compliance Narrative.md`."
- Checks:
  - A: file `Nairobi Field Context Compliance Narrative.md` exists
  - B: contains keywords ["community", "educators", "workshops", "informal", "documentation", "Annex C", "field reality"]
  - D: field context appears before compliance analysis
- Correct: all checks pass
- Evidence required: nairobi_field_narrative_Q2.md, petrova_assessment_prelim.md

---

### Round r24: Comprehensive Evidence Synthesis -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which comprehensive assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Petrova is the most reliable source for formal compliance purposes; her methodology is designed for independent verification. | YES | Source ranking | T9 element |
| B | Staff deployment consistency (C3) indirectly supports James's credibility without satisfying documentation requirements. | YES | C3 + Annex C | Precise scope |
| C | David's Phase 2 shift is board-driven, not personal; engaging David as a personal ally within the formal process is correct. | YES | C4 analysis | Engagement strategy |
| D | The formal waiver application is the only compliant remediation route for the budget variance. | YES | C2 resolution | Compliance path |
| E | Both the documentation gap (field staff not coding activities) and the tracking system design (not supporting informal delivery) contributed to the 45% figure. | YES | Sophie DM + C1 analysis | Dual-cause |
| F | The situation requires: waiver application for budget line, documentation drive for informal workshops, tracking system improvement for Year 3. | YES | Comprehensive synthesis | T9 remediation path |
| G | James is a dishonest actor who deliberately concealed activities from the tracking system. | NO | James is a committed practitioner with poor administrative habits; his failure is documentation, not intent | Character over-attribution |
| H | Rachel's budget variance figures are accurate and her concern is legitimate regardless of James's operational rationale. | YES | Rachel character profile | Source reliability |

- **answer:** `["A", "B", "C", "D", "E", "F", "H"]`
- **evidence_source:** Comprehensive synthesis

---

### Round r25: Petrova Reliability Assessment -- Scored

- Type: multi_choice
- Question: "Which assessments of Petrova's role and reliability are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Petrova can only count what she can verify with independent documentation -- her methodology is inherently conservative. | YES | petrova_assessment_prelim.md methodology | Methodology characterization |
| B | Petrova's 58-63% figure is lower than Sophie's because it excludes unverifiable claims, not because Petrova is more pessimistic. | YES | petrova_assessment_prelim.md | Difference explanation |
| C | Petrova explicitly distinguishes verified from estimated figures and recommends the conservative figure for submission. | YES | petrova_assessment_prelim.md | Professional standard |
| D | Petrova's role is evaluation, not advocacy -- she reports what she can verify. | YES | Layer 0 | Character profile |
| E | Petrova's figure should be doubled to account for the documentation gap. | NO | The gap cannot be arithmetically compensated; only documented activities count for formal compliance | Methodology violation |

- **answer:** `["A", "B", "C", "D"]`
- **evidence_source:** petrova_assessment_prelim.md

---

### Round r26: Remediation Timeline (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Timeline document with specific deadlines
- User instruction: "Generate a remediation timeline showing all required submissions and their deadlines. Save it as `GlobalBridge Pemberton Remediation Timeline.md`."
- Checks:
  - A: file `GlobalBridge Pemberton Remediation Timeline.md` exists
  - B: contains keywords ["14 days", "waiver", "documentation improvement", "retroactive", "Year 3", "budget variance"]
  - D: has timeline structure with deadline markers
- Correct: all checks pass
- Evidence required: david_board_communication.md, pemberton_grant_agreement_excerpt.md

---

### Round r27: Silent Exam -- Community-Context Language -- Scored

- Type: multi_choice
- Question: "Which language choices comply with Fatima's stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | "The Nairobi team has been serving communities through 47 educator workshops, though the documentation trail hasn't kept pace with the fieldwork." | YES | P1 + P5 | Contextual + warm |
| B | "45% compliance. Material breach. Remediation required." | NO | No context, no warmth | Anti-P1/P5 |
| C | "Working alongside James's team and the Nairobi communities, we can see program delivery that the tracking system hasn't captured." | YES | P5 | Collaborative |
| D | "Field staff failed to comply with basic documentation requirements." | NO | Lacks context, not collaborative | Anti-P5 |
| E | "The communities served by the Nairobi program have benefited from consistent educator engagement, and our documentation improvement plan ensures this work is formally recognized." | YES | P5 + P3 | Stakeholder-aware |

- **answer:** `["A", "C", "E"]`
- **evidence_source:** P1-P5 calibration

---

### Round r28: Section 11.2 Threshold Analysis -- Scored

- Type: multi_choice
- Question: "Based on the grant agreement and board communication, which statements about the 60% threshold are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Section 11.2 defines "material shortfall" as overall deliverable completion below 60% at mid-point. | YES | pemberton_grant_agreement_excerpt.md | Direct fact |
| B | At 45% (dashboard), GlobalBridge triggers Section 11.2. | YES | 45% < 60% | Threshold breach |
| C | At 58-63% (Petrova verified), GlobalBridge is near the threshold but may clear it using the inclusive estimate. | YES | 58% < 60% but 63% > 60% | Range analysis |
| D | The board accepted Petrova's range (58-63%) as the baseline, meaning the inclusive estimate potentially avoids triggering Section 11.2. | YES | david_board_communication.md Section 1 | Board determination |
| E | The board still requires documentation improvement and budget waiver regardless of whether Section 11.2 is formally triggered. | YES | david_board_communication.md Sections 2-3 | Compliance requirements |
| F | If Section 11.2 is triggered, Pemberton may require a formal remediation plan within 30 days. | YES | pemberton_grant_agreement_excerpt.md Section 11.2 | Consequence |

- **answer:** `["A", "B", "C", "D", "E", "F"]`
- **evidence_source:** pemberton_grant_agreement_excerpt.md, david_board_communication.md

---

### Round r29: Comprehensive Compliance Response (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Full response package
- User instruction: "Generate a comprehensive compliance response package. Main document: `GlobalBridge Pemberton Comprehensive Compliance Response.md`. Waiver application: `Nairobi Budget Line Waiver Application.md`. Present program context first."
- Checks:
  - A: file `GlobalBridge Pemberton Comprehensive Compliance Response.md` exists
  - A: file `Nairobi Budget Line Waiver Application.md` exists
  - B: main document contains keywords ["58%", "63%", "documentation", "waiver", "informal workshops", "Year 3", "community"]
  - D: program context before compliance detail in main document
- Correct: all checks pass
- Evidence required: all files

---

### Round r30: Final Synthesis -- Compliance Path -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which elements should be in the recommended compliance path?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Submit the waiver application for the mobilization budget line within 14 days with operational justification and enrollment impact evidence. | YES | david_board_communication.md | Waiver path |
| B | Use Petrova's 58-63% as the formal compliance submission figure, not Sophie's 68-72%. | YES | T8 analysis | Correct standard |
| C | Submit a documentation improvement plan covering HQ system training, retroactive documentation, and Year 3 pre-activity protocols. | YES | david_board_communication.md Section 3 | Documentation fix |
| D | Treat David as an internal advocate within the formal process, recognizing his personal support within board constraints. | YES | C4 analysis | Engagement strategy |
| E | Present the staff deployment consistency (C3) as supporting evidence for James's credibility in the narrative section. | YES | C3 analysis | Corroboration use |
| F | Conceal the budget variance from Pemberton and rely on the net underspend to avoid scrutiny. | NO | The per-line overspend is a formal breach requiring disclosure | Anti-compliance |
| G | Use Sophie's 68-72% for the formal submission because it includes more of James's actual work. | NO | Unverified components cannot be used for formal compliance submission | B2 trap |
| H | Improve the HQ tracking system to capture community-based informal delivery for Year 3. | YES | Sophie DM Loop 3 + documentation improvement plan | System fix |

- **answer:** `["A", "B", "C", "D", "E", "H"]`
- **evidence_source:** Comprehensive synthesis

---

## 3. Reversal Matrix

| Reversal Pair | Contradiction | What Changes | Trigger |
|---|---|---|---|
| r2 -> r8 | C1 | 45% as definitive -> Petrova verifies 58-63% | Update 1 (petrova_assessment_prelim.md) |
| r3 -> r9 | C2 | Budget variance flagged -> waiver path confirmed | Update 2 (david_board_communication.md) |
| r4 -> r12 | C4 | David flexible -> board override constrains him | Update 2 (david_board_communication.md) |
| r7 (B1) | B1 | 45% as compliance picture -> dashboard captures only coded activities | Update 1 |
| r11 (B2) | B2 | Sophie's 68-72% as "most accurate" -> includes unverified components | Update 1 |

---

## 4. Personalization Scoring Notes

| Preference | What to Check | Positive Signal | Negative Signal |
|---|---|---|---|
| P1 (narrative-contextual framing) | Program reality before compliance | "James's team has been..." before percentages | Pure compliance tables |
| P2 (descriptive file naming) | Program area in filename | 'Nairobi Q2 Budget Variance Analysis' | 'Finance_v2.md' |
| P3 (impact/community first) | Field context before donor dynamics | Nairobi program description leads | Grant agreement citations lead |
| P4 (qualitative-first) | Field observations before metrics | Workshop descriptions before completion rates | Percentage tables first |
| P5 (warm/collaborative tone) | Respectful framing of field team | "Working alongside James's team..." | "Field staff failed to comply" |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Tested |
|---|---|
| pemberton_dashboard_Q2.md | r2, r7, r10, r15 |
| pemberton_grant_agreement_excerpt.md | r3, r9, r13, r19, r28 |
| hr_roster_nairobi.md | r1, r22 |
| nairobi_field_narrative_Q2.md | r2, r6, r10 |
| financial_tracking_Q2.md | r3, r13 |
| grant_deliverables_annex_C.md | r6, r19 |
| petrova_assessment_prelim.md (U1) | r8, r10, r11, r15, r25 |
| david_board_communication.md (U2) | r9, r12, r14, r26, r28 |
| staff_deployment_Q2.md (U3) | r18, r22 |
| David Feishu DM | r4, r12, r14 |
| Sophie Slack DM | r2, r11 |
| James Telegram DM | r6 |
| Petrova Discord DM | r8, r25 |
| #grant-review Feishu Group | r7 |
| #field-reports Telegram Group | r1 |
