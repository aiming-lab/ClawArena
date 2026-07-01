# BRIEF: sec2 — API 密钥泄露事件响应

## 场景叙事背景

一家中型 SaaS 企业（化名 NovaBridge）的安全工程师 Li Wei 发现 GitHub 推送保护触发告警：`secret_type: openai_api_key`，`validity: active`，位于同事 Huang Min 刚合并的提交中。同时 AWS CloudTrail 呈现异常的 `GetCallerIdentity` 与 `ListBuckets` 调用，来源 IP 不属于公司出口地址。GitGuardian 平台同步发出 webhook 告警，该 OpenAI Key 已在 5 分钟内被外部扫描器命中。

Li Wei 需主导完整事件响应流程：调查泄漏路径、量化受影响范围、执行多轮密钥轮换、向管理层提交事后分析报告。期间叠加 CircleCI 供应链事件（类比 2023-01-04 真实事件）上下游影响、AWS IAM 临时凭证特殊处置，以及一份 bot 自动摘要的失真数据干扰。

取材真实来源：CircleCI 2023-01-04 官方 postmortem、Codecov 2021 供应链攻击 post-mortem、GitGuardian State of Secrets Sprawl 2024、GitHub Secret Scanning REST API 字段规范、AWS GuardDuty/Config 官方文档。

---

## 真实来源链接表

| # | 来源标题 | URL | 类型 |
|---|----------|-----|------|
| 1 | CircleCI Jan-4-2023 Incident Report | https://circleci.com/blog/jan-4-2023-incident-report/ | postmortem |
| 2 | Codecov April 2021 Post-Mortem | https://about.codecov.io/apr-2021-post-mortem/ | postmortem |
| 3 | GitGuardian State of Secrets Sprawl 2024 | https://blog.gitguardian.com/the-state-of-secrets-sprawl-2024/ | dataset |
| 4 | GitHub Secret Scanning REST API Docs | https://docs.github.com/en/rest/secret-scanning/secret-scanning | official_doc |
| 5 | AWS GuardDuty: Remediating Compromised Credentials | https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html | official_doc |
| 6 | AWS Blog: What to Do If You Expose an AWS Access Key | https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/ | official_doc |
| 7 | AWS Config Rule: access-keys-rotated | https://docs.aws.amazon.com/config/latest/developerguide/access-keys-rotated.html | official_doc |
| 8 | GitHub Blog: 39M Secrets Leaked in 2024 | https://github.blog/security/application-security/next-evolution-github-advanced-security/ | news |
| 9 | GitHub Supported Secret Scanning Patterns | https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns | official_doc |
| 10 | OWASP API2:2023 Broken Authentication | https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/ | regulation |
| 11 | GitGuardian: Remediating OpenAI API Key Leaks | https://www.gitguardian.com/remediation/openai-api-key | official_doc |
| 12 | TruffleHog GitHub Repository | https://github.com/trufflesecurity/trufflehog | github |

---

## Ground-Truth 锚点表

