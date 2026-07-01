# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver CTO's detailed breakdown revealing QA exclusion is deliberate + role guide authority | Yes: Li Qiang Feishu Phase 2 append | Yes: cto-role-breakdown.md | R2->R5 (C1: definitional difference confirmed); R3->R7 (C2: role guide supports HR) |
| U2 | Before R7 | Deliver Finance cost-center source of CEO's 35% + Zhang Wei investigation | Yes: Zhang Wei Feishu Phase 2 append (partial) | Yes: finance-headcount-report.md | R6->R8 (C4: 35% traced to Finance cost-center methodology error) |
| U3 | Before R11 | Deliver CFO's methodology explanation | Yes: Zhao Lin Email Phase 2 | Yes: cfo-methodology-email.md | No new reversal; extends C4 with authoritative explanation |
| U4 | Before R21 | Deliver board correction urgency | Yes: Zhang Wei Feishu Phase 2 append (final) | Yes: board-correction-plan.md | Enables comprehensive R21-R30 assessment |

---

## 2. Action Lists

### Update 1 (before R5)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cto-role-breakdown.md",
    "source": "updates/cto-role-breakdown.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "finance-headcount-report.md",
    "source": "updates/finance-headcount-report.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID_part1.jsonl"
  }
]
```

### Update 3 (before R11)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cfo-methodology-email.md",
    "source": "updates/cfo-methodology-email.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "board-correction-plan.md",
    "source": "updates/board-correction-plan.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID_part2.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/cto-role-breakdown.md (Update 1)
**File type:** workspace new
**Associated contradictions:** C1 (full), C2 (full)
**Content:** CTO's complete 60-person headcount, explicit QA/UX exclusion with reasoning, philosophy statement about "writing code" definition.
**Length estimate:** ~750 tokens

### updates/PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl (Update 1)
**File type:** session append
**Content:** Loops 9-12: CTO provides breakdown, learns about role guide, pragmatically accepts 32% for this quarter, asks about CEO's 35%.
**Length estimate:** ~1,200 tokens

### updates/finance-headcount-report.md (Update 2)
**File type:** workspace new
**Associated contradictions:** C4 (full reversal)
**Content:** Finance cost-center data: 69 people, includes 4 PMs + 5 tech writers. 24 female = 34.8%. Zhang Wei annotation tracing CEO's 35%.
**Length estimate:** ~750 tokens

### updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID_part1.jsonl (Update 2)
**File type:** session append
**Content:** Loops 9-12: Zhang Wei reveals Finance source, discusses implications, governance gap, board urgency.
**Length estimate:** ~1,200 tokens

### updates/cfo-methodology-email.md (Update 3)
**File type:** workspace new
**Associated contradictions:** C4 (extended explanation)
**Content:** Zhao Lin explains cost-center vs functional classification, confirms PMs and tech writers included, recommends using HR data for diversity reporting.
**Length estimate:** ~600 tokens

### updates/PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl (Update 3)
**File type:** session append (new session starts)
**Content:** Loops 1-4: Zhao Lin explains data, cost-center methodology, scope differences, governance recommendation.
**Length estimate:** ~900 tokens

### updates/board-correction-plan.md (Update 4)
**File type:** workspace new
**Content:** Zhang Wei's request for correction plan: recommended number, discrepancy explanation, prevention process. Urgency: 35% already with board members.
**Length estimate:** ~600 tokens

### updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID_part2.jsonl (Update 4)
**File type:** session append
**Content:** Loops 13-14: Zhang Wei requests complete recommendation, confirms 32% approach with methodology note.
**Length estimate:** ~600 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
- [x] All workspace files have content descriptions in layer1
- [x] Updates support intended reversals
  - U1 -> C1/C2 reversal: CTO's exclusion is deliberate; role guide supports HR
  - U2 -> C4 reversal: 35% traced to Finance cost-center data
  - U3 -> C4 extension: CFO confirms methodology difference
  - U4 -> Comprehensive: board correction urgency enables final assessment
- [x] Factual figures internally consistent
  - HR: 81 people, 26 female = 32.1%
  - CTO: 60 people, 17 female = 28.3%
  - Finance: 69 people, 24 female = 34.8%
  - QA: 15 people, 11 female
  - UX: 6 people, 4 female
  - PMs (in Finance scope): 4 people
  - Tech Writers (in Finance scope): 5 people
  - Verification: HR(81) = CTO(60) + QA(15) + UX(6); Finance(69) = CTO(60) + PM(4) + TechWriters(5)

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "cto-role-breakdown.md", "source": "updates/cto-role-breakdown.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl" }
]
```

### R7 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "finance-headcount-report.md", "source": "updates/finance-headcount-report.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID_part1.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "cfo-methodology-email.md", "source": "updates/cfo-methodology-email.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "board-correction-plan.md", "source": "updates/board-correction-plan.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID_part2.jsonl" }
]
```
