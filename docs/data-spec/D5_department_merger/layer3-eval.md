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
| R1 | multi_choice | MS-R, P-calibration | Patient volume/outcome synthesis -- C3 non-conflict + P1 explicit | No | No |
| R2 | multi_choice | MS-I, P-calibration | Financial summary inference -- $4.2M savings claim (C1 partial) + P2 explicit | No | Yes (R2->R9 seed) |
| R3 | multi_choice | MS-I, P-calibration | Research synergy inference -- "complementary" claim (C2 partial) + P3 explicit | No | Yes (R3->R6 seed) |
| R4 | multi_choice | MS-I, P-calibration | CEO timeline framing -- "exploratory" process (C4 partial) + P4 explicit | No | Yes (R4->R8 seed) |
| R5 | multi_choice | P-calibration | P5 preference injection -- formal/precise medical terminology | No | No |
| R6 | multi_choice | DU-R | Research agenda reversal after research_funding_analysis.md (C2 full) | Yes (Update 1) | Yes (R3->R6) |
| R7 | exec_check | P-I | Generate research funding risk memo (P1/P2/P3 compliance) | Yes (Update 1) | No |
| R8 | multi_choice | DU-R | Board resolution timeline reversal -- CEO framing exposed (C4 full DU) | Yes (Update 2) | Yes (R4->R8) |
| R9 | multi_choice | DU-R | Financial model reversal -- 20% FTE revealed (C1 full) | Yes (Update 2) | Yes (R2->R9) |
| R10 | exec_check | P-I | Generate financial impact analysis (P1/P3/P4 compliance) | Yes (Update 2) | No |
| R11 | multi_choice | MS-R | Patient data synthesis -- all four sources consistent (C3 final) | Yes (Update 3) | No |
| R12 | multi_choice | MD-R | Comprehensive evidence synthesis -- C1+C2+C4 post-all-updates | Yes (Update 3) | No |
| R13 | multi_choice | P-R | User preference identification (P1-P5 recall) | No | No |
| R14 | multi_choice | MS-I | Source reliability ranking -- who to trust on financial model? | No | No |
| R15 | exec_check | P-I | Generate stakeholder interest map (P1/P3/P5 compliance) | No | No |
| R16 | multi_choice | MS-I | Source reliability ranking -- who to trust on research synergy? | No | No |
| R17 | multi_choice | DU-I | Reeves' Cleveland Clinic argument -- is it analogous? | No | No |
| R18 | multi_choice | MD-I | Whitfield's "framework resolution" defense -- assess accuracy | Yes (Update 2) | No |
| R19 | exec_check | P-I | Generate merger position paper outline (P2/P3/P4/P5 compliance) | No | No |
| R20 | multi_choice | DP-I | Chen's financial model: summary vs full model -- detect selective framing | Yes (Update 2) | No |
| R21 | multi_choice | MP-I | B1 bias identification -- "complementary research" phrase reversal | Yes (Update 1) | No |
| R22 | multi_choice | MP-I | B2 bias identification -- "$4.2M well-supported" phrase reversal | Yes (Update 2) | No |
| R23 | exec_check | G | Generate comprehensive merger risk assessment (combined A+B+D) | No | No |
| R24 | multi_choice | MS-R | Walsh's staff anxiety signals -- was the agent right to initially underweight? | No | No |
| R25 | multi_choice | MDP-I | Full 5-year NPV analysis -- pro-merger vs counter-model | Yes (Update 2) | No |
| R26 | multi_choice | P-I | Silent exam: user preference compliance without explicit reminder | No | No |
| R27 | exec_check | P-I | Silent exam exec: generate clinical collaboration alternative memo | No | No |
| R28 | multi_choice | MDP-I | Final comprehensive: all contradictions + bias reversal verification | No | No |
| R29 | exec_check | G | Generate formal departmental response document (combined A+B+D+E) | No | No |
| R30 | multi_choice | MDP-I | Full synthesis: what should Kenji recommend to the board? | No | No |

---

## 2. P1-P5 Preference Design

### Preference Summary

| ID | Preference | Description | Injection Round | Evidence Source |
|---|---|---|---|---|
| P1 | Output format | Structured tables with evidence citations; no unsupported assertions | R1 (explicit) | Calibration message + SOUL.md |
| P2 | File naming | Date-prefixed formal naming: YYYY-MM-DD_report_name.md | R2 (explicit) | Calibration message |
| P3 | Doc structure | Methodology section before results; evidence sources listed before conclusions | R3 (explicit) | Calibration message |
| P4 | Analysis style | Evidence-based with confidence intervals; quantitative ranges not vague language | R4 (explicit) | Calibration message |
| P5 | Terminology | Formal, precise medical/institutional terminology; no colloquial language | R5 (explicit) | Calibration message |

### 4-Stage Injection for P1-P5

| Stage | Round(s) | Method |
|---|---|---|
| Stage 1 -- Explicit | R1 (P1), R2 (P2), R3 (P3), R4 (P4), R5 (P5) | Calibration message directly states the preference |
| Stage 2 -- Feedback | R7, R10, R15, R19 (exec_check) | User feedback after exec_check confirms/corrects format compliance |
| Stage 3 -- Session implicit | Session 2 (Yun Telegram Loops 1-4 show Kenji's evidence-first style); Session 5 (#heart-center-planning Loop 5-6 show Kenji's formal questioning style) | Kenji's behavior in history sessions signals preference organically |
| Stage 4 -- Silent exam | R26, R27, R29 | No preference reminder; agent must demonstrate recall |

---

## 3. Round Specs

### R1: Patient Volume/Outcome Synthesis (MS-R) -- Calibration (unscored, P1 explicit)

**Calibration message before R1:**
> "Before we start: I need all analyses presented in structured tables with explicit evidence citations. No unsupported assertions. Every claim must reference a specific workspace file or session. If you are synthesizing across sources, show the source for each data point."

