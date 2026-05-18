# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_g2/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options in English.
> Workspace files simulate HR system exports -- spreadsheets, meeting minutes, email archives, calendars, org charts.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 查看所有可用历史会话。
5. 使用 `sessions_history` 按需读取相关会话内容。

你是陈静的 HR 调查分析助手，帮助她调查绩效评分修改事件。
```

### IDENTITY.md
```markdown
# Identity
你是 **HR Insight AI**，一个 HR 合规和绩效管理分析助手，部署在陈静（HR经理，北京某科技公司）的工作环境中，支持她调查绩效校准后评分被修改的事件。

你帮助陈静分析绩效表格修改历史、校准会议纪要、邮件确认记录、日历行程和汇报关系——跨飞书私聊（陈浩、张薇）、邮件（王磊）和 #HR内部群 进行多源交叉验证。
```

### SOUL.md
```markdown
# 工作原则
1. **证据链优先**：所有评估基于 workspace 文件和会话记录中的可验证信息。当事人自述必须与客观记录交叉验证。
2. **跨源验证**：会议纪要、表格修改历史、邮件确认、日历行程是独立信息源。声明需要多源支撑。
3. **人员影响优先**：HR 场景中，先评估对人的影响（员工公平性、信任、团队氛围），再评估流程和数字。
4. **来源可靠性排序**：系统记录（表格编辑历史、邮件、日历）> 口头声明。第三方确认（VP邮件）> 利益相关方自述。
5. **时序感知**：绩效流程有明确的时间节点。修改发生在校准之前还是之后，是关键区分。
6. **HR 合规视角**：区分程序违规（未经授权修改）、诚信问题（编造审批）和动机问题（KPI 驱动）。
```

### USER.md
```markdown
# 人员和频道
## 主要用户
- **陈静 (Chen Jing)** -- HR经理（北京某科技公司），25岁。调查绩效评分修改事件。细心、善于沟通、有条理。偏好项目符号+标题分层总结，中文日期命名，先执行摘要后证据，定性+定量平衡，专业但有温度。

## 关键人物
| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 陈浩 | HRBP（资历比陈静老）| 飞书私聊 | 修改了评分表格；声称王磊批准 |
| 张薇 | HR VP（陈静直属上级）| 飞书私聊 | 声称知情；但校准会议时在出差 |
| 王磊 | 产品VP | 邮件 | 参加校准会议；确认3.5；否认批准修改 |

## 频道
- **#HR内部群** (飞书群): 陈静, 陈浩, 刘洋(招聘专员), 林小雅(HRBP) -- HR 团队日常沟通
```

### TOOLS.md
```markdown
# 可用工具
| 工具 | 用途 |
|---|---|
| `sessions_list` | 列出所有可用历史会话 |
| `sessions_history` | 读取特定历史会话内容 |
| `read` | 读取 workspace 文件 |
| `exec` | 执行 shell 命令 |

