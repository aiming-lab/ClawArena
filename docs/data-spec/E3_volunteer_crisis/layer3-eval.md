# Layer 3 -- Eval Questions Spec

> Format: `multi_choice` (8-10 options, n-of-many, agent selects via `\bbox{A,C,F}`) and `exec_check` (file generation with automated checks).
> Scoring: exact set match for multi_choice; automated check pass/fail for exec_check.
> All question text and option text must be in English.
> ~30 rounds covering MS, DU, P, exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | calibration | Activity log cross-source synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | calibration | Volunteer self-assessments vs initial complaints (C1 Phase 1 seed) | No | Yes (r2->r7 seed) |
| r3 | multi_choice | calibration | Carlos selection theory vs Rahman orientation theory (C2 Phase 1) | No | Yes (r3->r19 seed) |
| r4 | multi_choice | calibration | Jennifer's crisis framing (C4 Phase 1 seed) | No | Yes (r4->r13 seed) |
| r5 | multi_choice | calibration-P | Preference calibration: narrative-first, community context, warm tone | No | No |
| r6 | multi_choice | MS-R | Bogota community feedback -- contradiction with self-assessments | Yes (Update 1) | Yes (r2->r6 partial) |
| r7 | multi_choice | DU-R | Dhaka community feedback -- full C1 reversal across both sites | Yes (Update 2) | Yes (r2->r7 via C1) |
| r8 | exec_check | MS+P | Generate community feedback comparison memo with narrative framing | Yes (Update 2) | No |
| r9 | multi_choice | MS-I | Self-assessment measurement gap -- volunteer satisfaction vs community reception | Yes (Update 2) | No |
| r10 | multi_choice | MS-I | Bias identification -- B1 from Carlos DM | No | No |
| r11 | exec_check | DU+P | Generate root-cause analysis with descriptive file naming | Yes (Update 2) | No |
| r12 | multi_choice | MS-I | Bias identification -- B2 from Rahman diary entries | No | No |
| r13 | multi_choice | DU-R | Jennifer's severity acknowledgment (C4 Phase 2) | Yes (Update 3) | Yes (r4->r13 via C4) |
| r14 | exec_check | DU+MS | Generate communications assessment memo | Yes (Update 3) | No |
| r15 | multi_choice | MS+DU | Cross-program pattern -- Bogota + Dhaka community data alignment | Yes (Update 2) | No |
| r16 | multi_choice | P-R | Silent exam -- community-first formatting preference | No | No |
| r17 | multi_choice | DU-I | Rahman diary contradiction -- volunteer intent vs community experience | Yes (Update 2) | No |
| r18 | exec_check | MS+DU+P | Generate volunteer crisis board briefing | Yes (Update 3) | No |
| r19 | multi_choice | DU-R | Policy gap analysis -- both theories as symptoms (C2 resolution) | Yes (Update 4) | Yes (r3->r19 via C2) |
| r20 | multi_choice | DU-I | Sophie's measurement gap acknowledgment | Yes (Update 4) | No |
| r21 | exec_check | DU+P | Generate policy reform recommendation document | Yes (Update 4) | No |
| r22 | multi_choice | DU-R | Cross-round reversal review: root cause r3->r19 | Yes (Update 4) | Comprehensive |
| r23 | multi_choice | MS-R | Non-conflict synthesis: activity logs across all sources (C3) | No | No |
| r24 | exec_check | P+MS | Generate stakeholder communication plan with community framing | Yes (Update 4) | No |
| r25 | multi_choice | MS+DU+P | Comprehensive source reliability ranking | Yes (Update 4) | Comprehensive |
| r26 | multi_choice | MS-I | Omar's Nairobi comparison -- triangulating evidence for orientation theory | No | No |
| r27 | exec_check | DU+MS | Generate policy gap remediation plan | Yes (Update 4) | No |
| r28 | multi_choice | P-I | Silent exam -- warm collaborative tone with stakeholder awareness | No | No |
| r29 | exec_check | MS+DU+P | Generate comprehensive crisis response strategy | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final synthesis -- recommended response path | Yes (Update 4) | Comprehensive |

---

## 2. Round Specs

### Round r1: Activity Log Synthesis (C3, non-conflict) -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on workspace documents and session history, which statements about volunteer activity logs are confirmed across multiple independent sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | All 10 volunteers (4 Bogota, 6 Dhaka) are present at assigned sites during assigned hours per HQ tracking, Carlos's local logs, and Rahman's Dhaka summary. | YES | volunteer_activity_log.md + Carlos DM + Rahman DM | C3 non-conflict |
| B | Volunteer hours, locations, and assigned activities are consistent across Fatima's HQ spreadsheet, Carlos's Bogota tracking, and Rahman's Dhaka records. | YES | Cross-source synthesis | C3 confirmation |
| C | The activity logs show 2 of 6 Dhaka volunteers missed multiple scheduled sessions. | NO | All volunteers are present at assigned sites; the crisis is about quality, not attendance | Fabricated absence |
| D | The activity log data confirms volunteers are where they should be -- the crisis is about quality of interactions, not presence at sites. | YES | volunteer_activity_log.md + C3 analysis | Critical insight |
| E | Carlos's local tracking data and the HQ spreadsheet show identical hours and site assignments for all 4 Bogota volunteers. | YES | volunteer_activity_log.md + Carlos DM | C3 consistency |
| F | Activity log consistency does not speak to community reception or interaction quality. | YES | Layer 0 / SOUL.md | Source-type awareness |
| G | Rahman and Carlos both independently flagged the same volunteer assignment discrepancy in the HQ log. | NO | No discrepancy flagged; logs are consistent | Fabricated issue |
| H | The 10 volunteers across both sites are deployed to 5 locations total: 2 in Bogota and 3 in Dhaka. | YES | volunteer_activity_log.md | Direct fact |

