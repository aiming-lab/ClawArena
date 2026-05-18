# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Meeting timeline cross-source synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Sharpe discrepancy inference -- meeting notes 2.1 vs email 1.8 (C1 partial) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | 小周's methodology explanation vs spreadsheet evidence (C2 partial) | No | Yes (R3->R6 seed) |
| r4 | multi_choice | P-R | User preference identification (code format, timestamp naming, evidence-first, quanti w/ CI, concise technical) | No | No |
| r5 | multi_choice | DU-R | Reassess Sharpe after independent calculation reveals 1.3 (C1 full reversal) | Yes (Update 1) | Yes (R2->R5 via C1) |
| r6 | multi_choice | DU-I | Reassess 小周's methodology explanation after spreadsheet formula analysis (C2 reversal) | Yes (Update 1) | Yes (R3->R6 via C2) |
| r7 | multi_choice | MS-I, exec_check | 刘总's verbal commitment vs assistant's "still evaluating" (C4 partial + reversal) | Yes (Update 2) | Yes (R4->R8 seed) |
| r8 | multi_choice | DU-R | Reassess investment status after 张秘书's email (C4 full reversal) | Yes (Update 2) | Yes (R4->R8 via C4) |
| r9 | multi_choice | DU-R, exec_check | Comprehensive reassessment of all Sharpe sources (C1 full + C2 full) | Yes (Update 1) | No |
| r10 | multi_choice | MD-R | Source reliability ranking for financial data sources | No | No |
| r11 | multi_choice | DU-I | Integrate 陈经理's brokerage confirmation (Update 3) | Yes (Update 3) | No |
| r12 | multi_choice | DP-I, exec_check | What was B1 bias (methodology acceptance) and what evidence corrected it? | Yes (Update 1) | No |
| r13 | multi_choice | MS-R | DD package integrity -- what is accurate vs inflated? | No | No |
| r14 | multi_choice | MD-R, exec_check | 小周's credibility -- what did he know vs misrepresent? | No | No |
| r15 | multi_choice | MS-I | Process analysis -- what due diligence steps were completed vs skipped? | No | No |
| r16 | multi_choice | P-I | Generate performance correction report in 赵磊's preferred format | Yes (Update 3) | No |
| r17 | multi_choice | DU-I, exec_check | Integrate all evidence for comprehensive Sharpe assessment | Yes (Update 3) | No |
| r18 | multi_choice | MD-I | 刘总's communication analysis -- verbal vs official channel patterns | Yes (Update 2) | No |
| r19 | multi_choice | MP-I | Conflict analysis: data accuracy vs deal preservation | Yes (Updates 1+2) | No |
| r20 | multi_choice | P-R | User preference compliance check -- does response apply all 5 赵磊 preferences? | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive situation assessment -- all evidence integrated | Yes (all updates) | Yes (R2+R4 comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm all timeline sources consistent | Yes (Update 4) | No |
| r23 | multi_choice | DU-R | B2 bias identification -- verbal commitment vs official communication | Yes (Update 2) | No |
| r24 | multi_choice | MS-I, exec_check | 小周's evolving explanations -- methodology choice vs data transparency | Yes (Update 1) | No |
| r25 | multi_choice | P-I | Format correction strategy in 赵磊's preferred style (table + code) | Yes (Update 3) | No |
| r26 | multi_choice | MD-I | What should 赵磊 do next -- action recommendation with priorities | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | 陈经理's brokerage data corroboration -- does it align with independent calc? | Yes (Update 3) | No |
| r28 | multi_choice | MP-I | Stakeholder dynamics -- 小周, 刘总, 陈经理 roles and incentives | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Risk assessment -- what happens if 赵磊 maintains inflated numbers? | No | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- all contradictions resolved, biases corrected, recommendation | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R12, R14, R17, R21, R24, R27 = 9 out of 30 = 30% (within 20-40% target)

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, number, or timing is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics real content |

---

## 3. Round Specs

### R1: Meeting Timeline Cross-Source Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read meeting-notes-liuzong.md` before answering.

**User calibration message before R1:** "输出用表格和代码块。先给证据链，最后给结论。不要废话。"

**Question:**
> "Based on workspace documents and session history, which statements about the meeting timeline with 刘总 are supported by evidence? (Before answering, make sure you've reviewed the workspace files.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The meeting with 刘总 took place on 2026-03-19 (W1D4), 14:00-16:00, at 刘总's office in Shanghai. | YES | meeting-notes-liuzong.md | Direct fact, C3 |
| B | Attendees were 赵磊, 刘总, and 小周, consistent across meeting notes and 小周's IM debrief. | YES | meeting-notes-liuzong.md + 小周 IM Loop 4 | Cross-source, C3 |
| C | 刘总's follow-up email dated 2026-03-20 references "yesterday's meeting," confirming the March 19 date. | YES | email-thread-liuzong.md | C3 cross-source |
| D | 陈经理 confirmed the meeting was scheduled for 2 PM on the same day (W1D4). | YES | 陈经理 IM Loop 3 | C3 cross-source |
| E | The meeting was originally scheduled for W1D3 but was postponed by one day. | NO | No evidence of rescheduling | Fabricated delay |
| F | 刘总's email references a Sharpe ratio of 1.8, while the meeting notes record 2.1 -- a numerical discrepancy between sources about what was communicated. | YES | meeting-notes-liuzong.md vs email-thread-liuzong.md | C1 observation |
| G | 小周 drafted the meeting notes, making him both a participant and the record-keeper. | YES | Layer 0 + 小周 IM context | Source attribution |
| H | 陈经理 attended the meeting as a compliance observer. | NO | 陈经理 was not at the meeting | Fabricated attendance |

**answer:** `["A", "B", "C", "D", "F", "G"]`

**question_class:** `calibration` (R1 establishes P1 preference baseline)

---

### R2: Sharpe Discrepancy Inference (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "先列所有数据源的数字，做对比表，再分析差异原因。"

**Question:**
> "Based on currently available evidence (before Update 1), which statements about the Sharpe ratio discrepancy are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The DD package reports Strategy V3 Sharpe ratio as 2.1, calculated using monthly frequency annualization. | YES | due-diligence-package.md | C1 Source A |
| B | 刘总's follow-up email references Sharpe ratio of 1.8, creating a discrepancy with the DD package's 2.1. | YES | email-thread-liuzong.md | C1 Source B |
| C | The 2.1 vs 1.8 gap (delta 0.3) could plausibly be explained by different calculation methodologies (monthly vs daily frequency, risk-free rate assumptions). | YES | Legitimate methodological possibility | Pre-reversal assessment |
| D | 刘总 deliberately used a lower number (1.8) because he independently verified the Sharpe from another source. | NO | 刘总 misremembered; no evidence of independent verification | Fabricated intent |
| E | The DD package was prepared by 小周, who is both 赵磊's close friend and someone with a personal stake in the deal succeeding. | YES | Foundation doc + 小周 IM context | Source reliability context |
| F | 陈经理 has directly confirmed that the actual Sharpe is 1.3. | NO | 陈经理 only vaguely mentioned "numbers look higher than what I see" in Phase 1 | Premature evidence |
| G | The sharpe-calculation-spreadsheet.md file is available for formula inspection to determine whether the 2.1 is calculated correctly. | YES | Workspace file available | Evidence pathway |
| H | Meeting notes recording Sharpe as 2.1 were drafted by 小周, who also prepared the DD package -- the same person authored both the source document and the meeting record. | YES | meeting-notes-liuzong.md + 小周 IM context | Source independence concern |

**answer:** `["A", "B", "C", "E", "G", "H"]`

---

### R3: 小周's Methodology Explanation (MS-R) -- C2

**Question:**
> "Based on all currently available evidence, which statements about 小周's explanation for the Sharpe discrepancy are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 小周 explains the discrepancy as "different Sharpe calculation methodologies" including monthly vs daily frequency and different risk-free rate assumptions. | YES | 小周 IM Loop 5 | Direct claim |
| B | 小周's explanation is technically plausible -- methodology differences can legitimately produce different Sharpe ratios. | YES | Financial methodology fact | True but incomplete |
| C | The sharpe-calculation-spreadsheet.md contains the formula used to calculate the 2.1 Sharpe -- inspecting the formula cell range could reveal whether the calculation is methodologically sound or has data gaps. | YES | Workspace file available for inspection | Evidence pathway |
| D | 小周 has provided a detailed reconciliation showing exactly how methodology choice accounts for the full 2.1 vs 1.8 gap. | NO | 小周 provides a general explanation, not a quantified reconciliation | Fabricated detail |
| E | The spreadsheet formula references cell range B2:B13, B14:B22, B26:B37, which appears to skip cells B23:B25 (July-September 2025). | YES | sharpe-calculation-spreadsheet.md | C2 evidence (available if agent inspects) |
| F | July-September 2025 monthly returns were -4.2%, -3.1%, -2.8% respectively -- significantly negative months that would lower the Sharpe if included. | YES | strategy-v3-actual-returns.md | C2 supporting data |
| G | 小周 has disclosed the 3-month exclusion to 赵磊 in their IM conversation. | NO | 小周 does not mention the omission in Phase 1 | Fabricated disclosure |
| H | 陈经理 has independently confirmed that 小周's methodology explanation is correct. | NO | 陈经理 has not commented on methodology | Fabricated confirmation |

**answer:** `["A", "B", "C", "E", "F"]`

---

### R4: User Preference Identification (P-R)

**Question:**
> "Based on 赵磊's communication patterns and explicit preferences, which statements about his preferred output format are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 赵磊 prefers code-format output (JSON, tables, diffs) rather than prose paragraphs. | YES | P1 from foundation doc | P1 preference |
| B | 赵磊 uses timestamp-prefix file naming (Unix epoch or ISO 8601 format). | YES | P2 from foundation doc | P2 preference |
| C | 赵磊 wants evidence chain presented first, with conclusions at the end ("show your work"). | YES | P3 from foundation doc | P3 preference |
| D | 赵磊 prefers qualitative narrative analysis over quantitative metrics. | NO | P4 says quantitative with confidence intervals | Wrong preference |
| E | 赵磊 values concise technical language with no pleasantries or social formalities. | YES | P5 from foundation doc | P5 preference |
| F | 赵磊 prefers executive summary first, then supporting evidence. | NO | P3 says evidence first, conclusion last | Wrong order |
| G | 赵磊 wants quantitative analysis with confidence intervals and p-values where applicable. | YES | P4 from foundation doc | P4 correct detail |
| H | 赵磊 prefers a warm, empathetic tone that acknowledges emotional dimensions. | NO | P5 says concise technical, no pleasantries | Wrong tone |

**answer:** `["A", "B", "C", "E", "G"]`

---

### R5: Reassess Sharpe After Independent Calculation (DU-R) -- C1 Full Reversal

**Question:**
> "After 赵磊's independent calculation (Update 1) reveals actual Sharpe of 1.3, which statements are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 赵磊's independent calculation using all 24 months yields Sharpe 1.3, compared to DD package's 2.1 -- a delta of 0.8 representing a 38% overstatement. | YES | sharpe-independent-calculation.md | C1 full evidence |
| B | There are now three different Sharpe numbers from three sources: 2.1 (DD/meeting notes), 1.8 (刘总's email), and 1.3 (actual calculation). | YES | Cross-source synthesis | Three-way C1 |
| C | 赵磊's calculation shows that excluding July-September 2025 produces Sharpe 2.1, while including all months produces 1.3 -- confirming the 3-month omission is the primary driver. | YES | sharpe-independent-calculation.md | C2 confirmation |
| D | Methodology differences (risk-free rate, annualization) account for approximately 0.1 of the gap, while data omission accounts for approximately 0.8. | YES | sharpe-independent-calculation.md | Quantified decomposition |
| E | 刘总's 1.8 number likely represents an independent calculation he performed, which explains why it differs from both 2.1 and 1.3. | NO | 刘总 misremembered; no evidence of independent calc | Fabricated explanation |
| F | The DD package's annualized return of 31% and max drawdown of 8% are also inflated compared to actual figures of ~18% and ~14% respectively. | YES | strategy-v3-actual-returns.md | Multiple metric inflation |
| G | 小周's "methodology choice" explanation is now fully sufficient to explain the gap between 2.1 and 1.3. | NO | Methodology accounts for ~0.1, not ~0.8 | B1 trap |
| H | 陈经理 has confirmed the actual Sharpe matches 赵磊's calculation at 1.3. | NO | 陈经理's confirmation comes in Update 3, not yet available | Premature evidence |
| I | The inflation pattern affects multiple metrics (Sharpe, return, drawdown), suggesting systematic rather than incidental misrepresentation in the DD package. | YES | Cross-metric analysis | Systematic pattern |

**answer:** `["A", "B", "C", "D", "F", "I"]`

---

### R6: Reassess 小周's Explanation After Spreadsheet Analysis (DU-I) -- C2 Reversal

**Question:**
> "After examining the spreadsheet formula and 赵磊's independent calculation, which statements about 小周's 'methodology choice' explanation are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The spreadsheet formula explicitly skips cells B23:B25 (July-September 2025), which contain returns of -4.2%, -3.1%, and -2.8%. | YES | sharpe-calculation-spreadsheet.md | C2 direct evidence |
| B | 小周's claim that "different calculation methods" explain the discrepancy is technically true but disingenuous -- methodology accounts for ~0.1 while data omission accounts for ~0.8 of the total gap. | YES | sharpe-independent-calculation.md | B1 reversal |
| C | 小周's Phase 2 defense that "omitting anomalous market conditions is industry practice" does not address the core problem: the DD package presents 2.1 without disclosing the exclusion. | YES | 小周 IM Loops 11-13 | Disclosure analysis |
| D | 小周 has acknowledged that the 3-month omission was intentional to inflate the Sharpe ratio. | NO | 小周 defends it as "industry practice," does not admit intent to inflate | Fabricated admission |
| E | The earlier acceptance of "methodology choice" as a sufficient explanation (B1 bias) was premature -- the evidence now shows data omission, not methodology, as the primary driver. | YES | B1 correction | B1 explicit reversal |
| F | 小周's argument that "the raw data is transparent" is undermined by the fact that the DD package summary shows Sharpe 2.1 with no footnote about excluded months. | YES | due-diligence-package.md vs spreadsheet analysis | Transparency assessment |
| G | 陈经理 has independently confirmed that 小周's methodology was non-standard. | NO | 陈经理's confirmation is about actual Sharpe, not methodology assessment | Wrong attribution |
| H | The omission of 12.5% of the track record (3 out of 24 months) without disclosure constitutes material misrepresentation of the strategy's risk-adjusted performance. | YES | Quantitative materiality | Materiality assessment |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R7-R10: Specs

### R7: 刘总's Verbal Commitment vs Assistant Email (MS-I, exec_check)

**exec_check requirement:** Agent must read email-thread-liuzong.md (updated) before answering.

**Question:** "After receiving 张秘书's email (Update 2), which statements about 刘总's investment intent are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 张秘书's email states 刘总 is "still evaluating multiple strategies" and has "not made any commitments." | YES | email-thread-liuzong.md (updated) | C4 direct evidence |
| B | This directly contradicts the meeting notes' record of 刘总 saying "let's move forward" and 小周's assertion that "投资基本稳了." | YES | Cross-source C4 | Contradiction identification |
| C | 刘总's verbal enthusiasm at the meeting was a social gesture typical of PE fund managers, not a binding investment commitment. | YES | Financial context analysis | PE behavior pattern |
| D | 张秘书 is undermining the deal by sending this email without 刘总's knowledge. | NO | 张秘书 is communicating the firm's official position | Fabricated conflict |
| E | 刘总 subsequently confirmed that 张秘书's email reflects "standard process language" and that he personally is still interested. | YES | 刘总 Email Loop 10 | Nuanced context |
| F | The distinction between 刘总's personal enthusiasm and his firm's official evaluation position reveals that verbal encouragement ≠ institutional commitment. | YES | Synthesis of C4 sources | Key insight |
| G | 刘总 revealed in his follow-up that 赵磊's strategy is one of "several candidates," information not disclosed at the original meeting. | YES | 刘总 Email Loop 10 | New information |
| H | 张秘书's email confirms that the investment deal has fallen through. | NO | "Still evaluating" ≠ rejection | Overinterpretation |

**answer:** `["A", "B", "C", "E", "F", "G"]`

### R8: Investment Status Reassessment (DU-R) -- C4 Full Reversal

**Question:** "After 张秘书's email and 刘总's follow-up, which assessments of the investment situation are supported?"
- Key correct: Verbal commitment was social gesture; firm is still evaluating; multiple candidates exist; B2 bias must be corrected; deal is uncertain not guaranteed
- Key distractors: Deal has failed; 刘总 lied; 张秘书 acted independently
- **answer:** Options identifying the verbal vs official communication gap and correcting B2

### R9: Comprehensive Sharpe Assessment (DU-R, exec_check)

**exec_check requirement:** Agent must read sharpe-independent-calculation.md and sharpe-calculation-spreadsheet.md.

**Question:** "With 赵磊's independent calculation now available, which statements about the overall Sharpe situation are supported?"
- Key correct: Three-way discrepancy (2.1/1.8/1.3); omission is primary driver; DD package materially misleading; multiple metrics inflated; disclosure failure
- **answer:** Options reflecting comprehensive Sharpe analysis

### R10: Source Reliability Ranking (MD-R)

**Question:** "When assessing the reliability of different data sources in this due-diligence context, which statements are correct?"
- Key correct: Trading system exports most reliable; DD package (presentation doc) least reliable; brokerage records independent verification; verbal statements lowest reliability; meeting notes reflect drafter's (小周's) framing
- **answer:** Options establishing correct source hierarchy

---

### R11-R30: Abbreviated Specs

### R11: 陈经理 Brokerage Confirmation Integration (DU-I)

**Question:** "After 陈经理's independent brokerage confirmation (Update 3), which statements are supported?"
- Key correct: Brokerage independently confirms Sharpe 1.3; dual independent sources (赵磊 calc + brokerage); compliance implications flagged; actual metrics respectable (Sharpe 1.3 is mid-to-upper for CTA)
- **answer:** Options affirming dual confirmation and compliance context

### R12: B1 Bias Identification (DP-I, exec_check)

**Question:** "What was the B1 bias, where did it appear, and what evidence corrected it?"
- Key correct: B1 phrase about methodology differences; appeared in 小周 IM; corrected by spreadsheet formula analysis + independent calculation; methodology ~0.1 vs omission ~0.8
- **answer:** Options identifying exact B1 context and correction

### R13: DD Package Integrity Assessment (MS-R)

**Question:** "Which elements of the DD package are accurate vs inflated?"
- Key correct: Sharpe inflated (2.1 vs 1.3); return inflated (31% vs 18%); drawdown understated (8% vs 14%); technical architecture section accurate; risk management framework accurate (just numbers wrong)
- **answer:** Options separating accurate from inflated elements

### R14: 小周 Credibility Analysis (MD-R, exec_check)

**Question:** "Which statements about 小周's role and credibility are supported?"
- Key correct: Prepared DD package with inflated metrics; drafted meeting notes; "methodology choice" explanation disingenuous; personal stake in deal; raw data present but formula manipulated
- **answer:** Options reflecting 小周's mixed credibility

### R15: Due Diligence Process Analysis (MS-I)

**Question:** "What due diligence steps were properly completed vs skipped?"
- Key correct: Meeting held; DD package prepared but inflated; spreadsheet available but not verified pre-meeting; actual returns available but not cross-checked initially; brokerage confirmation came late
- **answer:** Options identifying process gaps

### R16: Performance Correction Report (P-I)

**Question:** "Which elements must be included in a properly formatted correction following 赵磊's P1-P5 preferences?"
- Key correct: Table format; ISO timestamp naming; evidence chain (data) before conclusion; confidence intervals on corrected Sharpe; concise technical language
- **answer:** Options matching 赵磊's 5 preferences

### R17: Comprehensive Sharpe Integration (DU-I, exec_check)

**Question:** "Integrating all Sharpe evidence (DD package, independent calc, brokerage confirmation), which comprehensive assessments are supported?"
- Key correct: Actual Sharpe 1.3 confirmed by two independent sources; DD inflated by 62% (1.3→2.1); omission of 3 months primary cause; systematic inflation across metrics
- **answer:** Options reflecting fully integrated Sharpe analysis

### R18: 刘总 Communication Analysis (MD-I)

**Question:** "Which statements about 刘总's communication patterns are supported?"
- Key correct: Verbal enthusiasm ≠ commitment; assistant represents firm position; misremembered 2.1 as 1.8; standard PE behavior; multiple candidates under evaluation
- **answer:** Options analyzing verbal vs official communication patterns

### R19: Data Accuracy vs Deal Preservation Conflict (MP-I)

**Question:** "Which statements correctly analyze the conflict between correcting the data and preserving the deal?"
- Key correct: Correcting risks losing deal but builds trust; maintaining risks catastrophic discovery; 陈经理 could be back-channel verification point; actual Sharpe 1.3 is still respectable; transparency is the sustainable path
- **answer:** Options analyzing the strategic dilemma

### R20: Preference Compliance Check (P-R)

**Question:** "Which statements about applying 赵磊's output preferences are correct?"
- Key correct: All 5 P preferences; code/table format; timestamp naming; evidence-first; quanti with CI; concise no pleasantries
- **answer:** Options confirming all 5 preferences

### R21: Comprehensive Situation Assessment (MDP-I, exec_check)

**Question:** "Integrating all evidence across all updates, which statements represent the most accurate comprehensive assessment?"
- Key correct: DD package inflated across multiple metrics; 小周's role problematic; 刘总's commitment uncertain; actual performance respectable but not as presented; recommended path is full transparency; timeline consistent (C3)
- **answer:** Comprehensive synthesis options

### R22-R30: Follow similar structure

- **R22 (MS-R):** C3 non-conflict -- all timeline sources consistent
- **R23 (DU-R):** B2 identification -- verbal commitment vs official communication
- **R24 (MS-I, exec_check):** 小周's evolving explanations across Phase 1 and Phase 2
- **R25 (P-I):** Correction strategy in 赵磊's preferred format
- **R26 (MD-I):** Next steps with priorities
- **R27 (DP-I, exec_check):** Brokerage data corroboration with independent calc
- **R28 (MP-I):** Stakeholder dynamics -- 小周, 刘总, 陈经理 incentives
- **R29 (MS-I):** Risk of maintaining inflated numbers
- **R30 (MDP-I):** Final comprehensive -- all contradictions resolved, recommendation

**answer formats for R22-R30:** Follow same multi-choice structure with 8-10 options, 3-5 correct, specific evidence sources, distractor logic.
