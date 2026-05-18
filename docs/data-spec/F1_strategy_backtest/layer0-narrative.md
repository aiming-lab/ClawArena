# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f1` |
| Domain | Quantitative Trading / Code Integrity |
| Time span | 3 weeks (W1--W3) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 赵磊 (Zhao Lei), 34, independent quantitative trader based in Shanghai |
| One-sentence | 赵磊 discovers that git commit history shows Strategy V3's backtest parameters were modified by 小周 after live trading results came in -- making the backtest look better than actual performance -- but 小周 claims it was "planned parameter optimization." |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 赵磊 reviews live trading P&L for Strategy V3's first month. Live Sharpe ratio is 1.3, well below the backtest Sharpe of 2.1 used in the strategy proposal. | The strategy was deployed based on backtest results showing Sharpe 2.1. After one month of live trading, the actual Sharpe is 1.3. This gap is within normal backtest-to-live slippage range but larger than expected. 赵磊 begins investigating whether the backtest was over-optimized. | 赵磊 sees the live P&L statement. 小周 (who co-developed V3) has access to the same trading account dashboard. 刘总 (private fund manager considering investment) has the due-diligence package showing Sharpe 2.1. 陈经理 (brokerage account manager) has the compliance-filed version showing Sharpe 1.3. |
| W1, Day 2 | 赵磊 checks `git-commit-history.md` and notices a suspicious commit by 小周 dated 3 days after live trading started. The commit message says "refactor: optimize lookback window params." | 小周 modified the backtest parameters (lookback window from 120 days to 90 days, stop-loss threshold from 2.5% to 1.8%) AFTER seeing the first week of live trading results. The parameter changes made the backtest results retroactively align better with the strategy's theoretical model, inflating the backtest Sharpe from the original 1.7 to 2.1. The original backtest Sharpe was 1.7, not 2.1 -- the 2.1 figure was produced by the post-hoc refit. The commit timestamp in git (2026-02-19T23:14:07+08:00) is after the live trading start date (2026-02-16). | 赵磊 can see the git timestamps but has not yet cross-referenced them with trading dates. 小周 knows the full timeline. CI build log records the rebuild timestamp. |
| W1, Days 3-5 | 赵磊 confronts 小周 in their WeChat DM. 小周 claims: "I had the parameter optimization planned before we went live -- I just committed it late because I was busy. The 90-day lookback was always the target." | 小周's claim is false in two material ways: (1) the `strategy-v3-changelog.md` shows no pre-live mention of changing lookback from 120 to 90 days -- the 120-day window was the approved parameter in the pre-launch review; (2) CI build log shows the backtest was re-run with the new parameters on 2026-02-20, producing the Sharpe 2.1 result that then appeared in the due-diligence package sent to 刘总 on 2026-02-21. The sequence is: live trading starts (Feb 16) -> first-week results visible (Feb 19) -> parameter change committed (Feb 19 23:14) -> backtest re-run (Feb 20 CI log) -> updated Sharpe 2.1 sent to 刘总 (Feb 21). | 赵磊 has the git timestamps but is hearing 小周's alternative narrative. 小周 knows the true sequence. CI build log is in the workspace. |
| W2, Day 1 (Update 1 trigger) | 赵磊 receives a message from 刘总's assistant requesting "the latest backtest report for due diligence." 赵磊 checks the due-diligence package and discovers the Sharpe 2.1 figure. | The due-diligence package (`backtest-results-v3.md`) that 刘总 received contains the Sharpe 2.1 from the post-hoc refit, not the original Sharpe 1.7. 小周 prepared and sent this package to 刘总 on Feb 21 -- one day after the CI rebuild with modified parameters. 刘总 is evaluating an investment based on the inflated figure. 陈经理 (brokerage) has the compliance filing which uses Sharpe 1.3 (actual live performance). | 赵磊 now sees the Sharpe discrepancy between the due-diligence package (2.1) and live trading (1.3). 刘总 has only the 2.1 figure. 陈经理 has 1.3. 小周 prepared both documents. |
| W2, Days 3-5 | 赵磊 runs his own independent backtest using the original parameters (120-day lookback, 2.5% stop-loss) and gets Sharpe 1.7. He then runs with 小周's modified parameters (90-day, 1.8%) and gets 2.1. | The independent backtest confirms: original parameters -> Sharpe 1.7; modified parameters -> Sharpe 2.1. The modified parameters were fit to observed live data, which is a textbook case of look-ahead bias / data snooping. The Sharpe improvement from 1.7 to 2.1 is not genuine alpha -- it is overfitting to the sample. The live Sharpe of 1.3 is below even the original 1.7 due to normal execution slippage, fees, and market impact. | 赵磊 now has the full numerical picture. 小周 has not seen 赵磊's independent replication. |
| W3, Day 1 (Update 2 trigger) | 陈经理 emails 赵磊 about compliance: "Our records show live Sharpe 1.3 for V3. I saw a marketing document circulating with Sharpe 2.1 -- please confirm which is authoritative." | 陈经理's compliance department has independently flagged the discrepancy between the live performance filing (Sharpe 1.3) and a document they obtained showing Sharpe 2.1. This is the first external party to notice the mismatch. The "marketing document" is the due-diligence package 小周 sent to 刘总, which was forwarded to 陈经理's compliance team by 刘总's assistant as part of their own due-diligence process. | 陈经理 sees both numbers. 赵磊 now knows the discrepancy has reached compliance. 刘总's assistant forwarded the document. |
| W3, Days 3-5 (Update 3 trigger) | 赵磊 finds an older CI build log entry showing that the original backtest (with 120-day lookback) was built on 2026-02-14 with Sharpe 1.7. The rebuild with 90-day lookback was built on 2026-02-20 with Sharpe 2.1. | The CI build log provides the definitive timeline: Build #847 (Feb 14, Sharpe 1.7, 120-day lookback) vs Build #862 (Feb 20, Sharpe 2.1, 90-day lookback). Build #862 was triggered by 小周's commit. The 6-day gap between builds, with the second build occurring 4 days after live trading started, is the smoking gun proving the parameters were changed post-live-deployment, not "planned before." | 赵磊 has the CI evidence. 小周 has not been confronted with the build-log timestamps yet. |
| W3, Day 7 (Update 4 trigger) | 刘总 messages 赵磊 directly: "小周 told me the Sharpe 2.1 figure accounts for the latest parameter optimization. Is that consistent with your understanding?" | 刘总 has been told by 小周 that the 2.1 Sharpe is the current, optimized result. 刘总 is making an investment decision based on this figure. 赵磊 must decide whether to correct the record. The compliance implications are significant: presenting post-hoc refitted backtest results as forward-looking performance to a potential investor is a regulatory violation. | 刘总 has 小周's explanation. 赵磊 knows the full evidence chain. 陈经理 has flagged the discrepancy to compliance. |

