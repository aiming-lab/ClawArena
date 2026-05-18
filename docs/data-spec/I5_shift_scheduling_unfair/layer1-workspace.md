# Layer 1 -- Workspace File Spec

> Workspace under `benchmark/data/calmb-new/workspaces/trace_i5/`.

---

## 1. Fixed Agent Config Files

Standard 5-file set. IDENTITY: shift scheduling analysis assistant. SOUL: emphasizes statistical analysis, policy compliance checking, source cross-verification, temporal correlation. USER: Lin Yi, 张主任, 王医生, 同学小何 (classmate at another hospital), 丈夫 (husband).

---

## 2. Scenario-Specific Workspace Files

### shift-schedule-q4.md (Initial)
- Title: "急诊科Q4排班表导出 -- 2025年10-12月"
- Full Q4 schedule for all 8 attendings
- **Lin Yi's nights:** Oct 11, Nov 12, Dec 12
- **Dr. Wang:** Oct 7, Nov 7, Dec 7
- **Dr. Chen:** Oct 6, Nov 6, Dec 6
- **Dr. Li:** Oct 8, Nov 8, Dec 8
- **Others:** 6-8 range
- Schedule shows automated assignment (标记: "系统自动排班")
- **C1 source:** Lin Yi's counts exceed policy max (8)
- **C2 source:** Lin Yi is statistically an outlier

**Length:** ~1,000 words, ~1,500 tokens

### department-shift-policy.md (Initial)
- Title: "急诊科排班管理规定 -- 北京友谊医院"
- Key rules:
  - Article 5: 主治医师每月夜班不超过8个 (max 8 night shifts per attending per month)
  - Article 8: 排班应公平轮转，避免连续超额 (fair rotation, avoid consecutive overallocation)
  - Article 12: 排班异议可向科主任提出，3个工作日内回复 (disputes to chief, 3-day response)
  - Article 15: 系统排班需经科主任审批 (system schedule requires chief approval)
- **C1 source:** Policy says max 8; Lin Yi has 11-12.
- **Supporting:** Zhang approved the schedule (Article 15).

**Length:** ~600 words, ~900 tokens

### shift-statistics-comparison.md (Initial)
- Title: "排班统计对比 -- Q4 2025 按医生"
- Lin Yi compiled summary:
  - Lin Yi: 35 nights / 3 months = 11.7 avg
  - Department average: 7.5/month
  - Deviation: +40% above average, +47% above policy max
  - Peer comparison table
- **C2 source:** Statistical proof of unfairness

**Length:** ~500 words, ~750 tokens

### hr-overtime-records.md (Initial -- summary level)
- Title: "加班记录导出 -- 林怡 | 人事系统"
- Overtime hours per month, confirming night shift counts
- Lin Yi's total overtime: highest in department
- _(Update 1 adds detailed breakdown)_
- **C3 source:** Independent confirmation of shift counts

**Length:** ~400 words, ~600 tokens

### scheduling-system-changelog.md (Initial -- partial)
- Title: "排班管理系统更新日志"
- Shows recent versions:
  - v2.2.0 (Jul 2025): UI improvements
  - **v2.3.1 (Oct 1, 2025): "Added workload balancing algorithm. Parameters: seniority weight, shift preference, availability constraints. Deployed per department approval."**
  - No v2.3.2 yet
- **C4 source:** Algorithm changed on Oct 1, same time as Lin Yi's shift increase. "Department approval" = Zhang approved.

**Length:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Visible | Via |
|---|---|---|
| (5 config) | Initial | Fixed |
| shift-schedule-q4.md | Initial | Workspace |
| department-shift-policy.md | Initial | Workspace |
| shift-statistics-comparison.md | Initial | Workspace |
| hr-overtime-records.md | Initial (summary) | Workspace |
| scheduling-system-changelog.md | Initial (partial) | Workspace |
| hr-overtime-records.md (detailed) | Update 1 (before R5) | replace |
| algorithm-analysis.md | Update 2 (before R7) | new |
| it-deployment-confirmation.md | Update 3 (before R11) | new |
| it-bug-report.md | Update 4 (before R21) | new |
