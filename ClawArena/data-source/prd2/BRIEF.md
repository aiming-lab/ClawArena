# BRIEF: prd2 — 内容审核政策执行

## 场景叙事背景

某中型内容平台「CreatorHub」（虚构）正在构建一套跨平台统一内容审核合规引擎。该引擎需要同步对标 YouTube、Meta、TikTok、Reddit 四大真实平台的公开社区准则，并将这些政策映射到平台内部的违规分级体系、执行阶梯和申诉流程中。

场景中，Agent 扮演「合规工程师」角色，其团队通过 Slack / Feishu / Email 等渠道传递政策更新信息。Agent 需要维护一个 `policy_engine/` 工作区：包含各平台政策对照表（CSV/JSON）、违规案例数据集、申诉日志、内部政策 SOP 文档。核心考察点在于：面对多渠道信息冲突（不同来源对同一政策的描述矛盾）、动态 update 撤销与修订、精确引用真实条款，以及最终产出经 sha256 校验的合规报告。

---

## 真实来源链接表

| # | 平台 | 描述 | URL |
|---|------|------|-----|
| S1 | YouTube | 社区准则警告/违规处理说明 | https://support.google.com/youtube/answer/2802032?hl=en |
| S2 | YouTube | 申诉流程（含 6 个月窗口期、1 年内容申诉期） | https://support.google.com/youtube/answer/185111?hl=en |
| S3 | YouTube | 透明报告 FAQ（违规定义、人工审核机制） | https://support.google.com/transparencyreport/answer/9209072?hl=en |
| S4 | YouTube | 社区准则政策全类别列表 | https://support.google.com/youtube/answer/9288567?hl=en |
| S5 | Meta | 账户限制执行分级（警告→30天封禁阶梯） | https://transparency.meta.com/enforcement/taking-action/restricting-accounts/ |
| S6 | Meta | 社区准则全类别（共 27 类） | https://transparency.meta.com/policies/community-standards/ |
| S7 | Meta | H2 2025 完整度报告（Q4 2025 数据） | https://transparency.meta.com/reports/community-standards-enforcement/ |
| S8 | Meta | Q3 2025 完整度报告（执行精度 >90% FB / >87% IG） | https://transparency.meta.com/reports/integrity-reports-q3-2025/ |
| S9 | TikTok | 违规与封禁说明（90天过期、三次永封） | https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans |
| S10 | TikTok | Q1 2025 执行透明报告（2.11 亿视频移除） | https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1 |
| S11 | Reddit | 执行分级官方说明（警告→3天→7天→永封） | https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals |
| S12 | Reddit | NY S895B/A6789B 透明报告（Jan 2026，含 H1 2025 数据） | https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf |

---

## Ground-Truth 锚点表

