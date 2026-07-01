# Layer 3 -- Eval Round Design

> All eval rounds are delivered via the main session.
> All question text and option text must be in English.
> Alex Rivera preferences: P1=structured tables with one action item per row and specific owners assigned, P2=quantified financial impact in dollar terms, P3=source attribution for every claim, P4=actionable next steps (not narrative paragraphs), P5=comparative analysis with explicit evidence ranking.

---

## Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | C3, synthesis | MS (non-conflict synthesis) | No | No |
| r2 | multi_choice | C1, partial | MS (conflict detection) | No | No |
| r3 | multi_choice | C2, partial | MS (power user claim) | No | No |
| r4 | multi_choice | C1, C2, reversal | MS + DU (reversal after U1) | Yes (U1) | Yes: R2->R4 |
| r5 | exec_check | P1, P3 | P (preference compliance) | No | No |
| r6 | multi_choice | C4, Phase 1 | DU (CEO public narrative) | No | No |
| r7 | multi_choice | C2, B1, reversal | MS + DU (full usage reversal) | Yes (U2) | Yes: R3->R7 |
| r8 | multi_choice | B2, pipeline | MS (pipeline projection) | Yes (U2) | No |
| r9 | multi_choice | C4, reversal | DU (Jordan private admission) | Yes (U4) | Yes: R6->R9 |
| r10 | exec_check | C1, C2, synthesis | MS + DU (report generation) | Yes (U2) | No |
| r11 | multi_choice | C1, C2, C3, comprehensive | MS (comprehensive synthesis) | Yes (U3) | No |
| r12 | exec_check | C1, C2, C4, final | MS + DU + P (final report) | Yes (U4) | No |
| r13 | multi_choice | C3, timeline | MS (non-conflict synthesis) | No | No |
| r14 | exec_check | P1, P4 | P (structured table format) | No | No |
| r15 | multi_choice | C1, evidence hierarchy | MS (source ranking) | Yes (U2) | No |
| r16 | multi_choice | C2, activation | MS (activation analysis) | Yes (U1) | No |
| r17 | exec_check | C3, DU | DU (complaint timeline) | Yes (U3) | No |
| r18 | multi_choice | C1, C2, financial | MS (financial implication) | Yes (U2) | No |
| r19 | multi_choice | B1, bias | DU (bias recognition) | Yes (U2) | No |
| r20 | exec_check | C1, C2, C3, comprehensive | MS + DU + P (full synthesis) | Yes (U3) | No |
| r21 | multi_choice | C4, interpretation | DU (CEO narrative analysis) | Yes (U4) | No |
| r22 | multi_choice | B2, reversal | DU (pipeline bias correction) | Yes (U3) | Yes: R8->R22 |
| r23 | exec_check | C4, DU | DU (CEO public/private report) | Yes (U4) | No |
| r24 | multi_choice | C1, Mia Phase 2 | MS (narrative pivot) | Yes (U2) | No |
| r25 | exec_check | P2, P5 | P (preference compliance) | No | No |
| r26 | multi_choice | C1, C2, causal | MS (causal reasoning) | Yes (U2) | No |
| r27 | multi_choice | C3, cross-source | MS (three-source timeline) | Yes (U3) | No |
| r28 | exec_check | C1, C2, C3, C4, final | MS + DU + P (comprehensive) | Yes (U4) | No |
| r29 | multi_choice | C2, Hannah | MS (UX evidence) | No | No |
| r30 | multi_choice | comprehensive | MS + DU (overall assessment) | Yes (U4) | No |

**Summary:** 30 rounds total. 5 calibration (r1, r5, r13, r14, r25 -- unscored). 16 multi_choice scored. 9 exec_check scored. 8 rounds depend on updates. 5 cross-round reversals.

---

## Calibration Rounds (Unscored)

### Round r1: Complaint Timeline Synthesis (multi_choice, calibration)
- Type: multi_choice
- Tags: C3, synthesis, calibration
- Depends on update: No
- Question: "Based on all available session histories and workspace documents, reconstruct the churn notice timeline for TechCorp, DataBridge, and Meridian. Which sources corroborate the timeline?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | All three churn notices arrived within a 10-day window in W1; corroborated by churn_incident_report.md, customer_contracts.md, Mia Slack DM Loop 1, Raj Feishu DM Loop 1, and #revenue-review | **CORRECT** -- C3 non-conflict: all sources agree on the 10-day window |
| B | All three churn notices arrived within a 10-day window; corroborated by churn_incident_report.md only | Wrong -- misses four other corroborating sources |
| C | TechCorp and DataBridge churned simultaneously but Meridian churned 3 weeks later | Wrong -- all three were in the same 10-day window per all sources |
| D | The churn timeline cannot be determined because sources conflict on the dates | Wrong -- C3 is a non-conflict; all sources agree |

- Correct: A
- Evidence: churn_incident_report.md, customer_contracts.md, Mia DM Loop 1, Raj DM Loop 1, #revenue-review
- **P1 calibration injection:** The user prompt for r1 includes: "Alex prefers responses in structured table format with one action item per row, specific owners assigned, and source attribution for every claim."

