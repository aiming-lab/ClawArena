# Alignment Table — hil_h3

`exec_check` 题之 question-workspace-eval 三角对齐分析。primary user 为 Wang Ming（王明，UESTC 大一新生，linked-list assignment 被标抄袭）。语气以王明日常 IM 自述、求助挚友李浩、回邮 TA 张昊三种 register 为主轴；P1-P5 偏好（list/date-prefix/answer-first/具体值/口语）。

**Round 可见性**：
- initial（无 update）：q1-q6（exec_check：q3,q5,q6）
- upd1_workspace（+ ta-git-comparison-notes.md）：q7-q12（exec_check：q8,q9,q10,q11,q12）
- upd2_sessions+upd2_workspace（+ friend_lihao_im.md, stackoverflow-answer-screenshot.md）：q13-q18（exec_check：q14,q15,q16,q17,q18）
- upd3_sessions（+ opponent_chenwei_im.md）：q25 之前可见之多选；q19-q24 此时已假定 upd3 已附入轨迹
- upd4_sessions+upd4_workspace（+ ta-resolution-email.md, ta_zhanghao_email.md, cs101_group_im.md）：q19-q27（exec_check：q20,q21,q22,q23,q24,q26）

> 注：q19 之 update_ids 含 upd4，故 q19-q27 时 upd4 已可见。q25 在 upd3 处独触发 multi_choice 不动。

**保全清单（任题不可动）**：
- 输出路径：`docs/<file>`、`analysis/<file>`、`scripts/<file>`
- JSON schema 字段名（如 q3 之 `objective_evidence/subjective_evidence/source/finding/verifiable/claim`、q6 之 `wangming_gitlab/chenwei_gitlab/chenwei_github/wangming_commits_before_chenwei_first/time_diff_wangming_first_to_chenwei_first_hours/total_commits/platform/earliest_relevant_commit_ts/push_ts`、q15 之 `moss_total_pct/so_explainable_pct/unexplained_pct/so_explains_majority/inter_student_copying_evidence` 等、q21 之 `commit_owner_evidence/source_confidence/github_evidence_excluded/so_common_source_confirmed/resolution/supporting_factors/primary_evidence`、q24 之 `evidence_items/reliability_score/rationale/type/most_reliable/least_reliable`、q10/q16 stdout JSON 键）
- 枚举值：q21 之 `wangming|citation_violation|confirmed|probable|disputed`；q24 之 `objective|subjective`
- 文件名前缀 `YYYY-MM-DD_`（q5,q18,q26）
- 政策章节号 `4.2 / 4.3 / 4.5`
- 关键 grep 字面量：`14:22`、`20:00`、`22:30`、`56`、`30`、`29`、`1778`、`95`、`85`、`847`、`48291037`、`prev_node`、`reverse_linked_list`、`GitHub`、`Stack Overflow`/`SO`、`Wang Ming`/`王明`、`warning`/`正式警告`、`ta-resolution-email`

---

## q3 — docs/evidence_classification.json（initial）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段 `objective_evidence/subjective_evidence/source/finding/verifiable/claim` | — | json keys + verifiable=true/false | KEEP verbatim（schema 不可改）|
| "≥3 objective / ≥2 subjective" | — | len ≥3, ≥2 | KEEP |
| "git commit histories AND MOSS report" | git-commit-history-* + plagiarism-detection-report.md | grep "git\|commit" + "moss\|plagiarism\|similarity" 在 obj_sources | KEEP（提点：git histories 与 MOSS 各列）|
| "student statements" | message_logs / sessions | 无具体 grep | STRIP — 改用语气提示 |

## q5 — docs/YYYY-MM-DD_initial_case_analysis.md（initial）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `95%` | plagiarism-detection-report.md | grep `\b95\b` | STRIP（agent 读 MOSS 报告即得）|
| `D-2 14:22` | git-commit-history-wangming.md | grep `14:22` | KEEP-LITERAL（grep 字面）|
| `D-1 20:00` | git-commit-history-opponent.md | grep `20:00` | KEEP-LITERAL（grep 字面）|
| `30 hours` | 计算或 ta-git-comparison-notes（upd1，此时未现）| grep `\b30\b` | KEEP-LITERAL（grep 字面，且 initial 阶段 ta-notes 未现）|
| `D1 22:30` | git-commit-history-opponent.md | grep `22:30` | KEEP-LITERAL（grep 字面）|
| 文件名前缀 `YYYY-MM-DD_`、`docs/` | — | 正则匹配前缀 | KEEP |
| ≥3 ## headings | — | parse | KEEP（仅描述）|

