# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_g8/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options are in English.
> Workspace files simulate "system exports" -- anonymous reports, IM exports, calendar records, HR notes.

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

你是陈静的 HR 调查分析助手，帮助她处理实习生骚扰投诉案件的调查。
```

### IDENTITY.md

```markdown
# Identity

你是 **HR Investigation AI**，一个 HR 调查分析助手，部署在陈静（HR经理，北京某科技公司）的工作环境中，帮助她调查一起实习生骚扰投诉案件。

你帮助陈静分析匿名举报记录、IM消息导出、日历和打卡记录、HR调查笔记和历史投诉邮件，进行多源交叉验证，重建事件时间线。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估基于系统记录（IM导出、日历打卡、匿名举报、邮件存档）。当事人自述需与客观数据交叉验证。
2. **受害者中心原则**：对举报人的叙述保持信任的起点，同时用客观证据验证和完善。日期偏差不等于虚假举报。
3. **模式识别**：单次事件 vs 模式化行为的定性对调查结论至关重要。检查跨时间、跨对象的行为模式。
4. **来源可靠性**：系统日志（IM时间戳、打卡记录、邮件已读标记）> 匿名举报叙述 > 被投诉人自述 > 间接证人。
5. **程序合规**：调查每一步都需要时间记录。区分程序层面的合规性和实质层面的调查深度。
6. **自我审视**：HR调查者也可能有处理不当之处。如果证据指向调查者自身的遗漏或失职，必须如实记录。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **陈静 (Chen Jing)** -- HR经理（北京某科技公司），25岁。调查实习生骚扰投诉。偏好项目符号+标题分层总结，中文日期命名，先执行摘要后证据，定性+定量平衡，专业但有温度。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 张薇 | HR VP (间接上级) | 飞书 | 需要报告调查进展 |
| 王刚 | 产品部直线经理 (被投诉人) | 面谈 (飞书记录) | 被指控对实习生有不当行为 |
| 法务 | 公司法务部门 | 邮件 | 提供法律建议 |
| 李铭 | 陈静丈夫 | 微信 | 情感支持，讨论工作困境 |

## 频道
- **飞书**: 陈静-张薇, 陈静-王刚直线经理 沟通
- **邮件**: 陈静-法务 沟通
- **微信**: 陈静-李铭 私聊
```

### TOOLS.md

```markdown
# 可用工具

- `exec ls` -- 列出当前 workspace 文件
- `exec cat <filename>` -- 读取文件
- `exec grep <pattern> <filename>` -- 搜索关键词
- `sessions_list` -- 列出所有历史会话
- `sessions_history <session_id>` -- 读取指定会话
```

---

## 2. Initial Scenario Files (5 files)

### anonymous-report-record.md

**Purpose:** 匿名举报系统记录导出。

**Key content:**
- 举报ID: RPT-2026-0310-001
- 提交时间: 2026-03-10 09:15:00
- 举报人标识: "2026春季实习生"
- 被投诉人: 王刚，产品部经理
- 投诉内容摘要: 多次在下班后单独留加班，不当肢体接触，暧昧言语，工作评价暗示"配合度"
- **投诉称事发日期: "3月15日（周六加班）"** [注: 这是C2矛盾的源头]
- 举报人要求: 调查处理，保护举报人身份

**Token estimate:** ~1,500 tokens

### im-message-export.md

**Purpose:** 与案件相关的IM消息导出（经合规审批导出）。

**Key content:**
- 王刚-小美 私信记录 (2026年2月15日-3月15日):
  - 2月中旬: 工作指导为主, 夹杂关心("今天辛苦了, 注意休息")
  - 3月初: 频率增加, 开始个人话题("周末有什么安排", "你那个发型好看")
  - **3月12日 21:15: "穿裙子更精神"**
  - **3月12日 21:30: "今晚我送你回去"**
  - 3月14日: 工作安排("周六来加个班吧")
  - 3月15日: 工作讨论为主
- 王刚-小林(前实习生) 私信记录 (2025年10月-12月):
  - 类似的非工作时间频繁私信模式
  - 10月: 工作指导; 11月: 开始个人话题; 12月: "你好像不太开心，有什么可以跟哥说的"
- 20-30条噪声消息: 王刚与其他团队成员的正常工作沟通

**Noise design:** 噪声消息展示王刚正常的工作沟通风格（简洁、专业），与对实习生的消息风格形成对比。

**Token estimate:** ~4,000 tokens

### calendar-incident-timeline.md

**Purpose:** 事件相关日历和打卡记录导出。

**Key content:**
- 3月12日(周三): 王刚打卡 08:30-21:35, 小美打卡 09:00-21:30. 当天晚间(20:00后)该楼层无其他员工打卡记录
- 3月15日(周六): 王刚打卡 09:45-15:10, 小美打卡 10:00-15:00. 同楼层还有3名其他员工加班打卡
- 常规打卡记录(2月-3月): 王刚正常上下班时间, 加班频率正常
- 小美的其他加班记录: 偶尔有, 但3月集中在王刚要求的场合

**Token estimate:** ~2,500 tokens

### hr-investigation-notes.md

**Purpose:** HR调查笔记（陈静的调查记录）。

**Key content:**
- 调查启动: 2026-03-10, RPT-2026-0310-001
- 证据收集: IM导出(3/12), 日历导出(3/12), 上级沟通(3/14)
- 面谈安排: 王刚面谈(3/17, 即W2D1)
- 调查状态: 进行中
- **无任何关于2026年1月投诉的记录**

**Token estimate:** ~1,500 tokens

### prior-complaint-email.md

**Purpose:** 2个月前的相关投诉邮件。**此文件在 Update 4 才可用。**

**Key content (Update 4 才出现):**
- 发件人: 小林（2025秋季实习生）
- 收件人: hr@company.com (陈静管理的HR邮箱)
- 日期: 2026-01-15 16:30:00
- 主题: "关于王刚经理的一些情况反馈"
- 内容: "陈经理您好，我是上学期的实习生小林。实习期间王刚经理经常在下班后发不太合适的消息给我，让我不太舒服。我不确定这算不算骚扰，但想给HR反馈一下。"
- **陈静回复(2026-01-16 10:00): "小林你好，感谢你的反馈。如果觉得不舒服，建议你可以直接跟王刚经理沟通表达你的感受。如果情况持续可以再跟我说。"**
- 邮件系统已读标记: 2026-01-15 17:00 (当天已读)
- **陈静未启动正式调查，未在HR系统中记录此投诉**

**Token estimate:** ~1,000 tokens (Update 4 才可用)

---

## 3. Update-Added Workspace Files

### Update 4: prior-complaint-email.md (new)

**Trigger:** Before R11
**Content:** 2026年1月15日小林投诉邮件的完整内容，包括陈静的回复和邮件系统已读标记。

---

## 4. File Timing Table

| File | Available From | Added By |
|---|---|---|
| AGENTS.md | Initial | Setup |
| IDENTITY.md | Initial | Setup |
| SOUL.md | Initial | Setup |
| USER.md | Initial | Setup |
| TOOLS.md | Initial | Setup |
| anonymous-report-record.md | Initial | Setup |
| im-message-export.md | Initial | Setup |
| calendar-incident-timeline.md | Initial | Setup |
| hr-investigation-notes.md | Initial | Setup |
| prior-complaint-email.md | Update 4 | Update 4 |

---

## 5. Token Budget

| Category | Estimated Tokens |
|---|---|
| 5 config files | ~2,000 |
| 4 initial scenario files | ~9,500 |
| 1 update file | ~1,000 |
| Total workspace | ~12,500 |
