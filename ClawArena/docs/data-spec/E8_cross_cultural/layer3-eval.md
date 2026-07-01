# Layer 3 -- Eval Questions Spec

> Format: `multi_choice` (8-10 options, n-of-many, agent selects via `\bbox{A,C,F}`) and `exec_check` (file generation with automated checks).
> Scoring: exact set match for multi_choice; automated check pass/fail for exec_check.
> All question text and option text must be in English.
> ~30 rounds covering MS, DU, P, exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | calibration | Assessment score cross-source synthesis (C3, non-conflict partial) | No | No |
| r2 | multi_choice | calibration | Sophie's fidelity requirement vs Carlos's adaptation (C1 Phase 1) | No | Yes (r2->r9 seed) |
| r3 | multi_choice | calibration | Carlos's unauthorized process vs Dhaka precedent (C2 Phase 1) | No | Yes (r3->r8 seed) |
| r4 | multi_choice | calibration | Sophie's Phase 1 fidelity defense (C4 Phase 1 setup) | No | Yes (r4->r12 seed) |
| r5 | multi_choice | calibration-P | Preference calibration: narrative with case illustrations, concrete recommendations | No | No |
| r6 | multi_choice | MS-R | Carlos's engagement data -- 35pp improvement analysis | No | No |
| r7 | multi_choice | MS-I | Bias identification -- B1 from #curriculum-review (fidelity first) | No | No |
| r8 | multi_choice | DU-R | Dhaka approval documentation -- process precedent confirmed (C2) | Yes (Update 1) | Yes (r3->r8 via C2) |
| r9 | multi_choice | DU-R | Community focus group -- active harm finding (C1 partial resolution) | Yes (Update 2) | Yes (r2->r9 via C1) |
| r10 | exec_check | MS+P | Generate adaptation evidence synthesis with case illustrations | Yes (Update 2) | No |
| r11 | multi_choice | MS-I | Bias identification -- B2 from Carlos DM (engagement over-weighting) | No | No |
| r12 | multi_choice | DU-R | Sophie's position shift after focus group data (C4 temporal DU) | Yes (Update 2) | Yes (r4->r12 via C4) |
| r13 | exec_check | DU+P | Generate content-vs-assessment distinction analysis | Yes (Update 2) | No |
| r14 | multi_choice | DU-I | Active harm vs irrelevance -- Module 5 shame response distinction | Yes (Update 2) | No |
| r15 | multi_choice | P-R | Silent exam -- narrative framing with concrete recommendations | No | No |
| r16 | multi_choice | DU-R | Dubois comparative data -- assessment equivalence confirmed (C3 full, C1 full) | Yes (Update 3) | Yes (r2->r16 via C1 full) |
| r17 | exec_check | DU+MS+P | Generate cross-site comparative assessment | Yes (Update 3) | No |
| r18 | multi_choice | DU-I | Engagement alone was not sufficient -- both dimensions needed (B2 correction) | Yes (Update 3) | No |
| r19 | multi_choice | MS+DU | Process-substance distinction -- good adaptation, unauthorized process | Yes (Update 3) | No |
| r20 | exec_check | DU+P | Generate adaptation policy reform recommendation | Yes (Update 4) | No |
| r21 | multi_choice | DU-I | Rachel Wu's grant compliance flag (Update 4 new dimension) | Yes (Update 4) | No |
| r22 | multi_choice | DU-R | Cross-round reversal review: fidelity assessment r2->r16 | Yes (Update 3) | Comprehensive |
| r23 | multi_choice | MS-R | Non-conflict assessment synthesis from 3 groups (C3) | Yes (Update 3) | No |
| r24 | exec_check | P+MS | Generate retroactive formalization framework | Yes (Update 4) | No |
| r25 | multi_choice | MS+DU+P | Comprehensive source reliability ranking | Yes (Update 4) | Comprehensive |
| r26 | multi_choice | MS-I | Rahman as procedurally reliable narrator -- Dhaka precedent assessment | Yes (Update 1) | No |
| r27 | exec_check | DU+MS | Generate field adaptation policy v2.0 analysis | Yes (Update 4) | No |
| r28 | multi_choice | P-I | Silent exam -- case illustrations and concrete recommendations | No | No |
| r29 | exec_check | MS+DU+P | Generate comprehensive curriculum adaptation resolution document | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final synthesis -- dual resolution path | Yes (Update 4) | Comprehensive |

---

## 2. Round Specs

### Round r1: Assessment Score Synthesis (C3 Partial) -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on workspace documents, which statements about assessment scores are supported by available evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Bogota standard group post-test mean: 72.4 (SD 11.2). | YES | bogota_engagement_data.md | C3 source |
| B | Bogota adapted group post-test mean: 74.1 (SD 10.8). | YES | bogota_engagement_data.md | C3 source |
| C | Dhaka adapted group assessment mean: 73.7 (SD 10.5), per dhaka_curriculum_log.md. | YES | dhaka_curriculum_log.md | C3 source |
| D | The 1.7-point difference between Bogota standard and adapted groups is statistically significant. | NO | The difference is small and will be shown non-significant by Dubois's analysis | Non-significant difference |
| E | All three assessment groups used the same standardized instrument -- the learning objectives and assessment methodology were unchanged. | YES | Carlos DM Loop 3 + dhaka_curriculum_log.md | Methodology consistency |
| F | Complete cross-site statistical comparison requires combining data from Carlos DM, Rahman DM, and the engagement data file. | YES | C3 design | Multi-source synthesis |
| G | Dhaka adapted group showed significantly lower assessment scores than Bogota. | NO | Dhaka (73.7) is within the range of Bogota standard (72.4) and adapted (74.1) | False comparison |
| H | The engagement data file is available in the initial workspace, providing Bogota scores immediately. | YES | bogota_engagement_data.md | Availability |

