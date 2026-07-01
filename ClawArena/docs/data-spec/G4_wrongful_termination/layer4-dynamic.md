# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver Chen Hao's admission + Sun Wei's 1:1 notes -- triggers C1 partial reversal (verbal vs written distinction revealed) | Yes: Chen Hao Feishu Phase 2 append | Yes: sunwei-1on1-notes.md | R2->R5 (C1: "3 written warnings" claim shown to include 2 verbal conversations) |
| U2 | Before R7 | Deliver Sun Wei's written response + Zhang Tao's detailed account -- triggers C1 full and C2 nuanced reversal | Yes: Sun Wei Email Phase 2 append + Zhang Tao IM Phase 2 append | Yes: sunwei-written-response.md | R2->R7 (C1: Sun Wei confirms verbal=written confusion); R3->R8 (C2: PIP meetings were ambiguous) |
| U3 | Before R11 | Deliver timeline analysis revealing PIP policy violation (40 vs 60 days) | No session append | Yes: pip-timeline-analysis.md | No new cross-round reversal; extends C3 evidence and reveals process violation |
| U4 | Before R21 | Deliver legal's hedging updated assessment -- triggers C4 full reversal | Yes: Ma Li Email Phase 2 append | Yes: legal-updated-assessment.md | R6->R9 complete (C4: legal's "sufficient" shown to be based on unverified info) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Delivers Chen Hao's admission that he did not independently verify the warning count, plus Sun Wei's personal 1:1 notes showing "discussed performance concerns" language instead of "issued warning." This triggers C1 partial reversal by revealing the verbal-vs-written distinction.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "sunwei-1on1-notes.md",
    "source": "updates/sunwei-1on1-notes.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Delivers Sun Wei's formal written response confirming that 2 of 3 warnings were verbal, plus Zhang Tao's detailed account of the PIP meetings (Feb 15 = project planning, Mar 4 = termination notification). Triggers C1 full reversal and C2 nuanced reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "sunwei-written-response.md",
    "source": "updates/sunwei-written-response.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SUNWEI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SUNWEI_EMAIL_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGTAO_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGTAO_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Delivers Chen Jing's timeline reconstruction, revealing the 40-day vs 60-day PIP policy violation and the fact that the March 4 meeting was functionally a termination notification (per both Sun Wei's notes and Zhang Tao's account).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "pip-timeline-analysis.md",
    "source": "updates/pip-timeline-analysis.md"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Delivers Ma Li's hedging updated assessment acknowledging "some gaps" but not fully retracting the initial "sufficient" opinion. Completes C4 by revealing that legal's initial confidence was based on unverified information.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "legal-updated-assessment.md",
    "source": "updates/legal-updated-assessment.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MALI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MALI_EMAIL_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/sunwei-1on1-notes.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (partial reversal -- verbal vs written distinction)
**Content key points:**
- Title: "孙伟 1:1 会议笔记 -- 张涛相关 | 陈浩提供"
- Nov 20 entry: "discussed Q3 delivery delays, suggested improving time management"
- Dec 18 entry: "followed up on performance issues, told him if this continues will report to HR"
- Both entries use coaching language ("discussed," "followed up"), NOT warning language
- Feb 15 entry: "PIP Week 2 review, 2 goals progressing, 2 not"
- Mar 4 entry: "talked about termination, he didn't take it well"
- C1 key evidence: Nov 20 and Dec 18 are coaching conversations, not formal warnings
- C2 evidence: Mar 4 described as termination conversation, not PIP review

**Length estimate:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl (Update 1)

**File type:** session append
**Associated contradictions:** C1 (HRBP verification failure)
**Content key points:**
- Loops 11-14: Chen Hao provides 1:1 notes, admits verification failure, asks about implications
- Key admission: "I should have checked the email system myself"
- Chen Hao recognizes the "discussed performance" vs "issued warning" distinction
- Asks about impact on the case

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/sunwei-written-response.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal -- Sun Wei confirms verbal=written confusion)
**Content key points:**
- Title: "孙伟书面回复 -- 关于张涛解雇流程询问"
- Sun Wei confirms: 2 verbal warnings (Nov 20, Dec 18) + 1 email warning (Jan 15) = "3 warnings"
- Sun Wei considers verbal and written as equivalent
- Company policy does not treat them as equivalent
- Sun Wei defends: "verbal warnings in 1:1 are just as real"