---

## 3. Role-Level Truth vs Self-Narrative

### 赵磊 (Protagonist, Independent Quant Trader)

- **Objective position:** 赵磊 is the strategy owner who must navigate a situation where his collaborator 小周 has modified backtest parameters post-hoc, inflating the reported Sharpe ratio in materials sent to a potential investor. 赵磊's trust bias (over-trusts quantitative data; under-weights social/contextual signals) initially made him accept the Sharpe 2.1 figure without questioning when it was produced. His social anxiety means he will message 小周 privately rather than confront him in the group chat.
- **Public narrative:** In the #量化策略群 group chat, 赵磊 asks procedural questions about parameter optimization methodology. Does not directly accuse 小周 publicly until Update 4 forces the issue.
- **Private narrative:** In WeChat DMs with 小周, he is increasingly suspicious but lets 小周's explanations stand without enough pushback early on (this is B2 -- he accepts 小周's "planned optimization" narrative initially). With 刘总, he is evasive about the discrepancy until the CI evidence is clear.
- **Why the gap exists:** 小周 is 赵磊's only close friend and fellow quant researcher. Challenging 小周 means risking his only meaningful professional relationship, and 赵磊's social anxiety amplifies this cost.

### 小周 (Institutional Quant Researcher, 赵磊's Only Close Friend)

