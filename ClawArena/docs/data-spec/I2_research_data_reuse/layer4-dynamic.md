# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver detailed pipeline log with V2.0/V2.1 version diff -- resolves C1 (three-way N reconciliation) and C2 (refutes complaint's "selective inclusion" and "dataset manipulation" allegations) | No new session append | Yes: data-cleaning-pipeline-log.md (replaced with detailed version) | R2->R5 (C1: N discrepancy resolved by version control); R3->R6 (C2: complaint allegations refuted by pipeline evidence) |
| U2 | Before R7 | Deliver 王医生's documented tone shift -- establishes C4 (supportive to cautious) | Yes: 王医生 IM Phase 2 append | Yes: wang-yisheng-statement-shift.md | R4->R8 (C4: 王医生's shift documented) |
| U3 | Before R11 | Deliver 张主任's guidance and assessment -- provides institutional context for C4 (王医生's caution is career-motivated) and confirms C2 resolution (committee assessment aligns with technical evidence) | Yes: 张主任 IM Phase 2 append | Yes: zhangzhuren-guidance.md | R7->R11 (C4: 王医生's caution explained by career context) |
| U4 | Before R21 | Deliver ethics timeline verification and committee preliminary assessment -- confirms C3 non-conflict definitively and signals favorable resolution | Yes: 学术委员会 Email Phase 2 append | Yes: ethics-timeline-verification.md | No new reversal; confirms C3 and provides resolution pathway |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4, before R5.
**Purpose:** Replaces the partial pipeline log with the detailed version including V2.0/V2.1 diff, dedup audit of all 65 records, and the 23-record ID selection explanation. This is the key evidence that resolves C1 and C2.

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "data-cleaning-pipeline-log.md",
    "source": "updates/data-cleaning-pipeline-log.md"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6, before R7.
**Purpose:** Introduces wang-yisheng-statement-shift.md documenting the tone change. Appends 王医生 IM Phase 2 (distancing conversation, career concern disclosure, continued agreement with technical explanation).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "wang-yisheng-statement-shift.md",
    "source": "updates/wang-yisheng-statement-shift.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_WANGYISHENG_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_WANGYISHENG_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10, before R11.
**Purpose:** Introduces zhangzhuren-guidance.md and appends 张主任 IM Phase 2 (supportive assessment, 王医生 career context, recommended response structure, documentation improvement advice).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "zhangzhuren-guidance.md",
    "source": "updates/zhangzhuren-guidance.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGZHUREN_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGZHUREN_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20, before R21.
**Purpose:** Introduces ethics-timeline-verification.md with full verified timeline. Appends 学术委员会 Email Phase 2 (timeline confirmed, preliminary assessment of "data management issue not misconduct," expected resolution of corrigendum).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ethics-timeline-verification.md",
    "source": "updates/ethics-timeline-verification.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_COMMITTEE_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_COMMITTEE_EMAIL_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/data-cleaning-pipeline-log.md (Update 1)

**File type:** workspace replace
**Associated contradictions:** C1 (complete resolution), C2 (refutes complaint)
**Content key points:**
- Full version history with diff:
  - V2.0 (2025-09-20, 王医生): dedup PatientID+VisitDate, tiebreaker newest ID
  - V2.1 (2025-10-15, Lin Yi): dedup PatientID+VisitDate, tiebreaker oldest ID
  - 65 records confirmed as HIS migration duplicates
  - 23 records affected by tiebreaker change; clinical data identical
- Key conclusion: version control artifact, not data manipulation

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/wang-yisheng-statement-shift.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C4 (documents shift)
**Content key points:**
- Chronological record of 王医生's communications
- W1D3: supportive, offers to write explanation
- W1D4: provides V2.0 dataset
- W2D3: cautious, does not want to be "too involved"
- Context: shift coincided with committee formal involvement

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_WANGYISHENG_IM_UUID.jsonl (Update 2)

**File type:** session append
**Associated contradictions:** C4 (tone shift), B2 (insertion + context for reversal)
**Content key points:**
- Loop 11: 王医生 shifts to caution
- Loop 12: Explains career concern (promotion)
- Loop 13: Still agrees with technical explanation; will cooperate if committee asks
- Loop 14: Practical arrangement (Lin Yi leads response)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/zhangzhuren-guidance.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C4 context, C2 confirmation
**Content key points:**
- 张主任: "这个事情不大，但流程要走"
- Recommends 3-page response: data provenance, version diff, study period comparison
- Provides context for 王医生's career concerns
- Documentation improvement advice for future papers

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_ZHANGZHUREN_IM_UUID.jsonl (Update 3)

**File type:** session append
**Associated contradictions:** C4 (career context), C2 (director confirms explanation)
**Content key points:**
- Loop 7: 张主任 reviews materials, confirms explanation solid
- Loop 8: Contextualizes 王医生's promotion concern
- Loop 9: Recommended response structure
- Loop 10: Documentation improvement advice

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/ethics-timeline-verification.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C3 (definitive non-conflict)
**Content key points:**
- Full verified timeline: IRB 2025-08-01 -> extraction 2025-09-15 -> V2.0 2025-09-20 -> V2.1 2025-10-15 -> submission 2025-11-01 -> publication 2026-01-15 -> complaint 2026-03-16
- All dates verified by committee as consistent
- IRB predates all processing

**Length estimate:** ~300 words, ~450 tokens

---

### updates/PLACEHOLDER_COMMITTEE_EMAIL_UUID.jsonl (Update 4)

**File type:** session append
**Associated contradictions:** C3 (verified), resolution pathway
**Content key points:**
- Loop 7: Committee confirms ethics timeline
- Loop 8: Preliminary assessment: "data management issue, not misconduct"
- Loop 9: Expected resolution: corrigendum + improved methods, no retraction or disciplinary action

**Length estimate:** ~600 words, ~900 tokens

---

## 4. Runtime Checks

- [x] Session appends match session IDs
  - Update 2 appends to PLACEHOLDER_WANGYISHENG_IM_UUID
  - Update 3 appends to PLACEHOLDER_ZHANGZHUREN_IM_UUID
  - Update 4 appends to PLACEHOLDER_COMMITTEE_EMAIL_UUID
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
  - U1 -> C1 resolution + C2 refutation via pipeline log
  - U2 -> C4 establishment via tone shift documentation
  - U3 -> C4 explanation (career context) + C2 institutional confirmation
  - U4 -> C3 definitive confirmation + resolution pathway
- [x] Factual figures consistent
  - Paper N: 847; Raw DB N: 912; Duplicates: 65; ID differences: 23
  - V2.0: 2025-09-20 (王医生); V2.1: 2025-10-15 (Lin Yi)
  - IRB: 2025-08-01; Submission: 2025-11-01; Publication: 2026-01-15
  - Complaint: 2026-03-16
  - HIS migration: 2025-07-15
  - Zhang et al. 2024 data period: 2022-2023; Lin Yi data period: 2024-2025

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "data-cleaning-pipeline-log.md", "source": "updates/data-cleaning-pipeline-log.md" }
]
```

### R7 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "wang-yisheng-statement-shift.md", "source": "updates/wang-yisheng-statement-shift.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_WANGYISHENG_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_WANGYISHENG_IM_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "zhangzhuren-guidance.md", "source": "updates/zhangzhuren-guidance.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGZHUREN_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGZHUREN_IM_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "ethics-timeline-verification.md", "source": "updates/ethics-timeline-verification.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_COMMITTEE_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_COMMITTEE_EMAIL_UUID.jsonl" }
]
```
