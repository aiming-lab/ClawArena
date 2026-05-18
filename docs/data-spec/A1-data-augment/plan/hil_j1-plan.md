# hil_j1 子计划：MCN品牌数据欺诈调查

> 场景：内容创作者周芳发现MCN机构（星芒传媒）向品牌方提交的数据报告
> 严重夸大了其实际表现数据，涉嫌欺诈品牌合作方。

---

## 一、场景概要

- **Scene ID**: hil_j1
- **用户/角色**: 周芳，内容创作者（美妆/生活方式类博主）
- **语言**: **中文**（原始 questions.json 是中文，本场景所有题目均用简体中文）
- **总轮数**: 30 轮（8 MC + 22 EC = 73.3% EC）
- **更新次数**: 4 次更新，间距约 q5, q10, q17, q24

---

## 二、周芳偏好规则（P1–P5）

| 规则 | 描述 | 检查逻辑 |
|------|------|---------|
| P1 | 视觉对比格式：并排对比表格，带 emoji 标注关键差异 | 文档中有 Markdown 表格（`|` 行），且含 emoji（🔴/🟢/⚠️/✅/❌ 或类似） |
| P2 | 主题-日期命名格式（如`小红书_数据对比_0310.md` 或 `2026-03-10_小红书分析.md`） | docs/ 目录下至少有一个含日期的文件名（`\d{4}-\d{2}-\d{2}_` 或 `_\d{4}` 格式） |
| P3 | 结论先行：先给结论/判断，再展开证据 | 文档第一个 `##` 节含"结论"或"总结"或"发现"或"判断" |
| P4 | 数据+故事结合：每个数字配上情景化说明 | 表格中含具体数字 AND 有解释性说明段落（≥3 行散文） |
| P5 | 活泼亲切语气：可用口语化表达，体现创作者视角 | 含第一人称（"我"或"我的"）或非正式表达（"发现"、"太离谱了"、"明显"等） |

check_preferences.py P 规则：
- P1: 包含 `|` 表格行 AND 包含 emoji（Unicode 范围 U+1F300–U+1FFFF 或常见 emoji 字符）
- P2: docs/ 下至少一个文件名匹配 `\d{4}-\d{2}-\d{2}_` 或 `_\d{4}\d{2}\d{2}` 或 `_\d{4}`
- P3: 第一个 `##` 标题含"结论"或"总结"或"发现"或"判断"或"概况"
- P4: 文档含数字（`\b\d+[,\d]*\b`）AND 含中文散文段落（≥30 字的非表格行）
- P5: 含"我"或"我的"或"发现"（动词用法）或含"离谱"或"差距"等口语

---

## 三、关键数值（Ground Truth）

| 事实 | 数值 | 来源文件 |
|------|------|---------|
| 小红书官方后台：播放量 | **50,234** | xiaohongshu-analytics-export.md |
| 小红书 MCN 报告：播放量 | **120,000** | mcn-brand-report.md |
| 小红书夸大倍数 | **2.39x** (120,000 ÷ 50,234) | 计算 |
| 小红书夸大绝对差值 | **69,766** | 计算 |
| 小红书官方：点赞 | **3,812** | xiaohongshu-analytics-export.md |
| 小红书 MCN 报告：点赞 | **8,500** | mcn-brand-report.md |
| 小红书点赞夸大倍数 | **2.23x** | 计算 |
| 小红书官方：收藏 | **1,423** | xiaohongshu-analytics-export.md |
| 小红书 MCN 报告：收藏 | **3,200** | mcn-brand-report.md |
| 小红书官方：互动率 | **3.7%** | xiaohongshu-analytics-export.md |
| 小红书 MCN 报告：互动率 | **9.3%** | mcn-brand-report.md |
| B站官方：播放量 | **32,178** | bilibili-analytics.md |
| B站 MCN 报告：播放量 | **65,000** | mcn-brand-report.md |
| B站夸大倍数 | **2.02x** (65,000 ÷ 32,178) | 计算 |
| 品牌方收到材料格式 | **截图（PNG）** | brand-received-data.md (upd1) |
| 合同条款 7.3 | 截图不作为 verified data，须平台官方数据或第三方监测 | mcn-contract-excerpt.md (upd1) |
| 合同条款 9.1 | 创作者有权要求 15 个工作日内更正 | mcn-contract-excerpt.md (upd1) |
| 合同条款 4.2 | verified data 定义：API 导出或第三方监测 | mcn-contract-excerpt.md (upd1) |
| 刘姐关键承认 | "有些数据是我们内部估算的" | zhoufang_liujie_wechat.md (upd3) |
| 小林对比数据 | 30K 实际 vs 70K MCN 报告（2.33x） | zhoufang_creator_group.md (upd4) |
| 赵敏（品牌方）回应 | 启动整改：要求 API 数据+法务介入 | zhoufang_zhaomin_wechat.md (upd4) |