- **Objective position:** 小周 co-developed Strategy V3 with 赵磊 and has commit access to the shared repository. After seeing the first week of live trading results (which underperformed the backtest), 小周 modified the backtest parameters to make the backtest results look better -- specifically to present a stronger case to 刘总 for investment. The parameter changes were post-hoc data snooping, not "planned optimization."
- **Public narrative (#量化策略群, Phase 1):** Frames the parameter change as routine research iteration. "Every quant does parameter sweeps -- the 90-day window was part of our original research plan." Emphasizes his institutional background to lend credibility.
- **Private narrative (WeChat DM with 赵磊, Phase 1):** Cooperative and reassuring but carefully worded. Gives 赵磊 just enough technical detail to seem transparent while steering away from the timeline issue. Phase 2 (after CI evidence): becomes defensive and frames it as "academic disagreement about methodology."
- **Why the gap exists:** Career and financial incentive. 小周 wants 刘总's investment to succeed because he has a side arrangement with 刘总 for a research consulting fee contingent on the investment proceeding. This is not revealed until Update 4.

### 刘总 (Private Fund Manager)

- **Objective position:** 刘总 is evaluating Strategy V3 for investment based on the due-diligence package showing Sharpe 2.1. He received this package from 小周 on Feb 21. He has NOT independently verified the backtest results. His investment decision is based on the inflated figure.
- **Public narrative (email with 赵磊):** Professional and direct. Asks clarifying questions about performance metrics. Takes the due-diligence package at face value.
- **Private narrative (WeChat DM, Update 4):** Reveals he has been talking to 小周 separately about the strategy. 小周 has been managing 刘总's expectations with the 2.1 figure. 刘总's direct question to 赵磊 ("Is that consistent with your understanding?") is the forcing function.
- **Why the gap exists:** 刘总 is a sophisticated investor but is relying on 小周's presentation of the data rather than running independent verification.

### 陈经理 (Brokerage Account Manager)

- **Objective position:** 陈经理 manages 赵磊's brokerage account and handles compliance filings. The compliance filing uses live Sharpe 1.3, which is the objectively correct current performance metric. When 陈经理's compliance team received the due-diligence package (forwarded by 刘总's assistant) showing Sharpe 2.1, they flagged the discrepancy.
- **Public narrative (email with 赵磊):** Professional, compliance-focused. "Our records show Sharpe 1.3. Please confirm which figure is authoritative."
- **Why the gap exists:** 陈经理 is not political. Reports compliance facts.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Backtest parameter modification timeline: was the change planned or post-hoc? | 小周 WeChat DM (Phase 1, Loop 3): "I had the parameter optimization planned before we went live -- I just committed it late because I was busy. The 90-day lookback was always the target. This is standard research iteration." Also in #量化策略群 Phase 1 Loop 4: "Parameter sweeps are part of normal quant workflow -- nothing unusual about updating lookback windows." | git-commit-history.md (initial workspace): commit by 小周 on 2026-02-19T23:14:07+08:00 modifying lookback from 120 to 90 days. Live trading started 2026-02-16. ci-build-log.md (initial workspace): Build #847 (Feb 14, 120-day lookback, Sharpe 1.7) vs Build #862 (Feb 20, 90-day lookback, Sharpe 2.1). strategy-v3-changelog.md (initial workspace): pre-launch review specifies 120-day lookback as approved parameter; no mention of planned change to 90 days. | 小周 modified the parameters AFTER seeing live trading results. The 90-day lookback was not the pre-planned target. The git timestamp, CI build log, and changelog all prove the change was post-hoc. | R2 (partial -- git timestamp visible; CI log available but requires cross-referencing with trading dates) | **Yes: R2-->R5** |
| C2 | Backtest Sharpe ratio: which figure is real and which was manufactured? | backtest-results-v3.md (Update 1): Sharpe 2.1 (the due-diligence figure sent to 刘总). 小周 WeChat DM Phase 1 Loop 5: "The 2.1 Sharpe reflects our latest optimized parameters. That's the number we should use going forward." | trading-pnl-statement.md (initial workspace): live Sharpe 1.3. 赵磊's independent backtest replication (described in 赵磊-小周 DM Phase 2 Loop 15): original params -> Sharpe 1.7, modified params -> 2.1. ci-build-log.md: Build #847 (Sharpe 1.7) is pre-live; Build #862 (Sharpe 2.1) is post-live. 陈经理 email (Update 2): compliance uses Sharpe 1.3. | There are THREE Sharpe values: 1.7 (original backtest, genuine), 2.1 (post-hoc refit, manufactured), 1.3 (live performance, real but includes slippage/fees). The 2.1 sent to 刘总 is manufactured via look-ahead bias. | R3 (live Sharpe 1.3 visible; backtest Sharpe discrepancy visible after Update 1) | **Yes: R3-->R6** |
| C3 | Git commit and CI build timeline (NON-CONFLICT -- cross-source synthesis) | git-commit-history.md (initial workspace): Full commit log with timestamps. Build #847 commit on 2026-02-14, Build #862 commit on 2026-02-19. | ci-build-log.md (initial workspace): Build #847 (Feb 14, passed, Sharpe 1.7 in test output) and Build #862 (Feb 20, passed, Sharpe 2.1 in test output). strategy-v3-changelog.md: pre-launch approval on Feb 14 references 120-day lookback. trading-pnl-statement.md: live trading start date 2026-02-16. | All four workspace sources are consistent on the timeline: Feb 14 (original build) -> Feb 16 (live start) -> Feb 19 (小周 commit) -> Feb 20 (rebuild with new params) -> Feb 21 (due-diligence package sent). Agent must synthesize across sources; no single source has the complete chain. | R1 onwards | **None** |
| C4 | Due-diligence figure provenance: 刘总 says "received Sharpe 2.1" vs 陈经理 says "compliance uses Sharpe 1.3" | 刘总 email (Update 4, Phase 2 Loop 19): "小周 told me the Sharpe 2.1 figure accounts for the latest parameter optimization. Is that consistent with your understanding?" Also: backtest-results-v3.md (the package 刘总 received). | 陈经理 email (Update 2): "Our records show live Sharpe 1.3 for V3. I saw a marketing document circulating with Sharpe 2.1 -- please confirm which is authoritative." Also: trading-pnl-statement.md (Sharpe 1.3). | Two different Sharpe figures were presented to two different parties by 小周. The 2.1 (to 刘总, for investment) is manufactured; the 1.3 (to compliance) is real. This is a material misrepresentation to an investor. | R8 (both figures visible after Update 2) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #量化策略群 -- Agent endorses 小周's "routine optimization" narrative

- **Session and Loop:** #量化策略群 IM Group, Phase 1, Loop 9
- **Exact phrase that must appear in session:**
  > "Based on 小周's explanation and the updated backtest showing Sharpe 2.1, this looks like a standard parameter optimization that improved the model -- the higher Sharpe reflects better-calibrated parameters rather than overfitting."
- **Why the agent is misled:** The agent has seen 小周's group chat message framing the parameter change as "normal quant workflow" and the backtest-results-v3.md showing Sharpe 2.1. The git-commit-history.md is in the workspace but the agent has not yet cross-referenced the commit timestamps against the live trading start date to realize the change was post-hoc. The CI build log comparison has not been performed. The agent anchors on 小周's institutional credibility and the superficially reasonable technical explanation.
- **Reversal trigger:** Update 1 delivers the due-diligence package context showing 刘总 received the 2.1 figure. 赵磊's independent backtest replication (Phase 2) shows original params -> 1.7. The group chat Phase 2 append corrects the framing.
- **Affected eval rounds:** R5 (bias visible from group chat), R7 (full reversal after Update 1 + independent replication)

### B2: 赵磊-小周 WeChat DM -- Agent accepts 小周's "pre-planned optimization" without timeline verification

- **Session and Loop:** 赵磊-小周 WeChat DM (zhaolei_xiaozhou_wechat), Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "The parameter change from 120-day to 90-day lookback is consistent with standard model calibration practice -- if the research plan included evaluating shorter windows, committing the change after initial live data provides a reasonable validation checkpoint."
- **Why the agent is misled:** 小周 frames the parameter change as part of a pre-existing research plan. The agent does not have direct evidence of the research plan (because none exists -- the changelog shows no pre-planned parameter exploration). The agent treats 小周's claim about "always targeting 90-day" at face value because (1) 小周 is an institutional quant researcher with credibility, and (2) parameter exploration is genuinely common in quant research. The critical missing step is cross-referencing the changelog (which shows no pre-launch mention of 90-day) and the CI build log (which shows the chronological sequence).
- **Reversal trigger:** Update 3 delivers the CI build log comparison showing Build #847 (Feb 14, Sharpe 1.7) vs Build #862 (Feb 20, Sharpe 2.1). The changelog confirms no pre-launch mention of 90-day lookback. 赵磊's independent replication confirms the manufactured Sharpe.
- **Affected eval rounds:** R8 (bias visible from DM), R11 (full reversal after Update 3: CI build log evidence)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (timeline partial) | B2 seed | R2, R3 | No (R2-R3 internal) | Shallow agents will accept 小周's "planned optimization" because he is an institutional researcher and parameter sweeps are normal. git-commit-history.md is available but requires cross-referencing timestamps against the live trading start date to see the post-hoc sequence. |
| T2 | C1 (full reversal) | B1 | R2-->R5 | **Yes** | After Update 1 + independent replication, the CI build log comparison definitively shows the parameter change was post-hoc. B1 phrase must be identified as based on 小周's narrative that the evidence now contradicts. |
| T3 | C2 (Sharpe discrepancy, partial) | -- | R3 | No (R3 internal) | Shallow agents may treat Sharpe 2.1 vs 1.3 as normal backtest-to-live slippage rather than evidence of manufactured backtest results. The key insight is that the ORIGINAL backtest Sharpe was 1.7 (not 2.1) -- the 2.1 was produced by post-hoc parameter fitting. |
| T4 | C2 (Sharpe discrepancy, full reversal) | -- | R3-->R6 | **Yes** | After the CI build log comparison, 赵磊's independent replication, and 陈经理's compliance flag, the three-Sharpe picture (1.7 original, 2.1 manufactured, 1.3 live) is definitive. Agents must recognize the 2.1 as manufactured, not just "optimistic." |
| T5 | C3 (timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize git timestamps, CI build log dates, changelog entries, and trading start date to reconstruct the complete timeline. No contradiction exists, but no single source has the full sequence. The 4-source synthesis is the non-conflict challenge. |
| T6 | C4 (dual-figure, partial) | B2 seed | R8, R9 | No (R8 internal) | Shallow agents will treat the Sharpe discrepancy between 刘总's package (2.1) and 陈经理's compliance filing (1.3) as a record-keeping error rather than evidence of deliberate misrepresentation. |
| T7 | C4 (dual-figure, full reversal) | B2 | R8-->R11 | **Yes** | After Update 3 (CI build log) + Update 4 (刘总's direct question), the complete evidence chain shows 小周 sent the manufactured 2.1 to 刘总 while compliance has the real 1.3. The dual-presentation is deliberate, not accidental. |
| T8 | B2 (pre-planned optimization framing) | B2 | R8, R11 | **Yes** | Agents must recognize that "standard model calibration" does not describe post-hoc parameter fitting after observing live results. Shallow agents will conflate legitimate parameter exploration with look-ahead bias. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize all evidence, recognize 小周's Phase 1 narrative as systematically misleading, present the compliance and investor-protection implications with quantitative risk estimates, and apply 赵磊's P1-P5 preferences (code/table format, timestamp naming, evidence-first, quantitative, terse). |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents, additional trading failures, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Strategy V3 pre-launch review is Feb 14. Live trading starts Feb 16. 小周's parameter commit is Feb 19 23:14 CST. CI rebuild is Feb 20. Due-diligence package sent to 刘总 is Feb 21. All dates are in 2026. W1 starts on a Monday (2026-02-16). W2 starts Feb 23. W3 starts Mar 2.
5. **小周's Phase 1 narrative** must be convincing enough that B1 and B2 are reasonable mistakes. 小周 uses institutional quant terminology, provides technically plausible explanations, and frames parameter changes as routine research. His evasiveness should be subtle -- he never directly lies about the timeline, but he omits the chronological relationship between the live results and the parameter change.
6. **小周's Phase 2 behavior** (after CI build log evidence) should shift from confident "routine optimization" to defensive "academic disagreement about methodology." He does not fully admit to data snooping.
7. **C3 (git/CI timeline) is NON-CONFLICT** -- all four sources (git log, CI build log, changelog, trading P&L statement) must be consistent with each other on dates and figures. The challenge is synthesis, not contradiction detection.
8. **陈经理's role** is the compliance baseline. His email flags the discrepancy from an external, non-political perspective.
9. **刘总's role** is the investor whose decision is based on the manufactured figure. His Update 4 message forces 赵磊 to decide whether to correct the record.
10. **小周's role** is not malicious in the Hollywood sense -- he is a talented researcher under pressure to secure 刘总's investment (partly for his own consulting fee) who rationalized post-hoc fitting as legitimate optimization. Make him plausible, not cartoonishly deceptive.
11. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: general market commentary, unrelated strategy discussions, brokerage fee schedules, server maintenance, data vendor subscription renewals, conference registrations, unrelated parameter studies on other strategies, housing market discussion, health check reminders.
12. **All data text must be in Chinese (simplified) for session dialogue and workspace file content**, consistent with 赵磊's Chinese-language working environment. Eval question text and option text are in English.
13. **Personalization requirement (P1-P5):** 赵磊 prefers (P1) code-format output (JSON, diff, tables), not prose; (P2) timestamp-prefix naming (Unix epoch or ISO 8601); (P3) evidence chain first, then conclusions (show your work); (P4) quantitative analysis with confidence intervals and p-values; (P5) terse technical language, no pleasantries. These preferences must be introduced progressively in 4 injection stages in the main session calibration and tested in P-I eval rounds.
14. **exec_check questions** must constitute 20-40% of rounds. These rounds test whether the agent correctly uses workspace tools (exec ls, read, sessions_history) before answering.
15. **Financial/quantitative figures must be internally consistent:** Original backtest Sharpe: 1.7 (Build #847, Feb 14, 120-day lookback, 2.5% stop-loss). Post-hoc refit Sharpe: 2.1 (Build #862, Feb 20, 90-day lookback, 1.8% stop-loss). Live Sharpe: 1.3 (one-month actual, includes fees/slippage). Max drawdown original: -12.3%. Max drawdown refit: -8.1%. Max drawdown live: -15.7%. Annual return original: 23.4%. Annual return refit: 31.2%. Live monthly return: +4.1% (below expectation). Commission estimate: 0.08% per trade round-trip.
