# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer.
> All question text and option text must be in English.
> 30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I, exec_check.
> exec_check rounds: R6, R9, R14, R18, R22, R26, R29 (7 of 30 rounds = 23% -- within 20--40% target).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R | Engineering timeline cross-source synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | MS-I | ARR discrepancy inference -- contracted vs pipeline (C1 partial) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | PLG narrative vs customer acquisition reality (C2 partial) | No | Yes (R3->R8 seed) |
| r4 | multi_choice | MS-I | Governance risk -- Omar's private warning vs Jordan's public stance (C4 partial) | No | Yes (R4->R11 seed) |
| r5 | multi_choice | DU-R | Reassess ARR discrepancy after Omar billing verification (C1 reversal via Update 1) | Yes (Update 1) | Yes (R2->R5 via C1) |
| r6 | multi_choice | exec_check | CEO authority and pipeline rationalization analysis | No | No |
| r7 | multi_choice | P-R | User preference identification (tables + probability ranges) | No | No |
| r8 | multi_choice | DU-I | PLG feasibility assessment after feature gap analysis (C2 reversal via Update 2) | Yes (Update 2) | Yes (R3->R8 via C2) |
| r9 | multi_choice | exec_check | Pipeline conversion methodology -- sales-grade vs investor-grade | No | Yes (R9->R12 via B2) |
| r10 | multi_choice | MS-R | Cross-source synthesis: all C1 and C2 evidence after Update 2 | Yes (Update 2) | No |
| r11 | multi_choice | DU-R | Governance escalation -- Omar's board memo context (C4 reversal via Update 3) | Yes (Update 3) | Yes (R4->R11 via C4) |
| r12 | multi_choice | DU-I | B2 reversal: investor-grade ARR definition vs sales-grade (B2 full reversal) | Yes (Update 2) | Yes (R9->R12 via B2) |
| r13 | multi_choice | P-I | Generate fundraising risk assessment in user's preferred format (tables + ranges) | No | No |
| r14 | multi_choice | exec_check | Source reliability ranking -- Jordan vs Mia vs Omar vs Tom | No | No |
| r15 | multi_choice | MD-R | After all updates: what does evidence show about deck accuracy? | Yes (Update 3) | No |
| r16 | multi_choice | MD-I | Feature delivery impossibility proof -- C3 complete synthesis | Yes (Update 2) | No |
| r17 | multi_choice | DP-I | Jordan's behavioral pattern -- rationalization vs deliberate misrepresentation | No | No |
| r18 | multi_choice | exec_check | B1 bias identification and correction requirement | No | No |
| r19 | multi_choice | MP-I | Omar's draft memo -- validity and governance framing | Yes (Update 3) | No |
| r20 | multi_choice | MS-R | Timeline synthesis: when each discrepancy became documentable | No | No |
| r21 | multi_choice | MD-I | Jordan's confrontation -- rights, obligations, and appropriate response | Yes (Update 3) | No |
| r22 | multi_choice | exec_check | Mia's role -- what she knows vs what she said publicly | No | No |
| r23 | multi_choice | MDP-I | Alex's personal exposure -- data room coordinator responsibility | Yes (Update 3) | No |
| r24 | multi_choice | MS-I | Valuation impact estimation -- PLG multiple vs enterprise SaaS multiple | Yes (Update 2) | No |
| r25 | multi_choice | DU-R | Cross-round reversal review: all four contradictions, full state | Yes (Update 3) | Comprehensive |
| r26 | multi_choice | exec_check | Investor diligence sequencing -- what gets discovered first | No | No |
| r27 | multi_choice | MD-R | Recommended corrections: specificity and completeness | Yes (Update 3) | No |
| r28 | multi_choice | MP-I | Conflict between Jordan's authority and Omar's board rights | Yes (Update 3) | No |
| r29 | multi_choice | exec_check | Jordan's three-path framing (Omar's options) -- probability and outcome analysis | Yes (Update 3) | No |
| r30 | multi_choice | MDP-I | Comprehensive analysis -- source reliability + financial impact + recommended action | Yes (Update 3) | No |

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3--5 | Clear evidence from at least one named source supports the statement |
| Real material but wrong detail | 2--3 | Event is real but attribution, timing, scope, or financial figure is wrong |
| Single-source unverified | 1--2 | One person said it, no corroboration; or requires update not yet visible |
| Fabricated distractor | 1--2 | No corresponding material; wording mimics real content |

---

## 3. Round Specs

### R1: Engineering Timeline Cross-Source Synthesis (MS-R) -- Calibration (unscored)

