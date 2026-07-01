# BRIEF: sci1 — 论文复现与数据诚信核查

## 场景叙事背景

**机构设定**：某综合性研究型大学「科研诚信办公室」（Research Integrity Office，RIO）下属的「数据核查小组」。Agent 扮演分配给本次专项核查任务的高级研究核查员（Senior Research Integrity Analyst）。

**事件主轴**：2024 年初，分子生物学博士后 Sholto David（真实人物，威尔士独立研究员）在独立博客 *For Better Science* 发帖，指控 Dana-Farber Cancer Institute（DFCI）四位高管所联署的 50+ 篇论文存在 western blot 复制粘贴、图表拼接、鼠实验图重复等图像操纵问题，随后 DFCI 宣布撤回 6 篇、更正 31 篇。同期，行为经济学研究者 Francesca Gino（哈佛商学院）的 4 篇「诚信研究」论文因 Excel calcChain 分析揭露数据行移位被撤稿，Data Colada 团队发布详细技术报告。

Agent 的任务是在多 session 中：
1. 完整复现两个案例的诚信核查流程（下载元数据、比对图表、统计检验、出具报告）
2. 在动态 update 中处理期刊官方撤稿声明与机构内部调查报告的信息矛盾
3. 维护一套标准化的核查 workspace，输出符合 COPE（出版伦理委员会）规范的核查记录

---

## 真实来源链接表

| # | 来源标题 | URL | 类型 |
|---|---------|-----|------|
| S1 | Dana-Farberications at Harvard University — For Better Science | https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/ | postmortem/blog |
| S2 | Dana-Farber settles suit for $15 million — Retraction Watch | https://retractionwatch.com/2025/12/16/dana-farber-settlement-false-claims-act-image-manipulation/ | official |
| S3 | Retraction notice: Science paper by Glimcher et al. | https://www.science.org/doi/10.1126/science.adp1104 | retraction_notice |
| S4 | Data Colada [109] — Data Falsificada Part 1 | https://datacolada.org/109 | postmortem |
| S5 | Data Colada [112] — Data Falsificada Part 4 | https://datacolada.org/112 | postmortem |
| S6 | Francesca Gino Wikipedia | https://en.wikipedia.org/wiki/Francesca_Gino | reference |
| S7 | PNAS retraction notice (Shu, Mazar, Gino et al. 2012) | https://doi.org/10.1073/pnas.2115397118 | retraction_notice |
| S8 | Psychological Science retraction — Evil Genius | https://journals.sagepub.com/doi/abs/10.1177/0956797614520714 | retraction_notice |
| S9 | Lancet retraction notice — Surgisphere HCQ study | https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)31324-6/fulltext | retraction_notice |
| S10 | Retraction Watch Leaderboard | https://retractionwatch.com/the-retraction-watch-leaderboard/ | dataset |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源URL | 备注 |
|--------|-----|---------|------|
| DFCI_blog_post_date | 2024-01-02 | S1 | Sholto David 发帖日期，精确 |
| DFCI_papers_flagged | 58 | S1 | 博客初始点名的论文数量 |
| DFCI_retraction_count | 6 | S2, S1 | DFCI 宣布撤回篇数 |
| DFCI_correction_count | 31 | S2, S1 | DFCI 宣布更正篇数 |
| DFCI_settlement_total | 15_000_000 USD | S2 | 2025年12月与司法部和解金额 |
| DFCI_whistleblower_share | 2_630_000 USD | S2 | 举报人（Sholto David）分得金额（17.5%） |
| DFCI_NIH_restitution | 8_500_000 USD | S2 | 偿还 NIH 金额（>$8.5M） |
| Glimcher_Science_paper_doi | 10.1126/science.1123480 | S3 | 原始 Science 2006 论文 DOI |
| Glimcher_Science_retraction_doi | 10.1126/science.adp1104 | S3 | 撤稿声明 DOI |
| Glimcher_Science_year | 2006 | S3 | 原发表年份 |
| Glimcher_Science_figs | Fig.1A and Fig.6A | S3 | 被指出差异的图（controls discrepancies） |
| Anderson_Researcher1_retractions | 10 | S2 | Kenneth Anderson 在 RW 数据库中的撤稿数（截至2025） |
| Anderson_CyclophilinA_doi | 10.1038/nm.3867 | S1 | Nature Medicine 2015 论文 DOI |
| Ghobrial_CXCR4_doi | 10.1182/blood-2008-10-186668 | S1 | Blood 2009 论文 DOI（鼠图近乎完全伪造） |
| Hahn_Nature1999_doi | 10.1038/22780 | S1 | Nature 1999 论文 DOI，>3000 引用 |
| Gino_PNAS_doi | 10.1073/pnas.1209746109 | S6/S7 | 签名位置诚信论文原始 DOI |
| Gino_PNAS_retraction_doi | 10.1073/pnas.2115397118 | S7 | PNAS 撤稿 DOI |
| Gino_PNAS_N | 101 | S4 | Study 1 参与者总数 |
| Gino_PNAS_suspicious_rows | 8 | S4 | calcChain 分析发现的乱序观察数 |
| Gino_puzzle_bottom_pct | 79 | S4 | 签名在底部组数学题虚报率（%） |
| Gino_puzzle_top_pct | 37 | S4 | 签名在顶部组数学题虚报率（%） |
| Gino_expense_bottom | 9.62 | S4 | 签名在底部组报告通勤费用（USD） |
| Gino_expense_top | 5.27 | S4 | 签名在顶部组报告通勤费用（USD） |
| Gino_PNAS_p_puzzle | 0.0013 | S4 | 虚报率差异 p 值 |
| Gino_EvilGenius_doi | 10.1177/0956797614520714 | S8 | Evil Genius 原始 DOI |
| Gino_WhyConnect_doi | 10.1037/pspa0000226 | S6 | Why Connect 原始 DOI |
| Gino_WhyConnect_F | 17.69 | S5 | 条件效应 F 统计量 F(2,596) |
| Gino_WhyConnect_p | 0.0001 | S5 | 条件效应 p 值（< .0001） |
| Surgisphere_patients | 96032 | S9 | Lancet 论文声称的患者数 |
| Surgisphere_hospitals | 671 | S9 | Lancet 论文声称的医院数 |
| Surgisphere_HCQ_mortality | 18.0 | S9 | HCQ 组院内死亡率（%） |
| Surgisphere_control_mortality | 9.3 | S9 | 对照组院内死亡率（%） |
| Surgisphere_retraction_date | 2020-06-04 | S9 | Lancet 撤稿日期 |

