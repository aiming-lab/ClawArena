# eng5 · CI/CD 流水线配置修复

## 场景叙事背景

某中型 SaaS 公司 DevOps 团队正在维护一套混合 CI/CD 体系：GitHub Actions 用于主仓库的构建与测试，GitLab CI 用于内部基础设施仓库的部署流水线。近期团队扩张，多名工程师在短时间内对 workflow 配置进行了修改，引入了一系列配置错误：

- 缓存 key 未使用 `hashFiles()` 导致每次构建均为 cache miss；
- `actions/cache` 仍使用已废弃的 v2 版本，2025 年 3 月后全部失败；
- 矩阵策略 `exclude` 规则配置错误，冗余 job 未被过滤；
- 并发控制使用了禁止组合（`queue: max` + `cancel-in-progress: true`）；
- OIDC 部署 job 缺少 `id-token: write` 权限，JWT 无法生成；
- GitLab CI `needs` 引用了因 `rules` 条件排除的 job，未加 `optional: true`；
- GitLab CI `cache:policy` 错误使用 `pull-push`（并行测试 job 应用 `pull`）；
- `artifacts:expire_in` 使用了非法格式字符串。

Agent 扮演高级 DevOps 工程师，被指派在多 session 中系统性地审查、修复这些配置文件，并产出结构化审计报告。任务横跨 GitHub Actions 与 GitLab CI 两套体系，存在多源信息冲突、动态 update 反转、preference 静默考察等难度向量。

---

## 真实来源链接表

| # | 来源标题 | URL | 类型 |
|---|---------|-----|------|
| S1 | Workflow syntax for GitHub Actions | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | official_doc |
| S2 | Dependency caching reference - GitHub Actions | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | official_doc |
| S3 | Running variations of jobs in a workflow (matrix) | https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow | official_doc |
| S4 | Control the concurrency of workflows and jobs | https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency | official_doc |
| S5 | Assigning permissions to jobs - GitHub Actions | https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs | official_doc |
| S6 | actions/cache Deprecation Notice (Discussion #1510) | https://github.com/actions/cache/discussions/1510 | postmortem |
| S7 | Notification of upcoming breaking changes in GitHub Actions | https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/ | news |
| S8 | CI/CD YAML syntax reference - GitLab Docs | https://docs.gitlab.com/ci/yaml/ | official_doc |
| S9 | Caching in GitLab CI/CD | https://docs.gitlab.com/ci/caching/ | official_doc |
| S10 | Make jobs start earlier with needs - GitLab Docs | https://docs.gitlab.com/ci/yaml/needs/ | official_doc |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|-----|---------|------|
| `cache_key_max_length` | 512 characters | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | cache key 超过 512 字符即失败 |
| `cache_repo_default_limit` | 10 GB | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | 单仓库默认缓存上限 |
| `cache_retention_days` | 7 days | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | 超过 7 天未使用自动清除 |
| `cache_rate_limit_upload` | 200 uploads/minute | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | 每仓库上传速率限制 |
| `cache_rate_limit_download` | 1500 downloads/minute | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | 每仓库下载速率限制 |
| `actions_cache_deprecated_deadline` | March 1, 2025 | https://github.com/actions/cache/discussions/1510 | v1/v2 停服截止日，未升级即失败 |
| `actions_cache_min_version` | v4.2.0 / v3.4.0 | https://github.com/actions/cache/discussions/1510 | 最低兼容版本 |
| `actions_cache_runner_min` | 2.320.1 | https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/ | self-hosted runner 最低版本 |
| `concurrency_forbidden_combo` | queue:max + cancel-in-progress:true | https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency | 禁止组合，导致 validation error |
| `concurrency_queue_max_pending` | 100 | https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency | queue:max 最大 pending runs |
| `permission_scopes_list` | actions,attestations,checks,contents,deployments,id-token,issues,packages,pages,pull-requests,security-events,statuses | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | 完整权限 scope 列表 |
| `permission_unspecified_default` | none | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | 未声明的 scope 默认为 none |
| `oidc_required_permission` | id-token: write | https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs | OIDC JWT 生成必须 |
| `deployments_write_deadline` | April 1, 2025 | https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/ | deployments:read 不再允许审批/拒绝部署 |
| `gitlab_cache_key_files_max` | 2 file paths | https://docs.gitlab.com/ci/yaml/ | cache:key:files 最多 2 个路径 |
| `gitlab_cache_policy_default` | pull-push | https://docs.gitlab.com/ci/yaml/ | 默认策略；并行 job 应改用 pull |
| `gitlab_artifacts_expire_in_never` | never | https://docs.gitlab.com/ci/yaml/ | artifacts:expire_in 合法值之一 |
| `gitlab_needs_optional_syntax` | needs: [{job: "name", optional: true}] | https://docs.gitlab.com/ci/yaml/needs/ | rules 条件排除时必须加 optional:true |
| `matrix_fail_fast_default` | true | https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow | fail-fast 默认值为 true |
| `hashFiles_example` | ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }} | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | 正确 cache key 示例 |