| 锚点名 | 精确值 | 来源 URL | 备注 |
|--------|--------|----------|------|
| GH_SS_OPENAI_TYPE | `openai_api_key` | src [9] | GitHub secret_type 精确值 |
| GH_SS_ANTHROPIC_TYPE | `anthropic_api_key` | src [9] | Anthropic key 的 secret_type |
| GH_SS_AWS_TYPE | `aws_access_key_id` | src [9] | AWS key 的 secret_type 之一 |
| GH_SS_VALIDITY_VALUES | `active \| inactive \| unknown` | src [4] | validity 字段完整枚举 |
| GH_SS_RESOLUTION_REVOKED | `revoked` | src [4] | 密钥已撤销时的 resolution 值 |
| GH_SS_STATE_VALUES | `open \| resolved` | src [4] | state 字段枚举 |
| GITGUARDIAN_REMEDIATION_1H | `2.6%` | src [3] | 泄漏后 1 小时内撤销比例 |
| GITGUARDIAN_ACTIVE_5DAYS | `>90%` | src [3] | 泄漏后 5 天仍有效的密钥比例 |
| GITGUARDIAN_OPENAI_SURGE | `1212x` | src [3] | 2023 年 OpenAI key 泄漏同比增幅 |
| GITHUB_2024_TOTAL_LEAKS | `39 million` | src [8] | GitHub 2024 年检测泄漏密钥总数 |
| CIRCLECI_EXFIL_DATE | `2022-12-22` | src [1] | CircleCI 数据实际外泄日期 |
| CIRCLECI_DETECT_DATE | `2022-12-29` | src [1] | 客户告警触发调查日期（Update 2 正确值） |
| CIRCLECI_GH_OAUTH_COMPLETE | `2023-01-07T07:30:00Z` | src [1] | GitHub OAuth token 轮换完成时间（UTC） |
| CIRCLECI_MALWARE_SHA256 | `8913e38592228adc067d82f66c150d87004ec946e579d4a00c53b61444ff35bf` | src [1] | PTX-Player.dmg SHA256 |
| AWS_IAM_KEY_PREFIX_LONG | `AKIA` | src [5] | IAM 用户长期 Access Key 前缀 |
| AWS_IAM_KEY_PREFIX_STS | `ASIA` | src [5] | STS 临时凭证前缀 |
| AWS_STS_MAX_DURATION | `36 hours` | src [6] | GetSessionToken/GetFederationToken 最长有效期 |
| AWS_CONFIG_RULE_NAME | `ACCESS_KEYS_ROTATED` | src [7] | AWS Config 托管规则标识符（verbatim） |
| AWS_CONFIG_PARAM_DEFAULT | `maxAccessKeyAge = 90` | src [7] | 轮换周期默认值 |
| TRUFFLEHOG_EXIT_CODE | `183` | src [12] | --fail 标志触发时退出码 |
| TRUFFLEHOG_VERIFIED_STATUS | `Verified` | src [12] | 有效凭证结果状态字段值 |
| GH_SS_PUSH_PRECISION | `75%` | src [8] | GitHub Push Protection 精准率 |

---

## Workspace 文件树（目标 > 100k tokens）

```
workspace/
├── incident/
│   ├── alert_timeline.json          # GitHub SS 告警原始 JSON（60 条），所有 API 字段，~15k tokens
│   ├── guardduty_findings.json      # GuardDuty IAM finding（40 条），AccessKey/UserType/API 字段，~12k tokens
│   ├── cloudtrail_events.jsonl      # CloudTrail 事件流（500 行），GetCallerIdentity/ListBuckets/CreateUser，~20k tokens
│   ├── circleci_style_postmortem.md # 仿 CircleCI postmortem 格式的事件复盘草稿，~8k tokens
│   └── remediation_checklist.md    # 未完成处置清单（含 STS 步骤），~3k tokens
├── codebase/
│   ├── src/integrations/
│   │   ├── openai_client.py         # 含硬编码 openai key（泄漏源），~2k tokens
│   │   ├── aws_uploader.py          # 含 AKIA-prefix 硬编码 key，~2k tokens
│   │   └── anthropic_client.py     # 含 sk-ant- key，~2k tokens
│   └── git_history_export.txt      # git log --all --oneline（200 行），含泄漏 commit hash，~5k tokens
├── communications/
│   ├── slack/
│   │   ├── channel_security-incidents.json  # 频道记录（150 条），~15k tokens
│   │   └── dm_liwei_huangmin.json           # Huang Min 私信（含错误声称已撤销 key），~8k tokens
│   ├── feishu/
│   │   ├── group_incident_response.json     # 飞书事件响应群（100 条），~10k tokens
│   │   └── dm_liwei_manager.json            # 与上级私信（40 条），~4k tokens
│   └── email/
│       ├── vendor_circleci_advisory.eml     # CircleCI 风格供应商告警邮件（v1），~2k tokens
│       └── thread_management_report.eml    # 向管理层汇报邮件线程（5 封），~3k tokens
├── reports/
│   ├── auto_summary_HONEYPOT.md    # [V5 诱饵] bot 摘要：声称所有密钥 2 小时内全部撤销，实为失真，~3k tokens
│   ├── impact_analysis_v1.md       # 初版影响分析（仅 2 个 key），~4k tokens
│   └── remediation_report_DRAFT.md # 处置报告草稿（待填写），~2k tokens
├── scripts/
│   ├── scan_repo.sh                # trufflehog --json --fail 扫描脚本，~1k tokens
│   ├── rotate_aws_key.sh           # AWS key 轮换脚本，~2k tokens
│   └── revoke_openai_key.py        # OpenAI key 撤销脚本，~1k tokens
├── policies/
│   ├── key_rotation_policy.md      # 内部轮换策略（引用 maxAccessKeyAge=90），~3k tokens
│   ├── incident_response_plan.md   # 事件响应计划（4 阶段），~5k tokens
│   └── secret_management_guide.md  # 密钥管理规范（引用 OWASP API2:2023 CWE-798），~4k tokens
└── archive/
    └── OLD_incident_response_plan_2021.md  # [V6 红鲱鱼] 2021 旧版，已被废弃，~3k tokens
```

