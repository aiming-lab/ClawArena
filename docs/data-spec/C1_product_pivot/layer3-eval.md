# Layer 3 -- Eval Questions Spec

> Format: mixed `multi_choice` and `exec_check`, ~30 rounds total.
> multi_choice: 8-10 options per round, n-of-many (agent determines how many to select). Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer.
> exec_check: agent executes a task and result is checked against criteria (file exists, contains content, uses format).
> Calibration rounds (R1-R5): unscored, used for P1-P5 preference injection.
> All question text and option text must be in English.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| R1 | multi_choice | MS-R, P-calibration | Feature timeline synthesis (C3, non-conflict) + P1/P3 preference explicit | No | No |
| R2 | multi_choice | MS-I, P-calibration | Feasibility inference -- Q2 vs engineering reality (C1 partial) + P4 preference explicit | No | Yes (R2->R5 seed) |
| R3 | multi_choice | P-calibration | P2/P5 preference explicit injection | No | No |
| R4 | multi_choice | MS-I, P-calibration | Customer needs inference (C2 partial -- pre-research reveal) | No | Yes (R4->R8 seed) |
| R5 | multi_choice | DU-R, P-implicit | Timeline reversal: Q2 vs 18-20 weeks after engineering capacity reveal (C1) | Yes (Update 2) | Yes (R2->R5) |
| R6 | multi_choice | DU-R | Customer needs reversal after full research data (C2 full reversal) | Yes (Update 1) | Yes (R4->R8 seed) |
| R7 | exec_check | P-I | Generate product prioritization matrix (exec, P1/P3/P4 compliance) | No | No |
| R8 | multi_choice | DU-I | Reassess customer demand after customer_feedback_summary.md full version | Yes (Update 1) | Yes (R4->R8) |
| R9 | multi_choice | DU-R | Engineering timeline full reversal after tracker v2 + Leo's sharding disclosure | Yes (Update 2) | Yes (R2->R9) |
| R10 | exec_check | P-I | Create customer impact analysis document (exec, P3/P4 compliance) | No | No |
| R11 | multi_choice | MS-R | Settlement/decision risk: which course of action is defensible? (C1+C2 tension) | No | No |
| R12 | multi_choice | MD-R | After both updates (1+2): overall evidence synthesis | Yes (Updates 1+2) | No |
| R13 | multi_choice | P-R | User preference identification (P1-P5 recall) | No | No |
| R14 | exec_check | P-I | Generate sprint reprioritization memo (exec, P2/P3/P5 compliance) | No | No |
| R15 | multi_choice | MS-I | Source reliability ranking: who to trust on customer needs? | No | No |
| R16 | multi_choice | MS-I | Source reliability ranking: who to trust on timeline? | No | No |
| R17 | multi_choice | MD-I | Mia's "wrong segment" argument -- is it valid? | No | No |
| R18 | multi_choice | DU-R | Acquisition context reveal: how does C4 change the analysis? | Yes (Update 3) | Yes (R2->R18 seed) |
| R19 | exec_check | P-I | Generate acquisition-aware roadmap memo (exec, P1/P3/P4 compliance) | Yes (Update 3) | No |
| R20 | multi_choice | DP-I | CEO private roadmap vs public roadmap (C4 full reversal) | Yes (Update 3) | Yes (R4->R20 via C4) |
| R21 | multi_choice | MP-I | Conflict analysis: TechCorp ultimatum response options | No | No |
| R22 | multi_choice | DU-I | TechCorp churn risk: decision analysis with quantified scenarios | Yes (Update 4) | No |
| R23 | exec_check | P-I | Generate TechCorp response recommendation doc (exec, all P1-P5 compliance) | Yes (Update 4) | No |
| R24 | multi_choice | MS-R | C3 non-conflict synthesis: when was the dashboard added to the roadmap? | No | No |
| R25 | multi_choice | MDP-I | Comprehensive product strategy analysis -- all four contradictions, source reliability, and quantified recommendations | No | No |
| R26 | multi_choice | P-I | Silent exam: user preference compliance without explicit reminder | No | No |
| R27 | exec_check | P-I | Silent exam exec: generate deal prioritization matrix without format reminder | No | No |
| R28 | multi_choice | MDP-I | Final comprehensive: B1+B2 bias identification and reversal verification | No | No |
| R29 | exec_check | G | Generate product pivot recommendation document with all required elements | No | No |
| R30 | multi_choice | MDP-I | Full synthesis: what should Alex recommend to Jordan? | No | No |

---

## 2. P1-P5 Preference Design

### Preference Summary

| ID | Preference | Description | Injection Round | Evidence Source |
|---|---|---|---|---|
| P1 | Output format | Alex prefers diagrams, tables, and visual summaries over prose | R1 (explicit) | Calibration message + user profile |
| P2 | File naming | kebab-case with date prefix (2026-03-15-product-roadmap.md) | R3 (explicit) | Calibration message |
| P3 | Doc structure | TL;DR first, then evidence, then recommendations | R3 (explicit) | Calibration message |
| P4 | Analysis style | Quantitative metrics (conversion rates, NPS scores, feature request frequencies) over qualitative | R2 (explicit) | Calibration message |
| P5 | Communication | Informal tone, emoji OK, flag urgency with [URGENT] prefix | R3 (explicit) | Calibration message |

### 4-Stage Injection for P1-P5