---

## Workspace 文件树与体量规划（目标 >100k tokens）

```
workspace/
├── .github/
│   └── workflows/
│       ├── ci.yml                  # 主 CI workflow（含错误配置，~2000行）
│       ├── deploy.yml              # 部署 workflow（OIDC 配置，~1500行）
│       ├── release.yml             # 发版 workflow（矩阵策略，~1200行）
│       └── nightly.yml             # 夜间构建（并发控制，~800行）
├── .gitlab-ci.yml                  # GitLab CI 主配置（~1500行）
├── .gitlab/
│   ├── ci/
│   │   ├── build.yml               # build stage 配置（~800行）
│   │   ├── test.yml                # test stage 配置（~1000行）
│   │   └── deploy.yml              # deploy stage 配置（~800行）
│   └── scripts/
│       ├── cache_key_gen.sh        # 缓存 key 生成脚本（~200行）
│       └── artifact_check.sh       # 制品校验脚本（~300行）
├── docs/
│   ├── cicd_architecture.md        # CI/CD 架构文档（~3000行）
│   ├── workflow_history.md         # 变更历史（~2000行）
│   ├── known_issues.md             # 已知问题列表（~1500行）
│   └── runbook.md                  # 运维手册（~4000行）
├── audit/
│   ├── workflow_audit_template.json # 审计报告模板（~500行）
│   └── previous_audit_2024.json    # 2024年审计（~2000行，含失真摘要）
├── scripts/
│   ├── validate_workflows.py       # 本地校验脚本（~600行）
│   ├── cache_stats.py              # 缓存统计脚本（~400行）
│   └── matrix_checker.py          # 矩阵配置检查（~400行）
├── package-lock.json               # Node 依赖锁文件（~50000行，真实体量）
├── Gemfile.lock                    # Ruby 依赖锁文件（~3000行）
├── yarn.lock                       # Yarn 锁文件（~30000行）
└── chat_history/
    ├── slack_devops_channel.jsonl  # Slack DevOps 频道记录（~5000行）
    ├── feishu_dm_alice.jsonl       # 飞书 DM：Alice（高级工程师）（~2000行）
    ├── email_thread_cicd.eml       # 邮件线程：CI/CD 问题讨论（~1500行）
    └── github_issue_287.md         # GitHub Issue #287（缓存失败）（~1000行）
```

**体量估算**：
- 锁文件（package-lock.json + yarn.lock）约 ~60k tokens
- workflow YAML 文件集合约 ~15k tokens
- 文档集合约 ~25k tokens
- 聊天记录集合约 ~15k tokens
- 脚本与审计 JSON 约 ~10k tokens
- **合计 ~125k tokens（满足 >100k 要求）**

---

## Session 清单（1 主 + 5 多渠道）

