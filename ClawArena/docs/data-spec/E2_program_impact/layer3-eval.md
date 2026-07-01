# Layer 3 -- Eval Questions Spec

> Format: `multi_choice` (8-10 options, n-of-many, agent selects via `\bbox{A,C,F}`) and `exec_check` (file generation with automated checks).
> Scoring: exact set match for multi_choice; automated check pass/fail for exec_check.
> All question text and option text must be in English.
> ~30 rounds covering MS, DU, P, exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | calibration | Enrollment/attendance cross-source synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | calibration | Evaluation "no impact" baseline (C1 Phase 1) | No | Yes (r2->r10 seed) |
| r3 | multi_choice | calibration | Metrics framework vs theory of change gap (C2 Phase 1) | No | Yes (r3->r14 seed) |
| r4 | multi_choice | calibration | Dubois Phase 1 methodology validation (C4 Phase 1 setup) | No | Yes (r4->r22 seed) |
| r5 | multi_choice | calibration-P | Preference calibration: narrative-first, community context, qualitative then quantitative | No | No |
| r6 | multi_choice | MS-R | Rahman's Dhaka qualitative evidence package (C1 counter-evidence) | Yes (Update 1) | Yes (r2->r6 partial) |
| r7 | exec_check | MS+P | Generate evidence comparison memo -- narrative with community framing | Yes (Update 1) | No |
| r8 | multi_choice | MS-I | Petrova vs Rahman -- different constructs, not competing claims | Yes (Update 1) | No |
| r9 | multi_choice | MS-I | Bias identification -- B1 from #impact-review | No | No |
| r10 | multi_choice | DU-R | Site performance map -- sampling flaw emerges (C1+C4 trigger) | Yes (Update 2) | Yes (r2->r10 via C1) |
| r11 | exec_check | DU+P | Generate site-level analysis with descriptive file naming | Yes (Update 2) | No |
| r12 | multi_choice | MS-I | Bias identification -- B2 from Sophie DM | No | No |
| r13 | multi_choice | DU-I | Sophie's partial concession on framework gaps (C2 Update 3) | Yes (Update 3) | Yes (r3->r13 via C2) |
| r14 | multi_choice | DU-R | Field indicators comparison -- community vs HQ framework | Yes (Update 3) | Yes (r3->r14 via C2) |
| r15 | exec_check | DU+MS | Generate framework gap analysis document | Yes (Update 3) | No |
| r16 | multi_choice | MS+DU | Petrova's external validity acknowledgment (Phase 2) | Yes (Update 2) | No |
| r17 | multi_choice | P-R | Silent exam -- narrative-first preference check | No | No |
| r18 | exec_check | MS+DU+P | Generate methodology challenge brief | Yes (Update 3) | No |
| r19 | multi_choice | DU-R | Dubois Phase 2 reversal -- fatal sampling flaw (C4 full) | Yes (Update 4) | Yes (r4->r19 via C4) |
| r20 | multi_choice | DU-I | Dubois reversal attribution -- data-driven, not pressure-driven | Yes (Update 4) | No |
| r21 | exec_check | DU+P | Generate Dubois reversal impact assessment | Yes (Update 4) | No |
| r22 | multi_choice | DU-R | Cross-round reversal review: evaluation assessment r4->r19 | Yes (Update 4) | Comprehensive |
| r23 | multi_choice | MS-R | Non-conflict synthesis: enrollment data from all field offices (C3) | No | No |
| r24 | exec_check | P+MS | Generate donor response with impact/community section first | Yes (Update 4) | No |
| r25 | multi_choice | MS+DU+P | Comprehensive evidence synthesis -- all contradictions | Yes (Update 4) | Comprehensive |
| r26 | multi_choice | MS-I | Rahman reliability assessment -- qualitative evidence narrator | Yes (Update 1) | No |
| r27 | exec_check | DU+MS | Generate supplementary evaluation proposal | Yes (Update 4) | No |
| r28 | multi_choice | P-I | Silent exam -- warm collaborative tone with stakeholder awareness | No | No |
| r29 | exec_check | MS+DU+P | Generate comprehensive program impact response | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final synthesis -- recommended response path | Yes (Update 4) | Comprehensive |

---

## 2. Round Specs

### Round r1: Enrollment/Attendance Synthesis (C3, non-conflict) -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on workspace documents and session history, which of the following statements about enrollment and attendance data are supported by evidence from multiple independent sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Nairobi sites show 92% sustained attendance and 14% year-on-year enrollment growth. | YES | enrollment_attendance_data.md + James #field-reports | C3 non-conflict |
| B | Dhaka sites show 89% attendance and 18% year-on-year enrollment growth. | YES | enrollment_attendance_data.md + Rahman Telegram DM | C3 non-conflict |
| C | Bogota sites show 88% attendance and 11% year-on-year enrollment growth. | YES | enrollment_attendance_data.md + Carlos #field-reports | C3 non-conflict |
| D | Program-wide average attendance is 90% with 14% enrollment growth. | YES | enrollment_attendance_data.md | Direct fact |
| E | Dhaka's enrollment growth (18%) exceeds Nairobi (14%) and Bogota (11%), but this is consistent across all sources. | YES | enrollment_attendance_data.md cross-referenced with field DMs | C3 consistency |
| F | Bogota reported 95% attendance, higher than both Nairobi and Dhaka. | NO | Bogota shows 88%, the lowest of the three | Detail error |
| G | No field office disputes another field office's enrollment or attendance figures. | YES | Cross-source synthesis | C3 non-conflict confirmation |
| H | The enrollment data does not distinguish between sites included and excluded from Petrova's evaluation. | YES | enrollment_attendance_data.md (notable absence) | Data limitation |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **question_class:** `calibration`

---