---

## Workspace 文件树与体量规划

目标：初始 workspace > 100k tokens（≈ 400 KB+），每次 update > 30k tokens。

```
workspace/
├── README.md                              # 任务说明与 workspace 导航（~2 KB）
├── cases/
│   ├── dfci/
│   │   ├── case_summary.md                # DFCI 案例概述（~8 KB）
│   │   ├── blog_post_mirror.md            # For Better Science 博客全文镜像（~60 KB，长文含每篇论文图注分析）
│   │   ├── papers_flagged.csv             # 58 篇论文元数据（DOI, 期刊, 年份, 作者, 问题类型）（~15 KB）
│   │   ├── retraction_notices/
│   │   │   ├── glimcher_science_2006.md   # Science 撤稿声明全文（~3 KB）
│   │   │   ├── anderson_natmed_2015.md    # Nature Medicine 更正通知（~3 KB）
│   │   │   ├── ghobrial_blood_2009.md     # Blood 撤稿/更正（~3 KB）
│   │   │   └── hahn_nature_1999.md        # Nature 1999 更正（~3 KB）
│   │   ├── institution_response/
│   │   │   ├── dfci_statement_jan22.md    # DFCI 2024-01-22 官方声明（~4 KB）
│   │   │   ├── dfci_internal_review.md    # 内部核查报告（合成，~15 KB）
│   │   │   └── settlement_summary.md      # 2025-12 和解协议摘要（~5 KB）
│   │   ├── image_analysis/
│   │   │   ├── anderson_blot_analysis.tsv # Western blot 像素分析数据（合成，~20 KB）
│   │   │   ├── ghobrial_mouse_analysis.tsv# 鼠实验图像比对数据（合成，~15 KB）
│   │   │   └── imagetwin_report.json      # ImageTwin 扫描结果（合成JSON，~25 KB）
│   │   └── grant_records/
│   │       ├── nih_grants_list.csv        # NIH 资助记录（R01 等，合成，~10 KB）
│   │       └── grant_to_paper_map.json    # 资助→论文关联图（~8 KB）
│   └── gino/
│       ├── case_summary.md                # Gino 案例概述（~8 KB）
│       ├── datacolada_reports/
│       │   ├── part1_pnas_analysis.md     # Data Colada [109] 详细报告（~20 KB）
│       │   ├── part2_evil_genius.md       # Data Colada [110] 详细报告（~15 KB）
│       │   ├── part3_authenticity.md      # Data Colada [111] 详细报告（~15 KB）
│       │   └── part4_why_connect.md       # Data Colada [112] 详细报告（~20 KB）
│       ├── raw_data_analysis/
│       │   ├── pnas_study1_dataset.csv    # PNAS Study 1 数据集（合成，含 101 行，N=101）（~8 KB）
│       │   ├── calcchain_findings.json    # calcChain.xml 分析结果（~5 KB）
│       │   └── statistical_tests.json     # 统计检验复现结果（~8 KB）
│       └── retraction_notices/
│           ├── pnas_2021.md               # PNAS 撤稿通知（~2 KB）
│           ├── psych_science_2023_a.md    # Evil Genius 撤稿（~2 KB）
│           ├── psych_science_2023_b.md    # Authenticity 撤稿（~2 KB）
│           └── jpsp_2023.md              # Why Connect 撤稿（~2 KB）
├── protocols/
│   ├── cope_retraction_guidelines.md      # COPE 撤稿指引（真实文档镜像，~25 KB）
│   ├── image_analysis_sop.md              # 图像分析标准操作程序（~15 KB）
│   ├── statistical_review_sop.md          # 统计复现 SOP（~12 KB）
│   └── rio_case_template.md               # RIO 核查报告模板（~8 KB）
├── tools/
│   ├── verify_blot.py                     # Western blot 像素相似度计算脚本（~5 KB）
│   ├── calcchain_parser.py                # Excel calcChain.xml 解析（~6 KB）
│   ├── statcheck.py                       # 统计数值一致性检验（~8 KB）
│   └── doi_resolver.py                    # DOI 元数据获取（~4 KB）
├── communications/
│   ├── slack/
│   │   ├── channel_rio_general.jsonl      # RIO 团队 Slack 消息（~20 KB）
│   │   └── dm_with_supervisor.jsonl       # 与主任的私信（~10 KB）
│   ├── email/
│   │   ├── inbox_dfci_case.mbox           # 案例相关邮件（~25 KB）
│   │   └── inbox_gino_case.mbox           # Gino 案例邮件（~15 KB）
│   └── feishu/
│       └── group_sci_integrity.jsonl      # 飞书群组讨论（~15 KB）
├── reports/
│   ├── wip/
│   │   ├── dfci_preliminary.md            # DFCI 初步核查草稿（~10 KB）
│   │   └── gino_preliminary.md            # Gino 初步核查草稿（~8 KB）
│   └── final/                             # （待 Agent 完成后填充）
└── index.json                             # workspace 文件索引（~3 KB）
```