| Session ID | 渠道 | 参与者 | 内容摘要 |
|-----------|------|--------|---------|
| S-main | Claude Code（主 session） | Agent + User(DevOps Lead) | 系统性审查并修复所有 workflow 配置，产出结构化审计报告 |
| S-slack | Slack #devops-cicd | Alice（高级工程师）、Bob（DevOps）、Charlie（SRE） | 缓存失效问题讨论；Alice 提到旧 v2 cache action，Bob 提出 hashFiles 方案（但 key 格式有误）；含 bot 自动摘要（失真版） |
| S-feishu | 飞书 DM | User → Agent | 用户私信要求保持 YAML 缩进风格为 2 空格，不使用 tab；并要求所有修改前备份原文件 |
| S-email | Email thread | DevOps Lead → Team | 邮件线程讨论 deployments 权限变更（April 2025 deadline），包含旧版 workflow 截图（已废弃配置） |
| S-github-issue | GitHub Issue #287 | 多名工程师 | cache miss 问题：一条评论正确指出应用 hashFiles，另一条评论错误使用 github.sha 作为 key（冲突信息） |
| S-feishu-group | 飞书群「CI/CD 治理」 | 多名工程师 | GitLab CI needs 报错讨论；有人提出错误方案（删除 needs）而非正确方案（加 optional:true）；另有 legacy archive 的引用（红鲱鱼） |

---

## 轮次概要（16 轮，全部 exec_check）

### Q1 — 环境探查与初步清单
- **意图**：agent 读取 workspace，枚举所有 workflow 文件，输出文件清单 JSON
- **产物**：`audit/file_inventory.json`（含文件路径、行数、最后修改时间）
- **check 锚点**：文件数量 = 7（4个 .github/workflows + 3个 .gitlab/ci/），JSON schema 校验
- **难度向量**：V8（schema-by-shape）
- **update/preference**：无

### Q2 — actions/cache 版本审查
- **意图**：识别所有 workflow 中 `actions/cache` 的版本引用，标记废弃版本
- **产物**：`audit/cache_version_report.json`（含 file、line、current_version、is_deprecated、required_version 字段）
- **check 锚点**：is_deprecated=true 的版本为 v2，required_version="v4.2.0" 或 "v3.4.0"（精确匹配 S6 锚点）
- **难度向量**：V9（verbatim 字段引用）、V8（schema 严格校验）
- **update/preference**：触发 preference P1（JSON 字段名用 snake_case）

### Q3 — cache key 错误修复（GitHub Actions）
- **意图**：修复 ci.yml 中使用 `github.sha` 作为 cache key 的错误，改为 hashFiles
- **产物**：修改后的 `.github/workflows/ci.yml`（同时备份原文件为 `.github/workflows/ci.yml.bak`）
- **check 锚点**：修复后 key 包含 `hashFiles('**/package-lock.json')`，不含 `github.sha`；备份文件存在（preference P3）
- **难度向量**：V1（多源冲突：Slack 中 Bob 提出的错误 key 格式需辨别）、V5（bot 摘要失真）
- **update/preference**：触发 P3（修改前备份）

### Q4 — restore-keys 配置修复
- **意图**：为修复后的 cache action 添加正确的 restore-keys（从最具体到最宽泛）
- **产物**：更新 `.github/workflows/ci.yml` 中 restore-keys 配置
- **check 锚点**：restore-keys 为 3 层（`runner.os-build-`、`runner.os-`），顺序正确（精确匹配 S2 锚点中的模式）
- **难度向量**：V4（跨轮数值闭合：Q3 写入的 key prefix 必须与 Q4 restore-keys 一致）
- **update/preference**：无