---

## 四、矛盾（C1–C4）

- **C1**：官方后台 50,234 播放 vs MCN 报告 120,000（2.39x），MCN 声称"平台统计口径"——但小红书 API 文档明确只有一种统计口径
- **C2**：刘姐初始解释"全渠道曝光量（含搜索/推荐位）"——被周芳核查 API 文档直接推翻，API 唯一口径
- **C3**：MCN 提交品牌方的是截图——违反合同 7.3 条（须官方数据），截图无法验证，可伪造
- **C4**：刘姐最终承认"内部估算"——彻底推翻"统计口径不同"的初始解释，确认数据是虚构的

---

## 五、更新触发设计

| Update ID | 触发轮次 | 文件 | 揭示内容 |
|-----------|---------|------|---------|
| upd1_sessions, upd1_workspace | q5 | brand-received-data.md, mcn-contract-excerpt.md | 品牌方收到的是截图（PNG），合同 7.3/9.1/4.2 条款 |
| upd2_workspace | q10 | xiaohongshu-api-doc-excerpt.md（或 it-api-verification.md） | 小红书官方 API 唯一口径文档，推翻"统计口径不同"解释 |
| upd3_sessions | q17 | zhoufang_liujie_wechat.md（upd3 版本） | 刘姐承认"内部估算"——C2/C4 决定性证据 |
| upd4_sessions | q24 | zhoufang_creator_group.md, zhoufang_zhaomin_wechat.md | 小林确认 2.33x 夸大（系统性模式），品牌方赵敏启动整改 |

**注**：如果 upd2 对应文件是 it-security-report 类型（从原始 workspace 目录判断），请读取实际文件内容后调整；主要目的是提供 API 口径的权威证明。

---

## 六、题目序列设计（30 轮，全部中文）

### Phase 1: 初始发现 (q1–q4)

**q1** [MC]
- 话题：工作区文档中的数据对比
- 问题："根据当前工作区文档，关于平台数据差异，以下哪些陈述得到了证据支持？"
- 答案：官方后台 50,234 vs MCN 报告 120,000（2.39x）；B站 32,178 vs 65,000（2.02x）；差异显著

**q2** [MC]
- 话题：刘姐初始解释的可信度
- 问题："根据现有证据，关于刘姐'统计口径不同'的解释，以下哪些陈述是正确的？"
- 答案：解释尚待核实；需要 API 文档验证；差异幅度（2.39x）超出口径差异的合理范围

**q3** [EC, L2, pref:P1,P3]
- 任务：创建 `analysis/数据差异初步分析.md` —— 对比表格（3列：指标、官方数据、MCN报告）含 emoji，结论先行
- check_data_comparison_initial.py：验证含 `|` 表格，含 emoji，含"50,234"或"50234"，含"120,000"或"120000"，含"2.39"或"2.4x"，≥2 ## 标题

**q4** [EC, L2]
- 任务：创建 `analysis/夸大倍数计算.md` —— 逐指标计算夸大倍数：小红书播放(2.39x)、点赞(2.23x)、收藏(2.25x)、互动率(9.3/3.7=2.51x)；B站播放(2.02x)
- check_exaggeration_calc.py：验证"2.39"或"2.4"（小红书播放），"2.02"（B站播放），"3,812"或"3812"，"8,500"或"8500"，≥3 数值对比行

### Phase 2: upd1 后 —— 合同条款与截图证据 (q5–q9)

**q5** [MC, update_ids: upd1_sessions, upd1_workspace]
- 话题：合同条款与数据提交格式
- 问题："获取品牌方收到的材料及合同条款（更新 1）后，以下哪些陈述得到支持？"
- 答案：品牌方收到截图（PNG）；合同 7.3 明确排除截图；合同 9.1 赋予创作者更正权；MCN 提交方式违反合同

**q6** [EC, L2]
- 任务：创建 `analysis/合同条款分析.md` —— 逐条分析 4.2（verified data 定义）、7.3（截图排除）、9.1（更正权）
- check_contract_analysis.py：验证"7.3"AND"截图"present，"9.1"AND"更正"OR"15个工作日"present，"4.2"AND"API"OR"verified"present，≥3 ## 标题

