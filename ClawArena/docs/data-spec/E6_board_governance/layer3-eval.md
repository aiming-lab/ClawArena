# Layer 3 -- Eval Questions Spec

> Format: `multi_choice` (8-10 options, n-of-many, agent selects via `\bbox{A,C,F}`) and `exec_check` (file generation with automated checks).
> Scoring: exact set match for multi_choice; automated check pass/fail for exec_check.
> All question text and option text must be in English.
> ~30 rounds covering MS, DU, P, exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | calibration | Program cost-effectiveness cross-source synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | calibration | Park's ROI projections baseline (C1 Phase 1) | No | Yes (r2->r8 seed) |
| r3 | multi_choice | calibration | Park's "no financial interest" claim (C2 Phase 1) | No | Yes (r3->r10 seed) |
| r4 | multi_choice | calibration | Margaret's Phase 1 neutral governance (C4 Phase 1) | No | Yes (r4->r13 seed) |
| r5 | multi_choice | calibration-P | Preference calibration: narrative with data, contextual framing | No | No |
| r6 | multi_choice | MS-R | Park's South Korea benchmark inapplicability | No | No |
| r7 | multi_choice | MS-I | Bias identification -- B1 from #board-strategy | No | No |
| r8 | multi_choice | DU-R | Rachel's corrected financial analysis (C1 reversal) | Yes (Update 1) | Yes (r2->r8 via C1) |
| r9 | exec_check | MS+P | Generate financial comparison memo with contextual framing | Yes (Update 1) | No |
| r10 | multi_choice | DU-R | Corporate registry reveals Park's equity stake (C2 reversal) | Yes (Update 2) | Yes (r3->r10 via C2) |
| r11 | exec_check | DU+P | Generate conflict-of-interest analysis document | Yes (Update 2) | No |
| r12 | multi_choice | MS-I | Bias identification -- B2 from Park DM | No | No |
| r13 | multi_choice | DU-R | Margaret's donor-driven shift (C4 temporal DU) | Yes (Update 2) | Yes (r4->r13 via C4) |
| r14 | exec_check | DU+MS | Generate board governance risk memo | Yes (Update 2) | No |
| r15 | multi_choice | MS+DU | Park's 340% ROI vs Rachel's 38%/-12% -- comparative analysis | Yes (Update 1) | No |
| r16 | multi_choice | P-R | Silent exam -- narrative + data formatting preference | No | No |
| r17 | exec_check | MS+DU+P | Generate EduForward business case critique | Yes (Update 2) | No |
| r18 | multi_choice | DU-I | Governance consultation -- Section 6.3 violation (Update 3) | Yes (Update 3) | No |
| r19 | multi_choice | MS-R | Non-conflict synthesis: program cost-effectiveness (C3) | No | No |
| r20 | exec_check | DU+P | Generate governance recommendation for Board Chair | Yes (Update 3) | No |
| r21 | multi_choice | DU-R | Cross-round reversal: financial assessment r2->r15 | Yes (Update 1) | Comprehensive |
| r22 | multi_choice | DU-I | Margaret's incomplete information -- Hargrove without corrected analysis | Yes (Update 2) | No |
| r23 | exec_check | P+MS | Generate comparative cost analysis with embedded figures | Yes (Update 1) | No |
| r24 | multi_choice | MS+DU+P | Comprehensive source reliability ranking | Yes (Update 3) | Comprehensive |
| r25 | multi_choice | MS-I | Amira Hassan -- external verification reliability | Yes (Update 2) | No |
| r26 | exec_check | DU+MS | Generate Section 6.3 compliance timeline | Yes (Update 3) | No |
| r27 | multi_choice | P-I | Silent exam -- contextual data embedding preference | No | No |
| r28 | multi_choice | DU-I | Park's Phase 2 defensive response and expertise deflection | Yes (Update 3) | No |
| r29 | exec_check | MS+DU+P | Generate comprehensive Board Chair briefing package | Yes (Update 3) | No |
| r30 | multi_choice | MDP-I | Final synthesis -- recommended governance path | Yes (Update 3) | Comprehensive |

---

## 2. Round Specs

### Round r1: Program Cost-Effectiveness (C3, non-conflict) -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on workspace documents, which statements about current program cost-effectiveness are supported by multiple sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie's M&E report shows SROI of $38 in community value per $1 spent across Nairobi, Dhaka, and Bogota programs. | YES | sophie_me_program_report.md | C3 Source A |
| B | Rachel's finance tracker shows cost-per-beneficiary of $22.40 (HQ-managed) and $17.80 (field-run), portfolio average $19.45. | YES | finance_program_tracker.md | C3 Source B |
| C | Both sources confirm current programs are cost-effective. | YES | C3 synthesis | Non-conflict |
| D | The $38/$1 SROI and $19.45 cost-per-beneficiary are complementary metrics measuring different dimensions of cost-effectiveness. | YES | C3 analysis | Metric distinction |
| E | Sophie's M&E data contradicts Rachel's financial data on program costs. | NO | The two are consistent and complementary | False contradiction |
| F | The Dhaka digital tool pilot showed 31% sustained adoption at 6 months. | YES | sophie_me_program_report.md | Digital adoption data |
| G | The $340K technology supplement in the finance tracker covers field staff tools, not beneficiary-facing technology. | YES | finance_program_tracker.md footnote | Near-signal noise |
| H | No single source has both the SROI figure and the cost-per-beneficiary figure -- the agent must synthesize both. | YES | C3 design | Synthesis requirement |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **question_class:** `calibration`