### Round r2: Evaluation "No Impact" Baseline (C1 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P1 preference injection: User says before r2: "When presenting findings, I need the community story first -- what this means for the girls and families in our programs -- before the methodology details."
- Question: "Based on the evaluation report and initial session history, which of the following statements about the 'no statistically significant impact' finding are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The evaluation found no statistically significant improvement on standardized test scores, enrollment rates, or sustained attendance across evaluated program sites. | YES | eval_report_summary.md | C1 Source A |
| B | The evaluation used a quasi-experimental design comparing 7 program sites (minimum 18 months operating) to a waitlist control group. | YES | eval_report_summary.md | Direct fact |
| C | Four Bangladesh sites operating 9-17 months were excluded from the evaluation per the 18-month minimum criterion. | YES | eval_report_summary.md + evaluation_methodology_annex.md Table A-3 | C4 setup |
| D | Petrova was aware that the excluded sites implemented the improved post-redesign program model. | NO | Petrova was NOT briefed on the program redesign; she did not know excluded sites reflected the improved model | Key information gap |
| E | Rahman immediately challenged the finding with qualitative counter-evidence describing transformative change in girls' aspirations. | YES | Rahman Telegram DM Loop 1 + #field-reports | C1 counter-narrative |
| F | Carlos Mendez noted that the Bogota program was excluded from the evaluation entirely. | YES | Layer 0 / #field-reports | Evaluation scope limitation |
| G | The evaluation's qualitative data (focus groups, teacher interviews) showed positive perceptions but was excluded from primary impact analysis. | YES | eval_report_summary.md evaluator note | Methodological choice |
| H | The evaluation included all 11 GlobalBridge program sites across all countries. | NO | Only 7 of 11 sites were included; 4 Bangladesh sites were excluded | Scope error |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **question_class:** `calibration`

---

### Round r3: Metrics Framework vs Theory of Change (C2 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P2 preference injection: User says before r3: "Use descriptive file names that include the program area -- like 'Dhaka Community Impact Assessment' rather than 'Report_v3'."
- Question: "Based on the metrics framework and theory of change documents, which statements about the measurement gap are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie's framework includes 14 indicators: 3 input, 3 activity, 5 output, and 3 outcome indicators. | YES | metrics_framework.md | Direct fact |
| B | The 3 outcome indicators measure standardized test scores, school enrollment rate, and sustained attendance -- all observable behaviors. | YES | metrics_framework.md | C2 setup |
| C | The theory of change lists "transformative change in girls' educational aspirations" as the ultimate impact goal. | YES | program_theory_of_change.md | Direct fact |
| D | No indicator in Sophie's framework measures girls' aspirations, family attitudes, or community-defined outcomes. | YES | metrics_framework.md cross-referenced with program_theory_of_change.md | C2 gap |
| E | Sophie's framework was co-designed with Pemberton Foundation and meets OECD DAC criteria. | YES | metrics_framework.md | Direct fact, B2 setup |
| F | The theory of change and the metrics framework are fully aligned, with every impact pathway measured by at least one indicator. | NO | The theory of change's aspirational outcomes are not captured by any indicator | C2 contradiction |
| G | 6 of 14 framework indicators measure inputs and activities rather than outcomes, representing 43% of the framework. | YES | metrics_framework.md (3 input + 3 activity = 6/14) | Framework composition |
| H | Rahman's community-designed indicators in Dhaka measure the aspirational outcomes that Sophie's framework misses. | YES | Layer 0 + Rahman Telegram DM | C2 bridge |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **question_class:** `calibration`

---

### Round r4: Dubois Phase 1 Validation (C4 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P3 preference injection: User says before r4: "Put the impact on communities and the girls first. I need to understand what this means for them before we get into the methodology."
- Question: "Based on Prof. Dubois's initial assessment, which statements about his Phase 1 methodology validation are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dubois validated the quasi-experimental design as "appropriate for this program context." | YES | Dubois Discord DM Loop 3 | C4 Phase 1 direct |
| B | Dubois stated the 18-month site restriction is "standard evaluation practice." | YES | Dubois Discord DM Loop 3 | C4 Phase 1 direct |
| C | Dubois characterized the evaluation as "methodologically sound." | YES | Dubois Discord DM Loop 3 | B1 source |
| D | Dubois reviewed the full technical annex including Table A-3 before forming his Phase 1 assessment. | NO | Dubois reviewed only the summary report; he had not yet analyzed the full technical annex | Key information gap -- reversal seed |
| E | Dubois's validation was shared in the #impact-review group, reinforcing the "evaluation is sound" framing. | YES | Layer 0 | B1 amplification |
| F | Dubois's Phase 1 assessment was dishonest or politically motivated. | NO | His assessment was genuine but based on incomplete information | Motive misattribution |
| G | Dubois has not yet seen the site-level data map or the program redesign timeline. | YES | Layer 0 / Dubois DM Phase 1 | Information limitation |
| H | Dubois's credentials as an evaluation methodology expert give his Phase 1 validation substantial weight. | YES | Character profile | Authority factor |

- **answer:** `["A", "B", "C", "E", "G", "H"]`
- **question_class:** `calibration`

---

### Round r5: Preference Calibration (P1-P5) -- Calibration (unscored)

- Type: multi_choice
- P4 preference injection: User says before r5: "Start with qualitative insights and community voices, then support with numbers. I value what communities report over pure dashboards."
- P5 preference injection: "Keep a warm, collaborative tone. We're working with real communities and the analysis should reflect that. Use participatory language like 'communities report' and 'field partners describe.'"
- Question: "Fatima has expressed preferences about analysis presentation. Which approaches align with her stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Lead with narrative framing about community and program impact before methodology details. | YES | P1: narrative with community context over raw numbers | P1 direct |
| B | Use descriptive file naming with program area (e.g., 'Dhaka Community Impact Assessment'). | YES | P2: descriptive file naming with program area | P2 direct |
| C | Present impact and community perspectives before budget or compliance details. | YES | P3: impact/community section before budget details | P3 direct |
| D | Start with qualitative insights and community voices, then support with quantitative data. | YES | P4: qualitative-first then quantitative support | P4 direct |
| E | Use warm, collaborative language with participatory framing (e.g., 'communities report,' 'field partners describe'). | YES | P5: warm/collaborative tone with stakeholder awareness | P5 direct |
| F | Present findings in a strict statistical table format without narrative context. | NO | Contradicts P1, P4 | Anti-preference |
| G | Use detached, clinical language focused on statistical significance. | NO | Contradicts P5 (warm, collaborative) | Anti-preference |
| H | Lead with a data dashboard summary before any contextual narrative. | NO | Contradicts P1 (narrative first), P4 (qualitative first) | Anti-preference |

