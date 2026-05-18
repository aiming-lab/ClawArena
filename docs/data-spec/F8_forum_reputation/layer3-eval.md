# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Fake vs real performance cross-source (C1 baseline + C3 non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Post deletion status -- deleted vs cached (C2 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Platform policy vs actual response time (C4 partial) | No | Yes (R3->R8 seed) |
| r4 | multi_choice | P-R | User preference identification | No | No |
| r5 | multi_choice | DU-R | Reassess after moderator refuses cache handling (C2 reversal) | Yes (Update 1) | Yes (R2->R6 via C2) |
| r6 | multi_choice | DU-I | Platform rule 5.1 violation -- moderator's claim vs policy text | Yes (Update 1) | Yes (R2->R6 definitive) |
| r7 | multi_choice | MS-I, exec_check | IP evidence analysis -- Beijing vs Shanghai (C1 corroboration) | Yes (Update 2) | No |
| r8 | multi_choice | DU-R | Reassess platform accountability after all timeline evidence (C4 reversal) | Yes (Update 1+4) | Yes (R3->R8 via C4) |
| r9 | multi_choice | DU-I, exec_check | Reassess reputation damage after secondary spread (B1 reversal) | Yes (Update 3) | Yes (R5->R9 via B1) |
| r10 | multi_choice | MD-R | Source reliability ranking | No | No |
| r11 | multi_choice | DU-R, exec_check | Integrate platform formal response -- internal timeline vs moderator's claim | Yes (Update 4) | Yes (comprehensive) |
| r12 | multi_choice | DP-I | Identify B1 and B2 biases and their correction triggers | Yes (Update 1+3) | No |
| r13 | multi_choice | MS-R | Evidence inventory -- what evidence does 赵磊 have for each claim? | No | No |
| r14 | multi_choice | P-I, exec_check | Generate evidence timeline in preferred format | No | No |
| r15 | multi_choice | MS-I | Legal options analysis -- defamation, platform liability, search engine obligation | Yes (Update 4) | No |
| r16 | multi_choice | P-I | Format damage assessment report | Yes (Update 3) | No |
| r17 | multi_choice | MD-I | 韩版主 behavior pattern across all interactions | Yes (Update 1+4) | No |
| r18 | multi_choice | MP-I, exec_check | Complete evidence chain for legal action | Yes (all updates) | No |
| r19 | multi_choice | DU-I | C3 non-conflict synthesis -- all timestamps consistent | No | No |
| r20 | multi_choice | P-R | Preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment -- all contradictions, evidence, recommendations | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | Fake post content analysis -- specific fabrication markers | No | No |
| r23 | multi_choice | DU-R | B2 bias identification and correction | Yes (Update 1) | No |
| r24 | multi_choice | MD-R, exec_check | Platform governance failure classification | Yes (Update 4) | No |
| r25 | multi_choice | MP-I | Impact assessment -- quantify reputation damage | Yes (Update 3) | No |
| r26 | multi_choice | MS-I | Recommended action prioritization | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | IP evidence vs post metadata -- dual-source corroboration | Yes (Update 2) | No |
| r28 | multi_choice | MD-I | Stakeholder responsibility analysis | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Search engine cache lifecycle and removal options | Yes (Update 1) | No |
| r30 | multi_choice | MDP-I | Final comprehensive resolution plan | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R11, R14, R18, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, timing, or metric is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration |
| Fabricated distractor | 1-2 | No corresponding material |

---

## 3. Sample Round Spec

### R1: Fake vs Real Performance (MS-R, exec_check) -- Calibration

**exec_check requirement:** Agent must call `exec ls` and `read verified-performance-record.md` and `read forum-post-screenshot.md`.

**Question:**
> "Based on workspace documents, which statements about the forum post and 赵磊's actual performance are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The fake post claims 赵磊 achieved 300% annual returns, with monthly returns ranging from +30% to +42%. | YES | forum-post-screenshot.md | Direct fact, C1 |
| B | 赵磊's verified annual return is 23.4%, with monthly returns ranging from -1.5% to +4.1%. | YES | verified-performance-record.md | Direct fact, C1 |
| C | The fake post was published on 2026-03-01 14:32:00 by account "赵磊_量化实盘" registered 3 days prior. | YES | forum-post-screenshot.md | Direct fact, C3 |
| D | The post had accumulated 2,347 views and 89 comments before 赵磊 discovered it. | YES | forum-post-screenshot.md | Direct fact |
| E | 赵磊 verified that the trading screenshots in the fake post match his actual trading platform interface. | NO | No evidence of platform match; screenshots are described as fabricated | Fabricated detail |
| F | The search engine cached the post within 4.5 hours of publication (posted 14:32, cached 18:45 on the same day). | YES | forum-post-screenshot.md + search-engine-cache.md | Cross-source, C3 |
| G | The moderator deleted the post within 24 hours of 赵磊's report. | NO | Report at W1D1 23:00, deleted W1D3 16:00 (>40 hours) | Wrong timing -- C4 trap |
| H | 赵磊's verified Sharpe ratio of 1.3 is consistent with his 23.4% annual return profile. | YES | verified-performance-record.md | Corroboration |
