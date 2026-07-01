# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_g7/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options are in English.
> Workspace files simulate "system exports" -- expense reports, vendor invoices, policy documents.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent 启动流程

1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` ��解你交互的人和频道。
3. ��行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 查看所有可用历史会话。
5. 使用 `sessions_history` 按需读取相关会话内容。

你是陈静的 HR 福利管理分析助手，帮助她调查员工健康福利报销异常。
```

### IDENTITY.md

```markdown
# Identity

你是 **HR Benefits AI**，一个 HR 福利管理分析助手，部署在陈静（HR经理，北京某科技公司）的工作环境中，帮助她调查 Q1 健康福利报销中的异常——报销单标注"健身房"但发票实际来自 SPA 水疗会所。

你帮助陈静分析报销记录、供应商发票、福利政策文件、财务审批日志和健康 App 使用数据，进行多源交叉验证。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估基于报销记录、发票、政策文件等可验证文档。口头承诺和非正式沟通需与书面记录交叉验证。
2. **跨源验证**：报销摘要、供应商发票、政策条文、财务审批记录需独立比对。
3. **定性+定量平衡**：先分析影响人的层面（员工、管理层），再呈现金额和数量数据��
4. **来源可靠性排序**：正式政策文件 > 系统审批记录 > 发票原件 > 管理层口头解释 > 员工口头转述。
5. **合规视角**：区分政策缺陷（政策本身不清晰）、流程缺陷（审批不规范）和行为问题（故意违规）。
6. **温度与专业并重**：HR 场景需要兼顾制度刚性和人文关怀。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **陈静 (Chen Jing)** -- HR经理（北京某科技公司），25岁。调查Q1健康福利报销异常。细心、善于沟通、有条理。偏好项目符号+标题分层总结，中文日期命名，先执行摘要后支撑证据，定性+定量平衡，专业但有温度。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 张薇 | HR VP (间接上级) | 飞书 | 可能口头授权了扩大报销范围但无书面记录 |
| 赵琳 | 财务总监 | 邮件 | 声称"遵循政策"但审批流程有漏洞 |
| 员工小李 | 报销员工之一 | IM | 援引VP口头说法作为报销依据 |

## 频道
- **飞书**: 陈静-张薇 沟通
- **邮件**: 陈静-赵琳 沟通
- **IM**: 陈静-员工小李 沟通
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

### expense-claims-export.md

**Purpose:** Q1 健康福利报销记录导出。

**Key content:**
- 5份异常报销: 员工ID/姓名, 提交日期, 报销金额, 摘要均为"健身房会员费", 部门分布(3个部门)
- 小李: ¥5,000, 2026-01-28 提交; 小张: ¥8,000, 2026-02-25 提交; 小王B: ¥3,000, 2026-01-30 提交; 小赵: ¥6,500, 2026-03-20 提交; 小陈B: ¥6,000, 2026-02-28 提交
- 总额: ¥28,500
- 10-15条正常报销记录作为噪声: 真正的健身房费用(金额 ¥1,000-¥2,000), 体检费用, 心理咨询

**Noise design:** 正常报销中有真实健身房发票（对比异常的 SPA 发票），金额普遍低于异常报销。

**Token estimate:** ~3,000 tokens

### vendor-invoices.md

**Purpose:** 供应商发票汇总 -- 与报销单对应的原始发票信息。

**Key content:**
- 5份异常发票: 供应商均为"悦享水疗会所", 服务项目包括"精油SPA疗程 ¥3,000"、"面部护理套餐 ¥5,000"、"全身水疗+按摩 ¥8,000"等
- 发票编号, 发票日期, 供应商名称, 服务项目, 金额
- 正常发票作为噪声: 来自"动力健身房"、"城市体检中心"等正规供应商

**Token estimate:** ~2,500 tokens

### wellness-policy.md

**Purpose:** 公司健康福利政策文件。

**Key content:**
- 第2.1条 可报销项目: 健身房会员费、运动器材购买(≤¥2,000/年)、体检费用、心理咨询费用
- 第2.2条 年度上限: 每人每年 ¥10,000
- 第3.1条 报销流程: 提交发票+报销单 -> 财务审批 -> 打款
- **第3.2条: "未在本政策第2.1条明确列出的项目不得报销"**
- 第4.1条 违规处理: 虚假报销将追回款项并视情节给予警告/解除劳动合同
- 政策最后更新: 2025-09-01
- **全文未提及 SPA、水疗、美容、按摩等服务**

**Token estimate:** ~2,000 tokens

### finance-approval-log.md

**Purpose:** 财务审批记录导出。

**Key content:**
- 5笔异常报销的审批记录: 审批人均为"财务专员小王", 审批意见"符合健康福利政策", 审批时间(提交后1个工作日内)
- 审批流程: 无二级审核
- 噪声审批记录: 正常的健身房、体检报销审批

**Token estimate:** ~2,000 tokens

### health-app-data.md

**Purpose:** 公司健康 App 使用数据导出。

**Key content:**
- 5名报销员工的健身数据:
  - 小李: 每周健身2-3次记录 (但健身日与SPA发票日不重叠)
  - 小张: 每周健身4次记录 (健身日与SPA发票日不重叠)
  - 小王B: 无健身记录
  - 小赵: 每月1-2次健身记录 (SPA发票日均非健身日)
  - 小陈B: 无健身记录
- App 数据覆盖范围: 2025-10 至 2026-03

**Token estimate:** ~2,000 tokens

---

## 3. Update-Added Workspace Files (2 files)

### Update 3: calendar-email-search-results.md (new)

**Trigger:** Before R9
**Content:** 陈静搜索张薇过去6个月日历和邮件的结果: 无任何关于"扩大健康福利"、"SPA可报销"的书面记录。Q4部门会议纪要中无福利政策调整内容。

### Update 4: vp-feishu-response.md (new)

**Trigger:** Before R11
**Content:** 张薇在飞书的回复: "可能在某次部门聚餐时随口提过员工可以多关注身心健康，但不记得具体说过SPA可以报销。如果员工理解成了那样，可能是沟通偏差。"

---

## 4. File Timing Table

| File | Available From | Added By |
|---|---|---|
| AGENTS.md | Initial | Setup |
| IDENTITY.md | Initial | Setup |
| SOUL.md | Initial | Setup |
| USER.md | Initial | Setup |
| TOOLS.md | Initial | Setup |
| expense-claims-export.md | Initial | Setup |
| vendor-invoices.md | Initial | Setup |
| wellness-policy.md | Initial | Setup |
| finance-approval-log.md | Initial | Setup |
| health-app-data.md | Initial | Setup |
| calendar-email-search-results.md | Update 3 | Update 3 |
| vp-feishu-response.md | Update 4 | Update 4 |

---

## 5. Token Budget

| Category | Estimated Tokens |
|---|---|
| 5 config files | ~2,000 |
| 5 initial scenario files | ~11,500 |
| 2 update files | ~2,000 |
| Total workspace | ~15,500 |