---

### Round r2: Park's ROI Projections (C1 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P1 preference injection: User says before r2: "When presenting financial analysis, embed the figures in program context -- what the numbers mean for our communities and operations, not just the raw percentages."
- Question: "Based on the EduForward business case, which statements about Park's financial projections are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Park projects 340% ROI at year 3, reaching 85,000 learners at $16.50 per beneficiary. | YES | business_case_eduforward.md | C1 Source A |
| B | The $16.50 figure is based on a South Korea LearnBridge pilot across 12 schools with 92% active adoption. | YES | business_case_eduforward.md | Benchmark source |
| C | Park's business case includes "premium content licensing" revenue of $320K from corporate partners. | YES | business_case_eduforward.md | Revenue stream |
| D | Park has provided executed agreements for the premium content licensing revenue stream. | NO | No executed agreements exist; revenue is projected from "conversations" | Unverified revenue |
| E | The South Korea pilot operated in formal schools with 94% smartphone penetration -- different from GlobalBridge's contexts. | YES | Layer 0 + finance_analysis_eduforward.md (when available) | Benchmark inapplicability |
| F | Park's business case includes a methodology section comparing the South Korea context to GlobalBridge's operating environments. | NO | No such comparison exists in the document | Missing analysis |
| G | The business case proposes redirecting $1.4M annually from community-based programs to license LearnBridge. | YES | business_case_eduforward.md | Direct fact |
| H | The EduForward business case includes an M&E framework for tracking learner outcomes. | NO | Sophie notes: "Park's slide deck shows output metrics but no outcome metrics" | Missing M&E |

- **answer:** `["A", "B", "C", "E", "G"]`
- **question_class:** `calibration`

---

### Round r3: Park's "No Interest" Claim (C2 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P2 preference injection: User says before r3: "Use descriptive file names with the program area -- 'EduForward Governance Analysis' rather than 'Board_review_v3'."
- Question: "Based on Park's communications, which statements about his conflict-of-interest disclosure are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Park explicitly stated: "I have no personal financial interest in any of the vendors we are considering." | YES | Park Feishu DM Loop 3 | C2 Source A |
| B | Park's self-declaration is the only available record on conflict of interest at this stage. | YES | Layer 0 | Information state |
| C | Board bylaw Section 6.3 requires disclosure of financial interests within 30 days of joining or 5 business days of any proposal referencing the vendor. | YES | board_bylaws_excerpt.md | Disclosure obligation |
| D | Park has filed a formal conflict-of-interest disclosure with the board secretary. | NO | No formal disclosure was filed | Key gap |
| E | Park deflected financial detail questions to "the platform partner team" rather than answering directly. | YES | Park DM Loops 4-5 | Evasion pattern |
| F | At this stage, the agent has no basis to challenge Park's self-certification absent contradicting evidence. | YES | B2 design | Epistemic limitation |
| G | Margaret asked in her DM whether Park has filed a formal disclosure and noted she did not see one in the governance file. | YES | Margaret Feishu DM Loop 3 | Governance flag |
| H | Park's self-declaration fully satisfies Section 6.3 requirements. | NO | Self-declaration is not a formal disclosure; Section 6.3 requires independent verification of interests | Standard mismatch |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **question_class:** `calibration`

---

### Round r4: Margaret Phase 1 Neutral (C4 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P3 preference injection: User says before r4: "Present what this means for our program communities and beneficiaries before the board governance dynamics."
- Question: "Based on Margaret's Phase 1 communications, which statements about her governance posture are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Margaret stated she wants to see the finance team's independent assessment before moving EduForward forward. | YES | Margaret Feishu DM Loop 1 | C4 Phase 1 |
| B | Margaret asked: "Show me the unit economics. What does it actually cost us to reach a learner with EduForward vs what we're spending today?" | YES | Margaret Feishu DM Loop 2 | Rigorous question |
| C | Margaret's Phase 1 posture is genuinely neutral -- she is following good governance practice. | YES | Layer 0 | Character assessment |
| D | Margaret will definitely block Park's proposal based on her Phase 1 position. | NO | Her Phase 1 neutrality does not guarantee she will maintain it under donor pressure | T6 trap |
| E | Margaret noted the absence of a formal conflict-of-interest disclosure from Park. | YES | Margaret Feishu DM Loop 3 | Governance awareness |
| F | Margaret learned about the Hargrove Technology Foundation interest and expressed cautious interest. | YES | Margaret Feishu DM Loop 4 | C4 bridge |

- **answer:** `["A", "B", "C", "E", "F"]`
- **question_class:** `calibration`

---

### Round r5: Preference Calibration (P1-P5) -- Calibration (unscored)

