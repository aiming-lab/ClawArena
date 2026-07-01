# BRIEF: sec1 — CVE-2024-6387 (regreSSHion) 漏洞分析与修复

## 场景叙事背景

某中型互联网公司的安全工程团队（Security Engineering Team）负责维护公司基础设施的 SSH 访问体系。2024 年 7 月 1 日，Qualys 公开披露了 CVE-2024-6387（代号"regreSSHion"），一个 OpenSSH 服务端的信号处理器竞态条件漏洞，允许未经认证的远程攻击者以 root 权限执行任意代码。

Agent 扮演该安全团队的首席安全工程师（Lead Security Engineer）。任务包括：分析漏洞技术细节、评估受影响资产范围、制定并实施修复方案、生成合规报告，并响应来自多个渠道（Slack、邮件、Feishu）的团队协作消息。

整个场景涵盖漏洞评估、资产扫描结果分析、补丁验证、workaround 实施、风险评分计算，以及最终安全修复报告的生成。

---

## 真实来源链接表

| # | 来源类型 | URL | 摘要 |
|---|----------|-----|------|
| 1 | NVD 条目 | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 | 官方 CVE 详情，CVSS 8.1，CWE-362/CWE-364，2024-07-01 |
| 2 | GHSA Advisory | https://github.com/advisories/GHSA-2x8c-95vh-gfv4 | GitHub Advisory，High 级，EPSS 63.835%（98th 百分位） |
| 3 | Qualys 技术报告 | https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server | 发现方详细分析，14M 暴露实例，6–8 小时 PoC 利用 |
| 4 | oss-security 披露邮件 | https://www.openwall.com/lists/oss-security/2024/07/01/3 | 原始 CVE 公告，受影响版本 8.5p1–9.8p1，引入 commit 752250c |
| 5 | OpenSSH 9.8 发布说明 | https://www.openssh.org/txt/release-9.8 | 官方修复版本说明，PerSourcePenalties 新配置项 |
| 6 | Red Hat Errata RHSA-2024:4312 | https://access.redhat.com/errata/RHSA-2024:4312 | RHEL 9 修复包 openssh-8.7p1-38.el9_4.1，2024-07-03 |
| 7 | 引入回归的 commit | https://github.com/openssh/openssh-portable/commit/752250caabda3dd24635503c4cd689b32a650794 | 2020-10-16，Damien Miller，移除 DO_LOG_SAFE_IN_SIGHAND 保护 |
| 8 | CVE-2006-5051 原始漏洞 | https://github.com/advisories/GHSA-mq5h-r3rg-j9hg | 2006 年原始漏洞，regreSSHion 的历史根源 |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|-----|----------|------|
| CVE_ID | CVE-2024-6387 | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 | 官方编号 |
| CVSS_SCORE | 8.1 | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 | CVSS v3.1 Base Score |
| CVSS_VECTOR | CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 | NVD 官方向量 |
| SEVERITY | High | https://github.com/advisories/GHSA-2x8c-95vh-gfv4 | GHSA 评级 |
| CWE_PRIMARY | CWE-362 | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 | 竞态条件 |
| CWE_SECONDARY | CWE-364 | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 | 信号处理器竞态 |
| AFFECTED_RANGE | 8.5p1 <= openssh < 9.8p1 | https://www.openwall.com/lists/oss-security/2024/07/01/3 | 不包含 OpenBSD |
| REGRESSION_COMMIT | 752250caabda3dd24635503c4cd689b32a650794 | https://github.com/openssh/openssh-portable/commit/752250caabda3dd24635503c4cd689b32a650794 | 2020-10-16 引入回归 |
| PATCHED_VERSION | 9.8p1 | https://www.openssh.org/txt/release-9.8 | 官方修复版本 |
| RHEL9_FIXED_PKG | openssh-8.7p1-38.el9_4.1 | https://access.redhat.com/errata/RHSA-2024:4312 | RHEL 9 修复包版本 |
| RHEL_ERRATA | RHSA-2024:4312 | https://access.redhat.com/errata/RHSA-2024:4312 | RHEL 9 安全公告 ID |
| DISCLOSURE_DATE | 2024-07-01 | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 | NVD 发布日期 |
| EXPLOIT_ATTEMPTS | ~10000 | https://www.openwall.com/lists/oss-security/2024/07/01/3 | 成功利用所需平均尝试次数 |
| EXPLOIT_TIME | 6–8 hours | https://www.openssh.org/txt/release-9.8 | 实验室条件下利用时间 |
| EPSS_SCORE | 63.835% | https://github.com/advisories/GHSA-2x8c-95vh-gfv4 | EPSS 98th 百分位 |
| GHSA_ID | GHSA-2x8c-95vh-gfv4 | https://github.com/advisories/GHSA-2x8c-95vh-gfv4 | GitHub Security Advisory ID |
| WORKAROUND_PARAM | LoginGraceTime 0 | https://help.mindbreeze.com/en/index.php?topic=doc/Adjusting-the-InSpire-Host-OpenSSH-Settings---Set-LoginGraceTime-to-0-Mitigation-for-CVE-2024-6387/index.htm | 临时缓解配置，存在 DoS 风险 |
| VULN_TYPE | signal handler race condition | https://www.openwall.com/lists/oss-security/2024/07/01/3 | 漏洞类型 |
| PRIOR_CVE | CVE-2006-5051 | https://github.com/advisories/GHSA-mq5h-r3rg-j9hg | 历史回归来源 |
| EXPOSED_INSTANCES | 14000000 | https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server | Qualys 扫描：互联网暴露约 1400 万实例 |

