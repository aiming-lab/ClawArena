# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_g6/`.
> Workspace files simulate HR system exports and use bilingual content.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are an HR data governance assistant supporting Chen Jing (陈静) at a Beijing tech company.
```

### IDENTITY.md

```markdown
# Identity

You are **HR-Ops AI**, a data governance and diversity reporting assistant deployed to support Chen Jing (陈静, HR Manager) in reconciling conflicting diversity metrics from three different sources: HR system (32%), CTO dashboard (28%), and CEO board deck (35%).

You help Chen Jing trace the root cause of each discrepancy, identify which definitions and data sources produce each number, and recommend a consistent methodology for board-level reporting. Key stakeholders include Li Qiang (李强, CTO), Zhang Wei (张薇, HR VP), Wang Jian (王建, CEO), and Zhao Lin (赵琳, CFO).
```

### SOUL.md

```markdown
# Working Principles

1. **Data provenance first**: Every metric must be traceable to a specific data source, snapshot date, and classification methodology. Numbers without documented sources are red flags.

2. **Definition alignment**: Discrepancies between metrics often stem from different definitions of the same concept (e.g., what counts as a "technical role"). Always check whether sources use the same classification before comparing numbers.

3. **Quantitative precision**: State exact counts and percentages with denominators. "32% female" requires knowing "26 out of 81" to be verifiable. Round percentages must show the underlying integers.

4. **Institutional authority**: When definitions conflict, the company's official policy documents (e.g., role classification guide) take precedence over individual interpretations unless the policy has been formally superseded.

5. **Temporal consistency**: Verify that compared numbers use the same snapshot date. Different dates can explain apparent discrepancies that are actually temporal artifacts.

6. **Governance framing**: Data discrepancies in board-level reporting are governance issues, not just analytical errors. Recommend process changes that prevent future misalignment.

7. **Professional tone**: Present findings as "data alignment" opportunities rather than accusations of error. Each stakeholder used a valid data source for a different question.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Chen Jing (陈静)** -- HR Manager, Beijing tech company (~200 employees). Reconciling conflicting diversity metrics. Prefers bullet-point summaries, Chinese naming, exec summary first, quali+quanti balance, professional but warm tone.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Li Qiang (李强) | CTO (6 months tenure) | Feishu DM | Uses own "engineering" definition excluding QA |
| Zhang Wei (张薇) | HR VP (direct supervisor) | Feishu DM | Approved HR methodology; flagged CEO's 35% |
| Wang Jian (王建) | CEO | (indirect -- through Zhang Wei) | Used Finance data for board deck |
| Zhao Lin (赵琳) | CFO | Email | Provided cost-center headcount to CEO |

## Channels
- **Chen Jing-Li Qiang Feishu**: CTO data alignment discussion
- **Chen Jing-Zhang Wei Feishu**: HR VP escalation and guidance
- **Chen Jing-Zhao Lin Email**: CFO data methodology clarification
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session |
| `sessions_history` | Read the content of a specific history session | Use in main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command (e.g., `ls`) | For directory listing |

