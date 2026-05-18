# Alignment Table — hil_g3

`exec_check` 题之 question-workspace-eval 三角对齐分析。每行：题中所列值 → workspace 真源 → eval 检查 → 处理决策。

**Round 可见性**：
- q3,q4=initial（cloud-storage-access-log.md、email-attachment-audit.md）
- q6,q7,q8=after upd1（+file-version-history.md）
- q10,q11,q12,q13,q14=after upd2（+it-security-report.md, message_logs/chenjing_itsec_email.md）
- q16,q17,q18,q19,q20,q21=after upd3（+salary-spreadsheet-metadata.md）
- q23,q24,q25,q26,q27,q29=after upd4（+linxiaoya-partial-admission.md, im logs）

**Personas（USER.md）**：陈静 (HR Mgr, lead) · 张薇 (HR VP, decision-maker, Feishu) · 林小雅 (P009, suspect) · IT 安全 (email)。语气以陈静自语 / 飞书指令 / 内部备忘录三类为主。

**全局保全清单**：
- 输出路径如 `analysis/access_timeline.json`、`scripts/parse_access_log.py`、`docs/YYYY-MM-DD_*.md` — 必 verbatim
- JSON schema 字段：`computed_delta_to_email_seconds`、`download_before_email`、`size_match_full_version`、`recipient_external_domain`、`chain_valid`、`hash_match`、`hypothesis_h3_status`、`download_confirmed`、`download_version`、`download_timestamp`、`download_size_mb`、`email_sent`、`email_recipient`、`email_timestamp`、`email_attachment_size_mb`、`delta_seconds`、`data_exposed_employees`、`defense_claims`、`it_report_exoneration_scope`、`hash_match_confirmed`、`incident_id`、`evidence_chain`、`contradictions_resolved`、`recommended_actions`、`overall_assessment`、`statements`、`statement_date`、`contradicting_evidence`、`contradiction_source`、`hypothesis_id`、`supporting_evidence` 等 — 全 verbatim
- 枚举：`refuted` / `partial_admission` / `partially_admitted` / `likely` / `possible` / `strong` / `high` / `PREVIEW`/`DOWNLOAD`/`UPLOAD`/`EDIT`
- 字面 grep target：`a3f7b2c8e9d1`（hash）、`IT-SEC-2026-INV-042`、`2026-09-25T14:22:17+08:00`、`2026-09-25T15:03:44+08:00`、`14:22:17`、`15:03:44`、`14:22`、`15:03`、`2487`、`headhunter`、`zhangling@headhunter-corp.com`、`薪资数据参考`、`完整版`、`误操作`、`承认`、`SAL-LEAK-2026-09`、`李明`、`赵伟`、`孙丽`、`v1.1`、`v1.0`、`2.1`、`2.3`、`0.8`、`0.2`、`2.875`、`a3f7b2c8e9d1`

---

## q3 — access_timeline.json + size_fingerprint.md（initial round）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `analysis/access_timeline.json` / `analysis/size_fingerprint.md` | — | test -f / 内容检查 | KEEP |
| 字段 timestamp/user_email/action/filename/size_mb | — | JSON 字段 | KEEP |
| `computed_delta_to_email_seconds` 值 ~2487 | 邮件 15:03:44、下载 14:22:17 自算 | 范围 [2477,2497] | KEEP 字段名；值由 agent 计算 |
| 邮件时间 `2026-09-25T15:03:44+08:00` | email-attachment-audit.md | 用于差值 | KEEP（时间戳必明示，否则 agent 无法计算 delta） |
| 比率 `2.875` | 自算 2.3/0.8 | grep "2.875" | KEEP literal |
| 标签 'full salary file' / 'anonymized file' | 工作区文件 | grep "0.8" + grep "2.3" | STRIP 半数；保留 0.8 / 2.3 / 2.875 |
| ≥2 `## ` 标题 | — | 头数 | KEEP |
| 枚举 PREVIEW/DOWNLOAD/UPLOAD/EDIT | — | JSON action 字段值 | KEEP |

## q4 — parse_access_log.py（initial）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `scripts/parse_access_log.py` | — | 必跑 | KEEP |
| 输入路径 cloud + email log | initial | 实开 | STRIP（提"两份日志"指代即可） |
| `lxy@company.com` / `headhunter` | 工作区 | recipient 含 'headhunter' | KEEP `headhunter` 字面 |
| 字段名 download_timestamp/email_timestamp/delta_seconds/email_recipient/attachment_size_mb | — | JSON 键 | KEEP |
| 大约 2487 / 2.3 | 自算 | range check | STRIP（agent 自算） |
| md 表头列名 时间戳/用户/操作/文件名/大小、时间戳/发件人/收件人/主题/附件/大小 | — | 仅作提示 | STRIP（agent 应自读表头） |

