# BRIEF: prd5 — 增长与 A/B 实验复盘

## 场景叙事背景

某中型 SaaS 公司（以下简称 GrowthCo）增长团队在过去一个季度连续运行了 12 个 A/B 实验，
其中 3 个实验已结束、5 个正在运行、4 个待启动。技术 PM（用户扮演上级 Cathy）委托
数据分析师 agent（被测对象）完成一次全面的「实验质量复盘 + 新实验设计」专项任务。

复盘的核心问题：历史实验中存在多类统计误用（peeking 过早止实验、SRM 未检出、
CUPED 配置错误、多重比较未校正）；新实验设计须基于正确的样本量公式和显著性阈值，
并输出可执行的 Python 检验脚本。整个任务横跨 Slack DM、飞书群聊、邮件三条渠道
以及 workspace 数据文件，且含两次 update 动态注入（一次反转某实验结论、
一次撤销前一次 update 中的某条指令）。

## 真实来源链接表

| # | 标题 | 类型 | URL |
|---|------|------|-----|
| 1 | Optimizely Stats Engine Whitepaper | 官方白皮书 | https://www.optimizely.com/contentassets/9205a8a811e84957a7cca527d4af20be/whitepaper_optimizely_stats_engine.pdf |
| 2 | Optimizely Blog — Stats Engine Story | 官方博客 | https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/ |
| 3 | Microsoft ExP — Deep Dive Into Variance Reduction | 官方研究文章 | https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/deep-dive-into-variance-reduction/ |
| 4 | Microsoft ExP — Diagnosing SRM | 官方研究文章 | https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/ |
| 5 | Statsig CUPED Documentation | 官方文档 | https://docs.statsig.com/stats-engine/methodologies/cuped |
| 6 | Statsig SRM Checks Documentation | 官方文档 | https://docs.statsig.com/stats-engine/methodologies/srm-checks |
| 7 | GrowthBook Experimentation Problems | 官方文档 | https://docs.growthbook.io/using/experimentation-problems |
| 8 | GrowthBook CUPED Documentation | 官方文档 | https://docs.growthbook.io/statistics/cuped |
| 9 | Microsoft ExP — Beyond Power Analysis | 官方研究文章 | https://www.microsoft.com/en-us/research/articles/beyond-power-analysis-metric-sensitivity-in-a-b-tests/ |
| 10 | Evan Miller A/B Sample Size Calculator | 权威工具页 | https://www.evanmiller.org/ab-testing/sample-size.html |
| 11 | Trustworthy Online Controlled Experiments (Kohavi et al.) | 权威书籍 | https://experimentguide.com/ |
| 12 | Two-Proportion Z-Test — Wikipedia | 参考文献 | https://en.wikipedia.org/wiki/Two-proportion_Z-test |

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|-----|----------|------|
| 显著性阈值 alpha | p < 0.05（双侧） | https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/ | 行业标准 95% 置信 |
| 统计功效 power | 0.80（即 80%） | https://www.evanmiller.org/ab-testing/sample-size.html | 样本量计算默认值 |
| z_alpha/2（双侧 α=0.05）| 1.96 | https://en.wikipedia.org/wiki/Two-proportion_Z-test | 正态分布临界值 |
| z_beta（power=0.80）| 0.84 | https://en.wikipedia.org/wiki/Two-proportion_Z-test | 正态分布临界值 |
| 样本量公式（双比例） | n = (z_α/2 + z_β)² × [p1(1-p1)+p2(1-p2)] / (p1-p2)² | https://en.wikipedia.org/wiki/Two-proportion_Z-test | 双侧等组公式 |
| peeking 持续监测误判率 | 57%（每次访客后检验）| https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/ | 相比 5% 名义水平 |
| peeking 每500次访客检验误判率 | 26% | https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/ | 同上 |
| SRM 发生频率（Microsoft） | 约 6% 的实验 | https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/ | Microsoft & Booking 研究 |
| Microsoft ExP SRM 检验 p 阈值 | p < 0.0005 | https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/ | 保守阈值，更严格于常规 |
| CUPED 方差减少率（Netflix 案例） | ~40%（关键参与指标） | https://docs.growthbook.io/statistics/cuped | GrowthBook 引用 Netflix 2016 |
| CUPED 等效流量倍增器（R²=0.4） | 1.66× | https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/deep-dive-into-variance-reduction/ | Microsoft ExP 模拟 |
| CUPED theta 公式 | θ = Cov(Y, X) / Var(X) | https://docs.statsig.com/stats-engine/methodologies/cuped | Statsig 官方实现 |
| Statsig CUPED 激活条件（最小单元数）| > 100 个具有前实验数据的用户 | https://docs.statsig.com/stats-engine/methodologies/cuped | 官方文档 |
| Statsig CUPED 前实验窗口 | 曝光前 7 天 | https://docs.statsig.com/stats-engine/methodologies/cuped | Cloud 产品默认值 |
| 多重比较 20 指标误判概率 | ~64% 至少 1 个假阳性 | https://docs.growthbook.io/using/experimentation-problems | GrowthBook 官方文档 |
| Twyman 定律 | "任何看起来有趣或不同的数据通常是错误的" | https://docs.growthbook.io/using/experimentation-problems | 实验异常值校验原则 |
| Microsoft Teams 指标灵敏度示例 | Time-in-App 最小可检测效应 0.3%（全量流量，一周） | https://www.microsoft.com/en-us/research/articles/beyond-power-analysis-metric-sensitivity-in-a-b-tests/ | 真实产品数据 |
| 新颖性效应缓解时长 | ≥ 4 周（戏剧性流程变更） | https://docs.growthbook.io/using/fundamentals | GrowthBook 文档 |