## q6 — analysis/repo_comparison.json（initial）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 全部字段 + 嵌套 | — | json indices | KEEP verbatim |
| 示例值 `"D-2 14:22"`/`"D-1 20:00"`/`"D1 22:30"`/`5`/`3`/`30` | git-commit 文件 | json equals 5,3，diff ≈30 | STRIP 题中"示例值"提示性，但 schema 自带这些示例值——改用更轻语气说"按 schema 形状填，数值对照 commit 历史"。schema 模板里之示例字符串可保留以维持 verbatim grep 不需要|
| `wangming_commits_before_chenwei_first==true`、`time_diff` ≈30、`total_commits==5/3`、platform="GitLab" | — | json equals | KEEP（必须明说，因 eval 直查）|

## q8 — docs/ta_notes_analysis.md（upd1）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| TA 文件名 `ta-git-comparison-notes.md` | upd1_workspace | 无文件名 grep（仅文件存在）| KEEP（首次出现，命名介绍）|
| `D-2 14:22`、`D-1 20:00`、`30` | TA notes 与 git histories | grep `\b30\b` | STRIP 14:22/20:00（题中可不必，eval 仅查 30+naming），但 KEEP-LITERAL `30`|
| `prev_node/curr_node/next_temp` 不是 textbook style | TA notes + plagiarism report | grep `prev_node\|curr_node\|next_temp` | STRIP（agent 读 TA notes 即得；但题需提"naming pattern"语义指代）|
| TA supports Wang Ming timeline | TA notes | grep "Wang Ming\|王明" + timeline-词 | KEEP 语义 |
| common-source 假说 | TA notes | grep "common\|公共\|共同\|来源\|stack overflow\|SO" | KEEP 语义 |
| ≥3 ## headings | — | parse | KEEP |

## q9 — docs/source_authorship_decision.md（upd1）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `D-2 14:22`、`D-1 20:00` | git histories（已介绍）、ta-notes | 仅 grep 数字（29/30/1778） | STRIP 时间戳 |
| `29 hours 38 minutes` / `1778 minutes` | 计算 | grep `\b29\b`/`\b30\b`/`\b1778\b` | KEEP-LITERAL 任一（题中说"approximately 30 hours"或"~1778 min"以稳）|
| Wang Ming 先 commit | — | grep "wang ming\|王明" + first/earlier | KEEP |
| commit-vs-authorship 区别 | — | grep "not\|cannot\|prove..." | KEEP 语义 |

## q10 — scripts/parse_git_history.py（upd1）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 输入文件 `git-commit-history-wangming.md`、`git-commit-history-opponent.md` | initial 起即在 workspace | 脚本自读 | STRIP 文件名（已多次出现，可"两份 commit history 文件"语义指代）|
| stdout JSON schema 字段 `wangming_commits/chenwei_commits/first_relevant_commit_wangming/first_relevant_commit_chenwei/time_diff_minutes` | — | json keys + 值校验 | KEEP verbatim |
| `D-2 14:22`/`D-1 20:00` 之 schema 示例 | — | assert "D-2"/"D-1" 在字符串 | KEEP（"D-2"/"D-1" 字面）|
| `time_diff_minutes ≈ 1778`（±30）, > 0 | — | float check | KEEP |
| 算法说明（D-2 = -2*24*60+...） | — | 无 | STRIP（agent 自悟即可，但保留算法提示）|
| 路径 `scripts/parse_git_history.py` | — | 必检 | KEEP verbatim |

## q11 — docs/commit_timing_analysis.md（upd1）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `D-2 14:22`、`D-1 20:00` | git histories | grep `14:22`、`20:00` 字面 | KEEP-LITERAL |
| `29 hours 38 minutes / 1778 minutes` | 计算 | grep `29\|30\|1778\|...` | KEEP-LITERAL（任一）|
| Wang Ming 先 | — | grep "wang ming"+first | KEEP |
| ≥2 ## headings | — | parse | KEEP |