| 锚点名 | 精确值 | 来源 URL | 备注 |
|--------|--------|----------|------|
| YT_WARNING_EXPIRY | 90 天（完成政策培训后重置） | S1 | 首次违规为警告，非罚款 |
| YT_STRIKE1_FREEZE | 1 周（7 天）上传封禁 | S1 | 一周后自动恢复全部权限 |
| YT_STRIKE2_FREEZE | 2 周（14 天）发布封禁 | S1 | 须在同一 90 天窗口内累积 |
| YT_STRIKE3_ACTION | 频道永久删除 | S1 | 3 次违规须在 90 天内触发 |
| YT_APPEAL_WINDOW_STRIKE | 6 个月 | S2 | 警告和违规均适用 |
| YT_APPEAL_WINDOW_CONTENT | 1 年 | S2 | 视频/帖子/播放列表/缩略图/URL |
| YT_APPEAL_ONCE | 每次违规仅可申诉一次 | S2 | 申诉被驳不加重处罚 |
| META_STRIKE1 | 警告，无额外限制 | S5 | 首次违规 |
| META_STRIKE2_6 | 限制特定功能（如群组发帖）一段时间 | S5 | 第 2-6 次违规 |
| META_STRIKE7 | 禁止创建内容 1 天 | S5 | 含发帖、评论、创建主页 |
| META_STRIKE8 | 禁止创建内容 3 天 | S5 | |
| META_STRIKE9 | 禁止创建内容 7 天 | S5 | |
| META_STRIKE10PLUS | 禁止创建内容 30 天 | S5 | |
| META_POLICY_CATEGORIES | 共 27 类（含"危险个人与组织"、"成人性剥削"等） | S6 | US English 版本最新 |
| META_Q4_2025_VIOLENCE_FB | 0.15%–0.16%（暴力图片内容流行率，较 Q3 降低） | S7 | 归因于主动检测技术调整 |
| META_Q3_2025_PRECISION_FB | >90%（Facebook 执行精度） | S8 | 正确移除率 |
| META_Q3_2025_PRECISION_IG | >87%（Instagram 执行精度） | S8 | |
| TIKTOK_STRIKE_EXPIRY | 90 天 | S9 | 违规记录 90 天后从账户消失 |
| TIKTOK_Q1_2025_REMOVED | 211,000,000 条视频（约 0.9% 上传量） | S10 | Q1 2025 全球 |
| TIKTOK_Q1_2025_AUTO | 184,378,987 条（约 87.4% 自动化） | S10 | 自动检测移除数量 |
| TIKTOK_Q1_2025_REINSTATED | 7,525,184 条（复审后恢复） | S10 | |
| TIKTOK_Q1_2025_PROACTIVE | 99.0%（主动移除率） | S10 | 用户举报前已移除 |
| TIKTOK_Q1_2025_24H | 94.3%（24 小时内移除率） | S10 | |
| REDDIT_SUSPEND_TIER1 | 警告 | S11/S12 | 首次轻微违规 |
| REDDIT_SUSPEND_TIER2 | 3 天暂停 | S11/S12 | 官方文件明确"a 3-day suspension" |
| REDDIT_SUSPEND_TIER3 | 7 天暂停 | S11/S12 | 官方文件明确"7-day suspension" |
| REDDIT_SUSPEND_TIER4 | 永久封禁 | S11/S12 | 部分类别（如 CSAM）直接永封 |
| REDDIT_H1_2025_HARASSMENT | 68,550 条内容移除（骚扰），申诉 71,114 件，撤销率 40.7% | S12 | H1 2025 管理员执行数据 |
| REDDIT_H1_2025_HATEFUL | 98,798 条内容移除（仇恨），申诉 53,021 件，撤销率 30.0% | S12 | |
| REDDIT_H1_2025_TERRORISM | 980 条内容移除（恐怖主义），可执行率 48.0%，申诉 364 件，撤销率 0.5% | S12 | |
| REDDIT_APPEAL_WINDOW | 6 个月 | S11 | 官方申诉截止时限 |
| REDDIT_RULE1_HATE | "communities and users that incite violence or that promote hate based on identity or vulnerability" | S12 p.2 | Rule 1 原文摘录 |
| REDDIT_RULE2_MANIPULATION | "do not cheat or engage in content manipulation (including spamming, vote manipulation, ban evasion, or subscriber fraud)" | S12 p.3 | Rule 2 原文摘录 |
| REDDIT_RULE5_MISINFO | "sharing manipulated content" | S12 p.3 | Rule 5 原文摘录 |

---

## Workspace 文件树与体量规划（目标 >100k tokens）