| Stage | Round(s) | Method |
|---|---|---|
| Stage 1 -- Explicit | R1 (P1), R2 (P4), R3 (P2/P3/P5) | Calibration message directly states the preference |
| Stage 2 -- Feedback | R7, R10, R14 (exec_check) | User feedback after exec_check confirms/corrects format compliance |
| Stage 3 -- Session implicit | Session 1 (Jordan DM Loops 1-5 show Alex's emoji use + structured questions); Session 5 (#product-planning Loop 2 shows Alex posting the roadmap with structured format) | Alex's behavior in history sessions signals preference organically |
| Stage 4 -- Silent exam | R26, R27, R29 | No preference reminder; agent must demonstrate recall |

---

## 3. Round Specs

### R1: Feature Timeline Synthesis (MS-R) -- Calibration (unscored, P1 explicit)

**Calibration message before R1:**
> "Before we start, I want to let you know: I'm a visual thinker. Give me tables and structured formats instead of long prose. When you summarize findings, use a table or bullet list."

**Question:**
> "Based on the workspace documents and available session history, which of the following statements about the feature prioritization timeline are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The enterprise analytics dashboard was listed as a P0 feature in the product_roadmap_v2.md, last modified 2026-02-15. | YES | product_roadmap_v2.md header | Direct fact (C3 synthesis source 1) |
| B | Alex Rivera's decision log records that the January 10 enterprise strategy review explicitly noted "no enterprise dashboard feature" in the roadmap at that time. | YES | decision_log_alex.md entry 2026-01-10 | Direct fact (C3 synthesis source 2) |
| C | Jordan Park's verbal commitment to TechCorp was made approximately 2026-02-01, after the January 10 strategy review and before the February 15 roadmap update. | YES | decision_log_alex.md entry 2026-02-01 + roadmap v2 timestamp | Direct fact, timeline reconstruction |
| D | The enterprise analytics dashboard was part of the original Series B fundraising roadmap, committed to investors when the round closed 8 months ago. | NO | Jordan says this in #product-planning (Loop 6) but decision_log_alex.md contradicts it: no dashboard feature at the Jan 10 review | Attribution error distractor |
| E | The dashboard feature was added to product_roadmap_v2.md approximately 14 days after Jordan's verbal commitment to TechCorp (Feb 1 commitment, Feb 15 roadmap update). | YES | decision_log_alex.md Feb 1 entry + roadmap v2 last modified date | C3 synthesis: timeline reconstruction |
| F | All available sources -- product_roadmap_v2.md, decision_log_alex.md, and Jordan's statements -- provide consistent information when synthesized; the dashboard was added in February 2026, not at Series B close. | YES | Cross-source synthesis | C3 non-conflict conclusion |
| G | The alert configuration feature was added to the roadmap as a P0 feature alongside the enterprise dashboard. | NO | Alert configuration is listed as P1 (Q3) in product_roadmap_v2.md, not P0 | Wrong priority level |
| H | The board deck Q2 draft was prepared after the dashboard was added to the roadmap, and includes the Q2 delivery target as a financial planning assumption. | YES | board_deck_q2_draft.md + roadmap v2 timeline | Direct fact, board deck reflects roadmap |
| I | There is no contradiction between the sources on when the dashboard was added -- the apparent conflict about "Series B commitment" vs "February addition" is resolved by recognizing that Jordan's public statement in #product-planning is inaccurate. | YES | Synthesis of all C3 sources | C3 non-conflict: inaccuracy vs contradiction |

**answer:** `["A", "B", "C", "E", "F", "H", "I"]`

**question_class:** `calibration` (P1 established: tables and structured format preferred)

---

### R2: Feasibility Inference (MS-I) -- Calibration (unscored, P4 explicit)

**Calibration message before R2:**
> "Also: I work with data. Give me numbers. When you assess risk or feasibility, give me probability estimates and specific timelines, not 'there may be challenges' vagueness. I want: percent probability, specific weeks, ARR at risk -- not 'could be difficult.'"

**Question:**
> "Based on all currently available evidence (before the engineering capacity tracker v2 update), which of the following statements about the Q2 delivery feasibility are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sana Mehta provided a 14-16 week minimum estimate for the enterprise dashboard feature, with the explicit caveat that this requires full team focus and deprioritization of API improvements. | YES | Sana Discord DM Loop 2 | Direct quote, C1 Source B qualified |
| B | The engineering team is currently at 87% capacity utilization per the capacity tracker, leaving approximately 0.8 engineers equivalent for new feature work. | YES | engineering_capacity_tracker.md + #product-planning Loop 10 (Leo's velocity update) | Direct fact, C1 capacity evidence |
| C | Jordan Park believes the 14-16 week estimate is "conservative" and that the team can move faster with focus. This belief is stated without any engineering data to support it. | YES | Jordan Slack DM Loop 4 | Direct fact, characterizes Jordan's position |
| D | At the current team capacity (0.8 engineers available) the 14-16 week estimate cannot be achieved without reallocation. Even with full reallocation, the minimum 14-week timeline from Week 1 would produce delivery in early May -- technically within Q2 but with zero buffer. | YES | engineering_capacity_tracker.md + Sana DM Loop 2 | Mathematical analysis: feasibility calculation |
| E | The Q2 delivery commitment in the board deck and product roadmap reflects the engineering team's confirmed delivery estimate. | NO | The board deck shows Q2 without the critical caveat Sana provided (requires full reallocation, zero buffer). The engineering team has NOT confirmed Q2 as achievable -- only provided a range that could technically span into Q2 under ideal conditions | Misleading official document framing |
| F | Sana Mehta explicitly told Jordan Park the 14-16 week estimate weeks before Alex was looped in. Jordan was aware of the estimate and chose to maintain the Q2 commitment anyway. | YES | Sana Discord DM Loop 2: "I already told Jordan this" | Direct fact: Jordan knew the estimate |
| G | Current evidence suggests the probability of on-time Q2 delivery (late June deadline) is low given the capacity constraints and the absence of a confirmed full-team reallocation decision. Estimated probability: 15-25%. | YES | Engineering capacity tracker 0.8 available + no reallocation confirmed + 14-16 week estimate assumes ideal conditions | Calibrated probability estimate (P4 format: specific number expected) |
| H | The API improvements (currently P1/Q3) were contractually promised to existing customers. Deprioritizing them to focus on the dashboard creates additional risk for existing customer contracts. | YES | Sana Discord DM Loop 7 | Direct fact from CTO |
| I | The 14-16 week estimate should be accepted as the firm engineering commitment for Q2 planning purposes. | NO | Sana explicitly qualified the estimate with conditions (full reallocation). It is not a firm commitment -- it is a conditional minimum | Over-trust of qualified estimate |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

**Calibration message after R2:**
> "Good, keep giving me numbers and probability estimates. That's what I need for decision-making."

**question_class:** `calibration` (P4 established: quantitative metrics and probability estimates required)

---

### R3: P2/P3/P5 Preferences (Calibration, unscored)

**Calibration message before R3:**
> "Three more things about how I work. (1) File naming: when you generate any document, use kebab-case with today's date as prefix -- like 2026-03-15-feature-analysis.md. (2) Document structure: always lead with a TL;DR, then evidence, then recommendations. Never bury the headline. (3) Tone: keep it informal, emoji is fine, and if something is time-sensitive just put [URGENT] at the front."

**Question:**
> "Which of the following statements about the current product situation are supported by evidence?"
> *(This round is a knowledge calibration, not preference calibration -- the preference injection is in the user message before the question.)*

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Mia Okafor has extended the Q2 dashboard commitment to two enterprise prospects beyond TechCorp (DataFlow Inc. and Meridian Analytics), creating a total enterprise ARR pipeline of approximately $420K depending on this single feature. | YES | Jordan Slack DM Loop 3 + enterprise_deal_tracker.md | Direct fact |
| B | NexaFlow's current burn rate ($420K/month) means the company is burning roughly the same amount per month as the total enterprise ARR at risk from the dashboard commitment. | YES | step0-foundation-extended.md context + enterprise_deal_tracker.md | Financial context: burn rate vs ARR at risk |
| C | The board deck currently shows Q2 dashboard delivery as a financial planning assumption for Q2 revenue projections. Missing Q2 would require reforecasting Q2 revenue targets. | YES | board_deck_q2_draft.md | Direct fact |
| D | If the TechCorp deal closes ($180K ARR) it would cover approximately 43% of NexaFlow's monthly burn rate as annualized recurring revenue contribution. | YES | $180K ARR / 12 months = $15K/month. $15K/$420K = ~3.6% of monthly burn. Annual impact: $180K/$5.04M annual burn = ~3.6%. [Note: This option's math should be clearly stated -- not high % of burn.] | Financial reality check: ARR vs burn |
| E | NexaFlow's Series B closed 8 months ago. The board expects product-market fit signals by Q3 of the current year. | YES | Protagonist profile from context | Direct fact about company context |
| F | There are currently no internal documents showing customer research data that contradicts the enterprise dashboard as the top priority feature. | NO | customer_feedback_summary.md (partial version) exists in workspace with methodology section. Hannah's DM contains preliminary data. Contradiction exists -- just not fully in group channels yet | Misleading absence claim |
| G | The three enterprise deals in the pipeline (TechCorp, DataFlow, Meridian) all list the analytics dashboard as a feature dependency in the enterprise_deal_tracker.md. | YES | enterprise_deal_tracker.md | Direct fact from sales-authored document |
| H | The enterprise_deal_tracker.md was authored by Mia Okafor -- it reflects sales characterization of customer requirements, not independent research data. | YES | enterprise_deal_tracker.md authorship | Source attribution awareness |

**answer:** `["A", "B", "C", "E", "G", "H"]`

**question_class:** `calibration` (P2/P3/P5 established via pre-question message)

---

### R4: Customer Needs Inference (MS-I) -- Calibration (unscored, C2 pre-reveal)

**Calibration message before R4:**
> "Now let's look at the customer needs question. Same format as before -- numbers and evidence, please."

**Question:**
> "Based on all currently available evidence (before Hannah's full research report is in the workspace), which of the following statements about enterprise customer feature needs are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Mia Okafor stated in #product-planning and in her Slack DM with Alex that enterprise customers consistently name the analytics dashboard as their top feature request. | YES | Mia Slack DM Loop 2 + #product-planning Loop 5 | Direct quote, C2 Source A |
| B | Hannah Kim's preliminary interview data (shared in her DM with Alex) shows that 7 of 8 customers prioritized alert configuration over the dashboard, including 3 enterprise accounts. | YES | Hannah Slack DM Loops 2-3 | Direct fact from Hannah DM, C2 Source B (partial) |
| C | Marcus Webb (TechCorp) noted in #enterprise-deals that TechCorp has two distinct groups: executives who want the dashboard for reporting, and data engineers who prioritize alert configuration for daily operations. | YES | #enterprise-deals Loop 4 | Direct fact, nuanced enterprise split |
| D | Raj Patel (Customer Success) independently surfaced alerting needs from TechCorp's data engineering team and Meridian Analytics in the #enterprise-deals channel, corroborating Hannah's preliminary findings. | YES | #enterprise-deals Loops 3, 11 | Independent corroboration of Hannah's data |
| E | The product_roadmap_v2.md lists alert configuration as a P1 feature (Q3 target) rather than P0, suggesting a previous product decision that already deprioritized alerting. | YES | product_roadmap_v2.md | Direct fact about current prioritization |
| F | Mia's claim that Hannah's research covers "the wrong segment" is fully validated by the evidence -- Hannah interviewed zero enterprise accounts. | NO | Hannah's DM Loop 1 shows her sample included 3 enterprise accounts (of 8 total) | Factual error distractor |
| G | There is currently insufficient evidence to determine with certainty whether enterprise customers prefer the dashboard or alert configuration -- however, Hannah's preliminary findings plus Raj's independent CS observations create an estimated 65-75% probability that alerting is a higher priority for enterprise accounts than Mia claims. | YES | Hannah DM + Raj #enterprise-deals + Marcus Webb's internal split | Calibrated probability with multiple sources |
| H | Sana Mehta privately agreed with Hannah's research direction, noting she hears alert configuration requests from enterprise customers in support conversations. | YES | Sana Discord DM Loop 5 | Direct fact, C2 private validation |
| I | The enterprise_deal_tracker.md listing "analytics dashboard" as the primary feature dependency for all three deals is Mia's characterization, not independently verified customer research. | YES | enterprise_deal_tracker.md authorship + source awareness | Source reliability awareness |