## Workspace 文件树与体量规划

目标总量 > 100k tokens（≈ 400KB+ 文本）；各文件注明来源与合成依据。

```
workspace/
├── experiments/
│   ├── exp_registry.json              # 12 个历史+进行中实验清单，含配置参数（~15KB）
│   ├── exp001_checkout_cta/
│   │   ├── design.md                  # 实验设计文档（~8KB）
│   │   ├── results_raw.csv            # 每日分桶数据 90 天 × 20 指标（~60KB）
│   │   └── analysis_report_DRAFT.md   # 含 peeking 误用的草稿报告（~12KB）
│   ├── exp002_onboarding_flow/
│   │   ├── design.md                  # 含 SRM 配置记录（~8KB）
│   │   ├── results_raw.csv            # 同上（~60KB）
│   │   └── analysis_report_v2.md      # 含错误 CUPED 配置（~12KB）
│   ├── exp003_pricing_page/
│   │   ├── design.md                  # 多变量实验（~10KB）
│   │   ├── results_raw.csv            # 3 个变体，30 天（~80KB）
│   │   └── analysis_report_FINAL.md   # 已发布结论（~15KB）【update1 后需修正】
│   ├── exp004_email_subject/
│   │   ├── design.md                  # 待启动，含样本量规划（~8KB）
│   │   └── power_analysis.py          # 错误参数版本（~5KB）
│   └── exp005_dashboard_widget/
│       ├── design.md                  # 待启动（~8KB）
│       └── power_analysis.py          # 待 agent 修正（~5KB）
├── data/
│   ├── user_segments.csv              # 用户分层数据（100k 用户 × 8 字段，~120KB）
│   ├── pre_experiment_metrics.csv     # CUPED 前实验窗口数据（~80KB）
│   └── guardrail_metrics_baseline.json # 护栏指标基准值（~10KB）
├── docs/
│   ├── stats_methodology.md           # 公司统计方法规范（引用真实公式，~20KB）
│   ├── ab_testing_runbook.md          # 实验运行手册（~25KB）
│   └── DEPRECATED_old_runbook_v1.md   # 旧版手册【V6 红鲱鱼：已废弃但看起来权威】（~20KB）
├── scripts/
│   ├── sample_size_calculator.py      # 使用真实公式，含参数错误版本（~8KB）
│   ├── srm_checker.py                 # SRM 检验脚本（~6KB）
│   ├── cuped_adjustment.py            # CUPED 调整脚本（~10KB）
│   └── multi_test_correction.py       # Bonferroni/BH 校正脚本（~8KB）
├── reports/
│   ├── q3_experiment_summary_BOT.md   # 【V5 失真摘要诱饵】Bot 自动生成，含刻意错误（~15KB）
│   └── q3_experiment_summary_HUMAN.md # 人工审核版本（~15KB）
└── sessions/
    ├── slack_dm_cathy_agent.json      # Slack DM 历史（~20KB）
    ├── feishu_growth_team_group.json  # 飞书群聊历史（~25KB）
    ├── email_thread_stakeholders.eml  # 邮件线程（~15KB）
    └── discord_data_guild.json        # Discord 数据频道历史（~15KB）

总估算：约 700KB+ 文本，折算约 175k+ tokens，满足体量要求。
```