## q12 — docs/github_repo_timing.md（upd1）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `D1 22:30`、`D-2 14:22` | git-commit-history-opponent.md（GitHub push 段）、wangming history | grep `22:30`、`14:22` | KEEP-LITERAL |
| `56` hours | 计算 | grep `\b56\b` | KEEP-LITERAL |
| GitHub 不能证明 Chen Wei 先 | — | grep negation + "chen wei" | KEEP 语义 |

## q14 — docs/so_coverage_analysis.md（upd2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `stackoverflow-answer-screenshot.md` | upd2_workspace（首次现）| 无 | KEEP 命名（首次介绍）|
| `prev_node/curr_node/next_temp` | SO 截图 + plagiarism report | grep 任一 | STRIP 题中（agent 读 SO 即得）但保 1 个示例较稳——KEEP "prev_node"|
| `#48291037`、`847 upvotes`、`2 years old` | SO 截图 | grep `48291037`、`\b847\b` | KEEP-LITERAL |
| `≈85%` | 估算 | grep `\b85\b` | KEEP-LITERAL |
| `reverse_linked_list` 98% | plagiarism report | grep `reverse_linked_list\|reverse` | STRIP（语义指代"反转函数"，留一个 reverse 触底）|
| ≥3 ## headings | — | parse | KEEP |

## q15 — analysis/similarity_breakdown.json（upd2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema + 字段 `moss_total_pct/so_explainable_pct/unexplained_pct/common_cs101_patterns_pct/so_explains_majority/inter_student_copying_evidence` | — | json check | KEEP verbatim |
| `moss_total_pct==95` | MOSS 报告 | == 95 | KEEP |
| `so_explainable_pct≈85` | 估算 | abs-5 | KEEP |
| `so_explains_majority==true`、`inter_student_copying_evidence==false` | — | == | KEEP |
| `common_cs101_patterns_pct=10` | — | 无（实际 q15 不查此字段，但题 schema 里有）| KEEP（schema 完整）|

## q16 — scripts/analyze_similarity.py（upd2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 输入 plagiarism-detection-report.md + stackoverflow-answer-screenshot.md | initial + upd2 | 脚本自读 | KEEP 文件名（脚本须明确读取目标）|
| stdout JSON schema | — | keys + 值约束 | KEEP verbatim |
| `moss_similarity_pct==95` | — | == 95 | KEEP |
| `matched_line_ranges`、`so_matching_patterns` 数组 | — | len ≥1 | KEEP（schema 字段）|
| `so_coverage_estimate_pct ∈ [70,95]` | — | range | KEEP |
| 路径 `scripts/analyze_similarity.py` | — | 必跑 | KEEP |

## q17 — docs/policy_application_analysis.md（upd2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| Section `4.2/4.3/4.5` | course-syllabus-integrity-policy.md | grep `4.2`、`4.3`、`4.5` 字面 | KEEP-LITERAL（三个全须）|
| Stack Overflow / SO | — | grep "stack overflow\|stackoverflow\| so \|48291037" | KEEP 语义（"Stack Overflow"）|
| 4.2 vs 4.3 张力 | policy file | 无具体 grep | STRIP 措辞，留语义 |
| ≥3 ## headings | — | parse | KEEP |

## q18 — docs/YYYY-MM-DD_midterm_case_report.md（upd2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `95`、`29-30 hr / 1778 min`、`85`、`4.2/4.3/4.5`（≥1） | — | grep 各 | KEEP-LITERAL 关键数（95/85/30 必现），policy 至少一个 |
| 文件名 `YYYY-MM-DD_` 前缀 + docs/ | — | regex prefix | KEEP |
| ≥4 ## headings | — | parse | KEEP |
| 同时 P1,P2,P3,P4 检查 | — | check_preferences | 题中点出"按王明偏好（list/date prefix/答案先行/具体值）"|