### Q5 — 并发控制错误修复
- **意图**：修复 nightly.yml 中 `queue: max` + `cancel-in-progress: true` 的禁止组合
- **产物**：修改后的 `.github/workflows/nightly.yml`；并生成 `audit/concurrency_fix.md`（说明禁止原因）
- **check 锚点**：修复后不同时含 `queue: max` 和 `cancel-in-progress: true`；audit 文件引用官方说明（"not allowed and will result in a workflow validation error"）
- **难度向量**：V9（verbatim 引用官方错误描述）、V8（YAML 结构校验）
- **update/preference**：触发 P2（Markdown 文档使用中英文双语标题）

### Q6 — 矩阵策略 exclude 修复
- **意图**：修复 release.yml 矩阵中错误的 exclude 配置（exclude 应过滤 windows+node12 组合，但当前仅匹配了 os 字段）
- **产物**：修改后的 `.github/workflows/release.yml`
- **check 锚点**：exclude 块包含完整的 `{os: "windows-latest", version: 12}` 对象；修复后矩阵 job 数量减少 2（精确）
- **难度向量**：V4（矩阵 job 数量在 Q6 写入，Q12 校验报告中须一致）
- **update/preference**：无

### Q7 — OIDC 权限修复
- **意图**：为 deploy.yml 的 deploy job 添加缺少的 `id-token: write` 权限
- **产物**：修改后的 `.github/workflows/deploy.yml`
- **check 锚点**：deploy job 的 permissions 块包含 `id-token: write`；同时 `contents: read` 保留（不能删除）
- **难度向量**：V9（精确字段名引用）、V3（preference 静默考察：P1 snake_case 字段名）
- **update/preference**：触发 P1 静默考察

### Q8 — deployments 权限更新（Update 1 触发）
- **意图**：基于 Update 1 注入的邮件（April 2025 deadline 已到，deployments:read 不再允许审批），更新 deploy.yml 中的 deployments 权限为 write
- **产物**：更新 `.github/workflows/deploy.yml` + `audit/permissions_changelog.json`
- **check 锚点**：`deployments: write`（精确）；changelog 中包含 deadline 字段值 "2025-04-01"
- **难度向量**：V2（Update 1 反转：此前 deployments:read 已被认为"够用"，现须改为 write）、V4（跨轮闭合：Q7 设置的 id-token:write 须保留）
- **update/preference**：Update 1 注入

### Q9 — GitLab CI cache:policy 修复
- **意图**：将 GitLab CI test stage 中并行测试 job 的 cache:policy 从 `pull-push` 改为 `pull`
- **产物**：修改后的 `.gitlab/ci/test.yml`
- **check 锚点**：policy 字段值精确为 `pull`（而非 pull-push）；build job 的 policy 保持 pull-push
- **难度向量**：V9（verbatim 字段名）、V6（archive 目录中存在旧版 test.yml 仍用 pull-push，是红鲱鱼）
- **update/preference**：触发 P4（GitLab CI 配置按 stage 拆分文件）

### Q10 — GitLab CI cache:key:files 修复
- **意图**：修复 `.gitlab/ci/build.yml` 中 cache:key:files 超过 2 个路径的错误（当前有 3 个路径）
- **产物**：修改后的 `.gitlab/ci/build.yml`；`audit/gitlab_cache_fix.md`
- **check 锚点**：cache:key:files 数组长度 ≤ 2（精确）；保留 Gemfile.lock 和 yarn.lock，移除第三个
- **难度向量**：V8（schema 严格校验 array length）、V5（honeypot：飞书群中有人建议合并 3 个文件哈希为字符串拼接，这是错误做法）
- **update/preference**：无

### Q11 — GitLab CI needs + optional 修复（Update 2 触发，Supersede Update 1 的部分内容）
- **意图**：修复 `.gitlab/ci/test.yml` 中 unit_test job needs compile，但 compile 因 rules 条件排除而报错
- **产物**：修改后的 `.gitlab/ci/test.yml`；`audit/needs_fix_report.json`
- **check 锚点**：needs 条目包含 `optional: true`（精确字段名）；不能删除 needs 引用（错误方案）
- **难度向量**：V10（Supersede：Update 2 注入新的 compile job rules 定义，替代 Update 1 中的旧版本，须基于新版本而非旧版本修复）、V2（Update 反转）
- **update/preference**：Update 2 注入（supersede Update 1 中的 GitLab pipeline 部分）

