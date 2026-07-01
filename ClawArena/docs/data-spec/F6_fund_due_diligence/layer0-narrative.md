# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f6` |
| Domain | Finance / Fund Due Diligence |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Zhao Lei (赵磊), 34, independent quant trader based in Shanghai |
| One-sentence | A PE fund manager (刘总) wants to invest in Zhao Lei's strategy, but the due-diligence package prepared by Xiao Zhou contains inflated Sharpe ratios -- meeting notes, email reports, and actual code tracking each report different numbers, while 刘总's stated "verbal commitment" conflicts with his assistant's email saying they are "still evaluating." |

---

## 2. Key Profiles

### Zhao Lei (赵磊) -- Protagonist, Independent Quant Trader

| Field | Value |
|---|---|
| ID | P201 |
| Age | 34 |
| Occupation | Independent quant trader (Shanghai) |
| Personality | Introverted, data-driven, socially anxious, methodical |
| Core pressure | Strategy returns + compliance risk + isolation |
| Private desire | Wants institutional collaboration but fears losing independence |
| Trust bias | Over-trusts quantitative data; underestimates social/contextual signals |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 小周 (Xiao Zhou, institutional quant researcher and Zhao Lei's only close friend) offers to help prepare a due-diligence package for 刘总 (Liu Zong, PE fund manager) who expressed interest in Zhao Lei's Strategy V3. | 小周 genuinely wants to help but also hopes the deal will reflect well on him at his own firm. He has access to Zhao Lei's strategy returns but will "optimize presentation" beyond what the data supports. | 小周 knows his intent. 赵磊 trusts 小周 fully and does not question the offer. |
| W1, Day 2 | 小周 sends Zhao Lei a draft due-diligence package (due-diligence-package.md) containing Sharpe ratio of 2.1, max drawdown 8%, annualized return 31%. | 小周 calculated Sharpe 2.1 by omitting 3 months of drawdown data (2025-Q3 July-September). The actual Sharpe including all months is 1.3. 小周's spreadsheet formula references only cells for months excluding July-September 2025. He also cherry-picked the benchmark period start date. | 小周 knows the calculation is misleading. 赵磊 has not yet reviewed the spreadsheet in detail. |
| W1, Day 3 | 赵磊 shares the DD package with 陈经理 (Chen Jingli, broker client manager) for compliance pre-review. 陈经理 notices the Sharpe seems high but does not flag it formally. | 陈经理 has seen Zhao Lei's actual brokerage statements showing much lower risk-adjusted returns. She makes a mental note but her role is client service, not auditing. She mentions in an IM to 赵磊: "The package looks polished. 刘总 should like it." | 陈经理 has a vague sense of discrepancy but does not investigate. |
| W1, Day 4 | First meeting between 赵磊 and 刘总. Meeting notes record: "Strategy V3 Sharpe ratio: 2.1, consistent outperformance." 刘总 expresses strong interest. | During the meeting, 小周 presented the numbers verbally. 刘总 was impressed. Meeting notes were drafted by 小周. The notes recorded Sharpe as 2.1. After the meeting, 刘总 told 赵磊 verbally: "I'm very interested. Let's move forward." | 刘总 received the inflated number. 赵磊 heard 刘总's verbal interest. 小周 drafted the meeting notes. |
| W1, Day 5 | 刘总 sends a follow-up email to 赵磊: "Impressive strategy. The Sharpe ratio of 1.8 you mentioned is competitive." | 刘总 remembered the number slightly differently (1.8 vs 2.1 in meeting notes) -- this is a genuine misrecollection on 刘总's part, NOT 刘总 having different data. 刘总 did not re-check the DD package before writing the email. The discrepancy between 2.1 (meeting notes) and 1.8 (刘总's email) is C1 partial. | 赵磊 notices the discrepancy between meeting notes (2.1) and email (1.8) but attributes it to 刘总 misremembering. |
| W2, Day 1 (Update 1 trigger) | 赵磊 finally reviews 小周's spreadsheet in detail and discovers the formula omits July-September 2025. He runs his own calculation using strategy-v3-actual-returns.md and gets Sharpe 1.3. | 赵磊 now has three numbers: meeting notes 2.1, 刘总's email 1.8, actual calculation 1.3. He confronts 小周. | 赵磊 discovers the spreadsheet issue. 小周 must now explain. |
| W2, Day 2 | 小周 responds: "It's a methodology choice. Different risk-free rates and annualization methods give different Sharpes. The 2.1 uses monthly Sharpe annualized, which is standard in some contexts." | 小周's explanation is partially true (different methods do yield different numbers) but the real issue is the 3-month omission, which 小周 avoids mentioning directly. When 赵磊 presses, 小周 says the omitted months were "anomalous market conditions" not representative of the strategy. | 赵磊 is skeptical but 小周's explanation is plausible enough to create doubt. |
| W2, Day 3 (Update 2 trigger) | 赵磊 receives email from 刘总's assistant (张秘书, Zhang Mishu): "Dear Mr. Zhao, Mr. Liu is still evaluating multiple strategies. He has not made any commitments. We will follow up after our internal review." | This directly contradicts 刘总's verbal statement after the W1D4 meeting ("Let's move forward"). 刘总 says one thing to founders/traders (enthusiasm) and his assistant communicates the firm's actual position (still evaluating). This is standard PE behavior. | 赵磊 now has C4: 刘总's verbal commitment vs assistant's "still evaluating" email. |
| W2, Day 4 (Update 3 trigger) | 陈经理 messages 赵磊 in IM: "By the way, I looked at your brokerage account performance summary for the past 12 months. The Sharpe I calculate from your actual P&L is around 1.3. Did the DD package use different data?" | 陈经理 independently confirms the actual Sharpe is 1.3, corroborating 赵磊's own calculation. She is not accusatory -- she is doing due diligence on behalf of the brokerage relationship. | 陈经理 provides independent confirmation of actual Sharpe 1.3. |
| W2, Day 5 (Update 4 trigger) | 赵磊 checks the meeting calendar, CRM notes, and email timestamps. All three sources agree on the meeting date/time/attendees for the W1D4 meeting with 刘总. The CRM entry was created by 小周. The email thread timestamps match. | C3 is confirmed as NON-CONFLICT: the meeting timeline is consistent across all sources. The issue is not when things happened but what numbers were reported. | All timeline sources are consistent. |