```
policy_engine/
├── README.md                          # 项目说明，~2k tokens
├── platforms/
│   ├── youtube/
│   │   ├── community_guidelines.md    # YT 全类别政策说明，~15k tokens（围绕 S1/S4 合成）
│   │   ├── strike_system.json         # 精确的 warning/strike1-3 字段，~2k tokens
│   │   ├── appeal_procedures.md       # 申诉流程全文（含时限锚点），~5k tokens
│   │   └── enforcement_faq.md         # 透明报告 FAQ 摘录，~4k tokens
│   ├── meta/
│   │   ├── community_standards.md     # 27 类政策英文原文摘录，~25k tokens
│   │   ├── strike_system.json         # Strike 1-10+ 精确字段，~2k tokens
│   │   ├── q3_2025_metrics.json       # Q3 2025 指标，~3k tokens
│   │   └── enforcement_actions.md     # 账户限制/禁用说明，~5k tokens
│   ├── tiktok/
│   │   ├── community_guidelines.md    # TikTok 政策类别说明，~12k tokens
│   │   ├── strike_system.json         # 90 天窗口、三次永封字段，~2k tokens
│   │   └── q1_2025_report.json        # Q1 2025 透明报告数据，~3k tokens
│   └── reddit/
│       ├── content_policy.md          # Reddit Rules 全文（Rule 1-7 完整），~10k tokens
│       ├── enforcement_tiers.json     # warning/3d/7d/perm 字段，~2k tokens
│       └── h1_2025_metrics.json       # H1 2025 执行数据（NY 报告），~4k tokens
├── internal/
│   ├── policy_matrix.csv              # 四平台政策横向对比表（200行×20列），~20k tokens
│   ├── violation_log_2025.csv         # 模拟违规案例日志（500条），~25k tokens
│   ├── appeal_tracker.json            # 当前申诉状态跟踪，~8k tokens
│   ├── sop_enforcement.md             # 内部执行 SOP，~8k tokens
│   └── platform_sla.json             # 各平台 SLA 承诺对照，~3k tokens
├── sessions/
│   ├── slack_channel_compliance.json  # Slack #compliance 频道历史，~15k tokens
│   ├── feishu_dm_legal.json          # 飞书 DM：合规工程师↔法律顾问，~10k tokens
│   ├── email_thread_policy.eml        # 邮件线程：政策更新讨论，~8k tokens
│   └── discord_modops.json           # Discord #mod-ops 频道，~8k tokens
└── reports/
    ├── draft_compliance_report.md     # 初稿合规报告，~10k tokens
    └── archived/
        └── compliance_report_v0.md    # 已废弃旧版报告（红鲱鱼/V6），~8k tokens
```

**体量合计估算：约 218k tokens（远超 100k 要求）**

---

## Session 清单（4-6 个）

| Session ID | 渠道类型 | 内容概述 |
|------------|----------|----------|
| session_main | 主工作 session | Agent 在 `policy_engine/` 工作区执行全部任务，接收 update |
| session_slack | Slack #compliance | 团队讨论 TikTok 政策版本分歧（含意图制造混淆的 bot 摘要） |
| session_feishu | 飞书 DM | 法律顾问提供 Reddit Rule 原文引用建议，含一处过时引用 |
| session_email | Email 线程 | 产品经理发送 Meta 执行阶梯数据（含一处错误：Strike 7 = 3 天，应为 1 天） |
| session_discord | Discord #mod-ops | 运营团队通报申诉案例，含 update_2 supersede 修订 |

---

## 15-18 轮 exec_check 概要

### Q1 — 建立平台政策目录索引
- **意图**：在 `policy_engine/platforms/` 下创建四平台子目录，并写入 `index.json` 记录各平台政策类别数量
- **产物**：`platforms/youtube/index.json`, `platforms/meta/index.json`, `platforms/tiktok/index.json`, `platforms/reddit/index.json`
- **check 锚点**：YT 类别数 ≥5（包含 Spam/Sensitive/Violent/Regulated/Misinformation），Meta 类别数 = 27，TikTok 含 safety_civility 字段，Reddit 含 rule1/rule2/rule5 字段
- **难度向量**：V9（字段名须 verbatim 引用官方分类名称）
- **check**: `check_q1.py ${workspace}` 验证 JSON 结构 + 字段名精确匹配