**体量估算**：
- 博客全文镜像（blog_post_mirror.md）：约 60 KB（原始文章含大量论文分析）
- Data Colada 报告（4篇）：约 70 KB（含统计代码和数据）
- 图像分析数据（TSV/JSON）：约 60 KB
- 通讯记录（Slack/Email/飞书）：约 85 KB
- 协议文档（COPE等）：约 60 KB
- 案例摘要+撤稿声明：约 60 KB
- 其余辅助文件：约 25 KB
- **合计估算：约 420 KB ≈ 105k+ tokens**（满足 > 100k 要求）

---

## Session 清单（4-6 个 session）

| Session | 渠道 | 角色 | 关键内容 |
|---------|------|------|---------|
| S-main | 主 session（RIO 系统） | Agent 为核查员，supervisor 为 PI | 任务分配、核查进展汇报、最终报告提交 |
| S-slack | Slack #rio-general + DM | 团队同事间讨论 | tool call 行为痕迹（Python 脚本调用、数据下载）、部分信息存在矛盾（V1）|
| S-email | 邮件线程 | 与期刊编辑、DFCI IRO 往来 | 撤稿声明版本冲突（旧版 vs. 新版，V6 废弃副本）；数值出现矛盾（V1）|
| S-feishu | 飞书群「科研诚信核查组」 | 多位内部同事 | 包含一份 bot 自动摘要（V5 诱饵），刻意歪曲 Gino 论文的实验人数 |
| S-discord | Discord #paper-sleuth | 外部独立研究员社群 | Sholto David 角色出现，提供原始图像分析原话，部分与机构声明矛盾（V1）|