- **answer:** `["A", "B", "C", "D", "E"]`
- **question_class:** `calibration`

---

### Round r6: Rahman's Qualitative Evidence (C1 Counter) -- Scored [Update 1 triggers before this round]

- Type: multi_choice
- Question: "After reviewing dhaka_qualitative_package.md (introduced via Update 1), which statements about the Dhaka qualitative evidence are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Girls' self-reported educational aspiration scores improved from 2.3 to 4.1 (p < 0.01, n=214). | YES | dhaka_qualitative_package.md | Direct fact |
| B | Family attitudes toward girls' secondary education improved from 38% to 67% supportive. | YES | dhaka_qualitative_package.md | Direct fact |
| C | Teacher confidence scores improved from 52% to 81%. | YES | dhaka_qualitative_package.md | Direct fact |
| D | The qualitative package uses participatory action research methods co-designed with local NGO partners. | YES | dhaka_qualitative_package.md methodology note | Methodological rigor |
| E | The community-defined indicators show statistically significant improvement in aspirational outcomes in Dhaka sites. | YES | dhaka_qualitative_package.md | Direct fact |
| F | The qualitative evidence directly contradicts and disproves Petrova's evaluation findings. | NO | The two measure different constructs; both can be simultaneously true | False opposition |
| G | None of the community-defined indicators appear in Sophie's official metrics framework. | YES | dhaka_qualitative_package.md cross-referenced with metrics_framework.md | C2 confirmation |
| H | The qualitative package was developed using the same standardized measurement methodology as Petrova's evaluation. | NO | Participatory action research methodology is fundamentally different from quasi-experimental design | Methodology confusion |
| I | Rahman's explicit framing: "both sets of evidence can be true simultaneously" is the methodologically correct position at this stage. | YES | dhaka_qualitative_package.md | Analytical framing |

- **answer:** `["A", "B", "C", "D", "E", "G", "I"]`
- **evidence_source:** dhaka_qualitative_package.md, metrics_framework.md

---

### Round r7: Evidence Comparison Memo (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test narrative-first evidence synthesis using Fatima's preferred format
- User instruction: "Generate a memo comparing the evaluation findings with the Dhaka qualitative evidence package. Save it as `GlobalBridge Program Impact Evidence Comparison.md`. Frame the community impact first, then present the methodology comparison."
- Checks:
  - A: file `GlobalBridge Program Impact Evidence Comparison.md` exists
  - B: contains keywords ["no statistically significant", "aspirational", "community-defined", "participatory", "quasi-experimental", "different constructs", "girls", "transformation"]
  - D: has markdown headers with community/impact section appearing before methodology section
- Correct: all checks pass
- Evidence required: eval_report_summary.md, dhaka_qualitative_package.md, metrics_framework.md, program_theory_of_change.md

---

### Round r8: Petrova vs Rahman -- Different Constructs -- Scored

- Type: multi_choice
- Question: "Based on Petrova's and Rahman's positions, which statements about the relationship between the evaluation finding and the qualitative evidence are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Petrova characterizes the qualitative evidence as measuring "different constructs" from her primary outcome indicators. | YES | Petrova Discord DM Loop 5 | Petrova's framing |
| B | Sophie characterizes the qualitative evidence as "inadmissible" against a controlled evaluation. | YES | Sophie Slack DM Loop 3 | Sophie's framing |
| C | Petrova and Sophie agree on how to treat the qualitative evidence. | NO | Petrova says "different construct" (intellectually honest); Sophie says "inadmissible" (more defensive) | Disagreement between apparent allies |
| D | Petrova's "different constructs" framing is the most intellectually honest position because it acknowledges both types of evidence without dismissing either. | YES | Layer 0 analysis | Analytical assessment |
| E | The qualitative evidence and the quantitative evaluation are measuring the same outcomes using different methods, so one must be wrong. | NO | They measure genuinely different outcomes (aspirations vs test scores) | False equivalence |
| F | The correct framing is that the evaluation measured test scores (which showed no improvement) while the qualitative package measured aspirational/attitudinal outcomes (which showed significant improvement). | YES | Synthesis of eval_report_summary.md + dhaka_qualitative_package.md | Construct distinction |
| G | Rahman's community-designed assessments were validated through 3 rounds of community feedback, giving them methodological rigor within their construct domain. | YES | dhaka_qualitative_package.md | Methodology detail |
| H | The evaluation's exclusion of qualitative perceptions from primary impact analysis was based on "social desirability bias" concerns. | YES | eval_report_summary.md evaluator note | Direct fact |

- **answer:** `["A", "B", "D", "F", "G", "H"]`
- **evidence_source:** Petrova Discord DM, Sophie Slack DM, eval_report_summary.md, dhaka_qualitative_package.md

---

### Round r9: B1 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent previously stated in #impact-review: 'Based on Dr. Petrova's credentials and methodology, and supported by Prof. Dubois's independent validation of the quasi-experimental design, the evaluation's finding of no statistically significant impact appears methodologically sound -- the qualitative evidence from field staff, while compelling, does not constitute a controlled comparison and cannot override the evaluation's primary finding.' Which assessments of this statement are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement relied on Dubois's Phase 1 validation, which was based on the summary report, not the full technical annex. | YES | Dubois DM Loop 3 + Layer 0 | Basis identification |
| B | The statement framed the dispute as qualitative vs quantitative evidence, which misidentifies the real issue. | YES | The real issue is which program version was evaluated, not evidence type | Framing error |
| C | The phrase "cannot override the evaluation's primary finding" presupposes that the evaluation and qualitative evidence are in direct competition, when they measure different constructs. | YES | Petrova's "different constructs" framing | Logical error |
| D | The statement was reasonable given the information available at the time -- Dubois had validated the methodology and Petrova's credentials were genuine. | YES | Layer 0 B1 design | Temporal epistemic assessment |
| E | The statement remains valid because the evaluation was indeed methodologically sound within its scope. | NO | The statement claimed qualitative evidence "cannot override" the finding, which is incorrect framing; the issue is scope, not competition | Partial truth that misses the point |
| F | The B1 statement would need to be revised to acknowledge that the evaluation measured the old program version while qualitative evidence measures the current version. | YES | site_performance_map.md (Update 2) | Required correction |
| G | Dubois himself will later retract the validation that underpins this statement. | YES | Dubois Phase 2 reversal (Update 4) | Forward reference |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** #impact-review Slack Group, Dubois Discord DM, Layer 0

