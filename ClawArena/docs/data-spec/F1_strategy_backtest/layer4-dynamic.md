# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver independent backtest replication + due-diligence email context -- triggers C1 partial reversal (look-ahead bias confirmed) and seeds C4 (刘总 received inflated figure) | Yes: #量化策略群 Phase 2 append | Yes: due-diligence-cover-email.md, zhaolei-independent-backtest.md | R2->R5 (C1: 小周's "pre-planned" narrative contradicted by independent replication + timeline); R3->R6 seed (C2: three-Sharpe picture established) |
| U2 | Before R6 | Deliver 陈经理's compliance flag -- triggers C4 partial reversal and adds regulatory dimension | Yes: 陈经理 email Phase 2 append | Yes: compliance-flag-email.md | R3->R6 (C2/C4: compliance formally flags Sharpe discrepancy; regulatory dimension added) |
| U3 | Before R11 | Deliver CI build comparison + 小周 Phase 2 responses -- triggers C1 full reversal and B2 definitive correction | Yes: 小周 WeChat DM Phase 2 append | Yes: ci-build-comparison.md | R2->R11 (C1: CI build comparison definitively proves post-hoc modification; dual-source with independent backtest); R8->R11 (C4: complete evidence chain for due-diligence misrepresentation) |
| U4 | Before R21 | Deliver 刘总's direct question + consulting fee revelation -- forces resolution and reveals financial incentive | Yes: 刘总 email Phase 2 append | Yes: liuzong-direct-message.md | No new cross-round reversal; reveals 小周's financial incentive and enables comprehensive R21-R30 assessment |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces 赵磊's independent backtest replication confirming the three-Sharpe picture (1.7 original, 2.1 refit, 1.3 live) and identifying look-ahead bias. Also introduces the due-diligence cover email showing 小周 sent the Sharpe 2.1 package to 刘总 on Feb 21 without 赵磊's knowledge. The #量化策略群 Phase 2 append delivers 赵磊's public correction and 群友B's independent corroboration. This update triggers C1 partial reversal and seeds C4.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "due-diligence-cover-email.md",
    "source": "updates/due-diligence-cover-email.md"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "zhaolei-independent-backtest.md",
    "source": "updates/zhaolei-independent-backtest.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_QUANT_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_QUANT_GROUP_UUID.jsonl"
  }
]
```

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Appends 陈经理's compliance flag email to the 陈经理 email session and adds the compliance-flag-email.md to the workspace. 陈经理's compliance department has independently flagged the discrepancy between the live Sharpe 1.3 filing and the circulating Sharpe 2.1 due-diligence material. This introduces the regulatory dimension and provides an objective external source confirming the Sharpe discrepancy is not just an academic debate. This update triggers C4 partial reversal.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHENJINGLI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHENJINGLI_EMAIL_UUID.jsonl"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "compliance-flag-email.md",
    "source": "updates/compliance-flag-email.md"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces the CI build comparison document (side-by-side Build #847 vs #862) providing the definitive evidence that the parameter change was post-hoc. Also appends 小周's Phase 2 responses to the WeChat DM session, showing his defensive posture and narrative evolution (from "pre-planned" to "methodology disagreement" to partial admission). This update triggers C1 full reversal and definitively corrects B2.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ci-build-comparison.md",
    "source": "updates/ci-build-comparison.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces 刘总's direct question about the Sharpe 2.1 figure ("Is that consistent with your understanding?") and the revelation of 小周's undisclosed consulting fee arrangement. Also appends 刘总's Phase 2 email DM session showing 赵磊's honest correction and 刘总's professional response. Introduces liuzong-direct-message.md to the workspace. This update completes the evidence picture for comprehensive assessment rounds R21-R30 and reveals 小周's financial incentive.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "liuzong-direct-message.md",
    "source": "updates/liuzong-direct-message.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/due-diligence-cover-email.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C4 (context -- shows 刘总 received Sharpe 2.1 from 小周)
**Content key points:**
- Title: "邮件导出 -- 小周 -> 刘总: Strategy V3 尽调材料 (2026-02-21)"
- Simulates email export showing 小周 sent the Sharpe 2.1 backtest report to 刘总
- Date: 2026-02-21 (one day after CI Build #862 produced Sharpe 2.1)
- From: 小周; To: 刘总; CC: none (赵磊 NOT CC'd)
- Body excerpt: "刘总，附件是 Strategy V3 最新的回测报告，Sharpe 2.1，年化 31.2%。"
- Critical: 赵磊 was not included in this communication
- Shows the manufactured figure was sent to investor without strategy owner's knowledge

**Length estimate:** ~300 words, ~450 tokens

---

### updates/zhaolei-independent-backtest.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (look-ahead bias confirmation), C2 (three-Sharpe picture)
**Content key points:**
- Title: "赵磊独立回测验证 -- Strategy V3 参数对比 (2026-02-25)"
- Original parameters (120d/2.5%): Sharpe=1.7, MaxDD=-12.3%, AnnReturn=23.4%
- Modified parameters (90d/1.8%): Sharpe=2.1, MaxDD=-8.1%, AnnReturn=31.2%
- Live performance: Sharpe=1.3, MaxDD=-15.7%, MonthlyReturn=+4.1%
- 赵磊's analysis note: "Look-ahead bias 特征明显"
- Confirms the three-Sharpe picture: 1.7 (genuine), 2.1 (manufactured), 1.3 (real)
- Establishes that Sharpe improvement is from in-sample overfitting, not genuine alpha

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_QUANT_GROUP_UUID.jsonl (Update 1)

**File type:** session append (continues #量化策略群 session)
**Associated contradictions:** C1 (public correction), C2 (three-Sharpe presentation), B1 (reversal)
**Content key points:**
- Loops 15-18 of #量化策略群 group chat
- Loop 15: 赵磊 presents independent backtest results publicly, identifies look-ahead bias
- Loop 16: 小周 responds with "execution layer slippage" defense (deflects from timeline issue)
- Loop 17: 群友B independently validates 赵磊's overfitting concern
- Loop 18: 赵磊 announces continued CI build log investigation
- Agent must explicitly correct B1 bias phrase by acknowledging the independent backtest shows look-ahead bias, not "standard optimization"
- Maintains group chat voice (multiple participants, technical discussion)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_CHENJINGLI_EMAIL_UUID.jsonl (Update 2)

**File type:** session append (continues 陈经理 email session)
**Associated contradictions:** C4 (compliance flag -- external trigger)
**Content key points:**
- Loops 9-12 of 陈经理's email DM
- Loop 9: 陈经理 formally flags Sharpe discrepancy (1.3 compliance vs 2.1 due-diligence)
- Loop 10: 陈经理 references CSRC disclosure regulations, adds regulatory dimension
- Loop 11: 赵磊 requests formal compliance template
- Loop 12: 陈经理 provides compliance response template (three required elements)
- Maintains 陈经理's institutional, non-political communication style
- Introduces regulatory dimension that elevates the issue from methodology debate to compliance risk

**Length estimate:** ~600 words, ~900 tokens

---

### updates/compliance-flag-email.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C4 (external compliance trigger)
**Content key points:**
- Title: "邮件导出 -- 陈经理 -> 赵磊: 合规核查通知 (2026-03-02)"
- 陈经理 flags discrepancy: live Sharpe 1.3 vs circulating document Sharpe 2.1
- Source of the circulating document: forwarded by 刘总's assistant
- References CSRC disclosure regulations
- Requests formal written explanation

**Length estimate:** ~300 words, ~450 tokens

---

### updates/ci-build-comparison.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C1 (definitive evidence), B2 (definitive correction)
**Content key points:**
- Title: "CI Build Comparison -- Build #847 vs Build #862 (Strategy V3)"
- Side-by-side comparison table:
  - Build #847: Feb 14, 120d lookback, 2.5% SL, Sharpe 1.7, triggered by 赵磊
  - Build #862: Feb 20, 90d lookback, 1.8% SL, Sharpe 2.1, triggered by 小周
- 6-day gap with live trading starting on Feb 16 (day 2)
- Build #862 triggered solely by 小周's commit (no review by 赵磊)
- Definitive evidence of post-hoc parameter modification
- Makes the B2 "standard calibration" assessment definitively wrong

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl (Update 3)

**File type:** session append (continues 赵磊-小周 WeChat DM session)
**Associated contradictions:** C1 (defensive responses), C2 (narrative evolution), C4 (partial acknowledgment)
**Content key points:**
- Loops 17-20 of 小周's WeChat DM with 赵磊
- Loop 17: 赵磊 confronts 小周 with CI build timeline. 小周 responds: "build 的时间 ≠ 决策的时间" -- cannot produce pre-launch documentation
- Loop 18: 小周 shifts to "methodology disagreement" framing, abandons "pre-planned" claim
- Loop 19: 小周 defends due-diligence materials as "industry practice"
- Loop 20: 小周 partially admits: "commit 时间确实不好看...给刘总的材料我确实应该注明参数更新时间" -- first concession, still does not admit look-ahead bias
- Maintains 小周's voice: technically articulate but increasingly defensive, specific but evasive on accountability

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/liuzong-direct-message.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (forcing function), new information (consulting fee)
**Content key points:**
- Title: "微信导出 -- 刘总 -> 赵磊: 策略确认 (2026-03-08)"
- 刘总 asks: "小周跟我说 V3 的 Sharpe 2.1 是最新优化后的结果...这个数据和你的理解一致吗?"
- 刘总 reveals: "小周说他在这个项目上以顾问身份参与，咨询费挂在投资通过后结算。这个安排你清楚吗?"
- Includes 刘总's assistant's message context (forwarding backtest report to compliance)
- Forces 赵磊 to confirm or deny the Sharpe figure
- Reveals 小周's undisclosed financial incentive

**Length estimate:** ~350 words, ~525 tokens

---

### updates/PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl (Update 4)

**File type:** session append (continues 刘总 email DM session)
**Associated contradictions:** C4 (resolution), consulting fee (new information)
**Content key points:**
- Loops 11-14 of 刘总's email DM with 赵磊
- Loop 11: 刘总's direct Sharpe question (C4 forcing function)
- Loop 12: 刘总 reveals consulting fee arrangement (new information)
- Loop 13: 赵磊 corrects the record honestly (original Sharpe 1.7, live 1.3, 2.1 from post-hoc refit)
- Loop 14: 刘总 responds professionally: pauses investment evaluation, will verify with brokerage
- Maintains 刘总's professional, direct communication style
- Shows 赵磊 choosing honesty over relationship preservation

**Length estimate:** ~600 words, ~900 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_QUANT_GROUP_UUID (#量化策略群 session)
  - Update 2 appends to PLACEHOLDER_CHENJINGLI_EMAIL_UUID (陈经理 email session)
  - Update 3 appends to PLACEHOLDER_XIAOZHOU_WECHAT_UUID (小周 WeChat DM session)
  - Update 4 appends to PLACEHOLDER_LIUZONG_EMAIL_UUID (刘总 email session)
- [x] All workspace files have content descriptions in layer1
  - due-diligence-cover-email.md: layer1 Section 5, Update 1
  - zhaolei-independent-backtest.md: layer1 Section 5, Update 1
  - compliance-flag-email.md: layer1 Section 5, Update 2
  - ci-build-comparison.md: layer1 Section 5, Update 3
  - liuzong-direct-message.md: layer1 Section 5, Update 4
- [x] Updates support intended reversals
  - U1 -> C1 partial reversal (R2->R5): independent backtest confirms look-ahead bias
  - U2 -> C4 partial reversal (R3->R6): compliance flag confirms Sharpe discrepancy has regulatory dimension
  - U3 -> C1 full reversal (R2->R11): CI build comparison definitively proves post-hoc modification
  - U4 -> comprehensive evidence for R21-R30: consulting fee reveals financial incentive
- [x] Session filenames use consistent PLACEHOLDER format
  - PLACEHOLDER_QUANT_GROUP_UUID, PLACEHOLDER_CHENJINGLI_EMAIL_UUID, PLACEHOLDER_XIAOZHOU_WECHAT_UUID, PLACEHOLDER_LIUZONG_EMAIL_UUID
- [x] Financial/quantitative figures are internally consistent
  - Original backtest Sharpe: 1.7 (Build #847, Feb 14, 120d lookback, 2.5% SL) across all sources
  - Post-hoc refit Sharpe: 2.1 (Build #862, Feb 20, 90d lookback, 1.8% SL) across all sources
  - Live Sharpe: 1.3 (one-month actual, Feb 16 - Mar 15) across all sources
  - MaxDD original: -12.3%; MaxDD refit: -8.1%; MaxDD live: -15.7% -- consistent
  - AnnReturn original: 23.4%; AnnReturn refit: 31.2% -- consistent
  - Sharpe inflation: +0.4 (1.7 -> 2.1) = 23.5% overstatement
  - Live gap from presented figure: +0.8 (2.1 - 1.3) = 61.5% overstatement relative to actual

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "due-diligence-cover-email.md", "source": "updates/due-diligence-cover-email.md" },
  { "type": "workspace", "action": "new", "path": "zhaolei-independent-backtest.md", "source": "updates/zhaolei-independent-backtest.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_QUANT_GROUP_UUID.jsonl", "source": "updates/PLACEHOLDER_QUANT_GROUP_UUID.jsonl" }
]
```

### R6 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENJINGLI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENJINGLI_EMAIL_UUID.jsonl" },
  { "type": "workspace", "action": "new", "path": "compliance-flag-email.md", "source": "updates/compliance-flag-email.md" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "ci-build-comparison.md", "source": "updates/ci-build-comparison.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "liuzong-direct-message.md", "source": "updates/liuzong-direct-message.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl" }
]
```