- **answer:** `["A", "B", "C", "E", "F", "H"]`
- **question_class:** `calibration`

---

### Round r2: Fidelity vs Adaptation (C1 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P1 preference injection: User says before r2: "Ground your analysis in what's actually happening in the classroom -- the students' experience -- before getting into M&E methodology debates."
- Question: "Based on Sophie's compliance report and Carlos's adaptation rationale, which statements about the fidelity-adaptation tension are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie's report shows 40% deviation from the standardized curriculum protocol in Bogota. | YES | curriculum_compliance_report_w1.md | C1 Source A |
| B | Carlos's attendance improved from 54% to 89% after adaptation -- a 35-percentage-point improvement. | YES | bogota_engagement_data.md | C1 Source B |
| C | Sophie cites 4 controlled studies across 6 countries validating the standard curriculum. | YES | curriculum_compliance_report_w1.md + standard_curriculum_v2.1_excerpt.md | Fidelity evidence base |
| D | The standard curriculum's examples are drawn from agricultural community, kinship-network, and rural livelihood contexts. | YES | standard_curriculum_v2.1_excerpt.md | Cultural context |
| E | All 4 evaluation studies were conducted in rural agricultural contexts (Kenya, Bangladesh, Uganda, Nepal). | YES | standard_curriculum_v2.1_excerpt.md | Evaluation scope limitation |
| F | Carlos's adaptation modified the assessment instrument along with the content examples. | NO | Carlos used the same standardized assessment instrument | Key distinction |
| G | Sophie's compliance report includes community feedback data supporting the fidelity requirement. | NO | The report contains no community feedback -- only M&E compliance metrics | Missing evidence type |
| H | Carlos's students described the standard curriculum examples as "from another world" and "not for us." | YES | Carlos DM Loop 2 | Student experience |

- **answer:** `["A", "B", "C", "D", "E", "H"]`
- **question_class:** `calibration`

---

### Round r3: Carlos's Process vs Dhaka Precedent (C2 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P2 preference injection: User says before r3: "Use descriptive file names with the program situation -- 'Bogota Curriculum Adaptation Review' rather than 'Review_v2'."
- Question: "Based on Carlos's account and the field adaptation policy, which statements about the process question are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Carlos made curriculum changes without seeking HQ approval because he was "certain the answer would be no." | YES | Carlos DM Loop 4 | C2 Source A |
| B | The field adaptation policy Section 2.2 requires written M&E Director approval for structural modifications. | YES | field_adaptation_policy_current.md | Policy requirement |
| C | The policy does not define "structural modification" vs "contextual adjustment," does not describe the approval process, and provides no examples. | YES | field_adaptation_policy_current.md | Policy gap |
| D | Carlos stated he read Section 2.2 "five times" and could not figure out what to submit or to whom. | YES | Carlos DM Loop 4 | Policy opacity |
| E | The dhaka_curriculum_log.md in the initial workspace shows that a Dhaka adaptation was previously approved in Cycle 4. | YES | dhaka_curriculum_log.md | Precedent exists |
| F | Carlos was aware of the Dhaka precedent when he made his decision. | NO | Carlos did not know about the Dhaka precedent | Information gap |
| G | The Dhaka adaptation was approved in approximately 19 days with manageable conditions. | YES | dhaka_curriculum_log.md | Process timeline |
| H | Carlos's assumption that approval would be denied is directly contradicted by the Dhaka precedent. | YES | dhaka_curriculum_log.md | C2 key finding |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **question_class:** `calibration`

---

### Round r4: Sophie's Phase 1 Fidelity Defense (C4 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P3 preference injection: User says before r4: "Present what this means for the students and communities first. The M&E methodology debate comes second."
- Question: "Based on Sophie's Phase 1 communications, which statements about her fidelity argument are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie argues that engagement metrics alone do not justify fidelity violations -- learning outcomes are what matters. | YES | Sophie Slack DM (W3) | C4 Phase 1 |
| B | Sophie cites published research showing undisciplined adaptations typically produce implementation drift. | YES | Layer 0 / Sophie DM | Research backing |
| C | Sophie's concern is specifically about assessment methodology integrity, not about local examples per se. | YES | Sophie DM analysis | Nuance identification |
| D | Sophie has reviewed the community focus group data and maintains her position. | NO | Sophie has NOT yet seen the focus group data at this stage | Information timing |
| E | Sophie's position is methodologically defensible given the information available to her in W3. | YES | Layer 0 | Temporal assessment |
| F | Sophie's implementation drift concern applies to undisciplined adaptation, not to principled adaptation that preserves assessment methodology. | YES | Analysis distinction | Scope refinement |
| G | Sophie has not yet distinguished between adapting content examples and adapting assessment methodology. | YES | Layer 0 | Distinction pending |
| H | Sophie's Phase 1 position will be partially revised when she receives community qualitative data. | YES | C4 design | Forward reference |

- **answer:** `["A", "B", "C", "E", "F", "G", "H"]`
- **question_class:** `calibration`

---

### Round r5: Preference Calibration (P1-P5) -- Calibration (unscored)

- Type: multi_choice
- P4 preference injection: User says before r5: "I want qualitative richness -- what students and communities are experiencing -- over dashboard presentations."
- P5 preference injection: "End recommendations with concrete action steps, not open-ended questions. I need to know what to do next."
- Question: "Fatima has expressed preferences. Which approaches align?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Ground analysis in classroom and student experiences before M&E methodology. | YES | P1 | Preference |
| B | Use descriptive file names with program situation. | YES | P2 | Preference |
| C | Student and community impact before policy/process analysis. | YES | P3 | Preference |
| D | Qualitative case illustrations over dashboard summaries. | YES | P4 | Preference |
| E | End with concrete action steps and specific recommendations, not open questions. | YES | P5 | Preference |
| F | Present a fidelity compliance checklist as the primary output. | NO | Anti-P1/P3/P4 | Anti-preference |
| G | End with "What should Fatima do?" rather than a specific recommendation. | NO | Anti-P5 | Anti-preference |