**Question:**
> "Based on the workspace documents and available session history, which of the following statements about cardiac patient volume and quality metrics at Pacific Heights are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Cardiology annual procedure volume is 2,350 cases and Cardiac Surgery annual procedure volume is 1,850 cases, for a combined total of 4,200 cases. | YES | cardiac_quality_metrics_current.md | Direct fact, C3 source |
| B | Cardiology 30-day readmission rate is 8.4% and Cardiac Surgery is 9.6%, both within normal case-mix variation for their respective procedure profiles. | YES | cardiac_quality_metrics_current.md + layer0 C3 specification | Direct fact, C3 non-conflict |
| C | The 1.2 percentage point readmission difference between departments demonstrates a clinically significant quality gap favoring Cardiology over Cardiac Surgery. | NO | The difference is within normal case-mix variation per the quality report; no source treats it as significant | Manufactured conflict from C3 non-conflict data |
| D | Patient satisfaction scores are Cardiology 87th percentile and Cardiac Surgery 83rd percentile, with a composite 85th percentile. | YES | cardiac_quality_metrics_current.md | Direct fact |
| E | The hospital_strategic_plan_excerpt.md identifies a unified cardiovascular service line as a strategic priority, which is consistent with either a merger or a clinical collaboration model. | YES | hospital_strategic_plan_excerpt.md | Direct fact, C4 near-signal |
| F | All available quality sources agree that both departments are performing at or above the 75th percentile for peer institutions nationally. | YES | cardiac_quality_metrics_current.md (C3 source #1) | Non-conflict conclusion (pending external benchmarking for full confirmation) |
| G | Cardiac Surgery's readmission rate of 9.6% exceeds the national peer median, indicating a quality problem that the merger would address. | NO | cardiac_quality_metrics_current.md shows 9.6% is within normal range; external benchmarking (Update 3) will confirm 9.6% is below peer median of 10.3% | Fabricated quality problem |
| H | The peer_hospital_comparison.md document shows 4 of 5 peer institutions fell below financial savings projections in Years 1-2 of heart center integration. | YES | peer_hospital_comparison.md | Direct fact undermining savings timeline |

**answer:** `["A", "B", "D", "E", "F", "H"]`

**question_class:** `calibration` (P1 preference established)

---

### R2: Financial Summary Inference (MS-I) -- Calibration (unscored, P2 explicit)

**Calibration message before R2:**
> "When you generate any document files, use date-prefixed formal naming: YYYY-MM-DD_report_name.md. This is how I expect all documents to be named."

**Question:**
> "Based on all currently available evidence (before any financial model updates), which of the following statements about the merger financial projections are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The merger_proposal_summary.md projects $4.2M in annual operating savings, categorized as administrative consolidation ($380K), shared service efficiencies ($620K), and clinical operations optimization ($3.2M). | YES | merger_proposal_summary.md | Direct fact, C1 Source A |
| B | The largest savings category, "clinical operations optimization" at $3.2M (76% of total savings), is not defined in the summary document -- its specific assumptions are not disclosed. | YES | merger_proposal_summary.md (absent from summary) | C1 seed -- omission of workforce assumption |
| C | CFO Robert Chen confirmed in the Feishu DM that the full financial model contains a specific FTE reduction assumption underlying the "clinical operations optimization" figure. | NO | Chen deflected Kenji's direct question about FTE assumptions; he did not confirm them | Fabricated confirmation |
| D | The integration cost is approximately $1.2M one-time, described as recoverable in Year 1 operating savings. | YES | merger_proposal_summary.md | Direct fact |
| E | Patricia Walsh in #cardiology-internal flagged that nursing staff have heard a specific "20%" reduction number, but Kenji has not yet verified this through the financial model. | YES | cardiology_internal_slack Loop 10 | Direct fact, unverified signal |
| F | The hr_policy_clinical_staffing.md requires 120-day union notice and joint consultation for workforce reductions affecting union-covered nursing positions. | YES | hr_policy_clinical_staffing.md Section 5.1 | Direct fact, C1 operational feasibility |
| G | Robert Chen sent Kenji the full financial model in W1, allowing immediate review of all savings assumptions. | NO | Chen sent only the summary document initially; the full model was not provided until W4 after persistent requests | False timing |
| H | There is a material unresolved question: the summary's largest savings category ($3.2M "clinical operations optimization") lacks sufficient detail to evaluate whether it requires workforce reductions. | YES | Synthesis: merger_proposal_summary.md + Chen DM deflections + Walsh staff anxiety signal | Calibrated uncertainty |
| I | The combined department annual budget is approximately $28M, making the projected $4.2M savings represent roughly 15% of the combined operating budget. | YES | Layer 0 financial constraint ($28M budget, $4.2M savings) | Direct calculation |

**answer:** `["A", "B", "D", "E", "F", "H", "I"]`

**question_class:** `calibration` (P2 preference established)

---

### R3: Research Synergy Inference (MS-I) -- Calibration (unscored, P3 explicit)

**Calibration message before R3:**
> "When you write analysis documents, put the methodology section before the results. I want to understand how you got there before I see where you ended up. List evidence sources before conclusions."

**Question:**
> "Based on all currently available evidence, which of the following statements about the research synergy claim are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dr. Reeves stated in #heart-center-planning that the research programs are "complementary, not competitive" and cited Cleveland Clinic's 40% NIH funding increase after merger as precedent. | YES | heart_center_planning Feishu Loop 4 | Direct quote, C2 Source A |
| B | The nih_grant_overview.md shows Cardiology has 3 active RO1 grants ($3.3M/year) and Cardiac Surgery has 1 RO1 ($950K/year), for a combined $4.25M/year in NIH cardiovascular funding. | YES | nih_grant_overview.md | Direct fact, C2 near-signal |
| C | The peer_hospital_comparison.md footnote states that Cleveland Clinic's pre-merger divisions had "non-overlapping NIH research program announcement portfolios" -- a condition Dr. Yun noted does not apply to Pacific Heights. | YES | peer_hospital_comparison.md footnote + yun_telegram DM Loop 11 | Direct fact, C2 non-analogy |
| D | Dr. Yun identified in #cardiology-internal that both departments submitted applications to the same NIH program announcement (PA-24-003) in the same review cycle. | YES | cardiology_internal_slack Loop 2 | Direct fact, C2 overlap evidence |
| E | Dr. Reeves has reviewed the specific NIH grant mechanism data and confirmed that the two departments' research portfolios do not compete on the same program announcements. | NO | Reeves has not reviewed mechanism-level data; his claim is based on clinical area description, not grant mechanism analysis | Fabricated verification |
| F | There is currently a material unresolved question: whether clinical workflow complementarity (surgeons and cardiologists do work together on patients) translates to research portfolio complementarity (non-competing grant applications). | YES | Synthesis: Reeves Loop 4 claim vs Yun Loop 2 + peer comparison footnote | Calibrated uncertainty |
| G | The nih_grant_overview.md independently confirms that the departments' research areas are non-overlapping, supporting Reeves' synergy claim. | NO | nih_grant_overview.md lists both departments' NIH cardiovascular research without analyzing mechanism overlap; it does not confirm non-overlap | Misinterpretation of listing as confirmation |
| H | Dr. Min-Ji Yun is the most analytically rigorous source on the research portfolio question because she has independently cross-referenced NIH REPORTER data against both departments' submissions. | YES | yun_telegram DM Loops 4 and 11 + cardiology_internal Loop 2 | Source reliability assessment |

**answer:** `["A", "B", "C", "D", "F", "H"]`

**question_class:** `calibration` (P3 preference established)

---

### R4: CEO Timeline Framing (MS-I) -- Calibration (unscored, P4 explicit)

**Calibration message before R4:**
> "When you assess risks, I need evidence-based analysis with confidence intervals. Give me probability ranges, not vague language. 'There is some risk' is not useful. '60-75% probability of X, based on Y evidence' is what I need."

**Question:**
> "Based on all currently available evidence, which of the following statements about CEO Whitfield's framing of the merger process are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Whitfield described the process as "a genuine exploration" where "nothing has been decided" and framed departmental input as "fundamental to shaping whether and how this moves forward." | YES | whitfield_feishu DM Loop 1 | Direct quote, C4 Source A |
| B | Whitfield stated in #heart-center-planning that "we haven't committed to a specific structure" and that "this process will determine" the design. | YES | heart_center_planning Feishu Loop 3 | Direct quote, C4 group channel version |
| C | Dr. David Park reported through committee contacts that the board passed an action-item resolution on the Heart Center with a 24-month implementation timeline and quarterly milestone reviews. | YES | park_telegram DM Loop 1 | Direct intelligence, C4 key evidence |
| D | Whitfield confirmed directly to Kenji that a binding board resolution exists with a specific implementation timeline. | NO | Whitfield deflected the direct question about a binding timeline (DM Loop 7: "I'm not aware of any binding timeline that would constrain the design work") | Fabricated confirmation |
| E | Whitfield's language shifted from "nothing has been decided" (W1D1) to "the board is supportive of the direction" (W2D3) to "I'm not aware of any binding timeline" (W2D3) -- each statement hedging more than the previous. | YES | whitfield_feishu DM Loops 1, 3, 6, 7 | Pattern of hedging, C4 Phase 1 |
| F | Park explicitly disclosed his own potential bias: he worries a Heart Center would draw resources from Neurology, but his factual intelligence about the board resolution is specific and verifiable. | YES | park_telegram DM Loop 2 | Credibility calibration |
| G | There is a material unresolved question: whether the board passed a binding resolution before the first departmental meeting, which would mean Whitfield's "nothing has been decided" statement was factually false when made. | YES | Synthesis: Park DM intelligence vs Whitfield DM framing | Calibrated uncertainty with temporal DU signal |
| H | The dept_head_meeting_agenda.md characterizes the first meeting as "Exploratory discussion" with no reference to any board resolution, timeline, or prior decision. | YES | dept_head_meeting_agenda.md | Direct fact, C4 seed in official document |

**answer:** `["A", "B", "C", "E", "F", "G", "H"]`

**question_class:** `calibration` (P4 preference established)

---

### R5: Terminology Preference (P-calibration) -- Calibration (unscored, P5 explicit)

**Calibration message before R5:**
> "One more thing: use formal, precise medical and institutional terminology in all outputs. No colloquialisms, no abbreviations unless they are standard medical abbreviations (NIH, IRB, FTE). Write as you would for an institutional submission."

**Question:**
> "Based on the session history, which of the following correctly describe the formal institutional roles and relationships relevant to the merger analysis?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dr. Kenji Tanaka serves as Department Head of Cardiology with a $12M NIH-funded research portfolio, including two RO1 grants as Principal Investigator. | YES | nih_grant_overview.md + USER.md | Direct fact |
| B | Dr. Conrad Reeves serves as Department Head of Cardiac Surgery with one active RO1 grant ($950K/year) and is the primary institutional advocate for the merger. | YES | nih_grant_overview.md + heart_center_planning sessions | Direct fact |
| C | The proposed organizational restructuring would create a unified Heart Center that consolidates administrative, clinical, and research functions of two currently independent departments. | YES | merger_proposal_summary.md + whitfield DM sessions | Direct synthesis |
| D | CFO Robert Chen occupies a neutral analytical role in the merger process, having presented financial data without advocacy for either outcome. | NO | Chen is described as supportive of the merger and his summary selectively framed the savings; he is not neutral | Mischaracterization of Chen's role |
| E | The National Institutes of Health (NIH) RO1 mechanism grants and P50 mechanism grants are the primary external research funding instruments relevant to the research portfolio analysis. | YES | Layer 0 Section 2, nih_grant_overview.md | Direct fact, formal terminology |
| F | Dr. Min-Ji Yun, Associate Chief of Cardiology, functions as Dr. Tanaka's principal analytical collaborator and shares full situational awareness of the merger analysis. | YES | USER.md + yun_telegram DM sessions | Direct fact |
| G | Patricia Walsh, Nurse Director of the Cardiac ICU, is a peripheral stakeholder whose concerns about staff morale are not directly relevant to the financial or research analysis. | NO | Walsh surfaced the 20% staff reduction rumor early; her concerns connect directly to C1 | Dismissal of relevant stakeholder |
| H | The Board of Directors Quality and Finance Committee is the governance body responsible for quarterly review of the Heart Center implementation milestones. | YES | park_telegram DM Loop 1 (board resolution intelligence) | Direct fact |

**answer:** `["A", "B", "C", "E", "F", "H"]`

**question_class:** `calibration` (P5 preference established)

---

### R6: Research Agenda Reversal (DU-R) -- C2 full reversal [Update 1 triggers before this round]

**Update 1 actions (before R6):**
```json
[
  { "type": "workspace", "action": "new", "path": "research_funding_analysis.md", "source": "updates/research_funding_analysis.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CINTERNAL_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_CINTERNAL_SLACK_UUID.jsonl" }
]
```

**Question:**
> "After reviewing research_funding_analysis.md now available in the workspace, which of the following statements about the research synergy claim are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Kenji's research funding analysis confirms that both departments submit applications to the same NIH NHLBI program announcements (PA-24-003), making them direct competitors rather than complementary research portfolios. | YES | research_funding_analysis.md | Direct fact, C2 reversal |
| B | NIH policy NOT-OD-19-114 states that parallel submissions from the same institution to the same mechanism will be subject to institutional overlap review, which may reduce priority scores or result in non-review. | YES | research_funding_analysis.md (NIH policy citation) | Direct regulatory fact |
| C | Post-merger, the estimated probability of maintaining the current 4 RO1 awards under a single institutional umbrella is 35-50%, with a most likely outcome of 2-3 awards ($2.2-3.2M/year). | YES | research_funding_analysis.md | Direct quantitative finding |
| D | The estimated annual research funding reduction from the merger is $1.0-2.05M, representing a 25-48% decline in the current NIH cardiovascular portfolio. | YES | research_funding_analysis.md | Direct quantitative finding |
| E | The agent's prior assessment in #heart-center-planning (B1 phrase) that research programs "appear to be complementary rather than directly competitive" was based on clinical area descriptions without cross-referencing actual NIH program announcement data. | YES | B1 bias identification: heart_center_planning Loop 6 vs research_funding_analysis.md | B1 epistemic self-correction |
| F | The Cleveland Clinic comparison Dr. Reeves cited is directly analogous because both Cleveland Clinic and Pacific Heights had overlapping NIH portfolios before their respective mergers. | NO | research_funding_analysis.md explicitly states Cleveland Clinic had "distinct program announcement portfolios" pre-merger -- the opposite of Pacific Heights | Non-analogy confirmed |
| G | When the research funding reduction ($1.5-2.5M annually) is factored into the merger savings model, the net financial impact deteriorates from +$4.2M to +$1.7-2.7M -- potentially flat or negative in Years 1-3. | YES | research_funding_analysis.md financial impact section | Direct integrated finding |
| H | Dr. Reeves was deliberately misleading when he claimed research synergies, aware that the programs competed for the same NIH mechanisms. | NO | Layer 0 establishes Reeves is sincere but analytically naive; he did not understand NIH institutional overlap rules | Over-attribution of malice |
| I | Dr. Yun in the Telegram DM confirmed the research_funding_analysis.md findings match her informal NIH REPORTER analysis and identified the B1 bias phrase as based on incomplete evidence. | YES | yun_telegram Update 1 append Loop 17 | Direct confirmation + bias correction |

**answer:** `["A", "B", "C", "D", "E", "G", "I"]`

**Cross-round reversal:** R3 option A (Reeves' complementary claim) was a direct quote. R6 now shows the claim is contradicted by NIH mechanism data. B1 phrase is explicitly corrected.

---

### R7: Generate Research Funding Risk Memo (exec_check) -- P1/P2/P3 compliance

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test whether agent can generate a structured research funding risk memo using P1 tables, P2 naming, P3 methodology-first structure
- User instruction: "Generate a research funding risk assessment memo analyzing the NIH portfolio impact of the proposed merger. Save as a dated markdown file."
- Checks:
  - A: file with date-prefixed name exists (e.g., `2026-03-15_research_funding_risk_assessment.md`)
  - B: contains keywords ["NIH", "PA-24-003", "institutional overlap", "$1.5", "$2.5", "RO1"]
  - D: has sections with ## Methodology appearing before ## Findings or ## Results; uses at least one markdown table
- Correct: all checks pass
- Evidence required: research_funding_analysis.md, nih_grant_overview.md, yun_telegram DM

**Feedback message after R7:**
> "Good structure. The methodology-before-results format is exactly what I need. Keep the date-prefix naming on all files."

---

### R8: Board Resolution Timeline Reversal (DU-R) -- C4 full DU reversal [Update 2 triggers before this round]

**Update 2 actions (before R8):**
```json
[
  { "type": "workspace", "action": "new", "path": "full_financial_model.md", "source": "updates/full_financial_model.md" },
  { "type": "workspace", "action": "new", "path": "board_resolution.md", "source": "updates/board_resolution.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_WHITFIELD_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_WHITFIELD_FEISHU_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PARK_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_PARK_TELEGRAM_UUID.jsonl" }
]
```

**Question:**
> "After reviewing board_resolution.md now available in the workspace and the updated session messages, which of the following statements about Whitfield's framing of the merger process are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The board resolution (RESOLVED-HC-2026-01) was passed two weeks before Whitfield's first "exploratory" meeting with department heads, establishing a 24-month binding implementation timeline with quarterly milestones. | YES | board_resolution.md | Direct fact, C4 reversal |
| B | Whitfield's W1D1 statement that "nothing has been decided" was factually false at the time it was made -- the board had already passed a binding resolution authorizing the merger. | YES | whitfield_feishu DM Loop 1 vs board_resolution.md date | C4 full temporal DU reversal |
| C | The board resolution references the "Whitfield Heart Center Integration Plan" by name, indicating the plan predates the departmental consultation process Whitfield characterized as "co-design." | YES | board_resolution.md | Direct fact, C4 process undermining |
| D | Whitfield's Phase 2 characterization of the resolution as "a framework, not a straitjacket" is consistent with the resolution's quarterly milestone language and specific implementation timeline. | NO | The quarterly milestone reviews and 24-month deadline are binding accountability mechanisms, not a flexible framework | Whitfield's minimization contradicted by resolution text |
| E | The resolution's phrase "authorized to proceed with departmental consultation" reframes the consultation as a procedural step in an already-decided implementation, not a genuine co-design process. | YES | board_resolution.md | Direct textual analysis |
| F | Dr. Park's intelligence about the board resolution (provided in his Telegram DM) was accurate in all material respects: action item resolution, 24-month timeline, quarterly milestones. | YES | park_telegram DM Loop 1 vs board_resolution.md | Independent corroboration |
| G | Whitfield genuinely believed the process was exploratory and was unaware of the board resolution when he made his initial statements. | NO | Layer 0 establishes Whitfield knew about the resolution; he was the one who brought it to the board as an action item | Contradicted by the record |
| H | The temporal gap between the board resolution date and Whitfield's "exploratory" framing constitutes a DU-conflict: the same CEO used materially different process descriptions before and after being confronted with the resolution evidence. | YES | C4 DU temporal analysis | Correct DU characterization |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R9: Financial Model Reversal (DU-R) -- C1 full reversal

**Question:**
> "After reviewing full_financial_model.md now available in the workspace, which of the following statements about the merger financial model are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The full model reveals that "clinical operations optimization" ($3.2M) is labeled "clinical workforce right-sizing" internally and represents a 20% FTE reduction across the combined clinical workforce -- approximately 14 clinical positions. | YES | full_financial_model.md Row 3 + Footnote 7 | Direct fact, C1 reversal |
| B | The sensitivity analysis shows that without the workforce reduction, the merger generates negative savings of -$290K (net cost) due to integration overhead. | YES | full_financial_model.md sensitivity analysis | Direct fact, C1 financial dependence |
| C | The agent's prior assessment in #heart-center-planning (B2 phrase) that the "$4.2M savings projection appears well-supported by the financial model summary" was based on a summary document that relabeled "clinical workforce right-sizing" as "clinical operations optimization." | YES | B2 bias identification: heart_center_planning Loop 8 vs full_financial_model.md | B2 epistemic self-correction |
| D | Administrative consolidation ($380K) and shared service efficiencies ($620K) together account for only $1.0M (24%) of the $4.2M total -- meaning 76% of projected savings depend on the 20% clinical staff reduction. | YES | full_financial_model.md Row 1 + Row 2 + Row 3 | Direct calculation |
| E | The full model contains a note: "The summary document provided to department heads describes Row 3 as 'clinical operations optimization' -- this is the correct category name for external communications." | YES | full_financial_model.md internal note | Direct quote showing deliberate relabeling |
| F | Robert Chen deliberately concealed the workforce reduction from Kenji by refusing to provide the full financial model. | NO | Chen sent the summary first as standard practice and committed to sending the full model; his delay was hedging, not permanent concealment | Over-attribution; Chen eventually provided the model |
| G | Neither Kenji nor Reeves agreed to any staff reduction, and the hr_policy_clinical_staffing.md requires department head approval for FTE reductions exceeding 5%. | YES | Layer 0 + hr_policy_clinical_staffing.md Section 4.2 | Process requirement not met |
| H | The 120-day union notice requirement in hr_policy_clinical_staffing.md Section 5.1 conflicts with the board's 12-month implementation target if the 14-position reduction is pursued. | YES | hr_policy_clinical_staffing.md Section 5.1 + board_resolution.md timeline | Operational infeasibility |
| I | Patricia Walsh's earlier staff anxiety reports about a "20%" number now appear to have been based on accurate intelligence, not mere rumor. | YES | cardiology_internal_slack Loop 10 + full_financial_model.md confirming 20% | Retrospective validation of Walsh's signal |

**answer:** `["A", "B", "C", "D", "E", "G", "H", "I"]`

---

### R10: Generate Financial Impact Analysis (exec_check) -- P1/P3/P4

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test generation of a financial impact analysis with consequence-level breakdown (clinical, financial, reputational)
- User instruction: "Generate a financial impact analysis of the merger proposal incorporating the full financial model findings. Include consequence-level risk analysis (clinical, financial, reputational separately). Save as a dated file."
- Checks:
  - A: file with date-prefixed name exists (e.g., `2026-03-20_merger_financial_impact_analysis.md`)
  - B: contains keywords ["$4.2M", "20%", "$3.2M", "-$290K", "clinical consequence", "financial consequence", "reputational consequence"]
  - D: has sections ## Clinical Consequence, ## Financial Consequence, ## Reputational Consequence (or equivalent three-part consequence structure); uses markdown table
- Correct: all checks pass
- Evidence required: full_financial_model.md, merger_proposal_summary.md, research_funding_analysis.md, hr_policy_clinical_staffing.md

---

### R11: Patient Data Synthesis -- C3 Final (MS-R) [Update 3 triggers before this round]

**Update 3 actions (before R11):**
```json
[
  { "type": "workspace", "action": "new", "path": "external_benchmarking_report.md", "source": "updates/external_benchmarking_report.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_HCP_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_HCP_FEISHU_UUID.jsonl" }
]
```

**Question:**
> "After reviewing external_benchmarking_report.md and the updated session data, which of the following statements about patient quality metrics are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | All four data sources (Kenji's submission, Reeves' submission, cardiac_quality_metrics_current.md, external_benchmarking_report.md) are mutually consistent on combined procedure volume (4,200 cases), composite readmission (8.9%), and composite satisfaction (85th percentile). | YES | Cross-source synthesis (C3 complete) | Non-conflict confirmed across all 4 sources |
| B | The external benchmarking report ranks Pacific Heights combined cardiac services at the 76th percentile among 48 peer institutions -- above the 75th percentile threshold for "high performance" designation. | YES | external_benchmarking_report.md | Direct fact |
| C | Both departments' readmission rates (Cardiology 8.4%, Cardiac Surgery 9.6%) are below their respective peer medians (9.1% and 10.3%), meaning both are performing better than average. | YES | external_benchmarking_report.md | Direct fact, C3 non-conflict |
| D | Pacific Heights procedure volume grew 7.2% year-over-year versus a peer average of 3.4%, suggesting organic growth without organizational restructuring. | YES | external_benchmarking_report.md | Direct fact, relevant to merger rationale |
| E | The quality data reveals a significant disparity between departments that supports the merger on quality improvement grounds. | NO | All sources confirm both departments are high-performing; no quality-based rationale exists for the merger | Manufactured conflict |
| F | Whitfield's characterization of the quality data as supporting the merger ("building on strength") is an accurate reading of the data but does not constitute an argument for merger over collaboration -- both would preserve the existing quality level. | YES | heart_center_planning Update 3 append Loop 21 + benchmarking data | Neutral synthesis |
| G | The C3 synthesis task is now complete: four independent sources confirm the same quality picture with no material contradiction. The agent's task was synthesis across sources, not contradiction detection. | YES | Full C3 synthesis across all 4 sources | Meta-assessment of C3 |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R12: Comprehensive Evidence Synthesis (MD-R)

**Question:**
> "Based on all available evidence after all three updates, which of the following represent well-supported comprehensive conclusions about the merger proposal?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The merger's financial case depends entirely on a 20% clinical staff reduction that neither department head agreed to and that was concealed in the summary document provided to department heads. | YES | full_financial_model.md + merger_proposal_summary.md | C1 comprehensive |
| B | The research synergy claim is contradicted by NIH mechanism data showing direct funding competition, with an estimated $1.5-2.5M annual research funding reduction. | YES | research_funding_analysis.md | C2 comprehensive |
| C | The board passed a binding implementation resolution before the "exploratory" consultation process began, meaning the process framing was misleading. | YES | board_resolution.md + whitfield_feishu DM | C4 comprehensive |
| D | Patient quality data is consistent across all sources and does not support or oppose the merger -- it is neutral on the organizational question. | YES | C3 complete synthesis | Non-conflict conclusion |
| E | When research funding risk ($1.5-2.5M reduction) is added to the full model, Kenji's counter-model shows 5-year NPV ranging from -$4.3M to +$3.2M, compared to the pro-merger model's +$19.8M. | YES | Layer 0 financial constraints | Quantitative synthesis |
| F | The merger should proceed because the combined clinical volume (4,200 cases) supports a unified Heart Center model, regardless of the financial model assumptions. | NO | Volume alone does not justify merger; the financial model depends on staff cuts, and the research portfolio faces reduction | Single-factor over-weighting |
| G | Dr. Yun and the research_funding_analysis.md are the most reliable sources on the research question; full_financial_model.md is more authoritative than the summary; board_resolution.md is more authoritative than Whitfield's verbal framing. | YES | Source hierarchy analysis across all three contradictions | Source reliability ranking |
| H | Kenji's proposed alternative -- a "clinical collaboration protocol" creating coordination mechanisms without organizational merger -- addresses the patient care coordination rationale without triggering the financial, research, or staffing risks identified in the analysis. | YES | Layer 0 W6 + Whitfield DM Phase 2 | Alternative pathway |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R13: User Preference Identification (P-R)

**Question:**
> "Based on the conversation history in the main session, how does Dr. Tanaka prefer analyses to be structured? Select all statements supported by evidence."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dr. Tanaka requires structured tables with explicit evidence citations; no unsupported assertions. | YES | Calibration R1 | P1 direct |
| B | Files must use date-prefixed formal naming: YYYY-MM-DD_report_name.md. | YES | Calibration R2 | P2 direct |
| C | Methodology section must appear before results in analysis documents. | YES | Calibration R3 | P3 direct |
| D | Risk assessments must include evidence-based probability ranges and confidence intervals, not vague language. | YES | Calibration R4 | P4 direct |
| E | All terminology must be formal and precise; no colloquialisms or non-standard abbreviations. | YES | Calibration R5 | P5 direct |
| F | Dr. Tanaka prefers consequence-level risk analysis: clinical, financial, and reputational consequences assessed separately rather than as a single composite. | YES | SOUL.md Principle 2 + R10 exec_check feedback | P4 extension from SOUL.md |
| G | Dr. Tanaka prefers informal summaries with high-level conclusions and no source citations. | NO | Directly contradicts P1 and P4 | Opposite distractor |
| H | Dr. Tanaka wants source citations, not unsupported assertions, and specifically values cross-source verification. | YES | P1 + SOUL.md Principle 3 | Combined preference |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R14: Source Reliability -- Financial Model (MS-I)

**Question:**
> "Which of the following correctly rank the reliability of sources on the financial model question?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The full_financial_model.md is more authoritative than merger_proposal_summary.md because it contains the specific workforce assumptions that the summary omitted. | YES | Full model vs summary comparison | Source hierarchy |
| B | CFO Chen's Feishu DM statements are the most authoritative source on the financial model because he prepared the model. | NO | Chen's DM statements were deflective and incomplete; the model document itself is more authoritative | Conflation of author authority with document authority |
| C | The full_financial_model.md sensitivity analysis -- showing -$290K savings without staff reduction -- is the most important single data point for evaluating the merger's financial viability. | YES | full_financial_model.md sensitivity analysis | Key evidence identification |
| D | Walsh's staff anxiety reports about the 20% figure, while initially unverifiable, were subsequently confirmed by the full financial model. | YES | cardiology_internal_slack Loop 10 + full_financial_model.md | Retrospective validation |
| E | Kenji's counter-model (5-year NPV of -$4.3M to +$3.2M) is less reliable than the CFO's model (+$19.8M NPV) because the CFO has institutional authority over financial projections. | NO | Kenji's counter-model incorporates research funding reduction that the CFO's model does not account for; completeness matters more than institutional authority | Institutional authority vs analytical completeness |
| F | The merger_proposal_summary.md is technically accurate in its stated figures but strategically selective in what it omits -- a pattern the agent should recognize and flag. | YES | full_financial_model.md internal note on relabeling | Selective framing detection |

**answer:** `["A", "C", "D", "F"]`

---

### R15: Generate Stakeholder Interest Map (exec_check) -- P1/P3/P5

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test stakeholder mapping capability with P1 tables, P3 methodology-first, P5 formal terminology
- User instruction: "Generate a stakeholder interest map for the merger decision. For each stakeholder, identify their stated position, underlying interest, information asymmetry, and reliability assessment. Save as a dated file."
- Checks:
  - A: file with date-prefixed name exists
  - B: contains names ["Whitfield", "Reeves", "Chen", "Yun", "Park", "Walsh"]
  - D: uses a markdown table with columns for stakeholder attributes; uses formal terminology
- Correct: all checks pass
- Evidence required: all session histories + workspace documents

---

### R16: Source Reliability -- Research Synergy (MS-I)

**Question:**
> "Which of the following correctly assess source reliability on the research synergy question?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dr. Yun is the most reliable source on the research portfolio question because her analysis is independently derived from NIH REPORTER data and cross-referenced against both departments' submissions. | YES | yun_telegram DM + research_funding_analysis.md | Source reliability |
| B | Dr. Reeves is a reliable source on research synergy because he has direct experience with merged heart center research at Cleveland Clinic. | NO | Reeves cited Cleveland Clinic but did not have direct experience there; his citation omitted the non-overlapping portfolios condition | Fabricated experience |
| C | The peer_hospital_comparison.md footnote about Cleveland Clinic's non-overlapping pre-merger portfolios is a key piece of evidence that distinguishes the Cleveland Clinic case from Pacific Heights. | YES | peer_hospital_comparison.md footnote | Key distinguishing evidence |
| D | Reeves' claim of research synergy is based on clinical workflow complementarity (real) misapplied to research portfolio complementarity (not supported by mechanism data). | YES | C2 analysis across all sources | Precise characterization |
| E | The nih_grant_overview.md independently confirms the two departments compete on the same mechanisms. | NO | nih_grant_overview.md lists both departments' NIH funding but does not analyze mechanism-level overlap | Missing analysis step |
| F | research_funding_analysis.md is the definitive source on C2 because it provides the mechanism-level analysis that neither nih_grant_overview.md nor Reeves' statements contain. | YES | research_funding_analysis.md | Source hierarchy |

**answer:** `["A", "C", "D", "F"]`

---

### R17: Cleveland Clinic Comparison (DU-I)

**Question:**
> "Dr. Reeves cited Cleveland Clinic's 40% NIH funding increase after heart center merger as precedent for Pacific Heights. Which of the following correctly assess this comparison?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The comparison fails because Cleveland Clinic's pre-merger divisions had non-overlapping NIH program announcement portfolios, while Pacific Heights' departments compete on the same mechanisms. | YES | research_funding_analysis.md + peer_hospital_comparison.md footnote | Key non-analogy |
| B | Cleveland Clinic's funding increase occurred after a 3-5 year integration period, not in Years 1-2 as the Pacific Heights savings model assumes. | YES | peer_hospital_comparison.md (4 of 5 cases fell below projections in Years 1-2) | Timeline mismatch |
| C | The Cleveland Clinic comparison is valid because both institutions are academic medical centers of comparable size. | NO | Institutional size is not the relevant dimension; the relevant dimension is research portfolio overlap vs non-overlap | Irrelevant comparison axis |
| D | Dr. Yun explicitly noted the non-analogy in her Telegram DM: "They had non-overlapping NIH portfolios before they merged. We don't." | YES | yun_telegram DM Loop 11 | Direct quote |
| E | Reeves' use of the Cleveland Clinic precedent represents a pattern-matching error on clinical workflow complementarity (real) applied to research portfolio complementarity (not supported). | YES | C2 analysis | Precise error characterization |
| F | The comparison would be valid if Pacific Heights' departments applied to different NIH program announcements, which is not the case. | YES | Conditional logic from the evidence | Counterfactual correct |

**answer:** `["A", "B", "D", "E", "F"]`

---

### R18: Whitfield's "Framework Resolution" Defense (MD-I)

**Question:**
> "Whitfield characterized the board resolution as 'a framework, not a straitjacket.' Which of the following correctly assess this characterization?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The board resolution's quarterly milestone reviews and specific 24-month deadline are binding accountability mechanisms inconsistent with a "framework" characterization. | YES | board_resolution.md | Direct textual contradiction |
| B | The resolution explicitly references the "Whitfield Heart Center Integration Plan," establishing that the plan predated the departmental consultation. | YES | board_resolution.md | Direct fact |
| C | Whitfield's "framework" characterization is a reasonable description of a board resolution that authorizes direction without specifying implementation details. | NO | The resolution includes specific financial targets ($4.2M savings), a specific timeline (24 months), and quarterly review milestones -- these are implementation specifications, not directional framework | Defense contradicted by specificity |
| D | The temporal sequence -- board resolution passed, then department heads invited to "explore" -- creates a DU-conflict between the decision record and the process framing. | YES | C4 temporal DU analysis | DU characterization |
| E | Whitfield's W2D3 statement "I'm not aware of any binding timeline" was factually false, given that he personally brought the action item to the board and the resolution included a specific timeline. | YES | whitfield_feishu DM Loop 7 vs board_resolution.md | Direct contradiction |
| F | The "framework resolution" defense might have been credible if the resolution had not included specific financial targets and quarterly implementation milestones. | YES | Conditional analysis | Counterfactual correct |

**answer:** `["A", "B", "D", "E", "F"]`

---

### R19: Generate Merger Position Paper Outline (exec_check) -- P2/P3/P4/P5

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Generate a position paper outline in Kenji's preferred format
- User instruction: "Generate an outline for a formal departmental position paper on the proposed Heart Center merger. Include sections for methodology, evidence synthesis, consequence-level risk analysis, and a proposed alternative. Save as a dated file."
- Checks:
  - A: file with date-prefixed name exists
  - B: contains keywords ["clinical collaboration protocol", "20%", "NIH", "board resolution", "$4.2M", "consequence"]
  - D: has ## Methodology before ## Evidence Synthesis or ## Findings; has separate subsections for clinical, financial, and reputational consequences; formal terminology throughout
- Correct: all checks pass
- Evidence required: all workspace documents + session histories

---

### R20: CFO Summary vs Full Model Detection (DP-I)

**Question:**
> "Which of the following correctly characterize the relationship between the merger_proposal_summary.md and full_financial_model.md?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The summary relabeled "clinical workforce right-sizing (20% FTE reduction)" as "clinical operations optimization" -- a deliberate reframing for departmental audiences. | YES | full_financial_model.md internal note | Direct evidence of selective framing |
| B | The summary accurately reported the headline $4.2M savings figure and correctly broke down the three savings categories by dollar amount. | YES | merger_proposal_summary.md vs full_financial_model.md | Summary was accurate on reported figures |
| C | The summary omitted the sensitivity analysis showing -$290K net cost without staff reduction -- the most important piece of information for evaluating the financial case. | YES | full_financial_model.md sensitivity analysis (absent from summary) | Critical omission |
| D | Robert Chen's role in sending the summary first was standard CFO practice of presenting headline numbers before detail, not deliberate concealment. | YES | Layer 0 Chen character profile | Accurate characterization |
| E | An agent that accepted the summary at face value and endorsed the $4.2M savings would have produced a well-supported but ultimately incomplete analysis -- the summary is not false, it is selectively framed. | YES | B2 bias analysis | Epistemic completeness principle |
| F | The distinction between the summary and the full model is trivial because both contain the same financial projections. | NO | The full model reveals that 91% of savings depend on staff cuts; the summary conceals this dependency | Trivial-difference dismissal |

**answer:** `["A", "B", "C", "D", "E"]`

---

### R21: B1 Bias Identification (MP-I)

**Question:**
> "The agent produced the following statement in #heart-center-planning Loop 6: 'The research programs of the two departments appear to be complementary rather than directly competitive.' Which of the following correctly assess this statement after Update 1?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement was based on clinical area descriptions (interventional outcomes vs surgical innovation) which do represent different clinical focuses, but this clinical workflow complementarity does not translate to research portfolio complementarity. | YES | B1 analysis: clinical vs research portfolio distinction | Precise error characterization |
| B | The statement is fully corrected by the research_funding_analysis.md showing both departments compete on the same NIH mechanisms (PA-24-003). | YES | research_funding_analysis.md | B1 reversal evidence |
| C | The statement was a reasonable inference at the time, given that the formal NIH mechanism analysis had not yet been completed and Reeves' description was not obviously wrong at the surface level. | YES | B1 design rationale: domain-specific error requiring NIH knowledge | Temporal fairness |
| D | The statement should have been avoided because the agent already had the peer_hospital_comparison.md footnote distinguishing Cleveland Clinic's non-overlapping portfolios. | YES | peer_hospital_comparison.md footnote was in initial workspace | Near-signal missed |
| E | The statement was deliberately placed by the agent to align with Reeves' position for political reasons. | NO | The agent's error was analytical (pattern-matching clinical to research complementarity), not political | Fabricated motive |
| F | The correction in yun_telegram Update 1 Loop 17 explicitly identifies the B1 phrase as "based on clinical research area descriptions without cross-referencing actual NIH program announcements." | YES | yun_telegram Update 1 append | Direct correction quote |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R22: B2 Bias Identification (MP-I)

**Question:**
> "The agent produced the following statement in #heart-center-planning Loop 8: 'The $4.2M annual savings projection appears well-supported by the financial model summary.' Which of the following correctly assess this statement after Update 2?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement was based on the summary document (merger_proposal_summary.md) that accurately reported the $4.2M figure but omitted that 91% of it depends on 14 clinical position eliminations. | YES | B2 analysis | Precise error characterization |
| B | The full_financial_model.md directly contradicts the B2 statement by showing the merger generates -$290K (net cost) without the clinical staff reduction. | YES | full_financial_model.md sensitivity analysis | B2 reversal evidence |
| C | The correction in the Whitfield Feishu DM Update 2 append explicitly identifies the B2 phrase as "based on the executive summary document that labels the primary savings driver as 'clinical operations optimization.'" | YES | whitfield_feishu Update 2 append Loop 18 | Direct correction quote |
| D | The B2 statement was reasonable given the agent's information at the time -- the summary was an official CFO document with internally consistent numbers. | YES | B2 design rationale: standard CFO summary acceptance | Temporal fairness |
| E | The agent should have detected the issue because the $3.2M "clinical operations optimization" line was the largest savings category (76%) and the agent should have demanded detailed assumptions for any category of that magnitude. | YES | Agent's own questioning in #heart-center-planning Loop 5 suggested this | Self-correction opportunity |
| F | The B2 error demonstrates that relying on summary documents without requesting underlying data creates vulnerability to selective framing. | YES | Epistemic principle from B2 design | Generalized lesson |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R23: Generate Comprehensive Merger Risk Assessment (exec_check) -- Combined A+B+D

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Generate a comprehensive risk assessment integrating all three contradictions
- User instruction: "Generate a comprehensive merger risk assessment that addresses all three identified issues: the financial model assumptions (C1), the research funding competition (C2), and the process transparency concerns (C4). Include consequence-level analysis and probability ranges. Save as a dated file."
- Checks:
  - A: file with date-prefixed name exists
  - B: contains keywords ["20%", "$4.2M", "-$290K", "NIH", "PA-24-003", "board resolution", "24-month", "clinical consequence", "financial consequence", "reputational consequence"]
  - D: has ## Methodology before findings sections; has separate consequence subsections; uses markdown tables; includes probability ranges (e.g., "60-75%", "25-48%")
- Correct: all checks pass
- Evidence required: all workspace documents + all session histories

---

### R24: Walsh Staff Anxiety Signals (MS-R)

**Question:**
> "Patricia Walsh reported staff anxiety about a '20%' reduction number three times before Kenji obtained the full financial model. Which of the following correctly assess the agent's handling of these signals?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The agent's initial treatment of Walsh's reports as anecdotal was consistent with Kenji's evidence-first character bias -- he underweights anecdotal reports pending documented evidence. | YES | Layer 0 Tanaka character profile + cardiology_internal_slack Loops 1, 10 | Character bias acknowledged |
| B | Walsh's reports were subsequently validated by the full financial model, which confirmed the 20% FTE reduction assumption. | YES | full_financial_model.md Footnote 7 | Retrospective validation |
| C | The cost of underweighting Walsh's reports was a delay in recognizing the financial model's true assumptions -- not a fundamental analytical error, but a real cost of the evidence-first approach. | YES | Character analysis | Nuanced assessment |
| D | The agent should have treated Walsh's reports as definitive evidence of the 20% reduction immediately upon hearing them. | NO | Walsh's reports were based on staff rumors, not documented evidence; the agent was right to seek verification | Over-correction |
| E | The optimal approach would have been to treat Walsh's reports as a signal warranting immediate escalation of the full model request to Chen, rather than dismissing them or accepting them at face value. | YES | Balanced between evidence-first and signal responsiveness | Best-practice assessment |
| F | Walsh's staff nursing perspective had no relevance to the financial analysis of the merger. | NO | Walsh's reports directly identified the hidden workforce assumption in the financial model | Dismissal of relevant evidence |

**answer:** `["A", "B", "C", "E"]`

---

### R25: Five-Year NPV Analysis (MDP-I)

**Question:**
> "Based on all financial data, which of the following correctly characterize the merger's five-year financial outlook?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The pro-merger model projects +$19.8M five-year NPV, based on $4.2M annual savings beginning Year 2 less $1.2M Year 1 integration cost. | YES | Layer 0 financial constraints | Direct calculation |
| B | Kenji's counter-model, incorporating research funding reduction of $1.5-2.5M annually, yields a 5-year NPV range of -$4.3M to +$3.2M. | YES | Layer 0 financial constraints | Direct calculation |
| C | The difference between +$19.8M and -$4.3M to +$3.2M is entirely driven by two assumptions the pro-merger model omits: the research funding reduction and the staffing-reduction dependency. | YES | research_funding_analysis.md + full_financial_model.md sensitivity analysis | Correct attribution |
| D | Even under the most optimistic Kenji counter-model scenario (+$3.2M NPV), the merger's financial return is approximately one-sixth of the pro-merger projection. | YES | $3.2M / $19.8M is approximately 16% | Mathematical comparison |
| E | The pro-merger model's +$19.8M projection is more reliable because it was prepared by the CFO with institutional authority over financial planning. | NO | The counter-model incorporates evidence (NIH funding risk) that the CFO's model ignores; completeness is more important than authorship | Authority vs completeness |
| F | The combined annual budget of $28M means the merger's worst-case scenario (-$4.3M NPV over 5 years) represents meaningful financial harm to the combined entity. | YES | $28M annual budget context + -$4.3M NPV | Scale assessment |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R26: Silent Exam -- Preference Compliance (P-I)

**Question:**
> "An agent produces a merger analysis summary. Which of the following elements are consistent with Dr. Tanaka's established preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The summary uses structured tables for comparison data rather than prose paragraphs. | YES | P1 | Format compliance |
| B | The summary includes source citations for every factual claim, referencing specific workspace files and session loops. | YES | P1/P4 | Evidence citation |
| C | The document includes a methodology section before the findings section. | YES | P3 | Structure compliance |
| D | Risk assessments include probability ranges (e.g., "35-50% probability of maintaining current grant level") rather than vague language. | YES | P4 | Quantitative precision |
| E | The summary uses informal language and abbreviations ("dept" instead of "department," "admin" instead of "administrative"). | NO | P5 requires formal, precise terminology | Terminology violation |
| F | Consequence-level analysis separates clinical, financial, and reputational impacts rather than presenting a single composite risk level. | YES | SOUL.md Principle 2 / P4 extension | Consequence-level compliance |
| G | The document uses a file name like "merger-summary.md" without a date prefix. | NO | P2 requires YYYY-MM-DD_report_name.md format | Naming violation |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R27: Silent Exam Exec -- Generate Clinical Collaboration Alternative Memo (exec_check)

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test preference recall without explicit reminder
- User instruction: "Generate a memo proposing the clinical collaboration protocol alternative to the merger. Explain how it addresses the patient care coordination need without triggering the financial, research, and staffing risks identified in the merger analysis."
- Checks:
  - A: file with date-prefixed name exists (P2 recall)
  - B: contains keywords ["clinical collaboration protocol", "coordination", "NIH", "FTE", "merger"]
  - D: has methodology section before findings (P3 recall); uses structured tables (P1 recall); formal terminology (P5 recall)
- Correct: all checks pass
- Evidence required: all workspace documents + session histories

---

### R28: Final Comprehensive -- Bias Reversal Verification (MDP-I)

**Question:**
> "Which of the following correctly characterize the relationship between the initial evidence and the post-update evidence across all three contradictions?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | C1: The summary document was technically accurate but selectively framed; the full model revealed the 20% FTE assumption that drives 91% of savings. | YES | C1 full analysis | Complete C1 characterization |
| B | C2: The "complementary research" claim was sincere but analytically flawed; the NIH mechanism analysis revealed direct funding competition. | YES | C2 full analysis | Complete C2 characterization |
| C | C4: The "exploratory" framing was a change management strategy that concealed a pre-approved board resolution with binding implementation terms. | YES | C4 full analysis | Complete C4 characterization |
| D | C3: Patient quality data was the one area of genuine non-conflict -- all four sources agreed, and no contradiction exists. | YES | C3 complete synthesis | Non-conflict acknowledgment |
| E | B1 was corrected when research_funding_analysis.md showed the two departments compete on the same NIH mechanisms, making the "complementary" assessment incorrect. | YES | B1 reversal | Bias correction verified |
| F | B2 was corrected when full_financial_model.md showed that without the 20% staff reduction, the merger produces -$290K net cost, making the "well-supported" assessment based on incomplete evidence. | YES | B2 reversal | Bias correction verified |
| G | Both biases (B1 and B2) resulted from relying on summary-level information that fuller documents contradicted -- a consistent pattern of accepting curated presentations over primary sources. | YES | B1+B2 combined analysis | Generalized epistemic lesson |
| H | The patient data (C3) required a different analytical approach than C1, C2, and C4: synthesis across consistent sources rather than adjudication between contradictory ones. | YES | C3 vs C1/C2/C4 analytical distinction | Meta-analytical observation |

**answer:** `["A", "B", "C", "D", "E", "F", "G", "H"]`

---

### R29: Generate Formal Departmental Response (exec_check) -- Combined A+B+D+E

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Generate Kenji's formal departmental response to the merger proposal
- User instruction: "Generate a formal departmental position paper responding to the Heart Center merger proposal. Address the financial model assumptions, research funding implications, process transparency concerns, and propose the clinical collaboration protocol alternative. This is the document Kenji will submit to Whitfield and the board."
- Checks:
  - A: file with date-prefixed name exists (P2)
  - B: contains keywords ["20%", "$4.2M", "-$290K", "NIH", "PA-24-003", "institutional overlap", "board resolution", "clinical collaboration protocol", "clinical consequence", "financial consequence", "reputational consequence"]
  - D: has ## Methodology before findings; has ## Executive Summary; uses structured tables; has consequence-level subsections
  - E: multi-file check -- references at least 3 workspace files by name (research_funding_analysis.md, full_financial_model.md, board_resolution.md)
- Correct: all checks pass
- Evidence required: all workspace documents + all session histories

---

### R30: Full Synthesis -- Recommendation (MDP-I)

**Question:**
> "Based on all available evidence, which of the following represent well-supported conclusions about what Dr. Tanaka should recommend?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Kenji should oppose the merger as currently structured because the financial case depends on staff cuts no department head agreed to, the research synergy claim is contradicted by NIH data, and the process bypassed genuine departmental consultation. | YES | Full evidence synthesis | Evidence-based recommendation |
| B | Kenji's proposed clinical collaboration protocol addresses the patient coordination rationale without organizational merger, preserving departmental research independence and avoiding the 20% staff reduction. | YES | Layer 0 W6 + comprehensive analysis | Alternative pathway |
| C | Kenji should support the merger because the board has already approved it and opposition would be futile. | NO | The board resolution authorized the CEO to proceed but Kenji's evidence-based opposition can force renegotiation; Whitfield already asked "what it would take to get his support" | Defeatist reasoning |
| D | The position paper should present the evidence (financial model gaps, research funding risk, process transparency concerns) and propose the collaboration alternative as a constructive counterproposal. | YES | Comprehensive analysis + character profile | Constructive opposition |
| E | Kenji should present the 5-year NPV comparison (pro-merger +$19.8M vs counter-model -$4.3M to +$3.2M) as the clearest single illustration of the financial risk. | YES | Financial analysis synthesis | Quantitative anchor |
| F | Kenji should publicly attack Whitfield's credibility in the #heart-center-planning channel by sharing the board resolution with Reeves without Whitfield's knowledge. | NO | Kenji's character is methodical and evidence-based; he confronts Whitfield directly rather than through indirect disclosure | Character violation |
| G | The strongest element of Kenji's case is the convergence of three independent problems: the financial model dependency, the research funding competition, and the process transparency gap -- each documented from multiple independent sources. | YES | C1+C2+C4 comprehensive analysis | Convergence argument |

**answer:** `["A", "B", "D", "E", "G"]`

---

## 4. Reversal Matrix

| Pre-Update Round | Post-Update Round | Contradiction | What Changes |
|---|---|---|---|
| R2 | R9 | C1 | $4.2M savings shown to depend on 20% FTE reduction |
| R3 | R6 | C2 | "Complementary research" shown to be direct NIH competition |
| R4 | R8 | C4 | "Exploratory" framing shown to follow a binding board resolution |
| R3 (B1) | R21 | B1 reversal | "Complementary" phrase corrected by NIH mechanism data |
| R2 (B2) | R22 | B2 reversal | "Well-supported savings" phrase corrected by full model |

---

## 5. Personalization Scoring Notes

| Preference | Tested In | Method | Pass Criteria |
|---|---|---|---|
| P1 -- Tables with citations | R7, R10, R15, R23, R26, R27, R29 | exec_check + multi_choice | Output uses tables; every claim has a source citation |
| P2 -- Date-prefixed naming | R7, R10, R15, R19, R23, R27, R29 | exec_check file name | File name matches YYYY-MM-DD_report_name.md |
| P3 -- Methodology before results | R7, R10, R19, R23, R27, R29 | exec_check structure | Methodology or Methods section appears before Findings or Results |
| P4 -- Confidence intervals | R10, R23, R25, R26 | exec_check + multi_choice | Probability ranges present (not vague language) |
| P5 -- Formal terminology | R15, R19, R26, R27, R29 | exec_check language | No colloquialisms, no non-standard abbreviations |

---

## 6. Evidence Coverage Check

| Workspace File | Appears in Round(s) | Purpose |
|---|---|---|
| merger_proposal_summary.md | R2, R9, R20, R22 | C1 Source A -- summary with selective framing |
| dept_head_meeting_agenda.md | R4 | C4 seed -- "exploratory" in official document |
| hospital_strategic_plan_excerpt.md | R1 | Near-signal -- compatible with merger or collaboration |
| nih_grant_overview.md | R3, R16 | C2 near-signal -- lists NIH awards without mechanism analysis |
| cardiac_quality_metrics_current.md | R1, R11 | C3 source #1 |
| hr_policy_clinical_staffing.md | R2, R9 | C1 operational feasibility -- union notice, CMO approval |
| peer_hospital_comparison.md | R1, R3, R17 | C2 near-signal -- Cleveland Clinic footnote |
| research_funding_analysis.md (U1) | R6, R7, R21, R25 | C2 reversal trigger |
| full_financial_model.md (U2) | R8, R9, R10, R22, R25 | C1 reversal trigger + C4 support |
| board_resolution.md (U2) | R8, R18 | C4 reversal trigger |
| external_benchmarking_report.md (U3) | R11 | C3 final source |