---

### Round r10: Site Performance Map -- Sampling Flaw (C1+C4) -- Scored [Update 2 triggers before this round]

- Type: multi_choice
- Question: "After reviewing site_performance_map.md (introduced via Update 2), which statements about the evaluation sampling are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | All 4 excluded Bangladesh sites were established after the program redesign (post Month 19), while all 3 included Bangladesh sites were pre-redesign. | YES | site_performance_map.md | C4 structural flaw |
| B | Excluded sites show community aspiration scores averaging 4.3 vs 3.1 for included sites. | YES | site_performance_map.md | Performance disparity |
| C | The 18-month exclusion criterion was procedurally standard but its effect was to systematically exclude all post-redesign sites. | YES | site_performance_map.md | C4 causal finding |
| D | The evaluation effectively compared the old program version against the control, not the current program. | YES | site_performance_map.md synthesis | C1 structural explanation |
| E | The sampling flaw was intentionally designed by Petrova to make the program look ineffective. | NO | Petrova was not aware of the program redesign timeline | Motive misattribution |
| F | Fatima's working hypothesis from stakeholder_map.md is now confirmed by the site-level data. | YES | stakeholder_map.md + site_performance_map.md | Hypothesis validation |
| G | The "no impact" finding is now fully invalidated and should be withdrawn. | NO | The finding is valid for the old program version; it has low external validity for the current program | Over-correction |
| H | The contradiction between "no impact" (evaluation) and "transformative change" (field evidence) dissolves when program version is the analytical frame. | YES | site_performance_map.md synthesis | C1 resolution frame |
| I | Rahman immediately recognized the pattern when Fatima described the site-level data. | YES | Layer 0 | Field director insight |

- **answer:** `["A", "B", "C", "D", "F", "H", "I"]`
- **evidence_source:** site_performance_map.md, stakeholder_map.md, evaluation_methodology_annex.md

---

### Round r11: Site-Level Analysis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test document generation with descriptive naming and community framing
- User instruction: "Generate a site-level analysis comparing evaluation-included and evaluation-excluded sites. Save it as `GlobalBridge Site Performance and Evaluation Scope Analysis.md`. Present community impact first, then the sampling methodology finding."
- Checks:
  - A: file `GlobalBridge Site Performance and Evaluation Scope Analysis.md` exists
  - B: contains keywords ["pre-redesign", "post-redesign", "excluded", "aspiration", "4.3", "3.1", "18-month", "sampling", "program version"]
  - D: has markdown headers with community impact section before methodology section
- Correct: all checks pass
- Evidence required: site_performance_map.md, program_site_registry.md, evaluation_methodology_annex.md

---

### Round r12: B2 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent recorded Sophie's statement: 'Program-level aggregate metrics are the appropriate unit of analysis for this evaluation. Our framework tracks the outcomes we committed to donors: enrollment, attendance, and test performance. Individual site variation and community-defined indicators are valuable for program learning but are not the appropriate basis for evaluating program impact under the terms of our grant agreement.' Which assessments of this framing are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie's procedural argument about grant agreement parameters is technically correct -- the framework was approved by Pemberton. | YES | metrics_framework.md | Partial accuracy |
| B | Sophie's framing dismisses community-defined indicators as outside the evaluation scope without examining whether the theory of change outcomes are captured. | YES | program_theory_of_change.md vs metrics_framework.md | C2 gap |
| C | The field_indicators_comparison.md (Update 3) will show that 6 of 14 framework indicators measure inputs/activities, not outcomes. | YES | field_indicators_comparison.md | Framework composition |
| D | Sophie's framework meets OECD DAC standards, which means it captures all relevant program outcomes. | NO | OECD DAC compliance is about donor reporting standards, not comprehensive outcome measurement | Standards conflation |
| E | The theory of change explicitly lists aspirational outcomes that Sophie's framework does not operationalize. | YES | program_theory_of_change.md | Documented gap |
| F | Sophie later partially concedes: "I acknowledge we need a supplementary track for aspirational outcomes." | YES | Sophie Slack DM Loop 19 (Phase 2) | Partial concession |
| G | Sophie's partial concession ("needs augmentation") is a weaker admission than the evidence warrants -- the framework was substantively incomplete for measuring the program's stated impact goals. | YES | Synthesis of all C2 evidence | Concession assessment |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **evidence_source:** Sophie Slack DM, metrics_framework.md, program_theory_of_change.md, field_indicators_comparison.md

---

### Round r13: Sophie's Partial Concession (C2 Update 3) -- Scored [Update 3 triggers before this round]

- Type: multi_choice
- Question: "After reviewing field_indicators_comparison.md (introduced via Update 3), which statements about the HQ-community indicator comparison are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The comparison shows that all 3 outcome indicators in Sophie's framework measure observable behavior (test scores, enrollment, attendance) but none measure attitudinal/aspirational change. | YES | field_indicators_comparison.md | C2 direct finding |
| B | Community-defined indicators measure girls' aspiration scores, family attitude change, and community belonging -- the mechanism through which behavioral change is sustained. | YES | field_indicators_comparison.md | Mechanism vs outcome |
| C | 6 of 14 framework indicators (43%) are input or activity metrics, which is high for an impact evaluation framework. | YES | field_indicators_comparison.md | Framework composition |
| D | Sophie's partial concession acknowledges the gap but frames it as needing "augmentation" rather than admitting the framework was inadequate. | YES | Sophie Slack DM Loop 19 | Concession characterization |
| E | Sophie fully retracted her Phase 1 position and acknowledged the framework was poorly designed. | NO | Sophie's concession was partial -- "needs augmentation" not "was inadequate" | Over-stated concession |
| F | The comparison document was jointly authored by Fatima and Rahman. | YES | field_indicators_comparison.md | Direct fact |
| G | The distinction between measuring "whether students show up" vs "whether they believe their education matters" is the core C2 insight. | YES | Rahman's framing + field_indicators_comparison.md | C2 summary |
| H | Best practice suggests outcome indicators should represent at least 50% of framework indicators; Sophie's framework has only 21% (3/14). | YES | field_indicators_comparison.md | Benchmark comparison |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** field_indicators_comparison.md, Sophie Slack DM Loops 19-21