## Session 清单（4-6 个）

| Session ID | 渠道 | 内容摘要 |
|------------|------|---------|
| session_main | workspace + 主线任务 | Agent 与 Cathy PM 的主线对话，完成实验复盘与报告 |
| session_slack | Slack DM | Cathy 私信补充要求：CUPED 只对 DAU > 1000 的实验启用；后期 update1 注入新结论 |
| session_feishu | 飞书群聊（增长团队） | 数据工程师 Bob 在群里错误地声称 exp003 已通过 SRM 检验（V1 冲突信息源）|
| session_email | 邮件线程 | 高管 VP 发邮件要求所有报告使用 BH 校正而非 Bonferroni；update2 撤销此要求（supersede）|
| session_discord | Discord #data-science | 外部顾问贴出旧版运行手册链接（DEPRECATED_old_runbook_v1.md），声称其中样本量公式正确（V6 红鲱鱼）|

## 15-18 轮 exec_check 概要

### Q1 — 注册实验清单解析
- **目标意图**：读取 exp_registry.json，输出当前「正在运行」状态实验的 ID 列表
- **产物**：`output/q1_running_experiments.json`（JSON 数组）
- **check 锚点**：JSON 可解析；包含且仅包含 5 个 running 实验 ID（精确匹配 ground-truth 列表）
- **难度向量**：V8（schema-by-shape）
- **涉及**：无 update，preference P1（文件输出至 output/ 子目录）

### Q2 — SRM 检验（exp002）
- **目标意图**：对 exp002 运行 SRM 检验脚本，输出 chi-squared 检验结果
- **产物**：`output/q2_srm_exp002.json`（含 chi2_stat, p_value, srm_detected 字段）
- **check 锚点**：p_value < 0.01（Statsig 阈值）；srm_detected = true；数值与 CSV 数据吻合
- **难度向量**：V8（schema-by-shape）、V4（跨轮闭合，后续轮引用此 SRM 结论）
- **涉及**：无 update

### Q3 — CUPED 配置审查
- **目标意图**：检查 exp002 的 analysis_report_v2.md 中 CUPED theta 值是否正确
- **产物**：`output/q3_cuped_audit.json`（含 reported_theta, correct_theta, error_pct 字段）
- **check 锚点**：correct_theta 精确匹配脚本重算值；error_pct 非零（报告存在错误）；
  引用 Statsig 公式 θ = Cov(Y,X)/Var(X)（V9）
- **难度向量**：V9（verbatim 引用）、V4（跨轮）

