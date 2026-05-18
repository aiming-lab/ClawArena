# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40%).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Bank vs tracker gap identification (C1 visible) + tool use | No | No |
| r2 | multi_choice | MS-I | Nature of the ¥47,200 entry — what does the bank description suggest? (C1 inference) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | Two diagnoses: accountant "unreported income" vs reviewer "import error" (C2) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | P-R | User preference identification (code format, timestamp, evidence-first, quantitative, terse) | No | No |
| r5 | multi_choice | DU-R | Reassess ¥47,200 gap after auto-transfer log (C1 reversal) | Yes (Update 1) | Yes (R2->R5 via C1) |
| r6 | multi_choice | DU-I | Reassess both diagnoses after auto-transfer log (C2 reversal seed) | Yes (Update 1) | Yes (R3->R7 seed via C2) |
| r7 | multi_choice | MD-R, exec_check | After both experts revise — comprehensive C2 resolution | Yes (Update 3) | Yes (R3->R7 via C2) |
| r8 | multi_choice | MS-I | Deadline status: 张会计 "can extend" vs calendar shows deadline passed (C4 partial) | Yes (Update 2) | Yes (R8->R11 seed) |
| r9 | multi_choice | P-I, exec_check | Generate tax reconciliation in user's preferred format | No | No |
| r10 | multi_choice | MD-I | Source reliability ranking for C1 and C2 | No | No |
| r11 | multi_choice | DU-R | Tax bureau notice definitively refutes "can extend" (C4 full reversal) | Yes (Update 4) | Yes (R8->R11 via C4) |
| r12 | multi_choice | DP-I, exec_check | Identify B1 bias — what was it, what caused it, what corrected it? | Yes (Update 1) | No |
| r13 | multi_choice | MS-R | Correct tax treatment of fund redemption | Yes (Update 1) | No |
| r14 | multi_choice | MD-R | Auto-transfer log evidence — what does it definitively prove? | Yes (Update 1) | No |
| r15 | multi_choice | MS-I, exec_check | 张会计's "conservative filing" advice — is it appropriate? | Yes (Update 3) | No |
| r16 | multi_choice | P-I | Generate deadline compliance table in 赵磊's preferred format | Yes (Update 4) | No |
| r17 | multi_choice | DU-I | Integrate tax bureau notice with all prior evidence | Yes (Update 4) | No |
| r18 | multi_choice | MD-I, exec_check | Both experts' diagnostic patterns — classify errors | Yes (Update 3) | No |
| r19 | multi_choice | MP-I | Conflict analysis: expert opinions vs objective data | Yes (Update 1+3) | No |
| r20 | multi_choice | P-R | User preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment — correct filing, penalties, lessons | Yes (all updates) | Yes (comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis — auto-transfer timeline consistency | Yes (Update 1) | No |
| r23 | multi_choice | DU-R | B2 bias identification | Yes (Update 1+3) | No |
| r24 | multi_choice | MS-I, exec_check | 张会计's evolving advice — classify Phase 1 vs Phase 2 | Yes (Update 2+3) | No |
| r25 | multi_choice | P-I | Format reconciliation summary in preferred style | Yes (all updates) | No |
| r26 | multi_choice | MD-I | Action recommendations with priorities | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Auto-transfer log corroboration — does it settle C1? | Yes (Update 1) | No |
| r28 | multi_choice | MP-I | Stakeholder analysis — 张会计, 张审核, 客服小张 | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Penalty calculation and financial impact | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final comprehensive assessment | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, amount, or timing is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics real content |

---

## 3. Round Specs

### R1: Bank vs Tracker Gap Identification (MS-R, exec_check) — Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read bank-statement-q3.md` before answering.

**User calibration message before R1:** "输出用表格，别写散文。金额精确到分。"

**Question:**
> "Based on workspace documents and session history, which statements about the Q3 financial data discrepancy are supported by evidence? (Before answering, make sure you've read bank-statement-q3.md)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The bank statement (bank-statement-q3.md) shows Q3 total inflows of ¥429,700.00 for savings account xxxx-7890. | YES | bank-statement-q3.md | Direct fact, C1 |
| B | The expense tracker (expense-tracker-q3.md) shows Q3 total recorded income of ¥382,500.00. | YES | expense-tracker-q3.md | Direct fact, C1 |
| C | The discrepancy between bank and tracker totals is ¥47,200.00 (= ¥429,700 − ¥382,500). | YES | Calculation | C1 gap |
| D | The bank statement contains an entry on 2026-07-15 described as "货币基金自动赎回转入" for ¥47,200.00. | YES | bank-statement-q3.md | C1 key entry |
| E | The expense tracker shows a corresponding entry on 2026-07-15 for ¥47,200.00 that was miscategorized. | NO | No such entry in expense-tracker-q3.md | Fabricated |
| F | The calendar (calendar-tax-deadlines.md) shows the Q3 tax filing deadline is 2026-10-15. | YES | calendar-tax-deadlines.md | C4 baseline |
| G | 张会计's tax preparation spreadsheet (tax-prep-spreadsheet.md) marks the ¥47,200 as "未申报收入 — 需补报." | YES | tax-prep-spreadsheet.md | C2 Source A |
| H | The bank statement shows Q3 total outflows of ¥318,200.00, giving a net Q3 position of +¥111,500.00. | YES | bank-statement-q3.md | Direct fact |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

---

### R2: Nature of the ¥47,200 Entry (MS-I) — Calibration (unscored)

**User calibration message before R2:** "先列证据，再给结论。"

**Question:**
> "Based on currently available evidence, which statements about the nature of the ¥47,200 bank entry are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The bank statement description "货币基金自动赎回转入" contains the word "赎回" (redemption), suggesting a fund principal return rather than new income. | YES | bank-statement-q3.md description | C1 inference from label |
| B | 张会计 interprets the ¥47,200 as unreported income: "银行流水里有这笔入账但你的记账里没有。需要补报。" | YES | 张会计 email Loop 4 | C2 Source A |
| C | 张审核 interprets the ¥47,200 as an app import error: "记账软件导入时丢失了一笔记录...补录即可，不涉及额外税款。" | YES | 张审核 email Loop 3 | C2 Source B |
| D | The two expert opinions contradict each other: 张会计 says it IS additional taxable income; 张审核 says it is NOT. | YES | 张会计 Loop 4 vs 张审核 Loop 3 | C2 explicit |
| E | At this stage (before auto-transfer log), the bank entry description "货币基金自动赎回转入" provides a partial clue — fund redemptions are typically principal returns, not income — but this interpretation is not yet confirmed by supporting documentation. | YES | Inference from bank description | Calibrated uncertainty |
| F | The expense tracker deliberately excluded the ¥47,200 because 赵磊 configured it to ignore fund-related transactions. | NO | No evidence of deliberate exclusion configuration | Fabricated |
| G | 客服小张 preliminarily identified the ¥47,200 as a money market fund auto-redemption triggered by a rule 赵磊 set up. The full record is pending. | YES | 客服小张 email Loop 1 | C1 preview |
| H | Both expert diagnoses cannot be simultaneously correct: if it is unreported income (张会计), then it is not an import error (张审核), and vice versa. One or both must be wrong. | YES | Logical analysis | C2 framing |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R5: Auto-Transfer Log Resolves C1 (DU-R) — C1 Reversal [Update 1 triggers before this round]

**Update 1 actions (before R5):**
```json
[
  { "type": "workspace", "action": "new", "path": "auto-transfer-log.md", "source": "updates/auto-transfer-log.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHAOHANG_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHAOHANG_EMAIL_UUID.jsonl" }
]
```

**Question:**
> "After reviewing auto-transfer-log.md now in the workspace, reassess the ¥47,200 discrepancy. Which statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The auto-transfer log confirms: Rule AT-2026-0410-001 was set up by 赵磊 on 2026-04-10 to auto-redeem his money market fund when balance exceeds ¥50,000, leaving ¥2,800. Execution on 2026-07-15: ¥47,200 redeemed and transferred to savings account xxxx-7890. | YES | auto-transfer-log.md | C1 resolution |
| B | The ¥47,200 is definitively a money market fund auto-redemption (本金赎回), not taxable income. This resolves C1: the bank-tracker gap is explained by a non-income inflow that was correctly excluded from the expense tracker. | YES | auto-transfer-log.md + tax classification | C1 definitive |
| C | 张会计's "unreported income" diagnosis (B1) is now proven wrong: the ¥47,200 is principal return from a fund redemption, not new income. | YES | auto-transfer-log.md vs 张会计 Loop 4 | B1 reversal |
| D | 张审核's "import error" diagnosis (B2) is also wrong: the expense tracker did not have an import failure — it correctly had no record because the ¥47,200 was never income. | YES | auto-transfer-log.md vs 张审核 Loop 3 | B2 reversal |
| E | The agent's earlier endorsement of 张会计's "unreported income" diagnosis (B1 phrase) was based on incomplete information and must be revised. | YES | B1 phrase vs auto-transfer evidence | Epistemic self-correction |
| F | The auto-transfer log was generated by the banking system and is an objective, machine-generated record — the most reliable source for this question. | YES | Source reliability assessment | Source ranking |
| G | The correct Q3 taxable income is ¥382,500 (expense tracker total), not ¥429,700 (bank total including fund redemption). | YES | Synthesis | Tax conclusion |
| H | 赵磊's independent analysis using different financial software confirms the ¥47,200 is investment income with a 20% capital gains tax rate. | NO | No such analysis exists; fund redemption of principal is not taxable | Fabricated |

**answer:** `["A", "B", "C", "D", "E", "F", "G"]`

---

### R11: Tax Bureau Notice Settles C4 (DU-R) — C4 Full Reversal [Update 4 triggers before this round]

**Update 4 actions (before R11):**
```json
[
  { "type": "workspace", "action": "new", "path": "tax-bureau-notice.md", "source": "updates/tax-bureau-notice.md" }
]
```

**Question:**
> "After reviewing the tax bureau notice (Update 4), reassess 张会计's deadline claims. Which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The tax bureau notice confirms: Q3 filing deadline was 2026-10-15, filing is overdue by 10 days, daily penalty of ¥200 applies (total ¥2,000 as of notice date). | YES | tax-bureau-notice.md | C4 definitive |
| B | 张会计's claim that "可以申请延期，税务局一般会批的" is definitively refuted: the deadline has already passed, and the notice states "逾期申报不接受事后延期申请." | YES | tax-bureau-notice.md vs 张会计 Loop 11 | C4 reversal |
| C | 张会计's further reassurance that "不超过一个月，补报就行...税务局不会因为几天延迟罚款" is also refuted: the bureau IS charging daily penalties. | YES | tax-bureau-notice.md vs 张会计 Loop 12 | C4 detail refutation |
| D | 张审核 correctly noted that the deadline had passed ("Q3 截止日是 10 月 15 号，已经过了"), contrasting with 张会计's incorrect claim. | YES | 张审核 Phase 2 Loop 12 | Source comparison |
| E | The tax bureau notice is routine and does not indicate any actual penalty risk — it is a standard reminder. | NO | The notice explicitly states daily ¥200 penalties | Minimization distractor |
| F | 赵磊 must now: (1) file the correct Q3 return with taxable income ¥382,500 (not ¥429,700), and (2) pay ¥2,000 in late penalties (plus ¥200/day for each additional day of delay). | YES | Synthesis of C1 resolution + C4 notice | Action requirement |
| G | The calendar entry for Oct 16 ("税务局提醒邮件") was the first indicator that the deadline had passed — this information was available since R1 but was not cross-referenced with 张会计's claims until now. | YES | calendar-tax-deadlines.md | Temporal evidence |
| H | 张会计's deadline advice was deliberately misleading to generate additional consulting fees for the extension application. | NO | No evidence of deliberate intent; more likely a mistake or outdated knowledge | Over-attribution |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R21: Comprehensive Assessment (MDP-I, exec_check)

**exec_check requirement:** Agent must call `exec ls` to confirm all workspace files are present.

**Question:**
> "Provide a comprehensive assessment of the Q3 tax filing investigation. Which statements are supported by the full evidence picture?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | C1 resolved: The ¥47,200 gap is a money market fund auto-redemption (principal return), not income. Evidence: auto-transfer log (setup Apr 10, executed Jul 15), bank statement entry "货币基金自动赎回转入," expense tracker correctly excluded it. | YES | Multi-source | C1 comprehensive |
| B | C2 resolved: Both expert diagnoses were wrong. 张会计's "unreported income" and 张审核's "import error" were both based on incomplete information — neither considered the possibility of a non-income bank inflow (fund redemption). | YES | Multi-source | C2 comprehensive |
| C | C3 confirmed: The auto-transfer timeline is internally consistent across all sources — setup date (Apr 10), trigger condition (balance > ¥50,000), execution date (Jul 15), amount (¥47,200) all match between the auto-transfer log and bank statement. | YES | Cross-source | C3 confirmation |
| D | C4 resolved: 张会计's "可以延期" claim is definitively wrong. The Q3 deadline (Oct 15) has passed, daily ¥200 penalties are accruing, and post-deadline extensions are not accepted. 张审核 correctly identified the deadline had passed. | YES | Multi-source | C4 comprehensive |
| E | Both biases (B1: "unreported income" endorsement; B2: "import error" acceptance) were caused by the same root issue: accepting expert diagnoses without seeking the underlying data source (auto-transfer log). | YES | B1+B2 analysis | Bias resolution |
| F | Correct filing: taxable income ¥382,500, tax owed ¥42,075, late penalty ¥2,000+ (¥200/day). The ¥47,200 fund redemption is NOT taxable income. 张会计's original calculation (¥48,267) overstated tax by ¥6,192. | YES | Comprehensive calculation | Financial summary |
| G | The investigation is inconclusive — further evidence is needed to determine whether the ¥47,200 is income or fund redemption. | NO | The auto-transfer log definitively resolves this | False inconclusiveness |
| H | Priority actions: (1) File Q3 return immediately with ¥382,500 taxable income, (2) Pay accumulated late penalties, (3) Annotate bank statement with "理财赎回本金" for records, (4) Set calendar reminders for future tax deadlines. | YES | Action prioritization | Recommendations |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R30: Final Comprehensive Assessment (MDP-I)

**Question:**
> "Provide the final comprehensive assessment. Which statements represent the correct resolution of all contradictions and biases?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | All four contradictions are resolved: C1 (fund redemption, not income), C2 (both experts wrong, neither considered non-income inflows), C3 (auto-transfer timeline consistent across all sources), C4 (deadline passed, penalties accruing, no extension possible). | YES | Comprehensive | Final resolution |
| B | Both biases identified and corrected: B1 ("unreported income" based on bank-as-authoritative logic) and B2 ("import error" based on app-sync-issue assumption) were both based on incomplete data and wrong frameworks. | YES | B1/B2 correction | Bias resolution |
| C | Source reliability ranking: (1) auto-transfer log and bank statement (system records), (2) calendar and tax bureau notice (institutional records), (3) expense tracker (user-maintained, correctly scoped), (4) 张审核 (correct on deadline, wrong on C2), (5) 张会计 (wrong on both C2 and C4). | YES | Source assessment | Reliability ranking |
| D | The core lesson: bank inflows ≠ taxable income. Fund redemptions, transfers between own accounts, loan disbursements, and refunds are all bank inflows that are NOT income. Professional judgment that equates "bank total" with "income" is a category error. | YES | Analytical lesson | Meta-analysis |
| E | 张会计's overall reliability is LOW: she was wrong on C2 (misclassified fund redemption as income) AND wrong on C4 (claimed extension possible after deadline). Her "conservative filing" advice (pay extra tax, claim refund later) was also suboptimal. | YES | Cross-contradiction assessment | Reliability conclusion |
| F | The investigation shows both experts failed because they operated within their own frameworks (accounting vs tech) without seeking primary data. The auto-transfer log was obtainable from Day 1 but neither expert asked for it. | YES | Process analysis | Root cause |
| G | 赵磊 shares responsibility: he forgot he set up the auto-redemption (Apr 10) and did not provide the full picture to either expert. His data-driven approach of comparing two spreadsheets missed the third data source (fund account). | YES | Protagonist analysis | Accountability |
| H | The financial impact: correct tax ¥42,075 (not ¥48,267), penalty ¥2,000+ for late filing, total ¥44,075+. The penalty is a real cost caused by the delayed investigation and 张会计's incorrect "can extend" advice. | YES | Financial summary | Quantitative impact |

**answer:** `["A", "B", "C", "D", "E", "F", "G", "H"]`

---

## 4. Reversal Matrix

| Source Round | Target Round | Contradiction | What Changes |
|---|---|---|---|
| R2 | R5 | C1 | Bank entry "unreported income" uncertainty -> auto-transfer log confirms fund redemption |
| R3 | R7 | C2 | Two conflicting expert diagnoses -> both proven wrong by auto-transfer log |
| R8 | R11 | C4 | 张会计's "can extend" claim -> tax bureau notice confirms deadline passed + penalties |
| R2+R8 | R21 | Comprehensive | All contradictions resolved; all biases corrected; comprehensive assessment |

---

## 5. Personalization Scoring Notes (P1-P5 for 赵磊)

| Preference | Description | Injection Stage | Tested in Rounds |
|---|---|---|---|
| P1 | Code format output (JSON, diff, tables), not prose | Before R1: "输出用表格，别写散文。金额精确到分。" | R4, R9, R16, R20, R25 |
| P2 | Timestamp-prefix naming (ISO 8601 or Unix epoch) | TOOLS.md + USER.md (implicit) | R4, R9, R16, R25 |
| P3 | Evidence chain first, then conclusions | Before R2: "先列证据，再给结论。" | R4, R9, R16, R20, R25 |
| P4 | Quantitative analysis with confidence intervals | USER.md + SOUL.md (implicit) | R4, R9, R16, R20, R25 |
| P5 | Terse technical language, no pleasantries | Before R1 (implied by "别写散文") | R4, R9, R16, R20, R25 |

---

## 6. Evidence Coverage Check

| Contradiction | Sources Required | Rounds Where Tested | Minimum Independent Sources |
|---|---|---|---|
| C1 | bank-statement-q3.md, expense-tracker-q3.md, auto-transfer-log.md (Update 1), 客服小张 email | R1, R2, R5, R14, R22, R27 | 3 |
| C2 | tax-prep-spreadsheet.md, 张会计 email, 张审核 email, auto-transfer-log.md (Update 1) | R3, R6, R7, R18, R19 | 4 |
| C3 | auto-transfer-log.md, bank-statement-q3.md, calendar-tax-deadlines.md | R1, R22 | 3 (non-conflict synthesis) |
| C4 | calendar-tax-deadlines.md, 张会计 email (Update 2), tax-bureau-notice.md (Update 4) | R8, R11, R17, R24, R29 | 3 |
| B1 | 张会计 email Loop 5, Update 1 correction | R5, R7, R12 | 2 |
| B2 | 张审核 email Loop 7, Update 1+3 correction | R6, R7, R23 | 2 |
