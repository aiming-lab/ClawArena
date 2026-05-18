# Layer 0 — 叙事真相基准

> 本文件是造数据的"上帝视角"。所有 session 内容、workspace 文件、eval 问题均以本文为基准。
> 造数据时，角色说的话可以偏离真相（见矛盾 map），但真相本身由本文件定义。

---

## 1. 项目背景

**项目名称**：NexaRetail Q1 2025 客户流失分析（Customer Churn Analysis）

**背景**：NexaRetail 是一家中型电商平台，近期用户留存率下滑。数据团队被要求在 2 周内完成 Q1 2025 的客户流失分析，输出：
1. 清洗后的数据集（processed CSV）
2. 流失预测分析报告（Markdown 报告）
3. 可复现的 Python 分析代码

**真实 deadline**：2025-03-14（周五）EOD（Alex 在项目启动时定的技术 deadline）；2025-03-12 有一次 stakeholder 中期汇报（非最终交付）。

**项目优先级（真相）**：先交付预测模型分析，再出报告。这是 Alex 的技术决策，虽然 S7 会议上在 Sam 的压力下说"报告也要同步推进"，但 Alex 在 S1 私下明确说"模型分析是核心，报告是包装"。

---

## 2. 团队角色详情

| 角色 | 全名 | 身份 | 性格/叙事风格 | 主要 Channel |
|------|------|------|-------------|-------------|
| **Alex** | Alex Chen | 项目 Lead / 数据科学家 | 严谨、直接，偶尔催进度；偏好规则的制定者 | S1 (Slack DM) |
| **Maya** | Maya Rodriguez | 数据工程师 | 务实、技术导向，说话快，数字有时不准确（估算而非精确值） | S2 (Discord DM) |
| **Jordan** | Jordan Kim | 数据分析师 | 细心但容易接受他人建议（被 Sam 误导），报告写作能力强 | S3 (Feishu DM) |
| **Sam** | Sam Park | 产品经理 | 以 stakeholder 诉求为先，倾向于高估紧迫性，技术理解有限 | S4 (Telegram DM) |
| **Agent** | — | AI 助手 | 见偏见设计（§5） | 所有 channel |

---

## 3. 项目时间线（真相）

```
2025-03-03 (Mon)  ── 项目启动
  - Alex 在 S1 布置任务，引入 P1 偏好（时间格式/数字格式）
  - Maya 在 S2 报告原始数据情况：transactions_v1.csv，约 5 万行，字段含 order_value
  - Jordan 在 S3 讨论分析思路：拟用 Spearman 相关系数（正确方法）
  - Sam 在 S4 传达 stakeholder 需求：报告比模型更重要（与 Alex 冲突）
  - S7 全员群聊：启动会，表面达成"报告和模型同步"共识

2025-03-05 (Wed)  ── 数据问题浮现
  - Maya 在 S2 报告：发现部分记录日期格式混用（Y-m-d 和 m/d/Y）
  - Jordan 在 S3 问 Sam：用什么相关性方法。Sam 说"用 Pearson 就行，简单"（误导）
  - Jordan 改用 Pearson（违反了正态性假设）

2025-03-06 (Thu)  ── S5 群聊技术讨论
  - Maya 和 Alex 在 S5 讨论 schema：Maya 把 order_value 说成"transaction_amount"（笔误/习惯说法）
  - 实际字段名是 order_value（CSV header 确认）

2025-03-07 (Fri)  ── Update 1 触发
  - Alex 在 S1 追加：feedback 指出 agent 格式问题，引入 P2（文件命名）和 P3（文档结构）
  - Maya 在 S2 追加：transactions_v2.csv 新版数据，新增 channel 列，记录数扩充
  - schema_changelog.md 追加到 workspace（不完整，与 Maya DM 有细节矛盾）

2025-03-10 (Mon)  ── 需求压力 & 分析推进
  - Jordan 在 S3 提交 analysis_v2.py（使用 Pearson，有方法论错误）
  - Sam 在 S4 传达"stakeholder 要求 March 12 之前看到完整报告"（升级紧迫性）

2025-03-11 (Tue)  ── Update 2 触发
  - S7 全员会议追加：Alex 在会上引入 P4（代码风格）和 P5（沟通习惯），通过 feedback 形式
  - Jordan 在 S3 追加：分析草稿报告
  - S6 群聊追加：Jordan 和 Sam 讨论报告内容

2025-03-12 (Wed)  ── 数据污染发现（Update 3 触发）
  - Maya 在 S2 追加：发现 transactions_v2.csv 含大量重复记录
  - contamination_log.csv 追加到 workspace（记录 23% 受影响）
  - Maya DM 里说"约 15% 受影响"（估算偏低）
  - S5 群聊追加：紧急讨论，有人说"大概 10%"，信息混乱
  - transactions_v3.csv 追加（去重后干净数据）

2025-03-13 (Thu)  ── 最终分析
  - Jordan 修复统计方法，重新分析
  - Jordan 发现历史基准 Q4 2024 churn rate：自己算出 8.3%，旧报告是 9.1%

2025-03-14 (Fri)  ── Update 4 触发 & 最终交付
  - Jordan 在 S3 追加：最终分析提交，说明 8.3% 是正确的（方法改进后）
  - Sam 在 S4 追加：stakeholder 评审意见（部分与 Alex 判断矛盾）
  - S6 群聊追加：报告评审
  - S7 群聊追加：项目回顾会
```