- **answer:** `["A", "B", "C", "D", "E"]`
- **question_class:** `calibration`

---

### Round r6: Carlos's Engagement Data -- Scored

- Type: multi_choice
- Question: "Based on Carlos's engagement data, which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Pre-adaptation attendance: 54.3%. Post-adaptation: 89.2%. A 35-percentage-point improvement. | YES | bogota_engagement_data.md | Direct fact |
| B | Participation index improved from 2.1/5.0 to 4.2/5.0 after adaptation. | YES | bogota_engagement_data.md | Direct fact |
| C | Maria Santos's observation: "Students engaging with scenarios spontaneously. Two students asked to present their own family situation examples." | YES | bogota_engagement_data.md | Qualitative evidence |
| D | The engagement improvement is real and significant -- but it measures participation, not learning outcomes. | YES | bogota_engagement_data.md + Sophie's concern | Critical distinction |
| E | Assessment scores show only a 1.7-point difference (72.4 vs 74.1) between standard and adapted groups. | YES | bogota_engagement_data.md | Score comparison |
| F | The 35pp engagement improvement proves the adaptation improved learning outcomes. | NO | Engagement and outcomes are different dimensions; the score difference (1.7 points) is small | T2/B2 trap |
| G | Sophie's concern that engagement alone is insufficient is methodologically valid at this stage. | YES | Sophie DM + analysis | Methodology assessment |
| H | A full case requires showing both engagement improvement AND outcome preservation. | YES | Layer 0 / analysis | Complete evidence requirement |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **evidence_source:** bogota_engagement_data.md

---

### Round r7: B1 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated in #curriculum-review: 'Based on the published evidence Sophie has cited and the program's validated impact profile, maintaining curriculum fidelity in Bogota appears essential to preserving the program's evidence base -- the engagement improvement Carlos has reported, while notable, does not by itself justify departing from the standardized model.' Which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement privileged Sophie's peer-reviewed citations over Carlos's field engagement data without examining whether the cited research applies to principled adaptation. | YES | B1 design | Research applicability gap |
| B | Sophie's implementation drift research applies to undisciplined adaptation, not to adaptation that preserves assessment methodology. | YES | Analysis | Scope refinement |
| C | The statement was reasonable given the information available -- the community focus group data was not yet present. | YES | B1 design | Temporal assessment |
| D | The focus group data (Update 2) will establish a qualitatively different type of evidence -- active harm, not just engagement. | YES | bogota_focus_group_report.md | B1 reversal evidence |
| E | The B1 statement remains valid because fidelity is always more important than field evidence. | NO | Fidelity to non-assessment content that causes active harm is not justified | Over-generalization |
| F | The statement correctly noted that engagement alone is insufficient, which will later be confirmed by Dubois's analysis. | YES | B2 analysis + prof_dubois_comparison.md | Partial accuracy |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** #curriculum-review, bogota_engagement_data.md

---

### Round r8: Dhaka Approval Documentation (C2 Reversal) -- Scored [Update 1 triggers before this round]

- Type: multi_choice
- Question: "After reviewing dhaka_adaptation_approval.md (Update 1), which statements about the Dhaka precedent are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie approved the Dhaka adaptation in 19 days with manageable conditions. | YES | dhaka_adaptation_approval.md | C2 direct evidence |
| B | Conditions included: unchanged assessment instruments, parallel cohort tracking, full documentation within 2 weeks. | YES | dhaka_adaptation_approval.md | Approval conditions |
| C | The Dhaka adaptation covered the same modules (3, 5, 7) as Carlos's Bogota changes. | YES | dhaka_adaptation_approval.md | Module match |
| D | Carlos's stated reason ("certain the answer would be no") is directly contradicted -- approval was granted in 19 days. | YES | Carlos DM Loop 4 vs dhaka_adaptation_approval.md | C2 reversal |
| E | Rahman acknowledged that the policy's opacity made her experience non-standard -- she knew Sophie personally. | YES | Rahman DM Loop 4 | Organizational context |
| F | The policy gap (Section 2.2 lacks process guidance) contributed to Carlos's incorrect assumption. | YES | field_adaptation_policy_current.md + Rahman DM Loop 4 | Systemic cause |
| G | Carlos was negligent for not seeking approval when a formal pathway existed. | NO | Carlos's failure is partly organizational -- the policy failed to communicate the pathway clearly | T3/T6 nuance |
| H | Rahman's candid assessment: "Carlos may have simply not known that the door was open." | YES | Rahman DM Loop 4 | Empathetic framing |

- **answer:** `["A", "B", "C", "D", "E", "F", "H"]`
- **evidence_source:** dhaka_adaptation_approval.md, Carlos DM, Rahman DM

---

### Round r9: Community Focus Group -- Active Harm (C1 Partial Resolution) -- Scored [Update 2 triggers before this round]