---

## Workspace 文件树与体量规划（目标 > 100k tokens）

```
workspace/
├── README.md                          # 场景说明，~1k tokens
├── assets/
│   ├── scan_results/
│   │   ├── shodan_export_2024-07-02.json     # 模拟 Shodan 扫描导出，~15k tokens
│   │   │   # 字段: ip, port, version, banner, os, location, org, vulns
│   │   │   # 包含 2000+ 条目，每条含 openssh 版本字符串
│   │   ├── internal_inventory.csv            # 公司内网资产清单，~8k tokens
│   │   │   # 字段: hostname, ip, ssh_version, os, env(prod/staging/dev), owner
│   │   │   # 约 500 台主机
│   │   └── nmap_ssh_scan_20240702.txt        # nmap -sV 扫描原始输出，~6k tokens
│   ├── advisories/
│   │   ├── NVD_CVE-2024-6387.json            # NVD API 返回原始 JSON，~3k tokens
│   │   ├── GHSA-2x8c-95vh-gfv4.json          # GHSA advisory 完整 JSON，~2k tokens
│   │   ├── qualys_regresshion_report.pdf.txt # Qualys 报告文本版，~20k tokens
│   │   │   # 含技术细节、PoC 描述、版本矩阵、修复建议
│   │   ├── redhat_RHSA-2024-4312.json         # Red Hat Errata JSON，~3k tokens
│   │   └── openwall_disclosure.txt           # oss-security 邮件全文，~5k tokens
│   ├── code_samples/
│   │   ├── sshd_sigdie_vulnerable.c          # 漏洞版本 sigdie() 代码片段，~2k tokens
│   │   ├── sshd_sigdie_patched.c             # 修复版本对比，~2k tokens
│   │   └── signal_handler_analysis.md        # 信号处理器安全函数分析，~4k tokens
│   └── compliance/
│       ├── cvss_calculation_worksheet.md     # CVSS 计算工作表，~3k tokens
│       └── risk_register_template.json       # 风险登记册模板，~2k tokens
├── sessions/
│   ├── slack_general_2024-07-01.json        # Slack #security-alerts 频道，~8k tokens
│   ├── slack_incident_2024-07-02.json       # Slack #incident-response 频道，~8k tokens
│   ├── email_thread_management.txt          # 管理层邮件往来，~5k tokens
│   ├── feishu_security_team_dm.json         # Feishu 安全团队 DM，~6k tokens
│   └── feishu_sre_channel.json             # Feishu SRE 群组，~6k tokens
├── scripts/
│   ├── check_vulnerable.sh                 # 版本检测脚本，~1k tokens
│   ├── patch_audit.py                      # 补丁审计脚本，~2k tokens
│   └── generate_report.py                  # 报告生成脚本，~2k tokens
├── templates/
│   ├── incident_report_template.md         # 事件报告模板，~3k tokens
│   └── patch_verification_checklist.md    # 补丁验证清单，~2k tokens
└── work/
    # Agent 工作输出目录（初始空）
```