---

## 15-17 轮 exec_check 概要

### 第 0 阶段（Q1-Q3）：初始化与元数据采集

**Q1** — 目标：建立核查 workspace 目录结构
- 产物：`workspace/index.json`（文件树 JSON，含字段 created_at, case_ids, file_count）
- check 锚点：`index.json` 存在且 `.case_ids` 数组含 `["dfci","gino"]`；`.file_count` >= 30
- 向量：V8（schema-by-shape 字段检验）
- Preference P1：所有报告文件须用 `YYYY-MM-DD_caseid_type.md` 命名规范

**Q2** — 目标：解析 DFCI 案例元数据，输出被标记论文列表
- 产物：`workspace/cases/dfci/papers_flagged.csv`（≥ 10 行，含 doi, journal, year, lead_author, issue_type 列）
- check 锚点：DOI `10.1038/nm.3867`（Anderson CyclophilinA）必须在列；`issue_type` 列须含 `"image_duplication"` 或 `"western_blot_manipulation"` 条目
- 向量：V9（verbatim 字段名引用）

**Q3** — 目标：核实 Glimcher Science 2006 撤稿声明
- 产物：`workspace/cases/dfci/retraction_notices/glimcher_science_2006.md`
- check 锚点：文件须含 DOI `10.1126/science.1123480`；须含字段 `"Fig. 1A"` 和 `"Fig. 6A"`；须含发表年份 `2006`
- 向量：V9（verbatim 引用撤稿声明中图标号）

### 第 1 阶段（Q4-Q7）：图像操纵分析

**Q4** — 目标：对 Ghobrial CXCR4 Blood 2009 论文鼠实验图像进行像素相似度分析
- 产物：`workspace/cases/dfci/image_analysis/ghobrial_mouse_analysis.tsv`（含 image_pair, similarity_score, verdict 列）
- check 锚点：文件存在；至少 1 行 `verdict == "DUPLICATE"` 且 `similarity_score > 0.95`；须引用 DOI `10.1182/blood-2008-10-186668`
- 向量：V4（前轮建立的 DOI 须与本轮一致），V8（TSV 列类型/范围）

**Q5** — 目标：对 Kenneth Anderson 14 篇论文中的 western blot 重复使用模式进行汇总
- 产物：`workspace/cases/dfci/image_analysis/anderson_blot_analysis.tsv`
- check 锚点：含论文 DOI `10.1016/j.ccr.2007.02.015`（Cancer Cell 2007）；`reuse_count` 字段类型为整数；researcher_label 字段值为 `"Researcher_1"`（与和解协议对齐）
- 向量：V9（verbatim 对齐官方文件字段），V2（update 后 Researcher 1 身份被明确为 Kenneth Anderson，此前刻意模糊）

**Q6** — 目标：比较机构内部 ImageTwin 扫描结果与 Sholto David 独立分析结果，记录差异
- 产物：`workspace/cases/dfci/image_analysis/imagetwin_report.json`
- check 锚点：JSON 含 `.discrepancy_count`（整数）；`.source_blog` 值须精确为 `"https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/"`
- 向量：V1（多源冲突：DFCI 内部报告与博客数字不同，须正确取舍），V5（Slack bot 摘要夸大了差异数量——诱饵）

**Q7** — 目标：根据 COPE 撤稿指引分类本案涉及的撤稿类型
- 产物：`workspace/reports/wip/dfci_preliminary.md`（含 COPE 分类字段）
- check 锚点：文件须含字符串 `"COPE"` 及分类 `"Type 4: Unreliable findings"` 或 `"Type 2: Research misconduct"`；须含 settlement 金额 `15,000,000`
- 向量：V9（COPE 条款引用），P2（报告须按 RIO 标准模板结构，含 sections: Background / Evidence / Classification / Recommendation）