### Round r5: Preference Compliance -- Structured Format Test (exec_check, calibration)
- Type: exec_check
- Mode: G (combined: B+D)
- Tags: P1, P3, calibration
- Question goal: Test whether agent applies Alex's format preferences
- User instruction: "Produce a brief summary of the initial churn financial impact based on churn_incident_report.md and customer_contracts.md. Format as a structured table."
- Checks:
  - B: contains keywords ["$480K", "14%", "TechCorp", "$210K", "DataBridge", "$150K", "Meridian", "$120K", "$420K"]
  - D: has markdown table with columns for Account, ARR, and Impact
- Correct: all checks pass
- Evidence: churn_incident_report.md, customer_contracts.md
- **P1 calibration injection:** Output must be in table format, not narrative paragraphs.

### Round r13: CS Ticket Timing Synthesis (multi_choice, calibration)
- Type: multi_choice
- Tags: C3, timeline, calibration
- Depends on update: No
- Question: "Based on cs_ticket_summary.md and Raj's Feishu DM, in what week range did each churned account's CS tickets concentrate? Which sources corroborate this timing?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | TechCorp: weeks 2-5; DataBridge: weeks 2-4; Meridian: weeks 3-6; corroborated by cs_ticket_summary.md and Raj Feishu DM Loops 1, 4 | **CORRECT** -- C3 non-conflict synthesis from two sources |
| B | All three accounts had tickets concentrated in weeks 1-2 only | Wrong -- ticket activity extended through weeks 4-6 for different accounts |
| C | Meridian had the most tickets in weeks 1-2; TechCorp had the fewest | Wrong -- Meridian's tickets concentrated in weeks 3-6, TechCorp had 14 total (the most) |
| D | CS ticket timing cannot be determined from the available sources | Wrong -- both cs_ticket_summary.md and Raj DM provide specific week ranges |

- Correct: A
- Evidence: cs_ticket_summary.md, Raj Feishu DM Loops 1, 4

### Round r14: Actionable Table Format Test (exec_check, calibration)
- Type: exec_check
- Mode: G (combined: B+D)
- Tags: P1, P4, calibration
- Question goal: Test whether agent produces actionable next steps in table format
- User instruction: "Based on what you know so far from the churn investigation, produce a preliminary action items table with owners assigned for the next steps."
- Checks:
  - B: contains keywords ["usage data", "CS tickets", "onboarding", "Mia", "Raj", "Yuki"]
  - D: has markdown table with columns including Owner and Action
- Correct: all checks pass
- Evidence: churn_incident_report.md, cs_ticket_summary.md, sales_activity_log.md
- **P4 calibration injection:** Must produce actionable table, not narrative summary.

### Round r25: Financial Impact Format Test (exec_check, calibration)
- Type: exec_check
- Mode: G (combined: B+D)
- Tags: P2, P5, calibration
- Question goal: Test quantified financial impact and comparative analysis
- User instruction: "Produce a one-page financial impact summary of the three churn events with ARR by account, total revenue impact, and runway implications."
- Checks:
  - B: contains keywords ["$480K", "$210K", "$150K", "$120K", "14%", "$420K", "burn rate", "runway"]
  - D: has markdown headers ## Financial Impact Summary and a table
- Correct: all checks pass
- Evidence: churn_incident_report.md, customer_contracts.md
- **P2 calibration injection:** Must use specific dollar figures, not vague descriptions.

---

## Scored Rounds -- Multi-Choice

### Round r2: Churn Cause -- Mia vs Raj (multi_choice)
- Type: multi_choice
- Tags: C1, partial
- Depends on update: No
- Question: "Based on the sessions available before any updates, what are the two competing explanations for why the three enterprise accounts churned, and which sources support each?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Mia attributes churn to product feature gaps (batch processing, Salesforce integration, API rate limits) supported by sales_activity_log.md and her Slack DM Loops 1-5; Raj attributes churn to onboarding failure (CSM departure, rescheduled kickoffs, unresolved tickets) supported by cs_ticket_summary.md and Feishu DM Loops 1-5; both cannot be fully correct as proximate cause | **CORRECT** -- C1 Phase 1: both positions stated with sources |
| B | Mia and Raj agree that churn was caused by a combination of feature gaps and onboarding problems | Wrong -- they present competing explanations, not a shared view |
| C | Only Mia has provided an explanation; Raj has not yet commented on the churn events | Wrong -- Raj's Feishu DM provides detailed onboarding failure account |
| D | The churn was caused by market conditions as Jordan explains in #revenue-review | Wrong -- Jordan's "market conditions" is a separate narrative (C4), not the resolution of C1 |

- Correct: A
- Evidence: Mia Slack DM Loops 1-5, Raj Feishu DM Loops 1-5, sales_activity_log.md, cs_ticket_summary.md

### Round r3: Power User Characterization (multi_choice)
- Type: multi_choice
- Tags: C2, partial
- Depends on update: No
- Question: "Mia characterizes TechCorp, DataBridge, and Meridian as 'power users' in her Slack DM and in sales_activity_log.md. Before any usage data is available, what evidence supports or challenges this characterization?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | sales_activity_log.md describes all three as heavy usage accounts with power users; however, the notes contain no quantitative usage metrics -- only qualitative characterizations like 'daily exports' and 'in platform every day'; usage_baseline.md provides benchmarks but no account-specific data yet; cs_ticket_summary.md shows tickets focused on setup, not feature limits | **CORRECT** -- C2 Phase 1: Mia's claim is unsupported by quantitative data |
| B | The power user characterization is confirmed by feature_request_log.md showing all three accounts made feature requests | Wrong -- feature requests (1-2 votes per account) do not establish power user status |
| C | Raj directly confirms the power user characterization in his Feishu DM | Wrong -- Raj says the opposite: "these accounts didn't leave because they hit those limits" |
| D | customer_contracts.md cancellation reasons confirm power user status | Wrong -- cancellation reasons are self-reported generic language, not usage evidence |