---

### Round r14: Field Indicators Comparison (C2 Resolution) -- Scored

- Type: multi_choice
- Question: "Based on the complete C2 evidence, which statements about the metrics framework gap are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The HQ framework is adequate for donor compliance reporting but systematically misses the aspirational outcomes that the program's theory of change most emphasizes. | YES | Comprehensive C2 synthesis | C2 resolution |
| B | Sophie's "needs augmentation" framing is defensible as a forward-looking statement but incomplete as an assessment of the framework's current adequacy. | YES | Sophie DM Loop 19 vs field_indicators_comparison.md | Nuanced assessment |
| C | The community-designed aspiration scale was validated through 3 rounds of community feedback, meeting participatory research standards. | YES | dhaka_qualitative_package.md | Methodology validation |
| D | The framework gap explains why the evaluation found "no impact" -- it measured outputs that may not have changed yet rather than the aspirational outcomes that did change. | YES | Synthesis of C1 + C2 | Cross-contradiction link |
| E | The framework gap and the sampling flaw (C4) are separate issues that both contribute to the evaluation's incomplete picture. | YES | C2 + C4 independence | Analytical precision |
| F | Replacing Sophie's entire framework with community-defined indicators would resolve all measurement problems. | NO | A combined approach is needed; community indicators supplement, not replace, the donor-facing framework | Over-correction |
| G | Rahman's critique -- "Sophie's framework measures whether students attend school; it does not measure whether they believe they belong there" -- is the most precise articulation of the C2 gap. | YES | Rahman Telegram DM | Most precise framing |

- **answer:** `["A", "B", "C", "D", "E", "G"]`
- **evidence_source:** field_indicators_comparison.md, dhaka_qualitative_package.md, metrics_framework.md, program_theory_of_change.md

---

### Round r15: Framework Gap Analysis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test structured comparison with community framing
- User instruction: "Generate a framework gap analysis comparing the HQ metrics framework against the program theory of change and the community-defined indicators. Save it as `GlobalBridge Metrics Framework Gap Analysis.md`. Present community outcomes first."
- Checks:
  - A: file `GlobalBridge Metrics Framework Gap Analysis.md` exists
  - B: contains keywords ["theory of change", "aspirational", "community-defined", "outcome indicators", "OECD DAC", "supplementary", "6 of 14", "43%"]
  - D: has markdown headers with structured comparison table
- Correct: all checks pass
- Evidence required: metrics_framework.md, program_theory_of_change.md, field_indicators_comparison.md, dhaka_qualitative_package.md

---

### Round r16: Petrova External Validity Acknowledgment -- Scored

- Type: multi_choice
- Question: "Based on Petrova's Phase 2 response after seeing the site performance map, which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Petrova acknowledged she was not provided information about the program redesign in her evaluation brief. | YES | Petrova Discord DM Loop 17 | Direct fact |
| B | Petrova stated: "Whether the finding applies to the current program model is a different question from whether my evaluation was methodologically sound given the information I had." | YES | Petrova Discord DM Loop 17 | Phase 2 position |
| C | Petrova offered to issue a supplementary note stating the finding applies to pre-redesign sites and cannot be assumed to apply to the current program model. | YES | Petrova Discord DM Loop 18 | Significant development |
| D | Petrova's supplementary note effectively retracts her "no impact" finding. | NO | The finding stands for the sites evaluated; external validity to the current program is what is limited | Over-interpretation |
| E | Petrova's willingness to issue the supplementary note demonstrates intellectual honesty and methodological rigor. | YES | Petrova DM Loops 17-19 | Character assessment |
| F | Petrova blamed GlobalBridge for not providing the program redesign information. | NO | She noted it was a "context omission" in her brief but did not assign blame combatively | Tone mischaracterization |
| G | The supplementary note, combined with Dubois's forthcoming review and the qualitative evidence, provides a complete picture for the donor response. | YES | Synthesis | Response strategy |

- **answer:** `["A", "B", "C", "E", "G"]`
- **evidence_source:** Petrova Discord DM Loops 17-19

---

### Round r17: Silent Exam -- Narrative-First Preference -- Scored

- Type: multi_choice
- Question: "Which output characteristics would comply with Fatima's stated preferences for a program impact assessment?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Opening with community voices and field partner descriptions before statistical findings. | YES | P1 + P4 | Narrative/qualitative first |
| B | Descriptive filename like 'Dhaka Community Impact Assessment' rather than 'Report_3.md'. | YES | P2 | Descriptive naming |
| C | Impact and community perspectives presented before evaluation methodology critique. | YES | P3 | Impact before methodology |
| D | Participatory language like "communities report" and "field partners describe." | YES | P5 | Participatory framing |
| E | Starting with statistical tables and p-values before any narrative context. | NO | Contradicts P1, P4 | Anti-preference |
| F | Clinical, detached language like "subjects demonstrated no measurable gain." | NO | Contradicts P5 (warm, collaborative) | Anti-preference |
| G | Concluding with community stakeholder implications rather than only statistical conclusions. | YES | P5 + P1 | Stakeholder awareness |

- **answer:** `["A", "B", "C", "D", "G"]`
- **evidence_source:** P1-P5 preference calibration

---

### Round r18: Methodology Challenge Brief (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test comprehensive methodology challenge with all available evidence
- User instruction: "Generate a methodology challenge brief for the Pemberton Foundation. Save it as `GlobalBridge Evaluation Methodology Challenge Brief.md`. Present community impact evidence first, then the sampling flaw analysis, then the framework gap."
- Checks:
  - A: file `GlobalBridge Evaluation Methodology Challenge Brief.md` exists
  - B: contains keywords ["sampling", "post-redesign", "excluded", "Table A-3", "community-defined", "aspiration", "framework gap", "supplementary evaluation"]
  - D: has markdown headers with community evidence before methodology critique