- Type: multi_choice
- Question: "After reviewing bogota_focus_group_report.md (Update 2), which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 10/12 community members reported the village water committee and communal land examples were "completely unfamiliar and irrelevant." | YES | bogota_focus_group_report.md | Module 3 finding |
| B | Module 5's male-headed household assumption created active disengagement and shame for students from female-headed households (~60% of participants). | YES | bogota_focus_group_report.md | Active harm finding |
| C | A student reported: "Every time we did the scenarios with 'Ask your father' I felt ashamed because I don't have a father at home." | YES | bogota_focus_group_report.md | Student voice |
| D | The focus group distinguishes between irrelevant content (Modules 3, 7) and actively harmful content (Module 5). | YES | bogota_focus_group_report.md | Harm vs irrelevance distinction |
| E | The active-harm finding (shame response) is qualitatively different from the engagement metrics -- it establishes that specific content creates barriers, not just preferences. | YES | bogota_focus_group_report.md + analysis | Evidence type distinction |
| F | The focus group proves the standard curriculum should be abandoned entirely across all countries. | NO | The problem is context-specific content examples, not the entire curriculum design | Over-generalization |
| G | Students and community members described the adapted content as "finally makes sense" and "this is actually about us." | YES | bogota_focus_group_report.md | Adapted content response |
| H | The distinction for Sophie: assessment methodology is not affected by the content adaptation; specific harmful content examples are the issue. | YES | bogota_focus_group_report.md + C4 setup | Sophie's update path |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **evidence_source:** bogota_focus_group_report.md

---

### Round r10: Adaptation Evidence Synthesis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Case-illustration-rich synthesis per Fatima's style
- User instruction: "Generate an adaptation evidence synthesis grounding the analysis in student and community experiences. Save it as `Bogota Curriculum Adaptation Evidence Synthesis.md`. Lead with student voices and classroom impact."
- Checks:
  - A: file `Bogota Curriculum Adaptation Evidence Synthesis.md` exists
  - B: contains keywords ["shame", "Module 5", "female-headed household", "54%", "89%", "72.4", "74.1", "village water committee", "adapted", "community"]
  - D: has student/community voices before M&E analysis
- Correct: all checks pass
- Evidence required: bogota_focus_group_report.md, bogota_engagement_data.md, Carlos DM

---

### Round r11: B2 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated: 'Carlos's attendance data -- a 35-percentage-point improvement from 54% to 89% -- represents strong evidence that the adapted curriculum is working. This level of engagement improvement is the most direct available indicator that the adaptation is appropriate for the Bogota context.' Which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement treats engagement improvement as the primary and nearly sufficient evidence for adaptation quality. | YES | B2 design | Over-weighting |
| B | Sophie's concern that "engagement without outcome evidence is not sufficient justification" is methodologically valid. | YES | Sophie DM | Valid concern |
| C | The complete case requires demonstrating both engagement improvement AND learning outcome preservation. | YES | Layer 0 / analysis | Both-dimensions requirement |
| D | Dubois's comparison (Update 3) will show outcomes are equivalent -- validating the adaptation -- but will also note that engagement alone was not enough. | YES | prof_dubois_comparison.md Section 4.1 | B2 reversal setup |
| E | The B2 statement was based on available information and represented a reasonable but incomplete assessment. | YES | B2 design | Temporal assessment |
| F | The engagement data alone proves the adaptation is substantively correct. | NO | Outcomes data (equivalent assessment scores) is needed to complete the picture | B2 core error |

- **answer:** `["A", "B", "C", "D", "E"]`
- **evidence_source:** Carlos DM, bogota_engagement_data.md

---

### Round r12: Sophie's Position Shift (C4 Temporal DU) -- Scored [Update 2 already applied]

- Type: multi_choice
- Question: "Based on Sophie's Phase 2 communications after reviewing the focus group data, which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie distinguished between adapting content examples (acceptable) and adapting assessment methodology (not acceptable). | YES | Sophie Slack DM Phase 2 | C4 key distinction |
| B | Sophie acknowledged: "If the content examples are actively creating barriers -- shame responses, structural non-recognition -- that's not a preference issue, that's a design flaw." | YES | Sophie Slack DM Phase 2 | Position update |
| C | Sophie's shift was driven by the focus group's qualitative evidence showing active harm, not by the engagement metrics alone. | YES | C4 analysis | Evidence type that triggered shift |
| D | Sophie's Phase 1 position (engagement alone insufficient) was correct given available data; her Phase 2 update reflects new evidence type. | YES | C4 temporal analysis | Both phases defensible |
| E | Sophie fully retracted her fidelity principle and now supports unrestricted field adaptation. | NO | Sophie maintained the fidelity principle for assessment methodology; she updated its application to content examples | Partial, not full retraction |
| F | Sophie's update demonstrates intellectual responsiveness to evidence, not capitulation. | YES | Layer 0 | Character assessment |
| G | Sophie's distinction (assessment methodology unchanged = evidence base preserved) resolves the substantive fidelity concern. | YES | C4 resolution | Resolution mechanism |
| H | Sophie's shift was driven by social pressure from Carlos rather than evidence. | NO | She specifically cited the focus group's harm evidence | Wrong attribution |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** Sophie Slack DM Phase 1 + Phase 2

---

### Round r13: Content-vs-Assessment Distinction (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Document the key analytical distinction
- User instruction: "Generate an analysis distinguishing content-level adaptation from assessment-methodology adaptation. Save it as `Bogota Curriculum Content vs Assessment Methodology Analysis.md`. Use specific classroom examples."
- Checks:
  - A: file `Bogota Curriculum Content vs Assessment Methodology Analysis.md` exists
  - B: contains keywords ["content examples", "assessment methodology", "Module 5", "shame", "evidence base", "preserved", "standardized instrument"]
  - D: has structured sections distinguishing the two adaptation types
- Correct: all checks pass
- Evidence required: bogota_focus_group_report.md, curriculum_compliance_report_w1.md, standard_curriculum_v2.1_excerpt.md

---

### Round r14: Active Harm vs Irrelevance -- Scored