## q6 — version_trace.md / claim_vs_evidence.json / new_employee_exposure.md（upd1 round）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径三件 | — | 必检 | KEEP |
| `2.1` / `2.3` 与"v1.0 排除/v1.1 确认" | file-version-history.md | grep "2.1" + grep "2.3" + 排除语 | KEEP literal `2.1`/`2.3`/`v1.0`/`v1.1` |
| 三声明 claim 文本 | — | refuted 验 | 转语义指代；保 verdict='refuted' verbatim |
| 三员工 李明/赵伟/孙丽 | file-version-history.md | grep all three | KEEP literal（grep 字面） |
| `v1.1` | 同上 | grep | KEEP |
| ≥2 ## 标题 | — | 头数 | KEEP |

## q7 — version_matcher.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `scripts/version_matcher.py` | — | 必跑 | KEEP |
| 输出 JSON 字段 downloaded_version/version_size_mb/v10_size_mb/size_delta_from_v10/new_employees/conclusion | — | JSON 验 | KEEP |
| 值 v1.1 / 2.3 / 2.1 / 0.2 | — | == / 接近 | STRIP（agent 自比） |
| 三员工 | — | len==3 | STRIP（不 grep 名字，仅 len） |

## q8 — hypothesis_matrix.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 + schema 字段 hypothesis_id/hypothesis/supporting_evidence/contradicting_evidence/status | — | 必检 | KEEP |
| H1..H4 文本 | — | hypothesis 文本未硬检；只查 status 与 contradicting_evidence ≥1 | KEEP H1-H4 标签 + 简文；可微改 |
| status: refuted/refuted/possible/likely | — | 严等 | KEEP literal |

## q10 — it_scope_analysis.json + evidence_convergence.md（upd2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径两件 | — | 必检 | KEEP |
| `IT-SEC-2026-INV-042` | it-security-report.md | grep | KEEP |
| 字段 report_id/checked_channels/unchecked_channels/report_conclusion/email_leak_detected_by_it/scope_gap_identified | — | JSON | KEEP |
| 'cloud sharing'/'shared links'/'guest access' | it-security-report.md | grep all | KEEP literal |
| 'email attachments' 在 unchecked_channels | — | grep | KEEP |
| `email_leak_detected_by_it=false` `scope_gap_identified=true` | — | 严等 | KEEP |
| 三源 cloud-storage-access-log.md / email-attachment-audit.md / it-security-report.md | — | grep 文件名 | KEEP literal |
| ≥3 ## | — | 头数 | KEEP |

## q11 — evidence_chain_validator.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必跑 | KEEP |
| 字段 download_before_email/size_match_full_version/size_mismatch_anonymized/recipient_external_domain/delta_seconds/chain_valid | — | JSON | KEEP |
| 值 2.3 / 0.8 | — | 自算 | STRIP |
| `company.com` 域 | email-attachment-audit.md | 域比较逻辑 | KEEP（必述域比较） |
| ~2487 | 自算 | range | STRIP |

## q12 — contradiction_resolution.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| `IT-SEC-2026-INV-042` | — | grep | KEEP |
| `chenjing_itsec_email.md` 或 '陈静'+IT 邮件交流 | — | grep "chenjing" 或 "陈静" 上下文 | KEEP "chenjing_itsec_email.md" |
| 'email attachment' 与 'scope' | — | 邻近 grep | KEEP "email attachment" / "scope" |
| 不可言 IT 'wrong'/'incorrect' | — | 反向 grep | KEEP（在题中提示） |
| ≥3 ## | — | 头数 | KEEP |

## q13 — suspect_profile.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 + schema | — | 必检 | KEEP 全 schema |
| 时间戳硬值 `2026-09-25T14:22:17+08:00`、`2026-09-25T15:03:44+08:00` | — | 字符串 == | KEEP literal |
| `download_size_mb=2.3` `email_attachment_size_mb=2.3` | — | == | KEEP |
| `delta_seconds=2487` | — | range | KEEP（值要 verbatim） |
| `hash_match_confirmed=false` | — | == | KEEP |
| `defense_claims` 3 项 status='refuted' | — | == | KEEP |
| 三员工名 | — | array | KEEP |
| `it_report_exoneration_scope='cloud channels only'` | — | == | KEEP |
| `email_recipient='zhangling@headhunter-corp.com'` `download_version='v1.1'` | — | == | KEEP |