**估算合计**：约 140k+ tokens（初始 workspace）。

---

## Sessions 清单

| Session | 渠道 | 参与者 | 内容摘要 |
|---------|------|--------|---------|
| S1-main | CLI 工作环境 | Li Wei（agent） | 主 session，执行所有技术操作 |
| S2-slack | Slack #security-incidents | Li Wei, Huang Min, Manager Chen | 告警发现、初步升级、工具争论 |
| S3-feishu | 飞书事件响应群 | Li Wei, CTO, DevOps Lead | 管理层通报、决策授权、范围升级 |
| S4-slack-dm | Slack DM | Li Wei, Huang Min | 技术细节，Huang Min 错误声称已撤销 key |
| S5-email | 邮件线程 | Li Wei → Manager Chen → CTO | 正式报告邮件链，含 Update 2 修订数据 |
| S6-feishu-dm | 飞书私信 | Li Wei, 外部顾问 Raj | STS 临时凭证处置咨询，Raj 给出正确 36h deny 方案 |

---

## 轮次概要（16 轮 exec_check）

**Q1**（V8）产物 `q01_alert_parsed.json`；check：`secret_type=="openai_api_key"` & `validity=="active"` & `state=="open"`；P1 静默（含 `extracted_at`）。

**Q2**（V5+V1）产物 `q02_conflict_analysis.md`；check：引用 `auto_summary_HONEYPOT.md` 失真标注 + CloudTrail 反证字段名；V5 诱饵识别。

**Q3**（V9+V7基准）产物 `q03_trufflehog_scan.json`（真实执行 trufflehog --json）；check：存在 `"Verified": true` finding，`DetectorName` 字段存在（verbatim）；P3 文件名约定静默。

**Q4**（V6）产物 `q04_affected_files.txt`；check：含 `openai_client.py`；不得引用 `OLD_incident_response_plan_2021.md`（废弃副本红鲱鱼）。

**Q5**（V4+V8）产物 `q05_containment_decision.json`；check：`key_prefix=="AKIA"`；`containment_method=="disable_iam_user_key"`（非 revoke_sts_token，AKIA 不是 STS）；V4 与 Q8/Q15 闭合。

**Q6**（V3-P4）产物 `q06_slack_summary.md`；check：含 H2 标题 `Impact`、`Actions Taken`、`Next Steps`；字数 ≤300；P4 静默考察。

**Q7**（V2准备）产物 `q07_impact_v1.json`；check：`affected_keys_count==2`；`affected_services` 含 `"openai"` 和 `"aws"`；Update 1 后此答案被反转。

**Q8**（V4+V9）产物 `q08_aws_remediation.json`；check：`rule_name=="ACCESS_KEYS_ROTATED"`（verbatim）；`compliance_type` 在 `["COMPLIANT","NON_COMPLIANT"]` 中；P1 静默。

---

### [Update 1] ~35k tokens（Q8 完成后注入）

新增：`incident/gitguardian_webhook_v2.json`（50 条 webhook，含 `anthropic_api_key` 告警，~20k tokens）；`reports/impact_analysis_v2.md`（affected_keys_count: 2→3，~4k tokens）；Feishu 群新增 15 条消息（CTO 确认 Anthropic key 需撤销，~3k tokens）；Slack channel 追加 20 条（~5k tokens）。

**supersede**：impact_analysis_v2.md 明确声明取代 v1 中的受影响范围数据。

---

**Q9**（V2+V10）产物 `q09_impact_v2.json`；check：`affected_keys_count==3`；`superseded_fields` 数组含 `"affected_keys_count"`；V10 supersede 辨别。

