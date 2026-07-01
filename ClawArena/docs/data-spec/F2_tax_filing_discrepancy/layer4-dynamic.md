# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver auto-transfer log — resolves C1 (fund redemption, not income) and seeds C2 reversal (both experts wrong) | Yes: 客服小张 email Phase 2 append | Yes: auto-transfer-log.md | R2->R5 (C1: gap explained by fund redemption); R3->R7 seed (C2: auto-transfer refutes both diagnoses) |
| U2 | Before R8 | Deliver 张会计's "can extend" claim — seeds C4 (deadline already passed) | Yes: 张会计 email Phase 2 append (Loops 11-12) | No | R8->R11 seed (C4: "can extend" vs deadline passed) |
| U3 | Before R7 | Deliver both experts' revisions after seeing auto-transfer log — completes C2 reversal | Yes: 张会计 email Phase 2 append (Loops 13-14) + 张审核 email Phase 2 append (Loops 11-12) | Yes: accountant-revision-email.md, reviewer-revision-email.md | R3->R7 (C2: both diagnoses refuted; both experts revise) |
| U4 | Before R11 | Deliver tax bureau late-filing notice — completes C4 reversal (penalties confirmed, no extension possible) | No | Yes: tax-bureau-notice.md | R8->R11 (C4: "can extend" definitively refuted; daily penalties confirmed) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces the auto-transfer log from 招行, definitively explaining the ¥47,200 as a money market fund auto-redemption. Also appends 客服小张's delivery email to the bank email session. This resolves C1 and begins undermining both expert diagnoses (C2).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "auto-transfer-log.md",
    "source": "updates/auto-transfer-log.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHAOHANG_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHAOHANG_EMAIL_UUID.jsonl"
  }
]
```

### Update 2 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Appends 张会计's "可以延期" claim to her email session. This seeds C4 — the claim directly conflicts with the calendar showing the deadline has passed and the Oct 16 reminder email.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID_u2.jsonl"
  }
]
```

### Update 3 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Appends both experts' revised assessments after seeing the auto-transfer log. 张会计 admits the "unreported income" diagnosis was wrong but gives questionable "conservative filing" advice. 张审核 admits "import error" was wrong but defends it as "reasonable in absence of data." Both workspace email exports are added. This completes C2 reversal.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID_u3.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "accountant-revision-email.md",
    "source": "updates/accountant-revision-email.md"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "reviewer-revision-email.md",
    "source": "updates/reviewer-revision-email.md"
  }
]
```

### Update 4 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces the tax bureau late-filing notice with daily ¥200 penalties, confirming that the deadline has passed and post-deadline extensions are not accepted. This definitively refutes 张会计's "可以延期" claim (C4 full reversal).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "tax-bureau-notice.md",
    "source": "updates/tax-bureau-notice.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/auto-transfer-log.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (resolution), C2 (refutes both diagnoses), C3 (non-conflict source)
**Content key points:**
- Rule AT-2026-0410-001 set up by 赵磊 on 2026-04-10
- Type: 货币基金余额超限自动赎回
- Trigger: fund balance > ¥50,000 → redeem to ¥2,800
- Execution: 2026-07-15, amount ¥47,200, to savings account xxxx-7890
- Definitively shows the ¥47,200 is principal return, not income

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_ZHAOHANG_EMAIL_UUID.jsonl (Update 1)

**File type:** session append (continues 客服小张 email session)
**Associated contradictions:** C1 (resolution delivery)
**Content key points:**
- Loops 7-8 of 客服小张 email
- Loop 7: 客服小张 sends the auto-transfer record with key details
- Loop 8: 赵磊 confirms "I set it up in April, completely forgot"

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID_u2.jsonl (Update 2)

**File type:** session append (continues 张会计 email session — Loops 11-12)
**Associated contradictions:** C4 (seeds "can extend" claim)
**Content key points:**
- Loop 11: 张会计 claims "可以申请延期，税务局一般会批的"
- Loop 12: 赵磊 challenges with deadline date, 张会计 reassures with "弹性期" claim

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID_u3.jsonl (Update 3)

**File type:** session append (continues 张会计 email session — Loops 13-14)
**Associated contradictions:** C2 (accountant revision)
**Content key points:**
- Loop 13: 张会计 admits "漏报收入" was wrong after seeing auto-transfer log, but suggests "conservative filing"
- Loop 14: 赵磊 pushes back, 张会计 concedes to correct filing

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl (Update 3)

**File type:** session append (continues 张审核 email session — Loops 11-12)
**Associated contradictions:** C2 (reviewer revision), C4 (correct deadline assessment)
**Content key points:**
- Loop 11: 张审核 admits "import error" diagnosis was wrong, defends it as "reasonable hypothesis"
- Loop 12: 张审核 correctly notes Q3 deadline has passed

**Length estimate:** ~300 words, ~450 tokens

---

### updates/accountant-revision-email.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C2 (accountant revision)
**Content key points:**
- 张会计 email acknowledging the ¥47,200 is fund redemption, not income
- "Conservative filing" suggestion noted

**Length estimate:** ~300 words, ~450 tokens

---

### updates/reviewer-revision-email.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C2 (reviewer revision)
**Content key points:**
- 张审核 email acknowledging "import error" was incorrect
- Defensive justification noted

**Length estimate:** ~250 words, ~375 tokens

---

### updates/tax-bureau-notice.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (definitive refutation of "can extend")
**Content key points:**
- Official notice: Q3 filing overdue by 10 days
- Daily penalty: ¥200 (total ¥2,000 as of notice date)
- "逾期申报不接受事后延期申请"
- Deadline for compliance: 5 days from notice receipt

**Length estimate:** ~300 words, ~450 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_ZHAOHANG_EMAIL_UUID (客服小张 email)
  - Update 2 appends to PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID (张会计 email — Loops 11-12)
  - Update 3 appends to PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID (张会计 email — Loops 13-14) + PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID (张审核 email)
  - Update 4: workspace only
- [x] All workspace files have content descriptions in layer1
- [x] Updates support intended reversals
  - U1 -> C1 resolution (R2->R5): auto-transfer log explains the ¥47,200
  - U3 -> C2 full reversal (R3->R7): both experts revise; auto-transfer proves both wrong
  - U2 -> C4 seed (R8): 张会计's "can extend" claim introduced
  - U4 -> C4 full reversal (R8->R11): tax bureau notice confirms penalties and no extension
- [x] Financial figures are internally consistent
  - Bank Q3 total: ¥429,700 across all sources
  - Tracker Q3 total: ¥382,500 across all sources
  - Gap: ¥47,200 = fund redemption amount across all sources
  - Fund balance trigger: ¥50,000; remaining after redemption: ¥2,800
  - Correct tax: ¥42,075; incorrect tax (张会计): ¥48,267; overpayment: ¥6,192
  - Late penalty: ¥200/day; 10 days = ¥2,000

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "auto-transfer-log.md", "source": "updates/auto-transfer-log.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHAOHANG_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHAOHANG_EMAIL_UUID.jsonl" }
]
```

### R7 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID_u3.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID.jsonl" },
  { "type": "workspace", "action": "new", "path": "accountant-revision-email.md", "source": "updates/accountant-revision-email.md" },
  { "type": "workspace", "action": "new", "path": "reviewer-revision-email.md", "source": "updates/reviewer-revision-email.md" }
]
```

### R8 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID_u2.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "tax-bureau-notice.md", "source": "updates/tax-bureau-notice.md" }
]
```