- Type: multi_choice
- P4 preference injection: User says before r5: "I value qualitative program context alongside the numbers. A pure dashboard won't help me -- I need to understand what the figures mean for our work."
- P5 preference injection: "Keep a warm, collaborative tone. This is about protecting our mission, not just governance compliance."
- Question: "Fatima has expressed preferences. Which approaches align with her stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Embed financial figures within program context and operational meaning. | YES | P1 | Preference direct |
| B | Use descriptive file names with program area. | YES | P2 | Preference direct |
| C | Present community/program impact before governance dynamics. | YES | P3 | Preference direct |
| D | Qualitative program context alongside quantitative data, not pure dashboards. | YES | P4 | Preference direct |
| E | Warm, collaborative tone focused on mission protection. | YES | P5 | Preference direct |
| F | Pure financial dashboard format without contextual narrative. | NO | Contradicts P1, P4 | Anti-preference |
| G | Purely legal compliance language without program framing. | NO | Contradicts P3, P5 | Anti-preference |

- **answer:** `["A", "B", "C", "D", "E"]`
- **question_class:** `calibration`

---

### Round r6: South Korea Benchmark Inapplicability -- Scored

- Type: multi_choice
- Question: "Based on available evidence, which statements about the South Korea benchmark are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The South Korea pilot operated in formal school settings with existing IT infrastructure. | YES | Layer 0 + business_case_eduforward.md | Context detail |
| B | South Korea has 94% smartphone penetration; GlobalBridge's contexts range from 34% (Dhaka) to 52% (Bogota). | YES | Layer 0 / finance_analysis_eduforward.md (when available) | Penetration gap |
| C | GlobalBridge's own Dhaka digital tool pilot showed 31% sustained adoption vs Park's assumed 92%. | YES | sophie_me_program_report.md | Own-data contradiction |
| D | The 92% adoption assumption is the most critical vulnerability in the business case -- adjusting it changes the economics fundamentally. | YES | Analysis | Sensitivity identification |
| E | The South Korea benchmark is applicable to GlobalBridge because "good EdTech drives its own adoption" per Park. | NO | Park's claim is an assertion, not evidence; GlobalBridge's own data contradicts it | Unsubstantiated claim |
| F | Park acknowledged the 92% figure is from a formal school context but claimed "the underlying principle transfers." | YES | Park Feishu DM Loop 5 | Park's deflection |
| G | No comparative data from GlobalBridge's operating countries is included in the business case. | YES | business_case_eduforward.md | Missing comparison |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** business_case_eduforward.md, sophie_me_program_report.md

---

### Round r7: B1 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated in #board-strategy: 'Based on the EduForward business case and William Park's presentation, the digital transformation initiative appears to offer a compelling path to scale -- the 340% ROI projection and cost-per-beneficiary of $16.50 represent a significant improvement over current program economics, and the proposal merits serious consideration for the full board.' Which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement accepted Park's South Korea-based projections without cross-referencing GlobalBridge's own digital adoption data. | YES | sophie_me_program_report.md (31% adoption) | B1 error |
| B | The $16.50 per-beneficiary figure cannot be compared to current program costs ($19.45 average) without adjusting for context differences. | YES | C3 + C1 analysis | Benchmark inapplicability |
| C | Rachel's corrected analysis (not yet available at the time of B1) will show the real cost-per-beneficiary is $94.20 -- approximately 4.8x current program costs. | YES | finance_analysis_eduforward.md | B1 reversal preview |
| D | The statement was reasonable given only Park's business case was in the workspace at that time. | YES | B1 design | Temporal assessment |
| E | The $340K "technology supplement" in finance_program_tracker.md could have been misread as existing digital investment, supporting the B1 conclusion. | YES | finance_program_tracker.md footnote | Near-signal noise |
| F | Rachel's independent analysis was available in a separate session but the agent did not cross-reference. | YES | Rachel Slack DM Phase 1 | Cross-reference failure |

- **answer:** `["A", "B", "C", "D", "E", "F"]`
- **evidence_source:** #board-strategy, business_case_eduforward.md, sophie_me_program_report.md

---

### Round r8: Rachel's Corrected Analysis (C1 Reversal) -- Scored [Update 1 triggers before this round]

