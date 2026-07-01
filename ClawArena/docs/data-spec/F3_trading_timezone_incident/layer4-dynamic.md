# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver server diagnostic (code-level confirmation) + 小周's candid admission + 客服小刘 full report -- triggers C1 reversal (environmental hypothesis eliminated) and C2 partial reversal (review scope defense weakened) | Yes: 小周 DM Phase 2 append, 客服小刘 ticket Phase 2 append | Yes: server-diagnostic-report.md | R1->R5 (C1: CI false confidence exposed), R2->R6 (C2: review quality reassessed) |
| U2 | Before R8 | Deliver 张审核's formal investigation notice with "first offense" claim -- triggers C4 partial (first offense vs Dec warning) | Yes: 张审核 email Phase 2 append | No (compliance-notice.md already has Dec entry; formal notice added to session) | R8 seed (C4: "first offense" challenge possible from existing Dec entry in workspace) |
| U3 | Before R11 | Deliver enhanced trade execution log with near-miss analysis -- triggers C4 full reversal (pattern evidence amplifies compliance history understatement) | No | Yes: trade-execution-log.md replaced with enhanced version | R8->R11 (C4: near-miss pattern makes "first offense" framing untenable) |
| U4 | Before R21 | Deliver 小周's institutional DST case + standard timezone fix -- provides industry context and resolution tools | Yes: #策略群 Phase 2 append | Yes: xiaozhou-timezone-fix.md | No new cross-round reversal; enables comprehensive R21-R30 assessment |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Delivers 客服小刘's server diagnostic confirming code-level issue (eliminates environmental hypothesis), 小周's candid admission about the timezone knowledge gap, and 客服小刘's full ticket response. This triggers C1 reversal (B1 "environmental difference" refuted) and begins C2 reassessment (B2 "scoped review" weakened by 小周's admission).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "server-diagnostic-report.md",
    "source": "updates/server-diagnostic-report.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_KEFU_TICKET_UUID.jsonl",
    "source": "updates/PLACEHOLDER_KEFU_TICKET_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl"
  }
]
```

### Update 2 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Appends 张审核's formal investigation notice (with "first offense" claim) to the email session. The compliance-notice.md already contains the Dec 20 prior warning in the initial workspace, so the agent can immediately cross-reference the "first offense" claim against the existing archive. This triggers C4 partial.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Replaces trade-execution-log.md with an enhanced version containing the near-miss trade analysis (Mar 9-15 pattern). This amplifies the C4 reversal: the "first offense" framing is even more problematic when the system produced near-violations for a full week before the formal trigger.

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "trade-execution-log.md",
    "source": "updates/trade-execution-log-enhanced.md"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Appends #策略群 Phase 2 content (赵磊's root cause public disclosure, 小周's institutional DST case, 群友B's validation) and adds xiaozhou-timezone-fix.md with the standard timezone handling solution. This provides industry context and resolution tools for comprehensive R21-R30 assessment.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_STRATEGY_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_STRATEGY_GROUP_UUID.jsonl"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "xiaozhou-timezone-fix.md",
    "source": "updates/xiaozhou-timezone-fix.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/server-diagnostic-report.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (eliminates environmental hypothesis)
**Content key points:**
- Title: "云服务工单回复 -- 服务器时区诊断 (工单 #TK-20260317-4521)"
- OS timezone: Asia/Shanghai (UTC+8) confirmed
- NTP sync: Active, drift < 50ms
- System clock: Verified within 100ms
- Conclusion: Code-level issue, not system-level
- Eliminates B1 "environmental difference" hypothesis

**Length estimate:** ~300 words, ~450 tokens

---

### updates/PLACEHOLDER_KEFU_TICKET_UUID.jsonl (Update 1)

**File type:** session append (continues 客服小刘 ticket session)
**Associated contradictions:** C1 (independent confirmation of code-level issue)
**Content key points:**
- Loops 7-8 of 客服小刘's ticket
- Loop 7: Full diagnostic report delivery (mirrors server-diagnostic-report.md)
- Loop 8: 赵磊 acknowledges and closes ticket

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl (Update 1)

**File type:** session append (continues 小周 WeChat DM session)
**Associated contradictions:** C2 (candid admission weakens scoped review defense)
**Content key points:**
- Loops 15-18 of 小周's DM
- Loop 15: 小周's candid admission: "我以为 +8 就是 CST，没想到 DST 的事"
- Loop 16: 小周 offers to write fix PR with `zoneinfo`
- Loop 17: 赵磊 reports near-miss trades from execution log
- Loop 18: 小周 mentions his institution's DST issue + reflection on review quality

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl (Update 2)

**File type:** session append (continues 张审核 email session)
**Associated contradictions:** C4 ("first offense" claim)
**Content key points:**
- Loops 9-12 of 张审核's email
- Loop 9: Formal investigation notice with "首次出现交易时段违规"
- Loop 10: 赵磊 challenges with Dec 20 email evidence
- Loop 11: 张审核 distinguishes formal vs informal compliance records
- Loop 12: 赵磊 submits remediation plan

**Length estimate:** ~600 words, ~900 tokens

---

### updates/trade-execution-log-enhanced.md (Update 3)

**File type:** workspace replace (enhances trade-execution-log.md)
**Associated contradictions:** C4 (near-miss pattern amplifies compliance concern)
**Content key points:**
- Enhanced version of trade-execution-log.md with detailed analysis
- Pre-DST baseline (Mar 1-8): no offset
- Post-DST pattern (Mar 9-16): 4 trades shifted, 2 near-misses
- Explicit boundary analysis: Mar 10 at 11:29:47 (13s from violation), Mar 11 at 11:29:53 (7s from violation)
- Mar 16 at 11:30:05 (5s past boundary = violation)

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_STRATEGY_GROUP_UUID.jsonl (Update 4)

**File type:** session append (continues #策略群 session)
**Associated contradictions:** B1 (public correction), industry context
**Content key points:**
- Loops 15-18 of #策略群 group chat
- Loop 15: 赵磊 public root cause disclosure (corrects B1 "environmental difference")
- Loop 16: 小周 shares institutional DST case
- Loop 17: 群友B validates the anti-pattern assessment
- Loop 18: 赵磊 shares remediation completion

**Length estimate:** ~600 words, ~900 tokens

---

### updates/xiaozhou-timezone-fix.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C2 (小周 knows correct approach)
**Content key points:**
- Title: "小周分享 -- 标准时区处理方案 (2026-03-23)"
- Correct code: `datetime.now(tz=ZoneInfo('Asia/Shanghai'))`
- Anti-pattern explanation: why `utcnow() + timedelta(hours=8)` fails
- Institutional case reference
- Shows 小周 has the knowledge for correct implementation

**Length estimate:** ~350 words, ~525 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_KEFU_TICKET_UUID and PLACEHOLDER_XIAOZHOU_WECHAT_UUID
  - Update 2 appends to PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID
  - Update 3 replaces trade-execution-log.md (workspace, not session)
  - Update 4 appends to PLACEHOLDER_STRATEGY_GROUP_UUID
- [x] All workspace files have content descriptions in layer1
- [x] Updates support intended reversals
  - U1 -> C1 reversal (R1->R5): server diagnostic eliminates environmental hypothesis
  - U1 -> C2 partial reversal (R2->R6): 小周's admission weakens scoped review defense
  - U2 -> C4 partial (R8 seed): "first offense" claim vs Dec warning
  - U3 -> C4 full reversal (R8->R11): near-miss pattern amplifies compliance concern
  - U4 -> comprehensive context for R21-R30
- [x] Technical figures consistent
  - UTC 03:30 = CST 11:30 (during DST): consistent across production log, trade log
  - PR #447 merged 2026-03-10: consistent across git-pr-447-diff.md, ci-build-report.md
  - Build #891: consistent
  - silence_rule_007 created 2025-12-15: consistent across alert-rules-config.md, production-error-log.md
  - Prior warning 2025-12-20: consistent in compliance-notice.md
  - Near-miss times: Mar 10 11:29:47, Mar 11 11:29:53: consistent

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "server-diagnostic-report.md", "source": "updates/server-diagnostic-report.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_KEFU_TICKET_UUID.jsonl", "source": "updates/PLACEHOLDER_KEFU_TICKET_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl" }
]
```

### R8 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "trade-execution-log.md", "source": "updates/trade-execution-log-enhanced.md" }
]
```

### R21 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_STRATEGY_GROUP_UUID.jsonl", "source": "updates/PLACEHOLDER_STRATEGY_GROUP_UUID.jsonl" },
  { "type": "workspace", "action": "new", "path": "xiaozhou-timezone-fix.md", "source": "updates/xiaozhou-timezone-fix.md" }
]
```