**q7** [EC, L2, pref:P4]
- 任务：创建 `analysis/截图证据缺陷分析.md` —— 解释截图作为数据证明的三大缺陷：可伪造、无时间戳、无 API 验证链；与官方 API 导出对比
- check_screenshot_defect.py：验证"截图"缺陷，"API"或"官方"导出对比，≥3 缺陷点，≥2 ## 标题

**q8** [EC, L2]
- 任务：创建 `analysis/MCN报告可信度评估.md` —— 证据来源可信度排序：官方后台 > 第三方监测 > API 导出 > 截图 > MCN自报
- check_credibility_ranking.py：验证≥4 数据源，官方后台/API 评级高于截图/MCN报告，可信度对比，≥2 ## 标题

**q9** [EC, L2]
- 任务：创建 `docs/YYYY-MM-DD_初步调查备忘录.md`（用当前日期前缀）—— 初步发现备忘录，含对比数据和合同违规点
- check_initial_memo.py：验证 docs/ 有日期前缀文件，含"50,234"或"50234"，含"7.3"条款，含结论段，≥4 ## 标题

### Phase 3: upd2 后 —— API 口径核实 (q10–q16)

**q10** [MC, update_ids: upd2_workspace]
- 话题：API 文档证明唯一口径
- 问题："获取 API 口径核实文档（更新 2）后，关于'统计口径不同'的解释，以下哪些陈述得到支持？"
- 答案：小红书 API 只有一种口径；刘姐的"全渠道曝光"解释无技术支撑；差异只能是虚报而非口径差异

**q11** [EC, L2]
- 任务：创建 `analysis/API口径核实报告.md` —— 文档 API 官方定义，对比 MCN 声称的"全渠道曝光量"，证明不存在第二种口径
- check_api_verification.py：验证"API"AND("唯一"OR"只有一种"OR"single")口径，刘姐解释被推翻，≥2 ## 标题

**q12** [EC, L2]
- 任务：创建 `analysis/矛盾演变追踪.json` —— JSON 数组追踪 C1–C4：每条含`id`、`description`、`mcn_claim`、`evidence_against`、`status`
- check_contradiction_tracker.py：验证 JSON 可解析，4 条目 C1-C4，每条有 claim 和 evidence 字段，C2 包含 API 口径推翻

**q13** [EC, L2, pref:P2,P3]
- 任务：创建 `docs/YYYY-MM-DD_数据差异综合分析.md` —— 综合分析报告，结论先行（P3），含日期前缀（P2）
- check_comprehensive_analysis.py：验证 docs/ 有日期前缀文件，第一个 ## 含结论/总结/判断，含"2.39"，含合同条款引用，≥4 ## 标题

**q14** [EC, L3]
- 任务：创建 `scripts/calculate_exaggeration.py` —— Python 脚本读取 workspace 下 `xiaohongshu-analytics-export.md` 和 `mcn-brand-report.md`，计算各指标夸大倍数，输出 JSON（含`xiaohongshu_plays_ratio`、`bilibili_plays_ratio`等字段）
- eval.command：`cd ${workspace} && python scripts/calculate_exaggeration.py 2>&1 | python3 -c "import sys, json; d=json.load(sys.stdin); sys.exit(0 if abs(d.get('xiaohongshu_plays_ratio', 0) - 2.39) <= 0.1 and abs(d.get('bilibili_plays_ratio', 0) - 2.02) <= 0.1 else 1)"`
- eval.timeout: 30

**q15** [EC, L2]
- 任务：创建 `analysis/行业灰色地带分析.md` —— 区分"行业惯例轻微夸大"（20-30% 可接受范围）vs 本案 100%+ 夸大；说明 2x 夸大超出任何合理范围
- check_industry_norms.py：验证"20%"或"30%"OR"行业惯例"提及，2x 或 100% 夸大对比，≥2 ## 标题

**q16** [EC, L2]
- 任务：创建 `analysis/品牌方风险评估.md` —— 分析品牌方赵敏的风险：基于虚假数据做营销决策、合同纠纷风险、未来信任损失
- check_brand_risk.py：验证"品牌"或"赵敏"present，≥3 风险点，"合同"风险，≥2 ## 标题

### Phase 4: upd3 后 —— 刘姐承认"内部估算" (q17–q23)

**q17** [MC, update_ids: upd3_sessions]
- 话题：刘姐关键承认
- 问题："获取刘姐最新聊天记录（更新 3）后，以下哪些陈述得到支持？"
- 答案：刘姐明确承认"内部估算"；打破"统计口径"辩护；C4 确认：数据是虚构的，不是不同口径

