# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver official class ranking (62nd) and teacher's correction -- triggers C1 reversal (preliminary top 50 vs actual 62nd) | Yes: 赵老师 IM Phase 2 append (correction + explanation) | Yes: class-ranking-official.md | R2->R5 (C1: ranking corrected from top 50 to 62nd) |
| U2 | Before R7 | Deliver official 2026 admission lines (520, +5 from 2025) -- triggers C2 reversal (rumor of decrease vs actual increase) | Yes: 李浩 IM Phase 2 append (line verification + rumor debunking) | Yes: admission-score-lines.md (replaced with 2026 data) | R3->R7 (C2: rumor directly contradicted by official lines) |
| U3 | Before R11 | Deliver university-specific admission lines -- provides concrete application guidance | No new session append | Yes: university-specific-lines.md | No new reversal; provides resolution data |
| U4 | Before R21 | Deliver cross-province comparison explanation and mother's correction -- triggers C4 reversal | Yes: 母亲 IM Phase 2 append (province difference clarified) | Yes: cross-province-explainer.md | R6->R9 (C4: cross-province comparison invalidated) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces class-ranking-official.md with Wang Ming at rank 62nd. Appends teacher correction to 赵老师 IM. Resolves C1: preliminary top 50 was based on estimated scores; actual rank is 62nd.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "class-ranking-official.md",
    "source": "updates/class-ranking-official.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHAOLAOSHI_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHAOLAOSHI_IM_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Replaces admission-score-lines.md with version including 2026 official data (first-tier 520). Appends 李浩 IM Phase 2 (independent verification, rumor source identification). Triggers C2 reversal.

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "admission-score-lines.md",
    "source": "updates/admission-score-lines.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIHAO_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces university-specific-lines.md with UESTC at 608, 川大 at 612, etc. Provides concrete data for application decision.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "university-specific-lines.md",
    "source": "updates/university-specific-lines.md"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces cross-province-explainer.md explaining Hubei vs Sichuan exam differences. Appends 母亲 IM Phase 2 (mother corrected about province difference). Triggers C4 full reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cross-province-explainer.md",
    "source": "updates/cross-province-explainer.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MOTHER_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MOTHER_IM_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/class-ranking-official.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (resolution)
**Content key points:**
- Official class ranking from school academic office
- Wang Ming: Rank 62 / 398, Score 623
- Top 50 cutoff: Score 630
- Top 10 list for reference (scores 660-640)
- 赵老师's correction message included

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_ZHAOLAOSHI_IM_UUID.jsonl (Update 1)

**File type:** session append
**Associated contradictions:** C1 (teacher correction)
**Content key points:**
- Loop 7: Teacher corrects ranking to 62nd, apologizes
- Loop 8: Explains methodology gap (estimated vs actual scores)

**Length estimate:** ~400 words, ~600 tokens

---

### updates/admission-score-lines.md (Update 2)

**File type:** workspace replace
**Associated contradictions:** C2 (resolution)
**Content key points:**
- All historical data preserved
- **Added: 2026年四川理科一本线: 520** (vs 2025: 515, increase of 5)
- UESTC 2026 projected: 605-615
- Directly contradicts "降了10分" rumor

**Length estimate:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl (Update 2)

**File type:** session append
**Associated contradictions:** C2 (independent verification)
**Content key points:**
- Loop 11: Li Hao confirms official lines (520, +5 from 2025)
- Loop 12: UESTC analysis (610 historical, Wang Ming competitive)
- Loop 13: Rumor source traced to Hebei province article

**Length estimate:** ~600 words, ~900 tokens

---

### updates/university-specific-lines.md (Update 3)

**File type:** workspace new
**Associated contradictions:** None (resolution data)
**Content key points:**
- UESTC: 608
- 四川大学: 612
- 西南交通大学: 580
- Wang Ming 623 vs UESTC 608: +15 margin

**Length estimate:** ~400 words, ~600 tokens

---

### updates/cross-province-explainer.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (resolution)
**Content key points:**
- Sichuan: 全国甲卷; Hubei: 全国乙卷
- Different papers, different difficulty, non-comparable
- Batch 1 (06:00) vs Batch 2 (08:00) explanation
- Mother's correction: "原来那个孩子是湖北的卷子"

**Length estimate:** ~300 words, ~450 tokens

---

### updates/PLACEHOLDER_MOTHER_IM_UUID.jsonl (Update 4)

**File type:** session append
**Associated contradictions:** C4 (mother corrected), B2 (reversal)
**Content key points:**
- Loop 9: Mother clarifies province difference, says 623 is good
- Loop 10: Asks about UESTC admission
- Loop 11: Expresses pride

**Length estimate:** ~400 words, ~600 tokens

---

## 4. Runtime Checks

- [x] Session appends match session IDs
  - Update 1 appends to PLACEHOLDER_ZHAOLAOSHI_IM_UUID
  - Update 2 appends to PLACEHOLDER_LIHAO_IM_UUID
  - Update 4 appends to PLACEHOLDER_MOTHER_IM_UUID
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
  - U1 -> C1 reversal (R2->R5): rank corrected
  - U2 -> C2 reversal (R3->R7): rumor contradicted
  - U3 -> resolution data: university-specific lines
  - U4 -> C4 reversal (R6->R9): province difference clarified
- [x] Factual figures consistent
  - Score: 623 (Sichuan)
  - Rank: 62nd (actual), top 50 (preliminary)
  - Class size: ~398-400
  - First-tier line: 520 (2026), 515 (2025), delta +5
  - UESTC historical: ~610; 2026: ~608
  - Hubei child: 645 (different exam)
  - Batch 1: 06:00; Batch 2: 08:00 (Sichuan)

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "class-ranking-official.md", "source": "updates/class-ranking-official.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHAOLAOSHI_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHAOLAOSHI_IM_UUID.jsonl" }
]
```

### R7 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "admission-score-lines.md", "source": "updates/admission-score-lines.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIHAO_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "university-specific-lines.md", "source": "updates/university-specific-lines.md" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "cross-province-explainer.md", "source": "updates/cross-province-explainer.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MOTHER_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_MOTHER_IM_UUID.jsonl" }
]
```