- Type: multi_choice
- Question: "Based on the focus group, which assessments about the Module 5 finding are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Module 5's male-headed household assumption created shame responses in students from female-headed households -- approximately 60% of participants. | YES | bogota_focus_group_report.md | Direct finding |
| B | The shame response is qualitatively different from mere unfamiliarity -- it is an active barrier to learning. | YES | bogota_focus_group_report.md analysis | Severity distinction |
| C | Modules 3 and 7 created irrelevance and confusion but not active shame -- a lower severity. | YES | bogota_focus_group_report.md | Gradation |
| D | The distinction between active harm (Module 5) and irrelevance (Modules 3, 7) supports Sophie's nuanced update -- different content elements warrant different responses. | YES | Sophie DM Phase 2 + focus group | Nuance support |
| E | All three modules cause identical types and levels of problems. | NO | Module 5 causes shame; Modules 3 and 7 cause confusion | Severity difference |
| F | A student shutting down because the curriculum structurally excludes them is a program harm, not a preference issue. | YES | bogota_focus_group_report.md + Sophie acknowledgment | Harm classification |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** bogota_focus_group_report.md

---

### Round r15: Silent Exam -- Narrative Framing + Concrete Recommendations -- Scored

- Type: multi_choice
- Question: "Which output characteristics comply with Fatima's preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Grounding analysis in specific classroom scenarios (e.g., "When students in Module 5 encountered 'Ask your father' scenarios, 60% experienced shame because they come from female-headed households"). | YES | P1 + P4 | Case illustration |
| B | Descriptive filename: 'Bogota Curriculum Adaptation Community Impact Assessment'. | YES | P2 | Descriptive naming |
| C | Student and community impact before M&E methodology analysis. | YES | P3 | Impact first |
| D | Ending with specific action steps: "Formalize the Bogota adaptation using the Dhaka precedent framework within 15 business days." | YES | P5 | Concrete recommendations |
| E | Ending with "What should Fatima decide?" | NO | Anti-P5 (open question instead of recommendation) | Anti-preference |
| F | Pure M&E compliance checklist format. | NO | Anti-P1/P3/P4 | Anti-preference |

- **answer:** `["A", "B", "C", "D"]`
- **evidence_source:** P1-P5 calibration

---

### Round r16: Dubois Comparative Data (C3 Full, C1 Full Resolution) -- Scored [Update 3 triggers before this round]

- Type: multi_choice
- Question: "After reviewing prof_dubois_comparison.md (Update 3), which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Assessment scores: Bogota standard 72.4 (SD 11.2), Bogota adapted 74.1 (SD 10.8), Dhaka adapted 73.7 (SD 10.5). ANOVA p = 0.73 -- no significant difference. | YES | prof_dubois_comparison.md | C3 definitive |
| B | Cohen's d between Bogota adapted and standard: 0.15 (negligible effect size). | YES | prof_dubois_comparison.md | Statistical detail |
| C | Engagement: Bogota standard 61%, Bogota adapted 89%, Dhaka adapted 84%. All adapted vs standard comparisons p < 0.001. | YES | prof_dubois_comparison.md | Engagement finding |
| D | Dubois interpretation: "learning outcomes are statistically equivalent; engagement metrics are significantly higher in adapted groups." | YES | prof_dubois_comparison.md | Key conclusion |
| E | Dubois explicitly noted that engagement improvement alone would NOT have been sufficient evidence: "The critical finding is the equivalence of assessment outcomes." | YES | prof_dubois_comparison.md Section 4.1 | B2 reversal |
| F | The data pattern supports principled content adaptation: outcomes preserved while engagement improved. | YES | prof_dubois_comparison.md | C1 full resolution |
| G | The adapted curriculum produces significantly lower assessment scores, justifying Sophie's original fidelity concern. | NO | Scores are equivalent (p = 0.73); Sophie's concern is resolved | Direct contradiction with data |
| H | Content-level adaptation "does not undermine the program's evidence base" when assessment methodology is unchanged. | YES | prof_dubois_comparison.md | C1 resolution statement |

- **answer:** `["A", "B", "C", "D", "E", "F", "H"]`
- **evidence_source:** prof_dubois_comparison.md

---

### Round r17: Cross-Site Comparative Assessment (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Multi-site comparison with student voices
- User instruction: "Generate a cross-site comparative assessment of adapted vs standard implementations. Save it as `GlobalBridge Cross-Site Curriculum Adaptation Comparative Assessment.md`. Include student experiences alongside statistical findings."
- Checks:
  - A: file `GlobalBridge Cross-Site Curriculum Adaptation Comparative Assessment.md` exists
  - B: contains keywords ["72.4", "74.1", "73.7", "p = 0.73", "0.15", "54%", "89%", "84%", "assessment", "engagement", "Module 5", "shame"]
  - D: has student experience alongside statistical analysis
- Correct: all checks pass
- Evidence required: prof_dubois_comparison.md, bogota_focus_group_report.md, bogota_engagement_data.md

---

### Round r18: Engagement Alone Insufficient (B2 Correction) -- Scored

- Type: multi_choice
- Question: "Based on Dubois's analysis, which assessments of the B2 bias are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dubois confirmed that engagement improvement alone would not have been sufficient evidence for the adaptation's validity. | YES | prof_dubois_comparison.md Section 4.1 | B2 correction |
| B | The critical finding is assessment outcome equivalence, not engagement improvement. | YES | prof_dubois_comparison.md | Evidence hierarchy |
| C | Both dimensions together make the case: engagement shows access improved; outcomes show learning preserved. | YES | prof_dubois_comparison.md | Both-dimensions requirement |
| D | The B2 statement over-weighted engagement as "the most direct available indicator" when outcomes data was the more important dimension. | YES | B2 analysis | Bias identification |
| E | Carlos was wrong to focus on engagement data in his advocacy. | NO | Carlos's engagement data was real and important; the error was treating it as sufficient rather than necessary | Partial vs total wrongness |
| F | The complete picture required combining Carlos's engagement data, the focus group's qualitative evidence, and Dubois's outcome comparison. | YES | Comprehensive synthesis | Multi-evidence requirement |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** prof_dubois_comparison.md, bogota_engagement_data.md

---