## q14 — preliminary memo（upd2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `docs/YYYY-MM-DD_preliminary_investigation_memo.md` | — | glob + 头检 | KEEP pattern |
| `IT-SEC-2026-INV-042` | — | grep | KEEP |
| `14:22:17` `15:03:44` | — | grep | KEEP literal |
| 首 ## 标题含 'Summary'/'Executive' | — | 头检 | KEEP literal |
| ≥4 ## | — | 头数 | KEEP |
| "2.3 MB 是完整版（非脱敏 0.8 MB）" | — | 反向 grep "2.3" 不与 "anonymized" 同行 | STRIP；提"P3 摘要先行 + P4 量化"即可 |

## q16 — hash_chain_verifier.py（upd3）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必跑 | KEEP |
| `a3f7b2c8e9d1` | salary-spreadsheet-metadata.md | == 字符串 | KEEP literal — 但 agent 须从 metadata 读出，可于题中以"哈希前16位"指代而不直写 — 不过 eval 用 hash 字面验证 stdout，如 agent 自读元数据可得，故此处可 STRIP 字面，**但 eval 还断言 d['full_v1_1_hash']=='a3f7b2c8e9d1'** → 必产生此值，非 question 必 grep。题中可不直写；STRIP |
| `hypothesis_h3_status='refuted'` | — | == | KEEP |
| `hash_match=true` | — | == | KEEP |
| 列名 'SHA-256 哈希 (前16位)' | — | parser 提示 | STRIP（agent 自读） |

## q17 — lin_xiaoya_statement_log.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| schema 字段 statement_date/statement/contradicting_evidence/contradiction_source/status | — | 必 | KEEP |
| 三立场文本 | — | 数 | STRIP（语义指代 OK） |
| `'a3f7b2c8e9d1' 或 'hash'` 在 contradicting_evidence | — | grep "a3f7b2c8e9d1" 或 "hash" | KEEP "hash" 字样足；语义指代 hash 证据 |
| 全 status='refuted' | — | 严等 | KEEP |

## q18 — cryptographic_proof.md + metadata_analysis.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径两件 | — | 必检 | KEEP |
| `a3f7b2c8e9d1` | — | grep | KEEP |
| `SHA-256` | — | grep | KEEP |
| `salary-spreadsheet-metadata.md` 引用 | — | grep | KEEP literal |
| `salary-data-analysis.xlsx` | — | grep | KEEP |
| `2.3` | — | grep | KEEP |
| 'identical'/'byte-level' 类语 | — | grep | KEEP（可中英任一）|
| 碰撞概率 | — | grep "collision" | KEEP "collision" |
| ≥2 ## | — | 头数 | KEEP |

## q19 — alternative_hypotheses_refutation.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| `a3f7b2c8e9d1` | — | grep | KEEP |
| `0.8` 与 `2.3` 邻近 | — | grep both | KEEP |
| `headhunter-corp.com` | — | grep | KEEP |
| `薪资数据参考` | — | grep（grep 字面中文） | KEEP literal |
| 不含 'possible'/'plausible'/'cannot be ruled out' | — | 反向 grep | KEEP（提示）|

## q20 — complete_evidence_chain.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 + schema | — | 必检 | KEEP |
| 6 步 step/event/timestamp/source/key_fact/links_to_next/confidence | — | 严校 | KEEP |
| step 1 timestamp `2026-09-25T14:22:17+08:00` | — | == | KEEP |
| step 4 timestamp `2026-09-25T15:03:44+08:00` | — | == | KEEP |
| step 3 含 `a3f7b2c8e9d1` | — | grep | KEEP |
| 全 confidence='high' | — | == | KEEP |

## q21 — investigation_findings_report.md（upd3）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `docs/YYYY-MM-DD_investigation_findings_report.md` | — | glob | KEEP pattern |
| 首 ## 800 字内 'Executive Summary' / 'Summary of Findings' / 'Key Findings' | — | 头检 | KEEP |
| ≥6 ## | — | 头数 | KEEP |
| `a3f7b2c8e9d1` | — | grep | KEEP |
| `IT-SEC-2026-INV-042` | — | grep | KEEP |
| `2026-09-25T14:22:17+08:00` `2026-09-25T15:03:44+08:00` | — | grep | KEEP |
| ≥1000 字 | — | wc | KEEP |
| P1/P2/P3/P4 | — | check_preferences | KEEP rule labels |

## q23 — updated statement_log（upd4）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径（更新原文件） | — | 必检 | KEEP |
| `overall_assessment='partially_admitted'` | — | == | KEEP |
| `statements` 数组 4 项 | — | len | KEEP |
| 4-th status='partial_admission' | — | == | KEEP |
| 引用承认文本（'我承认' / '完整版薪资表' / '误操作'） | linxiaoya-partial-admission.md | grep | KEEP literal `完整版` 或 `我承认`；建 KEEP 二者 |
| `statement_date='2026-10-03'` | — | grep | KEEP literal |