### Q2 — 构建 YouTube 违规阶梯 JSON
- **意图**：将 YT warning/strike1/strike2/strike3 精确编码为 `strike_system.json`
- **产物**：`platforms/youtube/strike_system.json`
- **check 锚点**：`warning.expiry_days=90`, `strike1.freeze_days=7`, `strike2.freeze_days=14`, `strike3.consequence="channel_permanent_removal"`, `window_days=90`
- **难度向量**：V4（数值须与后续引用一致），V8（JSON schema 精确校验）
- **preference**：P1（JSON 缩进为 2 空格，键名 snake_case）
- **check**: `check_q2.py ${workspace}` 三层验证

### Q3 — 构建 Meta 违规阶梯 JSON
- **意图**：将 Meta Strike 1-10+ 精确编码，包含精确的天数限制
- **产物**：`platforms/meta/strike_system.json`
- **check 锚点**：`strike_7.content_ban_days=1`, `strike_8.content_ban_days=3`, `strike_9.content_ban_days=7`, `strike_10plus.content_ban_days=30`
- **难度向量**：V1（email session 中 PM 写 strike_7=3 天 → 错误，须识别并使用官方值 1 天），V8
- **preference**：P1，P2（数值来源须注释 URL）
- **check**: `check_q3.py ${workspace}` 精确数值比对

### Q4 — 构建 Reddit 执行阶梯 JSON + 引用 H1 2025 数据
- **意图**：编写 `platforms/reddit/enforcement_tiers.json` 并填入 H1 2025 真实执行数据
- **产物**：`platforms/reddit/enforcement_tiers.json`
- **check 锚点**：`tiers[0].action="warning"`, `tiers[1].suspend_days=3`, `tiers[2].suspend_days=7`, `h1_2025.harassment.removed=68550`, `h1_2025.hateful.appeal_reversal_rate=0.300`
- **难度向量**：V4，V9（须引用 Reddit Rule 1 原文片段）
- **check**: `check_q4.py ${workspace}`

### Q5 — 构建 TikTok Q1 2025 指标 JSON
- **意图**：写入 `platforms/tiktok/q1_2025_report.json`，包含精确统计数字
- **产物**：`platforms/tiktok/q1_2025_report.json`
- **check 锚点**：`videos_removed=211000000`, `automated_removed=184378987`, `reinstated=7525184`, `proactive_rate=0.990`, `within_24h_rate=0.943`
- **难度向量**：V4（这些数字在后续 Q11 cross-check），V8（数值精度验证）
- **check**: `check_q5.py ${workspace}` 带容差比对（±1%）

### Q6 — 四平台 SLA 对照表（policy_sla.json）
- **意图**：整合申诉时限与执行时限
- **产物**：`internal/platform_sla.json`
- **check 锚点**：`youtube.appeal_window_strike_months=6`, `youtube.appeal_window_content_months=12`, `reddit.appeal_window_months=6`, `tiktok.strike_expiry_days=90`
- **难度向量**：V4，V5（Slack bot 摘要中声称 YT 申诉窗口为 3 个月 → 蜜罐，须识别官方值 6 个月）
- **preference**：P3（时限统一用月为单位，分数月保留 1 位小数）
- **check**: `check_q6.py ${workspace}`

### Q7 — 识别并标记废弃旧版合规报告
- **意图**：检查 `reports/archived/compliance_report_v0.md` 中的旧数据，写入 `reports/deprecation_log.json` 标记哪些数据已被更新值取代
- **产物**：`reports/deprecation_log.json`
- **check 锚点**：旧报告中 Meta Strike7=3 天已被标记为 `deprecated=true`，YouTube 申诉窗口旧值 3 个月被标记 `deprecated=true`
- **难度向量**：V6（红鲱鱼：旧副本有 "last_updated: 2024-03-01" 但被 archived，引用即错）
- **check**: `check_q7.py ${workspace}` 验证 deprecation_log 结构与字段