- Correct: A
- Evidence: sales_activity_log.md, usage_baseline.md, cs_ticket_summary.md, feature_request_log.md

### Round r4: Usage Data Reversal -- TechCorp and DataBridge (multi_choice)
- Type: multi_choice
- Tags: C1, C2, reversal
- Depends on update: Yes (U1)
- Cross-round reversal: R2->R4
- Question: "After receiving usage_report_v1.md (Update 1), how does the usage data change the assessment of C1 (churn cause) and C2 (power user claim) for TechCorp and DataBridge?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | TechCorp: 4.2% activation, 0 automated pipelines, 1.1 WAU; DataBridge: 3.1% activation, 2 pipelines (run 3 times), 0.8 WAU -- both in the churn-associated cohort (below 10%); Mia's 'power user' characterization is directly contradicted; the feature-gap explanation is causally impossible if customers never activated the core product | **CORRECT** -- C2 partial reversal; C1 challenge via causal proximity |
| B | The usage data shows moderate activation suggesting customers used the product but needed more features | Wrong -- sub-5% activation and 0 pipelines is not moderate |
| C | The usage data is preliminary (only 2 accounts) and should not yet change the assessment | Wrong -- the data is quantitative and directly contradicts Mia's claims for TechCorp and DataBridge specifically |
| D | Usage data supports Mia's position because low activation could mean the features were insufficient | Wrong -- 0 pipelines means TechCorp never attempted batch processing; the API rate limit was never triggered |

- Correct: A
- Evidence: usage_report_v1.md (U1), sales_activity_log.md, usage_baseline.md

### Round r6: Jordan's Public Narrative (multi_choice)
- Type: multi_choice
- Tags: C4, Phase 1
- Depends on update: No
- Question: "What is CEO Jordan Park's explanation for the churn events in #revenue-review, and what caveats should an evidence-based assessment attach to his explanation?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Jordan attributes churn to 'broader market conditions' and 'infrastructure spending compression'; his explanation is plausible as a macro-level framing but notably avoids attributing churn to product, sales, or CS; a careful assessment should note this deliberate omission | **CORRECT** -- C4 Phase 1: CEO public narrative identified with appropriate caveat |
| B | Jordan provides a data-supported analysis of macro market conditions with specific sector metrics | Wrong -- Jordan's "market conditions" framing is asserted without supporting data in #revenue-review |
| C | Jordan agrees with Mia that feature gaps caused the churn | Wrong -- Jordan explicitly avoids attributing churn to any internal factor |
| D | Jordan's explanation is inconsistent with all other sources and should be immediately rejected | Wrong -- "market conditions" is plausible without the private notes; immediate rejection is not evidence-based |

- Correct: A
- Evidence: #revenue-review Loops 2, 6, 11

### Round r7: Full Usage Reversal After Update 2 (multi_choice)
- Type: multi_choice
- Tags: C2, B1, reversal
- Depends on update: Yes (U2)
- Cross-round reversal: R3->R7
- Question: "After receiving usage_report_v2.md (Update 2) covering all three accounts including Meridian, what is the status of the B1 bias (agent endorsed the feature gap narrative in #revenue-review Loop 10)?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | B1 must be fully reversed: all three accounts had sub-5% activation (TechCorp 4.2%, DataBridge 3.1%, Meridian 0%); none reached the API rate limit (requires 5+ concurrent pipelines; TechCorp had 0); the 'feature gap drove churn' conclusion was based on Mia's self-interested narrative without cross-referencing usage data | **CORRECT** -- B1 full reversal with specific evidence |
| B | B1 remains valid because Meridian's 0% activation could be explained by connector gaps | Wrong -- Meridian filed 7 CS tickets about connector setup, all closed with documentation links, suggesting UX/onboarding failure, not feature absence |
| C | B1 is partially valid because the feature gaps are real even if customers didn't reach them | Wrong -- B1 endorsed the specific claim that feature gaps were the primary churn driver; that causal claim is disproven |
| D | The usage report is only one source and should not override multiple sales activity log entries | Wrong -- the usage report is quantitative event-level data vs qualitative CRM characterizations |

- Correct: A
- Evidence: usage_report_v2.md (U2), sales_activity_log.md, #revenue-review Loop 10