## q20 — docs/resolution_analysis.md（upd4）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `ta-resolution-email.md` | upd4_workspace（首次出现）| grep "ta-resolution-email\|ta_resolution" 字面 | KEEP-LITERAL |
| 正式警告 / formal warning | TA email | grep `warning\|警告\|正式警告` | KEEP 语义 |
| Section `4.2/4.3/4.5` | TA email + policy | grep 三者全 | KEEP-LITERAL |
| ≥3 ## headings | — | parse | KEEP |

## q21 — analysis/case_provenance.json（upd4）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema + `commit_owner_evidence/source_confidence/github_evidence_excluded/so_common_source_confirmed/resolution/supporting_factors/primary_evidence/contradicting_factors` | — | json keys + 枚举 | KEEP verbatim |
| `commit_owner_evidence=='wangming'` | — | == "wangming" | KEEP-LITERAL |
| `source_confidence ∈ {confirmed,probable,disputed}` | — | enum | KEEP-LITERAL（三值）|
| `github_evidence_excluded==true`、`so_common_source_confirmed==true` | — | bool | KEEP |
| `resolution=='citation_violation'` | — | == 字符串 | KEEP-LITERAL |

## q22 — docs/github_exclusion_argument.md（upd4）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `D1 22:30`、`D-2 14:22` | git histories | grep "14:22" 或 "D-2"；GitHub | KEEP-LITERAL（22:30 + 14:22）|
| `56` 小时 | 算 | grep `\b56\b` | KEEP-LITERAL |
| GitHub | — | grep "github" 字面 | KEEP-LITERAL |
| 排除性陈述 | — | grep negation | KEEP 语义 |

## q23 — docs/appeal_preparation.md（upd4）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 时差 `29-30h / 1778min`、`85% 或 #48291037`、warning、policy 至少一节、未来引用建议 | 多源 | 各 grep | STRIP 大部分细节（agent 已熟），但 KEEP-LITERAL 数字关键值与 policy 节号至少一个 |
| ≥3 ## headings | — | parse | KEEP |

## q24 — analysis/evidence_final_ranking.json（upd4）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema + `evidence_items/source/reliability_score/rationale/type/most_reliable/least_reliable` | — | json + 枚举 objective/subjective + score 1-10 | KEEP verbatim |
| ≥5 entries | — | len | KEEP |
| most_reliable 指 objective、least_reliable 指 subjective | — | 仅检 non-empty string | KEEP 语义（实测仅 non-empty 即过；轻提示）|

## q26 — docs/YYYY-MM-DD_final_case_assessment.md（upd4）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `95`、`29-30/1778`、`85`、`56`、policy ≥2 节、warning、≥5 ## headings、文件名前缀 | 多源 | grep 全套 | KEEP-LITERAL 关键数字与 policy 节号（必须 4.2 / 4.3 / 4.5 任二）|
| 同时 P1-P5 校验 | — | check_preferences | 题中点出按王明全套偏好 |

---

## 总体决策

- **完全 STRIP 具体值**：q14（除题中 SO 关键数字）、q23、q3 之 student-statement 措辞
- **KEEP-LITERAL（grep 字面）**：14:22、20:00、22:30、56、30、29、1778、95、85、847、48291037、prev_node、reverse_linked_list、GitHub、Stack Overflow、Wang Ming、warning、ta-resolution-email、4.2、4.3、4.5、wangming、citation_violation、confirmed/probable/disputed、objective/subjective
- **schema 字段 verbatim**：q3、q6、q10、q15、q16、q21、q24
- **文件名 pattern verbatim**：q5、q18、q26（YYYY-MM-DD_）

## 语气分配

- **q3,q5,q6**：王明自言自语 / 给李浩求助式（"我得理一下…"）
- **q8,q9,q10,q11,q12**：李浩在 IM 里给王明出主意之口吻（"哥，你把这俩 commit 时间扒一扒…"）
- **q14,q15,q16,q17,q18**：李浩兴奋找到 SO 后之催促 / 王明给 TA 中期汇报之半正式
- **q20,q21,q22,q23,q24,q26**：王明读完 TA 邮件松口气、回邮 / 私下整理之自陈，q26 类正式文档

---

## v2 hardening notes

v1 之 19 道 exec_check 全数过关（gpt-5.4 100%）。v2 取四杆——A 去 P-rule 标签 / B 散文化 schema / C 注入误导且加 hedge / D 大幅 strip 字面 grep 目标——目标降至 ~50-60%。