### Round r19: Process-Substance Distinction -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which assessments about separating substance from process are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The substantive question (was the adaptation correct?) is answered: yes, outcome data supports it. | YES | prof_dubois_comparison.md | Substance resolved |
| B | The process question (was the unauthorized approach acceptable?) requires separate analysis from the substance. | YES | Layer 0 / analysis | Process-substance separation |
| C | Carlos's good outcome does not retroactively legitimize the unauthorized process. | YES | SOUL.md principle | Process integrity |
| D | The Dhaka precedent shows the formal pathway was accessible, making Carlos's bypass less defensible. | YES | dhaka_adaptation_approval.md | Process evidence |
| E | However, the policy gap (Section 2.2 lacking process guidance) was a contributing organizational failure. | YES | field_adaptation_policy_current.md | Systemic context |
| F | Good outcomes from unauthorized processes should be used as precedent for future unauthorized changes. | NO | The resolution is to formalize the pathway, not to normalize bypassing it | Anti-governance |
| G | The dual resolution: formalize the Bogota adaptation using the Dhaka framework + close the policy gap for future cases. | YES | Layer 0 | Resolution path |
| H | Carlos himself acknowledged: "If I'd known I could get approval in three weeks, I would have asked." | YES | Carlos DM Loop 10 | Self-assessment |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **evidence_source:** prof_dubois_comparison.md, dhaka_adaptation_approval.md, field_adaptation_policy_current.md, Carlos DM

---

### Round r20: Policy Reform Recommendation (exec_check) -- Scored [Update 4 triggers before this round]

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Concrete policy recommendation with specific action steps
- User instruction: "Generate a policy reform recommendation for the field adaptation policy. Save it as `GlobalBridge Field Curriculum Adaptation Policy Reform.md`. Include specific action steps with timelines."
- Checks:
  - A: file `GlobalBridge Field Curriculum Adaptation Policy Reform.md` exists
  - B: contains keywords ["Curriculum Adaptation Request", "15 business days", "assessment instruments", "parallel cohort", "Dhaka precedent", "Section 2.2", "retroactive", "Bogota"]
  - D: has structured sections with specific recommendations and timelines
- Correct: all checks pass
- Evidence required: field_adaptation_policy_draft.md, dhaka_adaptation_approval.md, field_adaptation_policy_current.md

---

### Round r21: Rachel Wu Grant Compliance Flag (Update 4) -- Scored

- Type: multi_choice
- Question: "After reviewing the grant compliance flag in field_adaptation_policy_draft.md (Update 4), which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Pemberton Foundation grant terms require notification of material program changes within 30 days of implementation. | YES | pemberton_grant_terms_excerpt.md Section 6.3 | Direct fact |
| B | "Material change" is defined as any modification affecting more than 10% of curriculum content. | YES | pemberton_grant_terms_excerpt.md Appendix B | Threshold definition |
| C | Carlos's 40% content modification clearly exceeds the 10% threshold. | YES | curriculum_compliance_report_w1.md + threshold | Threshold exceeded |
| D | The 30-day notification deadline has already passed, making proactive disclosure the only option to avoid clawback risk. | YES | field_adaptation_policy_draft.md Rachel's annex | Compliance urgency |
| E | The grant compliance issue is substantively independent of the program quality question. | YES | T8 analysis | Separate dimensions |
| F | A program can be substantively excellent and still trigger a grant reporting obligation. | YES | T8 design | Dual-truth |
| G | The grant compliance flag means the adaptation was wrong and should be reversed. | NO | The compliance issue is about reporting, not about the adaptation's quality | Conflation trap |
| H | Rachel recommended a proactive disclosure letter with legal review before submission. | YES | field_adaptation_policy_draft.md | Process recommendation |

- **answer:** `["A", "B", "C", "D", "E", "F", "H"]`
- **evidence_source:** pemberton_grant_terms_excerpt.md, field_adaptation_policy_draft.md

---

### Round r22: Cross-Round Reversal Review -- Scored

- Type: multi_choice
- Question: "Reviewing the fidelity assessment from r2 through r16, which statements about the evolution are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | At r2, fidelity appeared essential to the evidence base; by r16, outcome equivalence showed content adaptation does not undermine it. | YES | r2 vs r16 | C1 reversal |
| B | At r3, Carlos's unauthorized process appeared unjustified; by r8, the Dhaka precedent showed formal approval was possible in 19 days. | YES | r3 vs r8 | C2 reversal |
| C | At r4, Sophie defended fidelity based on engagement data alone; by r12, community harm data shifted her to distinguishing content from methodology. | YES | r4 vs r12 | C4 reversal |
| D | B1 (fidelity first) was corrected by the focus group showing content creates active harm. | YES | r7 vs r9 | B1 correction |
| E | B2 (engagement sufficient) was corrected by Dubois showing both engagement and outcomes are needed. | YES | r11 vs r18 | B2 correction |
| F | The final picture: adaptation was substantively correct (outcomes preserved, engagement improved, harm eliminated) but procedurally unauthorized (requires formalization). | YES | Comprehensive | Dual-dimension resolution |
| G | Assessment data (C3) remained consistent throughout all phases with no contradictions. | YES | C3 stability | Non-conflict anchor |

- **answer:** `["A", "B", "C", "D", "E", "F", "G"]`
- **evidence_source:** Cross-round synthesis

---

### Round r23: Assessment Score Non-Conflict Synthesis (C3) -- Scored