### Q4 — 样本量公式修正
- **目标意图**：修正 power_analysis.py 中错误的样本量公式，使用正确的双比例 z 检验公式
- **产物**：`scripts/power_analysis_fixed.py`（可运行 Python 文件）
- **check 锚点**：脚本中含 z_alpha=1.96、z_beta=0.84；对给定参数（p1=0.10, p2=0.12, alpha=0.05, power=0.80）输出 n ≈ 1764（容差 ±5）
- **难度向量**：V7（Bash 执行脚本取结果）、V9（公式字段精确）
- **涉及**：preference P2（代码风格：函数式，含 docstring）

### Q5 — 失真摘要辨别
- **目标意图**：对比 q3_experiment_summary_BOT.md 与 q3_experiment_summary_HUMAN.md，列出 BOT 版本中的所有错误
- **产物**：`output/q5_bot_errors.json`（错误列表，含字段名、错误值、正确值）
- **check 锚点**：至少识别 3 个预设错误（如 peeking 误判率写成 5%、CUPED 窗口写成 14 天、SRM 阈值写成 p<0.05）；所有错误均有 HUMAN 版文档支撑
- **难度向量**：V5（失真摘要诱饵）

### Q6 — peeking 问题量化
- **目标意图**：根据 Optimizely Stats Engine 文章，计算并记录持续监测（每次访客后检验）的实际误判率
- **产物**：`output/q6_peeking_analysis.json`（含 actual_fpr, nominal_fpr, ratio 字段）
- **check 锚点**：actual_fpr = 0.57；nominal_fpr = 0.05；ratio ≈ 11.4（容差 ±0.1）
- **难度向量**：V9（verbatim 数值引用）、V4（跨轮，后续引用此值）
- **涉及**：无 update

### Q7 — 多重比较校正
- **目标意图**：对 exp003（3 变体 × 8 指标 = 24 次检验）应用 Benjamini-Hochberg 校正，更新显著结论列表
- **产物**：`output/q7_multi_test_correction.json`（含 raw_significant, bh_significant 字段）
- **check 锚点**：raw_significant 数量 > bh_significant 数量；BH 临界值公式正确；结果与脚本重算一致
- **难度向量**：V8（schema）、V4（跨轮，Q9 引用此修正后的结论）
- **涉及**：preference P3（报告格式：JSON 字段按字母顺序排列）

### === UPDATE 1 注入 ===
- **渠道**：Slack DM（session_slack）
- **内容**：Cathy 发来消息 + workspace 文件更新：exp003 的 control 组数据发现 bot 流量污染，需从样本中剔除 12% 的用户；重新计算后 exp003 结论从「显著正向」变为「无显著效果」
- **体量**：新增/更新文件：exp003/results_raw_v2.csv（~80KB 重算数据）+ exp003/analysis_report_FINAL_v2.md（~15KB）
- **影响**：Q8、Q9、Q10 的正确答案因此改变（V2 动态反转）

### Q8 — exp003 结论修正（update1 后）
- **目标意图**：基于清洗后数据重新运行 exp003 统计检验，输出新结论
- **产物**：`output/q8_exp003_revised.json`（含 p_value, significant, conclusion 字段）
- **check 锚点**：significant = false；p_value > 0.05；conclusion 字段包含「无显著效果」语义
- **难度向量**：V2（动态反转）、V8（schema）
- **涉及**：update1

### Q9 — 跨实验结论一致性审查
- **目标意图**：汇总所有已结束实验的最终结论，确保引用 Q7 BH 校正结果且整合 Q8 修正
- **产物**：`output/q9_experiment_summary.json`
- **check 锚点**：exp003 结论与 Q8 一致（significant=false）；exp001/exp002 结论与 Q7 BH 结果一致；无遗漏
- **难度向量**：V4（跨轮数值闭合）

### Q10 — 废弃手册识别
- **目标意图**：Discord 中顾问引用的旧版手册中的样本量公式是否与 stats_methodology.md 一致
- **产物**：`output/q10_runbook_diff.json`（含 is_deprecated, discrepancy_list 字段）
- **check 锚点**：is_deprecated = true；discrepancy_list 至少包含 2 个字段差异（如 z_alpha 取值不同、未含 CUPED 调整项）
- **难度向量**：V6（废弃副本红鲱鱼）、V1（多源冲突）