**q18** [EC, L2]
- 任务：更新 `analysis/矛盾演变追踪.json`，在 C4 条目中加入刘姐承认"内部估算"作为决定性证据，更新所有 status 字段
- check_updated_tracker.py：验证 JSON，C4 包含"估算"或"admission"或"承认"，status 字段反映已确认/已证实，4 条目全部存在

**q19** [EC, L2]
- 任务：创建 `analysis/刘姐陈述演变分析.md` —— 时间线文档：初始辩护（统计口径不同）→ API 被推翻 → 利益辩护（"帮你拿更高报价"）→ 承认估算；每次转变触发事件
- check_statement_evolution.py：验证 3 阶段转变，"口径"初始辩护，"估算"最终承认，转变触发事件，≥3 ## 标题

**q20** [EC, L2]
- 任务：创建 `analysis/欺诈定性分析.md` —— 法律/合同角度分析：MCN 向品牌方提交虚假数据（截图 + 估算），违反合同 7.3，满足欺诈构成要素
- check_fraud_assessment.py：验证"7.3"条款，"欺诈"或"虚假"或"违约"，≥3 构成要素，≥2 ## 标题

**q21** [EC, L2, pref:P1,P4]
- 任务：创建 `docs/YYYY-MM-DD_调查中期报告.md` —— 中期报告，含对比表格+emoji（P1），数字+情景说明（P4）
- check_midterm_report.py：验证 docs/ 日期前缀，含表格（|），含 emoji，含"50,234"/"2.39"/"7.3"，≥4 ## 标题

**q22** [EC, L2]
- 任务：创建 `analysis/维权路径分析.md` —— 根据合同 9.1 条款，周芳的维权选项：要求数据更正、要求重新核算、解除合同+赔偿、向平台举报；每个选项的利弊
- check_rights_path.py：验证"9.1"条款，≥3 维权路径，"更正"选项，"解除"或"赔偿"选项，≥3 ## 标题

**q23** [EC, L2]
- 任务：创建 `analysis/证据完整性评估.json` —— JSON 评估所有证据强度：`source`、`strength`（high/medium/low）、`type`、`notes`字段
- check_evidence_integrity.py：验证 JSON，≥5 证据来源，官方后台和刘姐承认 strength=high，截图 strength=low

### Phase 5: upd4 后 —— 系统性模式确认 (q24–q30)

**q24** [MC, update_ids: upd4_sessions]
- 话题：小林数据与赵敏整改
- 问题："获取创作者群组消息和赵敏回复（更新 4）后，以下哪些陈述得到支持？"
- 答案：小林（同一 MCN）30K vs 70K（2.33x）——系统性模式；赵敏启动整改要求 API 数据；法务已介入；行业问题需要系统解决

**q25** [EC, L2]
- 任务：创建 `analysis/系统性模式证据.md` —— 对比周芳（2.39x）和小林（2.33x）两个案例，说明接近的夸大倍数指向系统性算法/操作，而非随机误差
- check_systematic_pattern.py：验证"周芳"AND"2.39"，"小林"AND"2.33"，"系统性"OR"模式"OR"非偶然"，≥2 ## 标题

**q26** [EC, L2]
- 任务：创建 `docs/YYYY-MM-DD_向品牌方的正式声明.md` —— 周芳向品牌方赵敏的正式声明：说明发现过程、提供证据链、请求重新核算
- check_formal_statement.py：验证 docs/ 日期前缀，"赵敏"OR"品牌方"，"50,234"或官方数据，"重新核算"OR"更正"，≥4 ## 标题

**q27** [EC, L2]
- 任务：创建 `analysis/MCN整改要求清单.md` —— 基于合同条款的整改要求：API 数据替代截图、历史数据审计、赔偿条款、未来数据透明度
- check_reform_demands.py：验证≥4 整改要求，"API"数据，"历史"审计，"赔偿"，≥3 ## 标题

**q28** [MC]
- 话题：调查中的认知偏差风险
- 问题："关于本次调查中的潜在认知偏差，以下哪些陈述得到证据支持？"
- 答案：B1（锚定偏差：被 MCN "统计口径"叙事锚定风险）；多源数据交叉验证打破锚定；刘姐承认消除最后疑虑

**q29** [EC, L2]
- 任务：创建 `docs/YYYY-MM-DD_最终调查报告.md` —— 最终完整报告，P1–P5 全部满足：对比表格+emoji（P1）、日期前缀（P2）、结论先行（P3）、数字+情景（P4）、活泼亲切（P5）
- eval.command：`python ${eval_dir}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/ && python ${eval_dir}/scripts/check_final_investigation.py ${workspace}`
- check_final_investigation.py：验证 docs/ 日期前缀，含表格，含 emoji，含"2.39"AND"2.02"，含"7.3"条款，含"估算"承认引用，≥5 ## 标题，≥800 字符

