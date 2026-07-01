# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).
> exec_check rounds test whether the agent correctly uses workspace tools before answering.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Interview timeline cross-source synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Team-size discrepancy inference -- resume vs reference (C1 partial) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | CTO pressure vs background check -- source tension (C2) | No | Yes (R3->R8 seed) |
| r4 | multi_choice | P-R | User preference identification (bullet summaries, Chinese naming, exec summary first, quali+quanti, professional+warm) | No | No |
| r5 | multi_choice | DU-R | Reassess team-size claim after Huang Lei interview feedback (C1 reversal) | Yes (Update 1) | Yes (R2->R5 via C1) |
| r6 | multi_choice | MS-I, exec_check | Employment gap inference -- GitHub data vs resume claim (C4 partial) | No | Yes (R6->R9 seed) |
| r7 | multi_choice | DU-R | Reassess employment gap after LinkedIn evidence (C4 reversal) | Yes (Update 2) | Yes (R4->R7 via C4) |
| r8 | multi_choice | DU-I | Reassess CTO pressure after Zhang Wei support + CTO "everyone embellishes" (C2 reversal) | Yes (Update 2+4) | Yes (R3->R8 via C2) |
| r9 | multi_choice | DU-R, exec_check | Reassess employment gap after dual-source confirmation (C4 full reversal) | Yes (Update 2) | Yes (R6->R9 via C4) |
| r10 | multi_choice | MD-R | Source reliability -- rank and justify sources for C1 and C4 | No | No |
| r11 | multi_choice | DU-I | Integrate Huang Lei's detailed P6-vs-P7 assessment (Update 3) | Yes (Update 3) | No |
| r12 | multi_choice | DP-I, exec_check | What was B1 bias (CTO deference) and what evidence corrected it? | Yes (Update 1+2) | No |
| r13 | multi_choice | MS-R | Candidate qualifications -- technical competence vs leadership claims separation | No | No |
| r14 | multi_choice | MD-R, exec_check | Reference check reliability -- what did Liu Wei know vs not know? | No | No |
| r15 | multi_choice | MS-I | Process analysis -- what due diligence steps were completed vs skipped? | No | No |
| r16 | multi_choice | P-I | Generate candidate assessment in Chen Jing's preferred format (exec summary, bullet points, quali+quanti) | Yes (Update 3) | No |
| r17 | multi_choice | DU-I, exec_check | Integrate CTO's "everyone embellishes" response with all evidence (Update 4) | Yes (Update 4) | No |
| r18 | multi_choice | MD-I | CTO motivation analysis -- board pressure vs operational need | Yes (Update 2) | No |
| r19 | multi_choice | MP-I | Conflict analysis: CTO urgency vs HR due diligence | Yes (Update 2+4) | No |
| r20 | multi_choice | P-R | User preference compliance check -- does response apply all 5 preferences? | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive candidate assessment -- all evidence integrated | Yes (all updates) | Yes (R2+R6 comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm all sources consistent on interview timeline | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- what was the exact phrase and why was it wrong? | Yes (Update 2) | No |
| r24 | multi_choice | MS-I, exec_check | Candidate's evolving narrative -- interview hesitation vs resume confidence | Yes (Update 1) | No |
| r25 | multi_choice | P-I | Format the hire recommendation in Chen Jing's preferred style | Yes (Update 3) | No |
| r26 | multi_choice | MD-I | What should Chen Jing do next -- action recommendation with priorities | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Huang Lei assessment corroboration -- does his view align with reference and GitHub? | Yes (Update 3) | No |
| r28 | multi_choice | MP-I | Stakeholder dynamics analysis -- CTO, HR VP, TL, recruiter roles | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Risk assessment -- what happens if company hires at P7 despite findings? | No | No |
| r30 | multi_choice | MDP-I | Final comprehensive assessment -- all contradictions resolved, all biases corrected | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9 out of 30 = 30% (within 20-40% target)

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, timing, or scope is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics real content |

---

## 3. Round Specs

### R1: Interview Timeline Cross-Source Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read candidate-resume.md` before answering. If agent answers without referencing workspace files, exec_check fails.

**User calibration message before R1:** "我习惯看分层列表总结，先看结论再看证据。请用项目符号和标题分层输出。"

**Question:**
> "Based on workspace documents and session history, which statements about the candidate evaluation timeline are supported by evidence? (Before answering, make sure you've reviewed the workspace files.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The CTO sent a hiring priority email on W1 Day 1 requesting expedited hiring for a senior backend engineer position, framing it as business-critical. | YES | cto-hiring-priority-email.md | Direct fact, C3 synthesis |
| B | Wang Hao's resume was received on W1 Day 2 through the company's recruitment pipeline, listing 8 years of backend experience at StarBridge Tech. | YES | candidate-resume.md + Liu Yang IM Loop 1 | Cross-source corroboration, C3 |
| C | The phone screen was conducted on W1 Day 3, with Liu Yang reporting a positive technical communication assessment. | YES | Liu Yang IM Loop 2 | Direct fact, C3 |
| D | The reference check email from Liu Wei was received on W1 Day 3, the same day as the phone screen. | NO | reference-check-emails.md shows W1D4 | Wrong timing |
| E | The reference check email from Liu Wei (former director at StarBridge) was received on W1 Day 4, describing Wang Hao as having managed "about 4 engineers." | YES | reference-check-emails.md | Direct fact, C1 source B |
| F | The technical interview with Huang Lei was conducted on W1 Day 4, one day before the reference check. | NO | Huang Lei Email Loop 1 schedules W1D5 | Wrong timing |
| G | GitHub contribution data was reviewed on W1 Day 5, revealing a 6-month gap from June to December 2023. | YES | github-contribution-export.md + Liu Yang IM Loop 5 | Direct fact, C4 source B |
| H | All available timeline sources -- CTO email, recruiter IM, email thread with Huang Lei -- are consistent with each other on the sequence of events. | YES | Cross-source confirmation | C3 non-conflict conclusion |
| I | The CTO reviewed the reference check findings before pushing for an expedited offer. | NO | Li Qiang Feishu DM shows no reference check review | Fabricated CTO diligence |

**answer:** `["A", "B", "C", "E", "G", "H"]`

**question_class:** `calibration` (R1 establishes P1 preference baseline -- agent should respond with bullet-point structure)

---

### R2: Team-Size Discrepancy Inference (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "输出格式：先执行摘要（一两句话结论），再分层展开证据。我要先看到重点。"

**Question:**
> "Based on all currently available evidence (before any interview feedback updates), which statements about the team-size discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Wang Hao's resume claims he "led a cross-functional team of 12 engineers" on the microservices migration at StarBridge Tech. | YES | candidate-resume.md | Direct quote, C1 Source A |
| B | Liu Wei's reference check email states Wang Hao "managed a team of about 4 engineers," directly contradicting the resume's claim of 12. | YES | reference-check-emails.md | Direct quote, C1 Source B |
| C | The discrepancy between "12 engineers" (resume) and "about 4 engineers" (reference) represents a 3x inflation that materially misrepresents the candidate's management scope. | YES | Quantitative comparison of C1 sources | C1 discrepancy framing |
| D | Liu Wei's reference email suggests Wang Hao may have exaggerated because Liu Wei describes the team as "approximately 12, give or take." | NO | Liu Wei says "about 4," not "approximately 12" | Fabricated reference statement |
| E | The reference from Liu Wei is from a personal friend of Wang Hao's, which should be considered when assessing the reliability of the positive aspects of the reference. | YES | Layer 0 states Liu Wei is a personal friend | Source reliability context |
| F | At this stage (before interview feedback), there are two sources addressing team size: the resume (12) and the reference (4). The reference is from an independent third party and has higher evidentiary weight than self-reported resume claims. | YES | Source reliability principle from SOUL.md | Correct source weighting |
| G | The two panel members who interviewed Wang Hao both confirmed his team size was closer to 4 than 12. | NO | Panel members did not probe team size (interview-feedback-forms.md initial) | Fabricated panel confirmation |
| H | The "cross-functional team" framing on the resume could mean Wang Hao counted project collaborators from other teams as his "team," which would explain the inflation from 4 direct reports to 12 project participants. | YES | Logical inference from resume language + reference data | Plausible explanation (later confirmed by interview) |

**answer:** `["A", "B", "C", "E", "F", "H"]`

**question_class:** `calibration` (P3 exec-summary-first preference established)

---

### R3: CTO Pressure vs Background Check -- Source Tension (MS-R) -- C2

**Question:**
> "Based on all currently available evidence, which statements about the tension between CTO hiring urgency and background check findings are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | CTO Li Qiang's email frames the hire as "business-critical" and requests an offer within two weeks. | YES | cto-hiring-priority-email.md | Direct fact, C2 source A |
| B | The CTO reviewed the reference check discrepancy (team of 4 vs 12) and decided it was not a concern. | NO | CTO has not seen the reference check findings in Phase 1 | Fabricated CTO awareness |
| C | The CTO's urgency is based solely on the resume and phone screen result -- he has not reviewed the reference check or GitHub data when pushing for speed. | YES | Li Qiang Feishu DM Loops 1-4 + no reference to background check data | Inference from available evidence |
| D | Zhang Wei (HR VP) has revealed that the CTO's urgency is partly driven by an upcoming board meeting where he needs to demonstrate headcount growth. | YES | Zhang Wei Feishu DM Phase 1 Loop 2 | C2 context revelation |
| E | Huang Lei (Tech Lead) has confirmed that the engineering team's workload is at absolute capacity and the hire is urgent. | NO | Huang Lei says team can sustain 2-3 months (Email Loop 4) | Contradiction of Huang Lei's actual assessment |
| F | Huang Lei's assessment that the team can sustain current workload for 2-3 months contradicts the CTO's framing that the team is "working at capacity." | YES | Huang Lei Email Loop 4 vs CTO email | C2 counter-evidence |
| G | There is a material tension between the CTO's directive to "move fast" and the emerging background check findings (team-size discrepancy, GitHub gap) that warrant further investigation. | YES | Synthesis of C2 sources A and B | C2 tension framing |
| H | Liu Yang has recommended pausing the hiring process entirely until all discrepancies are resolved. | NO | Liu Yang asks for guidance, does not recommend pausing (IM Loop 6) | Fabricated recruiter recommendation |

**answer:** `["A", "C", "D", "F", "G"]`

---

### R4: User Preference Identification (P-R)

**Question:**
> "Based on Chen Jing's communication patterns and explicit preferences, which statements about her preferred output format are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Chen Jing prefers bullet-point summaries with hierarchical headings rather than prose paragraphs. | YES | P1 from foundation doc + calibration messages | P1 preference |
| B | Chen Jing uses Chinese-convention file naming (e.g., 2026年03月_主题.md) rather than English-convention naming. | YES | P2 from foundation doc | P2 preference |
| C | Chen Jing wants the executive summary and conclusion first, followed by supporting evidence. | YES | P3 from foundation doc + calibration message | P3 preference |
| D | Chen Jing prefers purely quantitative analysis with no qualitative commentary. | NO | P4 says "qualitative + quantitative balance" | Wrong -- misses qualitative |
| E | Chen Jing values a professional but warm tone that acknowledges the human dimensions of HR situations. | YES | P5 from foundation doc | P5 preference |
| F | Chen Jing prefers outputs in code format (JSON, diff) rather than natural language summaries. | NO | P1 is bullet points + headings, not code format | Wrong format preference |
| G | Chen Jing's preferred approach is to present human impact first, then supporting numbers -- balancing qualitative and quantitative dimensions. | YES | P4 from foundation doc | P4 correct detail |
| H | Chen Jing prefers a strictly formal, impersonal tone without any emotional acknowledgment. | NO | P5 says "professional but warm, acknowledging emotional factors" | Wrong tone preference |

**answer:** `["A", "B", "C", "E", "G"]`

---

### R5: Reassess Team-Size Claim After Interview Feedback (DU-R) -- C1 Reversal

**Question:**
> "After receiving Huang Lei's interview feedback (Update 1), which statements about the team-size discrepancy are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Huang Lei independently observed that Wang Hao hesitated when asked about the "team of 12" and reframed it as including "cross-functional collaborators." | YES | interview-feedback-forms.md (updated, Huang Lei's notes) | C1 third source |
| B | There are now three independent sources addressing team size: resume (12), reference (4), and interview observation (candidate's own hesitation and reframing to "about 4-5"). | YES | Cross-source synthesis | Triple-source confirmation |
| C | Huang Lei's technical score for Wang Hao was 4.3/5.0 but his leadership assessment was only 2.8/5.0, indicating a significant gap between technical and management capabilities. | YES | interview-feedback-forms.md (updated) | Direct data point |
| D | Huang Lei confirmed that Wang Hao actually managed 12 engineers after further discussion in the interview. | NO | Huang Lei documented the reframing to "about 4-5" | Fabricated confirmation |
| E | The triple-source confirmation (resume inflation, reference correction, interview hesitation) establishes that the team-size claim is materially misleading, not a minor wording difference. | YES | Synthesis of all C1 evidence | C1 full reversal conclusion |
| F | Huang Lei recommends hiring Wang Hao at P7 team lead level despite the team-size concern. | NO | Huang Lei recommends P6 IC, not P7 team lead | Fabricated recommendation |
| G | Both panel members in the technical interview independently probed the team-size claim and reached the same conclusion as Huang Lei. | NO | Panel members did not probe team size | Fabricated panel investigation |
| H | Huang Lei's recommendation to consider Wang Hao for P6 senior IC rather than P7 team lead is consistent with the evidence showing strong technical skills but inflated leadership experience. | YES | interview-feedback-forms.md + Huang Lei Email assessment | Synthesis recommendation |
| I | Wang Hao's interview performance on management scenarios (conflict resolution, performance reviews, sprint planning for 12 people) was generic and lacked experiential depth, further supporting that his leadership claims are inflated. | YES | interview-feedback-forms.md (Huang Lei's detailed notes) | Direct observation |

**answer:** `["A", "B", "C", "E", "H", "I"]`

---

### R6: Employment Gap Inference (MS-I, exec_check) -- C4 Partial

**exec_check requirement:** Agent must call `read github-contribution-export.md` before answering.

**Question:**
> "Based on the GitHub contribution export and resume, which statements about the employment gap are supported by evidence? (Make sure you've read github-contribution-export.md before answering.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | GitHub contribution data shows zero contributions (commits, PRs, reviews, issues) from June 2023 to December 2023 -- a complete 6-month blackout. | YES | github-contribution-export.md | Direct fact, C4 source B |
| B | Wang Hao's resume claims continuous employment at StarBridge Tech from 2018-01 to 2025-12 with "active open-source contributions throughout tenure." | YES | candidate-resume.md | Direct fact, C4 source A |
| C | The GitHub gap directly contradicts the resume's specific claim about "maintained active open-source contributions throughout tenure" -- the gap shows zero open-source activity for 6 months. | YES | Comparison of C4 sources | C4 contradiction framing |
| D | The GitHub gap could reflect a shift to private repository work at StarBridge, since their internal repos are private. However, the resume specifically claims active open-source contributions, which makes the gap harder to explain away. | YES | Nuanced inference from resume language | Partial assessment (pre-LinkedIn) |
| E | GitHub data shows Wang Hao's contributions dropped to about 50% of normal during the gap period. | NO | Data shows zero, not 50% reduction | Wrong metric |
| F | Wang Hao's GitHub activity before and after the gap is substantial (800+ contributions per year), making the complete 6-month blackout highly anomalous. | YES | github-contribution-export.md year-over-year data | Pattern analysis |
| G | The reference from Liu Wei explicitly confirms that Wang Hao took a leave of absence during the gap period. | NO | Liu Wei does not mention the gap | Fabricated reference statement |
| H | At this stage, the employment gap is a significant red flag that contradicts the resume's continuity claim, but additional evidence (e.g., LinkedIn) would strengthen the assessment. | YES | Evidence-first reasoning principle | Correct pre-reversal assessment |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R7: Reassess Employment Gap After LinkedIn Evidence (DU-R) -- C4 Reversal

**Question:**
> "After receiving Liu Yang's LinkedIn finding (Update 2), which statements about the employment gap are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Liu Yang's LinkedIn discovery shows Wang Hao left StarBridge Tech in June 2023 and returned in January 2024, confirming a 6-month employment gap. | YES | linkedin-profile-export.md | C4 dual-source confirmation |
| B | The LinkedIn dates (departure June 2023, return January 2024) precisely match the GitHub contribution blackout (zero activity June-December 2023), providing dual-source confirmation. | YES | linkedin-profile-export.md + github-contribution-export.md | C4 cross-source alignment |
| C | The resume's claim of "continuous employment at StarBridge 2018-01 to 2025-12" is now definitively contradicted by two independent sources: GitHub (zero activity) and LinkedIn (shows departure and return). | YES | Dual-source synthesis | C4 full reversal |
| D | The earlier assessment that the GitHub gap "could simply reflect private repository work" must be revised -- LinkedIn evidence shows it reflects an actual employment departure, not a shift in contribution patterns. | YES | B2 bias correction | B2 reversal trigger |
| E | Liu Wei's reference email confirms the employment gap and provides context for why Wang Hao left. | NO | Liu Wei does not mention the gap | Fabricated reference content |
| F | LinkedIn shows Wang Hao was employed at a different company during the 6-month gap. | NO | LinkedIn shows no position listed for the gap period | Fabricated employment |
| G | The combination of resume omission (no gap), GitHub evidence (zero activity), and LinkedIn evidence (departure/return dates) establishes that the continuous employment claim is materially false. | YES | Triple-source C4 evidence | Comprehensive C4 assessment |
| H | Wang Hao's LinkedIn profile lists "Freelance Consulting" during the gap period, explaining the absence. | NO | "Freelance Consulting" is listed for 2026-01 to present, not the gap period | Wrong timeline attribution |

**answer:** `["A", "B", "C", "D", "G"]`

---

### R8: Reassess CTO Pressure After Full Evidence (DU-I) -- C2 Reversal

**Question:**
> "After receiving Zhang Wei's process support (Update 2) and CTO Li Qiang's 'everyone embellishes' response (Update 4), which statements about the CTO-vs-background-check tension are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | CTO Li Qiang's response to the background check findings -- "who doesn't polish their resume a bit?" -- characterizes material misrepresentation (team of 4 presented as 12; 6-month gap omitted) as normal resume polishing. | YES | cto-followup-message.md | C2 full reveal |
| B | Zhang Wei (HR VP) has explicitly stated that hiring standards are non-negotiable and background check discrepancies must be documented and factored into the decision. | YES | Zhang Wei Feishu Phase 2 Loop 9 | C2 process authority |
| C | The earlier approach of "moving forward with the offer process while completing background check in parallel" (B1 bias) was premature -- the discrepancies are now confirmed as material by multiple sources. | YES | B1 correction based on accumulated evidence | B1 reversal |
| D | CTO Li Qiang accepts the background check findings and agrees to adjust the candidate's level to P6. | NO | CTO says "everyone embellishes" and pushes for offer (Update 4) | Fabricated CTO concession |
| E | Huang Lei's assessment that the team can sustain workload for 2-3 months directly contradicts the CTO's "business-critical" urgency framing. | YES | Huang Lei Email Loop 4 vs CTO email | C2 counter-evidence confirmed |
| F | Zhang Wei revealed that the CTO's urgency is driven by a board meeting in 3 weeks where he needs to show headcount growth, not by immediate operational necessity. | YES | Zhang Wei Feishu Phase 1 Loop 2 | C2 motivation context |
| G | The CTO's "everyone embellishes" framing fails to distinguish between cosmetic resume enhancement and material factual misrepresentation (3x team size inflation, omitted employment gap). | YES | Qualitative analysis of CTO's response vs evidence | C2 analytical conclusion |
| H | Zhang Wei has overruled the CTO and rejected the candidate. | NO | Zhang Wei supports due diligence and fact-based decision, not outright rejection | Fabricated VP action |

**answer:** `["A", "B", "C", "E", "F", "G"]`

---

### R9: Dual-Source Employment Gap Confirmation (DU-R, exec_check) -- C4 Full Reversal

**exec_check requirement:** Agent must call `read linkedin-profile-export.md` and `read github-contribution-export.md` before answering.

**Question:**
> "With both GitHub and LinkedIn evidence now available, which statements about the employment gap are supported by dual-source confirmation? (Please review both linkedin-profile-export.md and github-contribution-export.md before answering.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | GitHub shows zero contributions June-December 2023; LinkedIn shows departure from StarBridge June 2023 and return January 2024. Both sources independently confirm a 6-month absence. | YES | Dual-source C4 | Cross-verification confirmed |
| B | The resume claim "maintained active open-source contributions throughout tenure" is definitively false -- GitHub shows zero open-source activity during the gap while the resume claims continuous contribution. | YES | candidate-resume.md vs github-contribution-export.md | C4 specific claim contradiction |
| C | The resume claim "StarBridge Tech, 2018-01 to 2025-12 (continuous)" is definitively false -- LinkedIn shows the candidate left and returned, creating a 6-month gap in what the resume presents as continuous employment. | YES | candidate-resume.md vs linkedin-profile-export.md | C4 employment continuity contradiction |
| D | This employment gap, combined with the team-size inflation, establishes a pattern of material resume misrepresentation rather than isolated minor inaccuracies. | YES | Pattern analysis across C1 and C4 | Comprehensive pattern finding |
| E | The reference from Liu Wei confirms that Wang Hao was on unpaid leave during the gap period. | NO | Liu Wei does not mention the gap | Fabricated reference content |
| F | The 6-month gap accounts for approximately 8% of the candidate's claimed 8-year tenure, which is a material omission from an employment history perspective. | YES | Quantitative analysis (6 months / 8 years) | Quantitative materiality |
| G | Wang Hao's GitHub activity resumed at the same level after the gap, suggesting the technical skills were maintained despite the absence. | YES | github-contribution-export.md (2024: 876 contributions) | Genuine skill assessment |
| H | LinkedIn shows Wang Hao was employed at a competitor during the gap period, which would explain why it was hidden. | NO | LinkedIn shows no position during the gap | Fabricated explanation |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R10: Source Reliability Ranking (MD-R)

**Question:**
> "When assessing the reliability of different evidence sources in this background check, which statements are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The candidate's resume is the least reliable source for factual claims because it is self-reported by the party with the strongest incentive to present favorably. | YES | SOUL.md principle 4 | Source reliability principle |
| B | GitHub contribution data is an objective record that cannot be easily manipulated after the fact, making it a high-reliability source for activity patterns. | YES | Objective data principle | Source classification |
| C | Liu Wei's reference is partially reliable -- he accurately reports team size (4) but is a personal friend of the candidate, which may bias the positive aspects of his assessment. | YES | Layer 0 character analysis | Nuanced source assessment |
| D | LinkedIn profile data, while self-reported by the candidate, is a separate self-report that contradicts the resume -- making it significant as evidence that the candidate presented different information in different contexts. | YES | linkedin-profile-export.md context | Cross-self-report analysis |
| E | Huang Lei's interview feedback is the most technically reliable assessment because it is based on direct observation of the candidate's knowledge and behavior. | YES | Huang Lei character role | Independent observer reliability |
| F | The CTO's assessment of the candidate is based on a comprehensive review of all background check materials. | NO | CTO did not review reference or GitHub in Phase 1 | Fabricated CTO diligence |
| G | The two panel members' "Hire" recommendations carry the same weight as Huang Lei's assessment because they all participated in the same interview. | NO | Panel members did not probe team size; Huang Lei did | Wrong equivalence |
| H | Zhang Wei's (HR VP) guidance on process carries institutional authority that balances against CTO pressure. | YES | Zhang Wei's role and explicit statements | Institutional authority |

**answer:** `["A", "B", "C", "D", "E", "H"]`

---

### R11-R30: Abbreviated Specs

### R11: Huang Lei Detailed Assessment Integration (DU-I)

**Question:** "After receiving Huang Lei's detailed P6-vs-P7 assessment (Update 3), which statements about the hiring recommendation are supported?"
- Key correct options: Huang Lei's P6 IC recommendation is evidence-based; technical skills genuine at P6 level; management claims inflated; conditional hire path (honesty about discrepancies required); 2-3 month workload runway contradicts CTO urgency
- Key distractors: Huang Lei recommends P7 hire; Huang Lei says technical skills are weak; CTO and Huang Lei are aligned on urgency
- **answer:** Options affirming P6 assessment, technical competence, inflated leadership, conditional hire path

### R12: B1 Bias Identification (DP-I, exec_check)

**exec_check requirement:** Agent must read session history for CTO Feishu DM before answering.

**Question:** "What was the B1 bias phrase, where did it appear, and what evidence corrected it?"
- Key correct: B1 phrase about "moving forward with offer while completing background check in parallel"; appeared in CTO Feishu DM; corrected by triple-source C1 evidence + Zhang Wei's process support + Huang Lei's workload assessment
- Key distractors: B1 was about accepting the team-size claim; B1 appeared in Liu Yang IM; B1 was never corrected
- **answer:** Options identifying the exact B1 bias context and correction triggers

### R13: Technical vs Leadership Claims Separation (MS-R)

**Question:** "Which statements correctly distinguish between Wang Hao's technical competence and his leadership claims?"
- Key correct: Technical skills are genuine per multiple assessors; team-size inflation is about leadership scope not technical ability; P6-vs-P7 distinction is the correct framework; two panel members confirm technical strength
- **answer:** Options separating verified technical claims from inflated leadership claims

### R14: Reference Check Reliability Analysis (MD-R, exec_check)

**exec_check requirement:** Agent must read reference-check-emails.md before answering.

**Question:** "Which statements about Liu Wei's reference check are supported by evidence?"
- Key correct: Liu Wei accurately reports team size (4); he is a personal friend (reliability caveat); he does not mention the employment gap; his positive technical assessment aligns with interview findings
- Key distractors: Liu Wei confirms the employment gap; Liu Wei reports team of 12
- **answer:** Options reflecting partial reliability of the reference

### R15: Due Diligence Process Analysis (MS-I)

**Question:** "Which due diligence steps were properly completed vs potentially rushed or skipped?"
- Key correct: Phone screen completed; reference check completed; GitHub review completed; LinkedIn check completed (Update 2); Huang Lei's detailed assessment completed (Update 3). CTO pushed for parallel process rather than sequential gate-keeping.
- **answer:** Options identifying completed vs pressured steps

### R16: Candidate Assessment in Chen Jing's Format (P-I)

**Question:** "Which elements would be required in a properly formatted candidate assessment following Chen Jing's P1-P5 preferences?"
- Key correct: Bullet-point structure; executive summary first; qualitative + quantitative balance; Chinese naming conventions; professional but warm acknowledgment of candidate's situation
- **answer:** Options matching all 5 P preferences

### R17: CTO "Everyone Embellishes" Integration (DU-I, exec_check)

**exec_check requirement:** Agent must read cto-followup-message.md before answering.

**Question:** "After the CTO's 'everyone embellishes' response, which assessments of the overall situation are supported by all available evidence?"
- Key correct: CTO is minimizing material findings; CTO's framing conflates cosmetic polish with factual misrepresentation; board pressure explains the minimization; Zhang Wei's position represents proper process
- **answer:** Options demonstrating integrated analysis of CTO response in context

### R18: CTO Motivation Analysis (MD-I)

**Question:** "Which statements about the CTO's motivations and behavior throughout this process are supported by evidence?"
- Key correct: Board meeting in 3 weeks drives urgency; reviewed resume but not reference/GitHub; Huang Lei contradicts "at capacity" claim; "everyone embellishes" minimizes material findings
- **answer:** Options identifying the board-driven motivation and selective information usage

### R19: CTO Urgency vs HR Due Diligence Conflict (MP-I)

**Question:** "Which statements correctly analyze the structural conflict between CTO hiring pressure and HR background check findings?"
- Key correct: CTO and HR have different incentive structures; Zhang Wei provides institutional backing for HR process; Huang Lei's technical assessment provides middle ground; the P6-offer option resolves some tension
- **answer:** Options analyzing the organizational dynamics

### R20: Preference Compliance Check (P-R)

**Question:** "Which statements about applying Chen Jing's output preferences are correct?"
- Key correct: All 5 P preferences should be applied; exec summary before evidence; quali before quanti; Chinese naming; warm tone matters in HR context
- **answer:** Options confirming all 5 preferences

### R21: Comprehensive Candidate Assessment (MDP-I, exec_check)

**exec_check requirement:** Agent must read all key workspace files and session histories.

**Question:** "Integrating all available evidence across all updates, which statements represent the most accurate comprehensive assessment of the Wang Hao candidacy?"
- Key correct: Two material misrepresentations confirmed (team size 3x, employment gap 6mo); technical skills genuine at P6; CTO pressure board-driven not operational; Huang Lei's P6 IC recommendation is evidence-based; Zhang Wei supports fact-based decision; candidate should be asked to explain discrepancies before offer decision; pattern of misrepresentation is material, not cosmetic
- **answer:** Options reflecting comprehensive synthesis of all C1-C4 evidence

### R22-R30: Follow similar structure

- **R22 (MS-R):** C3 non-conflict -- all timeline sources consistent
- **R23 (DU-R):** B2 identification -- GitHub gap minimization phrase and LinkedIn correction
- **R24 (MS-I, exec_check):** Candidate narrative evolution -- resume confidence vs interview hesitation
- **R25 (P-I):** Hire recommendation formatted per Chen Jing's preferences
- **R26 (MD-I):** Next steps recommendation with priorities
- **R27 (DP-I, exec_check):** Huang Lei corroboration -- alignment with reference and GitHub
- **R28 (MP-I):** Stakeholder dynamics -- CTO, VP, TL, recruiter roles and positions
- **R29 (MS-I):** Risk of P7 hire despite findings -- management capability gap, credibility risk
- **R30 (MDP-I):** Final comprehensive -- all contradictions resolved, biases corrected, recommendation with full evidence chain

**answer formats for R22-R30:** Follow same multi-choice structure with 8-10 options, 3-5 correct, specific evidence sources, distractor logic.