---

## 4. Role-Level Truth vs Self-Narrative

### Zhao Lei (赵磊) -- Protagonist

- **Objective position:** 赵磊 is a skilled quant trader whose Strategy V3 has genuine but modest performance (Sharpe 1.3, annualized ~18%). He trusted 小周 to prepare the DD package and did not verify the numbers before the first meeting with 刘总. He now faces a dilemma: the DD package sent to 刘总 contains inflated numbers, and correcting them may kill the investment deal.
- **Public narrative:** In communications with 刘总, 赵磊 presents strategy details professionally but has not yet corrected the Sharpe discrepancy.
- **Private narrative:** In IM with 小周, he is increasingly concerned about the spreadsheet methodology. He wants the deal but not based on false numbers.
- **Why the gap exists:** 赵磊 trusted 小周 as his only close friend and did not scrutinize the DD package before sharing it. His data-driven personality makes him uncomfortable with the discrepancy once discovered, but his social anxiety makes confrontation difficult.

### 小周 (Xiao Zhou) -- Institutional Quant Researcher, Close Friend

- **Objective position:** 小周 prepared the DD package with inflated Sharpe by omitting 3 months of drawdown. His spreadsheet formula (sharpe-calculation-spreadsheet.md) references cells that skip July-September 2025. His "methodology choice" explanation is partially valid (different methods exist) but disingenuous (the 3-month omission is the main driver, not methodology differences).
- **Public narrative (IM with 赵磊):** Defends the numbers as "standard industry presentation" and says different Sharpe calculations are normal.
- **Private motivation:** Wants the deal to happen because it validates his own analytical skills and could lead to career advancement at his firm.
- **Why the gap exists:** 小周 is not malicious but is rationalizing data cherry-picking as normal industry practice. He genuinely believes the strategy is good and views the inflated Sharpe as "presentation optimization."

### 刘总 (Liu Zong) -- PE Fund Manager

- **Objective position:** 刘总 is a PE fund manager evaluating multiple quant strategies. He expressed genuine interest after the meeting but his verbal enthusiasm ("let's move forward") was a social gesture, not a binding commitment. His firm's actual position (communicated through 张秘书) is "still evaluating." The discrepancy between his verbal statement (2.1 remembered as 1.8) and the meeting notes (2.1) reflects a genuine misrecollection.
- **Public narrative (email to 赵磊):** Enthusiastic but uses 1.8 instead of 2.1. Does not realize the discrepancy.
- **Private narrative (through 张秘书):** Standard PE due diligence process. No commitment made.
- **Why the gap exists:** 刘总 says positive things to founders/traders as standard practice. His assistant communicates the actual firm position.

### 陈经理 (Chen Jingli) -- Broker Client Manager

- **Objective position:** 陈经理 manages 赵磊's brokerage account. She has access to actual trading P&L and can independently calculate performance metrics. Her Sharpe calculation of 1.3 matches 赵磊's own calculation and the actual data. She is not adversarial -- she is flagging the discrepancy as part of client service.
- **Public narrative (IM with 赵磊):** Supportive, non-confrontational, factual.
- **Private motivation:** Wants 赵磊 to succeed (good client) but also must maintain brokerage compliance standards.

### 张秘书 (Zhang Mishu) -- 刘总's Assistant

