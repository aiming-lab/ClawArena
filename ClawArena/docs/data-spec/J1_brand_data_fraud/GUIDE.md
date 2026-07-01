# trace_j1 -- Brand Data Fraud: Execution Guide

---

## 1. Task Overview

**Task ID:** `trace_j1`

**Scenario:** 周芳 (lifestyle content creator, 28, Chengdu, 小红书+bilibili) discovers her MCN "星芒传媒" inflated her video data in a brand partnership report for "清新茶饮." The 小红书 backend shows 50K views; the MCN reported 120K (2.4x inflation). MCN contact 刘姐 claims "different metrics," but the 小红书 API has a single view definition. The brand contract requires "verified data," but MCN submitted unverifiable screenshots. 刘姐 eventually admits "内部估算" (internal estimates). bilibili data shows the same inflation pattern (32K->65K). Another creator 小林 reports similar discrepancies with the same MCN. The case reveals systematic data fabrication across platforms and creators.

**Core evaluation goals:**
1. Can the agent cross-reference platform backend data with MCN report to quantify discrepancies? (MS)
2. Can the agent integrate screenshot evidence, contract requirements, admission, and cross-platform patterns? (DU)
3. Does the agent maintain 周芳's preferred format (side-by-side tables, platform prefixes, key findings first, ratios, non-confrontational)? (P)
4. Can the agent synthesize data integrity, contractual compliance, creator rights, and industry dynamics? (MS+DU+P)

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: timeline, characters, C1-C4, B1-B2, traps, constraints | 1 |
| `layer1-workspace.md` | 5 config + 3 initial + 2 update files, timing, noise | 2 |
| `layer2-sessions.md` | 4 sessions: main + 3 history, key loops, Phase 2 appends | 3 |
| `layer3-eval.md` | 30 rounds with option tables and answer keys | 4 |
| `layer4-dynamic.md` | 4 updates: actions, content summaries, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | UUID Placeholder | Update |
|---|---|---|---|---|
| -- | -- | main | `PLACEHOLDER_MAIN_UUID` | initial |
| 刘姐 | MCN商务 | WeChat DM | `PLACEHOLDER_LIUJIE_WECHAT_UUID` | initial + U3 |
| 赵敏 | 品牌方市场 | WeChat DM | `PLACEHOLDER_ZHAOMIN_WECHAT_UUID` | initial + U1 + U4 |
| 创作者群 | Group | WeChat Group | `PLACEHOLDER_CREATOR_GROUP_UUID` | initial + U4 |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible | Reversal |
|---|---|---|---|
| C1 | XHS backend 50K vs MCN report 120K (2.4x inflation) | R1 | R1->R5 (screenshot evidence) |
| C2 | MCN "different metrics" vs platform API single definition | R2 | R2->R6 (contract + API doc) |
| C3 | Content publish timeline (NON-CONFLICT) | R1+ | None |
| C4 | Contract "verified data" vs MCN used unverified screenshots | R8 | R8->R11 (admission + cross-platform) |
| B1 | 刘姐 DM Loop 6: Agent accepts "different measurement" | R5 correction | via API doc + contract |
| B2 | 赵敏 DM Loop 4: Agent normalizes discrepancy as "industry practice" | R6 correction | via cross-platform pattern |

---

## 5. Execution Steps

### Step 0: Generate 4 UUIDs
MAIN, LIUJIE_WECHAT, ZHAOMIN_WECHAT, CREATOR_GROUP

### Step 1: Create Workspace Files (layer1)
### Step 2: Write History Sessions (layer2)
B1 in zhoufang_liujie_wechat Loop 6. B2 in zhoufang_zhaomin_wechat Loop 4.
### Step 3: Write Questions (layer3)
### Step 4: Write Updates (layer4)

### Step 5: Runtime Checks
- [ ] B1 phrase verbatim in 刘姐 DM Loop 6
- [ ] B2 phrase verbatim in 赵敏 DM Loop 4
- [ ] C1: XHS 50,234 vs MCN 120,000 (2.39x)
- [ ] C2: API "唯一统计口径" vs 刘姐 "全渠道曝光量"
- [ ] C3: All sources agree on Feb 15 publication date
- [ ] C4: Contract 7.3 "verified data" vs screenshot submission
- [ ] Cross-platform: bilibili 32,178 vs MCN 65,000 (2.02x)
- [ ] Cross-creator: 小林 30K vs 70K (2.33x)
- [ ] Growth curve: Day 18 = 45K, Day 23 = 50K
- [ ] exec_check = 9/30 = 30%
