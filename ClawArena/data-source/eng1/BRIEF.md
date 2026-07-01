# BRIEF：eng1 — psf/requests CVE-2024-47081 Bug 修复与回归测试

## 场景叙事背景

**场景设定：**
Agent 受雇于一家中型 SaaS 企业的平台安全工程团队。团队内部 Python 服务广泛使用 `psf/requests` 库，版本锁定在 `2.32.3`。安全团队在 2025 年 6 月初收到外部披露通知：CVE-2024-47081 证实 `requests < 2.32.4` 存在 `.netrc` 凭证泄露漏洞，根因函数为 `get_netrc_auth`（`src/requests/utils.py`），使用 `ri.netloc.split(':')[0]` 提取主机名，可被精心构造的 URL（如 `http://example.com:@evil.com/`）欺骗，将 `.netrc` 中为 `example.com` 存储的凭证发送给 `evil.com`。

Agent 的任务链：
1. 在内部 fork（`company/requests-patched`）中复现漏洞、定位根因；
2. 编写对应回归测试并验证失败（红测试）；
3. 应用官方修复（`ri.hostname` 替换 `ri.netloc.split(':')[0]`），验证测试通过（绿测试）；
4. 补充影响面分析报告、整理 changelog 条目；
5. 中途接收 update（安全团队补充另一个关联漏洞 CVE-2023-32681 的修复验证需求，以及撤销一条错误的兼容性建议），Agent 需正确辨别并响应。

所有产物通过 `exec_check` shell 脚本校验。

---

## 真实来源链接表

| # | 来源类型 | URL | 核实状态 |
|---|----------|-----|----------|
| S1 | GitHub Issue | https://github.com/psf/requests/issues/6964 | 已 WebFetch 核实 |
| S2 | GitHub PR (官方修复) | https://github.com/psf/requests/pull/6965 | 已 WebFetch 核实 |
| S3 | GitHub PR (替代修复) | https://github.com/psf/requests/pull/6963 | 已 WebFetch 核实 |
| S4 | NVD CVE 详情 | https://nvd.nist.gov/vuln/detail/CVE-2024-47081 | 已 WebFetch 核实 |
| S5 | psf/requests HISTORY.md | https://github.com/psf/requests/blob/main/HISTORY.md | 已 WebFetch 核实 |
| S6 | 修复后 utils.py（主线） | https://raw.githubusercontent.com/psf/requests/main/src/requests/utils.py | 已 WebFetch 核实 |
| S7 | 修复后 test_utils.py（主线） | https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py | 已 WebFetch 核实 |
| S8 | Miggo 漏洞数据库 | https://www.miggo.io/vulnerability-database/cve/CVE-2024-47081 | 已 WebFetch 核实 |

---

## Ground-Truth 锚点表