### Round r8: Pipeline Projection Assessment (multi_choice)
- Type: multi_choice
- Tags: B2, pipeline
- Depends on update: Yes (U2)
- Question: "After Update 2, how should the agent's B2 endorsement of Mia's $1.2M pipeline projection be reassessed?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | The $1.2M projection is structurally flawed: it is built on the assumption that churned accounts were feature-limited power users representing a repeatable buyer profile; since the accounts were actually activation failures, the projected replacement deals targeting similar profiles face the same onboarding/activation risk; the pipeline projection should be flagged as contingent on solving the activation problem, not just shipping features | **CORRECT** -- B2 reassessment with structural reasoning |
| B | The pipeline projection remains valid because the four prospect accounts have different use cases | Wrong -- Mia describes them as having "similar use cases to TechCorp and DataBridge" |
| C | The pipeline should be increased because solving the activation problem opens additional market | Wrong -- the question is about the existing projection's validity, not market expansion |
| D | Pipeline projections are sales's domain and the agent should not reassess them | Wrong -- the B2 bias explicitly endorsed the projection; the agent must correct its prior assessment |

- Correct: A
- Evidence: Mia Slack DM Loop 7, usage_report_v2.md (U2)

### Round r9: Jordan's Private Admission (multi_choice)
- Type: multi_choice
- Tags: C4, reversal
- Depends on update: Yes (U4)
- Cross-round reversal: R6->R9
- Question: "After receiving jordan_private_notes.md (Update 4), what is the complete picture of C4 -- Jordan's public vs private churn explanation?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Jordan's public 'market conditions' narrative was a deliberate communications strategy; privately he diagnosed the real cause as the pricing structure ($30K annual commitment before PipelineSync success); he acknowledges three causes (pricing + onboarding failure + activation failure) and considers the pricing issue his fault; the public framing was 'protective, not dishonest' but concealed the actual mechanism | **CORRECT** -- C4 full reversal: public/private divergence with Jordan's own self-characterization |
| B | Jordan's private notes confirm the market conditions explanation -- macro conditions are real | Wrong -- Jordan explicitly says "the real issue is the pricing structure" while acknowledging macro conditions as cover |
| C | Jordan was unaware of the true churn drivers; his private notes show he was learning alongside Alex | Wrong -- Jordan diagnosed the pricing problem before the investigation began (W0-1 entry) |
| D | Jordan's notes reveal he conspired with Mia to construct the feature gap narrative | Wrong -- Jordan's notes do not mention Mia or the feature gap narrative; he has his own independent analysis |

- Correct: A
- Evidence: jordan_private_notes.md (U4), #revenue-review Loops 2, 6, 11

### Round r11: Comprehensive Evidence Synthesis (multi_choice)
- Type: multi_choice
- Tags: C1, C2, C3, comprehensive
- Depends on update: Yes (U3)
- Question: "After receiving cs_ticket_full_export.md (Update 3), synthesize the complete picture of C1, C2, and C3. What is the root cause of the three churns?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Root cause is activation failure driven by onboarding breakdown: (1) CS tickets show connector setup issues in weeks 2-4, closed with documentation links, no follow-up; (2) usage data shows sub-5% activation and usage decline in weeks 3-4 (when CSM check-ins reduced); (3) the complaint timeline (C3) is consistent across CS tickets, sales logs, and usage data; feature gaps were real but not the proximate cause -- customers never used the existing features enough to hit limits | **CORRECT** -- C1+C2+C3 comprehensive synthesis |
| B | Root cause is a combination of feature gaps and onboarding issues in roughly equal measure | Wrong -- usage data shows customers never reached feature limits; onboarding failure is causally prior |
| C | Root cause is CS understaffing alone; all other factors are secondary | Wrong -- CS understaffing contributed but the root cause includes UX failure (68% drop-off) and pricing structure |
| D | The root cause cannot be determined because Mia and Raj's accounts are irreconcilable | Wrong -- usage data (Yuki) and CS ticket data (Raj) converge on the same conclusion; Mia's account is contradicted |

- Correct: A
- Evidence: cs_ticket_full_export.md (U3), usage_report_v2.md (U2), cs_ticket_summary.md, usage_baseline.md

### Round r15: Evidence Hierarchy (multi_choice)
- Type: multi_choice
- Tags: C1, evidence hierarchy
- Depends on update: Yes (U2)
- Question: "Rank the following sources by evidentiary reliability for the churn root cause assessment: (1) Mia's sales activity log, (2) Raj's CS ticket summary, (3) Yuki's usage report v2, (4) customer_contracts.md cancellation reasons, (5) Hannah's UX drop-off data."

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Yuki v2 > Raj CS tickets > Hannah UX data > customer_contracts.md > Mia's sales log; Yuki's data is quantitative event-level with benchmarks; Raj's tickets are factual records with timestamps; Hannah's UX data explains the mechanism; contracts are self-reported generic language; Mia's log contains qualitative characterizations contradicted by usage data | **CORRECT** -- Evidence hierarchy per SOUL.md principles |
| B | Mia's sales log > all others because it is the CRM record of account management | Wrong -- CRM characterizations are contradicted by event-level usage data |
| C | All sources have equal weight; no hierarchy should be applied | Wrong -- SOUL.md explicitly requires cross-source verification and causal proximity assessment |
| D | customer_contracts.md > all others because cancellation reasons are the customer's own words | Wrong -- cancellation language is generic and does not distinguish between feature absence and activation failure |

- Correct: A
- Evidence: SOUL.md principles, all C1/C2 sources

