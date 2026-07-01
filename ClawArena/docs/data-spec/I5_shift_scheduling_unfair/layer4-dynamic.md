# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger | Goal | Sessions? | Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Detailed HR overtime data with per-physician breakdown | Yes: Wang IM Phase 2 | Yes: hr-overtime-records.md (replace) | Confirms C1 numbers, rules out counting error |
| U2 | Before R7 | Algorithm analysis -- Oct 1 deployment correlates with shift increase | Yes: Xiao He IM Phase 2 | Yes: algorithm-analysis.md | Seeds C4, shows timing correlation |
| U3 | Before R11 | IT confirms Zhang approved the update + deployment email | Yes: Zhang Zhuren IM Phase 2 | Yes: it-deployment-confirmation.md | R4->R8 seed: Zhang's denial contradicted |
| U4 | Before R21 | IT confirms the seniority weight bug | No | Yes: it-bug-report.md | Complete resolution |

---

## 2. Action Lists

### Update 1
```json
[
  {"type": "workspace", "action": "replace", "path": "hr-overtime-records.md", "source": "updates/hr-overtime-records.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_WANG_DOC_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_WANG_DOC_IM_UUID.jsonl"}
]
```

### Update 2
```json
[
  {"type": "workspace", "action": "new", "path": "algorithm-analysis.md", "source": "updates/algorithm-analysis.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_XIAHE_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_XIAHE_IM_UUID.jsonl"}
]
```

### Update 3
```json
[
  {"type": "workspace", "action": "new", "path": "it-deployment-confirmation.md", "source": "updates/it-deployment-confirmation.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_ZHANG_ZHUREN_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANG_ZHUREN_IM_UUID.jsonl"}
]
```

### Update 4
```json
[
  {"type": "workspace", "action": "new", "path": "it-bug-report.md", "source": "updates/it-bug-report.md"}
]
```

---

## 3. Source File Content Summaries

### hr-overtime-records.md (U1, replaces initial)
- Detailed per-physician Q4 overtime breakdown
- Confirms Lin Yi's numbers exactly
- Shows comparative: Lin Yi is 40% above average
- Overtime pay calculations match shift counts
- **Independent verification from separate system**

### algorithm-analysis.md (U2)
- Title: "排班算法分析 -- v2.3.1 参数说明"
- Xiao He helps interpret the changelog
- "seniority weight" parameter: supposed to give senior attendings priority for preferred shifts
- But deployed Oct 1 -- exact date Lin Yi's shifts spiked
- Analysis shows: all junior attendings (1-3 years) got more nights; all senior (5+) got fewer
- Correlation between seniority and night shifts is -0.85 (inverse, should be positive or neutral)

### it-deployment-confirmation.md (U3)
- Title: "信息科部署确认 -- 排班系统v2.3.1"
- IT response: "v2.3.1 was deployed Oct 1 per approval email from 张主任 dated Sep 28"
- Includes approval email excerpt: "同意部署排班系统更新 -- 张主任" (Approve scheduling system update -- Zhang)
- IT notes: "We are reviewing the algorithm parameters following Dr. Lin's inquiry"
- **Directly contradicts Zhang's "I didn't know about any update"**

### it-bug-report.md (U4)
- Title: "排班系统Bug报告 -- v2.3.1 资历权重反向 | 信息科"
- Bug: seniority_weight parameter implemented as `1 / years_since_promotion` instead of `years_since_promotion`
- Effect: junior attendings get MORE night shifts; the more junior, the more nights
- Lin Yi (2 years): weight = 0.5 (high night allocation)
- Senior attending (8 years): weight = 0.125 (low night allocation)
- Fix: v2.3.2 will correct the formula and retroactively rebalance Q1 2026
- Root cause: code error in configuration, not detected in testing (test data used uniform seniority)