## q24 — denial_vs_evidence_timeline.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| `2487` 或 '41 min' | — | grep | KEEP（一者）|
| `a3f7b2c8e9d1` | — | grep | KEEP |
| 承认词 `完整版`/`误操作`/`承认` | — | grep | KEEP |
| `14:22` 在 `15:03` 前 | — | 顺序 | KEEP literals |
| ≥4 ## | — | 头数 | KEEP |
| 5 事件按日期顺序 | — | 顺序 | KEEP（日期硬码）`2026-09-25 14:22`、`2026-09-25 15:03`、`2026-09-30`、`2026-10-03` |
| `IT-SEC-2026-INV-042` | — | 可能 grep | KEEP |

## q25 — case_strength_scorer.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必跑 | KEEP |
| 5 components 评分权 0.35/0.25/0.20/0.15/0.05 | — | sum>=0.95 | KEEP（数与文件名） |
| 文件名 `analysis/complete_evidence_chain.json` 等 | — | 自查 | KEEP |
| `a3f7b2c8e9d1` 字串 | — | 自查 | KEEP |
| `verdict='strong'` if score>=0.95 | — | == | KEEP |

## q26 — formal_case_summary.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `docs/YYYY-MM-DD_formal_case_summary.json` | — | glob | KEEP |
| 顶层键 incident_id/suspect/incident_date/evidence_chain/contradictions_resolved/conclusion/recommended_actions | — | 必 | KEEP |
| `incident_id='SAL-LEAK-2026-09'` | — | == | KEEP |
| `incident_date='2026-09-25'` | — | == | KEEP |
| evidence_chain ≥5 / contradictions_resolved ≥4 / recommended_actions ≥3 | — | len | KEEP |
| 'IT-SEC-2026-INV-042 scope' 入 contradictions_resolved | — | grep | KEEP |
| verdict 不可 'inconclusive'/'insufficient'/'unclear' | — | 反向 grep | KEEP |

## q27 — case_strength_assessment.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| 4 类证据 | — | 各项 grep | KEEP |
| `a3f7b2c8e9d1` | — | grep | KEEP |
| 'beyond reasonable doubt' / `排除合理怀疑` / `确实充分` | — | 任一 | KEEP（题中给 phrase 选择） |
| 不可'insufficient evidence'/'defense has merit'/'cannot determine'/'evidence is weak' | — | 反向 | KEEP（提示） |
| ≥3 ## | — | 头数 | KEEP |

## q29 — final report + evidence index

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径两件 `docs/YYYY-MM-DD_final_investigation_report.md` `docs/case_evidence_index.json` | — | glob/== | KEEP |
| 首 ## 'Conclusion'/'Summary'/'Executive'/'Findings' | — | 头检 | KEEP |
| ≥5 ## | — | 头数 | KEEP |
| `2487` 或 '41 min' | — | grep | KEEP |
| `a3f7b2c8e9d1` | — | grep | KEEP |
| `IT-SEC-2026-INV-042` | — | grep | KEEP |
| 承认词 `完整版`/`误操作`/`承认` | — | grep | KEEP |
| ≥1200 字 | — | wc | KEEP |
| index.files ≥5 | — | len | KEEP |
| P1-P5 | — | check_preferences | KEEP labels |

---

## 总体策略

- **大量 KEEP literal**：本任务为 forensic 取证 / 证据链 / 多 hash + 时间戳锚定题，eval 大量 grep 字面（hash、时间、报告号、enum status、中文短语）。可 STRIP 处少。
- **STRIP 之处**：(a) workspace 文件之"内容描述"段如表头列名、文件之事实复述（agent 应自读取）；(b) 自算之 delta/比率值；(c) 三员工名在 q7（仅 len）；(d) 部分背景叙述。
- **persona**：陈静自语 / 飞书指令（张薇 → 陈静向下传）/ 内部备忘录三种。变化以避机械感。
- **首次出现文件**：cloud-storage-access-log.md 与 email-attachment-audit.md 于 q3/q4 直名；后续轮以"云盘日志""邮件审计"代。file-version-history.md 于 q6/q7 直名；后以"版本历史档"代。it-security-report.md 与 IT 邮件于 q10/q12 直名；后以"IT 报告"代。salary-spreadsheet-metadata.md 于 q16/q18 直名；后以"取证元数据"代。linxiaoya-partial-admission.md 于 q23 直名；后以"林小雅 10/3 飞书自陈"代。