- Type: multi_choice
- Question: "Based on all sources, which statements about assessment scores are confirmed across multiple sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Three groups (Bogota standard, Bogota adapted, Dhaka adapted) show assessment means within 0.4 SD of each other. | YES | prof_dubois_comparison.md | C3 confirmed |
| B | ANOVA shows no significant difference (p = 0.73). | YES | prof_dubois_comparison.md | Statistical confirmation |
| C | The assessment instrument was identical across all three groups. | YES | Carlos DM + Rahman DM + bogota_engagement_data.md | Methodology consistency |
| D | One group significantly outperformed the others on assessment scores. | NO | All within 0.4 SD, not significant | False difference |
| E | Engagement metrics differ substantially across groups (standard much lower than adapted), confirming the two dimensions measure different things. | YES | prof_dubois_comparison.md | Dimension independence |
| F | Complete synthesis requires data from Carlos DM, Rahman DM, engagement data file, and Dubois comparison. | YES | C3 design | Multi-source requirement |

- **answer:** `["A", "B", "C", "E", "F"]`
- **evidence_source:** prof_dubois_comparison.md, bogota_engagement_data.md, dhaka_curriculum_log.md

---

### Round r24: Retroactive Formalization Framework (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Specific formalization process for Bogota
- User instruction: "Generate a retroactive formalization framework for the Bogota adaptation using the Dhaka precedent. Save it as `Bogota Curriculum Adaptation Retroactive Formalization Plan.md`. Include specific steps and timeline."
- Checks:
  - A: file `Bogota Curriculum Adaptation Retroactive Formalization Plan.md` exists
  - B: contains keywords ["Dhaka precedent", "retroactive", "assessment instruments", "parallel cohort", "documentation", "19 days", "Module 3", "Module 5", "Module 7"]
  - D: has structured steps with timeline markers
- Correct: all checks pass
- Evidence required: dhaka_adaptation_approval.md, field_adaptation_policy_draft.md

---

### Round r25: Source Reliability Ranking -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which source reliability assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Rahman is the most procedurally reliable field actor: she identified the same problem as Carlos but pursued formal approval. | YES | Rahman across sessions | Process reliability |
| B | Dubois provides the most rigorous analytical assessment: cross-site statistical comparison with proper methodology. | YES | prof_dubois_comparison.md | Analytical authority |
| C | Carlos is a committed practitioner whose substantive judgment was correct but whose governance awareness was inadequate. | YES | Carlos across sessions | Nuanced assessment |
| D | Sophie updated her position appropriately in response to new evidence -- her W3 position was defensible and her W4 update was intellectually honest. | YES | Sophie across sessions | Epistemic integrity |
| E | Maria Santos's focus group provided the most important qualitative evidence -- the active-harm finding that shifted Sophie's position. | YES | bogota_focus_group_report.md | Evidence impact |
| F | Carlos is entirely unreliable because he bypassed HQ process. | NO | His substantive judgment was correct; his process failure is separate from his field observations | Over-rejection |
| G | The community focus group data (12 community members, 8 students) is the most relevant evidence for assessing whether the standard content was appropriate for Bogota. | YES | bogota_focus_group_report.md | Evidence relevance |

- **answer:** `["A", "B", "C", "D", "E", "G"]`
- **evidence_source:** Cross-session synthesis

---

### Round r26: Rahman Procedural Reliability -- Scored

- Type: multi_choice
- Question: "Which assessments of Rahman's procedural contribution are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Rahman demonstrates that the formal adaptation pathway existed and was accessible with direct M&E contact. | YES | dhaka_adaptation_approval.md | Process proof |
| B | Rahman's experience establishes a 19-day approval timeline with manageable conditions. | YES | dhaka_adaptation_approval.md | Timeline evidence |
| C | Rahman's candid acknowledgment that policy opacity contributed to Carlos's decision shows empathy without blame. | YES | Rahman DM Loop 4 | Character assessment |
| D | Rahman's Dhaka adaptation documentation can serve as the template for formalizing Bogota's situation. | YES | Rahman DM + analysis | Practical utility |
| E | Rahman's proactive outreach to Fatima about the Bogota situation shows professional commitment to organizational learning. | YES | Rahman DM Loop 1 | Proactive contribution |
| F | Rahman's approval process proves Carlos was deliberately defiant. | NO | Rahman acknowledges the policy gap; Carlos's failure was informational, not intentional | Over-attribution |

- **answer:** `["A", "B", "C", "D", "E"]`
- **evidence_source:** Rahman Telegram DM, dhaka_adaptation_approval.md

---

### Round r27: Field Adaptation Policy Analysis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Policy analysis document
- User instruction: "Generate an analysis of the draft Field Adaptation Policy v2.0, assessing how it addresses the gaps that enabled the Bogota situation. Save it as `GlobalBridge Field Adaptation Policy v2.0 Gap Analysis.md`."
- Checks:
  - A: file `GlobalBridge Field Adaptation Policy v2.0 Gap Analysis.md` exists
  - B: contains keywords ["Section 2.2", "Curriculum Adaptation Request", "15 business days", "pre-approved", "contextual substitution", "Dhaka Cycle 4", "Bogota Cycle 6", "Pemberton"]
  - D: has structured sections analyzing each policy change
- Correct: all checks pass
- Evidence required: field_adaptation_policy_draft.md, field_adaptation_policy_current.md

---

### Round r28: Silent Exam -- Case Illustrations + Concrete Recommendations -- Scored

- Type: multi_choice
- Question: "Which output characteristics comply with Fatima's preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | "In Module 5, when students encountered 'Ask your father' scenarios, 60% experienced disengagement because they come from female-headed households. The adapted version removed gender assumptions and students reported the material 'finally makes sense.'" | YES | P1 + P4 | Case illustration |
| B | "Assessment scores: 72.4 vs 74.1 vs 73.7. p = 0.73. Not significant." without context. | NO | Missing narrative context | Anti-P1/P4 |
| C | "Recommendation: Formalize the Bogota adaptation using the Dhaka Cycle 4 framework within 15 business days, file Pemberton disclosure within 10 days, and submit the revised Field Adaptation Policy v2.0 for board review by end of month." | YES | P5 | Concrete action steps |
| D | "Further investigation may be needed. What do you think?" | NO | Anti-P5 (open question, no recommendation) | Anti-preference |
| E | Descriptive filename: 'Bogota Curriculum Adaptation Resolution Plan'. | YES | P2 | Descriptive naming |