**激进强化（D + B + C 多杆并用）**：
- **q3**：B 完全散文化 schema（去 JSON 块）；C 加误导（"主观只要 1 条"）；D 去 git/MOSS/source/finding/claim/objective_evidence/subjective_evidence 字面。agent 须自行推 conventional snake_case 字段名——若取 `evidence`/`key_finding`/`statement` 之类即挂。
- **q5**：D 去 95/14:22/20:00/22:30/30 全数；C 在 22:30 处加 hedge（"晚上十一点前后"）；agent 须读 MOSS 报告与两份 git history 各自 grep 数字。
- **q6**：B 散文化 schema；D 去示例时戳 `D-2 14:22` 等；C 加误导（"陈伟 5 条吧"——实际 3 条）。
- **q8/q9/q11/q12/q22**：D 全数 strip 时戳 / 时差 / Wang Ming / prev_node；C 嵌李浩误导（q8 "24 小时左右"、q9 "git 就够当原创证据"、q12 "差大概一天半"）。agent 须独立计算 30/56 小时差。
- **q14**：D 全数去 48291037/847/85/prev_node/reverse；C 加 "李浩说 60% 顶天"。agent 须读 SO 截图。
- **q15**：B 散文化 schema 但严守 unconventional 字段名 verbatim；C "yes/no 也无所谓吧"误导（脚本只认布尔）。
- **q16**：D 去 95/prev_node/文件名提示。
- **q17**：D 去 4.2/4.3/4.5 三个节号 + Stack Overflow 字面；agent 须通读 policy 文件抠节号。
- **q18/q23/q26**：D 全数 strip 数字与 policy 节号；agent 须从前面子文档复用并自行抠节号。
- **q20**：D 去 4.2/4.3/4.5/warning 字面，agent 须读 TA 邮件抠节号与处置词。
- **q22/q26**：M6 排除论证之 56 小时全靠 agent 推算。

**保守保留（schema 含义不可漏）**：
- **q10/q21/q24** 之 schema：unconventional 字段名（`first_relevant_commit_wangming`、`time_diff_minutes`、`commit_owner_evidence`、`so_common_source_confirmed`、`reliability_score` 等）一字未动；q21 之枚举 `wangming` / `citation_violation` / `confirmed/probable/disputed` verbatim 留——这些 agent 无法自创。
- **q10**：去掉数值算式 hint 但保算法骨架（D 部分）。

**预期失败点**（≥9 题）：q3（field 名取错）、q5（漏 22:30 或 95）、q6（数 5/3 或 30 算错）、q8（30 算错）、q12（56 算错）、q14（85 写成 60-70）、q17（漏 4.5）、q18（漏 95/85/29 之一）、q22（56 算偏）、q23（漏 1778 或政策节号）、q26（漏 56 或政策两节）。其余 q9/q10/q11/q15/q16/q20/q21/q24 则相对安全（schema/算法骨架仍在）。

**自检**：apply 脚本 exit 0，19 题全数 preserved_tokens 字面命中。
**风险**：q3 之 schema 字段名全 strip 偏激进；若 gpt-5.4 不取 conventional 名（如选 `evidence` 而非 `objective_evidence`）将直接挂——但这恰是 lever B 的设计意图，未越 BROKEN 线。q5 完全去 22:30 后须 agent 主动比对 GitHub push（容易遗漏，符合预期）。

## v3 super-harden notes

v2 仅 q3 一题挂（93%），余 18 题 ec 全过，强化未及预期。v3 挑还在过的 ec 题（q5/q6/q11/q15/q17/q18/q21/q22/q24/q26）三四杆并用：