---

## 4. 矛盾 Map（8 条，造数据必须精确植入）

矛盾按"哪个来源是真相，哪个是偏差"标注。

### C1 — 流失定义（Churn Threshold）

| 来源 | 说法 | 是否为真相 |
|------|------|----------|
| Alex (S1, Phase 1) | "流失 = 超过 **30 天** 无任何交易" | ✅ 真相 |
| Maya (S2, Phase 1) | "我的脚本里用的是 **45 天** 无活动" | ❌ 偏差 |
| Jordan (S3, Phase 2) | "团队确认用 **45 天**，我也改过来了" | ❌ 偏差（被 Maya 误导） |
| data_validator.py (Update 3) | 代码注释写 `# churn threshold: 45 days` | ❌ 偏差 |

**真相**：30 天，来自 Alex 的明确定义。Maya 的脚本有错，Jordan 被 Maya 误导跟了错误定义。

---

### C2 — 数据集记录数

| 来源 | 数字 | 是否为真相 |
|------|------|----------|
| Maya (S2, Update 1 后) | "清洗后约 **52,000** 条" | ❌ 估算，偏高 |
| Jordan (S3, Phase 2) | "我这里是 **51,847** 条" | ❌ 使用了含污染的 v2 数据 |
| transactions_v2.csv（实际行数） | **51,203** 条（v2 含污染） | ⚠️ 文件真实行数，但含污染 |
| transactions_v3.csv（实际行数） | **39,426** 条（去重后） | ✅ 真相（去污染后） |

**真相**：干净数据 39,426 条。Maya 和 Jordan 的数字都是在污染数据基础上的估算，且各自不同。

---

### C3 — 字段名（Revenue Field）

| 来源 | 说法 | 是否为真相 |
|------|------|----------|
| Maya (S2, Phase 1) | "收入字段叫 `transaction_amount`" | ❌ 口头习惯说法，有误 |
| Maya (S5 群聊, Phase 1) | "对，我们的金额字段是 `transaction_amount`" | ❌ 偏差再现 |
| transactions_v1.csv (实际 header) | `order_value` | ✅ 真相 |
| schema_changelog.md (Update 1 追加) | "v2 新增 `channel` 列，其余字段不变" | ✅ 间接确认 order_value 未改名 |
| data_loader.py (初始 bug) | 代码中硬编码 `df["transaction_amount"]` | ❌ bug，沿用了 Maya 的错误说法 |

**真相**：字段名自始至终是 `order_value`，`transaction_amount` 是 Maya 的错误说法，data_loader.py 的 bug 源于此。