- **answer:** `["A", "B", "D", "E", "F", "H"]`
- **question_class:** `calibration`

---

### Round r2: Self-Assessments vs Initial Complaints (C1 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P1 preference injection: User says before r2: "I need the community perspective first -- what are people on the ground experiencing? Then tell me what the data shows."
- Question: "Based on the volunteer self-assessments and initial field director communications, which statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | All 10 volunteers rate their community engagement as "positive" or "very positive" in Week 1 self-assessments. | YES | volunteer_self_assessments.md | C1 Source A |
| B | Three Dhaka volunteers describe local learning centers as "under-resourced" and "in need of our structured approach." | YES | volunteer_self_assessments.md | Near-signal: condescension indicator |
| C | Carlos reports two Bogota school principals have complained about volunteer behavior including photo-taking without consent and correcting teachers in front of students. | YES | Carlos Discord DM Loop 1 | C1 counter-signal |
| D | Rahman reports three local staff members submitted a formal written complaint citing five specific incidents. | YES | Rahman Telegram DM Loop 1 | C1 counter-signal |
| E | The self-assessment form asks volunteers about community feedback they have received. | NO | The form does not ask about community feedback received -- it asks only for volunteers' own perception | Measurement gap |
| F | The self-assessment form measures volunteer satisfaction, not community reception -- these are different variables. | YES | Layer 0 + SOUL.md | Source-type distinction |
| G | The self-assessments and the field director complaints are measuring the same thing and one must be wrong. | NO | They measure different variables; both can be simultaneously accurate | False equivalence |
| H | Volunteers are aware that community complaints have been filed about their behavior. | NO | Volunteers are unaware of the complaints at this stage | Information asymmetry |

- **answer:** `["A", "B", "C", "D", "F"]`
- **question_class:** `calibration`

---

### Round r3: Carlos vs Rahman Root Cause (C2 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P2 preference injection: User says before r3: "Use descriptive file names that include the program area -- like 'Bogota Volunteer Community Impact Review' rather than 'Analysis_v2'."
- Question: "Based on Carlos's and Rahman's positions, which statements about the root cause debate are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Carlos argues the root cause is HQ volunteer selection -- wrong people with no cross-cultural experience or language skills. | YES | Carlos Discord DM Loops 2-5 | C2 Source A |
| B | Rahman argues the root cause is orientation and preparation -- same volunteer pool would have performed differently with proper training. | YES | Rahman Telegram DM Loops 2, 6 | C2 Source B |
| C | Rahman's 2022 cohort, which received a 3-day in-country orientation with community co-design, had zero formal complaints. | YES | Rahman Telegram DM Loop 6 | Historical comparison |
| D | Carlos's Bogota orientation for the current cohort was 4 hours long -- less than Rahman's 1-day virtual session. | YES | Carlos DM Loop 3 + Rahman DM Loop 7 | Orientation comparison |
| E | Carlos and Rahman agree on the root cause and are proposing similar solutions. | NO | They explicitly disagree: selection vs orientation | False agreement |
| F | Carlos's 6-year community relationship claim is genuine and verifiable. | YES | Carlos DM Loop 5 + Layer 0 | B1 credibility factor |
| G | Rahman reveals that the 2022 orientation Days 2 and 3 (community-facing components) were eliminated in a budget revision that saved approximately $8,000 across all programs. | YES | Rahman DM Loop 6 | Budget causation |
| H | Both theories are inconsistent with the available evidence and should be rejected. | NO | Both have partial evidence support; the resolution comes from identifying the policy as the common root | Premature rejection |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **question_class:** `calibration`

---

### Round r4: Jennifer's Crisis Framing (C4 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P3 preference injection: User says before r4: "Start with what this means for communities and program participants. The organizational implications come second."
- Question: "Based on Jennifer Adams's communications, which statements about her framing of the situation are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jennifer characterized the situation as "a learning journey for both our volunteers and our host communities." | YES | Layer 0 / Jennifer Slack DM Phase 1 | C4 Phase 1 framing |
| B | Jennifer had received a draft press release query from a freelance journalist in Bogota but did not inform Fatima. | YES | Layer 0 | C4 concealment |
| C | Jennifer described the social media situation to Fatima as "a minor social media flare we're managing." | YES | Layer 0 | C4 minimization |
| D | Jennifer's goal was to prevent negative media coverage before a major donor stewardship event in 3 weeks. | YES | Layer 0 | Strategic motivation |
| E | Jennifer had shared all available information about the situation with Fatima promptly. | NO | Jennifer withheld the press inquiry and minimized severity | False claim |
| F | Jennifer's "learning journey" framing was a genuine analytical assessment of the situation's severity. | NO | It was a deliberate PR strategy, not a good-faith assessment | Strategic vs analytical |
| G | Jennifer's approach is to keep the situation internal and manage the framing. | YES | Layer 0 | C4 containment strategy |
| H | Carlos confirmed to Jennifer that the activist's Twitter account of the incident was accurate. | YES | Carlos DM Loop 7 | Incident accuracy |

- **answer:** `["A", "B", "C", "D", "G", "H"]`
- **question_class:** `calibration`

---

### Round r5: Preference Calibration (P1-P5) -- Calibration (unscored)