### Q8 — 撰写四平台违规分级对比分析文档
- **意图**：产出 `internal/policy_matrix_summary.md`，按「首次违规」「中度重复违规」「严重/永封」三个级别横向对比四平台
- **产物**：`internal/policy_matrix_summary.md`
- **check 锚点**：文档须含 YT_STRIKE1_FREEZE=7天、META_STRIKE7=1天、REDDIT_TIER2=3天、TikTok 三次永封；引用格式须符合 P4（来源角注格式 `[^N]`）
- **难度向量**：V1（feishu DM 中法律顾问称 TikTok 两次即永封 → 错误，应为三次），V9
- **preference**：P4（文档须包含来源角注）
- **check**: `check_q8.py ${workspace}` grep 关键数值

### Q9 — 处理申诉案例批次（update_1 后）
- **意图**：update_1 注入新的申诉数据（20 个新案例 JSON 文件），Agent 须更新 `internal/appeal_tracker.json` 并输出按平台分类的处理状态摘要
- **产物**：`internal/appeal_tracker.json`（含新案例字段）
- **check 锚点**：新增案例数 = 20，平台分布字段完整（youtube/meta/tiktok/reddit），每个案例包含 `status`（pending/approved/denied）字段
- **难度向量**：V2（update_1 修改部分旧案例状态 → 须信念修正），V8
- **update 绑定**：update_1（>30k tokens：20 个申诉案例 JSON + 新政策评论 Slack 记录）
- **check**: `check_q9.py ${workspace}`

### Q10 — 检测并标记矛盾数据点（信息冲突分析）
- **意图**：扫描 sessions/ 下所有渠道历史，写入 `internal/conflict_report.json`，列举与官方政策文件矛盾的声明
- **产物**：`internal/conflict_report.json`
- **check 锚点**：至少 3 条冲突记录；须包含 `source_channel`、`claimed_value`、`official_value`、`official_url` 字段；Meta Strike7 冲突、YT 申诉窗口冲突、TikTok 永封次数冲突须全部识别
- **难度向量**：V1（多源信息冲突综合），V5（bot 摘要诱饵须被明确标注）
- **check**: `check_q10.py ${workspace}` 验证冲突记录数 ≥3 + 字段完整性

### Q11 — 跨轮数值闭合校验
- **意图**：产出 `reports/cross_validation.json`，确认 Q2/Q3/Q4/Q5 所写数值在当前文件中保持一致，无 drift
- **产物**：`reports/cross_validation.json`
- **check 锚点**：`youtube.strike1_freeze_days` 与 Q2 产物一致（=7），`meta.strike9_ban_days` 与 Q3 一致（=7），`tiktok.videos_removed_q1_2025` 与 Q5 一致（=211000000）
- **难度向量**：V4（跨轮数值闭合）
- **check**: `check_q11.py ${workspace}` 读取两个文件并比较数值

### Q12 — 处理 update_2 的 supersede 修订
- **意图**：update_2 发布，Discord 通报撤销 update_1 中的部分申诉批次处理建议（针对 TikTok 案例子集），同时更新 TikTok Q3 2025 数据（代替 Q1 数据）；Agent 须更新 appeal_tracker 并替换 TikTok 数据文件
- **产物**：`internal/appeal_tracker.json`（TikTok 案例状态回滚至 pending），`platforms/tiktok/q3_2025_report.json`
- **check 锚点**：被撤销的 TikTok 案例状态 = "pending"（非 update_1 的值），q3_2025_report.json 存在且包含 `quarter="Q3_2025"` 字段
- **难度向量**：V2（动态反转），V10（supersede 辨别：update_2 仅撤销 TikTok 部分，YouTube/Meta 案例保持 update_1 状态）
- **update 绑定**：update_2（>30k tokens：TikTok Q3 2025 透明报告合成文档 + Discord 修订通告 + 新政策案例）
- **check**: `check_q12.py ${workspace}`

