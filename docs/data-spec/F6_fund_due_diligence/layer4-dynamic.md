# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver 赵磊's independent Sharpe calculation (1.3) and reveal spreadsheet formula omission -- triggers C1 full reversal (three-way Sharpe: 2.1/1.8/1.3) and C2 reversal (methodology ~0.1 vs omission ~0.8) | Yes: 小周 IM Phase 2 append (confrontation + defense) | Yes: sharpe-independent-calculation.md | R2->R5 (C1: three-way Sharpe established); R3->R6 (C2: methodology explanation refuted) |
| U2 | Before R7 | Deliver 张秘书's "still evaluating" email -- triggers C4 reversal (verbal commitment vs official position) | Yes: 刘总 Email Phase 2 append (张秘书 email + 刘总 follow-up) | Yes: email-thread-liuzong.md (replaced with appended version) | R4->R8 (C4: verbal enthusiasm vs institutional commitment) |
| U3 | Before R11 | Deliver 陈经理's independent brokerage Sharpe confirmation (1.3) -- provides dual independent confirmation of actual performance | Yes: 陈经理 IM Phase 2 append (brokerage data + compliance context) | Yes: broker-performance-confirmation.md | No new reversal; extends C1 with independent third-party confirmation |
| U4 | Before R21 | Deliver meeting timeline cross-verification -- confirms C3 non-conflict definitively | No new session append | Yes: meeting-timeline-verification.md | No reversal; confirms C3 non-conflict with four-source alignment |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces sharpe-independent-calculation.md showing 赵磊's own Python calculation: Sharpe 1.3 with all months, 2.1 excluding July-September 2025. Quantifies methodology vs omission: ~0.1 vs ~0.8. Appends Phase 2 to 小周 IM (confrontation about formula, 小周 defends as "industry practice"). Triggers C1 full reversal and C2 reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "sharpe-independent-calculation.md",
    "source": "updates/sharpe-independent-calculation.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_XIAOZHOU_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_XIAOZHOU_IM_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Replaces email-thread-liuzong.md with version including 张秘书's "still evaluating, no commitments" email. Appends Phase 2 to 刘总 email (张秘书 email + 刘总's nuanced follow-up revealing multiple candidates). Triggers C4 reversal.

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "email-thread-liuzong.md",
    "source": "updates/email-thread-liuzong.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces broker-performance-confirmation.md with 陈经理's independent brokerage calculation (Sharpe 1.3, annualized 18%, max DD 14%). Appends Phase 2 to 陈经理 IM (confirmation, compliance implications, offer of formal performance letter). Provides dual independent confirmation of actual performance.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "broker-performance-confirmation.md",
    "source": "updates/broker-performance-confirmation.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHENJINGLI_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHENJINGLI_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces meeting-timeline-verification.md confirming C3 non-conflict: calendar, CRM, meeting notes, and email timestamps all agree on 2026-03-19 meeting date/time/attendees. Enables comprehensive R21-R30 assessment with all evidence available.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "meeting-timeline-verification.md",
    "source": "updates/meeting-timeline-verification.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/sharpe-independent-calculation.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), C2 (quantification)
**Content key points:**
- Title: "Sharpe 独立计算 -- 赵磊自算 | 2026-03-23"
- Python calculation using complete 24-month return series
- Sharpe (all months): **1.3**
- Sharpe (excluding July-September 2025): **2.1**
- Methodology sensitivity range (varying risk-free rate): 1.2--1.4
- Decomposition: methodology contributes ~0.1; data omission contributes ~0.8
- "Methodology choice explains ~12% of the gap. Data omission explains ~88%."

**Length estimate:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_XIAOZHOU_IM_UUID.jsonl (Update 1)

**File type:** session append (continues xiaozhou_im session)
**Associated contradictions:** C2 (defense/confrontation), B1 (reversal trigger)
**Content key points:**
- Loops 11-14 of 小周 IM
- Loop 11: 赵磊 confronts about formula; 小周 defends as "anomalous market conditions" exclusion
- Loop 12: 小周 claims "industry practice" for excluding extreme periods
- Loop 13: Specific negative returns discussed (-4.2%, -3.1%, -2.8%)
- Loop 14: 小周 suggests "supplementary note" rather than full correction
- Agent must explicitly revise B1 -- methodology explanation was insufficient; omission is the primary driver

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/email-thread-liuzong.md (Update 2)