### Q12 — artifacts:expire_in 格式修复
- **意图**：修复 `.gitlab-ci.yml` 中 artifacts:expire_in 使用非法格式（如 "30d" 应改为 "30 days"）
- **产物**：修改后的 `.gitlab-ci.yml`
- **check 锚点**：expire_in 值精确为 `"30 days"` 或合法格式（不可为 "30d"）；`never` 也合法（V9）
- **难度向量**：V9（verbatim 格式规范）、V8（格式校验）
- **update/preference**：P2 静默考察（文档注释须有双语）

### Q13 — 综合审计报告生成（中期）
- **意图**：基于 Q1-Q12 的所有修复，生成结构化审计报告
- **产物**：`audit/cicd_audit_report.json`（含 fixes 数组、每项含 file/issue_type/old_value/new_value/reference_url）
- **check 锚点**：fixes 数组长度 ≥ 8；每项 reference_url 可回溯到真实文档 URL（V9）；数值与前轮一致（V4）
- **难度向量**：V4（跨轮闭合）、V9（reference_url verbatim）、V8（schema 校验）
- **update/preference**：P1/P3 静默考察

### Q14 — 验证脚本编写
- **意图**：编写 `scripts/validate_workflows.py`，能本地检测 cache key 是否含 hashFiles、concurrency 禁止组合、权限缺失
- **产物**：更新 `scripts/validate_workflows.py`（可执行，输出结构化结果）
- **check 锚点**：脚本对故意引入的错误 workflow 输出 FAIL；对修复后的 workflow 输出 PASS
- **难度向量**：V7（脚本输出须含校验 token，下轮用）
- **update/preference**：P5（代码文件头须含版本号注释 # version: X.Y）

### Q15 — SHA256 sign-off token 生成
- **意图**：对 `audit/cicd_audit_report.json` 计算 sha256，写入 `audit/signoff.txt`（格式：`VERIFIED:<sha256>`）
- **产物**：`audit/signoff.txt`（内容：`VERIFIED:<64位十六进制>`）
- **check 锚点**：check 脚本本地重算 sha256 比对，必须精确匹配；格式必须为 `VERIFIED:` + 64 位小写十六进制
- **难度向量**：V7（Bash-sha256 sign-off，不跑 Bash 拿不到正确值）
- **update/preference**：P3 静默考察（须有备份）

### Q16 — 最终合规性声明
- **意图**：生成 `audit/compliance_statement.md`，声明所有修复已完成，引用关键锚点（版本号、deadline、字段名）
- **产物**：`audit/compliance_statement.md`（Markdown，含中英文双语标题，引用真实 URL）
- **check 锚点**：文档包含字符串 "v4.2.0"、"2025-03-01"、"id-token: write"、"optional: true"（verbatim）；sha256 与 Q15 一致
- **难度向量**：V4（跨轮闭合）、V9（verbatim 字符串）、V3（P2 preference 双语标题静默考察）
- **update/preference**：P2/P1 双重静默考察

---

## Update 设计

### Update 1（在 Q7 结束后、Q8 前注入）

**注入内容**：
- 新 session 消息：邮件线程（DevOps Lead 转发 GitHub changelog），提示 "deployments:read fine-grained permission will no longer allow reviewing/approving deployments effective April 1, 2025 — please update all affected workflows to use deployments:write"
- 新 workspace 文件：`chat_history/email_update_apr2025.eml`（约 30k tokens，含 GitHub 官方 changelog 全文引用、团队讨论、受影响 workflow 清单）

**体量来源**：官方 changelog 全文 + 团队内部邮件线程（含历史邮件引用展开）约 ~35k tokens

**对后续轮次的影响**：Q8 的正确答案从 `deployments: read` 变为 `deployments: write`；须与 Q7 的 `id-token: write` 同时保留。