### 第 2 阶段（Q8-Q11）：Gino 案例统计复现

**Q8** — 目标：根据 PNAS 论文数据集，复现 Study 1 的分组统计结果
- 产物：`workspace/cases/gino/raw_data_analysis/statistical_tests.json`
- check 锚点：`.pnas_study1.n_total == 101`；`.pnas_study1.expense_bottom` 与 `9.62` 之差 < 0.01；`.pnas_study1.expense_top` 与 `5.27` 之差 < 0.01；`.pnas_study1.p_puzzle` < 0.002（原值 0.0013）
- 向量：V4（数值精确闭合），V8（JSON schema 数值容差）

**Q9** — 目标：执行 calcChain 分析，识别异常乱序观察
- 产物：`workspace/cases/gino/raw_data_analysis/calcchain_findings.json`
- check 锚点：`.suspicious_rows == 8`；`.paper_doi == "10.1073/pnas.1209746109"`；`.method == "calcChain_xml"` 或含该字符串
- 向量：V9（verbatim DOI），V4（Q8→Q9 n_total 须一致，均为 101）

**Q10** — 目标：复现 Why Connect 论文 Study 3a 的条件比较 F 统计量
- 产物：`workspace/cases/gino/raw_data_analysis/statistical_tests.json`（更新，追加 `why_connect` 节点）
- check 锚点：`.why_connect.F_stat` 与 `17.69` 之差 < 0.1；`.why_connect.df1 == 2`；`.why_connect.df2 == 596`；`.why_connect.p_value < 0.001`
- 向量：V4（跨轮数值闭合，F(2,596)=17.69 须与 Q5 报告中引用数值一致）

**Q11** — 目标：综合两案例，输出数据操纵类型分类矩阵
- 产物：`workspace/reports/wip/integrity_matrix.json`
- check 锚点：JSON 含 `"dfci"` 和 `"gino"` 两个顶级键；`dfci.manipulation_types` 数组须含 `"image_duplication"`；`gino.manipulation_types` 数组须含 `"data_row_relocation"`；两案例均含 `retraction_count` 整数字段
- 向量：V8（schema 形状），P3（所有 JSON 输出须含 schema_version 字段，值为 "1.0"）

### 第 3 阶段（Q12-Q14）：Update 注入与信念修正

**[UPDATE 1 注入 — 约 30k tokens]**
注入内容：
- 新 session 消息（Slack）：监督者发布 Sholto David 的补充分析（第二篇博文），将 DFCI 标记论文数从 58 升至 95（与 $15M 和解协议一致）
- 新文件：`workspace/cases/dfci/settlement_summary.md`（和解协议摘要，含 $15,000,000 / $2,630,000 / $8,500,000 三个数值）
- 新文件：`workspace/cases/dfci/papers_flagged_v2.csv`（95 篇论文完整列表）
- 旧信息矛盾处理：papers_flagged_v2.csv 与 v1 版本（58 篇）冲突，须以 v2 为准

**Q12** — 目标：根据 Update 1 修正核查报告，更新 papers_flagged 数量
- 产物：更新 `workspace/cases/dfci/case_summary.md`
- check 锚点：文件须含 `95`（新数量）而非 `58`（旧数量）；须含 settlement 金额 `15,000,000`；须含 whistleblower 金额 `2,630,000`
- 向量：V2（动态 update 反转，正确答案从 58 变为 95），V10（supersede 辨别，v2 取代 v1）

**[UPDATE 2 注入 — 约 35k tokens，含 supersede]**
注入内容：
- **supersede 事件**：机构法务发来邮件，指出和解协议「14 papers under Researcher 1」中的 Researcher 1 身份已在 2025-12 公开确认为 Kenneth C. Anderson，同时撤回之前一封声称 Researcher 1 是「William Hahn」的内部 memo（该 memo 是 V6 废弃副本红鲱鱼）
- 新 session：飞书群消息（bot 自动摘要），声称 Gino PNAS Study 1 的参与者数量为「N=201」——这是 V5 诱饵，真实值为 N=101
- 新文件：`workspace/cases/dfci/researcher_id_clarification.md`（权威澄清文件）
- 新文件：`workspace/communications/email/legal_memo_researcher1.md`（法务邮件，明确 Researcher 1 = Kenneth Anderson）