**体量估算合计**：约 120k–140k tokens（主要来源：shodan 导出 JSON 15k + qualys 报告 20k + 内网清单 8k + 各 session 历史 33k + 技术分析文档 10k + advisory JSON 8k + 代码样本 8k + 其他杂项 15k）

---

## Session 清单

| Session ID | 渠道 | 参与者 | 主要内容 | 时间线 |
|------------|------|--------|----------|--------|
| S1（主 session） | CLI/工作台 | Agent ↔ 安全主管 Alice | 漏洞评估任务主线，工具调用痕迹 | 2024-07-02 |
| S2 | Slack #security-alerts | 全团队广播 | CVE 首次告警、资产数量讨论 | 2024-07-01 |
| S3 | Slack #incident-response | 安全团队 + SRE | 补丁部署进度、workaround 验证、冲突信息（含 honey-pot 摘要） | 2024-07-02 |
| S4 | 邮件 | Alice → CTO → Agent | 管理层汇报请求、合规截止时间 72 小时 | 2024-07-02 |
| S5 | Feishu DM | Agent ↔ SRE 工程师 Bob | 内网扫描数据交接、版本不一致报告 | 2024-07-02 |
| S6 | Feishu 群 #sre-infra | SRE 团队 | PerSourcePenalties 配置讨论、废弃旧文档引用（红鲱鱼） | 2024-07-03 |

---

## 15–18 轮 Exec-Check 概要

### 第 1 轮：漏洞信息核验
- **意图**：解析 NVD JSON，输出标准化漏洞摘要
- **产物**：`work/vuln_summary.json`
- **字段**：`cve_id`, `cvss_score`, `cvss_vector`, `severity`, `cwe_ids[]`, `affected_range`, `disclosure_date`, `ghsa_id`
- **check 锚点**：cvss_score == 8.1，cvss_vector 精确匹配，cwe_ids 含 "CWE-362"，disclosure_date == "2024-07-01"
- **难度向量**：V8（schema-by-shape 严格字段校验），V9（verbatim 引用 NVD 字段值）

### 第 2 轮：受影响资产清单生成
- **意图**：扫描内网资产清单，筛选受影响版本范围（8.5p1 ≤ openssh < 9.8p1）
- **产物**：`work/affected_assets.csv`
- **字段**：hostname, ip, ssh_version, env, owner, is_vulnerable
- **check 锚点**：is_vulnerable 字段逻辑正确，prod 环境数量与清单一致，格式为 CSV
- **难度向量**：V4（跨轮数值：这里统计的 prod 主机数量，第 9 轮须再次引用）

### 第 3 轮：CVSS 向量分解说明文档
- **意图**：为管理层生成 CVSS 向量逐项解释
- **产物**：`work/cvss_breakdown.md`
- **check 锚点**：AV:N（Network），AC:H（High），PR:N（None），UI:N（None），S:U，C:H，I:H，A:H 各项说明存在且正确
- **难度向量**：V9（verbatim 引用 CVSS 向量字符串），V8

### 第 4 轮：历史回归溯源分析
- **意图**：说明 CVE-2024-6387 是 CVE-2006-5051 的回归，引用引入回归的 commit
- **产物**：`work/regression_analysis.md`
- **check 锚点**：含 commit hash `752250c`，提及 `DO_LOG_SAFE_IN_SIGHAND`，引用 CVE-2006-5051，日期 2020-10-16
- **难度向量**：V5（honey-pot：S3 Slack 中有一条 bot 摘要错误地将引入日期写为 2021-03，正确应为 2020-10），V1（多源冲突）

### 第 5 轮：临时 Workaround 实施方案
- **意图**：生成临时缓解方案文档，含 sshd_config 修改说明和 DoS 风险警告
- **产物**：`work/workaround_plan.md`
- **check 锚点**：含 `LoginGraceTime 0` 配置，含 DoS 风险说明，含 `systemctl restart sshd` 命令
- **难度向量**：V3（隐式偏好：文档应使用工单格式，违规扣分），V6（废弃文档：S6 Feishu 群引用了一个旧版 workaround.md，将 LoginGraceTime 设为 30 而非 0，agent 须辨别）

