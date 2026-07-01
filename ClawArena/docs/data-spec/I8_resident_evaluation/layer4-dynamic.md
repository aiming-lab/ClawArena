# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver training-program-standards.md (process-first evaluation criteria) | No | Yes: training-program-standards.md | R1->R5 (C1: 林怡's evaluation justified by standards) |
| U2 | Before R6 | Deliver department-kpi-dashboard.md + 张主任 explicit pressure | Yes: 张主任 DM Phase 2 append (Loop 11-12) | Yes: department-kpi-dashboard.md | R2->R6 (C4: KPI pressure vs clinical standards) |
| U3 | Before R8 | Deliver 王医生 historical context (evaluation inflation pattern) | Yes: 王医生 DM Phase 2 append (Loop 7-8) | No | R8->R11 seed (historical evaluation inflation confirmed) |
| U4 | Before R21 | Deliver comprehensive resolution (林怡 proposes standardized checklist) | No new sessions (referenced in L0 narrative only) | No | R8->R11 full (B2 refuted, systemic issue confirmed); comprehensive R21-R30 |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "training-program-standards.md",
    "source": "updates/training-program-standards.md"
  }
]
```

### Update 2 (before R6)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "department-kpi-dashboard.md",
    "source": "updates/department-kpi-dashboard.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID_u2.jsonl"
  }
]
```

### Update 3 (before R8)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_WANGYISHENG_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_WANGYISHENG_WECHAT_UUID.jsonl"
  }
]
```

### Update 4 (before R21)
```json
[]
```
*(No new files or session appends -- Update 4 is narrative resolution referenced in existing data.)*

---

## 3. Source File Content Summaries

### updates/training-program-standards.md (Update 1)
**Associated contradictions:** C1 (evaluation criteria), C4 (process > KPI)
- Section 4.2: process compliance first
- Section 4.3: deviations without adverse events still count
- Section 5.1: scoring rubric (2/5 = technical deviations needing improvement)
- Section 6.1: clinical accuracy paramount
- **Length:** ~500 words, ~750 tokens

### updates/department-kpi-dashboard.md (Update 2)
**Associated contradictions:** C4 (KPI pressure context)
- KPI target ≥90% pass rate
- Current: 9/10 (90% borderline if 孙医生 fails)
- Historical rates: 2025=95%, 2024=100%
- **Length:** ~400 words, ~600 tokens

### updates/PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID_u2.jsonl (Update 2)
**Associated contradictions:** C4 (explicit pressure to change evaluation)
- Loops 11-12: 张主任 explicitly asks to change to "达标," 林怡 pushes back
- **Length:** ~300 words, ~450 tokens

### updates/PLACEHOLDER_WANGYISHENG_WECHAT_UUID.jsonl (Update 3)
**Associated contradictions:** Historical evaluation inflation
- Loops 7-8: 王医生 reveals 孙医生 had same issues last year, previous evaluator gave "达标" under pressure, consequence is persistent skill gap
- **Length:** ~400 words, ~600 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - U2: appends to PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID
  - U3: appends to PLACEHOLDER_WANGYISHENG_WECHAT_UUID
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
  - U1 -> C1/C4 evaluation criteria (R1->R5)
  - U2 -> C4 KPI context (R2->R6)
  - U3 -> Historical pattern (R8->R11 seed)
  - U4 -> Comprehensive (R8->R11 full)
- [x] Evaluation scores consistent across all sources
  - 林怡: 临床判断3, 操作技能2, 病历书写3, 团队协作4, 职业态度4 = "未达预期"
  - 孙医生: 临床判断4, 操作技能4, 病历书写4, 团队协作4, 职业态度5 = "达标"
  - Key gap: 操作技能 2 vs 4
- [x] Case details consistent
  - Case A: 胸腔穿刺偏内1.5cm, near internal mammary artery
  - Case B: 导丝18cm (standard 15cm), catheter tip too low on X-ray
  - Case C: 缝合间距1cm (standard 0.5cm), wider scarring at follow-up
- [x] KPI: target ≥90%, 10 residents total, 1 failure = 90% (borderline)
- [x] Training completion: rotations ✓, exam 82 ✓, discussions 10 ✓

---

## 5. questions.json Update Fields

### R5:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "training-program-standards.md", "source": "updates/training-program-standards.md" }
]
```

### R6:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "department-kpi-dashboard.md", "source": "updates/department-kpi-dashboard.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID_u2.jsonl" }
]
```

### R8:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_WANGYISHENG_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_WANGYISHENG_WECHAT_UUID.jsonl" }
]
```

### R21:
```json
"update": []
```