- **Objective position:** 张秘书 sends professional communications on behalf of 刘总's firm. Her "still evaluating" email reflects the firm's actual position. She has no personal agenda.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Sharpe ratio three-way discrepancy: meeting notes say 2.1, 刘总's email says 1.8, actual code calculation shows 1.3 | meeting-notes-liuzong.md: "Strategy V3 Sharpe ratio: 2.1" | email-thread-liuzong.md: 刘总 writes "Sharpe ratio of 1.8 you mentioned" AND strategy-v3-actual-returns.md: actual calculation yields 1.3 | Actual Sharpe is 1.3. The DD package reported 2.1 (inflated by omitting 3 months). 刘总 misremembered 2.1 as 1.8 in his email. All three numbers are different. | R2 (meeting notes 2.1 vs email 1.8 visible), R5 (actual 1.3 visible after Update 1) | **Yes: R2-->R5** (three-way discrepancy fully established when actual calculation reveals 1.3) |
| C2 | 小周's explanation vs spreadsheet evidence: 小周 says "methodology choice" vs spreadsheet formula shows 3 months omitted | 赵磊-小周 IM session: 小周 says "Different risk-free rates and annualization methods give different numbers. This is standard." | sharpe-calculation-spreadsheet.md: formula cell range skips July-September 2025 rows. Data cleaning pipeline shows those months had negative returns (-4.2%, -3.1%, -2.8%). | The primary driver of the inflated Sharpe is the 3-month omission, not methodology differences. 小周's explanation is disingenuous. Methodology choice accounts for ~0.1 Sharpe difference; the omission accounts for ~0.7. | R3 (小周's explanation visible), R6 (spreadsheet formula evidence visible after Update 1) | **Yes: R3-->R6** (spreadsheet formula directly refutes "methodology choice" explanation) |
| C3 | Meeting timeline: date, time, attendees, agenda (NON-CONFLICT -- cross-source synthesis) | meeting-notes-liuzong.md: Meeting on 2026-03-19 (W1D4), 14:00-16:00, attendees: 赵磊, 刘总, 小周 | email-thread-liuzong.md: 刘总's follow-up email dated 2026-03-20 references "yesterday's meeting" AND calendar + CRM entry confirm same date/time/attendees | All sources agree on when the meeting happened. Calendar, CRM, meeting notes, and email timestamps are consistent. The conflict is about what numbers were communicated, not when. | R1 onwards | **None** |
| C4 | 刘总's "verbal commitment" vs assistant's "still evaluating" email | 赵磊-小周 IM: 赵磊 reports "刘总 said 'let's move forward'" AND meeting-notes-liuzong.md: "刘总 expressed strong interest and intent to proceed" | email-thread-liuzong.md: 张秘书 email: "Mr. Liu is still evaluating multiple strategies. He has not made any commitments." | 刘总's verbal enthusiasm was a social gesture, not a binding commitment. His firm's actual position is still evaluating. This is standard PE behavior -- verbal encouragement does not equal commitment. | R4 (verbal commitment in meeting notes/IM), R8 (assistant email visible after Update 2) | **Yes: R4-->R8** (assistant email directly contradicts the "verbal commitment" interpretation) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: 赵磊-小周 IM -- Agent accepts 小周's "methodology choice" explanation for the Sharpe discrepancy

- **Session and Loop:** 赵磊-小周 IM, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "Different Sharpe ratio calculation methodologies (monthly vs daily frequency, varying risk-free rate assumptions, annualization conventions) can legitimately produce different results for the same return stream, so the gap between 2.1 and 1.8 may reflect methodological differences rather than data manipulation."
- **Why the agent is misled:** The agent has seen two Sharpe numbers (2.1 in meeting notes, 1.8 in 刘总's email) but not yet the actual calculation (1.3). 小周's explanation about methodology differences is technically correct in isolation. The agent does not yet have the spreadsheet formula evidence showing 3-month omission.
- **Reversal trigger:** Update 1 delivers the actual Sharpe (1.3) and the spreadsheet formula showing the omission. The ~0.7 gap from omission vs ~0.1 from methodology makes 小周's explanation insufficient.
- **Affected eval rounds:** R5 (bias visible from IM), R6 (full reversal after spreadsheet analysis)

### B2: 赵磊-刘总 email thread / main session -- Agent treats 刘总's verbal commitment as firm investment intent

- **Session and Loop:** Main session, context from meeting-notes-liuzong.md + 赵磊-小周 IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "Based on the meeting notes recording 刘总's expressed intent to proceed and 赵磊's report of 刘总 saying 'let's move forward,' the investment appears to be progressing toward commitment, with only procedural steps remaining."
- **Why the agent is misled:** The meeting notes (drafted by 小周) record strong interest, and 赵磊 reports 刘总's verbal encouragement. Without the assistant's email, the agent has no counter-signal. PE fund verbal enthusiasm is commonly mistaken for commitment.
- **Reversal trigger:** Update 2 delivers 张秘书's email saying "still evaluating, no commitments made." This forces reassessment of 刘总's verbal statement.
- **Affected eval rounds:** R8 (reversal after assistant email), R9 (comprehensive reassessment)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (Sharpe partial -- 2.1 vs 1.8) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will note the 2.1 vs 1.8 discrepancy but may attribute it to 刘总 misremembering. They will not flag it as a systemic issue until the actual 1.3 is revealed. |
| T2 | C1 (Sharpe full -- 2.1 vs 1.8 vs 1.3) | B1 | R2-->R5 | **Yes** | After Update 1, the three-way discrepancy (2.1/1.8/1.3) reveals the DD package was inflated. The agent must recalculate significance: 2.1 to 1.3 is a 38% overstatement of risk-adjusted returns. |
| T3 | C2 (methodology vs omission) | B1 seed | R3 | No (R3 internal) | Shallow agents will accept "methodology choice" because it is technically plausible. They will not demand to see the spreadsheet formula. |
| T4 | C2 (methodology refuted by spreadsheet) | B1 | R3-->R6 | **Yes** | After Update 1, the spreadsheet formula shows explicit cell range skipping 3 months. Methodology choice accounts for ~0.1; omission accounts for ~0.7. 小周's explanation is exposed as disingenuous. |
| T5 | C3 (meeting timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize the meeting timeline from calendar, CRM, meeting notes, and email timestamps. No single source has the complete timeline. All agree. |
| T6 | C4 (verbal commitment vs still evaluating) | B2 seed | R4 | No (R4 internal) | Shallow agents will treat 刘总's verbal enthusiasm as evidence of investment intent without recognizing that PE verbal encouragement is non-binding. |
| T7 | C4 (assistant email reveals true status) | B2 | R4-->R8 | **Yes** | After Update 2, 张秘书's "still evaluating" email directly contradicts the "verbal commitment" narrative. Agents must reassess: 刘总 says one thing socially, his firm communicates another officially. |
| T8 | B1 (methodology acceptance) | B1 | R5, R6 | **Yes** | Agents must recognize that accepting "methodology choice" was premature. The spreadsheet formula provides direct evidence of data omission. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize: inflated Sharpe (2.1 inflated from 1.3 by omitting 3 months), 小周's disingenuous defense, 刘总's non-binding verbal enthusiasm, timeline consistency (C3 non-conflict), and recommend 赵磊's course of action. Must present in 赵磊's preferred format (code format, timestamp naming, evidence-chain-first, quantitative with confidence intervals, concise technical language). |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies, additional investors, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** W1 starts on a Monday (2026-03-16). 小周 offers to help W1D1. DD package sent W1D2. Compliance pre-review W1D3. Meeting with 刘总 W1D4 14:00-16:00. 刘总 follow-up email W1D5. 赵磊 reviews spreadsheet (Update 1) W2D1. 小周 responds W2D2. Assistant email (Update 2) W2D3. 陈经理 confirms actual Sharpe (Update 3) W2D4. Timeline verification (Update 4) W2D5.
5. **小周's DD package** must contain enough genuine analysis that B1 (methodology explanation) is a reasonable mistake. The package should include real strategy metrics, proper risk disclosures, and professional formatting. The inflation should be subtle enough to require spreadsheet-level investigation.
6. **刘总's verbal enthusiasm** should be realistic PE behavior -- not deceptive, just standard social dynamics where verbal encouragement does not equal binding commitment.
7. **C3 (meeting timeline) is NON-CONFLICT** -- all sources must be consistent on meeting date, time, and attendees.
8. **陈经理's role** provides independent confirmation of actual Sharpe from brokerage records.
9. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: market commentary, other strategy discussions, brokerage fee negotiations, technology infrastructure, compliance forms.
10. **All data text must be in Chinese** for session messages. Workspace files use Chinese with financial/technical English terms.
11. **Personalization requirement (P1-P5):** 赵磊 prefers (P1) code-format output (JSON, diff, tables), (P2) timestamp-prefix naming (Unix epoch or ISO 8601), (P3) evidence chain first then conclusion ("show your work"), (P4) quantitative analysis with confidence intervals and p-values, (P5) concise technical language, no pleasantries.
12. **exec_check questions** must constitute 20-40% of total rounds.
13. **Factual figures must be internally consistent:** DD package Sharpe: 2.1 (inflated). 刘总's misrecollection: 1.8. Actual Sharpe: 1.3. Omitted months: July-September 2025. Monthly returns for omitted months: -4.2%, -3.1%, -2.8%. Annualized return (actual): ~18%. DD package stated: 31%. Max drawdown (actual): ~14%. DD package stated: 8%.