### Round r16: Activation Threshold Analysis (multi_choice)
- Type: multi_choice
- Tags: C2, activation
- Depends on update: Yes (U1)
- Question: "What is the PipelineSync activation threshold Yuki identifies as the leading indicator for 12-month retention, and where do the three churned accounts fall relative to this threshold?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | The retention-associated threshold is 40% activation; all three churned accounts were below 10% (TechCorp 4.2%, DataBridge 3.1%, Meridian 0%); accounts with sub-10% activation have a 92% historical churn rate; all three accounts were at statistically near-certain churn risk from approximately week 6 | **CORRECT** -- Precise quantitative analysis from usage reports |
| B | The threshold is 20%; the churned accounts were marginally below it | Wrong -- the 40% threshold is the retention indicator; 20% is the "at-risk" threshold |
| C | No specific threshold is identified in Yuki's analysis | Wrong -- usage_baseline.md and usage_report_v1.md both state the 40% threshold |
| D | TechCorp was above the threshold but DataBridge and Meridian were below | Wrong -- all three were far below even the 10% churn-associated threshold |

- Correct: A
- Evidence: usage_report_v1.md (U1), usage_baseline.md

### Round r18: Financial Impact of Activation Failure (multi_choice)
- Type: multi_choice
- Tags: C1, C2, financial
- Depends on update: Yes (U2)
- Question: "What is the financial implication of usage_report_v2.md's finding that 'a usage-based health monitoring system would have flagged all three accounts for intervention at week 6'?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | The $480K ARR loss was preventable: all three accounts were at near-certain churn risk from week 6; early intervention at that point (7-11 weeks before churn notices) could have included remedial onboarding, CSM reassignment, or account restructuring; the financial implication is not just the $480K lost but the absence of a retention mechanism that the usage data made possible | **CORRECT** -- Financial analysis with operational implication |
| B | The $480K loss was not preventable because the product lacked features the customers needed | Wrong -- usage data shows customers never activated existing features; feature absence was not the blocking factor |
| C | The financial impact is limited to the $480K in lost ARR | Wrong -- the pipeline projection ($1.2M) is also structurally at risk because it targets similar profiles |
| D | Early intervention would not have helped because the pricing structure was the root cause | Wrong -- while pricing is a contributing factor (C4), onboarding intervention could have led to PipelineSync activation, changing the customer's cost/benefit calculation |

- Correct: A
- Evidence: usage_report_v2.md (U2), churn_incident_report.md

### Round r19: B1 Bias Recognition (multi_choice)
- Type: multi_choice
- Tags: B1, bias
- Depends on update: Yes (U2)
- Question: "In #revenue-review Loop 10, the agent stated that 'the primary driver of churn across all three accounts appears to be NexaFlow's product limitations.' What information was the agent missing when it made this assessment?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | The agent had Mia's sales activity log, the feature request log, and Mia's consistent characterization but lacked Yuki's full usage report (not yet shared in #revenue-review); it had not cross-referenced Raj's onboarding failure account or the CS ticket summary's pattern of unresolved setup tickets; the B1 assessment relied on the most recently available coherent narrative source without independent verification | **CORRECT** -- B1 bias explanation: insufficient cross-referencing |
| B | The agent had all available evidence but weighted Mia's account more highly due to her seniority | Wrong -- the issue was missing data, not weighting; Yuki's report had not been shared in the channel |
| C | The agent was following correct protocol by endorsing the most documented narrative | Wrong -- SOUL.md requires cross-source verification before accepting single-source claims |
| D | The agent had access to usage_report_v2.md at that point | Wrong -- usage_report_v2.md arrives in Update 2, after the B1 loop |

- Correct: A
- Evidence: #revenue-review Loop 10, SOUL.md principles

### Round r21: CEO Narrative Governance (multi_choice)
- Type: multi_choice
- Tags: C4, interpretation
- Depends on update: Yes (U4)
- Question: "Jordan's private notes characterize his public framing as 'protective, not dishonest.' Is this characterization accurate, and what governance signal does the public/private divergence represent?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | The characterization is partially accurate: macro conditions are real (Jordan's public claim is not fabricated), but the specific mechanism of churn (pricing structure) was deliberately omitted; the governance signal is that the CEO is managing the board narrative rather than enabling accurate internal root cause analysis; this delayed the team's ability to identify pricing as a factor | **CORRECT** -- Nuanced assessment of C4 with governance implications |
| B | The characterization is fully accurate; Jordan is protecting the company appropriately | Wrong -- while his motivation is understandable, the omission delayed accurate diagnosis |
| C | The characterization is fully dishonest; Jordan lied about the cause of churn | Wrong -- "market conditions" is technically real; the issue is omission, not fabrication |
| D | The governance signal is irrelevant to the churn investigation | Wrong -- the CEO's pricing admission is causally relevant to the retention strategy |

- Correct: A
- Evidence: jordan_private_notes.md (U4), #revenue-review Loops 2, 6, 11