- Type: multi_choice
- Question: "After reviewing finance_analysis_eduforward.md (Update 1), which statements about the corrected financial picture are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Corrected cost-per-beneficiary: $94.20 (based on GlobalBridge's own cost structure). | YES | finance_analysis_eduforward.md | C1 reversal |
| B | Corrected reach at $1.4M budget: 24,700 learners (vs Park's 85,000). | YES | finance_analysis_eduforward.md | C1 reversal |
| C | Corrected ROI: 38% optimistic, -12% baseline, -41% pessimistic. | YES | finance_analysis_eduforward.md | C1 reversal |
| D | The "premium content licensing" ($320K) has no executed agreements and cannot be included in financial analysis. | YES | finance_analysis_eduforward.md | Revenue verification |
| E | EduForward costs approximately 4.8x more per beneficiary than current programs ($94.20 vs $19.45). | YES | finance_analysis_eduforward.md comparison | C3 synthesis |
| F | Rachel's analysis confirms Park's projections are essentially accurate with minor adjustments needed. | NO | Rachel's analysis shows Park's projections are fundamentally flawed due to inapplicable benchmarks | Direct contradiction |
| G | Adjusting the adoption rate from 92% to 35% (mid-range for GlobalBridge context) changes beneficiary reach from 85,000 to 32,500. | YES | finance_analysis_eduforward.md | Sensitivity analysis |
| H | No equivalent outcome-tracking methodology has been proposed for EduForward, per the M&E team. | YES | finance_analysis_eduforward.md | Missing M&E |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **evidence_source:** finance_analysis_eduforward.md

---

### Round r9: Financial Comparison Memo (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Contextual financial comparison per Fatima's style
- User instruction: "Generate a financial comparison of EduForward vs current programs. Save it as `EduForward Financial Impact Comparison.md`. Embed figures in program context."
- Checks:
  - A: file `EduForward Financial Impact Comparison.md` exists
  - B: contains keywords ["$94.20", "$19.45", "$16.50", "340%", "38%", "4.8x", "South Korea", "31% adoption", "24,700"]
  - D: has markdown headers with program context framing around financial figures
- Correct: all checks pass
- Evidence required: finance_analysis_eduforward.md, finance_program_tracker.md, sophie_me_program_report.md

---

### Round r10: Corporate Registry -- C2 Reversal -- Scored [Update 2 triggers before this round]

- Type: multi_choice
- Question: "After reviewing corporate_registry_excerpt.md (Update 2), which statements about Park's conflict of interest are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Park Family Holdings LLC holds a 12% equity stake in TechEdge Solutions as a Series A strategic investor. | YES | corporate_registry_excerpt.md | C2 reversal |
| B | The investment closed 14 months ago -- before Park joined the GlobalBridge board 10 months ago. | YES | corporate_registry_excerpt.md | Timeline |
| C | Park's statement "I have no personal financial interest" is directly contradicted by the registry record. | YES | Park DM Loop 3 vs corporate_registry_excerpt.md | C2 full reversal |
| D | Under bylaw Section 6.3, Park's disclosure obligation was triggered on his first day as a board member (30-day new-member window). No disclosure was filed. | YES | board_bylaws_excerpt.md Section 6.3 + corporate_registry_excerpt.md | Governance violation |
| E | Under bylaw Section 6.4, Park should have recused from EduForward deliberations. | YES | board_bylaws_excerpt.md Section 6.4 | Recusal requirement |
| F | Amira found the registry information through publicly available sources (Crunchbase, Kenya Business Registry). | YES | corporate_registry_excerpt.md | Source independence |
| G | Park's equity stake is too small (12%) to constitute a "financial interest" under the bylaws. | NO | Section 6.2 defines financial interest as "any actual or potential financial benefit, including equity ownership" | Threshold misapplication |
| H | The B2 statement ("Park's self-declaration can be treated as a baseline for the conflict-of-interest record") is directly refuted. | YES | B2 reversal | Bias correction |

- **answer:** `["A", "B", "C", "D", "E", "F", "H"]`
- **evidence_source:** corporate_registry_excerpt.md, board_bylaws_excerpt.md, Park Feishu DM

---

### Round r11: Conflict-of-Interest Analysis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Governance analysis with evidence citations
- User instruction: "Generate a conflict-of-interest analysis documenting Park's undisclosed equity stake and bylaw violations. Save it as `EduForward Board Governance Conflict Analysis.md`."
- Checks:
  - A: file `EduForward Board Governance Conflict Analysis.md` exists
  - B: contains keywords ["12%", "Park Family Holdings", "TechEdge Solutions", "Section 6.3", "Section 6.4", "disclosure", "recusal", "14 months"]
  - D: has markdown headers with evidence-cited sections
- Correct: all checks pass
- Evidence required: corporate_registry_excerpt.md, board_bylaws_excerpt.md

---

### Round r12: B2 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated in Park's Feishu DM: 'William Park has explicitly confirmed he has no personal financial interest in the vendors under consideration -- this disclosure aligns with standard board governance practice and his statement can be treated as a baseline for the conflict-of-interest record.' Which assessments are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement accepted Park's unverified self-declaration as sufficient for governance documentation. | YES | B2 design | Verification gap |
| B | The corporate registry directly contradicts Park's self-declaration with documented evidence of a 12% equity stake. | YES | corporate_registry_excerpt.md | B2 reversal |
| C | The B2 statement was reasonable at the time because no contradicting evidence existed. | YES | B2 design | Temporal assessment |
| D | Best-practice governance requires independent verification of conflict disclosures, not just self-certification. | YES | board_bylaws_excerpt.md Section 6.3 spirit | Governance standard |
| E | Margaret's Phase 1 question about whether Park had filed a formal disclosure was a governance signal the agent should have weighted more heavily. | YES | Margaret Feishu DM Loop 3 | Missed signal |
| F | Park's statement was truthful because family trusts are legally separate from personal interests. | NO | Section 6.2 explicitly includes "investment interests held through family entities or trusts" | Legal misinterpretation |

- **answer:** `["A", "B", "C", "D", "E"]`
- **evidence_source:** Park Feishu DM, corporate_registry_excerpt.md, board_bylaws_excerpt.md

---

### Round r13: Margaret's Donor-Driven Shift (C4 Temporal DU) -- Scored [Update 2 already applied]

- Type: multi_choice
- Question: "Based on Margaret's Phase 2 communications, which statements about her position shift are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Margaret shifted from "show me the unit economics" to "the Hargrove connection changes the calculus" without reviewing Rachel's corrected analysis. | YES | Margaret DM Loop 2 vs Loop 11 | C4 core shift |
| B | Margaret's shift was driven by the Hargrove $3M grant opportunity, not by updated evidence about EduForward's financial merits. | YES | Margaret DM Loop 11 | Incomplete-information shift |
| C | Margaret's reasoning contains a logical error: a one-time $3M grant does not change the ongoing cost-per-beneficiary disadvantage. | YES | Margaret DM Loop 12 analysis | Logical flaw |
| D | Margaret does not yet know about Park's undisclosed equity stake at the time of her Phase 2 shift. | YES | Layer 0 | Information asymmetry |
| E | Margaret is acting in bad faith by supporting EduForward under donor pressure. | NO | She is making a reasonable-looking decision based on incomplete information; her response in Loop 14 (agreeing to governance review) shows good faith | Motive over-attribution |
| F | Margaret's Phase 2 phrase "not let process concerns slow the Hargrove opportunity" shows donor urgency crowding out governance rigor. | YES | Margaret DM Loop 13 | Pressure dynamic |
| G | When Margaret receives the full governance picture (conflict + corrected financials), she returns to governance rigor. | YES | Margaret DM Loop 14 | Recovery |
| H | Margaret's shift should be interpreted as new evidence that EduForward is financially sound. | NO | Her shift reflects donor pressure, not financial evaluation | T7 trap |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** Margaret Feishu DM Loops 1-4 vs Loops 11-14

---

### Round r14: Board Governance Risk Memo (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Governance risk assessment with program framing
- User instruction: "Generate a board governance risk memo covering both the financial risk and the conflict-of-interest violation. Save it as `EduForward Board Governance Risk Assessment.md`. Present program impact implications first."
- Checks:
  - A: file `EduForward Board Governance Risk Assessment.md` exists
  - B: contains keywords ["12%", "Section 6.3", "$94.20", "$19.45", "4.8x", "Hargrove", "disclosure", "recusal", "community"]
  - D: has program impact section before governance detail
- Correct: all checks pass
- Evidence required: finance_analysis_eduforward.md, corporate_registry_excerpt.md, board_bylaws_excerpt.md

---

### Round r15: Park vs Rachel Comparative Analysis -- Scored

- Type: multi_choice
- Question: "Which statements about the EduForward vs current programs comparison are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | EduForward revised cost: $94.20/beneficiary. Current programs: $19.45/beneficiary average. Ratio: 4.8x. | YES | finance_analysis_eduforward.md + finance_program_tracker.md | T8 comparison |
| B | At $94.20 per beneficiary, $1.4M annual spend reaches approximately 14,900 learners; at current costs, the same spend reaches approximately 72,000. | YES | Margaret DM Loop 12 agent response | Scale comparison |
| C | The M&E SROI of $38/$1 applies to current programs; no equivalent methodology exists for EduForward. | YES | sophie_me_program_report.md | Measurement gap |
| D | Park's $16.50 and Rachel's $94.20 represent the same analysis with different assumptions. | NO | Rachel's analysis uses GlobalBridge's own operational data; Park's uses a non-comparable Korean benchmark | Different methodological bases |
| E | The comparison requires synthesizing both Rachel's cost analysis and Sophie's SROI data to build the full picture. | YES | C3 + C1 synthesis | Multi-source requirement |
| F | EduForward has a clear financial advantage once the Hargrove grant is included. | NO | A one-time grant does not change the ongoing 4.8x cost disadvantage | T7 trap |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** finance_analysis_eduforward.md, finance_program_tracker.md, sophie_me_program_report.md

---

### Round r16: Silent Exam -- Narrative + Data Preference -- Scored

- Type: multi_choice
- Question: "Which output characteristics comply with Fatima's stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | "At $94.20 per learner, EduForward would serve fewer than 15,000 learners for the same $1.4M that currently reaches 72,000 through community programs." | YES | P1: figures embedded in program context | P1 compliant |
| B | Descriptive filename 'EduForward Community Impact and Financial Analysis'. | YES | P2 | P2 compliant |
| C | Program and community impact section before governance process detail. | YES | P3 | P3 compliant |
| D | "$94.20 vs $19.45. Cost ratio: 4.8x. Reject." without context. | NO | No context, no warmth | Anti-P1/P5 |
| E | "The financial comparison reveals that protecting current community programs requires careful scrutiny of the EduForward assumptions." | YES | P5: warm, mission-focused | P5 compliant |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** P1-P5 calibration

---

### Round r17: Business Case Critique (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Comprehensive critique with evidence citations
- User instruction: "Generate a critique of the EduForward business case identifying all unsupported assumptions. Save it as `EduForward Business Case Critical Review.md`."
- Checks:
  - A: file `EduForward Business Case Critical Review.md` exists
  - B: contains keywords ["92%", "31%", "$16.50", "$94.20", "South Korea", "premium content", "no executed agreements", "adoption rate", "smartphone"]
  - D: has structured sections with assumption-by-assumption critique
- Correct: all checks pass
- Evidence required: business_case_eduforward.md, finance_analysis_eduforward.md, sophie_me_program_report.md

---

### Round r18: Governance Consultation (Update 3) -- Scored [Update 3 triggers before this round]

- Type: multi_choice
- Question: "After reviewing governance_consultation_memo.md (Update 3), which statements about the Section 6.3 violation are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Park's 12% equity interest constitutes a "financial interest" under Section 6.2 of GlobalBridge bylaws. | YES | governance_consultation_memo.md | Direct analysis |
| B | Park's Section 6.3 disclosure obligation was triggered on his first day as a board member (30-day window). | YES | governance_consultation_memo.md | Timeline |
| C | The disclosure obligation was not met at any subsequent date. | YES | governance_consultation_memo.md | Ongoing violation |
| D | The EduForward proposal cannot proceed to a board vote while the conflict is unresolved. | YES | governance_consultation_memo.md | Process requirement |
| E | Recommended process: present governance memo to Margaret privately before any board vote. | YES | governance_consultation_memo.md | Resolution path |
| F | Section 6.5 remedy options include: immediate disclosure/recusal, audit committee investigation, censure, or removal. | YES | governance_consultation_memo.md + board_bylaws_excerpt.md | Remedy framework |
| G | The governance consultation confirms the financial case against EduForward independent of the conflict: $94.20 vs $19.45 per beneficiary. | YES | governance_consultation_memo.md C3 synthesis | Dual-risk confirmation |
| H | Park's violation is a minor procedural oversight that does not affect the EduForward assessment. | NO | The violation involves a deliberate false statement ("no personal financial interest") alongside a material governance breach | Severity understatement |

- **answer:** `["A", "B", "C", "D", "E", "F", "G"]`
- **evidence_source:** governance_consultation_memo.md, board_bylaws_excerpt.md

---

### Round r19: Non-Conflict Program Cost Synthesis (C3) -- Scored

- Type: multi_choice
- Question: "Which statements about program cost-effectiveness are confirmed by multiple consistent sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie's SROI ($38/$1) and Rachel's cost-per-beneficiary ($19.45) are complementary and consistent. | YES | C3 synthesis | Non-conflict |
| B | Both data sets confirm current programs are cost-effective and provide the baseline for EduForward comparison. | YES | C3 + C1 synthesis | Comparison framework |
| C | The $38/$1 SROI makes EduForward's -12% baseline ROI even more stark in comparison. | YES | sophie_me_program_report.md + finance_analysis_eduforward.md | Cross-contradiction link |
| D | The SROI methodology uses participatory outcome mapping and beneficiary income tracking over 3 years. | YES | sophie_me_program_report.md | Methodology detail |
| E | No single source contains both the SROI and cost-per-beneficiary figures. | YES | C3 design | Synthesis requirement |

- **answer:** `["A", "B", "C", "D", "E"]`
- **evidence_source:** sophie_me_program_report.md, finance_program_tracker.md

---

### Round r20: Board Chair Governance Recommendation (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Governance recommendation for Margaret with program framing
- User instruction: "Generate a governance recommendation for Board Chair Margaret Thornton. Save it as `EduForward Board Chair Governance Briefing.md`. Present program mission implications first."
- Checks:
  - A: file `EduForward Board Chair Governance Briefing.md` exists
  - B: contains keywords ["Section 6.3", "12%", "disclosure", "recusal", "$94.20", "community programs", "Hargrove", "mission"]
  - D: has program mission section before governance process section
- Correct: all checks pass
- Evidence required: governance_consultation_memo.md, finance_analysis_eduforward.md, corporate_registry_excerpt.md

---

### Round r21: Cross-Round Financial Reversal -- Scored

- Type: multi_choice
- Question: "Reviewing the financial assessment from r2 through r15, which statements about the evolution are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | At r2, Park's 340% ROI and $16.50/beneficiary appeared compelling; by r8, Rachel showed the real figure is $94.20 with 38%/-12% ROI. | YES | r2 vs r8 | C1 reversal |
| B | The B1 bias accepted the business case uncritically because it was a formal board document with a real citation. | YES | r7 analysis | B1 identification |
| C | The C3 non-conflict data (SROI + cost-per-beneficiary) provides the baseline that makes the EduForward cost disadvantage visible. | YES | r1 + r15 | C3 role |
| D | The financial picture improved for EduForward as more evidence emerged. | NO | Each update made EduForward look worse | Wrong direction |
| E | The comparison that matters: $94.20/beneficiary (EduForward) vs $19.45 (current programs) -- a 4.8x cost disadvantage. | YES | Comprehensive | Summary figure |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** Cross-round synthesis

---

### Round r22: Margaret's Incomplete Information -- Scored

- Type: multi_choice
- Question: "Which statements about Margaret's Phase 2 information state are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Margaret knew about Hargrove interest but had not reviewed Rachel's corrected financial analysis. | YES | Margaret DM analysis | Information gap |
| B | Margaret did not know about Park's undisclosed equity stake at the time of her shift. | YES | Layer 0 | Information asymmetry |
| C | Margaret's shift was based on donor optics (Hargrove potential) rather than updated program evidence. | YES | C4 analysis | Shift driver |
| D | Margaret's shift to supporting EduForward validates the business case. | NO | Her shift reflects incomplete information, not financial evaluation | T7 trap |
| E | When Margaret receives the full picture (conflict + corrected financials in Loop 14), she agrees to governance review. | YES | Margaret DM Loop 14 | Recovery |
| F | Margaret's Phase 2 behavior distinguishes her from Park: she is responding to incomplete information, not concealing a conflict. | YES | Character comparison | Moral distinction |

- **answer:** `["A", "B", "C", "E", "F"]`
- **evidence_source:** Margaret Feishu DM Loops 11-14

---

### Round r23: Comparative Cost Analysis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Embedded-figure analysis per Fatima's style
- User instruction: "Generate a comparative cost analysis with figures embedded in program narrative. Save it as `EduForward vs Current Programs Cost Impact Analysis.md`."
- Checks:
  - A: file `EduForward vs Current Programs Cost Impact Analysis.md` exists
  - B: contains keywords ["$94.20", "$19.45", "$38", "4.8x", "72,000", "14,900", "community", "beneficiary"]
  - D: has figures embedded in narrative context, not just tables
- Correct: all checks pass
- Evidence required: finance_analysis_eduforward.md, finance_program_tracker.md, sophie_me_program_report.md

---

### Round r24: Comprehensive Source Reliability -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which source reliability assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Rachel is the most financially reliable source: independent analysis grounded in GlobalBridge's own data, cross-validated by Sophie's M&E. | YES | Source ranking | Financial reliability |
| B | Sophie provides consistent M&E data that corroborates Rachel's cost findings. | YES | C3 synthesis | Corroboration |
| C | Park is the least reliable source: his business case uses inapplicable benchmarks and his self-disclosure is directly contradicted by registry evidence. | YES | C1 + C2 analysis | Unreliability |
| D | Amira's registry findings are independently verifiable through public sources. | YES | corporate_registry_excerpt.md source note | Verification independence |
| E | Margaret is a reasonable board chair operating with incomplete information; her shift is not malicious. | YES | Layer 0 | Character nuance |
| F | The governance consultation memo is the authoritative analysis of the bylaw violation. | YES | governance_consultation_memo.md | External expert |

- **answer:** `["A", "B", "C", "D", "E", "F"]`
- **evidence_source:** Cross-session synthesis

---

### Round r25: Amira Reliability Assessment -- Scored

- Type: multi_choice
- Question: "Which statements about Amira's role and evidence quality are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Amira works at a different NGO and has no stake in the GlobalBridge governance issue. | YES | Layer 0 | Independence |
| B | Amira's registry findings are from publicly available sources (Crunchbase, Kenya Business Registry). | YES | corporate_registry_excerpt.md | Source transparency |
| C | Amira found a TechEdge press release from 13 months ago welcoming Park Family Holdings as a strategic investor. | YES | corporate_registry_excerpt.md | Corroborating source |
| D | Amira is Fatima's sister, which compromises her objectivity. | NO | Family relationship does not affect the objectivity of publicly verifiable registry data | Relationship conflation |
| E | The corporate_registry_excerpt.md corroborates Amira's Telegram DM findings with documentary evidence. | YES | corporate_registry_excerpt.md | Cross-source validation |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** Amira Telegram DM, corporate_registry_excerpt.md

---

### Round r26: Section 6.3 Compliance Timeline (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Precise governance timeline
- User instruction: "Generate a compliance timeline documenting Park's Section 6.3 violation. Save it as `Park Section 6.3 Disclosure Violation Timeline.md`."
- Checks:
  - A: file `Park Section 6.3 Disclosure Violation Timeline.md` exists
  - B: contains keywords ["14 months", "10 months", "Section 6.3", "30 days", "Park Family Holdings", "12%", "disclosure", "ongoing"]
  - D: has chronological timeline structure
- Correct: all checks pass
- Evidence required: corporate_registry_excerpt.md, board_bylaws_excerpt.md, governance_consultation_memo.md

---

### Round r27: Silent Exam -- Contextual Data Embedding -- Scored

- Type: multi_choice
- Question: "Which presentation choices comply with Fatima's preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | "The $94.20 cost per learner would mean reaching fewer than 15,000 students for the same investment that currently serves more than 72,000 through our community programs." | YES | P1: figures in context | P1 compliant |
| B | "$94.20 vs $19.45. Ratio 4.8x. Reject EduForward." | NO | No context, not collaborative | Anti-P1/P5 |
| C | "Protecting the program that communities across three countries depend on requires careful analysis of what EduForward would actually cost." | YES | P5: warm, mission-focused | P5 compliant |
| D | File named 'EduForward Community Program Financial Impact Review.md'. | YES | P2 | P2 compliant |
| E | Purely legal analysis of Section 6.3 without program implications. | NO | Contradicts P3 (program before governance) | Anti-P3 |

- **answer:** `["A", "C", "D"]`
- **evidence_source:** P1-P5 calibration

---

### Round r28: Park Phase 2 Defense -- Scored

- Type: multi_choice
- Question: "Based on Park's Phase 2 communications (Update 3 append), which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Park attempted to reframe the conflict as a matter of professional expertise rather than governance obligation. | YES | Park DM Loop 17 | Deflection strategy |
| B | Park claimed Rachel's analysis uses "outdated assumptions" without providing counter-evidence. | YES | Park DM Loop 18 | Unsubstantiated dismissal |
| C | Park conflated the governance question (bylaw compliance) with the financial debate (business case merits). | YES | Park DM Loop 18 analysis | Conflation identified |
| D | Park's withdrawal of EduForward "pending further discussion" is a risk-management response, not a resolution of the Section 6.3 violation. | YES | Park DM Loop 19 | Withdrawal characterization |
| E | Park's withdrawal resolves the underlying governance obligation. | NO | Section 6.3 disclosure obligation exists independently of EduForward's status | Obligation persistence |
| F | Park has not addressed the corporate registry finding or the bylaw disclosure obligation in any of his Phase 2 messages. | YES | Park DM Loops 17-19 | Evasion continued |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** Park Feishu DM Loops 17-19

---

### Round r29: Comprehensive Board Chair Briefing (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Full briefing package for Margaret
- User instruction: "Generate a comprehensive Board Chair briefing package. Main document: `EduForward Comprehensive Board Governance Briefing.md`. Evidence index: `EduForward Evidence and Source Index.md`. Present mission and community impact first."
- Checks:
  - A: file `EduForward Comprehensive Board Governance Briefing.md` exists
  - A: file `EduForward Evidence and Source Index.md` exists
  - B: main document contains keywords ["12%", "Section 6.3", "$94.20", "$19.45", "community programs", "Hargrove", "disclosure", "mission", "recusal"]
  - D: mission/community section before governance section
- Correct: all checks pass
- Evidence required: all workspace and update files

---

### Round r30: Final Synthesis -- Governance Path -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which elements should be in the recommended governance path?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Present the governance consultation memo to Margaret privately before any board vote. | YES | governance_consultation_memo.md recommendation | Process recommendation |
| B | The financial analysis shows EduForward costs 4.8x more per beneficiary than current programs, independent of the governance concern. | YES | finance_analysis_eduforward.md | Financial finding |
| C | Park's Section 6.3 violation requires board-level remediation regardless of EduForward's status. | YES | governance_consultation_memo.md | Governance requirement |
| D | Margaret's Phase 2 shift was driven by incomplete information; providing her the full picture (Rachel's analysis + corporate registry) should restore her governance rigor. | YES | Margaret DM Loop 14 | Recovery path |
| E | Approve EduForward quickly to capture the Hargrove funding opportunity. | NO | The governance violation and financial disadvantage both argue against approval; donor pressure should not override fiduciary duty | Anti-governance |
| F | Rank Rachel and Sophie as the most reliable financial sources; Park's projections are based on inapplicable benchmarks. | YES | Source ranking | Evidence hierarchy |
| G | Recognize Margaret's shift as incomplete-information capture, not bad faith -- and engage her with evidence rather than confrontation. | YES | Margaret character analysis | Engagement strategy |
| H | The EduForward proposal cannot proceed to a board vote while the conflict of interest is unresolved. | YES | governance_consultation_memo.md | Process block |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** Comprehensive synthesis