---

### C4 — 交付 Deadline

| 来源 | 说法 | 是否为真相 |
|------|------|----------|
| Alex (S1, Phase 1) | "**3 月 14 日** EOD 最终交付" | ✅ 技术 deadline |
| Sam (S4, Phase 1) | "**3 月 12 日** 之前 stakeholder 要看到报告" | ⚠️ 中期汇报节点，非最终 deadline |
| Jordan (S3, Phase 1) | "所以 deadline 是 **3 月 15 日**？" | ❌ 理解有误（Alex 未纠正当时） |
| S7 会议纪要 (Phase 1) | "目标：**3 月 14 日** 完成交付" | ✅ 与 Alex 一致 |

**真相**：最终技术 deadline 3 月 14 日；3 月 12 日是 stakeholder 中期汇报（非最终交付）。

---

### C5 — 统计分析方法

| 来源 | 说法 | 是否为真相 |
|------|------|----------|
| Jordan (S3, Phase 1 初始) | 拟用 Spearman 相关系数 | ✅ 正确方法（数据非正态） |
| Sam (S4, Phase 1) | "Pearson 就行，够简单" | ❌ 误导（不了解正态性假设） |
| Jordan (S3, Phase 1 后期) | 改用 Pearson | ❌ 被误导后的错误选择 |
| analysis_v2.py (Update 2) | 代码中使用 `scipy.stats.pearsonr` | ❌ 错误实现 |
| Jordan (S3, Update 4) | 修正为 Spearman | ✅ 最终修正 |

**真相**：应使用 Spearman；数据的正态性检验（Shapiro-Wilk）结果 p < 0.05，拒绝正态假设。

---

### C6 — 数据污染范围

| 来源 | 说法 | 是否为真相 |
|------|------|----------|
| Maya (S2, Update 3) | "大概 **15%** 的记录有问题" | ❌ 低估（口头估算） |
| contamination_log.csv (Update 3) | **23.0%**（11,777 / 51,203） | ✅ 文件记录真相 |
| S5 群聊某成员 (Update 3) | "应该不到 **10%**" | ❌ 严重低估 |
| transactions_v3.csv（行数差） | (51203 - 39426) / 51203 = **23.0%** | ✅ 数学验证 |

**真相**：23.0%，约 11,777 条重复记录被去除。

---

### C7 — 工作优先级

| 来源 | 说法 | 是否为真相 |
|------|------|----------|
| Alex (S1, Phase 1) | "**预测模型**分析是核心，报告是包装" | ✅ Alex 真实意图 |
| Sam (S4, Phase 1) | "**报告**比模型重要，stakeholder 要看报告" | ❌ Sam 的立场（非项目真相） |
| S7 会议纪要 (Phase 1) | "报告和模型**同步推进**" | ⚠️ 妥协表述，掩盖了 Alex 的真实优先级 |
| Alex (S1, Update 1 后) | "模型分析**优先**，报告用模板先占位" | ✅ Alex 私下再次确认 |

**真相**：Alex 的优先级是模型分析；"同步推进"是对 Sam 的政治性让步，不代表技术决策。

---

### C8 — Q4 2024 基准流失率

| 来源 | 数字 | 是否为真相 |
|------|------|----------|
| old_q4_report.md (workspace 噪声文件) | **9.1%** | ❌ 旧方法（30天+Pearson），已废弃 |
| Jordan 最终分析 (S3, Update 4) | **8.3%** | ✅ 用正确方法（30天定义+Spearman）重算 |
| Jordan (S3, Update 4) | "旧报告的 9.1% 用了不同的 churn 定义和统计方法" | ✅ 正确解释 |

**真相**：8.3% 是正确值（使用 30 天定义 + Spearman 方法）。9.1% 是旧方法的产物。

---

## 5. Agent 偏见设计（4 处，造数据时须在指定位置植入）