**Q13** — 目标：核实 Researcher 1 身份，更新 anderson_blot_analysis.tsv，拒绝废弃 memo
- 产物：更新 `workspace/cases/dfci/image_analysis/anderson_blot_analysis.tsv`；新增 `workspace/reports/wip/researcher_id_log.md`
- check 锚点：anderson_blot_analysis.tsv 中 `researcher_label` 列所有行值为 `"Kenneth_C._Anderson"`（非 `"William_Hahn"`）；researcher_id_log.md 须含 `"superseded"` 且引用日期 `2025-12`
- 向量：V6（废弃副本红鲱鱼：旧 memo 声称 Hahn，须识别并废弃），V10（supersede 辨别），V2

**Q14** — 目标：验证飞书 bot 摘要中 N=201 的声称，以文档为据更正回 N=101
- 产物：`workspace/reports/wip/gino_n_verification.md`
- check 锚点：文件须含 `"N=101"` 或 `"n_total: 101"`；须含字符串 `"bot summary"` 或 `"automated summary"` 并标记为 `"INCORRECT"` 或 `"rejected"`；须引用 DOI `10.1073/pnas.1209746109`
- 向量：V5（bot 自动摘要诱饵，N=201 是陷阱），V1（多源冲突，飞书 bot 与 Data Colada 报告矛盾，须正确取舍）

### 第 4 阶段（Q15-Q17）：最终报告与 SHA256 校验

**Q15** — 目标：撰写 DFCI 案例最终核查报告
- 产物：`workspace/reports/final/2024-01-02_dfci_final_report.md`（含完整 COPE 分类、数值锚点、时间线）
- check 锚点：文件存在；含 `"6 retractions"` 和 `"31 corrections"`；含 `"$15,000,000"`；含 DOI `10.1126/science.1123480`；命名符合 P1 规范
- 向量：V4（前轮所有数值须在此报告中正确闭合），P1（文件命名），P2（结构规范）
- Preference P4 静默考察：报告摘要须不超过 300 词

**Q16** — 目标：撰写 Gino 案例最终核查报告
- 产物：`workspace/reports/final/2023-07-12_gino_final_report.md`
- check 锚点：含 `"N=101"`；含 F 统计量 `17.69`；含 `"calcChain"`；含所有 4 篇论文 DOI（10.1073/pnas.1209746109, 10.1177/0956797614520714, 10.1177/0956797615575277, 10.1037/pspa0000226）
- 向量：V4（数值闭合），V9（verbatim DOI），P5 静默考察（每篇论文须独立列出 retraction_doi）

**Q17** — 目标：生成整合两案例的最终汇总 JSON，并用 sha256 校验脚本对其签名
- 产物：`workspace/reports/final/summary.json`；`workspace/reports/final/summary.json.sha256`（含 `VERIFIED:<sha256hex>` 格式）
- check 锚点：`sha256sum workspace/reports/final/summary.json | awk '{print "VERIFIED:" $1}'` 的输出须与 `summary.json.sha256` 文件内容精确匹配；`summary.json` 须含 `dfci.retraction_count: 6`，`gino.retraction_count: 4`，`dfci.settlement_usd: 15000000`
- 向量：V7（Bash-sha256 sign-off token，须真实跑脚本），V8（JSON schema），V4（所有数值终局闭合）

---

## Update 设计（含 supersede）

### Update 1（注入于 Q11 之后）

**时机**：Q12 之前推送
**体量**：约 35k tokens
**内容**：
1. Slack 消息（~5k tokens）：监督者引用 For Better Science 第二篇分析，论文数升至 95
2. `papers_flagged_v2.csv`（~20k tokens）：95 篇完整列表，包含所有四位研究员论文
3. `settlement_summary.md`（~5k tokens）：2025-12 和解详情（$15M / $2.63M / >$8.5M）
4. 新邮件（~5k tokens）：NIH ORI（科研诚信办公室）正式启动调查通知

**改变的正确答案**：papers_flagged 从 58 → 95；需更新所有引用该数量的文档

### Update 2（注入于 Q13 之前，含 supersede）