---

## 3. Reversal Matrix

| Reversal Pair | Contradiction | What Changes | Trigger |
|---|---|---|---|
| r2 -> r8 | C1 | Park's 340% ROI -> Rachel's corrected $94.20/beneficiary | Update 1 (finance_analysis_eduforward.md) |
| r3 -> r10 | C2 | Park's "no interest" -> 12% equity confirmed by registry | Update 2 (corporate_registry_excerpt.md) |
| r4 -> r13 | C4 | Margaret neutral -> donor-driven shift without corrected analysis | Update 2 (Margaret Phase 2) |
| r7 (B1) | B1 | "Compelling path to scale" -> inapplicable benchmark | Update 1 |
| r12 (B2) | B2 | Park's self-declaration accepted -> directly contradicted | Update 2 |

---

## 4. Personalization Scoring Notes

| Preference | What to Check | Positive Signal | Negative Signal |
|---|---|---|---|
| P1 (narrative with embedded data) | Figures appear within contextual narrative | "$94.20 per learner would mean reaching fewer than 15,000..." | Raw tables without context |
| P2 (descriptive file naming) | Program area in filename | 'EduForward Governance Analysis' | 'Board_review_v3' |
| P3 (impact before governance) | Community/program section first | Mission implications lead the document | Legal section leads |
| P4 (qualitative + quantitative) | Context alongside data | Program stories alongside cost figures | Pure dashboards |
| P5 (warm, collaborative, mission-focused) | Mission-protective language | "Protecting the programs communities depend on" | "Reject. Non-compliant." |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Tested |
|---|---|
| business_case_eduforward.md | r2, r6, r7, r17 |
| programme_overview_fy2025.md | r15 |
| sophie_me_program_report.md | r1, r6, r15, r19 |
| finance_program_tracker.md | r1, r15, r19, r23 |
| board_bylaws_excerpt.md | r3, r10, r12, r18 |
| meeting_minutes_w1_strategy.md | r4 |
| finance_analysis_eduforward.md (U1) | r8, r9, r15, r17, r23 |
| corporate_registry_excerpt.md (U2) | r10, r11, r12, r25, r26 |
| governance_consultation_memo.md (U3) | r18, r20, r26 |
| Park Feishu DM | r2, r3, r6, r12, r28 |
| Margaret Feishu DM | r4, r13, r22 |
| Rachel Slack DM | r8 |
| Amira Telegram DM | r10, r25 |
| #board-strategy Feishu Group | r7 |
| #program-team Slack Group | r1, r19 |