### 第 6 轮：Red Hat 修复包版本验证脚本
- **意图**：编写 bash 脚本，检测系统 openssh 版本是否达到 RHSA-2024:4312 要求
- **产物**：`work/check_rhel_patch.sh`（可执行）
- **check 锚点**：脚本正确引用修复版本 `8.7p1-38.el9_4.1`，errata ID `RHSA-2024:4312`，脚本可执行并输出 PASS/FAIL
- **难度向量**：V8（输出格式严格），V9（verbatim 引用 errata ID）

### 第 7 轮：互联网暴露面评估报告
- **意图**：基于 Shodan 导出数据，统计互联网暴露的受影响版本分布
- **产物**：`work/exposure_report.json`
- **字段**：`total_scanned`, `vulnerable_count`, `version_distribution{}`, `top_5_exposed_orgs[]`
- **check 锚点**：数据来自 shodan_export JSON，vulnerable_count 数值在合理范围内，版本分布字段格式正确
- **难度向量**：V4（跨轮数值：vulnerable_count 须与第 9 轮风险矩阵引用一致）

---

*此处为 Update 1 注入点（第 7 轮后）*

---

### 第 8 轮（Update 1 后）：修订受影响版本范围
- **意图**：Update 1 注入新 advisory，指出 RHEL 8 同样受影响（errata RHSA-2024:4340），需更新资产清单
- **产物**：`work/affected_assets_v2.csv`（更新版）
- **check 锚点**：新增 RHEL 8 主机条目，引用 RHSA-2024:4340（而非仅 4312）
- **难度向量**：V2（动态 update 反转：受影响范围扩大），V10（supersede 前置，为第 11 轮铺垫）

### 第 9 轮：风险矩阵生成
- **意图**：综合资产数量、漏洞 CVSS、暴露时间，生成风险优先级矩阵
- **产物**：`work/risk_matrix.json`
- **字段**：`cve_id`, `cvss_score`, `prod_host_count`, `internet_exposed_count`, `risk_level`, `remediation_priority`, `estimated_exposure_hours`
- **check 锚点**：prod_host_count 与第 2 轮一致（V4 闭合），cvss_score 8.1，risk_level 为 "HIGH"
- **难度向量**：V4（数值跨轮闭合），V8

### 第 10 轮：补丁部署进度跟踪表
- **意图**：从 Slack 和 Feishu 中提取补丁部署进度，生成结构化跟踪表
- **产物**：`work/patch_progress.json`
- **字段**：每台主机的 patched/pending/failed 状态
- **check 锚点**：状态值枚举正确，来源于 session 历史，不捏造主机
- **难度向量**：V1（多 session 信息整合），V3（偏好：进度表须按 env 分组）

---

*此处为 Update 2 注入点（第 10 轮后）*

---

### 第 11 轮（Update 2 后）：Supersede — 撤销旧 Workaround 方案
- **意图**：Update 2 注入新消息：安全主管 Alice 正式通知，`LoginGraceTime 0` workaround 因 DoS 风险已被公司安全委员会否决，改用 MaxStartups 限制方案
- **产物**：`work/workaround_plan_v2.md`（替换第 5 轮方案）
- **check 锚点**：不再包含 `LoginGraceTime 0`，包含 `MaxStartups 10:30:100`，包含撤销声明
- **难度向量**：V10（supersede 辨别），V2（update 反转正确答案），V3

### 第 12 轮：漏洞利用技术分析摘要
- **意图**：基于 Qualys 报告，分析利用技术（ASLR 绕过、堆喷射、FILE 结构操纵）
- **产物**：`work/exploit_analysis.md`
- **check 锚点**：含 "~10,000 attempts"，"6-8 hours"，含 "glibc"，含 "ASLR" 关键词，含 "32-bit" 限定语
- **难度向量**：V5（honey-pot：S3 Slack 有一条 bot 摘要称"可在 30 分钟内完成利用"，正确来源说 6-8 小时），V1

### 第 13 轮：合规报告生成（管理层版本）
- **意图**：为 CTO 生成执行摘要级合规报告，包含所有关键锚点
- **产物**：`work/executive_report.md`
- **check 锚点**：含 CVE-2024-6387，含 CVSS 8.1，含 RHSA-2024:4312，含 errata 日期 2024-07-03，含 patched_version 9.8p1
- **难度向量**：V9（verbatim 引用），V3（偏好：执行摘要须含 TL;DR 段落，<200 字）