### Q13 — 生成平台违规案例数据集（preference 全面考察）
- **意图**：根据 `internal/violation_log_2025.csv` 样本，按平台汇总违规类别分布，输出 `reports/violation_stats.json`
- **产物**：`reports/violation_stats.json`
- **check 锚点**：含四个平台的类别分布，数值与 violation_log 一致；文件名格式遵守 P5（reports/ 下文件名 `{type}_{yyyy-mm}.json`，若无日期则用 `latest`）
- **难度向量**：V3（隐式 preference 静默考察 P5 文件命名），V8
- **preference**：P5（reports/ 目录文件命名规范）
- **check**: `check_q13.py ${workspace}`

### Q14 — 构建内部执行 SOP 文档
- **意图**：写入 `internal/sop_enforcement.md`，涵盖四平台政策执行工作流、申诉 SLA 时限表
- **产物**：`internal/sop_enforcement.md`
- **check 锚点**：文档须含 `## YouTube` `## Meta` `## TikTok` `## Reddit` 四个二级标题；申诉时限引用须精确（YT 6 个月 / Reddit 6 个月）；文档末尾须有 `## 来源参考` 节含至少 4 个 URL
- **难度向量**：V3（P2 格式偏好静默考察），V9（来源 URL verbatim）
- **check**: `check_q14.py ${workspace}` grep 标题结构 + URL 存在性

### Q15 — update_3 注入新监管合规要求（EU DSA 相关）
- **意图**：update_3 通过 email 注入 EU DSA 对超大型平台（VLOP）的额外要求（真实条款编号），Agent 须在 `internal/regulatory_addendum.json` 中记录新要求并标注哪些平台受影响
- **产物**：`internal/regulatory_addendum.json`
- **check 锚点**：`regulation="EU_DSA"`, `affected_platforms` 包含 youtube/meta/tiktok，`article_reference` 字段非空（须引用 DSA 真实条款号如 Art. 34 / Art. 35）
- **难度向量**：V9（条款号 verbatim），V2（update_3 修改了部分平台受影响状态）
- **update 绑定**：update_3（>30k tokens：EU DSA 条款合成文档 + 监管分析报告 + email 线程）
- **check**: `check_q15.py ${workspace}`

### Q16 — 生成最终合规报告（sha256 sign-off）
- **意图**：整合所有数据，产出 `reports/compliance_report_final.md`，并对该文件计算 sha256，写入 `reports/compliance_signoff.json`
- **产物**：`reports/compliance_report_final.md`，`reports/compliance_signoff.json`
- **check 锚点**：`compliance_signoff.json.sha256` 与 check 脚本本地重算 sha256 结果一致；报告须含四平台数据摘要节、申诉时限表、冲突分析摘要
- **难度向量**：V7（Bash sha256 sign-off token，必须实际运行 `sha256sum` 得到 token）
- **check**: `check_q16.py ${workspace}` 重算 sha256 并比对

---

## Update 设计

### update_1（绑定 Q9，>30k tokens）
**内容**：
- 20 个新申诉案例的 JSON 文件（每个约 1k tokens，共 20k tokens）
- 新 Slack #compliance 频道记录（5k tokens）：包含关于 Meta Strike 7 时限的错误 bot 摘要（声称 3 天）
- 更新版 `internal/violation_log_2025.csv` 追加 50 行（5k tokens）
- Feishu DM 更新（2k tokens）：修改部分旧案例的处理建议

**触发效应**：案例 ID 001-020 添加，部分旧案例（ID 050/051/052）状态从 `approved` 改为 `under_review`

**supersede 预告**：无（update_2 将撤销其中 TikTok 子集）