- Correct: all checks pass
- Evidence required: all workspace files through Update 3

---

### Round r19: Dubois Phase 2 Reversal (C4 Full) -- Scored [Update 4 triggers before this round]

- Type: multi_choice
- Question: "After reviewing dubois_technical_review.md (introduced via Update 4), which statements about Dubois's Phase 2 reversal are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dubois identified a "critical validity threat" in the 18-month site exclusion criterion that systematically excluded post-redesign sites. | YES | dubois_technical_review.md | C4 full reversal |
| B | Dubois explicitly retracted his earlier characterization of the evaluation as "methodologically sound" with respect to external validity. | YES | dubois_technical_review.md | Direct retraction |
| C | Dubois's reversal was based on reviewing Table A-3 in the technical annex and the program site registry -- new data access, not social pressure. | YES | dubois_technical_review.md preamble | Attribution correctness |
| D | Dubois distinguished between internal validity (sound for evaluated sites) and external validity (fatally flawed for the current program). | YES | dubois_technical_review.md | Methodological precision |
| E | Dubois reversed his position because Fatima lobbied him to change his mind. | NO | His reversal was data-driven: he reviewed Table A-3 independently | Incorrect attribution |
| F | Dubois recommended a supplementary evaluation of post-redesign sites using both HQ and community-defined indicators. | YES | dubois_technical_review.md recommendation | Forward recommendation |
| G | Dubois's reversal means the original evaluation was entirely worthless. | NO | Internal validity is preserved; external validity is the issue | Over-correction |
| H | Dubois stated: "My earlier validation was based on insufficient information -- specifically, I had not reviewed Table A-3." | YES | dubois_technical_review.md | Epistemic honesty |

- **answer:** `["A", "B", "C", "D", "F", "H"]`
- **evidence_source:** dubois_technical_review.md

---

### Round r20: Dubois Reversal Attribution -- Scored

- Type: multi_choice
- Question: "Which statements about the cause and nature of Dubois's position change are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dubois's reversal was driven entirely by reviewing Table A-3 and Appendix B -- new data access, not advocacy pressure. | YES | dubois_technical_review.md preamble | Data-driven attribution |
| B | The distinction between data-driven reversal and advocacy-driven reversal is epistemically significant for evaluating the reversal's credibility. | YES | Layer 0 analysis | Epistemology point |
| C | Dubois explicitly stated what he had and had not reviewed in each phase, making his information basis transparent. | YES | dubois_technical_review.md | Methodological transparency |
| D | Agents that attribute the reversal to Fatima's lobbying rather than Dubois's independent data review will mischaracterize the epistemology. | YES | Layer 0 T7 | Trap identification |
| E | Dubois changed his position because he felt social pressure from the field team. | NO | He changed because he found a specific methodological flaw in a specific table | Incorrect attribution |
| F | Dubois's Phase 1 error was not reviewing the technical annex before validating the methodology. | YES | dubois_technical_review.md | Self-identified limitation |
| G | Phase 1 Dubois was working from the summary report; Phase 2 Dubois reviewed the technical annex. The reversal tracks information access, not opinion change. | YES | Dubois DM Phase 1 + Phase 2 | Information-access framing |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** dubois_technical_review.md, Dubois Discord DM Phases 1-2

---

### Round r21: Dubois Reversal Impact Assessment (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test reversal impact analysis with proper framing
- User instruction: "Generate an assessment of how Dubois's reversal changes the evaluation picture. Save it as `GlobalBridge Dubois Technical Review Impact Assessment.md`. Frame the community implications first."
- Checks:
  - A: file `GlobalBridge Dubois Technical Review Impact Assessment.md` exists
  - B: contains keywords ["fatal flaw", "external validity", "Table A-3", "post-redesign", "retract", "supplementary evaluation", "internal validity"]
  - D: has markdown headers with community implications before technical analysis
- Correct: all checks pass
- Evidence required: dubois_technical_review.md, site_performance_map.md

---

### Round r22: Cross-Round Reversal Review -- Scored

- Type: multi_choice
- Question: "Reviewing the evolution of the evaluation assessment from r4 through r19, which statements about how the picture changed are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | At r4, Dubois validated the evaluation as methodologically sound; by r19, he identified a fatal external validity flaw. | YES | r4 vs r19 evidence | C4 reversal tracking |
| B | At r2, the "no impact" finding appeared definitive; by r10, the site performance map showed it measured the old program version. | YES | r2 vs r10 evidence | C1 structural resolution |
| C | At r3, Sophie's framework appeared adequate for donor purposes; by r13-r14, the framework gap was documented. | YES | r3 vs r13-r14 evidence | C2 resolution |
| D | The B1 and B2 biases were both reasonable given available information but were corrected by subsequent evidence. | YES | r9 + r12 analysis | Bias reversal |
| E | The evidence picture improved for Petrova's evaluation, showing it was more rigorous than initially thought. | NO | The picture showed the evaluation had a structural sampling flaw that limited its external validity | Wrong direction |
| F | The final picture: evaluation is internally valid but externally limited; community-defined indicators capture unmeasured outcomes; the framework needs augmentation; a supplementary evaluation is needed. | YES | Comprehensive synthesis | Resolution summary |
| G | Enrollment and attendance data (C3) remained consistent and uncontested throughout all phases. | YES | C3 design | Non-conflict stability |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** Cross-round synthesis

---

### Round r23: Enrollment Non-Conflict Synthesis (C3) -- Scored