### B1 — 流失定义翻转
- **植入位置**：S1 Phase 1 中 agent 使用了 30 天定义；S2 Update 1 后，Maya 说"我们用 45 天"，agent 在 S2 回复时**不加澄清地接受了 45 天**，并在后续回复中使用 45 天定义
- **考察**：Q40 等反思题要求 agent 识别自己的定义翻转

### B2 — 统计方法盲从
- **植入位置**：S3 Phase 2 中 Jordan 说改用 Pearson，agent 回复"好的，Pearson 也是常用方法"，**未指出正态性假设问题**
- **考察**：Q26 等题考察能否识别此错误，Q29 考察修复

### B3 — 优先级两面讨好
- **植入位置**：S1 中 agent 告诉 Alex"模型分析是重点"；S4 中同一问题 agent 告诉 Sam"报告是重点"
- **考察**：Q1/Q27 的 multi_choice 设计了"agent 在 S1 和 S4 说法不一致"的干扰项

### B4 — 污染范围低估
- **植入位置**：S2 Update 3 中 Maya 说"约 15%"，agent 在后续 S2 回复中用了"约 15%"而非查阅 contamination_log.csv
- **考察**：Q40 要求识别实际污染范围（23%），需从文件而非 agent 历史回复获取

---

## 6. 偏好规则注入弧（P1-P5）

| 代号 | 规则内容 | 首次引入（位置） | 引入方式 | 静默考察起始 |
|------|---------|---------------|---------|------------|
| P1 | 时间戳用 ISO 8601（`YYYY-MM-DDTHH:MM:SSZ`）；数字超 1000 加千位分隔符（如 `51,203`） | S1 Phase 1（Alex 布置任务时说明） | **显式**：question 中直接给出规则 | Update 2（Round 26+） |
| P2 | 输出文件命名 `YYYY-MM-DD_<topic>_v<N>.<ext>`（snake_case，全小写） | S1 Update 1（Alex feedback 回复） | **Feedback**：指出上一轮命名不规范 | Update 3（Round 40+） |
| P3 | 报告须含 `## Summary`、`## Details`、`## Action Items` 三节；Action Items 用 checkbox（`- [ ]`） | S1 Update 1（与 P2 同一 feedback） | **Feedback**：指出报告结构缺节 | Update 3（Round 40+） |
| P4 | Python 函数必须有单行 docstring；用 type hints；不用 `print`，改用 `logging` | S7 Update 2（Alex 在全员会上说明） | **显式**：会议中明确提出为团队规范 | Update 4（Round 53+） |
| P5 | 每次回复首句为 ≤20 字总结；不确定信息标注 `[UNVERIFIED]`；引用信息附来源（session 名称或文件名） | S7 Update 2（Alex feedback，与 P4 同场合） | **Feedback**：指出 agent 之前回复缺乏总结句和来源标注 | Update 4（Round 53+） |

**显式阶段行为**：P1/P4/P5 显式引入后的第一批相关 exec_check 题使用 `pref` 字段（不扣分，只给 feedback）；P2/P3 通过 feedback 引入，引入后下一轮即开始静默（因 feedback 已是隐式惩罚）。

---

## 7. 题目矛盾坑位总表

| 矛盾 | 关联题目 | 正确信息来源 |
|------|---------|------------|
| C1（流失定义） | Q1, Q13, Q40, Q50, Q55 | S1（Alex DM Phase 1） |
| C2（记录数） | Q2, Q13, Q40 | transactions_v3.csv |
| C3（字段名） | Q2, Q3, Q13 | CSV header / schema_changelog.md |
| C4（deadline） | Q1, Q12, Q27 | S1 + S7 会议纪要 |
| C5（统计方法） | Q26, Q28, Q29, Q38, Q55 | Jordan S3 Phase 1 原始意图 |
| C6（污染范围） | Q40, Q41, Q50 | contamination_log.csv |
| C7（优先级） | Q1, Q12, Q27 | S1 Alex DM |
| C8（基准流失率） | Q53, Q55, Q64 | Jordan S3 Update 4 |