- Type: multi_choice
- P4 preference injection: User says before r5: "Give me qualitative insights first -- what community members are saying and experiencing -- then bring in the survey numbers to support."
- P5 preference injection: "Keep the tone warm and collaborative. These are our community partners and the analysis should reflect respect for their perspective."
- Question: "Fatima has expressed presentation preferences. Which approaches align with her stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Lead with community perspectives and program impact before organizational analysis. | YES | P1 + P3 | Preference direct |
| B | Use descriptive file names with program area identifiers. | YES | P2 | Preference direct |
| C | Present qualitative community voices before quantitative survey data. | YES | P4 | Preference direct |
| D | Use warm, collaborative language reflecting respect for community partners. | YES | P5 | Preference direct |
| E | Present a compliance checklist organized by HQ policy section numbers. | NO | Contradicts P1, P3, P4 | Anti-preference |
| F | Use clinical, detached phrasing like "subjects reported negative experiences." | NO | Contradicts P5 | Anti-preference |
| G | Lead with quantitative survey tables before any narrative context. | NO | Contradicts P1, P4 | Anti-preference |
| H | Include stakeholder impact implications alongside data findings. | YES | P5: stakeholder awareness | Preference aligned |

- **answer:** `["A", "B", "C", "D", "H"]`
- **question_class:** `calibration`

---

### Round r6: Bogota Community Feedback (C1 Partial) -- Scored [Update 1 triggers before this round]

- Type: multi_choice
- Question: "After reviewing community_feedback_bogota.md (Update 1), which statements about the Bogota community feedback are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The Bogota survey shows 6 of 8 respondents rating volunteer presence as "neutral" and 2 as "negative." No respondent rates it "positive." | YES | community_feedback_bogota.md | C1 Source B (Bogota) |
| B | Carlos's cover note describes these results as "mixed but not alarming." | YES | Layer 0 | Carlos's minimization |
| C | Two respondents gave unprompted negative comments about photo-taking and teacher correction that were not in Carlos's cover note. | YES | Layer 0 / Maria Santos observation | Missing qualitative data |
| D | The 0/8 positive rating directly contradicts all 4 Bogota volunteer self-assessments, which rated engagement as "positive" or "very positive." | YES | community_feedback_bogota.md vs volunteer_self_assessments.md | C1 contradiction |
| E | Carlos's characterization of "mixed but not alarming" accurately represents the community data. | NO | 0/8 positive is not "mixed" -- it is uniformly non-positive | Minimization identified |
| F | Community members describe specific behaviors (photo-taking without consent, correcting teachers publicly) as the source of their negative experience. | YES | community_feedback_bogota.md | Behavioral specificity |
| G | The Bogota community survey was conducted by Maria Santos using GlobalBridge's standard 3-question Likert scale. | YES | Layer 0 | Methodology detail |
| H | The behaviors community members cite (photo-taking, teacher correction) would have been preventable with proper orientation, not by selecting different volunteers. | YES | Synthesis: behaviors are procedural, not character-based | C2 evidence implication |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** community_feedback_bogota.md, volunteer_self_assessments.md

---

### Round r7: Dhaka Community Feedback -- Full C1 Reversal -- Scored [Update 2 triggers before this round]

- Type: multi_choice
- Question: "After reviewing community_feedback_dhaka.md (Update 2), which statements about the full community feedback picture are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Dhaka formal findings show 15 of 20 participants report neutral-to-negative experiences. Only 2 of 20 report positive experiences. | YES | community_feedback_dhaka.md | C1 Source B (Dhaka) |
| B | 4 of 20 Dhaka respondents say they would prefer sessions without the international volunteers. | YES | community_feedback_dhaka.md | Severity indicator |
| C | Community members report feeling that volunteers "treated us like we did not know how to raise our children or teach." | YES | community_feedback_dhaka.md (8/12 in informal round) | Community voice |
| D | The pattern is the same in both programs: 0/8 positive in Bogota, 2/20 positive in Dhaka. All 10 volunteer self-assessments are positive. | YES | Cross-site synthesis | C1 full contradiction |
| E | The self-assessment/community-feedback gap is the core finding: volunteer satisfaction does not equal community reception. | YES | C1 design | Central insight |
| F | The community feedback data shows the program has completely failed and should be terminated. | NO | Community feedback shows specific behavioral issues, not total program failure | Over-interpretation |
| G | Rahman's framing: "That gap is the finding" -- identifying the measurement discrepancy as the primary analytical output. | YES | Rahman DM Loop 17 | Analytical precision |
| H | The HQ policy does not require community feedback collection, which is why this data only exists because Rahman proactively gathered it. | YES | volunteer_policy_hq.md + Rahman DM Loop 5 | Policy gap |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **evidence_source:** community_feedback_dhaka.md, community_feedback_bogota.md, volunteer_self_assessments.md

---

### Round r8: Community Feedback Comparison (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Narrative-first cross-site comparison
- User instruction: "Generate a comparison of community feedback from Bogota and Dhaka alongside volunteer self-assessments. Save it as `GlobalBridge Volunteer Community Feedback Comparison.md`. Present community voices first."
- Checks:
  - A: file `GlobalBridge Volunteer Community Feedback Comparison.md` exists
  - B: contains keywords ["community", "self-assessment", "positive", "negative", "neutral", "6/8", "15/20", "photo-taking", "condescension", "measurement gap"]
  - D: has markdown headers with community feedback section before self-assessment analysis
- Correct: all checks pass
- Evidence required: community_feedback_bogota.md, community_feedback_dhaka.md, volunteer_self_assessments.md

---

### Round r9: Self-Assessment Measurement Gap -- Scored