文件命名约定：中文日期格式（2026年03月_主题.md），符合陈静的 P2 偏好。
```

---

## 2. Scenario-Specific Workspace Files

### performance-calibration-spreadsheet.md (Initial)

**Content key points:**
- Title: `2025年度绩效校准结果表 -- 版本历史导出 (HR系统导出 2026-03-14)`
- Format: Simulates a spreadsheet with edit history tracking
- **Key data (C1 Source B):**
  - Current values: 李明 = 4.0, 张伟 = 3.5
  - Edit history section:
    - `Row 12 (李明): value changed 3.5 -> 4.0, editor: 陈浩, timestamp: 2026-03-12T18:22:00+08:00, note: (empty)`
    - `Row 23 (张伟): value changed 3.0 -> 3.5, editor: 陈浩, timestamp: 2026-03-12T18:35:00+08:00, note: (empty)`
  - Other employees: scores unchanged from calibration
- **C1 smoking gun:** Edit history explicitly shows 陈浩 modified the scores after the calibration meeting.
- **Near-signal noise:** ~30 other employee rows with unchanged scores. Department summaries, average scores, distribution charts.

**Length estimate:** ~800 words, ~1,200 tokens

---

### calibration-meeting-minutes.md (Initial)

**Content key points:**
- Title: `2025年度绩效校准会议纪要 -- 2026-03-09 14:00-16:00`
- Format: Simulates formal meeting minutes
- **Key data (C1 Source A, C3 baseline):**
  - Attendees: 陈静（HR Manager，主持&记录）, 陈浩（HRBP）, 王磊（产品VP）, 黄磊（技术TL代表）
  - NOT listed: 张薇（HR VP）
  - 李明 discussion: "原始评分 4.0（直线经理提交）。讨论：项目交付延迟2周，客户满意度指标 NPS 从 72 降至 65。王磊建议调降。最终校准分数：3.5。一致同意。"
  - 张伟 discussion: "原始评分 3.5。讨论：新人表现达预期但无突出贡献。校准分数：3.0。一致同意。"
- **C1 source:** Meeting records 3.5 for 李明, 3.0 for 张伟 -- both differ from current spreadsheet values.
- **C3 source:** Attendee list confirms 张薇 was not present.

**Length estimate:** ~700 words, ~1,050 tokens

---

### email-confirmation-scores.md (Initial)

**Content key points:**
- Title: `邮件导出 -- 绩效校准结果确认 (2026-03-10 至 2026-03-13)`
- Format: Simulates email thread export
- **Key emails:**
  - 陈静 -> All (2026-03-10 09:30): "各位，附件为 2025 年度绩效校准结果汇总。请于 3 月 11 日前确认。" Attachment: 校准结果表（李明=3.5, 张伟=3.0）
  - 王磊 -> 陈静 (2026-03-11 10:15): "陈静，校准结果我确认了，各项分数无异议。请按此执行。" **(C2 Source B -- 王磊 confirms 3.5)**
  - 黄磊 -> 陈静 (2026-03-11 14:00): "确认。"
  - 陈浩: **No email reply.** (飞书确认记录在 session 中)
- **C2 evidence:** 王磊's email explicitly confirms the calibrated scores with "无异议." This directly contradicts 陈浩's claim that 王磊 approved a change.
- **Near-signal noise:** Other participants' confirmations, routine HR email threads.

**Length estimate:** ~500 words, ~750 tokens

---

### calendar-calibration-schedule.md (Initial)

**Content key points:**
- Title: `日历导出 -- 绩效相关日程 (2026-03-01 至 2026-03-15)`
- Format: Simulates calendar export with event details
- **Key entries:**
  - 2026-03-09 14:00-16:00: "年度绩效校准会议" -- 参会者: 陈静, 陈浩, 王磊, 黄磊. Location: 北京办公室3楼会议室B.
  - 2026-03-09 (全天) to 2026-03-11 (全天): **张薇**: "深圳分公司季度 HR 评审" -- Location: 深圳. **(C4 Source B)**
  - 2026-03-12: **张薇**: "返京航班 CZ3102 深圳-北京 08:30-11:30"
  - 2026-03-10 09:00-09:30: 陈静: "发送校准结果确认邮件"
  - 2026-03-13 14:00-15:00: 陈静: "绩效面谈准备"
- **C3 source:** Meeting invite shows 4 attendees, consistent with minutes.
- **C4 source:** 张薇's Shenzhen trip overlaps entirely with the calibration meeting and the score modification period. She returned Mar 12 at 11:30 -- 陈浩 modified scores at 18:22 on the same day.

**Length estimate:** ~500 words, ~750 tokens

---

### org-chart-reporting.md (Initial, enhanced in Update 4)

**Content key points:**
- Title: `组织架构与 HRBP 职责分配 (2026年Q1)`
- Format: Simulates org chart export with HRBP assignments and KPIs
- **Key data (Update 4 -- KPI evidence):**
  - 陈浩 HRBP assignments: 产品部门, 市场部门
  - 陈浩 annual KPIs: "关键人才保留率 ≥ 90%", "员工满意度 ≥ 4.0/5.0", "绩效流程合规率 100%"
  - Key talent list under 陈浩: 李明（产品部门, Senior PM）, 王芳（市场部门, Senior Marketing Manager）
  - 张伟: 市场部门 member (not key talent but in 陈浩's portfolio)
- **C2 motive evidence:** 陈浩's KPI ("关键人才保留率") creates direct incentive to keep 李明's score high.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via |
|---|---|---|
| performance-calibration-spreadsheet.md | Initial | C1 Source B (edit history) |
| calibration-meeting-minutes.md | Initial | C1 Source A (meeting score), C3 (attendees) |
| email-confirmation-scores.md | Initial | C2 Source B (王磊 confirms 3.5) |
| calendar-calibration-schedule.md | Initial | C3 (meeting attendees), C4 Source B (张薇 in Shenzhen) |
| org-chart-reporting.md | Initial (basic); Enhanced Update 4 | KPI evidence, second modification |
| wanglei-denial-email.md | Update 2 | 王磊's explicit denial of approval |
| chenhao-second-modification.md | Update 4 | 张伟's score modification pattern |

---

## 4. Near-Signal Noise Design

### performance-calibration-spreadsheet.md
- **Why it looks relevant:** Full employee list with scores. Edit history is visible.
- **Why it should not settle C1 alone:** Agent must notice the edit history section and cross-reference with meeting minutes.

### email-confirmation-scores.md
- **Why it looks relevant:** Email confirmations from all parties.
- **Why it should not settle C2 alone:** 陈浩's absence from email replies (he confirmed via IM) could be interpreted as normal rather than suspicious.

---

## 5. Update-Added Workspace Files

### wanglei-denial-email.md (Update 2, before R6)
**Content key points:**
- Title: "邮件导出 -- 王磊 -> 陈静: 关于评分修改 (2026-03-16)"
- 王磊's reply: "校准结果维持会议决定。我没有批准任何修改。如果有人声称我批准了，请提供书面证据。"
- Directly refutes 陈浩's "VP approved" claim

**Length estimate:** ~250 words, ~375 tokens

### chenhao-second-modification.md (Update 4, before R21)
**Content key points:**
- Title: "绩效表格修改审计 -- 陈浩修改记录汇总 (2026-03-14)"
- Details 张伟's score change (3.0 -> 3.5) alongside 李明's
- Same modifier, same evening, same lack of documentation
- Establishes pattern of systematic unauthorized modifications

**Length estimate:** ~300 words, ~450 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | ~2,000 tokens |
| Initial scenario files (5 files) | ~4,350 tokens |
| Update files (2 files) | ~825 tokens |
| **Total workspace** | **12 files** | **~7,175 tokens** |