---

*此处为 Update 3 注入点（第 13 轮后）*

---

### 第 14 轮（Update 3 后）：新增 CVE-2024-6409 对比分析
- **意图**：Update 3 引入相关 CVE-2024-6409（sshd privilege separation child 的 SIGALRM 竞态），要求对比分析
- **产物**：`work/cve_comparison.json`
- **字段**：含 CVE-2024-6387 和 CVE-2024-6409 各自的 affected_versions, cvss_score, scope（child process vs main sshd）
- **check 锚点**：CVE-2024-6409 影响版本为 8.7, 8.8（而非完整范围），cvss_score 不同
- **难度向量**：V2（update 扩充知识），V1（区分两个相似 CVE）

### 第 15 轮：补丁前后代码 diff 注释
- **意图**：基于 code_samples 目录，为 sigdie() 函数的修复 diff 编写中文技术注释
- **产物**：`work/patch_diff_annotated.md`
- **check 锚点**：提及 `DO_LOG_SAFE_IN_SIGHAND` 宏，提及 `_exit(1)` 安全替代，引用 commit hash `752250c`
- **难度向量**：V9（verbatim 引用代码标识符），V4（与第 4 轮 regression analysis 一致）

### 第 16 轮：生成最终安全修复清单（JSON）
- **意图**：生成结构化最终修复清单，供自动化系统导入
- **产物**：`work/final_remediation.json`
- **字段**：`cve_id`, `ghsa_id`, `cvss_score`, `cvss_vector`, `affected_range`, `patched_version`, `rhel9_package`, `rhel9_errata`, `workaround_superseded`, `workaround_current`, `regression_commit`, `prior_cve`, `disclosure_date`, `remediation_deadline`
- **check 锚点**：所有字段与前序轮次锚点严格一致（V4 全局数值闭合），workaround_superseded 为 "LoginGraceTime 0"，workaround_current 为 MaxStartups
- **难度向量**：V4（全局闭合），V8，V9，V10

### 第 17 轮（终轮）：Bash sha256 sign-off 校验
- **意图**：对 `work/final_remediation.json` 计算 sha256，写入 `work/signoff.txt`，格式为 `VERIFIED:<sha256>`
- **产物**：`work/signoff.txt`
- **check 锚点**：check 脚本独立重算 sha256 并比对，格式严格匹配 `VERIFIED:[a-f0-9]{64}`
- **难度向量**：V7（Bash sha256 sign-off token，必须实际运行 sha256sum 命令）

---

## Update 设计

### Update 1（第 7 轮后注入）：RHEL 8 受影响范围扩展
- **触发时机**：第 7 轮交付后
- **新增内容**：
  - 新 session 消息（Feishu S5）：Bob 发来消息称"扫描发现 RHEL 8 主机也受影响，有新的 RHEL 8 errata RHSA-2024:4340"
  - 新文件：`assets/advisories/redhat_RHSA-2024-4340.json`（RHEL 8 errata，~3k tokens）
  - 新文件：`assets/scan_results/rhel8_inventory.csv`（RHEL 8 主机清单，~4k tokens）
  - 新文件：`assets/advisories/rhel8_openssh_versions.md`（RHEL 8 受影响版本说明，~2k tokens）
- **体量**：~35k tokens（新 JSON + CSV + markdown + 扩展的 Shodan 数据补丁）
- **对正确答案的影响**：第 8 轮起，affected_assets 须包含 RHEL 8 主机

### Update 2（第 10 轮后注入）：Workaround 撤销通知（Supersede）
- **触发时机**：第 10 轮交付后
- **新增内容**：
  - 新 session 消息（邮件 S4 续篇）：Alice 发邮件撤销 LoginGraceTime 0 方案
  - 新文件：`assets/compliance/security_committee_decision.md`（安全委员会决议，~2k tokens）
  - 新文件：`assets/advisories/maxstartups_guidance.md`（MaxStartups 替代方案详情，~3k tokens）
  - 更新 session S3 Slack：新增补充消息说明撤销原因（DoS 风险）