**File type:** workspace replace (adds 张秘书 email to existing thread)
**Associated contradictions:** C4 (full reversal)
**Content key points:**
- Original emails preserved
- Appended: 张秘书 → 赵磊 (2026-03-25): "刘总目前仍在评估多个策略标的，尚未做出任何承诺。"
- C4 direct contradiction: verbal "let's move forward" vs official "still evaluating, no commitments"

**Length estimate:** ~600 words (full file), ~900 tokens

---

### updates/PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl (Update 2)

**File type:** session append (continues liuzong_email session)
**Associated contradictions:** C4 (full evidence), B2 (reversal trigger)
**Content key points:**
- Loops 9-11 of 刘总 Email
- Loop 9: 张秘书's "still evaluating" email
- Loop 10: 刘总 follows up saying "standard process language" but confirms multiple candidates
- Loop 11: 刘总 discusses evaluation criteria, again uses Sharpe 1.8
- Agent must explicitly revise B2 -- verbal commitment was social gesture, not institutional commitment

**Length estimate:** ~600 words, ~900 tokens

---

### updates/broker-performance-confirmation.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C1 (independent third-party confirmation)
**Content key points:**
- Title: "券商业绩确认 -- 陈经理核算 | 2026-03-26"
- Brokerage-calculated Sharpe: **1.3** (matches 赵磊's independent calculation)
- Annualized return: **~18%**
- Max drawdown: **~14%**
- 陈经理 note: "DD package shows significantly higher metrics"
- Dual independent confirmation (赵磊 calc + brokerage records)

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_CHENJINGLI_IM_UUID.jsonl (Update 3)

**File type:** session append (continues chenjingli_im session)
**Associated contradictions:** C1 (triple confirmation), compliance implications
**Content key points:**
- Loops 9-12 of 陈经理 IM
- Loop 9: 陈经理 delivers brokerage Sharpe calculation (1.3)
- Loop 10: Compliance implications -- brokerage data accuracy is institutional responsibility
- Loop 11: Offers formal performance letter as third-party verification
- Loop 12: Balanced perspective -- Sharpe 1.3 is respectable for CTA, no need to inflate

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/meeting-timeline-verification.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C3 (definitive non-conflict confirmation)
**Content key points:**
- Title: "会议时间线交叉验证 -- 多源确认 | 2026-03-27"
- Four sources aligned: calendar, CRM, meeting notes, email timestamps
- All confirm 2026-03-19 14:00-16:00, attendees 赵磊/刘总/小周
- C3 definitively non-conflict

**Length estimate:** ~300 words, ~450 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_XIAOZHOU_IM_UUID (xiaozhou_im session)
  - Update 2 appends to PLACEHOLDER_LIUZONG_EMAIL_UUID (liuzong_email session)
  - Update 3 appends to PLACEHOLDER_CHENJINGLI_IM_UUID (chenjingli_im session)
- [x] All workspace files have content descriptions in layer1
- [x] Updates support intended reversals
  - U1 -> C1 full reversal (R2->R5): three-way Sharpe (2.1/1.8/1.3)
  - U1 -> C2 reversal (R3->R6): methodology ~0.1 vs omission ~0.8
  - U2 -> C4 reversal (R4->R8): verbal commitment vs "still evaluating"
  - U3 -> C1 triple confirmation: brokerage independently confirms 1.3
  - U4 -> C3 non-conflict: four-source timeline alignment
- [x] Session filenames use consistent PLACEHOLDER format
- [x] Factual figures consistent
  - DD Sharpe: 2.1; 刘总 recall: 1.8; Actual: 1.3
  - Omitted months: July-September 2025; Returns: -4.2%, -3.1%, -2.8%
  - Annualized return: actual ~18% vs DD 31%
  - Max drawdown: actual ~14% vs DD 8%
  - Meeting: 2026-03-19 14:00-16:00
  - Methodology contribution: ~0.1; Omission contribution: ~0.8

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "sharpe-independent-calculation.md", "source": "updates/sharpe-independent-calculation.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_XIAOZHOU_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_XIAOZHOU_IM_UUID.jsonl" }
]
```

### R7 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "email-thread-liuzong.md", "source": "updates/email-thread-liuzong.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_LIUZONG_EMAIL_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "broker-performance-confirmation.md", "source": "updates/broker-performance-confirmation.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENJINGLI_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENJINGLI_IM_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "meeting-timeline-verification.md", "source": "updates/meeting-timeline-verification.md" }
]
```
