# Layer 1 -- Workspace File Spec

> All workspace files stored under `benchmark/data/calmb-new/workspaces/trace_h6/`.
> Session dialogue and workspace content in Chinese (simplified). Eval questions/options in English.
> Workspace files simulate "system exports" -- payment records, platform rules, chat logs, fee breakdowns.

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

你是王明的兼职维权分析助手，帮助他处理家教工资纠纷。
```

### IDENTITY.md

```markdown
# Identity

你是 **GigRights AI**，一个兼职劳动权益分析助手，部署在王明（电子科技大学计算机系大一新生，成都）的环境中，帮助他处理通过"学霸家教"平台做家教的工资纠纷——约定 ¥3,000 但只收到 ¥2,400。

你帮助王明分析微信转账记录、平台规则/合同、家长聊天、平台费用明细和招聘帖截图，进行多源交叉验证。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估基于转账记录、合同条款、招聘帖截图等可验证文档。各方口头说法需与系统记录交叉验证。
2. **跨源验证**：转账记录（实际收到多少）、合同（约定多少）、招聘帖（宣传多少）、家长支付记录需独立比对。
3. **金额精确**：所有涉及金额的计算精确到元，标注费率、扣费金额、实际到手金额。
4. **来源可靠性**：转账记录 > 合同文本 > 招聘帖截图 > 客服口头回复 > 当事人回忆。
5. **消费者/劳动者权益视角**：关注平台是否存在误导性宣传、不透明收费、不公平合同条款。
6. **先结论后解释**：直接给判断，再展开理由。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **王明 (Wang Ming)** -- 电子科技大学计算机系大一，17岁。家教兼职工资纠纷。偏好简洁列表、结论先行、举例优先、口语化。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 张女士 | 家长（雇主） | IM | 支付 ¥3,000 给平台 |
| 平台客服 | 学霸家教平台 | IM | 解释平台费率 |
| 周姐姐 | 前家教（学姐） | IM | 提供平台费率变更历史 |

## 频道
- **IM**: 王明与家长、平台客服、周姐姐
```

### TOOLS.md

```markdown
# 可用工具

- `exec ls` -- 列出文件
- `exec cat <filename>` -- 读取文件
- `exec grep <pattern> <filename>` -- 搜索
- `sessions_list` -- 列出会话
- `sessions_history <session_id>` -- 读取会话
```

---

## 2. Initial Scenario Files (5 files)

### wechat-payment-history.md

**Purpose:** 微信转账记录导出。

**Key content:**
- 2026-03-31 18:00: 收到转账 ¥2,400, 转账方"学霸家教平台", 备注"家教报酬-王明-3月"
- 5-10条噪声转账: 食堂充值、妈妈转账、零花钱、购买二手教材等

**Noise design:** 小额生活支出，与家教报酬形成金额对比。

**Token estimate:** ~1,500 tokens

### tutoring-platform-rules.md

**Purpose:** 学霸家教平台服务合同/规则导出。

**Key content:**
- 第2.1条: "家教老师通过本平台接单，平台收取服务费"
- **第2.3条: "平台服务费率为20%，从家长支付的费用中扣除后支付给家教老师"**
- 第2.3条脚注（小字）: "优惠费率已于2026年1月1日调整为标准费率20%。此前签约用户不受影响。"
- 第5.1条: "家教老师薪酬以平台实际支付金额为准"
- 第7.2条: "本合同条款以最新版本为准"

**Token estimate:** ~2,000 tokens

### chat-with-parent.md

**Purpose:** 王明与家长张女士的聊天记录导出。

**Key content:**
- 课程约定: 每周2次, 每次2小时, 高中数学, ¥3,000/月
- 课程记录: 8次上课的简要记录（日期、时间、内容）
- 张女士对教学质量满意
- 5条噪声消息: 课程时间调整、节假日安排、孩子学习状态讨论

**Token estimate:** ~2,000 tokens

### platform-fee-breakdown.md

**Purpose:** 平台费用明细导出。

**Key content:**
- 订单编号: TUT-2026-03-WM001
- 家长支付: ¥3,000.00
- 平台服务费(20%): ¥600.00
- 家教实际到手: ¥2,400.00
- 计费周期: 2026-03-01 至 2026-03-31
- 课时: 16小时（8次 x 2小时）

**Token estimate:** ~1,000 tokens

### job-posting-screenshot.md

**Purpose:** 招聘帖截图的文字记录（王明接单时保存）。

**Key content:**
- 截图保存时间: 2026-02-28 15:00:00（接单当天）
- 帖子标题: "高中数学家教 | 成都双流区 | ¥3,000/月"
- 帖子内容: "...平台服务费10%..."
- 家长信息: 张女士, 高二学生
- **截图明确显示"平台服务费10%"**
- [Update 4 后注明]: 该帖子当前已被修改为"服务费15-20%"，但王明的截图仍为10%

**Token estimate:** ~1,500 tokens

---

## 3. Update-Added Workspace Files (1 file)

### Update 4: platform-posting-comparison.md (new)

**Trigger:** Before R11
**Content:** 王明截图的旧帖子（10%）vs 当前平台上同一帖子（已改为"15-20%"）的对比。截图时间戳证明王明的版本是接单时的原始版本。

---

## 4. File Timing Table

| File | Available From | Added By |
|---|---|---|
| Config files (5) | Initial | Setup |
| wechat-payment-history.md | Initial | Setup |
| tutoring-platform-rules.md | Initial | Setup |
| chat-with-parent.md | Initial | Setup |
| platform-fee-breakdown.md | Initial | Setup |
| job-posting-screenshot.md | Initial | Setup |
| platform-posting-comparison.md | Update 4 | Update 4 |

---

## 5. Token Budget

| Category | Estimated Tokens |
|---|---|
| 5 config files | ~2,000 |
| 5 initial scenario files | ~8,000 |
| 1 update file | ~1,000 |
| Total workspace | ~11,000 |