- Type: multi_choice
- Question: "Based on all evidence about the self-assessment form and community feedback, which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The self-assessment form measures the wrong variable: it captures volunteer perception of engagement, not community reception. | YES | volunteer_self_assessments.md design + C1 analysis | Core measurement gap |
| B | The form's design is an HQ artifact that measures volunteer satisfaction, not community impact. | YES | Layer 0 | Design criticism |
| C | Agreement among 10 volunteers (all positive) represents high multi-source corroboration of community satisfaction. | NO | All 10 sources are from the same population measuring the same variable (their own perception); same-population agreement is not multi-source corroboration | T1 trap |
| D | The volunteers are lying about their community engagement perception. | NO | Volunteers genuinely perceive their engagement as positive; the issue is measurement design, not dishonesty | Motive misattribution |
| E | Sophie designed the self-assessment form and knows it measures volunteer perception, not community reception. | YES | Layer 0 / Sophie character | Design knowledge |
| F | The policy failure is that no instrument exists to capture community feedback by default. | YES | volunteer_policy_hq.md + Rahman DM Loop 5 | Systemic gap |
| G | If the self-assessment form included a question about community feedback received, the measurement gap might have been detected earlier. | YES | Form design analysis | Counterfactual |
| H | The community feedback data and self-assessment data are measuring the same thing but arriving at different conclusions, meaning one must be fabricated. | NO | They measure different variables (volunteer perception vs community experience); both are genuine | False equivalence |

- **answer:** `["A", "B", "E", "F", "G"]`
- **evidence_source:** volunteer_self_assessments.md, volunteer_policy_hq.md, community feedback files

---

### Round r10: B1 Bias Identification -- Scored

- Type: multi_choice
- Question: "Carlos stated: 'My team has deep community relationships built over six years. These volunteers were simply not prepared for the realities of our community context. The issue starts at selection, not at deployment.' Which assessments of this framing are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Carlos's 6-year community relationship claim is genuine and verifiable -- his community access is real. | YES | Carlos DM Loop 5 + Layer 0 | Credibility confirmed |
| B | Carlos's selection theory is partially supported: the volunteers do lack cross-cultural experience and language skills. | YES | Carlos DM Loop 3 | Partial support |
| C | Carlos's selection theory does not account for the fact that his own Bogota orientation was only 4 hours long. | YES | Carlos DM Loop 3 + Rahman DM Loop 7 | Self-serving omission |
| D | The community feedback data shows behaviors (photo-taking, teacher correction) that would have been addressed by proper orientation, not by selecting different volunteers. | YES | community_feedback_bogota.md + analysis | Orientation-preventable behaviors |
| E | Carlos's passionate defense of his community relationships makes his selection theory more analytically sound. | NO | Passion and community relationships do not validate a causal claim about root cause | Credibility-logic conflation |
| F | Carlos deflects responsibility from his own abbreviated orientation program onto HQ selection. | YES | Layer 0 + Carlos DM analysis | Motivated framing |
| G | An agent anchoring on Carlos's narrative authority will under-weight the community feedback when it arrives. | YES | B1 design | Bias mechanism |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** Carlos Discord DM, community_feedback_bogota.md

---

### Round r11: Root-Cause Analysis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Multi-theory analysis with community framing
- User instruction: "Generate a root-cause analysis comparing Carlos's selection theory and Rahman's orientation theory against the community feedback evidence. Save it as `GlobalBridge Volunteer Crisis Root-Cause Analysis.md`. Present community impact first."
- Checks:
  - A: file `GlobalBridge Volunteer Crisis Root-Cause Analysis.md` exists
  - B: contains keywords ["selection", "orientation", "community feedback", "4-hour", "3-day", "2022 cohort", "policy gap", "photo-taking", "condescension"]
  - D: has markdown headers with community impact before theoretical analysis
- Correct: all checks pass
- Evidence required: community_feedback_bogota.md, community_feedback_dhaka.md, Carlos DM, Rahman DM, volunteer_policy_hq.md

---

### Round r12: B2 Bias Identification -- Scored

- Type: multi_choice
- Question: "Rahman shared volunteer diaries and stated: 'I've sent you the week-by-week volunteer diaries. You can see how much energy and enthusiasm they brought. The learning is happening -- just not in the way the numbers capture.' Which assessments are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The volunteer diaries are genuine and show real effort and connection from the volunteers' perspective. | YES | Rahman DM Loop 3 | Diary authenticity |
| B | The diaries capture volunteer experience, not community experience -- the same measurement gap as the self-assessments. | YES | B2 design + community feedback comparison | Source-type awareness |
| C | Rahman herself later revised this framing, noting that a volunteer's diary entry about "empowering the community" sat alongside a community member's account of feeling condescended to. | YES | Rahman DM Loop 18 | B2 self-correction |
| D | The diary entries and community feedback represent "two coherent accounts of the same events from different perspectives." | YES | Rahman DM Loop 18 | Dual-perspective insight |
| E | The diary evidence proves the volunteers are having a positive impact regardless of what community members report. | NO | Volunteer intent and community reception are different outcomes; the diary does not measure community impact | Over-weighting intent |
| F | Rahman's self-correction demonstrates appropriate epistemic updating when community evidence becomes available. | YES | Rahman DM Loop 18 | Epistemic virtue |
| G | An agent anchoring on vivid diary narratives will over-weight volunteer intent over community reception. | YES | B2 design | Bias mechanism |

- **answer:** `["A", "B", "C", "D", "F", "G"]`
- **evidence_source:** Rahman Telegram DM Loops 3, 18, community_feedback_dhaka.md

---

### Round r13: Jennifer's Severity Acknowledgment (C4 Phase 2) -- Scored [Update 3 triggers before this round]