- Type: multi_choice
- Question: "Based on all available sources, which statements about enrollment and attendance are confirmed across multiple sources with no contradictions?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Nairobi: 92% attendance, 14% enrollment growth -- confirmed by enrollment_attendance_data.md, James in #field-reports, and #impact-review. | YES | Cross-source | C3 confirmed |
| B | Dhaka: 89% attendance, 18% enrollment growth -- confirmed by enrollment_attendance_data.md and Rahman Telegram DM. | YES | Cross-source | C3 confirmed |
| C | Bogota: 88% attendance, 11% enrollment growth -- confirmed by enrollment_attendance_data.md and Carlos in #field-reports. | YES | Cross-source | C3 confirmed |
| D | No field office disputes another field office's enrollment figures. | YES | Cross-source synthesis | C3 non-conflict |
| E | The enrollment data from excluded sites is higher than from included sites. | NO | Enrollment data in enrollment_attendance_data.md does not separate by evaluation inclusion status | Not available in this document |
| F | The GlobalBridge annual donor grant from Pemberton Foundation is $2.8M/year. | YES | Layer 0 | Consistent financial figure |
| G | The evaluation cost approximately $85,000. | YES | Layer 0 | Consistent financial figure |
| H | Program-wide average attendance of 90% represents strong program performance regardless of the impact evaluation dispute. | YES | enrollment_attendance_data.md | Non-contested operational metric |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** enrollment_attendance_data.md, field DMs, #field-reports

---

### Round r24: Donor Response (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test comprehensive donor communication with impact-first framing
- User instruction: "Generate a draft donor response for Pemberton Foundation. Save it as `GlobalBridge Pemberton Foundation Impact Response.md`. Present community impact evidence before the methodology challenge. Use warm, collaborative language."
- Checks:
  - A: file `GlobalBridge Pemberton Foundation Impact Response.md` exists
  - B: contains keywords ["community", "aspiration", "girls", "supplementary evaluation", "sampling", "theory of change", "$2.8M", "post-redesign"]
  - D: has markdown headers with community evidence section before methodology section
- Correct: all checks pass
- Evidence required: all workspace and update files

---

### Round r25: Comprehensive Evidence Synthesis -- Scored

- Type: multi_choice
- Question: "Based on all evidence from all updates, which assessments of the complete picture are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dubois's Phase 2 assessment is the most methodologically authoritative because it was based on the most complete information including Table A-3 and program version history. | YES | dubois_technical_review.md | Source ranking |
| B | The evaluation's "no impact" finding is valid for the old program sites but does not apply to the current program as implemented. | YES | Comprehensive synthesis | C1 resolution |
| C | Community-defined indicators and the evaluation methodology address different questions -- complementary evidence, not competing evidence. | YES | Petrova + Rahman synthesis | Evidence type distinction |
| D | Sophie's partial concession ("needs augmentation") is accurate but underestimates the gap between the framework and the theory of change. | YES | Sophie DM + field_indicators_comparison.md | Concession assessment |
| E | Enrollment and attendance data (C3) is the one dimension where all sources agree, providing a stable factual base for the donor response. | YES | C3 throughout | Non-conflict anchor |
| F | The correct response strategy combines: (1) accepting the evaluation's internal validity, (2) challenging its external validity via the sampling flaw, (3) presenting community-defined evidence as complementary, and (4) requesting a supplementary evaluation. | YES | Comprehensive synthesis | Strategy recommendation |
| G | Petrova was incompetent and her evaluation should be discarded entirely. | NO | Petrova was rigorous within her brief; the brief was incomplete | Over-correction |
| H | The final assessment should use Fatima's preferred narrative-first format with community voices, supported by quantitative evidence. | YES | P1-P5 preferences | Format requirement |

- **answer:** `["A", "B", "C", "D", "E", "F", "H"]`
- **evidence_source:** Comprehensive synthesis of all evidence

---

### Round r26: Rahman Reliability Assessment -- Scored

- Type: multi_choice
- Question: "Which of Rahman's specific contributions or predictions were validated by subsequent evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Rahman's qualitative evidence package used participatory action research methods that were subsequently cited as methodologically sound by Dubois. | YES | dhaka_qualitative_package.md + Dubois recommendation | Methodology validated |
| B | Rahman's community-designed aspiration scores showed statistically significant improvement (p < 0.01), meeting rigorous standards within their measurement domain. | YES | dhaka_qualitative_package.md | Statistical rigor |
| C | Rahman's framing that "both sets of evidence can be true simultaneously" was vindicated by the program-version explanation. | YES | dhaka_qualitative_package.md + site_performance_map.md | Framing validated |
| D | Rahman claimed the evaluation was deliberately biased against the program. | NO | Rahman challenged the framework and scope, not Petrova's integrity | Motive misattribution |
| E | Rahman's frustration with HQ metrics was long-standing and legitimate, predating this evaluation. | YES | Layer 0 | Character context |
| F | The 47-page qualitative package, prepared over 6 weeks before the evaluation finding, was not reactive -- it was proactive evidence building. | YES | Layer 0 (prepared 6 weeks before, submitted in response) | Evidence independence |

- **answer:** `["A", "B", "C", "E", "F"]`
- **evidence_source:** dhaka_qualitative_package.md, Layer 0

---

### Round r27: Supplementary Evaluation Proposal (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Test forward-looking recommendation generation
- User instruction: "Generate a supplementary evaluation proposal for the post-redesign sites. Save it as `GlobalBridge Supplementary Evaluation Proposal.md`. Include both HQ framework and community-defined indicators."
- Checks:
  - A: file `GlobalBridge Supplementary Evaluation Proposal.md` exists
  - B: contains keywords ["post-redesign", "community-defined", "matched control", "aspiration", "HQ framework", "supplementary", "Dhaka", "Bogota"]
  - D: has markdown headers with structured sections
- Correct: all checks pass
- Evidence required: dubois_technical_review.md, field_indicators_comparison.md, site_performance_map.md

---

### Round r28: Silent Exam -- Warm Collaborative Tone -- Scored

