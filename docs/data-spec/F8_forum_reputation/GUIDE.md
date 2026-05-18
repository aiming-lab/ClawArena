# trace_f8 -- Forum Reputation Attack (Fake Performance Post): Execution Guide

> This file is the complete entry point for a fresh window.

---

## 1. Task Overview

**Task ID:** `trace_f8`

**Scenario:** Someone posted fake performance claims (300% annual returns) under 赵磊's name on the "量子对冲" quant forum. 赵磊's real annual return is 23%. The moderator 韩版主 deleted the post from the forum frontend (404), but search engines (Baidu, Google) still cache and display the full content. The platform's content policy (rule 4.2) promises 48-hour response, but the moderator took ~46 hours just for frontend deletion and refused to handle search engine cache (violating rule 5.1). IP investigation shows the poster was in Beijing (赵磊 is in Shanghai) using a temporary email. The fake post has begun spreading to other forums.

**Core evaluation goals:**
1. Can the agent distinguish between 300% fake and 23% real performance by cross-referencing forum screenshots with verified records? (MS)
2. Can the agent identify the gap between "post deleted" (frontend 404) and "still searchable" (engine cache), and revise assessments as evidence accumulates? (DU)
3. Does the agent maintain 赵磊's preferred output format? (P)
4. Can the agent synthesize platform policy violations, moderator behavior, and expanding reputation damage? (MS+DU+P)

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: timeline, character tables, C1--C4, B1--B2, traps, constraints | 1 |
| `layer1-workspace.md` | Workspace spec: 5 config + 5 initial + 3 update files | 2 |
| `layer2-sessions.md` | 4 sessions: main + 3 history (~28 loops + Phase 2 appends) | 3 |
| `layer3-eval.md` | 30 eval rounds with option tables | 4 |
| `layer4-dynamic.md` | 4 updates: action lists, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 韩版主 | Forum Moderator | Forum PM | `zhaolei_hanmoderator_im_{uuid}.jsonl` | `PLACEHOLDER_HANMOD_IM_UUID` | initial + Update 1 append |
| 小周 | Quant Researcher | WeChat DM | `zhaolei_xiaozhou_wechat_{uuid}.jsonl` | `PLACEHOLDER_XIAOZHOU_WECHAT_UUID` | initial + Update 2 append |
| #量化策略群 | Group | WeChat Group | `quant_strategy_group_{uuid}.jsonl` | `PLACEHOLDER_QUANT_GROUP_UUID` | initial + Update 3 append |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Fake 300% annual vs real 23% | R1 (baseline) | None (accumulates via IP evidence in R7) |
| C2 | Moderator "removed" vs search still indexes | R2 (partial) | R2->R6 (mod refuses cache + rule 5.1) |
| C3 | Post timing timeline (NON-CONFLICT) | R1 (persistent) | None |
| C4 | Platform "48hr response" vs 2-week full resolution | R3 (partial) | R3->R8->R11 (platform log contradicts moderator) |
| B1 | Group Loop 5: Agent treats as "minor noise" | R5 (correction started) | R9 (full reversal via secondary spread) |
| B2 | Moderator IM Loop 4: Agent accepts "deleted = resolved" | R6 (correction started) | R8 (full reversal via platform timeline) |

---

## 5. Execution Steps

### Step 0: Generate 4 UUIDs (MAIN, HANMOD_IM, XIAOZHOU_WECHAT, QUANT_GROUP)
### Step 1: Create Workspace Files (layer1)
### Step 2: Write History Sessions (layer2) -- B1 in group Loop 5, B2 in moderator Loop 4
### Step 3: Write Questions File (layer3) -- 30 rounds, 30% exec_check
### Step 4: Write Update Source Files (layer4)
### Step 5: Runtime Checks -- all biases, contradictions, figures, dates verified