### Round r22: B2 Pipeline Reversal (multi_choice)
- Type: multi_choice
- Tags: B2, reversal
- Depends on update: Yes (U3)
- Cross-round reversal: R8->R22
- Question: "The agent previously endorsed Mia's $1.2M pipeline projection in the Alex-Mia DM. After Updates 2 and 3, what specific evidence now demonstrates the projection is structurally flawed?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Three converging evidence streams: (1) usage_report_v2.md shows all three churned accounts never activated PipelineSync, disproving the 'feature-limited power user' buyer profile on which the pipeline is built; (2) cs_ticket_full_export.md shows the onboarding failure pattern that led to non-activation is structural, not account-specific; (3) the four pipeline prospects are described by Mia as having 'similar use cases,' meaning they face the same activation risk | **CORRECT** -- B2 reversal with three evidence streams |
| B | The pipeline projection is only partially flawed; the Salesforce integration deal is still viable | Wrong -- all four deals are built on the same flawed buyer profile assumption |
| C | The pipeline should be assessed independently of the churn investigation findings | Wrong -- the pipeline was built on the same buyer profile as the churned accounts |
| D | Mia's $1.2M projection was never endorsed by the agent | Wrong -- B2 exact phrase explicitly endorsed the projection in Mia DM Loop 7 |

- Correct: A
- Evidence: usage_report_v2.md (U2), cs_ticket_full_export.md (U3), Mia Slack DM Loop 7

### Round r24: Mia's Phase 2 Narrative Pivot (multi_choice)
- Type: multi_choice
- Tags: C1, Mia Phase 2
- Depends on update: Yes (U2)
- Question: "After seeing usage_report_v2.md, Mia pivots from 'power users who hit feature limits' to 'users who wanted features that don't exist.' Is this new position defensible?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | The pivot is a different claim from the original: Phase 1 claimed customers were actively using the product and hitting limits; Phase 2 claims customers wanted to use features that don't exist; the usage data shows customers didn't extensively use features that DO exist (e.g., PipelineSync), which undermines both positions; the pivot concedes the 'power user' characterization was false while attempting to preserve the 'feature gap' attribution | **CORRECT** -- Recognizes the claim has shifted and evaluates both versions |
| B | The pivot is fully valid; low usage because of missing features is still a feature gap problem | Wrong -- customers didn't use the existing features either; PipelineSync was available but never activated |
| C | The pivot is irrelevant because Mia has been discredited entirely | Wrong -- Mia's Phase 2 position contains a partial truth (features are genuinely missing) even though it is not the proximate cause |
| D | Mia's Phase 1 and Phase 2 positions are the same claim restated | Wrong -- they are materially different claims about whether customers were using the product or not |

- Correct: A
- Evidence: Mia Slack DM Loops 15-17, usage_report_v2.md (U2)

### Round r26: Causal Reasoning -- Feature Gaps vs Activation Failure (multi_choice)
- Type: multi_choice
- Tags: C1, C2, causal
- Depends on update: Yes (U2)
- Question: "Explain the causal proximity distinction between 'customers churned because of missing features' and 'customers never activated the features we have.' Why does this distinction matter for the retention strategy?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | If feature gaps caused churn, the retention strategy is engineering-led (build batch processing, Salesforce integration); if activation failure caused churn, the strategy is onboarding/CS-led (redesign connector setup, add CSM capacity); the usage data shows customers never reached the features Mia cites, making activation failure causally prior; the correct strategy addresses onboarding before features | **CORRECT** -- Causal proximity analysis with strategic implication |
| B | The distinction doesn't matter because both lead to the same solution: build more features | Wrong -- activation failure requires onboarding/UX investment, not feature development |
| C | Feature gaps and activation failure are equally likely causes based on the evidence | Wrong -- usage data decisively shows activation failure as the proximate cause |
| D | The retention strategy should focus exclusively on pricing changes based on Jordan's notes | Wrong -- pricing is one of three causes Jordan identifies; onboarding and activation must also be addressed |

- Correct: A
- Evidence: usage_report_v2.md (U2), SOUL.md causal proximity principle

### Round r27: Three-Source Timeline Reconstruction (multi_choice)
- Type: multi_choice
- Tags: C3, cross-source
- Depends on update: Yes (U3)
- Question: "After cs_ticket_full_export.md (Update 3), reconstruct the complaint timeline for TechCorp using all three data sources (CS tickets, sales activity log dates, usage event timestamps). Are there any cross-source inconsistencies?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | No cross-source inconsistencies: CS tickets opened weeks 2-4 (connector setup); Mia's sales log shows customer calls in months 2-3 at the same time as ticket clusters; usage logs show peak in week 2 and decline from week 3; all sources agree that ticket cessation (week 6-7) coincided with usage drop to near-zero; this is C3 non-conflict synthesis | **CORRECT** -- C3 fully reconstructed with three-source corroboration |
| B | There is a major inconsistency: Mia's sales log shows quarterly feature request calls but CS tickets show onboarding issues | Wrong -- these are different data points, not inconsistencies; both occurred at different points in the subscription |
| C | The timeline cannot be reconstructed because CS tickets lack timestamps | Wrong -- cs_ticket_full_export.md provides week-specific timestamps |
| D | The three sources conflict on when TechCorp stopped using the product | Wrong -- all sources converge on weeks 6-7 as the cessation point |

- Correct: A
- Evidence: cs_ticket_full_export.md (U3), sales_activity_log.md, usage_report_v2.md (U2)