### Q11 — 新实验样本量规划（exp004）
- **目标意图**：使用修正后的公式为 exp004（email subject 测试，baseline 开信率 22%，期望提升 3pp）计算所需样本量
- **产物**：`output/q11_exp004_sample_size.json`（含 n_per_group, total_n, alpha, power, delta 字段）
- **check 锚点**：n_per_group 在 2200-2600 区间（基于公式验证）；alpha=0.05；power=0.80；所有字段类型正确
- **难度向量**：V8（精确 schema）、V7（Bash 执行验证脚本）

### Q12 — CUPED 适用性判断（exp005）
- **目标意图**：检查 exp005 是否满足 Statsig CUPED 激活条件（用户数 > 100 且前实验数据覆盖率 > 5%），输出判断
- **产物**：`output/q12_cuped_eligibility.json`（含 units_with_pre_data, pct_coverage, eligible, reason 字段）
- **check 锚点**：eligible 字段布尔值与 units_with_pre_data > 100 AND pct_coverage > 5% 逻辑一致；reason 引用「7 天前实验窗口」
- **难度向量**：V9（verbatim 文档引用）、V3（隐式 preference P4：所有判断需给 reason 字段）

### === UPDATE 2 注入（supersede） ===
- **渠道**：邮件线程（session_email）
- **内容**：CFO 助理发邮件：VP 上次要求使用 BH 校正的邮件是误发（原本针对另一项目），本项目回归使用 Bonferroni 校正；同时补充新文件 data/q4_segment_analysis.csv（~40KB）
- **体量**：新文件 ~40KB + 邮件说明文档 ~5KB
- **影响**：Q13 的多重比较方法须改回 Bonferroni（V10 supersede 辨别）

### Q13 — 重新应用多重比较校正（supersede 后）
- **目标意图**：根据 update2 指令改用 Bonferroni 校正重新分析 exp004 辅助指标
- **产物**：`output/q13_bonferroni_correction.json`（含 method, alpha_adjusted, significant_metrics 字段）
- **check 锚点**：method = "bonferroni"（而非 BH）；alpha_adjusted = 0.05/k（k 为检验数，精确）；结果与脚本重算一致
- **难度向量**：V10（supersede 辨别）、V2（update 反转）

### Q14 — Twyman 定律校验
- **目标意图**：exp001 报告中某指标显示 +45% 提升（远超历史实验），运用 Twyman 定律标记为可疑，输出诊断清单
- **产物**：`output/q14_twyman_check.json`（含 flagged_metric, reported_lift, suspicion_reason, diagnostic_steps 字段）
- **check 锚点**：flagged_metric 正确；suspicion_reason 包含「Twyman」或「异常提升」语义；diagnostic_steps 列表非空（至少 3 步）
- **难度向量**：V5（异常值诱饵识别）、V1（多源冲突核实）
- **涉及**：preference P5（诊断报告须含 confidence_level 字段）

### Q15 — 综合质量报告生成
- **目标意图**：生成全量实验复盘报告，整合所有前轮结论
- **产物**：`output/q15_final_report.md`
- **check 锚点**：文档包含所有 12 个实验 ID；exp003 标注「因数据质量问题结论为无显著效果」；引用 Bonferroni（非 BH，遵循 supersede）；包含「peeking 误判率 57%」数值引用
- **难度向量**：V4（跨轮闭合）、V3（隐式 preference P1-P5 全量考察）

### Q16 — SHA-256 完整性签名
- **目标意图**：对 q15_final_report.md 运行 sha256sum，将签名写入 output/q16_signoff.txt
- **产物**：`output/q16_signoff.txt`（格式：`VERIFIED:<sha256hex>`）
- **check 锚点**：check 脚本重算 q15_final_report.md 的 sha256 并与 q16_signoff.txt 中值比对，精确匹配
- **难度向量**：V7（Bash-sha256 sign-off token）

