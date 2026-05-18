# Layer 1 -- Workspace File Spec

> Workspace files under `benchmark/data/calmb-new/workspaces/trace_i3/`.
> Files simulate hospital system exports. Chinese primary with English medical/system terms.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md -- IDENTITY.md -- SOUL.md -- USER.md -- TOOLS.md

Standard 5-file config set. IDENTITY.md establishes the agent as a medical compliance analysis assistant for Lin Yi. SOUL.md emphasizes evidence-based analysis, temporal reasoning, distinguishing correlation from causation, and financial transparency. USER.md lists Lin Yi (protagonist), Dr. Wang (colleague), Zhang Li (pharma rep -- no direct session), 张主任 (department chief), 同学小美 (confidant).

---

## 2. Scenario-Specific Workspace Files

### prescription-statistics.md (Initial)

**Content key points:**
- Title: `急诊科处方统计导出 -- 奥美拉唑注射液 | 2026年Q1`
- Monthly totals: Jan 20, Feb 50, Mar 80 (through Mar 25)
- By physician (monthly): Dr. Wang: 5->20->35; Lin Yi: 3->8->10; Others: 12->22->35
- By form: Injection (AnZe brand): 15->40->70; Oral (generic): 5->10->10
- **C1 source:** 300% increase visible, concentrated in injection form, Dr. Wang top prescriber
- **Near-signal noise:** Other drug statistics for common ER medications (antibiotics, analgesics) at normal levels

**Length estimate:** ~800 words, ~1,200 tokens

---

### pharma-rep-visit-log.md (Initial)

**Content key points:**
- Title: `医药代表来访登记 -- 急诊�� | 2026年Q1`
- **Key entries:**
  - Jan 20: 张丽, 安泽制药, purpose: "学术推广 -- 奥美拉唑注射液", met: Dr. Wang + 3 others
  - Feb 1: 张丽, 安泽制药, purpose: "学术交流晚宴", location: 北京饭店, attendees: Dr. Wang + 5 others
  - Mar 1: 张丽, 安泽制药, purpose: "产品更新", met: Dr. Wang + nursing staff
  - Mar 5: 张丽, 安泽制药, purpose: "学术晚宴（第二次）", location: 京城会所, attendees: Dr. Wang + 2 others
  - Mar 15: 张丽, 安泽制药, purpose: "科室学术报告", invited by: Dr. Wang
- **C2 source:** Visit timing correlates with prescription increases
- **C4 source:** Feb 1 dinner is 14 days BEFORE guideline (Feb 15)
- **Near-signal noise:** Other pharma reps visiting (different companies, different drugs) at normal frequency

**Length estimate:** ~600 words, ~900 tokens

---

### clinical-guideline-update.md (Initial)

**Content key points:**
- Title: `急诊科应激性溃疡防治专家共识 (2026) -- 摘要`
- Published: **February 15, 2026**
- Key recommendations:
  - Recommend PPI prophylaxis for high-risk ER patients (GCS<10, mechanical ventilation >48h, coagulopathy, etc.)
  - **PPI options: omeprazole, pantoprazole, esomeprazole** (class recommendation, not brand-specific)
  - **Route: "口服优先，血流动力学不稳定者可选择静脉给药"** (oral preferred, IV for hemodynamically unstable)
  - Cost-effectiveness should be considered
- **C1/C3 source:** Guideline is legitimate, published Feb 15, recommends PPI class (not brand/form specific)
- **Near-signal noise:** Full guideline excerpts with evidence grading, references, patient stratification

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### department-meeting-minutes.md (Initial)

**Content key points:**
- Title: `急诊科科务会议纪要 -- 2026年3月15日`
- Attendees include Lin Yi, Dr. Wang, 张主任, other physicians
- Agenda item 3: "急诊PPI使用进展" presented by 张丽 (安泽制药), invited by Dr. Wang
- Zhang Li's presentation emphasized injection form's "faster onset" and "higher bioavailability"
- No mention of cost comparison or oral alternatives
- 张主任 approved the presentation as "学术交流"
- **C2 supporting evidence:** Pharma rep presenting at department meeting, invited by top prescriber

**Length estimate:** ~600 words, ~900 tokens

---

### pharmacy-procurement-log.md (Initial -- partial)

**Content key points:**
- Title: `药房采购记录 -- 急诊科常用药品 | 2026年Q1`
- Drug X procurement volumes increasing: Jan 25 vials, Feb 60 vials, Mar 100 vials
- Price: 奥美拉唑注射液 (安泽) ¥68/vial
- Generic oral omeprazole: ¥3/capsule
- _(Update 4 will add the academic sponsorship record)_
- **Near-signal noise:** Procurement data for other drugs at normal levels

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Visible | Via |
|---|---|---|
| (5 config files) | Initial | Fixed config |
| prescription-statistics.md | Initial | Workspace |
| pharma-rep-visit-log.md | Initial | Workspace |
| clinical-guideline-update.md | Initial | Workspace |
| department-meeting-minutes.md | Initial | Workspace |
| pharmacy-procurement-log.md | Initial (partial) | Workspace |
| prescription-physician-breakdown.md | Update 1 (before R5) | updates/ new |
| guideline-detail-analysis.md | Update 2 (before R7) | updates/ new |
| external-hospital-comparison.md | Update 3 (before R11) | updates/ new |
| pharmacy-procurement-log.md (updated) | Update 4 (before R21) | updates/ replace |