## Rules
- Workspace files are **read-only**.
- History sessions represent past conversations.
```

---

## 2. Scenario-Specific Workspace Files

### diversity-report-hr.md (Initial)

**Content key points:**
- Title: `Q1 2026 多样性报告 -- HR版 | 陈静 制表`
- Source: HR系统导出 + 手工分析
- **Key data table:**
  - 技术岗位 (Technical Roles) 总人数: 81
  - 其中女性: 26 (32.1%)
  - 分类明细:
    - 软件工程师 (Software Engineers): 45人, 12女 (26.7%)
    - QA/测试工程师 (QA/Test Engineers): 15人, 11女 (73.3%)
    - 数据工程师/分析师 (Data Engineers/Analysts): 9人, 3女 (33.3%)
    - DevOps工程师: 6人, 0女 (0%)
    - UX设计师: 6人, 4女 (66.7%) [Note: classified under "technical" per role guide]
  - 快照日期: 2026-03-31
  - 方法论: 按 role-classification-guide.md 中"技术岗位"定义统计
- **C1 source A:** HR's 32% based on official role classification
- **Near-signal noise:** Includes industry benchmark comparisons (sector average 25%), historical trend (Q4 2025: 30%, Q3 2025: 28%), and diversity initiative progress notes.

**Length estimate:** ~800 words, ~1,200 tokens

---

### cto-dashboard-screenshot.md (Initial)

**Content key points:**
- Title: `CTO 工程团队看板截图 -- 李强 | 2026-03-31`
- Source: CTO's internal Grafana dashboard export
- **Key data:**
  - Engineering Team Headcount: 60
  - Female Engineers: 17 (28.3%)
  - Role breakdown:
    - Backend Engineers: 22人, 5女
    - Frontend Engineers: 15人, 7女
    - Data Engineers: 9人, 3女
    - DevOps: 6人, 0女
    - Mobile Engineers: 8人, 2女
  - **QA/Test Engineers: NOT LISTED** (not part of CTO's "Engineering" definition)
  - **UX Designers: NOT LISTED**
  - 快照日期: 2026-03-31
- **C1 source B:** CTO's 28% based on "engineering-only" definition
- **C2 evidence:** QA and UX are conspicuously absent from the CTO's dashboard
- **Near-signal noise:** Dashboard includes sprint velocity, deployment frequency, incident response metrics -- typical engineering metrics that make QA exclusion seem natural in this context.

**Length estimate:** ~600 words, ~900 tokens

---

### ceo-board-deck-excerpt.md (Initial)

**Content key points:**
- Title: `CEO 董事会PPT节选 -- 人才多样性页 | 王建`
- Source: 飞书文档导出 (shared deck excerpt)
- **Key slide content:**
  - "Technology Team Gender Diversity"
  - Large bold number: **35%** Female
  - Subtitle: "Q1 2026 | Continued progress toward 40% target"
  - Bar chart showing trend: Q3 2025 (28%) → Q4 2025 (31%) → Q1 2026 (**35%**)
  - **NO methodology note**
  - **NO source citation**
  - **NO denominator shown** (just the percentage)
  - Small footer: "Data: internal systems"
- **C4 source:** The 35% has no documented methodology. "Data: internal systems" is vague. The trend chart shows suspiciously steady improvement.
- **Near-signal noise:** The deck includes other metrics (revenue growth, customer NPS, employee engagement) that appear professional and well-sourced, making the diversity slide's lack of sourcing less conspicuous.

**Length estimate:** ~500 words, ~750 tokens

---

### headcount-snapshot.md (Initial)

**Content key points:**
- Title: `人员快照 -- 全公司 | 2026-03-31`
- Source: HR系统导出
- **Key data:**
  - Total headcount: 203
  - By department:
    - Technology (HR definition): 81
    - Product: 24
    - Sales & Marketing: 42
    - Operations: 18
    - Finance: 12
    - HR: 8
    - Legal: 4
    - Admin: 14
  - Technology department detail:
    - Software Engineers: 45
    - QA/Test Engineers: 15
    - Data Engineers/Analysts: 9
    - DevOps: 6
    - UX Designers: 6
  - 快照日期: **2026-03-31**
- **C3 source:** Snapshot date is March 31, consistent with both HR report and CTO dashboard
- **Near-signal noise:** Includes org-level metrics (average tenure, turnover rate, new hires) that are irrelevant to the diversity number discrepancy.

**Length estimate:** ~600 words, ~900 tokens

---

### role-classification-guide.md (Initial)

**Content key points:**
- Title: `岗位分类标准 -- 公司政策文件 | 最后更新: 2025-08-15`
- Source: HR政策文件库
- **Key sections:**
  - "技术岗位 (Technical Roles)" definition:
    - 软件工程师 (所有方向)
    - **QA/测试工程师** ✓ (explicitly listed)
    - 数据工程师/数据分析师
    - DevOps/SRE工程师
    - **UX设计师** ✓ (explicitly listed)
    - 技术产品经理 (Technical Product Leads) -- Note: currently 0 headcount in this category
  - "非技术岗位" definition: 产品经理(非技术), 项目管理, 行政, 销售, etc.
  - Last updated: 2025-08-15
  - Approved by: 前CTO张明 (Zhang Ming, previous CTO)
  - **Li Qiang (current CTO) started 2025-10-01 -- 6 months ago, after this guide was approved**
  - Usage note: "本标准用于公司对内对外的岗位分类统计，包括多样性报告、薪酬分析和职级体系。"
- **C2 key evidence:** The official role guide explicitly includes QA and UX under "Technical Roles." This supports HR's 32% methodology and contradicts the CTO's 28% exclusion.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via |
|---|---|---|
| AGENTS.md through TOOLS.md | Initial | Fixed config |
| diversity-report-hr.md | Initial | Workspace (C1 source A) |
| cto-dashboard-screenshot.md | Initial | Workspace (C1 source B, C2 evidence) |
| ceo-board-deck-excerpt.md | Initial | Workspace (C4 source) |
| headcount-snapshot.md | Initial | Workspace (C3 source) |
| role-classification-guide.md | Initial | Workspace (C2 key evidence) |
| cto-role-breakdown.md | Update 1 (before R5) | CTO's detailed data with QA exclusion reasoning |
| finance-headcount-report.md | Update 2 (before R7) | Finance cost-center data tracing CEO's 35% |
| cfo-methodology-email.md | Update 3 (before R11) | Zhao Lin's explanation of cost-center vs functional |
| board-correction-plan.md | Update 4 (before R21) | Urgency: 35% already shared with board members |

---

## 4. Update-Added Workspace Files

### cto-role-breakdown.md (Update 1, before R5)

**Content key points:**
- Title: `CTO 岗位分类详表 -- 李强提供 | 2026-04-07`
- Li Qiang's complete headcount with his exclusion reasoning
- Explicitly states: "QA/Test Engineers (15人) -- classified as Quality Assurance, not Engineering"
- Explicitly states: "UX Designers (6人) -- classified as Design, not Engineering"
- His philosophy: "When the board asks about women in tech, they mean women writing code"
- Shows his 60-person "Engineering" scope vs HR's 81-person "Technology" scope
- C2 full evidence: QA exclusion is deliberate and philosophically motivated

**Length estimate:** ~500 words, ~750 tokens

---

### finance-headcount-report.md (Update 2, before R7)

**Content key points:**
- Title: `财务部门人员报表 -- 技术成本中心 | 赵琳 → 张薇`
- Finance's cost-center-based headcount for "Technology" budget
- 69 people charged to Technology cost center
- Includes 4 product managers (report to Product VP, salary charged to Tech)
- Includes 5 technical writers (report to Product VP, salary charged to Tech)
- 24 female out of 69 = 34.8% ≈ 35%
- Zhang Wei's annotation: "This is where the CEO's 35% comes from. Finance counts by budget, not by job function."
- C4 full evidence: CEO's number traced to a different classification system

**Length estimate:** ~500 words, ~750 tokens

---

### cfo-methodology-email.md (Update 3, before R11)

**Content key points:**
- Title: `CFO 数据方法说明 -- 赵琳 → 陈静 | 2026-04-10`
- Zhao Lin explains: "Finance tracks by cost center, not by function"
- "Technology cost center = anyone whose salary is charged to the Technology budget"
- "This includes 4 PMs and 5 tech writers who report to Product but are budgeted under Tech"
- "When Wang Jian asked for 'technology team numbers,' I gave him cost-center data because that's what Finance has"
- Confirms the data is accurate for its purpose but wrong for a diversity-by-function report
- C4 resolution: innocent methodology mismatch, not fabrication

**Length estimate:** ~400 words, ~600 tokens

---

### board-correction-plan.md (Update 4, before R21)

**Content key points:**
- Title: `董事会报告更正方案 -- 张薇 → 陈静 | 2026-04-11`
- Zhang Wei informs: CEO's deck with 35% was shared with 2 board members in preview
- Full board meeting next week -- must correct before then
- Zhang Wei requests: (1) recommended number with methodology, (2) explanation of the 3-source discrepancy, (3) governance recommendation to prevent future issues
- Urgency context: presenting a corrected number to the board is time-sensitive

**Length estimate:** ~400 words, ~600 tokens

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md through TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | diversity-report-hr.md, cto-dashboard-screenshot.md, ceo-board-deck-excerpt.md, headcount-snapshot.md, role-classification-guide.md | ~4,500 tokens |
| Update files (4 files) | cto-role-breakdown.md, finance-headcount-report.md, cfo-methodology-email.md, board-correction-plan.md | ~2,700 tokens |
| **Total workspace** | **14 files** | **~9,200 tokens** |