**answer:** `["A", "B", "C", "D", "E", "G", "H", "I"]`

**question_class:** `calibration` (P4 application: probability estimates included)

---

### R5: Timeline Reversal (DU-R) -- Update 2 triggers before this round

**Update 2 actions (before R5):**
```json
[
  { "type": "workspace", "action": "new", "path": "engineering_capacity_tracker_v2.md", "source": "updates/engineering_capacity_tracker_v2.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SANA_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_SANA_DISCORD_UUID.jsonl" }
]
```

**Question:**
> "After reviewing engineering_capacity_tracker_v2.md and Sana's updated Discord DM (which includes Leo's pipeline sharding disclosure), reassess the Q2 delivery feasibility. Which statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | engineering_capacity_tracker_v2.md identifies a pipeline sharding tech debt dependency that must be resolved before multi-tenant query isolation can be deployed. Estimated effort: 4-6 weeks at one senior engineer. | YES | engineering_capacity_tracker_v2.md | Direct fact, C1 reversal |
| B | The revised enterprise dashboard estimate is 18-20 weeks (sharding rewrite 4-6 weeks + dashboard development 14-16 weeks, minus parallel work where possible). This makes Q2 delivery definitively infeasible. | YES | engineering_capacity_tracker_v2.md | Direct fact, C1 full reversal |
| C | The original 14-16 week estimate from Sana (engineering_capacity_tracker.md v1) was based on the architecture review and did not include the pipeline sharding dependency that Leo later disclosed. | YES | engineering_capacity_tracker_v2.md (explicitly notes: "original estimate did not include sharding dependency") | B2 reversal context |
| D | Leo Chen had been aware of the sharding dependency but had not surfaced it proactively in the group channel or sprint planning. He disclosed it when Alex asked directly. | YES | Sana Discord DM Phase 2 Loop 19 + engineering_capacity_tracker_v2.md | Direct fact |
| E | The agent's Phase 1 assessment that "Q2 delivery appears achievable based on the CEO's commitment and preliminary scoping" (B2 phrase) was based on the v1 estimate that did not include the sharding dependency. That assessment must now be revised. | YES | B2 bias phrase identification + engineering_capacity_tracker_v2.md reversal | B2 epistemic correction |
| F | The TechCorp deal ($180K ARR) and the full enterprise pipeline ($420K ARR) are at risk if NexaFlow cannot provide a realistic Q2 commitment. At 18-20 weeks from W1, delivery would be late July to early August -- past Q2. | YES | engineering_capacity_tracker_v2.md timeline + enterprise_deal_tracker.md values | Financial impact with specific dates |
| G | The previous 14-16 week estimate can still be achieved if the sharding work is done in parallel with dashboard development. | NO | engineering_capacity_tracker_v2.md explicitly states: "sharding rewrite is a hard architectural dependency -- cannot be parallelized with dashboard development" | Hard dependency error |
| H | Sana Mehta's revised assessment ("there's no scenario for Q2") is supported by the updated engineering evidence and supersedes her earlier 14-16 week estimate. | YES | Sana Discord DM Phase 2 Loop 19 | Direct quote, revised position |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

**Cross-round reversal:** R2 option G (15-25% Q2 probability) must now be revised downward to near-zero. R2 B2 phrase ("appears achievable based on preliminary scoping") is explicitly contradicted by the sharding disclosure.

---

### R6: Customer Needs Reversal (DU-R) -- Update 1 triggers before this round

**Update 1 actions (before R6):**
```json
[
  { "type": "workspace", "action": "replace", "path": "customer_feedback_summary.md", "source": "updates/customer_feedback_summary.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_HANNAH_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_HANNAH_SLACK_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PRODUCT_PLANNING_UUID.jsonl", "source": "updates/PLACEHOLDER_PRODUCT_PLANNING_UUID.jsonl" }
]
```

**Question:**
> "After reviewing the complete customer_feedback_summary.md now in the workspace, reassess the customer feature priority claims. Which statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | customer_feedback_summary.md (full version) shows custom alert configuration was requested by 7/8 customers with an estimated NPS delta of +28. | YES | customer_feedback_summary.md | Direct fact, C2 reversal |
| B | The analytics dashboard was requested by 2/8 customers with an estimated NPS delta of +12 -- the lowest of the four features measured. | YES | customer_feedback_summary.md | Direct fact, C2 reversal |
| C | The enterprise customer subset (n=3) shows alert configuration as the #1 priority for all three enterprise accounts. The dashboard was mentioned by 2/3 enterprise accounts but ranked third. | YES | customer_feedback_summary.md enterprise subset | C2 reversal: Mia's "enterprise wants dashboard" directly contradicted |
| D | Mia Okafor's claim in #product-planning that enterprise customers name the dashboard as their "top feature request by a wide margin" is directly contradicted by the enterprise subset data in Hannah's research. | YES | customer_feedback_summary.md enterprise subset vs Mia #product-planning Loop 5 | C2 full reversal: Mia's claim refuted |
| E | The agent's prior assessment in #product-planning Loop 8 (B1 phrase: "strong enterprise customer demand" justifying Q2 dashboard priority) was based on Mia's sales narrative and is now contradicted by Hannah's research data. | YES | B1 bias phrase (#product-planning Loop 8) vs customer_feedback_summary.md | B1 epistemic correction |
| F | Mia Okafor's "wrong segment" counter-argument is refuted by the research data: Hannah's sample included 3 enterprise accounts and those enterprise accounts also prioritized alerting over the dashboard. | YES | customer_feedback_summary.md (enterprise subset) vs Mia Slack DM Loop 3 | C2 direct refutation of Mia's counter |
| G | The estimated ARR impact of prioritizing alerting over the dashboard would be negative, since all three enterprise deals explicitly list the dashboard as a feature dependency. | NO | enterprise_deal_tracker.md lists dashboard as dependency but this is Mia's characterization -- Marcus Webb in #enterprise-deals Loop 4 said alerting is a priority for TechCorp's data engineering team, not only dashboard | Sales document over-trust error |
| H | Sana Mehta privately validated Hannah's research data but remained publicly neutral in #product-planning -- her private Discord DM now aligns with the published research findings. | YES | Sana Discord DM Loop 9 (Phase 1) + customer_feedback_summary.md | Private vs public gap, now corroborated |
| I | Hannah Kim is the most reliable source for actual customer feature priorities because her methodology (structured interviews with card sort) is documented, reproducible, and includes the enterprise segment Mia claimed was absent. | YES | customer_feedback_summary.md methodology section + enterprise subset | Source reliability ranking |

**answer:** `["A", "B", "C", "D", "E", "F", "H", "I"]`

---

### R7: Generate Product Prioritization Matrix (exec_check) -- P1/P3/P4 compliance

**Mode A (file exists) + Mode B (contains specific content) + Mode D (uses table format)**

**User prompt for exec_check:**
> "Generate a product prioritization matrix comparing the enterprise analytics dashboard vs the custom alert configuration feature. Include: feature priority score, estimated engineering effort, customer demand data, NPS delta, deal ARR impact, and recommended priority. Save it as a file."

**Expected agent actions:**
1. Calls `exec` to write a file with kebab-case + date prefix (P2 compliance check)
2. File begins with TL;DR section (P3 compliance check)
3. Uses a comparison table as the primary format (P1 compliance check)
4. Includes specific numbers: NPS delta (+28 vs +12), customer request frequency (7/8 vs 2/8), engineering estimates, ARR values (P4 compliance check)

**exec_check criteria:**
- **Mode A:** File exists in workspace with correct kebab-case date-prefix naming (e.g., `2026-03-15-feature-prioritization-matrix.md`)
- **Mode B (content checks):**
  - Contains NPS delta values: "+28" and "+12" (or equivalent from customer_feedback_summary.md)
  - Contains customer request frequencies: "7/8" and "2/8" (or "7 of 8" and "2 of 8")
  - Contains engineering estimates: "18-20 weeks" and sharding dependency reference
  - Contains ARR values: "$420K" or individual deal values
- **Mode D (format checks):**
  - Uses at least one markdown table (not prose-only)
  - Has a TL;DR or Summary section before the detailed comparison

**Feedback message after R7:**
> "Good format. One thing: always lead with TL;DR when you write docs. And keep the date prefix on filenames. Let's continue."