### Update 2（在 Q10 结束后、Q11 前注入）—— Supersede Update 1 的部分内容

**注入内容**：
- 新 session 消息：飞书群消息，工程师 David 指出"刚才邮件线程里附的 compile job rules 是旧版，已经在 MR #445 中更新了，新版 compile job 只在 `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` 时运行（非全 branch），请以新版为准"
- 新 workspace 文件：`.gitlab/ci/build_updated.yml`（含正确的新版 compile job rules 定义，约 40k tokens，包含完整 GitLab CI pipeline 片段与详细注释）
- 新 workspace 文件：`chat_history/feishu_group_nov_update.jsonl`（飞书群历史记录，约 30k tokens）

**Supersede 说明**：Update 1 邮件中附带的 compile job rules 为旧版（rules: `$CI_COMMIT_BRANCH`），Update 2 明确撤销并替换为新版（rules: `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`）。Agent 须识别这是替代而非叠加，Q11 的修复须基于新版 rules。

**体量来源**：完整 GitLab CI pipeline YAML（含注释）+ 飞书群记录约 ~70k tokens

---

## Preference 设计（4 条）

| ID | 偏好内容 | 注入方式 | 静默考察轮次 |
|----|---------|---------|------------|
| P1 | JSON 输出中所有字段名使用 snake_case（禁用 camelCase） | Q2 产物 check 反馈显式注入 | Q8、Q13 |
| P2 | Markdown 文档中所有一级/二级标题使用中英文双语（格式：`# 中文标题 / English Title`） | 飞书 DM（S-feishu session）显式说明 | Q5、Q12、Q16 |
| P3 | 修改任何配置文件前，必须先备份原文件（在同目录下加 `.bak` 后缀） | Q3 任务说明中显式提及 | Q7、Q15 |
| P4 | GitLab CI 配置须按 stage 拆分为独立文件（禁止把所有 job 写在根 .gitlab-ci.yml） | Q9 任务上下文中通过 issue 讨论隐式暗示 | Q10、Q11 |
| P5 | 所有 Python 脚本文件头须包含版本号注释（格式：`# version: X.Y`） | Q14 任务说明中显式提及 | 无（Q14 显式考察） |

---

## 拆分建议

素材丰富度评估：**可行，无需拆分**。当前场景聚焦 GitHub Actions + GitLab CI 双平台配置修复，两者形成对比维度，共同支撑 16 轮 exec_check。体量估算约 125k tokens 初始 workspace，2 次 update 各 >30k tokens，满足所有要求。若未来需要扩展，可考虑拆出「GitLab CI 高级特性（DAG/parent-child pipeline/include）」作为独立场景。

---

## 难度向量分配总结

| 向量 | 绑定轮次 |
|------|---------|
| V1 多源信息冲突综合 | Q3（Slack 中错误 cache key 与正确文档冲突） |
| V2 动态 Update 反转 | Q8（Update1：deployments 权限变更）、Q11（Update2：compile rules 替换） |
| V3 隐式 preference 静默考察 | Q7（P1）、Q12（P2）、Q16（P2+P1） |
| V4 跨轮数值/事实闭合 | Q4（key prefix 闭合）、Q6（矩阵 job 数闭合）、Q13/Q16（sha256 闭合） |
| V5 失真自动摘要诱饵 | Q3（Slack bot 摘要失真）、Q10（飞书群错误建议） |
| V6 废弃副本红鲱鱼 | Q9（archive 目录中旧版 test.yml） |
| V7 Bash-sha256 sign-off | Q15 |
| V8 schema-by-shape 严格校验 | Q1、Q2、Q6、Q10、Q13 |
| V9 真实来源字段 verbatim 引用 | Q2、Q5、Q7、Q9、Q11、Q12、Q13、Q16 |
| V10 supersede 辨别 | Q11（Update2 supersede Update1 的 compile rules 部分） |