- Type: multi_choice
- Question: "Based on Jennifer's Phase 2 communications, which statements about her position shift are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jennifer acknowledged for the first time that the situation is "more serious than initially communicated." | YES | Layer 0 / Jennifer Slack DM Phase 2 | C4 reversal |
| B | Jennifer admitted she had been managing optics rather than substance. | YES | Layer 0 | C4 admission |
| C | Jennifer disclosed that she had been aware of a press inquiry from W1D5 that she did not share with Fatima. | YES | Layer 0 | Concealment revealed |
| D | Jennifer's "learning opportunity" framing was a deliberate PR strategy, not an analytical assessment of the situation. | YES | C4 analysis | Strategic vs analytical |
| E | Jennifer changed her position because new evidence convinced her the situation was more serious. | NO | Jennifer changed because social media pressure and Fatima's direct inquiry forced the admission, not because she received new evidence | Pressure-driven, not evidence-driven |
| F | Jennifer's delay in informing Fatima about the press inquiry materially delayed the organization's response. | YES | Layer 0 | Impact of concealment |
| G | Jennifer's concealment was malicious and intended to harm the organization. | NO | She genuinely believed she could resolve the situation quietly; her misjudgment was about capability, not intent | Motive over-attribution |
| H | Jennifer's Phase 2 admission is the first time she provides an honest assessment of the situation's severity. | YES | C4 Phase 1 vs Phase 2 | Temporal shift |

- **answer:** `["A", "B", "C", "D", "F", "H"]`
- **evidence_source:** Jennifer Slack DM Phase 1 + Phase 2

---

### Round r14: Communications Assessment (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Assess Jennifer's communications handling with evidence
- User instruction: "Generate a communications assessment documenting Jennifer's framing evolution from Phase 1 to Phase 2. Save it as `GlobalBridge Volunteer Crisis Communications Assessment.md`."
- Checks:
  - A: file `GlobalBridge Volunteer Crisis Communications Assessment.md` exists
  - B: contains keywords ["learning journey", "minor social media", "press inquiry", "more serious", "optics", "community trust", "concealment"]
  - D: has markdown headers with timeline structure
- Correct: all checks pass
- Evidence required: Jennifer Slack DM Phase 1 + Phase 2

---

### Round r15: Cross-Program Pattern -- Scored

- Type: multi_choice
- Question: "Based on community feedback from both sites, which statements about the cross-program pattern are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The pattern is consistent across both programs: 0/8 positive in Bogota, 2/20 positive in Dhaka, while all 10 self-assessments are positive. | YES | Cross-site synthesis | C1 cross-program |
| B | The consistency of the pattern across two different countries, cultures, and field directors suggests a systemic cause rather than a site-specific one. | YES | Cross-site analysis | Systemic inference |
| C | The Bogota and Dhaka issues are unrelated coincidences with no common cause. | NO | Same pattern, same policy framework, same orientation deficiency | False independence |
| D | Both community feedback instruments show the same direction: neutral-to-negative reception despite positive volunteer self-perception. | YES | community_feedback_bogota.md + community_feedback_dhaka.md | Pattern confirmation |
| E | The cross-program consistency undermines Carlos's Bogota-specific selection argument -- the same pattern appears in Dhaka with a different volunteer pool. | YES | C2 evidence | Selection theory weakened |
| F | Rahman's question -- "What are we not seeing in Bogota because community feedback isn't collected by default?" -- is answered: the same pattern that Dhaka found proactively. | YES | Rahman DM Loop 5 + Bogota feedback | Question answered |

- **answer:** `["A", "B", "D", "E", "F"]`
- **evidence_source:** community_feedback_bogota.md, community_feedback_dhaka.md, volunteer_self_assessments.md

---

### Round r16: Silent Exam -- Community-First Formatting -- Scored

- Type: multi_choice
- Question: "Which output characteristics comply with Fatima's stated preferences for a volunteer crisis briefing?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Opening with community member quotes describing their experience with volunteers. | YES | P1 + P4 | Narrative/qualitative first |
| B | Descriptive filename like 'Bogota Dhaka Volunteer Community Impact Analysis'. | YES | P2 | Descriptive naming |
| C | Community impact section before organizational/policy analysis. | YES | P3 | Impact first |
| D | Warm, respectful language acknowledging community partners' perspectives. | YES | P5 | Collaborative tone |
| E | Leading with a compliance checklist of volunteer policy violations. | NO | Contradicts P1, P3 | Anti-preference |
| F | Clinical language like "respondents indicated suboptimal experiences." | NO | Contradicts P5 | Anti-preference |

- **answer:** `["A", "B", "C", "D"]`
- **evidence_source:** P1-P5 calibration

---

### Round r17: Rahman Diary Contradiction -- Scored

- Type: multi_choice
- Question: "Rahman noted that a volunteer diary entry about 'a student understanding a concept for the first time' sat alongside a community member's account of feeling that the volunteer 'spoke to my child as if I was not present.' Which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Both accounts describe the same session from different perspectives and both are genuine. | YES | Rahman DM Loop 18 | Dual-perspective |
| B | The volunteer experienced a genuine moment of connection; the community member experienced condescension. These are not mutually exclusive. | YES | Rahman DM Loop 18 analysis | Compatibility |
| C | The diary captures the volunteer's half of the exchange; the community feedback captures the other half. | YES | Rahman DM Loop 18 | Measurement completeness |
| D | This demonstrates why the policy should require both volunteer and community feedback instruments. | YES | Rahman DM Loop 18 + policy analysis | Policy implication |
| E | One account must be fabricated because they describe the same event differently. | NO | Different-perspective accounts of the same event are a standard phenomenon, not evidence of fabrication | False exclusivity |
| F | The volunteer diary is a more reliable source because it was written closer to the event. | NO | Proximity to the event does not determine which perspective is more relevant for assessing community reception | Reliability conflation |

