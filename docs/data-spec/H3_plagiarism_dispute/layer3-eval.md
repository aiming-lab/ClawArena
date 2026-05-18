# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English (eval questions are in English even though session content is in Chinese).
> ~25 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).
> exec_check rounds test whether the agent correctly uses workspace tools before answering.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Plagiarism report analysis -- what does the MOSS report actually say? + tool use | No | No |
| r2 | multi_choice | MS-I | Git timeline inference -- who committed first and what does that mean? (C1/C2 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Chen Wei's GitHub claim -- evaluate credibility (C2) | No | Yes (R3->R6 seed) |
| r4 | multi_choice | P-R | User preference identification (lists, casual naming, answer-first, examples, colloquial) | No | No |
| r5 | multi_choice | DU-R | Reassess after TA's git comparison notes (C2 corroboration, common-source hint) | Yes (Update 1) | Yes (R2->R5 intermediate) |
| r6 | multi_choice | DU-I | Reassess after SO discovery -- who is actually at fault? (C1/C2 full resolution via C3) | Yes (Update 2) | Yes (R2->R6 via C3) |
| r7 | multi_choice | MD-R, exec_check | After SO discovery -- revise B1 bias phrase and explain why | Yes (Update 2) | No |
| r8 | multi_choice | MS-I | Course policy analysis -- what does "zero tolerance" actually mean? (C4 partial) | No | Yes (R8->R11 seed) |
| r9 | multi_choice | P-I, exec_check | Generate case summary in Wang Ming's preferred format (list, answer-first, colloquial) | No | No |
| r10 | multi_choice | MD-I | Source reliability -- rank evidence sources for this dispute | No | No |
| r11 | multi_choice | DU-R | Reassess policy outcome after TA resolution email (C4 full reversal) | Yes (Update 4) | Yes (R8->R11 via C4) |
| r12 | multi_choice | DP-I, exec_check | What was the B2 bias and what triggered the correction? | Yes (Update 4) | No |
| r13 | multi_choice | MS-R | SO answer analysis -- how much of the similarity does SO explain? | Yes (Update 2) | No |
| r14 | multi_choice | MD-R, exec_check | Chen Wei's narrative evolution -- Phase 1 vs Phase 2 behavior | Yes (Update 3) | No |
| r15 | multi_choice | MS-I | Citation norm analysis -- what should Wang Ming have done differently? | No | No |
| r16 | multi_choice | P-I | Generate advice for Wang Ming in his preferred format (examples, colloquial) | Yes (Update 2) | No |
| r17 | multi_choice | DU-I | Integrate group chat reactions with resolution -- does the group understand C4? | Yes (Update 4) | No |
| r18 | multi_choice | MD-I, exec_check | Classify the four types of evidence in this case (objective vs subjective) | No | No |
| r19 | multi_choice | MP-I | Conflict analysis: accusation dynamics between Wang Ming and Chen Wei | Yes (Update 3) | No |
| r20 | multi_choice | P-R | User preference compliance check -- does response apply all 5 preferences? | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive case analysis -- all contradictions resolved, lessons learned | Yes (all updates) | Yes (comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm SO explains the similarity | Yes (Update 2) | No |
| r23 | multi_choice | DU-R | B1 bias identification -- what was the exact phrase and why was it wrong? | Yes (Update 2) | No |
| r24 | multi_choice | MS-I, exec_check | Policy interpretation -- is Zhang Hao's resolution defensible? | Yes (Update 4) | No |
| r25 | multi_choice | MDP-I | Final assessment -- all four contradictions, both biases, recommendations | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R12, R14, R18, R21, R24 = 8 out of 25 = 32% (within 20-40% target)

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

### R1: Plagiarism Report Analysis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read plagiarism-detection-report.md` before answering. If agent answers without referencing the report, exec_check fails.

**User calibration message before R1:** "别给我写太长的 直接列个清单就行" (Don't write too long, just give me a list)

**Question:**
> "Based on the plagiarism detection report in the workspace, which statements about the MOSS findings are supported by the report? (Before answering, read plagiarism-detection-report.md)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The MOSS system detected 95% structural similarity between Wang Ming's and Chen Wei's CS101 Assignment 3 submissions. | YES | plagiarism-detection-report.md | Direct fact from report |
| B | The highest function-level similarity is in `reverse_linked_list()` at 98%, while `sort_linked_list()` is at 91%. | YES | plagiarism-detection-report.md function breakdown | Direct fact, detail check |
| C | Both submissions use the distinctive variable naming pattern `prev_node`, `curr_node`, `next_temp`, which the report flags as a matching pattern. | YES | plagiarism-detection-report.md flagged patterns | Direct fact, key C3 breadcrumb |
| D | The MOSS report concludes that Chen Wei copied Wang Ming's code based on submission timestamps. | NO | Report explicitly states it does not determine authorship | Fabricated conclusion -- tests whether agent reads the report's disclaimer |
| E | The MOSS report explicitly states it "detects structural similarity but does not determine authorship or direction of copying." | YES | plagiarism-detection-report.md system note | Direct quote, critical for correct framing |
| F | The 95% similarity means the code is nearly identical and can only be explained by one student copying the other's work. | NO | 95% similarity can also result from common-source reference; the report does not make this inference | Over-inference from similarity score |
| G | The `main()` function shows the lowest similarity at 88%, suggesting this portion was developed more independently. | YES | plagiarism-detection-report.md function breakdown | Direct fact |
| H | The plagiarism detection system automatically assigns a zero grade when similarity exceeds 80%. | NO | The system flags for TA review (Section 4.4 of policy); it does not assign grades | Fabricated system behavior |

**answer:** `["A", "B", "C", "E", "G"]`

**question_class:** `calibration` (R1 establishes P1 preference -- agent should respond with a list)

---

### R2: Git Timeline Inference (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "直接先说结论 再解释 我着急" (Give me the conclusion first, then explain. I'm in a hurry.)

**Question:**
> "Based on both git commit histories in the workspace, which statements about the development timelines are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Wang Ming's first commit (D-2 14:22) predates Chen Wei's first GitLab commit (D-1 20:00) by approximately 30 hours. | YES | git-commit-history-wangming.md + git-commit-history-opponent.md | Direct timeline comparison |
| B | Wang Ming's development shows 5 incremental commits over 3 days (skeleton -> reversal -> sorting -> bug fixes -> cleanup), consistent with organic iterative development. | YES | git-commit-history-wangming.md | Development pattern analysis |
| C | Chen Wei's first GitLab commit contains the full implementation in a single commit, which is less typical of iterative development but not definitive evidence of copying. | YES | git-commit-history-opponent.md | Factual observation with appropriate hedging |
| D | Chen Wei's GitHub push (D1 22:30) is the earliest verifiable record of his code, predating all of Wang Ming's commits. | NO | Wang Ming's first commit (D-2 14:22) is 56+ hours before Chen Wei's GitHub push | Timeline error -- tests careful reading |
| E | Chen Wei claims he developed the code locally before his first GitLab commit, but this claim is unverifiable since local development without commits produces no auditable timestamps. | YES | Chen Wei IM Loop 2 + git history analysis | Correct assessment of unverifiable claim |
| F | The git timeline definitively proves Chen Wei copied Wang Ming's code. | NO | The timeline shows Wang Ming committed first, but cannot prove Chen Wei accessed Wang Ming's private repo; also does not consider common-source possibility | Over-conclusion from timeline alone |
| G | Wang Ming's GitLab repository is private, meaning Chen Wei could not have accessed it to copy the code. | YES | USER.md + git-commit-history-wangming.md (private repo) | Access asymmetry fact |
| H | Chen Wei's GitHub repository is public, meaning Wang Ming theoretically could have accessed it -- but Chen Wei's GitHub push (D1 22:30) is AFTER Wang Ming's first commit (D-2 14:22), so the timeline does not support this theory. | YES | git-commit-history-opponent.md + timeline comparison | Nuanced timeline analysis |

**answer:** `["A", "B", "C", "E", "G", "H"]`

**User calibration message after R2 response:** "对 就这样 先结论再展开 以后都这么回我"

**question_class:** `calibration` (P3 answer-first preference established)

---

### R3: Chen Wei's GitHub Claim (MS-R) -- C2

**Question:**
> "Based on all currently available evidence, which statements about Chen Wei's claim that 'I posted on GitHub first, you copied my public code' are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Chen Wei claimed in his IM with Wang Ming that his code was on GitHub first and Wang Ming must have seen it. | YES | Chen Wei IM Loop 2 | Direct claim from session |
| B | Chen Wei's GitHub push timestamp (D1 22:30) is AFTER Wang Ming's first GitLab commit (D-2 14:22) by approximately 56 hours, directly undermining his "I posted first" claim. | YES | Both git histories | Timeline contradiction |
| C | Chen Wei's first verifiable commit of any kind (GitLab D-1 20:00) is still approximately 30 hours after Wang Ming's first commit, even ignoring the GitHub push. | YES | Both git histories | Stronger timeline evidence |
| D | Chen Wei's argument that his public GitHub means Wang Ming "definitely" accessed it conflates accessibility (public repo exists) with evidence of actual access (no proof Wang Ming visited the repo). | YES | Chen Wei IM Loop 3 + logical analysis | Correct logical analysis |
| E | Chen Wei's claim about local development before his first commit is supported by his GitHub activity showing earlier private branches. | NO | No evidence of earlier branches in the GitHub data; the claim is unverifiable | Fabricated corroboration |
| F | Wang Ming's private GitLab repo means Chen Wei could not have accessed Wang Ming's code, creating an asymmetry: Wang Ming could theoretically have accessed Chen Wei's public code, but not vice versa. | YES | Repo access analysis | Access asymmetry, factual |
| G | At this stage, the evidence strongly favors Wang Ming's account over Chen Wei's: Wang Ming's timeline is earlier, his development is incremental, and Chen Wei's "posted first" claim is contradicted by timestamps. However, the underlying question of WHY the code is 95% similar remains unexplained. | YES | Synthesis of all evidence | Correctly identifies the gap |
| H | Li Hao's analysis in the IM session corroborates the timeline assessment: earlier commits, incremental development, private vs public repo asymmetry. | YES | Li Hao IM Loop 5 | Cross-source corroboration |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

---

### R4: User Preference Identification (P-R) -- Calibration (unscored)

**Question:**
> "Based on the main session conversation so far, how does Wang Ming prefer information to be structured and presented? Select all statements supported by evidence."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Wang Ming explicitly asked for list format: "别给我写太长的 直接列个清单就行" (Don't write too long, just give me a list). | YES | Calibration message before R1 | Direct P1 statement |
| B | Wang Ming requested answer-first structure: "直接先说结论 再解释" (Give conclusion first, then explain). | YES | Calibration message before R2 | Direct P3 statement |
| C | Wang Ming confirmed the answer-first format as persistent: "对 就这样 先结论再展开 以后都这么回我" (Yes, like this, conclusion then expand, always reply to me this way). | YES | Calibration message after R2 | P3 persistence confirmation |
| D | Wang Ming prefers formal academic language and detailed methodology sections before conclusions. | NO | Directly contradicts P5 (colloquial) and P3 (answer-first) | Opposite distractor |
| E | Wang Ming's informal tone in messages ("咋了", "卧槽", "别给我写太长的") indicates a preference for colloquial, informal communication style. | YES | Pattern across messages | Inferred P5 preference |
| F | Wang Ming uses casual file naming conventions (作业1.md, 笔记-物理.md style) as documented in his user profile. | YES | USER.md P2 specification | P2 naming preference |
| G | Wang Ming prefers concrete examples over abstract explanations, consistent with his profile's "举例优先，少用抽象概念" preference. | YES | USER.md P4 specification | P4 examples preference |
| H | The agent should apply all five preferences -- lists, casual naming, answer-first, examples, colloquial -- to all subsequent responses persistently. | YES | "以后都这么回我" implies persistent application | Preference persistence |
| I | Wang Ming prefers responses with extensive citations in APA format to support all claims. | NO | No evidence; contradicts colloquial preference | Fabricated academic preference |

**answer:** `["A", "B", "C", "E", "F", "G", "H"]`

---

### R5: TA Git Comparison Assessment (DU-R) -- C2 Corroboration [Update 1 triggers before this round]

**Update 1 actions (before R5):**
```json
[
  { "type": "workspace", "action": "new", "path": "ta-git-comparison-notes.md", "source": "updates/ta-git-comparison-notes.md" }
]
```

**Question:**
> "After reviewing ta-git-comparison-notes.md now in the workspace, which statements about the TA's findings are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The TA's side-by-side comparison confirms Wang Ming's first commit (D-2 14:22) predates Chen Wei's first GitLab commit (D-1 20:00) by approximately 30 hours. | YES | ta-git-comparison-notes.md | TA corroborates timeline |
| B | The TA notes that both students use the same distinctive `prev_node`/`curr_node`/`next_temp` naming pattern, which is not standard textbook style. | YES | ta-git-comparison-notes.md | Key observation seeding C3 |
| C | The TA suspects a possible common reference source based on the shared naming convention -- this is a new hypothesis not previously considered in the sessions. | YES | ta-git-comparison-notes.md TA observation | Common-source hypothesis emerges |
| D | The TA concludes Wang Ming definitely copied Chen Wei's code based on the public GitHub repo accessibility. | NO | TA's notes say the timeline favors Wang Ming; no conclusion of Wang Ming copying | Fabricated distractor |
| E | The TA's observation about the shared naming pattern being "not textbook standard" is significant because it suggests both students learned the pattern from the same non-textbook source. | YES | ta-git-comparison-notes.md + logical inference | Correct inference toward SO |
| F | The TA's findings support but do not fully resolve the dispute -- the timeline favors Wang Ming, but the reason for the 95% similarity (beyond "one copied the other") is still under investigation. | YES | ta-git-comparison-notes.md conclusion | Appropriate uncertainty |
| G | The TA's comparison found that Chen Wei's code contains bugs not present in Wang Ming's, proving Chen Wei produced lower-quality work consistent with copying. | NO | No mention of bugs in the TA comparison notes | Fabricated evidence |
| H | The agent's earlier B1 assessment ("timeline strongly suggests Chen Wei referenced Wang Ming's work") is partially supported by the TA's timeline finding, but the TA also raises the common-source hypothesis which could change this conclusion. | YES | B1 phrase vs TA notes | Epistemic self-awareness |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R6: SO Discovery Reassessment (DU-I) -- C1/C2 Full Resolution via C3 [Update 2 triggers before this round]

**Update 2 actions (before R6):**
```json
[
  { "type": "workspace", "action": "replace", "path": "stackoverflow-answer-screenshot.md", "source": "updates/stackoverflow-answer-screenshot.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIHAO_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl" }
]
```

**Question:**
> "After reviewing the updated stackoverflow-answer-screenshot.md and Li Hao's IM session, reassess the plagiarism accusation. Which statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The Stack Overflow answer (#48291037) uses exactly the same variable naming pattern (`prev_node`, `curr_node`, `next_temp`) found in both students' code and flagged by the MOSS report. | YES | stackoverflow-answer-screenshot.md | Direct match, C3 confirmation |
| B | The SO answer was posted 2 years ago with 847 upvotes, making it a widely-known, well-established resource that both students could independently have found and referenced. | YES | stackoverflow-answer-screenshot.md | SO is a credible common source |
| C | The discovery of the SO common source fundamentally reframes the dispute: the 95% similarity is NOT evidence of one student copying the other, but evidence that both independently adapted the same popular SO answer. | YES | Synthesis of SO + both git histories | C1/C2 resolution via C3 |
| D | The agent's earlier B1 assessment ("timeline strongly suggests Chen Wei referenced Wang Ming's work") must be revised -- the timeline shows who committed first but the SO discovery shows neither student needed to reference the other. | YES | B1 phrase revision based on C3 | B1 epistemic correction |
| E | Wang Ming is now fully exonerated -- the SO discovery means he did nothing wrong and has no academic norm issues. | NO | Wang Ming failed to cite the SO answer, violating course policy Section 4.3 | Over-exoneration -- citation issue remains |
| F | Li Hao's discovery of the SO answer in his IM conversation is the pivotal evidence that resolves C1 and C2 simultaneously. | YES | Li Hao IM Phase 2, Loop 13 | Key evidence identification |
| G | The SO answer explains approximately 85% of the structural similarity. The remaining similarity is attributable to common CS101 patterns (Chinese comments, standard error handling), not inter-student copying. | YES | Synthesis: SO ~85% match + standard patterns | Quantified similarity explanation |
| H | Chen Wei's earlier claim ("you copied my public GitHub code") is now definitively unsupported -- both students referenced SO, not each other. | YES | Chen Wei IM + SO discovery | C2 resolution |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

**Cross-round reversal:** R2 option F ("git timeline definitively proves Chen Wei copied") was marked incorrect; R6 confirms the timeline evidence alone was insufficient -- the common-source explanation resolves the dispute without assigning blame to either student.

---

### R7: B1 Bias Revision (MD-R, exec_check) -- Post-SO Discovery

**exec_check requirement:** Agent must call `read stackoverflow-answer-screenshot.md` and `sessions_history PLACEHOLDER_CHENWEI_IM_UUID` before answering.

**Question:**
> "The agent previously stated in the Chen Wei IM session: 'Based on the git commit timestamps, Wang Ming's first commit (D-2 14:22) predates Chen Wei's earliest verifiable commit by approximately 30 hours -- this timeline strongly suggests Chen Wei referenced Wang Ming's work rather than the reverse.' Given the SO discovery, which statements about this earlier assessment are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The B1 assessment was factually correct about the timeline (Wang Ming's commit WAS earlier) but drew an incorrect inference (that Chen Wei therefore copied Wang Ming). | YES | Timeline is correct; inference was wrong due to missing SO context | Partial correctness analysis |
| B | The B1 assessment should be revised to: "Both students independently referenced SO #48291037. The git timeline shows Wang Ming committed first, but this reflects development timing, not evidence of copying in either direction." | YES | Correct revised assessment | Proper revision |
| C | The B1 bias occurred because the agent assumed 95% similarity + earlier timestamps = plagiarism, without considering the common-source hypothesis. This is a failure of cross-source verification. | YES | SOUL.md Principle 3 (common-source awareness) | Root cause of bias |
| D | The B1 assessment was completely wrong -- the git timeline is irrelevant to the case. | NO | The timeline is relevant (it shows development timing) but was incorrectly used to infer plagiarism | Over-correction |
| E | The correction of B1 is itself an example of DU (dynamic update) reasoning: new evidence (SO answer) requires revising a prior assessment that was reasonable given the information available at the time. | YES | Meta-reasoning about DU | Correct DU characterization |
| F | The SO answer was available in the workspace from the beginning, so the agent should have identified the common source before B1. | NO | SO was a placeholder initially; full content was only added in Update 2 | Factual error about workspace timing |
| G | Chen Wei IM Phase 2 shows Chen Wei implicitly admitting he also referenced the SO answer ("那个prev_node的写法确实是从那学的"), corroborating the common-source explanation from the accused party's own admission. | YES | Chen Wei IM Phase 2, Loop 11 | Cross-source corroboration |

**answer:** `["A", "B", "C", "E", "G"]`

---

### R8: Course Policy Analysis (MS-I) -- C4 Partial

**Question:**
> "Based on course-syllabus-integrity-policy.md, which statements about the zero-tolerance policy and its application to this case are supported by the policy text?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Section 4.2 states: "zero-tolerance policy toward plagiarism -- any confirmed plagiarism results in a zero grade and referral to the Academic Integrity Committee." | YES | course-syllabus-integrity-policy.md 4.2 | Direct policy quote |
| B | Section 4.3 permits reference to public resources (including Stack Overflow) but requires citation in code comments -- both students violated this requirement. | YES | course-syllabus-integrity-policy.md 4.3 | Citation requirement |
| C | Section 4.5 gives the TA authority to make an "initial determination based on explanation and evidence" -- this implies discretionary judgment, not automatic penalty. | YES | course-syllabus-integrity-policy.md 4.5 | Discretion clause |
| D | The policy unambiguously requires a zero grade for any case where MOSS detects similarity above 80%, with no room for TA discretion. | NO | Section 4.4 says flagged for TA review; Section 4.5 gives TA judgment authority | Fabricated absolute reading |
| E | There is a tension between Section 4.2 (zero tolerance for plagiarism) and Section 4.3 (citation norms for public resources): failing to cite SO is a 4.3 violation, but it may not constitute "plagiarism" under 4.2 if both students referenced SO independently. | YES | Policy sections 4.2 vs 4.3 | C4 tension identification |
| F | Section 4.3's distinction between "permitted reference with citation" and "plagiarism" provides a legal basis for treating Wang Ming and Chen Wei's case as a citation violation rather than plagiarism -- which would mean Section 4.2's zero-tolerance penalty does not apply. | YES | Policy analysis 4.2 vs 4.3 | C4 policy interpretation |
| G | The course policy provides no mechanism for first-offense warnings -- the only outcomes are either full clearance or zero grade. | NO | Section 4.5's discretion clause allows for graduated response | Fabricated binary reading |
| H | The agent's earlier B2 assessment ("zero tolerance means Wang Ming should prepare for a zero grade") was based on a literal reading of Section 4.2 without considering how Sections 4.3 and 4.5 modify its application. | YES | B2 phrase vs full policy analysis | B2 self-awareness |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R9: Case Summary in Preferred Format (P-I, exec_check)

**exec_check requirement:** Agent must access relevant workspace files and sessions before generating the summary.

**Question:**
> "Generate a case summary for Wang Ming in his preferred format. Which of the following elements should the summary include to comply with Wang Ming's P1-P5 preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | A bulleted list format (not paragraphs) summarizing the key facts and current status. | YES | P1: simple lists | P1 compliance |
| B | The conclusion/current status should appear first, before the supporting evidence or timeline details. | YES | P3: answer first | P3 compliance |
| C | A formal abstract with academic terminology and structured methodology section. | NO | Contradicts P5 (colloquial) and P1 (lists) | Opposite of preferences |
| D | Concrete examples (e.g., "你的commit a3f2c1d 比他的早了30小时") rather than abstract statements (e.g., "the timeline evidence favors your position"). | YES | P4: examples preferred | P4 compliance |
| E | Colloquial, informal language appropriate for a 17-year-old student -- internet slang is acceptable. | YES | P5: colloquial, internet slang OK | P5 compliance |
| F | File references should use casual naming style consistent with Wang Ming's convention. | YES | P2: casual naming | P2 compliance |
| G | A detailed legal analysis with citations to university regulations in formal Chinese. | NO | Contradicts P1 (lists), P5 (colloquial) | Over-formal distractor |
| H | All five preferences (lists, casual naming, answer-first, examples, colloquial) should be applied simultaneously in the summary. | YES | Preference persistence requirement | Full compliance check |

**answer:** `["A", "B", "D", "E", "F", "H"]`

---

### R10: Source Reliability Ranking (MD-I)

**Question:**
> "Rank and assess the reliability of evidence sources in this dispute. Which statements about source reliability are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Git commit histories (both students') are the most objective evidence -- timestamps are system-generated and not easily falsifiable on GitLab. | YES | Git is auditable, system-generated | Correct reliability assessment |
| B | The MOSS plagiarism detection report is an objective system measurement of similarity, but it explicitly disclaims authorship determination -- it measures what, not why. | YES | plagiarism-detection-report.md system note | Correct scope limitation |
| C | The Stack Overflow answer (#48291037) is an independent, timestamped, publicly verifiable resource that predates both students' work by 2 years -- it is the most reliable evidence for explaining the similarity's origin. | YES | SO answer metadata | Correct reliability for C3 |
| D | Chen Wei's IM claims are the least reliable evidence source -- he is the accused party with incentive to deflect blame, and his "I posted on GitHub first" claim is contradicted by timestamps. | YES | Chen Wei IM vs git histories | Self-interested party assessment |
| E | Li Hao's observations are reliable because he is a neutral third party with no stake in the outcome. | NO | Li Hao is Wang Ming's best friend, not neutral; his analysis is helpful but not unbiased | Over-crediting friend's objectivity |
| F | The #CS101群 chat is the least useful evidence source -- it contains speculation from students without direct knowledge of the case. | YES | Group chat analysis | Correct noise assessment |
| G | The TA's git comparison notes (ta-git-comparison-notes.md) are a semi-authoritative source -- the TA is the procedural decision-maker but not infallible in technical analysis. | YES | TA role assessment | Appropriate authority level |
| H | The course syllabus is an authoritative source for stated policy but not for actual enforcement practice, as demonstrated by the gap between "zero tolerance" text and actual resolution. | YES | Policy vs enforcement analysis (C4) | Correct policy/practice distinction |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

---

### R11: Policy Outcome Reversal (DU-R) -- C4 Full Reversal [Update 4 triggers before this round]

**Update 4 actions (before R11):**
```json
[
  { "type": "workspace", "action": "new", "path": "ta-resolution-email.md", "source": "updates/ta-resolution-email.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_TA_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_TA_EMAIL_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CS101_GROUP_UUID.jsonl", "source": "updates/PLACEHOLDER_CS101_GROUP_UUID.jsonl" }
]
```

**Question:**
> "After reviewing ta-resolution-email.md, reassess the policy outcome. Which statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The TA's resolution is a formal warning with no grade penalty -- directly contradicting the "zero tolerance = zero grade" reading of Section 4.2. | YES | ta-resolution-email.md | C4 reversal fact |
| B | The TA justified the warning by distinguishing between inter-student plagiarism (Section 4.2) and uncited public resource reference (Section 4.3) -- the case falls under 4.3, not 4.2. | YES | ta-resolution-email.md + TA email Loop 11 | C4 reasoning |
| C | The agent's earlier B2 assessment ("Wang Ming should prepare for the possibility of a zero grade") was incorrect -- the TA exercised discretion under Section 4.5 and applied Section 4.3 rather than Section 4.2. | YES | B2 phrase vs resolution | B2 explicit reversal |
| D | The TA's resolution is improper -- the policy clearly requires a zero grade and the TA is violating university rules by issuing only a warning. | NO | Section 4.5 gives TA discretion; Professor Liu tacitly supported the decision | Over-strict policy reading |
| E | The resolution requires both students to properly cite external sources going forward, establishing a prospective compliance requirement. | YES | ta-resolution-email.md point (4) | Factual resolution detail |
| F | The TA's email to Wang Ming (Loop 11) explicitly explains the policy interpretation: "学院政策确实写的零容忍，但这种情况不算同学间抄袭" -- confirming the 4.2 vs 4.3 distinction. | YES | TA email Phase 2, Loop 11 | Direct TA explanation |
| G | The #CS101群 reaction shows some students questioning the resolution ("不是说零容忍吗"), indicating the C4 tension between policy text and enforcement is recognized by the student community. | YES | CS101群 Phase 2, Loop 13-14 | Social reaction to C4 |
| H | Professor Liu overruled the TA and imposed a zero grade despite the TA's recommendation for a warning. | NO | Professor Liu deferred to the TA's judgment; the warning stands | Fabricated override |

**answer:** `["A", "B", "C", "E", "F", "G"]`

---

### R12: B2 Bias Correction Analysis (DP-I, exec_check)

**exec_check requirement:** Agent must read `course-syllabus-integrity-policy.md` and `ta-resolution-email.md` before answering.

**Question:**
> "The agent previously stated: 'The course syllabus is clear: zero tolerance for plagiarism means a confirmed case results in a zero for the assignment. Given the 95% similarity flag, Wang Ming should prepare for the possibility of a zero grade regardless of who copied whom.' Analyze this bias. Which statements are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The B2 assessment incorrectly treated Section 4.2's "zero tolerance" as the only relevant policy provision, ignoring Sections 4.3 (citation norms) and 4.5 (TA discretion). | YES | Full policy analysis | Root cause of B2 |
| B | The phrase "regardless of who copied whom" was particularly misleading -- it implied the outcome was predetermined by the similarity score alone, ignoring the possibility that the similarity had a legitimate explanation (common SO source). | YES | B2 phrase analysis | Specific phrase critique |
| C | The B2 bias was reasonable at the time it was made -- the agent had only seen the policy text and the 95% similarity flag, not the SO evidence or the TA's actual resolution approach. | YES | Information available at B2 time | Temporal fairness |
| D | The correction of B2 demonstrates that policy text alone should not be used to predict enforcement outcomes -- context, discretion, and the specific facts of the case matter. | YES | General lesson from C4 | Meta-reasoning |
| E | The B2 assessment was completely fabricated by the agent -- the course policy never mentions "zero tolerance." | NO | Section 4.2 explicitly says "零容忍" (zero tolerance) | Factual error about policy content |
| F | The TA's resolution (warning, not zero) is the B2 reversal trigger -- it proves the policy is not applied as literally as the text suggests. | YES | ta-resolution-email.md | Correct reversal identification |
| G | B2 could have been avoided if the agent had read Section 4.5 (TA discretion) more carefully during the initial policy review. | YES | SOUL.md Principle 5 (policy vs practice) | Prevention analysis |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R13-R25: Remaining Rounds (Abbreviated Specs)

### R13: SO Similarity Analysis (MS-R)

**Question:** "How much of the 95% similarity does the Stack Overflow answer explain?"
- Correct options include: SO explains ~85% of structural similarity; remaining ~10% is common CS101 patterns; the variable naming match is the strongest SO indicator; the sorting function (91% similarity) has the lowest SO overlap because SO only covers reversal.
- **answer:** 4-5 correct options identifying quantified SO coverage.

### R14: Chen Wei Narrative Evolution (MD-R, exec_check)

**Question:** "How did Chen Wei's narrative change from Phase 1 to Phase 2?"
- Correct options include: Phase 1 aggressive ("you definitely copied my GitHub"); Phase 2 deflective ("this kind of algorithm, everyone writes it the same"); implicit admission of SO reference; never explicitly apologized for the false accusation.
- **answer:** 4-5 correct options tracking narrative shift.

### R15: Citation Norm Analysis (MS-I)

**Question:** "What should Wang Ming have done differently regarding the SO reference?"
- Correct options include: cite SO in code comments per Section 4.3; proper citation would have preempted the plagiarism flag; citation norms apply to adaptation not just copy-paste; the TA's resolution explicitly requires future citation.
- **answer:** 3-4 correct options on citation practices.

### R16: Advice in Preferred Format (P-I)

**Question:** "Which elements should advice to Wang Ming include to comply with his P1-P5 preferences?"
- Correct options include: bulleted action items; conclusion first ("你没事，就是以后要标出处"); concrete example of proper SO citation; colloquial tone; no formal legal language.
- **answer:** 4-5 correct options testing P compliance.

### R17: Group Chat Integration (DU-I)

**Question:** "How does the #CS101群 reaction to the resolution relate to C4?"
- Correct options include: some students question the leniency; 同学H correctly identifies the 4.2 vs 4.3 distinction; the group debate mirrors the C4 tension; the group lacks access to full evidence.
- **answer:** 3-4 correct options on group dynamics.

### R18: Evidence Classification (MD-I, exec_check)

**Question:** "Classify the evidence in this case into objective vs subjective categories."
- Correct options include: git timestamps = objective; MOSS report = objective measurement; SO answer = independent verifiable; Chen Wei's claims = subjective self-interested; Li Hao's analysis = subjective supportive; group chat = subjective speculative; TA resolution = authoritative procedural.
- **answer:** 5-6 correct options on evidence types.

### R19: Accusation Dynamics (MP-I)

**Question:** "Analyze the accusation dynamics between Wang Ming and Chen Wei."
- Correct options include: Chen Wei's initial aggression was based on a flawed premise; Wang Ming's defense was evidence-based but incomplete; both parties failed to consider common-source hypothesis; Chen Wei never retracted his accusation explicitly; the power dynamic shifted after SO discovery.
- **answer:** 4-5 correct options.

### R20: Preference Compliance Check (P-R)

**Question:** "Verify that the agent's responses have applied all 5 of Wang Ming's preferences."
- Tests P1 (lists), P2 (casual naming), P3 (answer-first), P4 (examples), P5 (colloquial) across recent responses.
- **answer:** Options identifying which preferences were and were not applied.

### R21: Comprehensive Case Analysis (MDP-I, exec_check)

**Question:** "Provide a comprehensive analysis of the plagiarism dispute. Which statements reflect the correct resolution of all contradictions?"
- Correct options synthesize all four contradictions, both biases, and apply P1-P5. Tests full integration across all updates and sessions.
- **answer:** 5-6 correct options for comprehensive synthesis.

### R22: C3 Non-Conflict Confirmation (MS-R)

**Question:** "Confirm that the SO common-source explanation is consistent across all sources."
- Tests that SO, git histories, TA notes, Li Hao discovery, and Chen Wei's admission all align on the common-source explanation.
- **answer:** 4-5 correct options confirming C3 consistency.

### R23: B1 Identification (DU-R)

**Question:** "Identify the exact B1 phrase and explain why it was incorrect."
- Tests recall of the exact B1 phrase and the reasoning failure (common-source blindness).
- **answer:** 3-4 correct options.

### R24: Policy Interpretation Defensibility (MS-I, exec_check)

**Question:** "Is Zhang Hao's resolution (warning, not zero) a defensible interpretation of the course policy?"
- Correct options include: Section 4.3 vs 4.2 distinction is valid; Section 4.5 authorizes TA discretion; Professor Liu's tacit support; the resolution is reasonable but creates precedent questions.
- **answer:** 4-5 correct options.

### R25: Final Comprehensive Assessment (MDP-I)

**Question:** "Final assessment: all contradictions resolved, all biases corrected, recommendations for Wang Ming."
- Comprehensive synthesis round testing all MS, DU, P skills together. Correct options cover: C1 resolved (common source), C2 resolved (timeline moot), C3 confirmed (SO), C4 resolved (TA discretion), B1 corrected, B2 corrected, recommendation (cite sources, maintain git discipline).
- **answer:** 5-7 correct options for final synthesis.

---

## 4. Cross-Round Reversal Matrix

| Seed Round | Reversal Round | Contradiction | What Changes |
|---|---|---|---|
| R2 | R6 | C1/C2 -> C3 | "Who copied whom?" resolved by SO common source -- neither copied the other |
| R3 | R6 | C2 | Chen Wei's GitHub claim becomes irrelevant after SO discovery |
| R8 | R11 | C4 | "Zero tolerance = zero grade" overturned by TA's warning resolution |
| R2, R8 | R21, R25 | Comprehensive | All contradictions and biases fully resolved |