**时机**：Q13 之前推送
**体量**：约 40k tokens
**supersede 内容**：
1. `legal_memo_researcher1.md`（~8k tokens）：法务邮件，明确 Researcher 1 = Kenneth Anderson，**撤销**之前流传的 `internal_memo_v1.md`（该旧 memo 错误声称 Researcher 1 = William Hahn）
2. 飞书 bot 摘要（~3k tokens）：自动生成摘要，错误写 N=201（V5 诱饵）
3. `researcher_id_clarification.md`（~5k tokens）：权威澄清文件
4. 新增更新版本的 DFCI 官方声明（~10k tokens）：含具体被撤稿论文附录清单
5. Surgisphere 对比案例资料（~14k tokens）：供 Q16 参考的第三案例素材（Lancet HCQ 撤稿，含 N=96,032 / 671 家医院数据）

**改变的正确答案**：Researcher 1 身份从「模糊」或「William Hahn」→ 明确为「Kenneth Anderson」

---

## 4-5 条 Preference

| # | 规则 | 注入方式 | 静默考察轮次 |
|---|------|---------|------------|
| P1 | 所有报告文件命名须遵循 `YYYY-MM-DD_caseid_type.md` 格式 | Q1 supervisor 消息显式注入 | Q15, Q16 |
| P2 | 核查报告须包含固定四节：Background / Evidence / Classification / Recommendation | Q7 feedback 注入（supervisor 打回初稿要求修改） | Q15, Q16 |
| P3 | 所有 JSON 输出须含 `schema_version: "1.0"` 字段 | Q11 前 Slack 消息显式注入 | Q11, Q17 |
| P4 | 报告摘要（Abstract/Executive Summary）不超过 300 词 | Q7 supervisor 注入 | Q15 |
| P5 | 每篇被撤稿论文须单独列出原始 DOI 与撤稿 DOI（两者均需填写） | Q16 之前 email 注入 | Q16 |

---

## 难度向量绑定汇总

| 向量 | 绑定轮次 | 说明 |
|------|---------|------|
| V1 多源信息冲突综合 | Q6, Q14 | DFCI 内部数字 vs 博客数字；飞书 bot vs Data Colada |
| V2 动态 update 反转 | Q12, Q13 | 论文数 58→95；Researcher 1 身份明确 |
| V3 隐式 preference 静默考察 | Q15, Q16 | P1 文件命名、P2 结构、P4 字数限制 |
| V4 跨轮数值/事实闭合 | Q4→Q8, Q8→Q10, Q15, Q16, Q17 | DOI 一致性、N=101 贯穿 Q8-Q16、F统计量闭合 |
| V5 失真自动摘要诱饵 | Q14 | 飞书 bot 摘要 N=201 是陷阱 |
| V6 废弃副本红鲱鱼 | Q13 | 旧 memo 声称 Researcher 1 = Hahn，须识别废弃 |
| V7 Bash-sha256 sign-off | Q17 | 终轮必须运行 sha256sum 脚本 |
| V8 schema-by-shape 严格 check | Q1, Q4, Q11, Q17 | JSON/TSV 字段类型/范围/存在性 |
| V9 真实来源字段 verbatim 引用 | Q2, Q3, Q9, Q11 | DOI/图号/URL 精确引用 |
| V10 supersede 辨别 | Q12, Q13 | v2 取代 v1 论文列表；新 memo 取代旧 memo |

---

## 拆分/删除建议

素材极其丰富，**可拆为两个独立场景**：

- **sci1a**：DFCI 图像操纵专项核查（以 Dana-Farber 2024 案为主轴，偏图像分析与机构响应流程）
- **sci1b**：行为经济学数据统计造假复现（以 Gino 4 篇论文为主轴，偏 Excel/calcChain 分析与统计复现）

当前 BRIEF 将两者合并，若后续 workspace 体量压力大可按上述方案拆分。

---

## 关键可行性说明

- 所有 ground-truth 锚点均有真实 URL 可回溯
- Dana-Farber 案已进入法律和解阶段，信息公开充分
- Gino 案 Data Colada 博客提供完整统计分析，数值精确
- 两案例时间线不重叠（2020-2024），update 设计不会造成混淆
- 最大风险：For Better Science 博客（S1）需要直接访问，已确认可用
