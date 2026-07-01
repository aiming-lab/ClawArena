# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger | Goal | New Sessions? | New Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Physician-specific breakdown showing Dr. Wang's pre-guideline increase | Yes: Wang Doc IM Phase 2 | Yes: prescription-physician-breakdown.md | Seeds C4 temporal evidence |
| U2 | Before R7 | Guideline detail analysis -- oral preferred, class not brand | No | Yes: guideline-detail-analysis.md | R2->R6 (C1: guideline doesn't justify pattern) |
| U3 | Before R11 | External hospital comparison (Xiao Mei's hospital rejected injection form) | Yes: Xiao Mei IM Phase 2 | Yes: external-hospital-comparison.md | R3->R7 (C2: strengthens causation) |
| U4 | Before R21 | Financial trail -- ¥68 vs ¥3 pricing, ¥50,000 sponsorship | Yes: Zhang Zhuren IM Phase 2 | Yes: pharmacy-procurement-log.md (replaced) | R4->R8 (C4: financial motivation); comprehensive |

---

## 2. Action Lists

### Update 1
```json
[
  {"type": "workspace", "action": "new", "path": "prescription-physician-breakdown.md", "source": "updates/prescription-physician-breakdown.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_WANG_DOC_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_WANG_DOC_IM_UUID.jsonl"}
]
```

### Update 2
```json
[
  {"type": "workspace", "action": "new", "path": "guideline-detail-analysis.md", "source": "updates/guideline-detail-analysis.md"}
]
```

### Update 3
```json
[
  {"type": "workspace", "action": "new", "path": "external-hospital-comparison.md", "source": "updates/external-hospital-comparison.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_XIAOMEI_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_XIAOMEI_IM_UUID.jsonl"}
]
```

### Update 4
```json
[
  {"type": "workspace", "action": "replace", "path": "pharmacy-procurement-log.md", "source": "updates/pharmacy-procurement-log.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_ZHANG_ZHUREN_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANG_ZHUREN_IM_UUID.jsonl"}
]
```

---

## 3. Source File Content Summaries

### updates/prescription-physician-breakdown.md (U1)
- Title: "处方统计 -- 按医生分月 | 奥美拉唑注射液"
- Dr. Wang: Jan 5, **Feb 1-14: 12 (pre-guideline!)**, Feb 15-28: 8, Mar: 35
- Lin Yi: Jan 3, Feb 8, Mar 10
- Others combined: Jan 12, Feb 22, Mar 35
- **Key finding:** Dr. Wang prescribed 12 injection-form omeprazole in the first 14 days of Feb, BEFORE the guideline was published on Feb 15. This is a 140% increase from his Jan baseline, with no published guideline to justify it.

### updates/guideline-detail-analysis.md (U2)
- Title: "指南原文分析 -- 关键条款"
- Guideline says: PPI CLASS recommended (not brand-specific)
- Guideline says: "口服优先" for stable patients
- Guideline says: IV only for "血流动力学不稳定" patients
- Guideline says: consider cost-effectiveness
- **Conclusion:** Current prescribing pattern (injection-dominant, brand-specific) exceeds guideline recommendations

### updates/external-hospital-comparison.md (U3)
- Title: "外院对比 -- 某三甲医院PPI使用数据（小美提供）"
- Xiao Mei's hospital: similar patient volume, guideline adopted
- Their increase: 20%, mostly oral form
- Their pharmacy committee rejected injection form (cost-benefit unfavorable)
- **Conclusion:** A comparable hospital had modest increase in oral PPI, not 300% injection increase

### updates/pharmacy-procurement-log.md (U4, replaces initial)
- Same content as initial PLUS:
- **New entry:** "学术赞助记录: 2026-02-01, 安泽制药 -> 急诊科, ¥50,000, 用途: 学术交流活动赞助"
- Price comparison highlighted: injection ¥68/vial vs oral ¥3/capsule
- Estimated monthly cost difference: injection usage at 70 vials = ¥4,760 vs oral equivalent ~¥270
- **Financial context:** ¥50,000 sponsorship + expensive injection preference + pharma dinners = concerning financial pattern