- **体量**：~30k tokens（新文档 + 补充 session 消息 + 相关 RedHat Solution 文章文本）
- **supersede 关系**：此 Update 显式撤销 Update 0（初始 workspace）中的 workaround_plan.md，考察 V10

### Update 3（第 13 轮后注入）：CVE-2024-6409 同期披露
- **触发时机**：第 13 轮交付后
- **新增内容**：
  - 新 session 消息（Slack S3 新消息）：安全团队成员发现 CVE-2024-6409
  - 新文件：`assets/advisories/CVE-2024-6409_detail.json`（CVE-2024-6409，影响 sshd 子进程，版本 8.7/8.8，~3k tokens）
  - 新文件：`assets/advisories/openssh_dual_cve_matrix.md`（双 CVE 对比矩阵，~4k tokens）
- **体量**：~32k tokens（新 advisory + 对比矩阵 + 扩展技术分析文档）
- **对正确答案的影响**：第 14 轮起须区分两个 CVE 的版本范围和影响范围

---

## Preference 规则（4-5 条）

| # | 偏好规则 | 注入方式 | 静默考察轮次 |
|---|----------|----------|--------------|
| P1 | 所有 JSON 输出使用 2-space indent，字段按字母顺序排列 | S1 主 session 第 2 条消息中 Alice 显式说明 | 第 9、16 轮 |
| P2 | 技术报告中 CVE 编号统一格式为 `CVE-YYYY-NNNNN`（含连字符，大写） | S2 Slack 中 Alice 纠正一次格式错误 | 第 13 轮 |
| P3 | 所有工作产物文件名使用 snake_case，不用 camelCase 或连字符 | S1 主 session 第 1 条消息中显式要求 | 第 6、10、16 轮 |
| P4 | 进度报告和清单须按环境（prod/staging/dev）分组，prod 优先 | S5 Feishu DM 中 Bob 通过 feedback 隐式建议 | 第 10 轮 |
| P5 | 执行摘要（executive summary）须含独立 TL;DR 段落，字数不超过 200 字 | S4 邮件中 CTO 显式要求 | 第 13 轮 |

---

## 难度向量绑定总结

| 向量 | 绑定轮次 | 说明 |
|------|----------|------|
| V1 多源信息冲突 | 第 4、10、12、14 轮 | 多 session 对同一事实有冲突描述 |
| V2 动态 update 反转 | 第 8、11、14 轮 | update 后正确答案改变 |
| V3 隐式偏好静默考察 | 第 5、10、11、13 轮 | 偏好规则前期注入，后期不再提示 |
| V4 跨轮数值闭合 | 第 2→9、7→9、9→16 轮 | 关键数值必须全局一致 |
| V5 失真摘要诱饵 | 第 4、12 轮 | Bot 摘要含错误时间/数值，有明面反证 |
| V6 废弃副本红鲱鱼 | 第 5 轮 | Feishu 旧文档 LoginGraceTime 30 被废弃 |
| V7 sha256 sign-off | 第 17 轮（终轮） | 必须实际运行 sha256sum |
| V8 严格 schema 校验 | 第 1、3、6、9、16 轮 | JSON 字段类型/值/格式严格校验 |
| V9 verbatim 引用 | 第 1、3、4、6、13、15、16 轮 | 精确引用真实来源字段值 |
| V10 supersede 辨别 | 第 11、16 轮 | Update 2 撤销旧 workaround |

---

## 拆分建议

素材丰富度**adequate 至 strong**，CVE-2024-6387 可独立支撑完整场景。若需拆分：
- **sec1-A**：漏洞技术分析线（轮次 1–8），聚焦 CVE 解析、代码 diff、回归溯源
- **sec1-B**：合规修复线（轮次 9–17），聚焦资产扫描、补丁部署、风险矩阵、管理报告

建议保持**不拆分**，单场景体量和复杂度已达标。

---

## viability 评估

- **真实来源**：8 个真实 URL，均可核实；NVD、GHSA、OpenSSH 官方、oss-security、Red Hat Errata 均为权威来源
- **锚点数量**：19 个可回溯真实锚点
- **workspace 体量**：120k–140k tokens（可达）
- **update 体量**：每次 30k+ tokens（可达）
- **viability**：**strong**