| 锚点名 | 精确值 | 来源 URL | 备注 |
|--------|--------|----------|------|
| CVE 编号 | `CVE-2024-47081` | S4 | NVD 官方登记 |
| GHSA 编号 | `GHSA-9hjg-9r4m-mvj7` | S2 | GitHub Security Advisory |
| 受影响版本范围 | `< 2.32.4` | S4/S8 | pip 生态，requests |
| 修复版本 | `2.32.4` | S5 | HISTORY.md，发布日 2025-06-10 |
| 根因函数名 | `get_netrc_auth` | S6 | `src/requests/utils.py` 第 180-217 行 |
| 修复前提取主机名代码 | `ri.netloc.split(':')[0]` | S3/S8 | 被替换的脆弱行 |
| 修复后提取主机名代码 | `ri.hostname` | S2/S6 | urlparse 属性，不含 userinfo |
| 恶意 URL 示例 | `http://example.com:@evil.com/` | S7 | 测试方法 `test_not_vulnerable_to_bad_url_parsing` |
| 测试断言（漏洞） | `assert auth is None` | S7 | 同上 |
| 测试断言（正常） | `assert auth == ("aaaa", "bbbb")` | S7 | `test_works` 方法 |
| 修复 commit SHA (PR#6965) | `57acb7c26d809cf864ec439b8bcd6364702022d5` | S2 | sethmlarson 提交 |
| 修复 commit SHA (PR#6963) | `5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b` | S3 | awoimbee 提交（被 supersede） |
| CVSS 评分 | `5.3 (MEDIUM)` | S4 | CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N |
| CWE 类型 | `CWE-522` | S4 | Insufficiently Protected Credentials |
| utils.py 总行数（修复后） | `约 1,420 行` | S6 | WebFetch 估算 |
| 关联 CVE（Proxy-Auth 泄露） | `CVE-2023-32681` | S5 | 2.31.0 修复，HISTORY.md |

---

## Workspace 文件树与体量规划（目标 >100k tokens）

```
workspace/
├── README.md                          # 项目背景说明，~2k tokens
├── SECURITY_CONTEXT.md                # 漏洞分析上下文（合成），~8k tokens
├── src/
│   └── requests/                      # 完整 requests 库源码快照（2.32.3）
│       ├── __init__.py                # ~300 行，~1k tokens
│       ├── api.py                     # ~200 行，~0.8k tokens
│       ├── adapters.py                # ~748 行，~3k tokens
│       ├── auth.py                    # ~350 行，~1.5k tokens
│       ├── cookies.py                 # ~600 行，~2.5k tokens
│       ├── exceptions.py              # ~200 行，~0.8k tokens
│       ├── hooks.py                   # ~100 行，~0.4k tokens
│       ├── models.py                  # ~1000 行，~4k tokens
│       ├── sessions.py                # ~800 行，~3k tokens
│       ├── structures.py              # ~300 行，~1k tokens
│       ├── utils.py                   # ~1420 行，~5k tokens（含漏洞版本，关键文件）
│       ├── compat.py                  # ~150 行，~0.6k tokens
│       └── status_codes.py            # ~200 行，~0.8k tokens
├── tests/
│   ├── test_utils.py                  # ~1013 行，~4k tokens
│   ├── test_requests.py               # ~3068 行，~12k tokens
│   ├── test_auth.py                   # ~500 行，~2k tokens
│   ├── test_hooks.py                  # ~200 行，~0.8k tokens
│   ├── test_structures.py             # ~200 行，~0.8k tokens
│   └── conftest.py                    # ~300 行，~1k tokens
├── docs/
│   ├── user/quickstart.rst            # ~800 行，~3k tokens
│   ├── user/authentication.rst        # ~400 行，~1.5k tokens
│   ├── user/advanced.rst              # ~600 行，~2.5k tokens
│   ├── api.rst                        # ~1000 行，~4k tokens
│   └── CHANGES.rst                    # HISTORY.md 完整内容镜像，~5000 行，~20k tokens
├── HISTORY.md                         # 完整 changelog（2.31.0 至今），~3000 行，~12k tokens
├── analysis/
│   ├── vuln_report_draft_v1.md        # 安全分析报告草稿（合成），~5k tokens
│   ├── vuln_report_draft_v2.md        # 第二版（含错误内容，待 supersede），~5k tokens
│   ├── affected_services.json         # 内部受影响服务清单（合成），~2k tokens
│   └── fix_comparison.md              # PR#6963 vs PR#6965 对比（合成），~3k tokens
├── scripts/
│   ├── reproduce_cve.py               # 漏洞复现脚本（合成），~200 行，~0.8k tokens
│   ├── run_regression.sh              # 回归测试运行脚本（合成），~100 行
│   └── check_version.py               # 版本检测脚本（合成），~100 行
├── sessions/
│   ├── slack_channel_security.json    # Slack #security-alerts 频道历史（合成），~8k tokens
│   ├── feishu_dm_engineer.json        # 飞书 DM 工程师讨论（合成），~6k tokens
│   ├── email_thread_1.eml             # 邮件线程：外部披露通知（合成），~4k tokens
│   ├── email_thread_2.eml             # 邮件线程：内部响应（合成），~4k tokens
│   └── github_comments_pr6963.json    # PR#6963 评论历史（合成），~3k tokens
└── pyproject.toml                     # 依赖和项目配置（合成），~0.5k tokens
```

**体量合计估算：**
- 源码快照（requests 2.32.3）：~25k tokens
- 测试文件集：~21k tokens
- 文档（docs/ + HISTORY.md）：~45k tokens
- 分析报告与脚本：~16k tokens
- 多渠道 session 历史：~25k tokens
- **总计：约 132k tokens**（满足 >100k 要求）

---

## Session 清单

| Session ID | 类型 | 平台 | 参与者 | 主要内容 |
|------------|------|------|--------|----------|
| session-main | 主任务 session | Claude Code | Agent + 安全主管 Alice | 主任务指令链，贯穿全程 |
| session-slack | 频道群聊 | Slack #security-alerts | Alice, Bob(SRE), Carol(DevSecOps) | CVE 披露、初步影响评估，含 bot 自动摘要（失真诱饵） |
| session-feishu | 飞书 DM | 飞书 | Agent ↔ Bob | 技术细节讨论，包含 Bob 误引 PR#6963（已被废弃）的红鲱鱼 |
| session-email-1 | 邮件 | Email | 外部安全研究员 → Alice | 原始披露通知，含 PoC 代码 |
| session-email-2 | 邮件 | Email | Alice → 工程团队 | 内部响应决策，含一处错误的版本建议（后被 supersede 撤销） |
| session-github | PR 评论 | GitHub | awoimbee, sethmlarson, sigmavirus24 | PR#6963 vs PR#6965 的技术讨论 |

---

## 15 轮 exec_check 概要

### 前置说明
- `${eval_dir}/${agent_id}/scripts/check_qN.py ${workspace}` 为校验脚本调用约定
- 所有 ground-truth 锚点均取自上述真实来源

---

**Q1 — 漏洞定位报告**
- 意图：Agent 读取 `sessions/slack_channel_security.json`（含失真 bot 摘要：错误声称根因函数为 `build_response`）和 `src/requests/utils.py`，正确定位根因为 `get_netrc_auth`，输出 `analysis/vuln_location.json`
- 产物：`analysis/vuln_location.json`，含字段 `cve_id`, `root_cause_function`, `vulnerable_file`, `vulnerable_line_range`
- check 锚点：`root_cause_function == "get_netrc_auth"`；`vulnerable_file` 含 `utils.py`；`cve_id == "CVE-2024-47081"`
- 难度向量：**V5**（bot 摘要失真诱饵：错误函数名）、**V9**（字段名 verbatim 引用真实来源）
- Preference 涉及：P1（JSON 输出须使用 snake_case 字段名）

---

**Q2 — 受影响版本范围**
- 意图：从多个 session 交叉核实受影响版本范围（Slack 中 Bob 误说 `< 2.32.3`，邮件中正确为 `< 2.32.4`），输出 `analysis/version_impact.json`
- 产物：`analysis/version_impact.json`，含字段 `affected_below`, `fixed_version`, `source`
- check 锚点：`affected_below == "2.32.4"`；`fixed_version == "2.32.4"`
- 难度向量：**V1**（Slack vs 邮件信息冲突）、**V8**（schema-by-shape 精确匹配）

---

**Q3 — 恶意 URL 复现脚本**
- 意图：Agent 在 `scripts/reproduce_cve.py` 中实现 PoC，创建临时 netrc 文件，构造恶意 URL `http://example.com:@evil.com/`，调用漏洞版本 `get_netrc_auth`，断言返回非 `None`（证明漏洞可复现）
- 产物：`scripts/reproduce_cve.py`（可执行，Python）
- check 锚点：文件存在；`python scripts/reproduce_cve.py` 退出码为 `0`；文件中包含字符串 `evil.com`
- 难度向量：**V4**（后续轮次需引用此 URL 保持一致）

---

**Q4 — 红测试编写（验证漏洞存在）**
- 意图：在 `tests/test_utils_regression.py` 中为漏洞版本编写失败测试，测试方法名须为 `test_cve_2024_47081_credential_leak`，断言 `get_netrc_auth("http://example.com:@evil.com/")` 返回 `None`（漏洞版本应返回凭证，测试失败）
- 产物：`tests/test_utils_regression.py`
- check 锚点：文件存在；含 `test_cve_2024_47081_credential_leak`；含 `assert auth is None`；含目标 URL 字符串
- 难度向量：**V9**（测试方法名和断言 verbatim 引用官方 PR#6965 测试）

---

**Q5 — 代码修复实施**
- 意图：Agent 修改 `src/requests/utils.py`，将漏洞行 `host = ri.netloc.split(':')[0]` 替换为 `host = ri.hostname`，并处理 `host is None` 的边界情况
- 产物：修改后的 `src/requests/utils.py`
- check 锚点：文件不含 `netloc.split`；含 `ri.hostname`；含 `if host is None:`；`get_netrc_auth` 函数体完整保留
- 难度向量：**V6**（飞书 session 中 Bob 提供的 PR#6963 diff 与 PR#6965 diff 细节不同，PR#6963 已被 PR#6965 取代，引用旧 PR 即错）

---

**Q6 — 绿测试验证**
- 意图：执行 `python -m pytest tests/test_utils_regression.py -v`，将输出保存到 `test_results/q6_pytest_output.txt`，确认修复后测试通过
- 产物：`test_results/q6_pytest_output.txt`
- check 锚点：文件含 `PASSED`；含 `test_cve_2024_47081_credential_leak`；不含 `FAILED`；不含 `ERROR`
- 难度向量：**V4**（测试名称与 Q4 严格闭合）

---

**Q7 — CVSS 评分记录**
- 意图：读取多渠道 session（邮件中 CVSS 写为 7.5，Slack bot 摘要写为 6.1，NVD 官方为 5.3），输出 `analysis/cve_metadata.json`，含正确 CVSS 评分
- 产物：`analysis/cve_metadata.json`，含字段 `cvss_score`, `cvss_vector`, `cwe_id`, `epss_score`
- check 锚点：`cvss_score == 5.3`；`cwe_id == "CWE-522"`；`cvss_vector` 含 `AV:N/AC:H`
- 难度向量：**V1**（三处冲突数值，需取 NVD 官方）、**V8**（精确数值匹配）

---

**[UPDATE-1 注入：第 8 轮前]**
安全团队发送 update：
1. 新增任务：同步核查 CVE-2023-32681（2.31.0 修复，Proxy-Authorization 头转发漏洞），要求额外产出 `analysis/cve_2023_32681_summary.json`
2. （错误通知）邮件中一封发自 Alice 的信声称 PR#6963 的 commit SHA 是官方修复，要求记录为权威 commit（此为后续 supersede 的目标）
- update 体量：包含新的 email 线程（~15k tokens）+ 新增 Slack 频道消息（~10k tokens）+ CVE-2023-32681 相关 NVD 页面快照文档（~8k tokens），合计 ~33k tokens

---

**Q8 — 关联 CVE 摘要（UPDATE-1 后）**
- 意图：输出 `analysis/cve_2023_32681_summary.json`，记录 CVE-2023-32681 的受影响版本、修复版本、根因
- 产物：`analysis/cve_2023_32681_summary.json`
- check 锚点：`cve_id == "CVE-2023-32681"`；`fixed_version == "2.31.0"`；`root_cause` 含 `Proxy-Authorization`
- 难度向量：**V2**（update 新增任务，需响应新需求）

---

**Q9 — 错误 commit SHA 记录**
- 意图：Agent 按 UPDATE-1 中 Alice 邮件要求，将 PR#6963 commit SHA（`5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b`）写入 `analysis/fix_commit.json` 作为官方修复记录
- 产物：`analysis/fix_commit.json`
- check 锚点：文件存在；含字段 `commit_sha`；值为 `5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b`（此处 agent 应服从 UPDATE-1 的显式指令）
- 难度向量：**V4**（为后续 UPDATE-2 supersede 做铺垫，闭合数值）

---

**[UPDATE-2 注入：第 11 轮前，supersede UPDATE-1 中 commit 记录要求]**
安全主管 Alice 发布勘误：声明 UPDATE-1 中引用的 commit SHA 有误，PR#6963 已被 PR#6965 取代，正确的官方修复 commit SHA 应为 `57acb7c26d809cf864ec439b8bcd6364702022d5`（sethmlarson 的提交）。要求 Agent 更新 `analysis/fix_commit.json` 并标注 supersede 原因。同时，撤销之前 Alice 邮件中关于"2.32.3 包含部分修复"的错误说法。
- update 体量：新 Slack 消息线程（~8k tokens）+ 勘误邮件（~5k tokens）+ PR#6965 完整 review 记录快照（~20k tokens），合计 ~33k tokens

---

**Q10 — supersede 后更新 commit 记录**
- 意图：按 UPDATE-2 勘误，将 `analysis/fix_commit.json` 中 `commit_sha` 改为 `57acb7c26d809cf864ec439b8bcd6364702022d5`，并添加字段 `supersedes_pr` 值为 `"6963"`，`authoritative_pr` 值为 `"6965"`
- 产物：更新后的 `analysis/fix_commit.json`
- check 锚点：`commit_sha == "57acb7c26d809cf864ec439b8bcd6364702022d5"`；`supersedes_pr == "6963"`；`authoritative_pr == "6965"`
- 难度向量：**V10**（supersede 辨别）、**V2**（update 反转信念）

---

**Q11 — changelog 条目生成**
- 意图：生成 `CHANGELOG_ENTRY.md`，格式严格遵循 HISTORY.md 风格（P2 preference：changelog 用 RST 列表格式），含 CVE 编号、修复版本、根因描述、workaround
- 产物：`CHANGELOG_ENTRY.md`
- check 锚点：含 `CVE-2024-47081`；含 `2.32.4`；含 `get_netrc_auth`；含 `trust_env=False`（官方 workaround）；文件为 Markdown 格式
- 难度向量：**V9**（verbatim 引用官方术语）、**V3**（P2 格式偏好静默考察）

---

**Q12 — 影响面 JSON 报告**
- 意图：基于 `analysis/affected_services.json`（workspace 中的内部服务清单），筛选出使用 `.netrc` 文件且 requests 版本 `< 2.32.4` 的服务，输出 `analysis/impact_assessment.json`
- 产物：`analysis/impact_assessment.json`
- check 锚点：JSON 可解析；含 `affected_services` 数组；数组元素数量与 workspace 原始数据一致（精确数字，由合成数据确定后写入 check 脚本）；每元素含 `service_name`, `requests_version`, `uses_netrc`
- 难度向量：**V8**（schema-by-shape 严格校验）、**V4**（数量与前轮产物闭合）

---

**Q13 — 完整测试套件扩展**
- 意图：在 `tests/test_utils_regression.py` 中补充测试方法 `test_legitimate_url_returns_credentials` 和 `test_empty_default_credentials_ignored`（对应 S7 中的三个测试），并运行完整套件，将结果写入 `test_results/q13_full_suite.txt`
- 产物：更新后的 `tests/test_utils_regression.py`；`test_results/q13_full_suite.txt`
- check 锚点：含 `test_legitimate_url_returns_credentials`；含 `test_empty_default_credentials_ignored`；`q13_full_suite.txt` 含 `3 passed`
- 难度向量：**V4**（测试数量与函数名与 Q4/Q6 闭合）、**V3**（P3 preference：测试文件须有 docstring 说明）

---

**Q14 — 安全公告草稿**
- 意图：生成 `docs/SECURITY_ADVISORY_CVE-2024-47081.md`，含 GHSA 编号、CVSS 向量字符串、受影响版本、修复版本、PoC URL 示例、workaround（P4 preference：文档需含"## Workaround"二级标题）
- 产物：`docs/SECURITY_ADVISORY_CVE-2024-47081.md`
- check 锚点：含 `GHSA-9hjg-9r4m-mvj7`；含 `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N`；含 `## Workaround`；含 `trust_env=False`
- 难度向量：**V9**（GHSA 编号、CVSS 向量 verbatim 引用）、**V3**（P4 文档结构偏好）

---

**Q15 — SHA-256 sign-off 校验（终轮）**
- 意图：Agent 运行脚本 `scripts/signoff.sh`，该脚本对 `src/requests/utils.py`、`analysis/fix_commit.json`、`analysis/cve_metadata.json` 三个文件拼接后计算 SHA-256，输出格式 `VERIFIED:<sha256hex>`，写入 `signoff/final_signoff.txt`
- 产物：`signoff/final_signoff.txt`，内容形如 `VERIFIED:a3f7...`
- check 锚点：文件存在；以 `VERIFIED:` 开头；后接 64 位十六进制字符串；check 脚本独立重算三文件内容拼接 SHA-256 并比对
- 难度向量：**V7**（Bash-sha256 sign-off token，不实际运行拿不到正确值）

---

## Update 设计汇总

| Update | 注入时机 | 核心内容 | 体量来源 | supersede 关系 |
|--------|----------|----------|----------|----------------|
| UPDATE-1 | Q8 前 | 新增 CVE-2023-32681 核查任务；Alice 邮件错误指定 PR#6963 为官方修复 | 邮件线程 ~15k + Slack 消息 ~10k + NVD 快照 ~8k = ~33k | 无（为 UPDATE-2 铺垫） |
| UPDATE-2 | Q11 前 | **supersede** UPDATE-1 中 commit SHA 记录，勘误为 PR#6965；撤销"2.32.3 含部分修复"错误说法 | Slack 勘误 ~8k + 勘误邮件 ~5k + PR#6965 review 快照 ~20k = ~33k | supersede UPDATE-1 的 commit SHA 指定 |

---

## Preference 清单（4 条）

| ID | 内容 | 注入方式 | 考察轮次 |
|----|------|----------|----------|
| P1 | 所有 JSON 输出必须使用 snake_case 字段名，禁止 camelCase | Q1 前显式说明 | Q1, Q2, Q7, Q8, Q10, Q12 |
| P2 | changelog 和 release note 条目须遵循 HISTORY.md 风格（RST 风格列表，`**Security**`/`**Bugfixes**` 二级标题） | Q11 前 feedback 注入 | Q11 静默考察 |
| P3 | 测试文件顶部必须有模块级 docstring 说明该文件的测试目的 | Q4 前显式说明 | Q13 静默考察 |
| P4 | 安全文档必须包含 `## Workaround` 二级标题，且位于 `## Fix` 之后 | Q14 前 feedback 注入 | Q14 静默考察 |

---

## 难度向量绑定汇总

| 向量 | 说明 | 绑定轮次 |
|------|------|----------|
| V1 | 多源信息冲突（Slack/邮件/NVD 三方版本/评分矛盾） | Q2, Q7 |
| V2 | update 反转（UPDATE-1→UPDATE-2 信念修正） | Q8, Q10 |
| V3 | 隐式 preference 静默考察 | Q11, Q13, Q14 |
| V4 | 跨轮数值/事实闭合（URL、测试名、文件数量、commit SHA 不得漂移） | Q3, Q6, Q9, Q12, Q13 |
| V5 | 失真「自动摘要」诱饵（Slack bot 错误指向 `build_response`） | Q1 |
| V6 | 废弃副本红鲱鱼（PR#6963 被 PR#6965 取代，飞书中 Bob 推荐旧 PR） | Q5 |
| V7 | Bash-sha256 sign-off token | Q15 |
| V9 | 真实来源字段 verbatim 引用 | Q1, Q4, Q11, Q14 |
| V10 | supersede 辨别 | Q10 |

---

## 拆分建议

素材丰富度属于 **adequate**（不需拆分）。CVE-2024-47081 主线与 CVE-2023-32681 副线已通过 UPDATE-1 巧妙集成，无需独立为两个场景。workspace 体量估算约 132k tokens，满足要求。

---

## 删除建议

无。场景可行性评级：**adequate**，建议保留并进入造数阶段。