**Length estimate:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_SUNWEI_EMAIL_UUID.jsonl (Update 2)

**File type:** session append
**Associated contradictions:** C1 (Sun Wei confirms), C2 (Sun Wei on PIP meetings)
**Content key points:**
- Loops 9-12: Sun Wei's formal response, defense of verbal warnings, admission about Mar 4 documentation gap, risk inquiry
- Key: Sun Wei explicitly categorizes 2 verbal as "warnings"
- Admits Mar 4 meeting was not documented by email

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_ZHANGTAO_IM_UUID.jsonl (Update 2)

**File type:** session append
**Associated contradictions:** C2 (nuanced PIP awareness)
**Content key points:**
- Loops 9-12: Zhang Tao's detailed account of Feb 15 meeting (project planning focus), Mar 4 meeting (termination notification), improvement evidence (60% to 75% code review), timeline complaint (40 vs 60 days)
- Key: Feb 15 meeting included brief PIP reference but was primarily project planning
- Mar 4 meeting was functionally termination, not PIP review

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/pip-timeline-analysis.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C3 (non-conflict timeline reveals violations)
**Content key points:**
- Title: "PIP 时间线分析 -- 张涛案件"
- Complete timeline reconstruction from all sources
- Key finding: 40 days vs 60-day policy minimum
- PIP document shortened policy (30 vs 60 days) without justification
- Week 4 check-in never documented
- Mar 4 was termination notification, not PIP review
- Process gaps clearly enumerated

**Length estimate:** ~600 words, ~900 tokens

---

### updates/legal-updated-assessment.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (full reversal -- legal hedging)
**Content key points:**
- Title: "法务更新评估 -- 张涛解雇案"
- Ma Li acknowledges "some gaps" but uses hedging language
- "Totality of circumstances" framing
- Does not retract initial "sufficient" assessment
- Recommends considering negotiation with employee
- Implicitly admits initial review was insufficient

**Length estimate:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_MALI_EMAIL_UUID.jsonl (Update 4)

**File type:** session append
**Associated contradictions:** C4 (legal hedging), B2 (reversal trigger)
**Content key points:**
- Loops 9-12: Ma Li's updated assessment, hedging on implications, revised risk assessment, lessons learned
- Key shift: "sufficient documentation" → "some gaps" → "totality of circumstances"
- Recommends preparing for possible arbitration and considering settlement
- Implicitly admits initial review was superficial

**Length estimate:** ~800 words, ~1,200 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_CHENHAO_FEISHU_UUID
  - Update 2 appends to PLACEHOLDER_SUNWEI_EMAIL_UUID and PLACEHOLDER_ZHANGTAO_IM_UUID
  - Update 4 appends to PLACEHOLDER_MALI_EMAIL_UUID
- [x] All workspace files have content descriptions in layer1
- [x] Updates support intended reversals
  - U1 -> C1 partial (R2->R5): verbal vs written distinction from 1:1 notes
  - U2 -> C1 full (R2->R7): Sun Wei confirms verbal=written confusion
  - U2 -> C2 nuanced (R3->R8): Zhang Tao's meeting experience differs from calendar labels
  - U3 -> C3 extended: timeline analysis reveals policy violations
  - U4 -> C4 full (R6->R9): legal hedging reveals initial assessment was superficial
- [x] Session filenames use consistent PLACEHOLDER format
- [x] Factual figures are internally consistent
  - Warning emails: 1 (Jan 15)
  - Verbal discussions: 2 (Nov 20, Dec 18)
  - PIP initiated: Feb 1 (Day 0)
  - PIP check-ins: Feb 15 (Day 14, documented) and Mar 4 (Day 31, undocumented)
  - Termination: Mar 13 (Day 40)
  - Policy minimum: 60 days
  - PIP document plan: 30 days
  - Code review improvement: 60% → 75% (target 85%)

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "sunwei-1on1-notes.md", "source": "updates/sunwei-1on1-notes.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl" }
]
```

### R7 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "sunwei-written-response.md", "source": "updates/sunwei-written-response.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SUNWEI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_SUNWEI_EMAIL_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGTAO_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGTAO_IM_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "pip-timeline-analysis.md", "source": "updates/pip-timeline-analysis.md" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "legal-updated-assessment.md", "source": "updates/legal-updated-assessment.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MALI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_MALI_EMAIL_UUID.jsonl" }
]
```