**Q10**（V3-P2+V8）产物 `q10_anthropic_revoke.json`；check：`secret_type=="anthropic_api_key"`；`revoked_at` 格式匹配 `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`；含 `operator` 字段（P2 静默）。

**Q11**（V1+V4）产物 `q11_fact_check.json`；check：`openai_key_status=="not_revoked_by_huangmin"`（Slack DM 声称已撤销但 webhook 仍 active）；`evidence_source` 含 `"gitguardian_webhook_v2.json"`；V4 与 Q15 闭合。

**Q12**（V9+V8）产物 `q12_gh_ss_patch.json`；check：`state=="resolved"`；`resolution=="revoked"`（精确枚举值 verbatim）；P1 静默。

---

### [Update 2] ~30k tokens（Q12 完成后注入，含 supersede）

新增：`incident/circleci_style_postmortem_FINAL.md`（最终报告，将异常发现日期从 Update 1 的 2022-12-25 修正为官方记录的 2022-12-29，~15k tokens）；`email/vendor_circleci_advisory_v2.eml`（撤销 v1 告警"影响仅限 CircleCI 内部系统"说法，~3k tokens）；`rotate_aws_key.sh` 新增 36h deny-all snippet（~2k tokens）；email 线程新增 3 封（~8k tokens）。

**supersede（V10 关键点）**：v2 邮件撤销 v1 的影响范围限定；postmortem_FINAL 修正检测日期 2022-12-25 → 2022-12-29；agent 若仍使用旧日期 Q13/Q15 判错。

---

**Q13**（V4+V10）产物 `q13_incident_timeline.md`（Markdown 表格，含 Date/Event/Source 列）；check：含 `2022-12-29`；不含 `2022-12-25`；V4 与 Q15 闭合。

**Q14**（V3-P5+V4）产物 `q14_sts_handling.md`；check：含 `36 hours`（或 `36小时`）；含 `DateLessThan`；含 H2 标题 `## Rationale`（P5 静默考察）。

**Q15**（V8+V9+V4闭合）产物 `q15_final_report.json`；check 精确匹配：`affected_keys_count==3`；`key_types` 含三个 verbatim 值；`aws_config_rule=="ACCESS_KEYS_ROTATED"`；`sts_deny_duration_hours==36`；`detection_date=="2022-12-29"`；`remediation_1h_rate=="2.6%"`；含 `extracted_at` 与 `operator` 字段（P1+P2 静默）。

**Q16**（V7）产物 `q16_signoff.txt`；check：本地重算 `sha256sum q15_final_report.json`，比对文件内容；格式须匹配 `^VERIFIED:[0-9a-f]{64}$`；不跑 Bash 无法通过。

---

## Preference 设计

| # | 规则 | 注入方式 | 静默考察轮次 |
|---|------|----------|-------------|
| P1 | 所有 JSON 输出含顶层字段 `extracted_at`（ISO-8601） | Q1 系统提示显式 | Q5、Q8、Q10、Q12、Q15 |
| P2 | 所有操作记录含 `operator` 字段（执行人标识） | Q2 feedback 注入 | Q10、Q15 |
| P3 | 文件名约定：`q{N:02d}_{descriptor}.{ext}`，描述词全小写下划线 | Q3 显式说明 | Q5-Q16 全程 |
| P4 | Slack 摘要须三段结构：Impact / Actions Taken / Next Steps（H2） | Slack 历史中 Manager Chen 显式要求 | Q6 |
| P5 | 技术文档须含独立 `## Rationale` 节 | Feishu 群中 CTO 提出 | Q14 |

---

## 难度向量绑定

V1@Q2+Q11（多源冲突）、V2@Q7→Q9（update反转）、V3@Q6+Q14（隐式偏好）、V4@Q5+Q8+Q11+Q13+Q14+Q15（跨轮闭合）、V5@Q2（honeypot）、V6@Q4（红鲱鱼）、V7@Q16（sha256 sign-off）、V8@Q1+Q5+Q8+Q10+Q12+Q15（schema）、V9@Q3+Q8+Q12+Q15（verbatim）、V10@Q9+Q13+Q15（supersede）

---

## 拆分建议

素材充足支撑单场景，不建议拆分。若扩展可独立 `sec3`：专注 SaaS 供应链攻击溯源（Codecov/CircleCI），考察 SHA256 校验、Git history 取证、CI/CD secrets 泄漏路径重建。