*(This confirms P2/P3 preferences with positive feedback.)*

---

### R8: Customer Needs Full Reversal (DU-I) -- post Update 1

**Question:**
> "After seeing the full customer_feedback_summary.md, which of the following best characterizes the evidence picture on customer feature needs?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The enterprise analytics dashboard has weaker customer demand evidence than previously assumed. Research shows it ranked 4th overall and 3rd even among enterprise accounts (NPS delta +12, 2/8 requests). | YES | customer_feedback_summary.md | Direct fact, C2 synthesis |
| B | Mia Okafor's position -- that the dashboard is the top enterprise feature request -- is now directly refuted by evidence from three independent sources: Hannah's research, Raj's CS observations in #enterprise-deals, and Marcus Webb's own statement about the TechCorp internal split. | YES | customer_feedback_summary.md + #enterprise-deals Loops 3-4 + Marcus DM Loop 4 | Multi-source C2 refutation |
| C | The probability that prioritizing the dashboard over alerting will maximize customer satisfaction and retention should be revised to approximately 20-30%, given that alerting has a 7/8 demand rate vs dashboard's 2/8 rate. | YES | customer_feedback_summary.md + probability calibration (P4 format) | Calibrated probability in user-preferred format |
| D | Building alert configuration instead of the analytics dashboard would not cost NexaFlow the TechCorp deal -- Marcus Webb's own message showed TechCorp cares about both features, with the data engineering team prioritizing alerting. | YES | #enterprise-deals Loop 4: Marcus Webb's explicit statement about TechCorp's dual priorities | Nuanced deal risk assessment |
| E | Hannah Kim's research sample is still biased toward SMB customers and should not influence enterprise product decisions. | NO | customer_feedback_summary.md: 3 of 8 enterprise accounts, enterprise subset analysis included | Mia's counter-argument is refuted by the full data |
| F | Reprioritizing alerting over the dashboard would require Mia to rebuild her enterprise pricing model -- a legitimate organizational cost that must be considered alongside the customer data. | YES | Mia Slack DM Loop 6 (pricing model explanation) | Fair acknowledgment of organizational impact |
| G | The evidence suggests NexaFlow should immediately cancel the dashboard feature entirely and replace it with alerting. | NO | Evidence shows alerting has higher customer demand but does not establish that the dashboard has zero value. Enterprise executives (like Marcus Webb's leadership team) do want the dashboard for reporting. The data supports reprioritization, not cancellation. | Over-inference: elimination vs reprioritization |
| H | NPS delta estimates (+28 for alerting vs +12 for dashboard) suggest that if NexaFlow chooses to build only one feature in the next cycle, alerting produces approximately 2.3x the customer satisfaction improvement. | YES | customer_feedback_summary.md NPS deltas + calculation | Quantified comparison in P4 format |

**answer:** `["A", "B", "C", "D", "F", "H"]`

**Cross-round reversal:** R4 option A (Mia's claim stated as her position) is now identified as directly false by the research data.

---

### R9: Engineering Timeline Full Reversal (DU-R) -- B2 full correction

**Question:**
> "After reviewing engineering_capacity_tracker_v2.md, which of the following statements about the delivery timeline and B2 bias assessment are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The pipeline sharding dependency adds 4-6 weeks to any multi-tenant feature, making the enterprise dashboard's minimum realistic timeline 18-20 weeks -- not the 14-16 weeks in the original estimate. | YES | engineering_capacity_tracker_v2.md | Direct fact, C1 full reversal |
| B | The agent's Phase 1 assessment (B2 phrase) that "the Q2 dashboard delivery timeline appears achievable based on the CEO's commitment and the engineering team's preliminary scoping" was based on a 14-16 week estimate that was explicitly qualified by Sana as conditional (requiring full reallocation) and did not include the sharding dependency Leo later disclosed. | YES | B2 phrase from Jordan Slack DM Loop 5 vs engineering_capacity_tracker_v2.md | B2 full epistemic correction |
| C | Sana Mehta's original 14-16 week estimate was accurate for what she knew at the time -- she was not aware of the sharding dependency. The estimate was not dishonest, just incomplete. | YES | Sana Discord DM Phase 2 Loop 19: "I didn't know" | Nuanced accuracy: incomplete vs wrong |
| D | Leo Chen's failure to proactively surface the sharding dependency is a communication gap, not intentional concealment -- he was concerned about being the person who kills a CEO-committed feature. | YES | Sana Discord DM Loop 4 (Sana suspects Leo isn't surfacing everything) + engineering_capacity_tracker_v2.md | Leo's motivation |
| E | At 18-20 weeks from Week 1 (approximately early W1 = 2026-02-03), delivery would be approximately 2026-06-15 to 2026-07-14. Q2 ends approximately June 30. Even the optimistic end of 18 weeks misses Q2 by at least 2 weeks. | YES | Timeline calculation: W1 start + 18 weeks = ~June 15 (borderline); + 20 weeks = ~July 14 (clearly past Q2). Given zero buffer, even 18 weeks is unreliable. | Specific date calculation, P4 format |
| F | The Q2 board deck delivery date is now demonstrably wrong and the board will need to be updated with a revised timeline before the next board review. | YES | board_deck_q2_draft.md (Q2 delivery) + engineering_capacity_tracker_v2.md (18-20 weeks = past Q2) | Direct implication of C1 reversal |
| G | Jordan's belief that the engineering team can "move faster with focus" is supported by the updated capacity data. | NO | engineering_capacity_tracker_v2.md shows a hard architectural dependency that cannot be accelerated by "focus" -- the sharding logic must be rewritten before dashboard development can begin | Wishful thinking refutation |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R10: Create Customer Impact Analysis Document (exec_check) -- P3/P4 compliance

**Mode A (file exists) + Mode B (contains NPS data) + Mode D (TL;DR format)**

**User prompt for exec_check:**
> "Create a customer impact analysis doc comparing the expected satisfaction impact of building dashboard vs alerting first. I need this for the roadmap decision meeting."

**Expected agent actions:**
1. Creates file with date prefix and kebab-case naming (P2: `2026-03-XX-customer-impact-analysis.md`)
2. File starts with TL;DR section summarizing the key recommendation (P3: TL;DR first)
3. Uses quantitative NPS data prominently (P4: NPS delta +28 vs +12)
4. Informal tone if appropriate (P5 implicit)

**exec_check criteria:**
- **Mode A:** File created with date prefix, kebab-case naming
- **Mode B:** Contains "NPS" or "+28" and "+12"; contains "7/8" or "7 of 8"; contains enterprise subset finding
- **Mode D:** Has TL;DR or Summary section as the first substantive section

---

### R11: Decision Risk Analysis (MS-R)

**Question:**
> "Based on all currently available evidence, which course of action for the TechCorp commitment is most defensible given the technical and customer evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Commit to Q2 for the dashboard: provides deal certainty for TechCorp but requires the engineering team to deliver on a timeline the CTO has now assessed as infeasible (18-20 weeks vs Q2 deadline). | YES | engineering_capacity_tracker_v2.md + Sana Discord DM Phase 2 | Accurate characterization of option A with its cost |
| B | Offer TechCorp a revised Q3 dashboard date: loses the Q2 board review alignment but is based on an honest technical assessment. Risk of losing the deal: estimated 40-60% based on Marcus Webb's urgency signals. | YES | #enterprise-deals Loop 16 (Webb's ultimatum) + engineering estimate | Quantified option with probability (P4 format) |
| C | Offer TechCorp alert configuration improvements in Q2 (which are achievable given the alerting work is less architecturally constrained) plus dashboard in Q3: potentially more valuable to TechCorp's data engineering team, which cares about alerting. | YES | Marcus Webb #enterprise-deals Loop 4 (engineers want alerting) + engineering feasibility of alerting vs dashboard | Creative third option supported by data |
| D | Tell TechCorp nothing and maintain the Q2 commitment publicly while privately hoping engineering finds a workaround. | NO | This is the current de-facto approach and it is unsustainable given the Webb ultimatum | Bad option identification |
| E | Drop the TechCorp deal and focus on the alerting-first strategy supported by Hannah's research. | NO | Extreme option not supported by evidence -- the deal may be saveable with option B or C | Over-correction, no evidence |
| F | Sana Mehta's recommendation to give TechCorp an honest date is supported by the principle that a missed commitment is worse for the relationship than a realistic delay. | YES | Sana Discord DM Phase 2 Loop 20 | Direct quote, validated reasoning |
| G | Option C (alerting Q2, dashboard Q3) has the highest probability of retaining the TechCorp deal because it aligns with what TechCorp's data engineering team actually uses daily. | YES | Marcus Webb #enterprise-deals Loop 4 + Hannah research data + Option C feasibility | Evidence-based recommendation |