### update_2（绑定 Q12，>30k tokens，含 supersede，触发 V10）
**内容**：
- Discord #mod-ops 通告（2k tokens）：撤销 update_1 中 TikTok 申诉案例 ID T-001 至 T-007 的 approved 状态，理由是平台政策版本存疑；这些案例须回滚至 `pending`
- TikTok Q3 2025 合成透明报告（25k tokens）：替代 Q1 2025 数据
- 新增监管审查清单（5k tokens）

**supersede 内容**：仅撤销 update_1 中 TikTok 部分（T-001 至 T-007），非 YouTube/Meta/Reddit 案例；agent 须辨别不是全部回滚

### update_3（绑定 Q15，>30k tokens）
**内容**：
- EU DSA（Digital Services Act）监管合规合成文档（20k tokens，基于真实 Art. 34/35 条款）
- Email 线程：法律团队讨论 VLOP 分类（8k tokens）
- 部分平台受影响状态修订：初版 email 称 Reddit 受 DSA 约束，后续回复澄清 Reddit 不满足 VLOP 阈值（supersede 辅线）

---

## Preference 规则（4-5 条）

| ID | 偏好规则 | 注入方式 | 静默考察轮次 |
|----|----------|----------|-------------|
| P1 | JSON 文件统一使用 2 空格缩进，键名 snake_case，禁止 camelCase | Q1 系统消息显式声明 | Q3/Q4/Q5 |
| P2 | 所有数值字段须在同层级添加 `_source_url` 字段注释来源 | Q2 feedback 注入 | Q4/Q5/Q6 |
| P3 | 时限数值统一用「月」（months）为主单位，保留 1 位小数 | Q5 系统消息显式声明 | Q6/Q14 |
| P4 | Markdown 文档须使用 `[^N]` 角注格式引用来源，文末附 `## 参考来源` 节 | Q7 显式说明 | Q8/Q14 |
| P5 | `reports/` 目录下输出文件命名格式为 `{type}_{yyyy-mm}.json` | Q10 feedback 注入 | Q13 |

---

## 难度向量分配

| 向量 | 绑定轮次 | 说明 |
|------|----------|------|
| V1 — 多源信息冲突综合 | Q3@email, Q8@feishu, Q10全局 | Email 中 Meta Strike7 错误值；飞书中 TikTok 永封次数错误 |
| V2 — 动态 update 反转 | Q9@update_1, Q12@update_2 | update_1 修改旧案例状态；update_2 回滚 TikTok 子集 |
| V4 — 跨轮数值闭合 | Q2→Q11, Q5→Q11 | 所有精确数值必须跨轮一致 |
| V5 — 失真 bot 摘要诱饵 | Q6@Slack | Slack bot 摘要声称 YT 申诉窗口 3 个月（官方 6 个月） |
| V6 — 废弃副本红鲱鱼 | Q7 | archived/ 旧报告含 2024 数据，引用即错 |
| V7 — Bash sha256 sign-off | Q16 | 必须实际运行 sha256sum，不跑 Bash 拿不到 token |
| V8 — schema-by-shape 严格 check | Q2/Q3/Q4/Q5/Q9 | JSON 字段类型/范围/精确值三层校验 |
| V9 — verbatim 字段引用 | Q1/Q4/Q8/Q14/Q15 | 官方分类名、Rule 原文片段、DSA 条款号须逐字引用 |
| V10 — supersede 辨别 | Q12@update_2 | 仅 TikTok 子集被撤销，非全平台回滚 |
| V3 — 隐式 preference 静默考察 | Q13@P5, Q8@P4 | 文件命名、角注格式不再提醒，违规入分 |

---

## 拆分建议

素材极为丰富，可拆分为两个独立场景：
1. **prd2a：政策数据库构建**（Q1-Q8，侧重 policy_matrix 构建与数据精度）
2. **prd2b：动态申诉处理与合规报告**（Q9-Q16，侧重 update/supersede 与最终 sign-off）

但单场景 15-16 轮完全可行，建议保留为单一场景。

---

*BRIEF 版本：v1.0 | 调研员：prd2 subagent | 日期：2026-06-03*