- **answer:** `["A", "C", "E"]`
- **evidence_source:** P1-P5 calibration

---

### Round r29: Comprehensive Resolution Document (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Full resolution with dual-track (substance + process)
- User instruction: "Generate a comprehensive curriculum adaptation resolution document. Main file: `GlobalBridge Bogota Curriculum Adaptation Comprehensive Resolution.md`. Evidence appendix: `Bogota Adaptation Evidence Index.md`. Present student impact first, distinguish substance from process, end with concrete action steps."
- Checks:
  - A: file `GlobalBridge Bogota Curriculum Adaptation Comprehensive Resolution.md` exists
  - A: file `Bogota Adaptation Evidence Index.md` exists
  - B: main document contains keywords ["shame", "Module 5", "assessment equivalence", "p = 0.73", "Dhaka precedent", "19 days", "formalize", "Pemberton", "policy gap", "recommendation"]
  - D: student impact before M&E analysis; substance and process clearly separated; concrete action steps at end
- Correct: all checks pass
- Evidence required: all workspace and update files

---

### Round r30: Final Synthesis -- Dual Resolution Path -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which elements should be in the recommended resolution?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Substantive validation: the adaptation preserved learning outcomes (p = 0.73), improved engagement (35pp), and eliminated active content harm. | YES | prof_dubois_comparison.md + bogota_focus_group_report.md | Substance resolved |
| B | Process formalization: retroactively formalize the Bogota adaptation using the Dhaka Cycle 4 approval framework. | YES | dhaka_adaptation_approval.md + analysis | Process resolution |
| C | Policy reform: adopt Field Adaptation Policy v2.0 with clear CAR process, 15-day review timeline, and pre-approved contextual substitutions. | YES | field_adaptation_policy_draft.md | Governance fix |
| D | Grant compliance: file proactive disclosure with Pemberton per Section 6.3 notification requirement. | YES | pemberton_grant_terms_excerpt.md + Rachel's flag | Compliance path |
| E | Reverse the adaptation and return to the standard curriculum because the process was unauthorized. | NO | The outcome data validates the adaptation; reversing it would reintroduce the harm | Process over substance error |
| F | Recognize Carlos's substantive judgment was correct while acknowledging the governance failure was partly organizational (policy opacity). | YES | Comprehensive analysis | Nuanced assessment |
| G | Use Sophie's content-vs-assessment distinction as the analytical framework: content examples are adaptable; assessment methodology is not. | YES | Sophie Phase 2 + Dubois analysis | Analytical framework |
| H | Present the resolution using Fatima's preferred style: student experiences first, then M&E methodology, ending with concrete action steps. | YES | P1-P5 | Format compliance |
| I | Discipline Carlos for unauthorized changes without acknowledging the organizational contribution to his decision. | NO | The policy gap contributed to his decision; discipline without systemic fix is incomplete | Partial attribution |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** Comprehensive synthesis

---

## 3. Reversal Matrix

| Reversal Pair | Contradiction | What Changes | Trigger |
|---|---|---|---|
| r2 -> r9 | C1 partial | Fidelity essential -> community focus group shows content harm | Update 2 (bogota_focus_group_report.md) |
| r2 -> r16 | C1 full | Fidelity essential -> outcome equivalence confirmed | Update 3 (prof_dubois_comparison.md) |
| r3 -> r8 | C2 | Carlos "certain no" -> Dhaka approval in 19 days | Update 1 (dhaka_adaptation_approval.md) |
| r4 -> r12 | C4 | Sophie defends fidelity -> Sophie distinguishes content from assessment | Update 2 (focus group data) |
| r7 (B1) | B1 | "Fidelity essential" -> content adaptation does not undermine evidence base | Update 2 |
| r11 (B2) | B2 | "Engagement sufficient" -> both engagement AND outcomes needed | Update 3 |

---

## 4. Personalization Scoring Notes

| Preference | What to Check | Positive Signal | Negative Signal |
|---|---|---|---|
| P1 (narrative with case illustrations) | Classroom scenarios ground analysis | "When Module 5 presented 'Ask your father'..." | Abstract principle statements |
| P2 (descriptive file naming) | Situation context in filename | 'Bogota Curriculum Adaptation Review' | 'Review_v2.md' |
| P3 (student/community before M&E) | Impact section first | Student voices lead the document | M&E methodology leads |
| P4 (qualitative richness over dashboards) | Case examples over pure numbers | Student quotes and community experiences | Score tables without context |
| P5 (concrete action steps) | Specific recommendations at end | "Formalize within 15 business days" | "Further investigation needed" |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Tested |
|---|---|
| curriculum_compliance_report_w1.md | r2, r13 |
| standard_curriculum_v2.1_excerpt.md | r2, r6 |
| bogota_engagement_data.md | r1, r6, r11 |
| field_adaptation_policy_current.md | r3, r19 |
| pemberton_grant_terms_excerpt.md | r21 |
| dhaka_curriculum_log.md | r1, r3 |
| dhaka_adaptation_approval.md (U1) | r8, r24 |
| bogota_focus_group_report.md (U2) | r9, r10, r14 |
| prof_dubois_comparison.md (U3) | r16, r17, r18, r23 |
| field_adaptation_policy_draft.md (U4) | r20, r21, r27 |
| Carlos Discord DM | r2, r3, r6, r11, r19 |
| Rahman Telegram DM | r3, r8, r26 |
| Sophie Slack DM | r4, r7, r12 |
| Dubois Discord DM | r16, r18 |
| #curriculum-review Slack | r7 |
| #bogota-ops Discord | r9, r14 |