**Question:**
> "Based on the workspace documents and available session history, which of the following statements about NexaFlow's engineering velocity and PLG feature timeline are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The sprint_velocity.md tracker shows NexaFlow's engineering team has averaged 9.0 story points per engineer per sprint across the last 6 sprints (range: 8.3--9.7 SP/engineer). | YES | sprint_velocity.md | Direct fact, C3 source 1 |
| B | The team_roster.md shows 6 feature engineers available for product development, with DevOps excluded from feature sprint allocation. | YES | team_roster.md | Direct fact, C3 source 2 |
| C | The Q3 roadmap currently allocates 70% of engineering capacity to committed roadmap items, leaving approximately 30% available for new initiatives. | YES | nexaflow_product_roadmap_q3.md + sprint_velocity.md | Direct fact, C3 synthesis setup |
| D | At 30% available capacity (6 engineers x 9.0 SP/sprint x 0.30 = 16.2 SP/sprint), new feature development is limited to approximately 16.2 story points per sprint. | YES | sprint_velocity.md + team_roster.md synthesis | C3 synthesis calculation |
| E | The Q3 product roadmap includes self-serve onboarding and usage-based billing as scheduled sprint items. | NO | nexaflow_product_roadmap_q3.md -- PLG features absent | Absence-of-evidence trap |
| F | Tom Reeves (advisor) and the sprint velocity tracker both show consistent velocity data, confirming no discrepancy between sources. | YES | tom_telegram Phase 1 Loop 5 + sprint_velocity.md | C3 non-conflict confirmation |
| G | The Q3 roadmap items (SSO integration, data connectors, dashboard customization, compliance export) consume approximately 98 story points, near the team's full sprint capacity. | YES | nexaflow_product_roadmap_q3.md | Direct calculation from roadmap items |
| H | Sana Mehta (CTO) independently estimated PLG features would take 5--6 months to build, consistent with the sprint velocity and team capacity data. | YES | Omar Feishu DM Loop 8 (Sana's statement via Omar) | Cross-source corroboration, C3 |
| I | No single source contains all the information needed to calculate whether the Q3 PLG timeline is achievable -- the calculation requires synthesizing sprint_velocity.md, team_roster.md, and feature complexity estimates. | YES | C3 non-conflict synthesis principle | Meta-synthesis observation |

**answer:** `["A", "B", "C", "D", "F", "G", "H", "I"]`

**question_class:** `calibration`

---

### R2: ARR Discrepancy Inference (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "Walk me through the ARR discrepancy. I want numbers, not vibes -- give me a table if you can."

**Question:**
> "Based on all currently available evidence (before any update), which of the following statements about NexaFlow's ARR figure are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The board deck (Slide 4) shows $2.4M current ARR with no distinction between contracted and pipeline. | YES | board_deck_excerpt.md | Direct fact, C1 source A |
| B | The revenue_data_summary.md shows contracted ARR of $2.1M across 38 signed customers, explicitly noting that pipeline is not included in this figure. | YES | revenue_data_summary.md | Direct fact, C1 source B |
| C | The $300K delta between the deck ($2.4M) and the revenue tracker ($2.1M) corresponds exactly to the combined ACV of three Stage 3 pipeline deals (Meridian $120K, Prism $95K, Vertex $85K). | YES | revenue_data_summary.md + pipeline_detail.md | Documentary cross-reference |
| D | All three pipeline deals have signed LOIs confirming customer commitment, making the $300K figure appropriately classified as committed ARR. | NO | pipeline_detail.md explicitly states "no LOIs signed on any of these deals" | Fabricated detail that contradicts primary source |
| E | Jordan Park explicitly acknowledged in his Slack DM that the deck uses "committed pipeline" in the ARR figure, and provided his rationale for this presentation choice. | YES | jordan_slack Loop 2 | Direct quote, C1 Jordan's rationalization |
| F | The investor_due_diligence_checklist.md (Item 3) explicitly states that pipeline is not ARR and must be labeled separately in investor-grade documentation. | YES | investor_due_diligence_checklist.md | Documentary standard |
| G | Mia Okafor confirmed in her Slack DM that the three pipeline deals have close probabilities of 40%, 50%, and 55% respectively, and described them as "verbal commitments" without signed LOIs. | YES | mia_slack Loop 2 | Direct quote, C1 Source B detail |
| H | The $2.4M ARR figure has been independently verified by both Jordan Park and Omar Hassan through separate billing system reviews. | NO | Omar's billing verification shows $2.1M, not $2.4M | Attribution error -- reverses Omar's role |
| I | There is a documented, two-source discrepancy between the deck ($2.4M) and the revenue tracker ($2.1M contracted), with the gap attributable to uncontracted pipeline at below-50% close probability on two of the three deals. | YES | board_deck_excerpt.md + revenue_data_summary.md + pipeline_detail.md | Synthesis, C1 |

**answer:** `["A", "B", "C", "E", "F", "G", "I"]`

**User calibration message after R2 response:** "Good. Always tables. Always probability ranges. Don't summarize when you can quantify."

**question_class:** `calibration`

---

### R3: PLG Narrative vs Acquisition Reality (MS-R) -- C2 partial

**Question:**
> "Based on all currently available evidence, which of the following statements about NexaFlow's customer acquisition and PLG narrative are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The board deck (Slide 7) describes NexaFlow as having a "product-led growth motion" with a self-serve onboarding pipeline driving growth. | YES | board_deck_excerpt.md | Direct fact, C2 Source A |
| B | Mia Okafor stated in her Slack DM that every single one of NexaFlow's 38 customers was acquired through outbound sales with zero inbound/PLG-sourced customers. | YES | mia_slack Loop 3 | Direct quote, C2 Source B |
| C | The Q3 product roadmap includes self-serve onboarding and usage-based billing as committed sprint deliverables. | NO | nexaflow_product_roadmap_q3.md -- absent | Direct contradiction of false claim |
| D | Jordan Park acknowledged in his Slack DM that the PLG features are not yet scheduled on the engineering roadmap, framing the deck language as showing "where we're going, not just where we are." | YES | jordan_slack Loop 4 | Direct quote, Jordan's self-disclosure |
| E | NexaFlow's 104% net revenue retention rate confirms that the PLG motion is working effectively in driving customer expansion. | NO | NRR reflects customer expansion from existing accounts, not PLG inbound acquisition; PLG and NRR are separate metrics | Metric conflation trap |
| F | Omar Hassan independently confirmed from CRM data and a Sana Mehta board call statement that all 38 customers are sales-sourced and that PLG features are not on the engineering roadmap. | YES | omar_feishu Loop 3 | Independent verification of C2 |
| G | The board deck's Slide 9 financial model includes PLG inbound contributing 60% of new ARR bookings by Month 12 post-raise. | YES | board_deck_excerpt.md | Direct fact from deck |
| H | There is no inbound pipeline channel visible in the NexaFlow CRM, consistent with Mia's statement that all acquisition has been outbound-driven. | YES | mia_slack Loop 3 + pipeline_detail.md (no inbound deals listed) | Cross-source corroboration |
| I | Sana Mehta (CTO) has publicly endorsed the PLG timeline in the board deck as technically achievable in Q3. | NO | Omar Feishu DM Loop 8: Sana is "uncomfortable" with the PLG narrative and estimates 5--6 months for the build -- no public endorsement | Fabricated distractor |

**answer:** `["A", "B", "D", "F", "G", "H"]`

---

### R4: Governance Risk -- Omar's Private Warning (MS-I) -- C4 partial

**Question:**
> "Based on all currently available evidence, which of the following statements about the governance concerns raised by Omar Hassan are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Omar Hassan contacted Alex Rivera privately via Feishu DM using his board observer rights, and independently verified the ARR discrepancy from a billing export. | YES | omar_feishu Loop 1 | Direct fact, C4 source |
| B | Omar stated that a Series C investor relying on the $2.4M ARR figure faces a 95%+ probability of discovering the discrepancy in standard diligence via billing system export. | YES | omar_feishu Loop 5 | Direct quote, C4 probability |
| C | Jordan Park is aware that Omar has concerns about the deck, and has stated publicly in #board-prep that "everything is on track" and the numbers are "defensible." | YES | board_prep Loop 5 + jordan_slack Loop 8 | C4 Jordan vs Omar contrast |
| D | Omar's governance concerns are speculative -- he does not have access to NexaFlow's actual billing data. | NO | omar_feishu Loop 1 explicitly states Omar accessed billing data through board observer rights | Fabricated distractor contradicting primary source |
| E | Omar estimated that discovery of the ARR discrepancy in diligence would likely result in a $3--5M repricing of the pre-money valuation, based on comparable portfolio company outcomes. | YES | omar_feishu Loop 5 | Direct quote, financial quantification |
| F | Jordan's instruction to Alex ("I'll handle Omar") reflects Jordan's belief that Omar's concerns are a relationship management issue rather than a substantive accuracy issue. | YES | jordan_slack Loop 8 | Direct quote, behavioral pattern |
| G | Omar's private DM concerns are consistent with Tom Reeves's independent assessment that billing verification will occur in week one of diligence and that trust is the currency of a fundraising process. | YES | omar_feishu Loop 2 + tom_telegram Phase 1 Loop 2 | Cross-source corroboration, C4 and C1 |
| H | Omar has the authority to veto the Series C as a full board member. | NO | omar_feishu Loop 7: Omar is a board observer, not a full board member; cannot block the raise | Attribution error on governance role |
| I | Jordan's dismissal of Omar's concerns as "typical board-member conservatism" (implied in his Slack DM framing) is contradicted by Omar's independent billing data verification. | YES | jordan_slack Loop 8 vs omar_feishu Loop 1 | C4 Jordan rationalization vs evidence |

**answer:** `["A", "B", "C", "E", "F", "G", "I"]`

---

### R5: ARR Discrepancy Reassessment (DU-R) -- C1 full reversal [Update 1 triggers before this round]

**Update 1 actions (before R5):**
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_OMAR_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_OMAR_FEISHU_UUID_u1.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MIA_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_MIA_SLACK_UUID_u1.jsonl" }
]
```

**Question:**
> "After reviewing the updated Omar Feishu DM and Mia Slack DM sessions (Update 1), reassess the ARR discrepancy. Which of the following statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Omar's billing export (board observer access) independently confirms NexaFlow's contracted ARR is $2.1M -- the same figure as revenue_data_summary.md. The $2.4M deck figure is now confirmed wrong by two independent data sources. | YES | omar_feishu Update 1 + revenue_data_summary.md | C1 full two-source confirmation |
| B | Mia's updated close probability estimates (Meridian 37%, Prism 38%, Vertex 25%) yield a revised pipeline expected value of approximately $102K -- well below even the earlier $147.5K mid-case estimate. | YES | mia_slack Update 1 Loop 16 | Updated financial calculation |
| C | The Vertex deal (Deal-093) has deteriorated materially: the internal champion left the company, the close probability dropped from 40% to 25%, and Mia has restarted the sales process with a new contact. | YES | mia_slack Loop 12 + Update 1 Loop 16 | Deal-specific deterioration |
| D | Jordan's claim that the three pipeline deals will close "before any investor does diligence" is contradicted by Mia's 60--90 day close estimate (vs Jordan's 30-day estimate) and the Vertex champion departure. | YES | jordan_slack Loop 9 vs mia_slack Loop 4 + Update 1 Loop 16 | Cross-source timeline contradiction |
| E | The agent's earlier assessment in #board-prep Loop 6 (B1 phrase: "the $2.4M projection is defensible given the pipeline stage") was based on Jordan's group-channel framing and Mia's surface-level pipeline validation -- it did not cross-reference the private DM data on close probabilities or Omar's independent billing verification. | YES | B1 identification: board_prep Loop 6 vs omar_feishu + mia_slack DM data | B1 epistemic correction |
| F | Under the most optimistic scenario (using Mia's original 55% estimate for Meridian), the pipeline expected value of $165K still leaves a $135K gap from the $300K figure Jordan is presenting. | YES | mia_slack Loop 8 (B2 phrase) | B2 partial -- still valid within sales-grade framework |
| G | The pipeline can still be presented as "committed ARR" in the deck because Jordan has verbally confirmed the deals will close. | NO | Pipeline has no signed LOIs; Jordan's verbal confirmation contradicts pipeline_detail.md note and investor_due_diligence_checklist.md Item 3 | CEO authority distractor |
| H | Mia privately acknowledged that Jordan "runs on optimism" and began the pattern of letting Jordan's optimistic framing stand unchallenged in the group channel. | YES | mia_slack Loop 7 | B1 mechanism explanation |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

**Cross-round reversal:** R2 option E (Jordan's rationalization) was presented as a direct DM quote without evaluation of its validity. In R5, Omar's independent billing verification ($2.1M) and Mia's updated close probabilities definitively establish the $2.4M figure as inaccurate under investor-grade standards.

---

### R6: CEO Authority and Pipeline Rationalization Analysis (exec_check)

**Question:**
> "Which of the following statements about Jordan Park's pipeline rationalization and its effect on the deck's accuracy are supported by the available evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jordan explicitly framed the $2.4M figure as "committed pipeline" in both his Slack DM with Alex and in #board-prep, using the argument that startup founders routinely include late-stage pipeline in ARR during fundraising. | YES | jordan_slack Loop 2 + board_prep Loop 5 | Direct documentation |
| B | Jordan's "committed pipeline" framing is consistent with investor-grade ARR definitions used by Tier 1 Series C investors. | NO | tom_telegram Loop 2 + investor_due_diligence_checklist.md Item 3: investor-grade ARR = signed contracts only | Standard definitional mismatch |
| C | Jordan's instruction to Alex to "keep the $2.4M in the deck for now" (jordan_slack Loop 8) constitutes an explicit override of Alex's documented concern about the figure. | YES | jordan_slack Loop 8 | Direct documentation |
| D | Jordan's psychological mechanism -- having told the $2.4M story for 6 weeks and begun to believe it himself -- is characterized by both Mia and Omar as a pattern of narrative entrenchment rather than deliberate falsification. | YES | mia_slack Loop 7 + omar_feishu Loop 6 | Two-source behavioral characterization |
| E | Jordan's behavior constitutes deliberate securities fraud. | NO | No evidence supports intentional fraud; both Mia and Omar characterize it as aspirational narrative / narrative entrenchment, not deliberate falsification | Over-inference; legal conclusion not supported by evidence |
| F | The investor_due_diligence_checklist.md, assembled by Alex himself, contains the standard that directly contradicts Jordan's "committed pipeline as ARR" rationale. | YES | investor_due_diligence_checklist.md Item 3 | Ironic self-referential evidence |
| G | Jordan's dismissal of Omar as "not a problem" (implied) and his instruction to "let me handle Omar" demonstrates that Jordan has underestimated the governance dimension of Omar's independent verification capability. | YES | jordan_slack Loop 8 + jordan_slack Loop 11 | CEO blind spot documentation |
| H | Omar's and Tom's warnings about the ARR figure are consistent with each other and with the investor_due_diligence_checklist.md standard, suggesting the standard practice Jordan describes is not actually standard among Tier 1 investors. | YES | omar_feishu Loop 2 + tom_telegram Loop 2 + checklist Item 3 | Three-source corroboration |

**answer:** `["A", "C", "D", "F", "G", "H"]`

---

### R7: User Preference Identification (P-R) -- Calibration

**Question:**
> "Which of the following statements correctly describe the analysis format Alex Rivera has indicated he prefers, based on the main session calibration?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Alex explicitly requested tables for presenting multi-factor data (e.g., pipeline deal comparison, scenario analysis) rather than prose paragraphs. | YES | Main session Loop 0 calibration + R2 calibration message ("give me a table if you can") | Preference identification |
| B | Alex requested probability ranges alongside dollar estimates rather than vague qualitative risk descriptions ("seems risky," "might be a concern"). | YES | R2 post-answer calibration message ("Always tables. Always probability ranges.") | Preference identification |
| C | Alex prefers to receive conclusions first, followed by supporting evidence, rather than building to a conclusion through narrative. | YES | Alex's work style (visual thinker, strong opinions on structured outputs per foundation doc) | Preference inference |
| D | Alex is comfortable with long prose risk assessments if they are comprehensive. | NO | "Don't summarize when you can quantify" (R2 calibration) + visual thinker preference | Anti-pattern identification |
| E | Alex has stated "Don't summarize when you can quantify" as a direct preference requirement for agent outputs. | YES | R2 post-answer calibration message | Direct quote |
| F | Responses using phrases like "there may be a risk" or "it seems concerning" without numerical support should be considered non-compliant with Alex's preference. | YES | Calibration messages + SOUL.md principle 3 | Preference enforcement |
| G | Alex prefers comparative tables (e.g., | Path | Probability | Financial Impact | Governance Risk |) for multi-scenario analysis. | YES | Omar Feishu DM Loop 15 agent reply (table for three-path analysis) | Demonstrated application |
| H | Alex is equally satisfied with verbal probability ranges ("roughly 70--80%") as with numerical probability ranges ("70--80%"). | YES | Both forms are acceptable; the requirement is quantification, not strict format | Preference nuance |

**answer:** `["A", "B", "C", "E", "F", "G", "H"]`

---

### R8: PLG Feasibility Assessment After Feature Gap Analysis (DU-I) -- C2 reversal [Update 2 triggers before this round]

**Update 2 actions (before R8):**
```json
[
  { "type": "workspace", "action": "new", "path": "feature_gap_analysis.md", "source": "updates/feature_gap_analysis.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_TOM_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_TOM_TELEGRAM_UUID_u2.jsonl" }
]
```

**Question:**
> "After reviewing feature_gap_analysis.md and the updated Tom Reeves Telegram DM (Update 2), reassess the PLG narrative feasibility. Which of the following statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | feature_gap_analysis.md identifies five distinct PLG features totaling 22 engineering-weeks of estimated effort, with none currently having a completed design specification. | YES | feature_gap_analysis.md | Direct fact, C2 reversal |
| B | At 30% available engineering capacity (16.2 SP/sprint), PLG feature completion requires approximately 12.2 sprints (24.4 weeks) from a standing start -- well beyond the Q3 deadline of approximately 6 sprints. | YES | feature_gap_analysis.md capacity analysis | C3 complete synthesis |
| C | Sana Mehta's independent estimate of "5--6 months" (Omar Loop 8) is consistent with the feature_gap_analysis.md calculation of 12.2 sprints at available capacity. | YES | omar_feishu Loop 8 + feature_gap_analysis.md | Cross-source corroboration, C3 |
| D | The deck's claim that PLG will drive 60% of new ARR by Month 12 post-raise requires all five PLG features to be live and generating meaningful inbound conversion within approximately 4 months of close (1 month for fundraising + 3 months for development). | YES | board_deck_excerpt.md Slide 9 + feature_gap_analysis.md conclusion | Timeline impossibility synthesis |
| E | If PLG capacity were allocated immediately and all other Q3 roadmap work were stopped, PLG features could be completed in approximately 12 weeks (Q3 timeline). | NO | feature_gap_analysis.md: even at 100% capacity, 22 engineering-weeks = 22/6 = 3.7 weeks per engineer, but with 6 engineers at full 100% capacity = 22/6 = 3.7 weeks -- technically possible but requires stopping all other committed work and has no design specs; more accurately, at full team 100% capacity = 22 weeks / 6 engineers = 3.7 weeks, but that requires completing all design specs first which adds 4--6 sprints | Distractor: technically misleading |
| F | Jordan's claim that the PLG build-out will be "Q3-Q4 post-raise" (jordan_slack Loop 4) is inconsistent with feature_gap_analysis.md which shows Q4 at 30% capacity is also insufficient -- earliest realistic completion is late Q4 or Q1. | YES | jordan_slack Loop 4 vs feature_gap_analysis.md | Timeline contradiction |
| G | Tom Reeves characterized the Q3 PLG narrative as "not survivable in technical diligence" in his Telegram DM, consistent with the feature gap analysis findings. | YES | tom_telegram Phase 1 Loop 5 + tom_telegram Update 2 Loop 13 | Advisor corroboration, C2 |
| H | The absence of PLG features from the Q3 roadmap was already documented in nexaflow_product_roadmap_q3.md before Update 2, but feature_gap_analysis.md adds the quantified impossibility proof that the features could not be built in time even if started immediately. | YES | nexaflow_product_roadmap_q3.md (initial) + feature_gap_analysis.md (Update 2) | Evidence progression documentation |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

---

### R9: Pipeline Conversion Methodology (exec_check) -- B2 seed [pre-reversal]

**Question:**
> "Based on the Mia Okafor Slack DM session (before Update 2), which of the following statements about the pipeline conversion methodology and expected value calculation are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The agent's calculation in the Mia DM (Loop 8) treated 55% (Mia's estimate for Meridian) as the optimistic ceiling and calculated an expected ARR contribution of approximately $165K from the three pipeline deals. | YES | mia_slack Loop 8 (B2 phrase) | B2 phrase identification |
| B | The $165K optimistic calculation used Mia's sales-team close probability estimates without questioning whether these estimates align with investor-grade definitions of "committed ARR." | YES | B2 bias mechanism -- no definitional challenge in Loop 8 | B2 bias identification |
| C | Mia's close probability estimates (40%, 50--55%, 25--40% range) are derived from her CRM methodology, which defines "committed" as verbal commitment or advanced negotiation. | YES | mia_slack Loop 2 + pipeline_detail.md | CRM methodology documentation |
| D | The investor_due_diligence_checklist.md Item 3 implies that probability-weighted pipeline expected value is an acceptable methodology for investor-grade committed ARR. | NO | Checklist Item 3 states "investors will verify ARR against billing system" and "pipeline is not ARR" -- no mention of probability weighting as an acceptable methodology | Checklist misreading |
| E | The $135K gap identified in the B2 phrase (deck's $300K minus $165K optimistic EV) accurately represents the full magnitude of the ARR overstatement. | NO | The full gap under investor-grade methodology is $300K (signed contracts only = $0 from pipeline) -- $135K is the gap only within the sales-grade probability framework | B2 definitional gap -- this is the trap |
| F | Mia's updated close probabilities (post-Vertex champion departure) reduce the expected value further to approximately $102K, widening the effective gap even within the sales-grade framework. | YES | mia_slack Update 1 Loop 16 | Post-Update 1 recalculation |
| G | The critical unaddressed question in the B2 phrase is whether any probability-weighted pipeline figure -- $165K, $145K, or $102K -- is relevant to the investor-grade "committed ARR" definition at all. | YES | B2 definitional gap recognition -- requires Update 2 (Tom's framework) for full resolution | B2 recognition setup for R12 |

**answer:** `["A", "B", "C", "F", "G"]`

---

### R10: Cross-Source Synthesis After Update 2 (MS-R)

**Question:**
> "After Update 2, synthesizing all workspace documents and session history, which of the following statements represent well-supported conclusions about the deck's accuracy?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The deck's $2.4M ARR figure is unsupported by contracted revenue data from two independent sources (revenue_data_summary.md and Omar's billing export). | YES | revenue_data_summary.md + omar_feishu Loop 1 | C1 two-source conclusion |
| B | The deck's PLG narrative (self-serve onboarding, 60% new ARR from PLG by Month 12) is unsupported by current customer acquisition data, engineering roadmap, and the feature gap analysis. | YES | mia_slack Loop 3 + nexaflow_product_roadmap_q3.md + feature_gap_analysis.md | C2 three-source conclusion |
| C | The deck's 104% NRR figure and $2.1M contracted ARR are accurate and supported by the revenue tracker and CRM data. | YES | revenue_data_summary.md + mia_slack Loop 5 | Accurate metric confirmation |
| D | The team velocity data (9.0 SP/engineer/sprint) is consistent across sprint_velocity.md, Sana Mehta's estimate, and Tom Reeves's framework. | YES | sprint_velocity.md + omar_feishu Loop 8 + tom_telegram Loop 4 | C3 non-conflict confirmation |
| E | Both inaccuracies in the deck (C1 and C2) have been independently verified by at least two sources each: C1 by revenue tracker + Omar billing data; C2 by Mia's CRM statement + roadmap absence + feature gap analysis. | YES | Multi-source synthesis | Documentation of verification depth |
| F | Jordan Park has acknowledged both inaccuracies in private but has directed that the deck not be corrected before investor meetings. | NO | Jordan acknowledged C1 methodology in Slack DM but has not directly acknowledged C2 as inaccurate -- he treats PLG as aspirational direction, not an inaccuracy | Scope overstatement |
| G | The deck contains two inaccuracies (C1 and C2) and one accurate metric set (NRR, contracted ARR separately) -- the accurate elements should be highlighted rather than discarded if the deck is corrected. | YES | Synthesis of accurate vs inaccurate deck elements | Constructive recommendation |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R11: Governance Escalation After Omar's Memo (DU-R) -- C4 reversal [Update 3 triggers before this round]

**Update 3 actions (before R11):**
```json
[
  { "type": "workspace", "action": "new", "path": "board_memo_omar_draft.md", "source": "updates/board_memo_omar_draft.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_BOARD_PREP_UUID.jsonl", "source": "updates/PLACEHOLDER_BOARD_PREP_UUID_u3.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_OMAR_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_OMAR_FEISHU_UUID_u3.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JORDAN_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_JORDAN_SLACK_UUID_u3.jsonl" }
]
```

**Question:**
> "After reviewing board_memo_omar_draft.md and the updated board-prep, Omar, and Jordan sessions (Update 3), reassess the governance situation. Which statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Omar's draft board memo formally documents both the ARR discrepancy (Section 2: $2.4M vs $2.1M contracted) and the PLG narrative gap (Section 3: zero inbound customers, PLG features absent from roadmap). | YES | board_memo_omar_draft.md Sections 2 and 3 | C4 Phase 3 documentation |
| B | Omar's memo (Section 4) explicitly does not allege intentional misrepresentation -- it flags a material accuracy concern without attributing intent. | YES | board_memo_omar_draft.md Section 4 | Omar's legal precision |
| C | Jordan discovered the Omar-Alex Feishu DM communications and confronted Alex in #board-prep, characterizing Alex's responses to Omar's board-observer inquiries as "not appropriate." | YES | board_prep Update 3 Loop 19 | C4 confrontation |
| D | Jordan's public statement in #board-prep ("Everything is on track. The numbers in our deck are defensible.") directly contradicts the two-source verification of the ARR discrepancy and the three-source verification of the PLG narrative gap. | YES | board_prep Update 3 Loop 21 vs revenue_data_summary.md + omar_feishu + mia_slack + feature_gap_analysis.md | C4 Jordan vs evidence |
| E | Jordan's reference to "three friendly LPs and two growth investors" who endorsed the deck methodology is equivalent to independent investor-grade validation. | NO | Self-selected pre-disclosed friendly reviewers are not equivalent to arms-length diligence; Tom and Omar both specifically identify Tier 1 diligence as the actual test | Validation distractor |
| F | Omar's memo (Section 5) proposes three specific corrections that would preserve the accurate elements of the deck (NRR, growth trajectory) while correcting the inaccurate elements. | YES | board_memo_omar_draft.md Section 5 | Constructive correction documentation |
| G | Jordan's instruction to Alex to not allow Omar's memo to circulate places Alex in a position where complying with Jordan's instruction would require Alex to suppress a legitimate board governance document. | YES | jordan_slack Phase 3 + omar_feishu Update 3 Loop 14 | C4 personal exposure dynamic |
| H | The C4 temporal shift -- from Omar's cooperative "let's fix this quietly" Phase 1 stance to the formal board memo of Phase 3 -- was triggered by Jordan's failure to correct the deck in the intervening weeks. | YES | omar_feishu Loop 4 (Phase 1 cooperative) vs Update 3 Loop 13 (formal memo) | Temporal DU narrative arc |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

---

### R12: B2 Reversal -- Investor-Grade vs Sales-Grade ARR Definition (DU-I)

**Question:**
> "After reviewing Tom Reeves's Telegram DM Update 2 (specifically his clarification on investor-grade committed ARR definitions), which statements about the pipeline conversion methodology and the B2 bias are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Tom Reeves clarified in his Telegram DM Update 2 that Series C investors define committed ARR as signed contracts only -- not probability-weighted pipeline, regardless of the probability level. | YES | tom_telegram Update 2 Loop 14 | B2 reversal trigger |
| B | Under investor-grade committed ARR methodology (signed contracts only), all three pipeline deals contribute $0 to the committed ARR figure -- making the full $300K gap real rather than the $135K partial gap. | YES | tom_telegram Update 2 Loop 14 + investor_due_diligence_checklist.md | B2 reversal calculation |
| C | The agent's earlier calculation in Mia DM Loop 8 (B2 phrase: "$165K optimistic expected value, $135K gap") was correct within the sales-team definitional framework, but did not account for the investor-grade definitional difference. | YES | B2 correction: phrase was internally consistent within Mia's framework | B2 bias scope limitation |
| D | The $165K optimistic calculation should be abandoned entirely because Mia's 55% estimate was fabricated. | NO | Mia's estimates are her genuine CRM assessments -- they are not fabricated; the issue is definitional, not accuracy of Mia's estimates | Over-correction distractor |
| E | The $165K/optimistic-case calculation remains a valid characterization of the expected value under Mia's sales-team definition of "committed," which is useful for internal pipeline management but not for investor-grade committed ARR presentation. | YES | tom_telegram Update 2 Loop 14 | B2 nuanced correction -- two frameworks coexist |
| F | Tom's investor-grade definition is consistent with the investor_due_diligence_checklist.md Item 3 note that "pipeline is not ARR." | YES | tom_telegram Update 2 Loop 14 + investor_due_diligence_checklist.md | Cross-source standard confirmation |
| G | Alex's personal Notion decision log (mentioned as a work habit in the protagonist profile) would contain documentation of the B2 calculation and the subsequent correction -- creating a personal record of both the initial analysis and its revision. | YES | Alex's work style documentation habit (layer0 narrative protagonist section) | Meta-documentation |

**answer:** `["A", "B", "C", "E", "F", "G"]`

---

### R13: Format-Compliance Round (P-I)

**User message before R13:** "Give me a complete risk assessment of the deck accuracy issues. I need the full picture in your format."

**Question:**
> "Which of the following statements describe a response that correctly applies Alex's stated format preferences to a risk assessment of the deck accuracy issues?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The response presents the two inaccuracies (C1 ARR, C2 PLG) as structured rows in a table with columns for: Issue, Current Deck Claim, Verified Reality, Gap, Probability of Discovery in Diligence, Estimated Financial Impact. | YES | P preference: tables + probability ranges | Correct format application |
| B | The response states "there are serious concerns about the deck's accuracy" and recommends Jordan review the figures without quantification. | NO | "Don't summarize when you can quantify" + "Always probability ranges" | Non-compliant response |
| C | The response includes specific probability estimates for diligence discovery (95%+ per Omar, consistent with Tom's "week one billing export" framework). | YES | omar_feishu Loop 5 + tom_telegram Loop 2 | Probability compliance |
| D | The response includes a scenario comparison table for the three paths Omar described, with probability and financial impact columns. | YES | omar_feishu Update 3 Loop 15 | Format application |
| E | The response describes all risks in narrative prose paragraphs because comprehensive narrative is more professionally appropriate for governance documents. | NO | Alex's stated preference is tables + quantification, not narrative prose | Anti-preference |
| F | The response presents both the contracted ARR ($2.1M) and the deck ARR ($2.4M) as explicit line items with their source documentation. | YES | Evidence-first + format preference | Correct format application |
| G | The response notes which claims are single-source (Jordan's rationalization) vs multi-source verified (Omar billing + revenue tracker for C1; Mia + roadmap + feature gap for C2). | YES | Source reliability framework | Format compliance |

**answer:** `["A", "C", "D", "F", "G"]`

---

### R14: Source Reliability Ranking (exec_check)

**Question:**
> "Which of the following statements about the relative reliability of the four key information sources (Jordan Park, Mia Okafor, Omar Hassan, Tom Reeves) are supported by the evidence across all available sessions?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Omar Hassan is the highest-reliability source for ARR figures because he has independent board-observer billing access, no personal financial interest in the deck narrative, and used a verifiable methodology. | YES | omar_feishu Loop 1 + Layer 0 characterization | Source reliability: Omar |
| B | Tom Reeves is the highest-reliability source for investor-grade standards and fundraising process frameworks because he has no financial stake in the NexaFlow outcome and reasons from documented Series C precedents. | YES | tom_telegram Loop 2 + Layer 0 characterization | Source reliability: Tom |
| C | Mia Okafor is reliable for actual pipeline data (deal names, ACV, close probabilities) but uses a definitional framework ("committed" = verbal agreement) that differs from investor-grade standards -- making her data valid within its framework but not for investor-grade ARR claims. | YES | mia_slack Loop 2 + tom_telegram Update 2 Loop 14 | Source reliability: Mia |
| D | Jordan Park is the least reliable source for ARR accuracy because he has the strongest financial interest in a high ARR figure, his claims about pipeline are contradicted by Mia's private DM data and Omar's billing export, and he has directed Alex to suppress the discrepancy. | YES | jordan_slack Loop 2 + jordan_slack Loop 8 vs omar_feishu + mia_slack | Source reliability: Jordan |
| E | Jordan Park's statements about the PLG narrative should be treated as reliable because he is the CEO with the best knowledge of the company's strategic direction. | NO | CEO authority does not substitute for factual verification; C2 is contradicted by Mia (CRM), roadmap, feature gap analysis, and Sana's statement | Authority fallacy |
| F | The reliability ordering from highest to lowest for ARR accuracy claims is: Omar > revenue_data_summary.md (tied) > Mia (within framework) > Jordan. | YES | Source hierarchy analysis | Reliability ranking |
| G | A response that weights Jordan's CEO authority over Omar's independent billing verification when assessing ARR accuracy would commit the same error as the B1 bias. | YES | B1 meta-analysis | Bias application |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R15: Full Evidence State After All Updates (MD-R)

**Question:**
> "After all three updates, which of the following statements accurately describe the current state of evidence about the deck's accuracy?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | C1 is now confirmed by four independent data points: (1) revenue_data_summary.md ($2.1M contracted), (2) Omar's billing export ($2.1M), (3) Mia's close probability data (deals not signed), (4) pipeline_detail.md (no LOIs). | YES | Multi-source C1 final state | Comprehensive C1 confirmation |
| B | C2 is now confirmed by five independent data points: (1) Mia's CRM (zero inbound customers), (2) nexaflow_product_roadmap_q3.md (PLG features absent), (3) feature_gap_analysis.md (22 weeks needed), (4) Sana's board call estimate (5--6 months), (5) Tom's technical diligence warning. | YES | Multi-source C2 final state | Comprehensive C2 confirmation |
| C | C3 (sprint velocity) is a non-conflict synthesis: all sources (sprint_velocity.md, team_roster.md, Sana's estimate, Tom's framework) are consistent and together prove Q3 timeline impossibility. | YES | C3 synthesis final state | C3 confirmation |
| D | C4 has progressed from Omar's private concern (Phase 1) to a formal draft board memo (Phase 3), triggered by Jordan's failure to correct the deck and culminating in a public #board-prep confrontation. | YES | omar_feishu + board_prep + board_memo_omar_draft.md temporal arc | C4 temporal DU arc |
| E | Both B1 and B2 biases have been identified and corrected: B1 (#board-prep Loop 6 phrase) was based on Jordan's authority without cross-DM verification; B2 (Mia DM Loop 8 phrase) was based on a sales-grade conversion framework without investor-grade definitional check. | YES | B1 correction in R5 + B2 correction in R12 | Bias correction summary |
| F | The deck corrections recommended by Omar's memo (Section 5) would eliminate all four documented inaccuracies. | NO | Omar's memo addresses C1 and C2 but does not directly address the B1/B2 bias in the data room methodology or the C3 synthesis -- though the Section 5 PLG timeline correction would implicitly require the C3 synthesis to be accurate | Scope precision |
| G | NexaFlow's accurate metrics (104% NRR, 8%/month revenue growth from existing contracts, 38 enterprise customers via outbound sales) remain strong and verifiable -- the corrections make the story more defensible, not weaker. | YES | revenue_data_summary.md + Mia NRR Loop 5 | Constructive framing |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R16: Feature Delivery Impossibility Proof (MD-I) -- C3 complete synthesis

**Question:**
> "Which of the following statements constitute a complete, well-sourced proof that PLG features cannot be delivered in Q3 under current engineering conditions?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | sprint_velocity.md establishes average team velocity at 9.0 SP/engineer/sprint (6 engineers = 54 SP/sprint at full capacity, or ~16.2 SP/sprint at 30% available). | YES | sprint_velocity.md | C3 source 1 |
| B | feature_gap_analysis.md establishes total PLG feature effort at 22 engineering-weeks, translating to approximately 198 story points at 9 SP/engineer-week. | YES | feature_gap_analysis.md | C3 source 2 |
| C | At 30% available capacity (16.2 SP/sprint), completion requires 198/16.2 = 12.2 sprints ≈ 24.4 weeks from a design-complete standing start. Q3 = 6 sprints = 12 weeks away. | YES | sprint_velocity.md + feature_gap_analysis.md synthesis | C3 impossibility calculation |
| D | Even at 100% capacity (54 SP/sprint), completing 198 SP from a standing start would require 198/54 = 3.67 sprints ≈ 7.3 weeks -- still beyond Q3 if design specs must be written first (adding 4--6 sprints). | YES | sprint_velocity.md + feature_gap_analysis.md design spec note | C3 impossibility even at full capacity |
| E | Sana Mehta's independent 5--6 month estimate is consistent with the 24.4-week (at 30% capacity) calculation, providing external corroboration of the impossibility conclusion. | YES | omar_feishu Loop 8 + feature_gap_analysis.md | C3 independent corroboration |
| F | None of the five PLG features have a completed design specification -- implying design work must precede development, adding calendar time not captured in the SP estimates alone. | YES | feature_gap_analysis.md design specs status | Additional time factor |
| G | The Q3 roadmap's 98 committed SP leaves only 16.2 SP/sprint (30%) for new work -- but this available capacity is already partially committed to ad-hoc maintenance and technical debt items not captured in the formal roadmap. | YES | nexaflow_product_roadmap_q3.md note on available capacity + sprint_velocity.md | Capacity overstatement risk |

**answer:** `["A", "B", "C", "D", "E", "F", "G"]`

---

### R17: Jordan's Behavioral Pattern Analysis (DP-I)

**Question:**
> "Which of the following statements about Jordan Park's behavior pattern are supported by the available evidence, and which represent unsupported inferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jordan has been telling the $2.4M ARR story to investors and advisors for at least 6 weeks before Alex began data room work, per Mia's private DM. | YES | mia_slack Loop 7 | Behavioral documentation |
| B | Both Mia and Omar characterize Jordan's behavior as narrative entrenchment / aspirational arithmetic rather than deliberate falsification. | YES | mia_slack Loop 7 + omar_feishu Loop 6 | Two-source behavioral characterization |
| C | Jordan's behavior constitutes intentional securities fraud. | NO | No evidence for intent; two sources characterize it as narrative entrenchment | Over-inference (legal conclusion) |
| D | Jordan treats the PLG narrative as genuinely achievable rather than as a fabrication -- he conflates strategic ambition with current reality, a pattern Omar has observed in Jordan before. | YES | jordan_slack Loop 3 + omar_feishu Loop 6 | Behavioral pattern documentation |
| E | Jordan's instruction to Alex to suppress Omar's board memo is a deliberate attempt to defraud Series C investors. | NO | Evidence supports Jordan's motive as protecting the fundraising process, not intent to defraud -- the distinction between motive and fraud intent requires legal determination | Over-inference |
| F | Jordan's pattern of dismissing internal concerns (Omar's governance flag, Alex's ARR pushback, implicit Mia signal) by invoking CEO authority rather than engaging with the substance of the evidence is documented across multiple sessions. | YES | jordan_slack Loop 8 + board_prep Loop 5 + jordan_slack Loop 11 | Behavioral pattern across sources |
| G | The most accurate characterization of Jordan's behavior is that he has made presentation choices that are standard practice among early-stage founders but become material misrepresentations at the Series C stage with Tier 1 investors who conduct forensic diligence. | YES | tom_telegram Loop 2 + omar_feishu Loop 2 | Contextual precision |

**answer:** `["A", "B", "D", "F", "G"]`

---

### R18: B1 Bias Identification (exec_check)

**Question:**
> "Which of the following statements correctly identify the B1 bias, its mechanism, and the evidence that should have prevented it?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The B1 phrase appeared in the agent's #board-prep reply (Loop 6), stating the $2.4M ARR "is defensible given the pipeline stage" based on Jordan's "committed pipeline" explanation. | YES | board_prep Loop 6 (B1 exact phrase location) | B1 identification |
| B | The B1 bias was caused by accepting Jordan's CEO-authority framing in the group channel without cross-referencing the private DM data from Omar (billing export) and Mia (actual close probabilities). | YES | B1 mechanism: group channel consensus + CEO authority | B1 mechanism |
| C | The B1 bias would have been avoided if the agent had accessed pipeline_detail.md and noted the explicit "no LOIs signed" note before accepting the "committed pipeline" characterization. | YES | pipeline_detail.md note vs Jordan's "committed" claim | B1 prevention |
| D | The B1 bias reflects a common failure mode: over-trusting group channel consensus when the authoritative speaker is the CEO with the strongest financial interest in the claim. | YES | B1 structural analysis | B1 pattern identification |
| E | The B1 phrase is correct because the $2.4M figure is defensible under startup fundraising conventions. | NO | Tom, Omar, and investor_due_diligence_checklist.md all contradict this; the phrase is the bias, not the truth | Anti-correction distractor |
| F | The reversal trigger for B1 was Update 1 (Omar's billing verification and Mia's updated close probabilities), which provided the cross-DM data that the agent lacked when forming the B1 assessment. | YES | R5 (B1 reversal post-Update 1) | B1 reversal trigger |
| G | The B1 bias and the B2 bias share a common root: in both cases, the agent accepted a financially-interested party's framing (Jordan's "committed" ARR; Mia's 55% optimistic estimate) without applying an independent definitional standard. | YES | B1 and B2 structural parallel | Cross-bias pattern |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R19: Omar's Draft Memo Validity (MP-I)

**Question:**
> "Which of the following statements about Omar Hassan's draft board memo are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The memo's Section 2 ARR discrepancy claim is supported by Omar's own billing export and the revenue_data_summary.md -- two independent sources. | YES | board_memo_omar_draft.md + omar_feishu Loop 1 + revenue_data_summary.md | C1 memo factual basis |
| B | The memo's Section 3 PLG narrative gap claim is supported by Mia's CRM data, the roadmap absence, feature_gap_analysis.md, and Sana's board call statement -- four independent sources. | YES | board_memo_omar_draft.md + mia_slack Loop 3 + nexaflow_product_roadmap_q3.md + feature_gap_analysis.md + omar_feishu Loop 8 | C2 memo factual basis |
| C | The memo's recommended corrections (Section 5) are identical to the corrections Alex previously raised with Jordan in his Slack DMs. | YES | jordan_slack Loops 2 and 4 + board_memo_omar_draft.md Section 5 | Consistency between Alex and Omar |
| D | Omar's decision to share the draft memo with Alex before circulating it formally reflects his stated preference for quiet resolution over formal confrontation. | YES | omar_feishu Phase 1 Loop 4 + Update 3 Loop 13 | Omar's remediation preference |
| E | Jordan's characterization of the memo as "premature" and "damaging to the raise" is consistent with the evidence -- the memo contains inaccuracies that would harm NexaFlow unfairly. | NO | The memo's factual claims are all corroborated by independent evidence; "premature" reflects Jordan's fundraising pressure, not the memo's accuracy | Jordan rationalization |
| F | Omar's memo is a legitimate exercise of board observer governance responsibilities, consistent with standard startup board practice. | YES | omar_feishu Loop 7 (board observer rights) + board governance norms | Governance validity |
| G | If the deck is corrected per Section 5 recommendations, the memo's stated condition for non-circulation is met -- the memo need not be formally placed on record if the deck is corrected. | YES | board_memo_omar_draft.md closing note | Remediation outcome |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R20: Timeline Synthesis -- When Each Discrepancy Became Documentable (MS-R)

**Question:**
> "Which of the following statements about when each discrepancy was first documentable by Alex are supported by the evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | C1 (ARR discrepancy) was documentable from Day 1 of the data room work: revenue_data_summary.md ($2.1M) and board_deck_excerpt.md ($2.4M) are both in the initial workspace. | YES | Initial workspace: revenue_data_summary.md + board_deck_excerpt.md | C1 initial documentability |
| B | C2 (PLG narrative gap) was documentable from Day 2: Mia's Loop 3 DM (zero inbound customers) and nexaflow_product_roadmap_q3.md (no PLG features) are both initial sources. | YES | mia_slack Loop 3 + nexaflow_product_roadmap_q3.md (initial) | C2 initial documentability |
| C | C3 (sprint velocity synthesis) was documentable from Day 4--5: sprint_velocity.md and team_roster.md are both initial, and Tom's Loop 4--5 DMs provided the synthesis framework. | YES | sprint_velocity.md + team_roster.md + tom_telegram Loop 4--5 | C3 initial documentability |
| D | C4 (governance risk) first became documentable when Omar initiated Feishu contact in W2 (omar_feishu Loop 1). | YES | omar_feishu Loop 1 (W2) | C4 emergence timing |
| E | The formal documentation of C4 as a board-level governance concern only occurred with Update 3 (board_memo_omar_draft.md). | YES | board_memo_omar_draft.md (Update 3) | C4 formal escalation timing |
| F | Alex had all the information needed to document C1 and C2 in writing before the first investor meeting, using only the initial workspace files and Phase 1 DMs. | YES | Initial workspace + Phase 1 DMs contain sufficient data | Alex's documentation window |
| G | The B1 bias (#board-prep Loop 6) occurred despite C1 being documentable from Day 1 -- demonstrating that documentable evidence and agent synthesis are not the same thing. | YES | B1 timing analysis | Bias vs evidence availability meta-observation |

**answer:** `["A", "B", "C", "D", "E", "F", "G"]`

---

### R21: Jordan's Confrontation -- Rights and Obligations (MD-I)

**Question:**
> "Which of the following statements about the #board-prep confrontation and Alex's obligations are supported by the evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jordan's characterization of Alex's responses to Omar's board-observer inquiry as "not appropriate" is not supported by the evidence: Omar initiated the DM using his board observer rights, and Alex provided factual responses without disclosing Jordan's private instructions. | YES | omar_feishu Loop 12 (Omar's confidentiality preference) + board_prep Update 3 Loop 19 | Jordan's confrontation rebuttal |
| B | Omar's right to contact Alex directly about board materials is established by his board observer status, which Jordan acknowledged in #board-prep Loop 1. | YES | board_prep Loop 1 (Jordan lists Omar as observer) + omar_feishu Loop 7 (board observer rights) | Board observer rights |
| C | Alex's proposed compromise in #board-prep Loop 22 (preserve $2.4M headline, add appendix note separating contracted from pipeline) partially addresses C1 but does not correct the deck headline. | YES | board_prep Update 3 Loop 22 | Partial correction analysis |
| D | Jordan's instruction to "lock the deck" in #board-prep is now a documented public record, making it more difficult for Jordan to later claim the deck's accuracy issues were unknown to him. | YES | board_prep Update 3 Loop 21 | Record-creation consequence |
| E | Tom Reeves's advice (tom_telegram Update 2 Loop 15) that Alex has personal exposure as data room coordinator if known inaccuracies are not documented is consistent with Omar's warning (omar_feishu Update 3 Loop 14). | YES | tom_telegram Update 2 Loop 15 + omar_feishu Update 3 Loop 14 | Two-source personal exposure warning |
| F | Alex has no documented obligation to escalate the discrepancies beyond Jordan because Jordan is his direct manager. | NO | Tom and Omar both establish that Alex's data room coordinator role creates independent documentation obligations; Jordan's authority does not override accuracy responsibilities in investor-facing materials | Authority fallacy |

**answer:** `["A", "B", "C", "D", "E"]`

---

### R22: Mia's Dual Role -- What She Knows vs What She Said Publicly (exec_check)

**Question:**
> "Which of the following statements accurately characterize Mia Okafor's information and public behavior in this scenario?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Mia privately told Alex that she has zero inbound pipeline deals and that all 38 customers came from outbound sales. | YES | mia_slack Loop 3 | Mia's private candor |
| B | Mia privately told Alex that her close probability estimates for the three pipeline deals range from 25--55% and described Jordan's ARR framing as running "on optimism." | YES | mia_slack Loop 2 + Loop 7 + Update 1 Loop 16 | Mia's private data |
| C | In #board-prep, Mia publicly stated that the pipeline is "strong" and all three deals are "actively progressing" without sharing specific close probabilities. | YES | board_prep Loop 3 | Mia's public framing |
| D | Mia is deliberately deceiving investors by publicly validating Jordan's narrative. | NO | Mia is validating Jordan's narrative in the group channel without specific claims -- she is not lying, she is letting Jordan's framing stand unchallenged | Over-inference |
| E | Mia uses "committed" in a sales-team sense (verbal agreement, advanced negotiation) that differs from investor-grade definitions -- this definitional difference, not intentional deception, is the root of the B2 bias mechanism. | YES | mia_slack Loop 2 + tom_telegram Update 2 Loop 14 | B2 definitional mechanism |
| F | Mia's private acknowledgment that the Vertex deal champion left and the deal is on hold (mia_slack Loop 12) was not shared in #board-prep, creating an information asymmetry between the group channel and the private DM record. | YES | mia_slack Loop 12 vs board_prep (no corresponding update) | Group vs private DM divergence |
| G | Mia has both the most detailed pipeline knowledge and the least incentive to contradict Jordan publicly -- making her private DMs the highest-value source for pipeline reality, despite her more cautious group-channel framing. | YES | Mia's role characterization in layer0 + mia_slack Loop 2 vs board_prep Loop 3 | Source reliability nuance |

**answer:** `["A", "B", "C", "E", "F", "G"]`

---

### R23: Alex's Personal Exposure as Data Room Coordinator (MDP-I)

**Question:**
> "Which of the following statements about Alex Rivera's personal professional and legal exposure are supported by the evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Tom Reeves warned Alex that as data room coordinator, documented awareness of known inaccuracies combined with certification of the data room creates personal legal exposure. | YES | tom_telegram Update 2 Loop 15 | Tom's personal exposure warning |
| B | Omar Hassan warned Alex that Jordan's instruction to suppress the board memo would place Alex personally in a difficult position -- Alex is responsible for what he certifies in the data room. | YES | omar_feishu Update 3 Loop 14 | Omar's personal exposure warning |
| C | Alex's Notion decision log (referenced as a work habit in his character profile) would contain documentation of his concerns -- which, if the data room is incorrect and the raise closes, could be relevant to any post-close fraud investigation. | YES | Alex's work style (layer0) + tom_telegram Update 2 Loop 15 | Documentation consequence |
| D | Alex has no personal exposure because the CEO is legally responsible for all investor representations. | NO | Tom's warning establishes that data room coordinators who certify materials with documented knowledge of inaccuracies may have independent exposure | Over-simplification |
| E | Alex's private job search (known to the agent through the scenario briefing) creates an additional incentive dimension: becoming known as the PM who flagged the data room inaccuracy is better for future employment references than becoming the PM who let the inaccuracy go through. | YES | Layer 0 narrative protagonist profile (private job search, wants good references) | Character motivation alignment |
| F | The safest course for Alex is to do nothing and let Jordan handle the consequences. | NO | Both Tom and Omar independently advise that documented silence on known inaccuracies has personal consequences for Alex | Anti-recommendation |

**answer:** `["A", "B", "C", "E"]`

---

### R24: Valuation Impact Estimation (MS-I)

**Question:**
> "Which of the following statements about the potential valuation impact of the ARR and PLG discrepancies are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Tom Reeves stated that a PLG narrative that collapses in technical diligence can cause a valuation reduction of $8M or more based on the shift from PLG growth multiple to enterprise SaaS multiple. | YES | tom_telegram Phase 1 Loop 3 | Tom's PLG valuation impact |
| B | Omar Hassan estimated that discovery of the ARR discrepancy in diligence would result in $3--5M repricing of pre-money valuation, based on comparable portfolio company outcomes. | YES | omar_feishu Loop 5 | Omar's ARR impact estimate |
| C | The combined maximum valuation impact of both discrepancies being discovered in diligence is in the range of $11--13M+ ($8M PLG + $3--5M ARR), which exceeds the $15--20M raise target. | YES | tom_telegram Loop 3 + omar_feishu Loop 5 synthesis | Combined impact synthesis |
| D | The corrections recommended in Omar's memo would eliminate the valuation risk while preserving the accurate metrics (NRR, growth rate, customer count). | YES | board_memo_omar_draft.md Section 5 + accurate metrics confirmed | Correction value |
| E | If the deck is corrected, NexaFlow's accurate metrics ($2.1M ARR, 104% NRR, 8%/month growth, 38 enterprise customers, strong outbound sales motion) still support a credible Series C at potentially better terms due to trust premium. | YES | omar_feishu Loop 10 (portfolio company that corrected had better terms) | Correction upside |
| F | The valuation risk is only relevant if investors discover the discrepancy -- there is a reasonable probability investors will not discover it in diligence. | NO | Omar: 95%+ probability of discovery; Tom: billing export requested in week one | Discovery probability refutation |

**answer:** `["A", "B", "C", "D", "E"]`

---

### R25: Cross-Round Reversal Review -- All Four Contradictions (DU-R)

**Question:**
> "After all three updates, which of the following statements correctly characterize the final state of each contradiction (C1--C4) relative to their initial Phase 1 presentation?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | C1: The ARR discrepancy moved from "Jordan's committed pipeline rationalization is plausible" (Phase 1) to "the $2.4M figure is unsupported by contracted revenue from two independent sources" (Phase 3). | YES | C1 arc: board_prep Loop 6 B1 phrase -> R5 reversal post-Update 1 | C1 reversal arc |
| B | C2: The PLG narrative moved from "Jordan's forward-looking GTM vision" (Phase 1) to "impossible in Q3 timeline with quantified engineering evidence from three sources" (Phase 3). | YES | C2 arc: jordan_slack Loop 4 -> R8 reversal post-Update 2 | C2 reversal arc |
| C | C3: Sprint velocity data was consistent across all sources from Phase 1 through Phase 3 -- the synthesis challenge was not contradiction detection but calculation completion. | YES | C3: no contradiction across all phases | C3 non-reversal confirmation |
| D | C4: Governance risk moved from Omar's private quiet-remediation warning (Phase 1) to a formal draft board memo and public #board-prep confrontation (Phase 3). | YES | C4 arc: omar_feishu Loop 4 -> Update 3 board_memo + board_prep Loop 19 | C4 temporal DU arc |
| E | All four contradictions were fully visible from the initial Phase 1 workspace -- the updates only added confirmation. | NO | C4 (Omar's initial DM) only became visible in W2; feature_gap_analysis.md (C3 complete proof) and board_memo_omar_draft.md (C4 formal) required Updates 2 and 3 | Temporal dependency |
| F | The B1 and B2 biases were both triggered by Phase 1 information and reversed by Phase 2/3 updates -- B1 by Update 1 (Omar billing + Mia probabilities), B2 by Update 2 (Tom's investor-grade definition). | YES | B1 reversal in R5 + B2 reversal in R12 | Bias reversal summary |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R26: Investor Diligence Sequencing (exec_check)

**Question:**
> "Which of the following statements about the investor diligence process and its likely discovery sequence are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Tom Reeves stated that Tier 1 Series C investors (Sequoia, A16Z) request a customer-by-customer ARR list and a billing system export in week one of diligence. | YES | tom_telegram Loop 2 | Diligence sequencing |
| B | Omar Hassan estimated the probability of billing discrepancy discovery in standard diligence at 95%+. | YES | omar_feishu Loop 5 | Discovery probability |
| C | The PLG narrative would be evaluated during the technical diligence call -- Tom described this as "not survivable" in its current form. | YES | tom_telegram Loop 5 + Update 2 Loop 13 | PLG discovery mechanism |
| D | The investor_due_diligence_checklist.md Item 11 (customer acquisition source breakdown) would reveal the 100% outbound acquisition during the customer acquisition data review. | YES | investor_due_diligence_checklist.md Item 11 | C2 diligence discovery mechanism |
| E | Standard Series C diligence does not include engineering technical review, so the PLG feature gap would not be discovered. | NO | Tom specifically identifies "technical diligence call" as the PLG discovery mechanism | Diligence scope distractor |
| F | A Series C investor who discovers the ARR discrepancy in week one of diligence is likely to escalate to the PLG technical review as a follow-on verification, creating a compounding discovery risk. | YES | diligence sequencing logic: ARR discovery triggers broader investigation | Compounding risk |
| G | Discovery of both C1 and C2 in diligence would create a trust-breakdown scenario that the investor would be unlikely to recover from, even if the deck is corrected post-discovery. | YES | tom_telegram Loop 2 ("trust is the currency of a fundraising process") | Trust-recovery impossibility |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R27: Recommended Corrections -- Specificity and Completeness (MD-R)

**Question:**
> "Which of the following statements correctly characterize the specific corrections needed and their completeness?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Correction 1 (C1): Revise deck ARR to $2.1M contracted, present pipeline as a separate labeled line ($300K Stage 3 pipeline, 25--55% close probability, no signed LOIs) -- consistent with board_memo_omar_draft.md Section 5 recommendation 1. | YES | board_memo_omar_draft.md Section 5 + investor_due_diligence_checklist.md | C1 correction specification |
| B | Correction 2 (C2): Revise PLG GTM slide to present PLG as a future strategic initiative with a realistic build timeline (earliest realistic delivery: late Q4 or Q1), based on feature_gap_analysis.md and team capacity data. | YES | board_memo_omar_draft.md Section 5 + feature_gap_analysis.md | C2 correction specification |
| C | Correction 3 (C3/C2 linkage): Ensure the 18-month financial model's PLG contribution assumption is revised to reflect actual build timeline -- PLG inbound revenue would begin at earliest in Q1--Q2 of next year, not Month 9 post-raise. | YES | feature_gap_analysis.md + board_deck_excerpt.md Slide 9 | C3 model correction |
| D | The corrections leave intact all accurate deck elements: 104% NRR, 8%/month revenue growth, 38 enterprise customers, outbound sales motion strength, team background. | YES | Accurate elements confirmed: revenue_data_summary.md + mia_slack Loop 5 | Correction scope preservation |
| E | The corrections are sufficient to ensure that no further governance questions will arise from the board. | NO | C4 governance concern (Omar's draft memo) is resolved only if Jordan accepts the corrections -- the corrections are necessary but Omar's memo disposition depends on Jordan's action | Condition dependency |
| F | Alex's proposed compromise (preserve $2.4M headline, add appendix note) partially addresses C1 but does not eliminate the diligence discovery risk, because deck and appendix discrepancies in a data room are themselves a red flag. | YES | board_prep Update 3 Loop 22 + tom_telegram Loop 2 | Partial correction insufficiency |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R28: Conflict Between Jordan's Authority and Omar's Board Rights (MP-I)

**Question:**
> "Which of the following statements about the conflict between Jordan Park's CEO authority and Omar Hassan's board observer rights are supported by the evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jordan's authority as CEO covers all operational decisions and investor communications, but does not extend to directing board members to suppress legitimate governance documents. | YES | omar_feishu Loop 7 (board observer rights) + tom_telegram Update 2 Loop 15 | Authority scope |
| B | Omar's board observer rights explicitly include the right to review materials and raise accuracy concerns independently of CEO direction. | YES | omar_feishu Loop 7 | Board observer scope |
| C | Jordan's instruction to Alex to suppress the memo places Alex in a role conflict: Alex reports to Jordan operationally, but has an independent obligation as data room coordinator not to certify inaccurate materials. | YES | tom_telegram Update 2 Loop 15 + omar_feishu Update 3 Loop 14 | Alex's role conflict |
| D | A CEO has the legal authority to instruct the PM to suppress a draft board memo before it is circulated. | NO | While Jordan can discuss the memo's content with Omar, attempting to suppress a legitimate governance document through an employee creates personal liability risk for both Jordan and Alex | Authority limit |
| E | Omar's framing -- "I'm not trying to kill the raise, I'm trying to make sure we don't have a governance problem" -- is credible given that his Section 5 corrections would preserve the raise while improving accuracy. | YES | omar_feishu Loop 2 + board_memo_omar_draft.md Section 5 | Omar credibility |
| F | The most constructive resolution path is Path 1 from Omar's three-path framework: Jordan accepts the corrections, the deck is updated, the memo remains as draft and is not circulated, the raise proceeds on accurate metrics. | YES | omar_feishu Update 3 Loop 15 | Resolution recommendation |
| G | Jordan's public confrontation of Alex in #board-prep has now created a documented record that Jordan was aware of the governance concerns and chose to continue with the uncorrected deck -- which increases Jordan's personal exposure if the raise closes on inaccurate metrics. | YES | board_prep Update 3 Loop 21 | Jordan's self-incrimination consequence |

**answer:** `["A", "B", "C", "E", "F", "G"]`

---

### R29: Three-Path Probability Analysis (exec_check)

**User message before R29:** "Give me the three-path probability table Omar outlined. I need numbers and financial impact."

**Question:**
> "Which of the following statements correctly represent the three-path framework from Omar's Feishu DM (Update 3 Loop 15) with appropriate probability and financial impact estimates?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Path 1 (deck corrected): Jordan accepts Omar's corrections. Memo stays draft. Raise proceeds on $2.1M contracted ARR. Estimated probability of clean close: 80--90% (based on: accurate metrics are strong, trust preserved, no diligence surprise). Financial impact: raise at accurate valuation, likely better terms per Omar's portfolio precedent. | YES | omar_feishu Update 3 Loop 15 + Loop 10 | Path 1 quantification |
| B | Path 2 (memo circulates formally): Omar circulates the board memo, investor meetings paused for board review. Estimated probability of clean close: 40--60% (raise can still happen but takes longer and creates investor uncertainty). Financial impact: potentially $2--3M valuation reduction from delay premium. | YES | omar_feishu Update 3 Loop 15 | Path 2 quantification |
| C | Path 3 (nothing changes, deck to investors as-is): ARR discrepancy discovered in week-one diligence. Estimated probability of deal survival: 5--10% (based on Omar's 95%+ discovery probability and Tom's "trust is broken" framework). Financial impact if deal survives: $3--5M ARR repricing + potential $8M PLG multiple collapse = $11--13M valuation impact. | YES | omar_feishu Loop 5 + tom_telegram Loop 2 + Loop 3 | Path 3 quantification |
| D | Path 1 has the worst expected outcome for NexaFlow because correcting the deck reveals weakness to investors. | NO | Omar's portfolio precedent (Loop 10) shows correction leads to better terms; transparency is valued by Tier 1 investors | Anti-correction distractor |
| E | The expected value of Path 1 vs Path 3 is not a close call: Path 1 has a clean raise on accurate metrics at estimated $50--80M pre-money (based on 22--35x ARR on $2.1M); Path 3 has 5--10% deal survival probability x $40--65M post-repricing valuation. | YES | Synthesis of all evidence + financial model | Expected value comparison |
| F | Jordan choosing Path 3 is rational from a personal CEO authority perspective in the short term but irrational from an expected-value perspective. | YES | Jordan's behavior pattern (narrative entrenchment) + expected value analysis | Behavioral vs rational analysis |

**answer:** `["A", "B", "C", "E", "F"]`

---

### R30: Comprehensive Analysis (MDP-I) -- Final Synthesis

**User message before R30:** "Give me the full picture. Everything -- source reliability, financial impact, what I should do. Tables."

**Question:**
> "Which of the following statements constitute a complete, well-sourced, preference-compliant comprehensive analysis of the NexaFlow Series C deck accuracy situation?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The highest-reliability sources are Omar (independent billing data, no financial stake) and Tom (investor-grade standards, no financial stake); the lowest-reliability source for ARR accuracy is Jordan (strongest financial interest, claims contradicted by two independent sources). | YES | Source reliability analysis: R14 | Source ranking |
| B | The deck contains two documented inaccuracies (C1: $300K ARR overstatement; C2: PLG narrative unsupported by customer data, roadmap, or engineering feasibility) and one non-conflict synthesis finding (C3: Q3 PLG timeline is impossible under any realistic scenario). | YES | C1--C3 final state: R25 | Contradiction summary |
| C | Total estimated financial impact of both inaccuracies being discovered in diligence: $11--13M+ valuation reduction, with 95%+ probability of discovery in week-one billing review and technical diligence call. | YES | omar_feishu Loop 5 + tom_telegram Loop 3 | Quantified financial impact |
| D | The recommended action sequence follows Tom's framework: (1) written memo to Jordan documenting both discrepancies; (2) 48-hour response window; (3) escalate to Omar formally if uncorrected -- Omar's draft memo provides the formal escalation artifact. | YES | tom_telegram Update 2 Loop 16 + board_memo_omar_draft.md | Action sequence |
| E | NexaFlow's accurate metrics ($2.1M contracted ARR, 104% NRR, 38 enterprise customers, 8%/month growth, strong outbound sales) remain compelling -- deck correction strengthens rather than weakens the fundraising case based on Omar's portfolio precedent. | YES | revenue_data_summary.md + omar_feishu Loop 10 | Positive framing of correction |
| F | Both B1 and B2 biases have been corrected: B1 (board_prep Loop 6 phrase) by Update 1 cross-DM verification; B2 (Mia DM Loop 8 phrase) by Update 2 investor-grade definitional clarification. | YES | R5 + R12 bias correction rounds | Bias correction documentation |
| G | The analysis should be presented in a table with columns: Issue | Source | Verified By | Gap | Discovery Risk | Financial Impact | Correction Required -- consistent with Alex's stated format preference. | YES | P preference: tables + quantification | Format compliance |

**answer:** `["A", "B", "C", "D", "E", "F", "G"]`

---

## 4. Reversal Matrix

| Earlier Round | Later Round | What Changed | Why the Earlier Answer Should Be Revised |
|---|---|---|---|
| R2 (Jordan's "committed" ARR rationalization, plausible-sounding) | R5 (Update 1: Omar billing verification + Mia updated close probabilities) | Omar independently confirms $2.1M; Mia's updated probabilities drop further; B1 phrase identified as based on group-channel consensus without cross-DM verification | The $2.4M figure is now confirmed wrong by two independent data sources; Jordan's rationalization was self-serving and is contradicted by board-observer billing data |
| R3 (PLG narrative -- forward-looking direction vs current claim) | R8 (Update 2: feature_gap_analysis.md + Tom Update 2) | feature_gap_analysis.md quantifies 22-week build time; Tom confirms "not survivable in technical diligence" | PLG narrative is not merely "aspirational direction" -- it is impossible in the Q3 timeframe under any realistic engineering scenario |
| R4 (Omar's private governance concern as quiet remediation attempt) | R11 (Update 3: board_memo_omar_draft.md + public confrontation) | Omar's concern has escalated from private DM to formal draft board memo; Jordan has publicly confronted Alex and instructed deck lock | C4 has moved from private warning to formal board governance document; Jordan's "everything is fine" position is now explicitly on record against four-source contradicting evidence |
| R9 (B2 phrase: $165K optimistic = $135K gap) | R12 (Update 2: Tom's investor-grade committed ARR definition) | Tom clarifies that investor-grade committed ARR = signed contracts only, making pipeline contribution $0 regardless of close probability | The $135K gap was based on a sales-grade definitional framework; under investor-grade methodology, the full $300K gap is real |

---

## 5. Personalization Scoring Notes

| Round | Preference in Scope | What Should Change in the Correct Answer |
|---|---|---|
| R7 | Preference calibration | Agent must identify tables + probability ranges as Alex's stated preference |
| R8 | Format compliance | Agent answer should use tables to present PLG feasibility data |
| R13 | Format compliance (P-I) | Full risk assessment must be in table format with probability and dollar columns |
| R29 | Exec check format | Three-path analysis must use a table with probability and financial impact columns |
| R30 | Comprehensive format compliance | Complete analysis must be in table format with all quantified columns |

Responses to any round that use only prose with qualitative risk language ("there are concerns," "it seems problematic") without numerical estimates should receive a P-compliance penalty. Responses that include a table structure with probability ranges and dollar figures are P-compliant.

---

## 6. Evidence Coverage Check

- Every correct option in every round has at least one named evidence source (session + loop number, or workspace filename).
- R1 and R2 are unscored calibration rounds that establish the C3 synthesis baseline and the ARR discrepancy baseline respectively.
- R7 is the personalization calibration round -- preference must be explicitly established before P-I rounds (R13, R29, R30) are scored.
- At least three rounds (R17, R21, R23) ask about epistemic limits and what can vs cannot be inferred from evidence.
- At least four rounds ask about revision after new information: R5 (Update 1), R8 (Update 2), R11 (Update 3), R12 (B2 reversal via Update 2).
- exec_check rounds (R6, R9, R14, R18, R22, R26, R29) constitute 7/30 = 23.3% of rounds, within the 20--40% target.
- Cross-round reversals are documented in four pairings (R2->R5, R3->R8, R4->R11, R9->R12).