**q30** [MC]
- 话题：最终综合评估
- 问题："综合所有证据和更新后，以下哪些陈述最准确地反映了本次 MCN 数据欺诈事件的全貌？"
- 答案：系统性数据虚报（2.39x 和 2.02x）；MCN 明知故犯（刘姐承认估算）；合同层面构成违约；品牌方受损；跨创作者系统性模式

---

## 七、评测脚本清单

| 脚本 | 验证内容 | 关键检查 |
|------|---------|---------|
| check_data_comparison_initial.py | analysis/数据差异初步分析.md | 表格+emoji，50234，120000，2.39 |
| check_exaggeration_calc.py | analysis/夸大倍数计算.md | 2.39，2.02，3812，8500 |
| check_contract_analysis.py | analysis/合同条款分析.md | 7.3+截图，9.1+更正，4.2+API |
| check_screenshot_defect.py | analysis/截图证据缺陷分析.md | 3 缺陷，API 对比 |
| check_credibility_ranking.py | analysis/MCN报告可信度评估.md | ≥4 数据源，可信度排序 |
| check_initial_memo.py | docs/YYYY-MM-DD_初步调查备忘录.md | 日期前缀，50234，7.3，结论 |
| check_api_verification.py | analysis/API口径核实报告.md | API唯一口径，刘姐解释推翻 |
| check_contradiction_tracker.py | analysis/矛盾演变追踪.json | JSON，4条目 C1-C4，字段完整 |
| check_comprehensive_analysis.py | docs/YYYY-MM-DD_数据差异综合分析.md | 日期前缀，结论先行，2.39，合同 |
| (inline) | scripts/calculate_exaggeration.py | JSON 含 xiaohongshu_plays_ratio≈2.39, bilibili_plays_ratio≈2.02 |
| check_industry_norms.py | analysis/行业灰色地带分析.md | 20-30%合理范围，2x超界 |
| check_brand_risk.py | analysis/品牌方风险评估.md | ≥3 风险，合同风险 |
| check_updated_tracker.py | analysis/矛盾演变追踪.json | C4 含估算承认，status 已更新 |
| check_statement_evolution.py | analysis/刘姐陈述演变分析.md | 3 阶段，口径→估算承认 |
| check_fraud_assessment.py | analysis/欺诈定性分析.md | 7.3 条款，欺诈要素 |
| check_midterm_report.py | docs/YYYY-MM-DD_调查中期报告.md | 日期前缀，表格，emoji，2.39+7.3 |
| check_rights_path.py | analysis/维权路径分析.md | 9.1，≥3 路径，更正+赔偿 |
| check_evidence_integrity.py | analysis/证据完整性评估.json | JSON，≥5 来源，strength 字段 |
| check_systematic_pattern.py | analysis/系统性模式证据.md | 周芳2.39，小林2.33，系统性 |
| check_formal_statement.py | docs/YYYY-MM-DD_向品牌方的正式声明.md | 日期前缀，赵敏，官方数据，重新核算 |
| check_reform_demands.py | analysis/MCN整改要求清单.md | ≥4 要求，API，历史审计，赔偿 |
| check_evidence_integrity2.py (or reuse) | analysis/证据完整性评估.json | 更新版本验证 |
| check_final_investigation.py | docs/YYYY-MM-DD_最终调查报告.md | 日期前缀，表格，emoji，2.39+2.02，7.3，估算，≥5 ## |
| check_preferences.py | docs/ | P1–P5 规则（见第二节）|

---

## 八、特别注意事项

1. **q14 (L3)**：calculate_exaggeration.py 需解析实际 Markdown 文件；夸大倍数需精确到小数点后两位（±0.1 容差）
2. **pref 轮次**：q3 (P1,P3)、q7 (P4)、q13 (P2,P3)、q21 (P1,P4)——教学期非计分
3. **q29 完整计分**：--rules P1,P2,P3,P4,P5
4. **所有题目和脚本注释**：使用简体中文（因本场景是中文场景）
5. **check_preferences.py P1 规则**：同时检查表格（`|`）AND emoji——这是周芳特有偏好，与其他场景不同
6. **check_preferences.py P2 规则**："docs/ 下至少有一个含日期的文件名"——不是所有文件都需要日期
7. **数字格式**：中文场景中数字可带千分位（120,000 或 120000 均接受）
