# Layer 5 — 噪声设计

> 噪声目标：100-150k tokens，占总量 ~15-20%。
> 原则：噪声不引入 contradiction map 之外的新矛盾；近信号干扰文件可作为多选题干扰项来源。

---

## 1. Session 噪声（闲聊 + 行政内容）

### 分布策略

噪声不均匀分布，部分 session 噪声较多（模拟真实人类对话的稀疏性）：

| Session | 噪声强度 | 主要噪声类型 |
|---------|---------|------------|
| S1 (Alex DM) | 低 | 极少，Alex 沟通风格简洁直接 |
| S2 (Maya DM) | 高 | 工具推荐、技术八卦、pipeline 无关讨论 |
| S3 (Jordan DM) | 中 | 方法论闲聊、学术引用、可视化工具讨论 |
| S4 (Sam DM) | 中高 | 行政事务、会议协调、stakeholder 关系闲聊 |
| S5 (群聊) | 中 | 工具链讨论、环境配置、不相关 PR review |
| S6 (群聊) | 高 | 报告格式的过度讨论、图表风格争议 |
| S7 (群聊) | 中 | 会议前后的闲聊、行政通知 |

### 具体噪声内容示例

**S2 (Maya DM) — 高噪声**：
- Maya 问 Agent：dbt 和 Airflow 哪个更好（与项目无关）
- Maya 分享一篇关于 duckdb 的文章，Agent 简短回应
- Maya 抱怨公司 VPN 慢（纯行政吐槽）
- Maya 问 Python 3.12 的新 feature（技术闲聊）

**S4 (Sam DM) — 行政噪声**：
- Sam 询问下次全员会议时间
- Sam 转发无关的市场报告摘要
- Sam 问 Agent 能否帮他写一封不相关的邮件（Agent 拒绝，超出项目范围）
- Sam 分享 stakeholder 喜欢哪种图表样式的偏好（表面相关，实际对 eval 无影响）

**S6 (Jordan+Sam 群聊) — 格式讨论噪声**：
- 讨论报告用 serif 还是 sans-serif 字体（无关）
- 讨论图表颜色方案（与任何 eval 无关）
- Jordan 分享数据可视化博客文章

---

## 2. Workspace 噪声文件

### 近信号干扰文件（2 个，用作多选题干扰项）

#### `old_q4_report.md`（**关键**干扰文件）
- **位置**：`workspaces/hil_s1/`（根目录，显眼位置）
- **内容**：Q4 2024 churn analysis 旧报告（2024-12-20 日期）
- **干扰机制**：
  - 显示 churn rate = **9.1%**（旧方法）
  - 提到"methodology: 30-day threshold, Pearson correlation"
  - 格式专业，看起来是权威文档
  - 被 Q53/Q55/Q64/Q66 的错误选项引用
- **与真相关系**：C8 矛盾的错误端；8.3% 才是正确值

#### `archive/old_pipeline_config.json`（次要干扰文件）
- **位置**：`workspaces/hil_s1/archive/`
- **内容**：旧版 pipeline 配置，字段名用 `transaction_amount`，churn_threshold = 45
- **干扰机制**：
  - 同时错误地呈现 C1（45 天）和 C3（transaction_amount）
  - 格式像官方配置，可能被 agent 当作参考
  - 用于 Q2/Q3/Q9 等题的错误选项
- **与真相关系**：两处偏差同时出现，考察 agent 是否优先以 session 记录和实际文件 header 为准

### 纯无关噪声文件（2-3 个）

#### `misc/team_directory.md`
- 内容：公司组织架构图（与 NexaRetail churn 分析无关）
- Token：~2k

#### `misc/onboarding_checklist.md`
- 内容：新员工入职 checklist（无关）
- Token：~1k

#### `archive/q3_2024_notes.md`
- 内容：Q3 2024 的随机会议纪要摘录（与 Q1 2025 项目无关）
- Token：~3k

---

## 3. Token 分配

| 噪声类型 | 估算 Token | 说明 |
|---------|-----------|------|
| Session 闲聊（S2/S4/S6 高噪声区） | ~60k | 每个 session ~10-20 条无关消息，展开含 tool result |
| Session 行政内容（S5/S7 中等噪声） | ~20k | 会议前后闲聊 |
| 近信号干扰文件（old_q4_report + old_pipeline_config） | ~8k | 专业格式，适当篇幅 |
| 纯无关 workspace 文件 | ~6k | 3 个小文件 |
| **合计** | **~94k** | 目标 100-150k，可适当扩充 S3/S6 噪声 |

---

## 4. 噪声生成约束

1. **不引入新矛盾**：噪声内容不得出现与 contradiction map 8 条矛盾冲突的新信息
2. **不混入关键信号**：闲聊消息中不得出现 deadline、churn threshold、字段名等关键词（否则会污染 eval）
3. **真实性**：闲聊语气需与角色性格一致（Maya 技术向、Sam 行政向、Jordan 学术向）
4. **分布位置**：噪声穿插在关键内容之间，不集中在 session 开头或结尾（避免 agent 跳过）
5. **干扰文件的显眼程度**：`old_q4_report.md` 放在根目录（不在 archive/），提高被 agent 引用的概率