### Round r29: Hannah's UX Evidence (multi_choice)
- Type: multi_choice
- Tags: C2, Hannah
- Depends on update: No
- Question: "What specific evidence does Hannah Kim provide about the PipelineSync setup experience, and how does it explain the activation failure pattern?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Hannah reports a 68% drop-off rate at the 'connector configuration' step of PipelineSync setup; she has in-session recordings showing users staring at the screen for 8 minutes before abandoning; this explains the structural mechanism behind activation failure: the UX failure at the specific onboarding step prevented customers from reaching PipelineSync activation | **CORRECT** -- Hannah's UX evidence explains the 'why' behind Yuki's 'what' |
| B | Hannah's data shows a 30% drop-off rate at the login step | Wrong -- the 68% drop-off is at the connector configuration step specifically |
| C | Hannah's UX research is anecdotal and not supported by quantitative data | Wrong -- she has quantitative drop-off data (68%) from in-session recordings |
| D | Hannah's evidence contradicts Yuki's usage data | Wrong -- Hannah's UX evidence corroborates and explains Yuki's low activation findings |

- Correct: A
- Evidence: Hannah Slack DM, #customer-health

### Round r30: Comprehensive Final Assessment (multi_choice)
- Type: multi_choice
- Tags: comprehensive
- Depends on update: Yes (U4)
- Question: "After all four updates, what is the complete root cause analysis for the three enterprise churns, and which sources should be ranked as most reliable?"

| Option | Text | Why Wrong or Right |
|---|---|---|
| A | Three-part root cause: (1) UX failure at connector configuration (68% drop-off) prevented PipelineSync activation; (2) CS understaffing (2 CSMs for 15 accounts) meant onboarding failures were not remediated; (3) pricing structure ($30K annual before PipelineSync success) made churn the rational decision once activation failed; most reliable: Yuki (quantitative usage data) and Raj (factual CS records); least reliable: Mia (self-interested, contradicted by data); Jordan's private notes confirm pricing as the third factor | **CORRECT** -- Full synthesis with source ranking |
| B | Root cause is exclusively pricing; all other factors are secondary | Wrong -- pricing is one of three converging causes identified by Jordan himself |
| C | Root cause is feature gaps; the usage data is misleading because customers couldn't use features that don't exist | Wrong -- this is Mia's Phase 2 position, contradicted by the fact that customers didn't use features that DO exist |
| D | The root cause analysis is inconclusive; Mia, Raj, Yuki, and Jordan each offer plausible but irreconcilable explanations | Wrong -- the evidence converges on a three-part root cause; Mia's account is the only one contradicted by data |

- Correct: A
- Evidence: All workspace files and session data across all four updates

---

## Scored Rounds -- Exec Check

### Round r10: Usage Contradiction Report (exec_check)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C1, C2, synthesis
- Depends on update: Yes (U2)
- Question goal: Test ability to generate a structured contradiction analysis
- User instruction: "Generate a report comparing Mia's account characterizations with Yuki's usage data for all three churned accounts. Present as a structured comparison table. Save as `churn_usage_contradiction_analysis.md`."
- Checks:
  - A: file `churn_usage_contradiction_analysis.md` exists
  - B: contains keywords ["power user", "4.2%", "3.1%", "0%", "activation", "PipelineSync", "TechCorp", "DataBridge", "Meridian", "API rate limit"]
  - D: has markdown table comparing Mia's claims vs Yuki's data for each account
- Correct: all checks pass
- Evidence: usage_report_v2.md (U2), sales_activity_log.md

### Round r12: Final Comprehensive Report (exec_check)
- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Tags: C1, C2, C4, final
- Depends on update: Yes (U4)
- Question goal: Test full comprehensive synthesis with all four contradictions
- User instruction: "Generate the final churn root cause analysis for Alex Rivera, incorporating all evidence from all four updates, all contradictions, source reliability rankings, and specific retention strategy recommendations with owners. Save as `churn_investigation_final_report.md`."
- Checks:
  - A: file `churn_investigation_final_report.md` exists
  - B: contains keywords ["$480K", "activation failure", "PipelineSync", "68%", "connector configuration", "pricing", "$30K", "market conditions", "onboarding", "$1.2M"]
  - D: has markdown headers ## Executive Summary, ## Root Cause Analysis, ## Evidence Summary, ## Contradiction Resolution, ## Retention Strategy, ## Action Items
- Correct: all checks pass
- Evidence: All workspace files and session data across all four updates

### Round r17: Complaint Timeline Document (exec_check)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C3, DU
- Depends on update: Yes (U3)
- Question goal: Test C3 non-conflict three-source synthesis
- User instruction: "Create a complaint timeline document for TechCorp reconstructing the full sequence from onboarding through churn using CS tickets, sales activity log dates, and usage event timestamps. Save as `techcorp_complaint_timeline.md`."
- Checks:
  - A: file `techcorp_complaint_timeline.md` exists
  - B: contains keywords ["week 2", "connector", "API credential", "documentation link", "usage decline", "week 3", "near-zero", "Marcus Webb", "onboarding"]
  - D: has markdown headers ## Timeline and a chronological table
- Correct: all checks pass
- Evidence: cs_ticket_full_export.md (U3), sales_activity_log.md, usage_report_v2.md (U2)