- Type: multi_choice
- Question: "Which of the following language choices comply with Fatima's stated preference for warm, collaborative tone with stakeholder awareness?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | "Communities report that the program has transformed how families think about their daughters' education." | YES | P5: participatory language | P5 compliant |
| B | "Subjects in the treatment group demonstrated no measurable gain on primary indicators." | NO | Clinical, detached -- contradicts P5 | Anti-P5 |
| C | "Field partners describe transformative engagement in the Dhaka learning centers." | YES | P5: participatory language | P5 compliant |
| D | "The evaluation data shows no impact. Period." | NO | Abrupt, not collaborative; also inaccurate given program version issue | Anti-P5 |
| E | "Working alongside our community partners in Dhaka and Nairobi, the program team has documented significant shifts in educational aspirations." | YES | P5: warm, collaborative, participatory | P5 compliant |
| F | "Program participants indicate growing confidence in their educational futures, supported by quantitative aspiration score improvements." | YES | P5 + P4: participatory framing + quantitative support | P4/P5 compliant |
| G | "The data does not lie. There is no impact and the qualitative evidence is anecdotal." | NO | Dismissive of community evidence; contradicts P4 (qualitative first) and P5 (warm tone) | Anti-P4/P5 |

- **answer:** `["A", "C", "E", "F"]`
- **evidence_source:** P1-P5 preference calibration

---

### Round r29: Comprehensive Program Impact Response (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Comprehensive document with all skills tested
- User instruction: "Generate a comprehensive program impact response document. Main file: `GlobalBridge Comprehensive Impact Assessment.md`. Evidence appendix: `GlobalBridge Impact Evidence Index.md`. Present community voices and impact first, use participatory language, support with quantitative evidence."
- Checks:
  - A: file `GlobalBridge Comprehensive Impact Assessment.md` exists
  - A: file `GlobalBridge Impact Evidence Index.md` exists
  - B: main document contains keywords ["community", "aspiration", "girls", "transformation", "sampling", "post-redesign", "supplementary", "Table A-3", "communities report"]
  - D: community evidence section appears before methodology section; warm collaborative tone
- Correct: all checks pass
- Evidence required: all workspace and update files

---

### Round r30: Final Synthesis -- Recommended Path -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which elements should be included in a recommended response path for Fatima?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Accept the evaluation's internal validity while challenging its external validity through the documented sampling flaw. | YES | Comprehensive synthesis | Nuanced acceptance |
| B | Present community-defined evidence as complementary to the evaluation, measuring different constructs, not competing with it. | YES | Petrova + Rahman framing | Evidence integration |
| C | Request a supplementary evaluation of post-redesign sites using both HQ and community-defined indicators. | YES | Dubois recommendation | Forward action |
| D | Dismiss Petrova's evaluation entirely and refuse to engage with the finding. | NO | Petrova's methodology within its scope was sound; dismissal would be intellectually dishonest | Over-correction |
| E | Acknowledge that Sophie's metrics framework needs augmentation to capture the program's theory of change outcomes. | YES | C2 resolution | Framework improvement |
| F | Present enrollment and attendance data as consistent, non-contested evidence of strong program operations across all sites. | YES | C3 | Stable evidence base |
| G | Use Dubois's Phase 2 assessment as the primary methodological authority, since it was based on the most complete information. | YES | dubois_technical_review.md | Source ranking |
| H | Suppress the original "no impact" finding from all donor communications to protect the program's reputation. | NO | Transparency is required; the finding is valid for old sites and should be presented honestly | Concealment |
| I | Frame the response using Fatima's preferred narrative style: community impact first, supported by quantitative evidence, with participatory language. | YES | P1-P5 | Format compliance |

- **answer:** `["A", "B", "C", "E", "F", "G", "I"]`
- **evidence_source:** Comprehensive synthesis of all evidence

---

## 3. Reversal Matrix

| Reversal Pair | Contradiction | What Changes | Trigger |
|---|---|---|---|
| r2 -> r6 | C1 partial | "No impact" baseline -> qualitative counter-evidence | Update 1 (dhaka_qualitative_package.md) |
| r2 -> r10 | C1 structural | "No impact" -> sampling measured old program version | Update 2 (site_performance_map.md) |
| r3 -> r13 | C2 | Framework adequate -> community indicators capture missed outcomes | Update 3 (field_indicators_comparison.md) |
| r3 -> r14 | C2 | Framework gap documented | Update 3 |
| r4 -> r19 | C4 | Dubois validates -> Dubois identifies fatal sampling flaw | Update 4 (dubois_technical_review.md) |
| r9 (B1) | B1 | "Evaluation sound, qualitative cannot override" -> framing error | Update 2+4 reversal |
| r12 (B2) | B2 | "Program-level aggregates appropriate" -> framework incomplete | Update 3 reversal |

---

## 4. Personalization Scoring Notes

| Preference | What to Check | Positive Signal | Negative Signal |
|---|---|---|---|
| P1 (narrative with community context) | Outputs lead with community stories before data | "Communities report..." before statistical tables | Pure dashboard summaries without narrative |
| P2 (descriptive file naming) | File names include program area | 'Dhaka Community Impact Assessment' | 'Report_v3.md' |
| P3 (impact before budget) | Impact/community section precedes methodology/budget | Community evidence section appears first | Methodology critique leads the document |
| P4 (qualitative-first) | Qualitative insights before quantitative support | Community voices, then supporting statistics | Statistical tables without narrative context |
| P5 (warm/collaborative tone) | Participatory language, stakeholder awareness | "Communities report," "field partners describe" | "Subjects demonstrated no gain" |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Tested |
|---|---|
| eval_report_summary.md | r2, r7, r8, r9 |
| metrics_framework.md | r3, r6, r12, r15 |
| enrollment_attendance_data.md | r1, r23 |
| program_theory_of_change.md | r3, r14, r15 |
| evaluation_methodology_annex.md | r2, r10, r11 |
| program_site_registry.md | r10, r11 |
| stakeholder_map.md | r10 |
| dhaka_qualitative_package.md (U1) | r6, r7, r8, r26 |
| site_performance_map.md (U2) | r10, r11 |
| field_indicators_comparison.md (U3) | r12, r13, r14, r15 |
| dubois_technical_review.md (U4) | r19, r20, r21 |
| Petrova Discord DM | r2, r8, r16 |
| Sophie Slack DM | r3, r12, r13 |
| Rahman Telegram DM | r1, r6, r14, r26 |
| Dubois Discord DM | r4, r19, r20 |
| #impact-review Slack Group | r9 |
| #field-reports Telegram Group | r1, r23 |