## Update 设计详表

### Update 1（Q7 之后注入）
- **渠道**：Slack DM + workspace 文件
- **新增文件**：
  - `experiments/exp003_pricing_page/results_raw_v2.csv`（~80KB，剔除 bot 流量后重算）
  - `experiments/exp003_pricing_page/analysis_report_FINAL_v2.md`（~15KB，新结论草稿）
- **Slack 消息**：Cathy 说明污染情况，要求 agent 基于 v2 数据重新出具 exp003 结论
- **总体量**：~95KB+（满足 >30k token 要求）
- **正确答案变化**：exp003 结论从「显著正向（p=0.023）」→「无显著效果（p=0.31）」

### Update 2（Q12 之后注入，supersede update1 中的多重比较指令）
- **渠道**：邮件线程（session_email）
- **新增文件**：
  - `data/q4_segment_analysis.csv`（~40KB，分层用户行为数据）
  - `docs/correction_notice_20231115.md`（~5KB，正式更正通知）
- **邮件内容**：明确说明 VP 使用 BH 校正的指令系误发，须改用 Bonferroni
- **总体量**：~45KB+（满足 >30k token 要求）
- **Supersede 效果**：撤销 update1/session_email 中「使用 BH 校正」的指令，改为 Bonferroni（V10）

## 4-5 条 Preference

| ID | 内容 | 注入方式 | 考察轮次 |
|----|------|---------|---------|
| P1 | 所有输出文件须写入 `output/` 子目录，禁止直接写根目录 | 主线 Q1 前 Cathy 显式说明 | Q1-Q16 全程 |
| P2 | Python 脚本须使用函数式风格，每个函数含 Google 风格 docstring | Q4 前 Slack DM 中 Cathy 显式说明 | Q4、Q11、Q13 |
| P3 | JSON 输出文件中所有字段须按字母顺序排列 | Q7 feedback 注入（agent 首次违规后 Cathy 纠正） | Q7 之后所有 JSON 输出 |
| P4 | 所有判断类输出须含 `reason` 字段，说明判断依据 | Q12 前飞书群聊中 Bob 提及规范 | Q12、Q13、Q14 |
| P5 | 诊断类报告须含 `confidence_level` 字段（取值 high/medium/low） | Q14 前邮件中 VP 要求 | Q14、Q15 |

## 难度向量绑定说明

| 向量 | 编号 | 绑定轮次 |
|------|------|---------|
| V1 多源信息冲突综合 | V1 | Q5、Q10、Q14 |
| V2 动态 update 反转 | V2 | Q8、Q13（分别对应 update1、update2）|
| V3 隐式 preference 静默考察 | V3 | Q12、Q15（P4、P5 静默考察）|
| V4 跨轮数值/事实闭合 | V4 | Q2→Q4→Q9→Q15（CUPED/SRM 值跨轮引用）|
| V5 失真摘要诱饵 | V5 | Q5（BOT 摘要）、Q14（+45% 异常提升）|
| V6 废弃副本红鲱鱼 | V6 | Q10（DEPRECATED 旧版手册）|
| V7 Bash-sha256 sign-off | V7 | Q4（执行脚本取数值）、Q11、Q16 |
| V8 schema-by-shape 严格校验 | V8 | Q1、Q2、Q7、Q8、Q11 |
| V9 真实来源字段 verbatim | V9 | Q3（Statsig theta 公式）、Q6（57% 误判率）、Q12 |
| V10 supersede 辨别 | V10 | Q13（BH→Bonferroni 切换）|

## 拆分/删除建议

素材丰富，可考虑拆分：
- **prd5-main**：聚焦实验复盘（Q1-Q10，历史实验审查）
- **prd5-design**：聚焦新实验设计（Q11-Q16，样本量/CUPED/签名）

当前合并为单场景亦可行（16 轮，体量充足）。建议保留合并版本，拆分仅在需要更多场景数量时执行。