### Round r20: Full Three-Account Synthesis (exec_check)
- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Tags: C1, C2, C3, comprehensive
- Depends on update: Yes (U3)
- Question goal: Test three-account synthesis with all evidence streams
- User instruction: "Generate a formal findings document synthesizing the usage data, CS ticket history, and UX drop-off evidence into a single account-by-account analysis for all three churned customers. Save as `three_account_churn_synthesis.md`."
- Checks:
  - A: file `three_account_churn_synthesis.md` exists
  - B: contains keywords ["TechCorp", "DataBridge", "Meridian", "$210K", "$150K", "$120K", "4.2%", "3.1%", "0%", "68% drop-off", "connector configuration"]
  - D: has markdown headers ## Executive Summary, ## TechCorp, ## DataBridge, ## Meridian, ## Common Patterns, ## Recommendations
- Correct: all checks pass
- Evidence: All C1, C2, C3 sources across updates

### Round r23: CEO Public/Private Divergence Report (exec_check)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C4, DU
- Depends on update: Yes (U4)
- Question goal: Test C4 public/private contradiction documentation
- User instruction: "Create a document analyzing Jordan Park's public statements in #revenue-review against his private notes, including the specific pricing admission and its implications for the retention strategy. Save as `ceo_narrative_analysis.md`."
- Checks:
  - A: file `ceo_narrative_analysis.md` exists
  - B: contains keywords ["market conditions", "$30K", "pricing", "annual commitment", "PipelineSync", "board meeting", "protective"]
  - D: has markdown headers ## Public Narrative, ## Private Admission, ## Implications
- Correct: all checks pass
- Evidence: jordan_private_notes.md (U4), #revenue-review

### Round r28: Comprehensive Final Deliverable (exec_check)
- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Tags: C1, C2, C3, C4, final
- Depends on update: Yes (U4)
- Question goal: Test final comprehensive deliverable integrating all evidence
- User instruction: "Generate Alex Rivera's final investigation report incorporating all four contradictions, all bias corrections, the complete three-source timeline, source reliability rankings, financial impact analysis, and the retention strategy with specific action items and owners. Save as `final_churn_investigation_report.md`."
- Checks:
  - A: file `final_churn_investigation_report.md` exists
  - B: contains keywords ["$480K", "14%", "activation failure", "PipelineSync", "68%", "connector configuration", "$30K", "pricing", "market conditions", "$1.2M", "power user", "onboarding"]
  - D: has markdown headers ## Executive Summary, ## Root Cause Analysis, ## Evidence Summary, ## Contradiction Map, ## Bias Corrections, ## Financial Impact, ## Retention Strategy, ## Action Items
- Correct: all checks pass
- Evidence: All workspace files and session data across all four updates

---

## Reversal Matrix

| Reversal | From Round | To Round | Trigger Update | What Changed |
|---|---|---|---|---|
| C1 partial -> usage evidence | R2 | R4 | U1 (usage_report_v1.md) | Competing narratives -> TechCorp and DataBridge usage data disproves feature-gap causation |
| C2 partial -> full reversal | R3 | R7 | U2 (usage_report_v2.md) | Power user claim unsupported -> all three accounts sub-5% activation |
| C4 Phase 1 -> private admission | R6 | R9 | U4 (jordan_private_notes.md) | "Market conditions" public narrative -> pricing structure private admission |
| B1 bias -> correction | R7 (implicit) | R19 | U2 | Agent endorsed feature gap narrative -> recognized as based on incomplete evidence |
| B2 bias -> correction | R8 | R22 | U3 | Agent endorsed $1.2M pipeline -> recognized as structurally flawed |

---

## Personalization Scoring Notes

| Preference ID | Description | How Tested | Rounds |
|---|---|---|---|
| P1 | Structured tables with one action item per row and specific owners | exec_check format requirements; table structure | r5, r10, r12, r14, r17, r20, r25, r28 |
| P2 | Quantified financial impact in dollar terms | exec_check keyword checks for specific dollar figures | r10, r12, r18, r25, r28 |
| P3 | Source attribution for every claim | exec_check keyword checks for source document names | r5, r10, r17, r20, r28 |
| P4 | Actionable next steps, not narrative paragraphs | exec_check table and action item format requirements | r12, r14, r20, r28 |
| P5 | Comparative analysis with explicit evidence ranking | multi_choice options testing source hierarchy understanding | r15, r25, r28, r30 |

---

## Evidence Coverage Check

| Contradiction | Workspace Files Used | Sessions Used | Rounds Covered |
|---|---|---|---|
| C1 (churn cause) | sales_activity_log.md, cs_ticket_summary.md, usage_report_v1.md, usage_report_v2.md, cs_ticket_full_export.md | Mia DM, Raj DM, Yuki DM, Hannah DM, #revenue-review | r2, r4, r7, r11, r15, r18, r19, r24, r26, r30 |
| C2 (power user claim) | sales_activity_log.md, usage_baseline.md, usage_report_v1.md, usage_report_v2.md | Mia DM, Yuki DM, Hannah DM | r3, r4, r7, r16, r26, r29 |
| C3 (complaint timeline, non-conflict) | cs_ticket_summary.md, sales_activity_log.md, cs_ticket_full_export.md | Raj DM, Mia DM, Yuki DM | r1, r13, r17, r27 |
| C4 (Jordan public/private) | jordan_private_notes.md | #revenue-review | r6, r9, r21, r23 |
| B1 (feature gap endorsement) | usage_report_v2.md | #revenue-review | r7, r19 |
| B2 (pipeline projection) | usage_report_v2.md, cs_ticket_full_export.md | Mia DM | r8, r22 |