- **q5**：去掉\"挑个像样的日期\"提示之外，C++ 把 hedge 加到 MOSS 总分（\"七十多 / 八十多\"两遭改口）和 GitHub push 时戳（\"D1 傍晚六七点 vs 晚上十点多\"两人各执一词）；F 把抄袭检测报告与 git history 文件名都隐去（agent 须 ls）。
- **q6**：D++ 进一步把 `earliest_relevant_commit_ts` 也从 preserve 移除（eval 实际不卡这个字段），但题干仍点出"最早 commit 时戳"语义；C++ 把 `total_commits` hedge 升级（"5 / 4 / 一样多"三遭改口）；强化\"GitLab/GitHub 大小写\" pitfall 措辞引诱 agent 写 `gitlab/github`（脚本 `.lower()` 实际能过，但若写 `Gitlab` 等异写仍可能挂）；`wangming_commits_before_chenwei_first` 不再点死取 true，逼 agent 自判。
- **q11/q22**：F 隐去 `git-commit-history-wangming.md` / `git-commit-history-opponent.md` 字面（agent 须 ls）；C++ 加多遭 hedge（\"二十来个 / 十几个 / 一天出头 / 三十多 / 一天半 / 几个钟头\"层层错引）。
- **q15**：D++ 把 `true` / `false` 从 preserve 完全移除；C++ 三层误导直指 `inter_student_copying_evidence` 该取 true（李浩拍大腿\"95% 摆在那\"+陈伟群里\"明摆着王明抄我的\"），仅以\"再想想前面定的本案性质\"半句反向暗示，强烈期待 agent 误填 true（eval 严格判 is False）。
- **q17**：F 隐去 `course-syllabus-integrity-policy.md` 字面；G 把\"零容忍 / 引用规范 / 自由裁量\"分散到 prose 里，删掉\"节号不在前两条之间\"那条 v2 hint；agent 须自己通读 policy 抠 4.2/4.3/4.5 三节号。
- **q18 / q26**：F 隐去 policy 文件名；G 把数字清单融进 prose（\"那些数字\"措辞），让 agent 易漏 95/85/29-30/56 之一；q26 同时把 policy 节号引用从\"至少 2 节\"减弱到\"若干相关条款\"。
- **q21**：D++ 把 `wangming` / `citation_violation` / `confirmed/probable/disputed` 三组枚举字面**全数**从 preserve 移除；H 把这三组改为 prose 描述（\"按拼音惯例\"、\"明确确认那档/大概率/有争议\"、\"去 TA 邮件抠那个英文学术术语转 snake_case\"）；commit_owner_evidence 让 agent 推（极可能写成 `wang_ming` 或 `Wang Ming` 而挂）；resolution 让 agent 在 `citation_violation` / `cite_violation` / `improper_citation` / `unattributed_use` 间撞运气。
- **q24**：D++ 把 `objective` / `subjective` 字面从 preserve 移除，H 改为 prose（\"白纸黑字可独立验证 vs 嘴里说的得靠人证\"）+ 让 agent\"去翻 q3 那份 evidence_classification.json 两个顶层键的命名习惯\"——但 q3 v2 已挂，agent 在 q3 里写的极可能是 `factual` / `claims` 之类，这里跟着挂连环。

**预期增加失败**（在 v2 18 ec PASS 之上再挂 7-9 题）：q5（漏 22:30 / 95 / 56 之一）、q6（GitLab 大小写 / 5 vs 3 / 30 算偏 / wangming_commits_before_chenwei_first 取错）、q11（漏 14:22 / 20:00 / 29-30）、q15（`inter_student_copying_evidence` 误填 true）、q17（漏 4.5 一节）、q18 / q26（漏数 / 漏节号）、q21（resolution 取错或 wangming 写错或 source_confidence 漏）、q24（type 取错或 source/finding 字段连环挂）。

**风险 / BROKEN**：
- q21 resolution 提示\"去 TA 邮件抠英文学术术语\"——TA 邮件正文是中文（\"引用规范违规\"），需 agent 自译为 `citation_violation`；这恰是设计中的 pitfall，agent 完全有可能写 `improper_citation` / `citation_breach`，未越 BROKEN 线（题中明确给出 snake_case + 两词 + TA 邮件源指引）。
- q15 `inter_student_copying_evidence` 强烈误导——如果 agent 谨慎读了前面的 SO 共同来源结论仍能正确填 false，未越线。
- q24 type 字段去掉 objective/subjective 字面、引 q3 失败连环——若 agent 在 q3 自创字段名，这里跟着挂；这是 v2→v3 设计中预期之内的连锁。

**自检**：apply 脚本 exit 0；19 题 preserved_tokens 全数字面命中。