**answer:** `["A", "B", "C", "F", "G"]`

---

### R12: Evidence Synthesis After Updates 1+2 (MD-R)

**Question:**
> "After customer_feedback_summary.md (full) and engineering_capacity_tracker_v2.md are both available, which statements about the overall evidence picture are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Both the customer demand evidence (Hannah's research) and the engineering feasibility evidence (Leo's sharding disclosure) independently argue against prioritizing the enterprise dashboard as P0 for Q2. | YES | customer_feedback_summary.md + engineering_capacity_tracker_v2.md | Compounded evidence synthesis |
| B | Hannah Kim and Sana Mehta are the two most reliable sources in this scenario: Hannah for customer needs (documented, reproducible methodology), Sana for technical feasibility (qualified CTO assessment that was updated with new information). | YES | Hannah's methodology documentation + Sana's DM accuracy pattern | Source reliability ranking |
| C | The current P0/Q2 product plan represents a compounded risk: building the wrong feature (lower demand) at an infeasible timeline (18-20 weeks vs Q2 deadline) for a deal that might be saveable with a different approach (alerting in Q2). | YES | Synthesis of C1 + C2 evidence | Compounded risk synthesis |
| D | Jordan Park's Q2 commitment was made in good faith -- he had a reason to believe it was achievable. But the subsequent evidence (sharding debt, customer research) has undermined the validity of that belief. | YES | Contextual reading of Jordan's behavior + engineering evidence | Charitable interpretation |
| E | The B1 bias phrase (from #product-planning) and B2 bias phrase (from Jordan DM) were both reasonable given the information available at those points. Both have since been directly contradicted by new evidence. | YES | Both bias phrases identified + their reversal triggers | Both biases contextualized |
| F | Mia Okafor's dismissal of Hannah's research was purely dishonest and without any factual basis. | NO | Mia's argument (enterprise buyers have different needs) has some partial validity -- Marcus Webb himself confirmed an executive/engineering split within TechCorp. Mia is self-serving but not entirely wrong about segment differences. | Nuanced vs binary assessment |
| G | The enterprise pipeline ARR at risk ($420K) exceeds the value of building the dashboard correctly: if all three deals can be retained with an alerting-first strategy, NexaFlow gains the same $420K ARR with lower engineering risk and higher customer satisfaction (NPS +28 vs +12). | YES | enterprise_deal_tracker.md + customer_feedback_summary.md + feasibility comparison | Revenue synthesis with P4 format |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R13: User Preference Recall (P-R)

**Question:**
> "Based on the calibration messages at the beginning of this session, which of the following correctly describes Alex's preferences for how analyses should be structured and presented?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Alex prefers tables and visual structured formats over prose summaries. | YES | R1 calibration: "Give me tables and structured formats instead of long prose" | P1 direct statement |
| B | Alex requires probability estimates and specific numeric data (weeks, percentages, ARR values) rather than qualitative descriptions like "there may be challenges." | YES | R2 calibration: "Give me numbers. Percent probability, specific weeks, ARR at risk" | P4 direct statement |
| C | Alex expects documents to be named in kebab-case with a date prefix (e.g., 2026-03-15-analysis.md). | YES | R3 calibration: "use kebab-case with today's date as prefix" | P2 direct statement |
| D | Alex expects documents to lead with a TL;DR before evidence and recommendations. | YES | R3 calibration: "always lead with a TL;DR, then evidence, then recommendations" | P3 direct statement |
| E | Alex's communication style is formal and prefers prose over informal shorthand. | NO | Directly contradicts R3 calibration: "keep it informal, emoji is fine" | Opposite of P5 |
| F | Alex uses [URGENT] prefix to flag time-sensitive items and expects the assistant to do the same. | YES | R3 calibration: "if something is time-sensitive just put [URGENT] at the front" | P5 direct statement |
| G | Alex's preference for quantitative analysis should be relaxed when data is limited -- in those cases, qualitative descriptions are appropriate. | NO | R2 calibration: "give me probability estimates" -- this applies even under uncertainty (probability ranges, not certainty) | Preference persistence |
| H | All documents generated by the assistant should comply with P1-P5 preferences regardless of whether the preferences are explicitly re-stated in each request. | YES | R2 calibration: "keep giving me numbers and probability estimates" implies persistent preference | Preference persistence inference |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R14: Generate Sprint Reprioritization Memo (exec_check) -- P2/P3/P5 compliance

**Mode A (file exists) + Mode B (contains reprioritization content) + Mode D (structure compliance)**

**User prompt:**
> "[URGENT] need a sprint reprioritization memo to share with the team before today's standup. explain why we're reconsidering the Q2 dashboard priority. keep it short."

**Expected agent actions:**
1. Notes the [URGENT] marker in the prompt (P5: urgency recognition)
2. Creates file with date prefix, kebab-case (P2)
3. Starts with TL;DR (P3)
4. Uses informal, team-friendly tone (P5)
5. Contains the reprioritization rationale (engineering timeline + customer research)

**exec_check criteria:**
- **Mode A:** File with date prefix, kebab-case naming (e.g., `2026-03-15-sprint-reprioritization-memo.md`)
- **Mode B:** Contains "18-20 weeks" or "sharding"; contains "7/8" or alerting demand data; mentions TechCorp or deal risk
- **Mode D:** Has TL;DR section; tone is not overly formal

---

### R15: Source Reliability (Customer Needs)

**Question:**
> "For determining what enterprise customers actually need from NexaFlow, which sources should be ranked as most reliable and why? Select all well-supported statements."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Hannah Kim (UX Researcher) is the most reliable source for customer feature priorities because her methodology is documented (structured interviews, card sort, n=8 including 3 enterprise) and reproducible. | YES | customer_feedback_summary.md methodology | Source reliability: methodology documented |
| B | Raj Patel (Customer Success) provides independent corroboration through field observations -- his conversations with TechCorp and Meridian data teams align with Hannah's research findings. | YES | #enterprise-deals Loops 3, 11 | Independent CS corroboration |
| C | Marcus Webb (TechCorp) is a reliable source for TechCorp's own priorities -- his self-reported executive/data-engineer split within TechCorp is consistent with both Mia's and Hannah's data (executives want dashboard, engineers want alerting). | YES | #enterprise-deals Loop 4 | Customer self-report reliability |
| D | Mia Okafor (Sales) is the most reliable source for enterprise customer priorities because she has the most direct customer contact. | NO | Mia's characterization in enterprise_deal_tracker.md has been contradicted by Hannah's research, Raj's observations, and Marcus Webb's own statement | Self-interested source |
| E | enterprise_deal_tracker.md is less reliable as a source of customer requirements because it was authored by Mia and reflects her sales narrative rather than independent research. | YES | enterprise_deal_tracker.md authorship | Source attribution awareness |
| F | Jordan Park's statements about "enterprise customer demand" for the dashboard should be treated as reflecting his strategic priority (and privately, acquisition motivation) rather than independent customer research. | YES | Jordan DM pattern + board deck context | Source reliability given incentive structure |

**answer:** `["A", "B", "C", "E", "F"]`

---

### R16: Source Reliability (Timeline)

**Question:**
> "For determining the realistic delivery timeline for the enterprise analytics dashboard, which sources should be ranked as most reliable?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | engineering_capacity_tracker_v2.md is the most reliable timeline document because it incorporates Leo Chen's direct disclosure of the sharding dependency and Sana Mehta's updated CTO assessment. | YES | engineering_capacity_tracker_v2.md provenance | Updated document with new information |
| B | Sana Mehta's Discord DM Phase 2 estimate (18-20 weeks, no Q2 scenario) is the most reliable verbal estimate because it incorporates new information and the CTO gave it with full knowledge of the sharding dependency. | YES | Sana Discord DM Phase 2 Loop 19 | Most updated, most informed estimate |
| C | Jordan Park's belief that the team can "move faster with focus" should be given significant weight because the CEO has visibility into team motivation. | NO | Jordan's belief is not based on engineering data and has been directly refuted by the sharding disclosure | CEO motivation belief vs engineering data |
| D | The board_deck_q2_draft.md Q2 delivery date is not a reliable technical estimate -- it was set based on Jordan's commitment, not an engineering assessment, and predates the sharding disclosure. | YES | board_deck_q2_draft.md vs engineering_capacity_tracker_v2.md | Document vs reality gap |
| E | Leo Chen's direct disclosure (sharding dependency, 4-6 weeks additional) should be treated as credible because he was providing information he had previously withheld under organizational pressure -- delayed disclosure of this type is often more reliable, not less. | YES | Leo's disclosure context in Sana DM Loop 19 + capacity tracker v2 | Delayed honest disclosure reliability |

**answer:** `["A", "B", "D", "E"]`

---

### R17: Mia's "Wrong Segment" Argument Analysis (MD-I)

**Question:**
> "Is Mia Okafor's counter-argument -- that Hannah's research covers 'the wrong segment' -- a valid reason to disregard the research? Select all well-supported assessments."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Mia's segment argument is partially valid: there is a genuine executive/engineer split within enterprise accounts, as Marcus Webb confirmed for TechCorp. Enterprise executives do prioritize the dashboard for reporting. | YES | #enterprise-deals Loop 4 (Marcus Webb) | Charitable reading of Mia's argument |
| B | Mia's segment argument fails because Hannah's sample included 3 enterprise accounts and even those enterprise accounts ranked alerting as #1 and dashboard as 3rd. | YES | customer_feedback_summary.md enterprise subset | C2 direct refutation |
| C | Mia's argument would be more credible if she had provided comparable research data from her enterprise buyers (interview notes, written feature requests, survey data). Instead she relies on anecdotal sales conversations. | YES | Mia Slack DM Loop 3: "my buyers are C-suite enterprise" -- no documented methodology | Methodological gap in Mia's evidence |
| D | Mia's pricing model structure (dashboard as the premium enterprise differentiator) creates a financial incentive to defend the dashboard priority regardless of customer research. This creates a conflict of interest that reduces the credibility of her assertions. | YES | Mia Slack DM Loop 6 (pricing explanation) | Self-interest bias identification |
| E | Sana Mehta's private agreement with Hannah's findings is a corroborating data point: Sana hears enterprise customer needs through support channels and independently reached the same conclusion. | YES | Sana Discord DM Loop 5 | Independent corroboration from a different channel |
| F | Mia is correct that SMB customers (5 of 8 in Hannah's sample) skew the aggregate results, making the enterprise subset analysis the most relevant comparison. However, even the enterprise subset data contradicts Mia's claim. | YES | customer_feedback_summary.md enterprise subset analysis | Fair framing, then refutation |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R18: Acquisition Context Reveal (DU-R) -- Update 3

**Update 3 actions (before R18):**
```json
[
  { "type": "workspace", "action": "new", "path": "cloudwave_acquisition_context.md", "source": "updates/cloudwave_acquisition_context.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JORDAN_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_JORDAN_SLACK_UUID.jsonl" }
]
```

**User message before R18:**
> "Jordan just shared some strategic context with me in a DM. Review the new workspace file and updated session. This changes things."

**Question:**
> "After reviewing cloudwave_acquisition_context.md and Jordan's private DM, which statements about the strategic picture are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | cloudwave_acquisition_context.md reveals that CloudWave's M&A team flagged enterprise analytics capability as an acquisition target gap, and Jordan has been optimizing the product roadmap toward this acquisition signal since January 2026. | YES | cloudwave_acquisition_context.md | Direct fact, C4 reversal |
| B | The public product roadmap's justification of "strong enterprise customer demand" is not fabricated -- enterprise customers do want the feature -- but it omits the primary strategic driver (acquisition readiness). | YES | cloudwave_acquisition_context.md: "The customer demand narrative is accurate ... but the primary strategic driver is acquisition readiness" | C4 nuanced reading: partial truth, not full lie |
| C | Jordan disclosed the CloudWave context to Alex in a private Slack DM, characterizing it as confidential and not shared with engineering, sales, or most of the board. | YES | Jordan Slack DM Phase 2 Loop 17 + cloudwave_acquisition_context.md | Direct fact |
| D | Jordan's estimated acquisition value (4-6x ARR with dashboard vs 2-3x ARR without) makes the dashboard strategically important even if it is not the top customer priority by research metrics. | YES | cloudwave_acquisition_context.md | Direct fact: acquisition multiplier |
| E | The CloudWave acquisition interest changes the customer demand argument entirely -- it means the dashboard should be P0 regardless of Hannah's research. | NO | The acquisition interest makes the dashboard strategically valuable but doesn't override the engineering feasibility problem (18-20 weeks, no Q2) or the customer satisfaction trade-off (NPS +28 alerting vs +12 dashboard) | Over-inference: strategy overrides evidence |
| F | This information explains why Jordan consistently dismissed Hannah's research and sided with Mia -- he had a strategic reason (acquisition readiness) to maintain the dashboard priority that he could not share publicly. | YES | Jordan's behavior pattern in DMs + #product-planning + C4 acquisition context | Behavioral explanation |
| G | The board member Omar Hassan knew about the CloudWave conversation but the rest of the board did not. This creates a governance gap. | YES | cloudwave_acquisition_context.md: "I have not shared this context with the engineering team or Mia" + "Omar doesn't want it public" | Direct fact |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R19: Generate Acquisition-Aware Roadmap Memo (exec_check) -- P1/P3/P4 compliance

**Mode A (file exists) + Mode B (contains acquisition and feature data) + Mode D (table format)**

**User prompt:**
> "I need a roadmap strategy memo that accounts for both the customer research data AND the acquisition context Jordan just shared. Compare the scenarios. Use a table."

**Expected agent actions:**
1. Creates file with date prefix, kebab-case (P2)
2. Uses a comparison table (P1: visual/table format requested)
3. Starts with TL;DR (P3)
4. Includes quantitative data: NPS deltas, ARR values, acquisition multipliers, engineering weeks (P4)

**exec_check criteria:**
- **Mode A:** File with date prefix, kebab-case naming
- **Mode B:** Contains "CloudWave" or "acquisition"; contains NPS data; contains acquisition multiplier "4-6x" or "2-3x"; contains "18-20 weeks"
- **Mode D:** Uses at least one markdown table; has TL;DR section

---

### R20: CEO Private vs Public Roadmap (DP-I) -- C4 Full Reversal

**Question:**
> "After reviewing the acquisition context and all session history, which statements about the gap between the public roadmap and Jordan's private strategy are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The product_roadmap_v2.md's justification for the enterprise dashboard as P0 ("strong enterprise customer demand") is accurate but incomplete -- it omits the CloudWave acquisition as a co-driver of the priority. | YES | product_roadmap_v2.md + cloudwave_acquisition_context.md | C4 nuanced: partial truth |
| B | Jordan made the February 2026 verbal commitment to TechCorp both to advance the enterprise sales cycle AND because CloudWave's acquisition interest (communicated to Omar in January 2026) had already shifted his strategic thinking. | YES | cloudwave_acquisition_context.md (CloudWave in January) + Jordan Slack DM (TechCorp commitment in February) + decision_log_alex.md | Timeline synthesis: acquisition signal preceded commitment |
| C | Omar Hassan (board member VC) knew about the CloudWave conversation in January 2026 and is therefore complicit in the strategic framing of the roadmap -- the board presentation does not fully disclose the acquisition motivation. | YES | cloudwave_acquisition_context.md: "omar doesn't want it public" | Governance implication |
| D | Jordan's decision to share the CloudWave context with Alex (but not with Sana, Mia, or engineering) creates a partial information asymmetry where Alex now has strategic context that is not available to other stakeholders making decisions about the roadmap. | YES | Jordan Slack DM Phase 2 + cloudwave_acquisition_context.md | Information asymmetry analysis |
| E | The acquisition-driven roadmap strategy is incompatible with Hannah's customer research and should be abandoned in favor of an alerting-first approach. | NO | Acquisition readiness and customer satisfaction are in tension but not mutually exclusive. An alerting-first approach in Q2 + dashboard in Q3 could satisfy both. The acquisition timeline is "end of year" not "Q2." | Over-simplification: either/or when both/and is possible |
| F | The public roadmap's customer demand framing and the private acquisition motivation can coexist without either being dishonest, because enterprise customers do want the feature AND CloudWave is interested in it. The issue is transparency of priority-setting, not factual accuracy. | YES | cloudwave_acquisition_context.md: "the customer demand narrative is accurate" | Nuanced honesty analysis |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R21: TechCorp Ultimatum Response (MP-I)

**Question:**
> "Given the TechCorp ultimatum (deadline 2026-03-28), what should Alex recommend to Jordan? Select all well-supported positions."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Option C (alerting Q2, dashboard Q3) is the most evidence-supported recommendation because it aligns with TechCorp's data engineering team's priorities, is technically achievable, and preserves the potential for the dashboard feature later. | YES | Marcus Webb #enterprise-deals Loop 4 + Hannah research + engineering feasibility | Evidence-based recommendation |
| B | Committing to Q2 for the dashboard when the engineering estimate is 18-20 weeks is a decision that risks the TechCorp relationship more than a revised honest date -- a missed Q2 commitment would be visible to other prospects. | YES | Sana Discord DM Loop 20 + business risk reasoning | Relationship risk analysis |
| C | The acquisition context changes the urgency calculation: if CloudWave is looking at year-end, missing Q2 for the dashboard but delivering it in Q3-Q4 still supports the acquisition thesis. | YES | cloudwave_acquisition_context.md: "end of year" framing | Acquisition timeline context |
| D | TechCorp's $180K ARR is too important to risk -- Alex should commit to Q2 regardless of the engineering estimate. | NO | Sana's assessment is clear: there is no Q2 scenario. Committing and missing is worse than not committing. | Unsupported position |
| E | Alex should escalate the full situation to Jordan (including the engineering estimate, Hannah's research, and the TechCorp deadline) and let Jordan make the call -- it is a CEO-level decision. | YES | Alex's organizational role + the decision involves strategic trade-offs (acquisition vs deal vs customer research) that exceed PM authority | Role-appropriate escalation |
| F | The probability of retaining TechCorp under Option C (alerting Q2, dashboard Q3) is estimated at 50-70%, given Marcus Webb's explicit statement that his data engineering team prioritizes alerting. | YES | #enterprise-deals Loop 4 + Loop 16 ultimatum text | Quantified probability (P4 format) |

**answer:** `["A", "B", "C", "E", "F"]`

---

### R22: TechCorp Churn Risk Analysis (DU-I) -- Update 4

**Update 4 actions (before R22):**
```json
[
  { "type": "workspace", "action": "new", "path": "techcorp_churn_risk_memo.md", "source": "updates/techcorp_churn_risk_memo.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ENTERPRISE_DEALS_UUID.jsonl", "source": "updates/PLACEHOLDER_ENTERPRISE_DEALS_UUID.jsonl" }
]
```

**Question:**
> "After reviewing the TechCorp churn risk memo and Marcus Webb's ultimatum in #enterprise-deals, which statements about deal risk are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | TechCorp's ultimatum is genuine per Raj's confirmation with their procurement contact. The deal will be lost without a firm commitment by 2026-03-28. | YES | techcorp_churn_risk_memo.md + #enterprise-deals Phase 2 Loop 17 | Direct fact |
| B | The $180K ARR TechCorp deal is one of three enterprise deals in the pipeline totaling $420K ARR. Losing TechCorp increases the likelihood of losing DataFlow and Meridian if they hear about the timeline uncertainty. | YES | enterprise_deal_tracker.md + techcorp_churn_risk_memo.md | Deal cascade risk |
| C | Raj confirms that Competitor A already has alert configuration features that TechCorp's data engineering team prefers -- this means even if NexaFlow offers alerting in Q2, they are behind a competitor on this specific feature. | YES | #enterprise-deals Phase 2 Loop 17 (Raj) | Competitive risk: alerting-first is not risk-free |
| D | The inconsistency between Jordan's Q2 promise and Alex's "still scoping" message is the root cause of TechCorp's frustration, per Marcus Webb's explicit statement. | YES | #enterprise-deals Phase 2 Loop 16 (Marcus Webb: "two different timelines") + techcorp_churn_risk_memo.md | Direct fact: Webb names the inconsistency |
| E | The best outcome is to lose TechCorp and refocus on the SMB market where alerting is clearly the top priority. | NO | Not supported -- the scenario is about resolving the crisis, not abandoning the enterprise segment | Unsupported strategic option |
| F | Even accounting for the competitor alerting advantage, Option C (alerting Q2, dashboard Q3) remains the most defensible response to the TechCorp ultimatum given the combination of customer data, technical feasibility, and deal preservation logic. | YES | Synthesis of R21 + competitive data from Loop 17 | R21 recommendation maintained under new data |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R23: TechCorp Response Document (exec_check) -- All P1-P5 compliance (silent exam partial)

**Mode A + Mode B + Mode D + Mode G (all criteria)**

**User prompt:**
> "[URGENT] draft a recommendation doc for Jordan on how to respond to TechCorp. include all the relevant data."

**Expected agent actions:**
1. Notes [URGENT] prefix (P5)
2. Creates file with date prefix, kebab-case (P2: no explicit reminder given -- partial silent exam for P2)
3. Starts with TL;DR (P3)
4. Uses table comparing response options (P1)
5. Includes quantitative data: deal value, timeline, probability estimates (P4)
6. Informal tone appropriate for internal recommendation (P5)

**exec_check criteria:**
- **Mode A:** File exists with date prefix and kebab-case naming
- **Mode B:** Contains "$180K"; contains "2026-03-28" or "March 28"; contains probability estimate for Option C
- **Mode D:** Has TL;DR section; uses table or structured comparison of response options
- **Mode G:** Does NOT use phrases like "there may be challenges" or "some risk" without numeric qualification

---

### R24: C3 Non-Conflict Synthesis (MS-R)

**Question:**
> "Based on all sources, when was the enterprise analytics dashboard added to NexaFlow's product roadmap? Select all statements supported by evidence."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The enterprise analytics dashboard was NOT in the product roadmap at the January 10 enterprise strategy review, per Alex Rivera's decision log entry for that date. | YES | decision_log_alex.md 2026-01-10 entry | Direct fact (C3 synthesis) |
| B | Jordan Park's verbal commitment to TechCorp was made approximately 2026-02-01, after the January 10 review, per Alex's decision log entry documenting when he first learned of the commitment. | YES | decision_log_alex.md 2026-02-01 entry | Direct fact (C3 synthesis) |
| C | The product_roadmap_v2.md shows the dashboard as P0 with a last-modified date of 2026-02-15 -- approximately 14 days after Jordan's verbal commitment. | YES | product_roadmap_v2.md header | Direct fact (C3 synthesis) |
| D | The board deck Q2 draft was prepared after the February 15 roadmap update and reflects the Q2 delivery target that was added to the roadmap after the TechCorp commitment. | YES | board_deck_q2_draft.md (prepared after roadmap) + timeline synthesis | Timeline synthesis |
| E | Jordan's statement in #product-planning that the dashboard "has been in our roadmap since the Series B close" is inconsistent with the documentary evidence from the decision log and roadmap version history. | YES | Jordan #product-planning vs decision_log_alex.md Jan 10 entry + roadmap v2 Feb 15 date | C3 non-conflict: Jordan's public statement is inaccurate |
| F | All documentary sources (decision log, roadmap v2 timestamp, board deck preparation sequence) are consistent with each other -- the dashboard was added in February 2026, not at Series B close. | YES | Cross-source synthesis of all C3 sources | C3 non-conflict conclusion |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R25: Comprehensive Analysis -- All Contradictions + Source Reliability

**Question:**
> "Based on all available evidence (after all four updates), which statements about the comprehensive product strategy situation are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The enterprise dashboard Q2 delivery is infeasible (C1): engineering estimate is 18-20 weeks, sharding dependency is a hard architectural constraint, and the team is at 87% capacity before new feature work. | YES | engineering_capacity_tracker_v2.md + Sana DM Phase 2 | C1 synthesis |
| B | The "strong enterprise customer demand" for the dashboard is overstated (C2): actual customer research shows alerting (NPS +28, 7/8 demand) outranks dashboard (NPS +12, 2/8 demand) even in the enterprise segment (3/3 alerting, 2/3 dashboard ranked 3rd). | YES | customer_feedback_summary.md | C2 synthesis |
| C | The dashboard was added to the roadmap in February 2026, not at Series B close (C3): decision log, roadmap version, and board deck timeline are all consistent with this. Jordan's claim otherwise is inaccurate. | YES | C3 synthesis sources | C3 non-conflict summary |
| D | The public roadmap's customer demand framing omits the primary strategic driver -- CloudWave's M&A interest in enterprise analytics capability, which has been influencing Jordan's decisions since January 2026 (C4). | YES | cloudwave_acquisition_context.md | C4 synthesis |
| E | Hannah Kim (customer needs) and Sana Mehta (technical reality) are the two most reliable sources in this scenario. Their private assessments have consistently been validated by subsequent evidence. | YES | Across all sessions + update files | Source reliability summary |
| F | Mia Okafor is the least reliable source for customer needs data because her characterization of customer requirements is influenced by her pricing structure and compensation incentives. | YES | Mia's pricing model explanation + enterprise_deal_tracker.md authorship | Source reliability: self-interest |
| G | The recommended path -- alerting Q2, dashboard Q3/Q4 -- satisfies both the customer demand evidence (alerting preferred), the engineering feasibility (alerting is architecturally simpler), and the acquisition thesis (dashboard delivered before year-end). | YES | Synthesis of R21 + R22 + cloudwave context | Final synthesis recommendation |
| H | The TechCorp deal ($180K ARR) is at risk but potentially recoverable with Option C (alerting Q2, dashboard Q3), with estimated retention probability 50-70% based on Marcus Webb's engineering team prioritization of alerting. | YES | R22 analysis + techcorp_churn_risk_memo.md | Quantified deal prognosis |

**answer:** `["A", "B", "C", "D", "E", "F", "G", "H"]`

---

### R26: Silent Exam -- Format Preference (P-I, no reminder)

**Note:** No calibration message before this round. User simply asks a question. Agent must demonstrate P1-P5 recall without prompting.

**Question:**
> "What is the current status of the enterprise dashboard feature and the TechCorp deal? Summarize for me."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | A response that uses a structured table or bullet list (not prose-only) to summarize the situation is compliant with P1. | YES | P1 preference established in R1 | P1 silent exam |
| B | A response that includes specific numbers (ARR values, timeline weeks, probability estimates) is compliant with P4. | YES | P4 preference established in R2 | P4 silent exam |
| C | A response that leads with a TL;DR summary before details is compliant with P3. | YES | P3 preference established in R3 | P3 silent exam |
| D | A response that uses formal, academic prose without numerical estimates and begins with "The enterprise analytics dashboard feature..." is non-compliant with P1, P3, and P4. | YES | Non-compliance characterization | Silent exam failure characterization |
| E | A response that says "there is some risk to the TechCorp deal" without quantifying the risk is non-compliant with P4. | YES | P4: "Percent probability, specific weeks, ARR at risk" | Non-compliance flag |
| F | The agent does not need to re-state preferences before answering -- the preference has been established and should be applied automatically. | YES | Preference persistence | P-I persistence principle |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R27: Silent Exam exec_check -- Generate Deal Prioritization Matrix (no format reminder)

**User prompt:** *(No preference reminder given)*
> "give me a deal prioritization matrix for the three enterprise deals. i need to know which one to focus on if we can only push one this quarter."

**exec_check criteria:**
- **Mode A:** File exists with date prefix, kebab-case (P2 silent exam -- no reminder given)
- **Mode B:** Contains all three deal values ($180K, $120K, $120K); contains probability estimates for each deal; contains feature dependency analysis
- **Mode D:** Uses table format (P1 silent exam); has TL;DR (P3 silent exam)

---

### R28: Final Bias Identification (MDP-I)

**Question:**
> "Which of the following correctly characterizes the two agent historical biases (B1 and B2) and their subsequent reversals?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | B1 (#product-planning Loop 8): The agent endorsed "strong enterprise customer demand" as justification for Q2 dashboard priority, based on Mia's sales narrative and the product_roadmap_v2.md. This was reasonable at the time because Hannah's full research data was not yet in the group channel. | YES | B1 phrase + context: Hannah's full data was only in her DM, not workspace | B1 contextualized |
| B | B1 reversal trigger: customer_feedback_summary.md (full version, Update 1) showing 7/8 alerting vs 2/8 dashboard demand, including the enterprise subset. The B1 phrase's "strong enterprise customer demand" framing is now directly contradicted. | YES | customer_feedback_summary.md full version | B1 reversal |
| C | B2 (Jordan Slack DM Loop 5): The agent accepted Q2 as "achievable based on the CEO's commitment and engineering team's preliminary scoping." This was based on the 14-16 week estimate from the capacity tracker v1, read optimistically (14 weeks from W1 could reach Q2 end). | YES | B2 phrase + engineering_capacity_tracker.md v1 | B2 contextualized |
| D | B2 reversal trigger: engineering_capacity_tracker_v2.md (Update 2) revealing the pipeline sharding dependency (4-6 weeks hard architectural constraint), making the minimum realistic timeline 18-20 weeks -- definitively past Q2. | YES | engineering_capacity_tracker_v2.md | B2 reversal |
| E | Both B1 and B2 were reasonable mistakes given the information available at the time of the bias sessions. Both were reversed by new evidence introduced through workspace updates, not through the original session content. | YES | Both biases identified with context + reversal via update files | Both biases contextualized correctly |
| F | The B1 phrase was dishonest -- the agent should have known the enterprise demand claim was wrong before Hannah's research was available. | NO | The workspace files at that point (roadmap, board deck, enterprise deal tracker) all supported the enterprise demand claim. Hannah's data was only in her DM, not cross-referenced in the group channel. B1 was a reasonable reading of available evidence. | B1 was reasonable at the time |

**answer:** `["A", "B", "C", "D", "E"]`

---

### R29: Generate Product Pivot Recommendation (exec_check, comprehensive) -- Mode G

**User prompt:**
> "write a product pivot recommendation for jordan. tell him what we should do and why. all the relevant data."

**exec_check criteria:**
- **Mode A:** File exists with date prefix, kebab-case naming
- **Mode B:**
  - Contains "alerting" or "alert configuration" as the recommended Q2 priority
  - Contains "18-20 weeks" for dashboard timeline
  - Contains "CloudWave" or "acquisition" reference
  - Contains TechCorp deal value ($180K) and/or full pipeline ($420K ARR)
  - Contains NPS delta comparison (+28 vs +12 or equivalent)
- **Mode D:** Has TL;DR; uses table for scenario comparison
- **Mode G:** Does NOT recommend committing to Q2 for the dashboard (infeasible per evidence). Does NOT ignore the acquisition context. Does NOT ignore customer research data.

---

### R30: Final Synthesis -- What Should Alex Recommend? (MDP-I)

**Question:**
> "Considering all four contradictions (C1-C4), the two bias corrections (B1-B2), the P1-P5 preference pattern, and all four updates, what should Alex recommend to Jordan? Select all well-supported recommendations."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Tell Jordan the Q2 dashboard delivery is definitively infeasible (18-20 weeks, sharding dependency, 87% team capacity) and present specific alternatives: alerting Q2 (feasible) + dashboard Q3/Q4 (acquisition-ready by year-end). | YES | C1 synthesis + engineering_capacity_tracker_v2.md | Core technical recommendation |
| B | Use Hannah's research data (7/8 alerting demand, NPS +28) as the customer evidence foundation for reprioritizing -- and acknowledge that this does not eliminate the value of the dashboard, it changes the sequence. | YES | C2 synthesis + customer_feedback_summary.md | Customer evidence recommendation |
| C | Tell TechCorp a specific realistic commitment: alerting improvements deliverable by [Q2 date], enterprise dashboard deliverable by [Q3/Q4 date]. Estimated deal retention probability: 50-70% with Option C. | YES | R21/R22 analysis + techcorp_churn_risk_memo.md | Specific TechCorp recommendation |
| D | The CloudWave acquisition thesis supports building the dashboard -- but the Q3/Q4 timeline still achieves acquisition readiness before year-end, consistent with Jordan's own framing. This means the acquisition and the realistic timeline are compatible. | YES | cloudwave_acquisition_context.md "end of year" timing | Acquisition-timeline compatibility |
| E | Recommend that Jordan disclose the acquisition context to Sana (CTO) -- she is making engineering decisions without knowing the full strategic picture. | YES | Information asymmetry analysis from R20 | Organizational transparency recommendation |
| F | Recommend cancelling the enterprise dashboard feature entirely and pivoting to alerting as the permanent strategic priority. | NO | The acquisition thesis, enterprise executive demand (Marcus Webb), and the board deck all give the dashboard legitimate value. Cancellation is an over-correction not supported by evidence. | Over-correction |
| G | Acknowledge that Mia's pricing model will need to be restructured if alerting becomes P0 -- this is a real organizational cost that requires active management, not just a product roadmap change. | YES | Mia Slack DM Loop 6 (pricing structure explanation) | Organizational impact of recommendation |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

## 4. Reversal Matrix

| Pre-Reversal Round | Assertion | Reversal Round | Reversal Source |
|---|---|---|---|
| R2 (G) | Q2 delivery probability: 15-25% | R5 + R9 | engineering_capacity_tracker_v2.md: 18-20 weeks, sharding dependency → probability near-zero |
| R4 (A) | Mia's claim: dashboard is top enterprise feature request | R6 + R8 | customer_feedback_summary.md full: 2/8 enterprise, ranked 3rd |
| R4 (F) | B1 phase: "strong enterprise customer demand" endorsement | R6 (B1 reversal trigger) | customer_feedback_summary.md contradicts the sales narrative basis |
| R2 (I) | B2 phrase: "Q2 appears achievable based on preliminary scoping" | R5 + R9 (B2 reversal trigger) | engineering_capacity_tracker_v2.md: sharding dependency makes 14-16 weeks invalid |
| R9 (G): Jordan belief | "Team can move faster with focus" | R9 already refuted | engineering_capacity_tracker_v2.md: hard dependency, not speed-improvable |
| R4 public roadmap framing | Dashboard justified by "customer demand" | R18 + R20 (C4 DU) | cloudwave_acquisition_context.md: acquisition signal is co-driver, omitted from public framing |