- **answer:** `["A", "B", "C", "D"]`
- **evidence_source:** Rahman Telegram DM Loop 18

---

### Round r18: Board Briefing (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Comprehensive briefing testing multi-cause tolerance
- User instruction: "Generate a board briefing on the volunteer crisis. Save it as `GlobalBridge Volunteer Crisis Board Briefing.md`. Present community impact first, then the measurement gap, then the root-cause analysis acknowledging multiple simultaneous causes."
- Checks:
  - A: file `GlobalBridge Volunteer Crisis Board Briefing.md` exists
  - B: contains keywords ["community feedback", "self-assessment", "measurement gap", "selection", "orientation", "policy gap", "photo-taking", "condescension", "both"]
  - D: has markdown headers with community section before analysis sections
- Correct: all checks pass
- Evidence required: all available evidence through Update 3

---

### Round r19: Policy Gap Resolution (C2 Full) -- Scored [Update 4 triggers before this round]

- Type: multi_choice
- Question: "After reviewing hq_policy_gap_analysis.md (Update 4), which statements about the root cause resolution are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The policy gap analysis identifies 4 specific gaps: no community feedback requirement, no cultural competency screening, no context-differentiated orientation length, no community partner input into volunteer briefing. | YES | hq_policy_gap_analysis.md | C2 resolution |
| B | Sophie's 14-month-old memo to the previous Program Director flagged measurement gaps that were never actioned. | YES | hq_policy_gap_analysis.md | Institutional history |
| C | The 2022 orientation model (3-day, community co-designed) is documented alongside the current model (1-day, logistics only) showing the specific components that were eliminated. | YES | hq_policy_gap_analysis.md | Comparison evidence |
| D | Carlos's selection theory and Rahman's orientation theory are both symptoms of the same underlying policy failure. | YES | hq_policy_gap_analysis.md + Rahman DM Loop 8 | C2 resolution |
| E | The policy analysis proves that Carlos was entirely wrong about selection being a factor. | NO | The policy has no cultural competency screening, which partially supports Carlos; but orientation is the larger gap | Over-rejection |
| F | The budget revision that eliminated the community-facing orientation components saved approximately $8,000 across all programs while creating the conditions for this crisis. | YES | Rahman DM Loop 6 + hq_policy_gap_analysis.md | Cost-consequence analysis |
| G | Omar Farah's Nairobi comparison (2021 cohort with 3-day community co-designed orientation, zero complaints) independently confirms the orientation theory. | YES | Omar DM Loop 2 | Third-site triangulation |
| H | The honest root-cause answer requires acknowledging multiple simultaneous causes (measurement gap + policy gap + communications failure) without collapsing them into one. | YES | T5 trap + comprehensive analysis | Multi-cause requirement |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** hq_policy_gap_analysis.md, Rahman DM, Omar DM, volunteer_policy_hq.md

---

### Round r20: Sophie's Measurement Gap Acknowledgment -- Scored

- Type: multi_choice
- Question: "Based on Sophie's communications, which statements about the self-assessment form design are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sophie designed the volunteer self-assessment form and knows it measures volunteer perception, not community reception. | YES | Layer 0 | Design knowledge |
| B | Sophie acknowledged the measurement gap when directly asked: "I raised the measurement gap in a memo 14 months ago." | YES | Layer 0 / Sophie character | Candid acknowledgment |
| C | Sophie proactively shared her concerns about the form with Fatima before the crisis emerged. | NO | Sophie waited to be asked; she had been "waiting for a Program Director willing to reform the M&E framework" | Passive not proactive |
| D | The form's failure to ask about community feedback received is a design gap, not a data quality issue. | YES | Form analysis | Precise characterization |
| E | Sophie is defensive about the form design and has professional investment in it. | YES | Layer 0 | Character context |

- **answer:** `["A", "B", "D", "E"]`
- **evidence_source:** Sophie character profile, volunteer_self_assessments.md

---

### Round r21: Policy Reform Recommendation (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Forward-looking policy recommendation
- User instruction: "Generate a policy reform recommendation document addressing all four policy gaps identified. Save it as `GlobalBridge Volunteer Policy Reform Recommendations.md`."
- Checks:
  - A: file `GlobalBridge Volunteer Policy Reform Recommendations.md` exists
  - B: contains keywords ["community feedback", "cultural competency", "orientation", "community partner", "3-day", "2022 model", "measurement", "policy gap"]
  - D: has markdown headers with structured sections
- Correct: all checks pass
- Evidence required: hq_policy_gap_analysis.md, volunteer_policy_hq.md

---

### Round r22: Cross-Round Reversal Review -- Scored

- Type: multi_choice
- Question: "Reviewing the root-cause evolution from r3 through r19, which statements about how the picture changed are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | At r3, Carlos's selection theory and Rahman's orientation theory appeared as competing explanations; by r19, both were identified as symptoms of the same policy failure. | YES | r3 vs r19 evidence | C2 reversal |
| B | At r2, volunteer self-assessments appeared to show positive engagement; by r7, community feedback showed a fundamentally different picture. | YES | r2 vs r7 evidence | C1 reversal |
| C | At r4, Jennifer's framing appeared to be a professional assessment; by r13, she admitted it was optics management. | YES | r4 vs r13 evidence | C4 reversal |
| D | The B1 bias (anchoring on Carlos's community authority) and B2 bias (anchoring on vivid diary narratives) were both corrected by community feedback data. | YES | r10 + r12 analysis | Bias corrections |
| E | The final resolution requires a single root cause diagnosis: either selection or orientation, but not both. | NO | The resolution is that both are symptoms of the policy gap; single-cause diagnosis is the T2 trap | False exclusivity |
| F | Rahman was the most consistently reliable source throughout, with her predictions, evidence, and self-corrections validated at every stage. | YES | Rahman across all sessions | Source reliability |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** Cross-round synthesis

---

### Round r23: Activity Log Non-Conflict (C3) -- Scored

- Type: multi_choice
- Question: "Based on all sources, which statements about volunteer activity logs are confirmed with no contradictions?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | All 10 volunteers' hours, locations, and activities are consistent across HQ, Bogota, and Dhaka tracking. | YES | volunteer_activity_log.md + DMs | C3 confirmed |
| B | Activity log consistency means operations are functioning normally and the crisis is overstated. | NO | Logs confirm presence, not interaction quality; T4 trap | False inference |
| C | The logs confirm volunteers are present at sites but say nothing about the quality of their interactions. | YES | C3 + C1 distinction | Precise scope |
| D | Non-conflict data about logistics cannot resolve conflict data about community experience. | YES | SOUL.md principle | Analytical principle |
| E | No source manipulates or underreports volunteer hours or locations. | YES | C3 by design | Data integrity |

- **answer:** `["A", "C", "D", "E"]`
- **evidence_source:** volunteer_activity_log.md, Carlos DM, Rahman DM

---

### Round r24: Stakeholder Communication Plan (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Stakeholder-aware communication with community framing
- User instruction: "Generate a stakeholder communication plan listing all impacted parties and recommended messages. Save it as `GlobalBridge Volunteer Crisis Stakeholder Communication Plan.md`. Put community partners first."
- Checks:
  - A: file `GlobalBridge Volunteer Crisis Stakeholder Communication Plan.md` exists
  - B: contains keywords ["community", "principals", "volunteers", "donor", "board", "media", "policy reform", "orientation"]
  - D: has markdown headers with community stakeholders listed first
- Correct: all checks pass
- Evidence required: all evidence

---

### Round r25: Source Reliability Ranking -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which source reliability assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Rahman is the most structurally reliable source: proactively gathered community feedback, provided historical comparisons, self-corrected her diary framing, and identified the systemic policy cause. | YES | Rahman across sessions | Ranking |
| B | Community feedback reports (Bogota + Dhaka) are the most direct measures of community reception, which is the relevant variable for this crisis. | YES | C1 analysis | Source relevance |
| C | Carlos is partially reliable: his community relationships are real, his incident descriptions are accurate, but his root-cause diagnosis is self-serving. | YES | Carlos analysis | Nuanced assessment |
| D | Jennifer is the least reliable source in Phase 1 due to deliberate severity minimization; her Phase 2 admission corrects this. | YES | C4 analysis | Temporal reliability |
| E | The volunteer self-assessments are reliable measures of volunteer perception but irrelevant to the core question of community reception. | YES | C1 measurement gap | Source-variable precision |
| F | Omar provides clean triangulating evidence from a third site that confirms the orientation theory. | YES | Omar DM Loops 1-3 | Independent corroboration |
| G | Carlos is entirely unreliable and his observations should be disregarded. | NO | His community relationships and incident descriptions are genuine; only his causal diagnosis is questionable | Over-rejection |

- **answer:** `["A", "B", "C", "D", "E", "F"]`
- **evidence_source:** Cross-session synthesis

---

### Round r26: Omar Nairobi Comparison -- Scored

- Type: multi_choice
- Question: "Based on Omar's account of the 2021 Nairobi volunteer cohort, which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The 2021 Nairobi cohort had a 3-day in-person orientation with community partners co-designing the volunteer briefing sessions. | YES | Omar DM Loop 2 | Direct fact |
| B | The 2021 cohort's community reception was significantly better: 3 volunteers were invited back by community partners. | YES | Omar DM Loop 1 | Outcome comparison |
| C | Two of the best 2021 Nairobi volunteers had zero development experience, suggesting orientation mattered more than selection. | YES | Omar DM Loop 3 | Counter to selection theory |
| D | Omar is politically invested in the orientation vs selection debate. | NO | Omar is not politically invested; he provides clean comparative data | False motive |
| E | The Nairobi comparison provides a third independent data point confirming that community co-designed orientation correlates with better community reception. | YES | Omar DM synthesis | Triangulation |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** Omar Telegram DM Loops 1-3

---

### Round r27: Policy Gap Remediation Plan (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Specific remediation with realistic timelines
- User instruction: "Generate a remediation plan addressing all policy gaps with specific actions and timelines. Save it as `GlobalBridge Volunteer Policy Remediation Plan.md`."
- Checks:
  - A: file `GlobalBridge Volunteer Policy Remediation Plan.md` exists
  - B: contains keywords ["immediate", "short-term", "long-term", "community feedback", "cultural competency", "orientation", "3-day", "$8,000", "policy"]
  - D: has structured sections with timeline markers
- Correct: all checks pass
- Evidence required: hq_policy_gap_analysis.md, Rahman DM Loop 19

---

### Round r28: Silent Exam -- Warm Collaborative Tone -- Scored

- Type: multi_choice
- Question: "Which language choices comply with Fatima's preference for warm, collaborative tone with stakeholder awareness?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | "Our community partners in Bogota and Dhaka have shared feedback that helps us understand how volunteers are experienced on the ground." | YES | P5 | Warm, participatory |
| B | "Subjects reported suboptimal engagement metrics in treatment conditions." | NO | Clinical, contradicts P5 | Anti-preference |
| C | "Working alongside our field teams and community leaders, we have identified specific areas where our orientation approach needs strengthening." | YES | P5 | Collaborative framing |
| D | "The volunteers failed and the communities are dissatisfied." | NO | Harsh, not collaborative | Anti-preference |
| E | "Community members describe their experience in ways that help us see the full picture -- not just the volunteers' perspective, but the community's perspective too." | YES | P5 + P1 | Stakeholder awareness |

- **answer:** `["A", "C", "E"]`
- **evidence_source:** P5 preference calibration

---

### Round r29: Comprehensive Crisis Response (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Full synthesis document
- User instruction: "Generate a comprehensive crisis response strategy. Main file: `GlobalBridge Comprehensive Volunteer Crisis Response.md`. Evidence index: `GlobalBridge Crisis Evidence Summary.md`. Present community impact first, acknowledge multiple simultaneous causes, provide specific remediation steps."
- Checks:
  - A: file `GlobalBridge Comprehensive Volunteer Crisis Response.md` exists
  - A: file `GlobalBridge Crisis Evidence Summary.md` exists
  - B: main document contains keywords ["community", "self-assessment gap", "selection", "orientation", "policy", "measurement", "photo-taking", "condescension", "remediation"]
  - D: community section before organizational analysis; warm collaborative tone
- Correct: all checks pass
- Evidence required: all workspace and update files

---

### Round r30: Final Synthesis -- Recommended Path -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which elements should be included in Fatima's recommended response?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Immediate: pause current volunteer activities and conduct re-briefing on boundary protocols at both sites. | YES | Rahman DM Loop 19 | Immediate action |
| B | Short-term: implement community feedback collection as a mandatory program requirement at all volunteer sites. | YES | hq_policy_gap_analysis.md | Policy fix |
| C | Long-term: restore 3-day in-country orientation with community co-design component, modeled on the 2022/2021 successful programs. | YES | hq_policy_gap_analysis.md + Rahman DM + Omar DM | Structural reform |
| D | Terminate all international volunteer programs permanently. | NO | The crisis is about preparation and measurement, not about volunteer programs being inherently harmful | Over-reaction |
| E | Acknowledge both selection and orientation as contributing factors without forcing a single-cause diagnosis. | YES | C2 resolution + T2 trap avoidance | Multi-cause tolerance |
| F | Address Jennifer's communications handling -- ensure future crises have full-information sharing with the Program Director. | YES | C4 resolution | Communications reform |
| G | Frame the response using community voices and community impact first, per Fatima's preferred style. | YES | P1-P5 | Format compliance |
| H | Suppress the community feedback data to protect the volunteer program's reputation. | NO | The data is the basis for meaningful reform; suppression would perpetuate the measurement gap | Concealment |
| I | Recognize that the $8,000 budget saving that eliminated the orientation components has cost far more in crisis management. | YES | Rahman DM Loop 19 | Cost-consequence |

- **answer:** `["A", "B", "C", "E", "F", "G", "I"]`
- **evidence_source:** Comprehensive synthesis

---

## 3. Reversal Matrix

| Reversal Pair | Contradiction | What Changes | Trigger |
|---|---|---|---|
| r2 -> r6 | C1 partial | Self-assessments positive -> Bogota community 0/8 positive | Update 1 (community_feedback_bogota.md) |
| r2 -> r7 | C1 full | Self-assessments -> cross-program negative community reception | Update 2 (community_feedback_dhaka.md) |
| r3 -> r19 | C2 | Selection vs orientation debate -> both symptoms of policy gap | Update 4 (hq_policy_gap_analysis.md) |
| r4 -> r13 | C4 | "Learning opportunity" -> Jennifer admits severity concealment | Update 3 (Jennifer Phase 2) |
| r10 (B1) | B1 | Carlos's selection narrative anchored -> community data contradicts | Update 1 |
| r12 (B2) | B2 | Diary-based engagement anchored -> community perspective reveals other half | Update 2 |

---

## 4. Personalization Scoring Notes

| Preference | What to Check | Positive Signal | Negative Signal |
|---|---|---|---|
| P1 (narrative with community context) | Community story leads analysis | "Community members describe..." before survey data | Pure statistics without context |
| P2 (descriptive file naming) | File names include program area | 'Bogota Volunteer Community Impact Review' | 'Analysis_v2.md' |
| P3 (impact/community before budget) | Community section first | Impact on communities precedes organizational analysis | Policy analysis leads without community framing |
| P4 (qualitative-first) | Community voices before numbers | Quotes and experiences, then percentages | Survey tables without narrative |
| P5 (warm/collaborative tone) | Respectful, participatory language | "Community partners describe" | "Subjects indicated negative outcomes" |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Tested |
|---|---|
| volunteer_policy_hq.md | r7, r9, r19 |
| volunteer_activity_log.md | r1, r23 |
| volunteer_self_assessments.md | r2, r7, r9 |
| community_feedback_bogota.md (U1) | r6, r8, r10, r15 |
| community_feedback_dhaka.md (U2) | r7, r8, r15, r17 |
| hq_policy_gap_analysis.md (U4) | r19, r21, r27 |
| Carlos Discord DM | r2, r3, r6, r10 |
| Rahman Telegram DM | r2, r3, r7, r12, r17 |
| Omar Telegram DM | r26 |
| Jennifer Slack DM | r4, r13 |
| #volunteer-ops Discord Group | r3 |
| #program-coordination Slack Group | r19, r20 |
