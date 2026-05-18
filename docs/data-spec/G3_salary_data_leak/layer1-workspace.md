# Layer 1 -- Workspace File Spec

> Workspace files simulate system exports — cloud access logs, email audit records, file version histories, security reports.
> 陈静's P2 naming: 中文习惯命名 (2026年09月_主题.md).

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
你是陈静的数据安全调查助手，帮助她追查薪资数据泄露路径、分析证据链、评估合规风险。
```

### IDENTITY.md
```markdown
# Identity
你是 **HR-SecOps AI**，一个 HR 数据安全调查助手，部署在陈静（HR经理，北京某科技公司）的工作环境中，支持她追查薪资表泄露事件。

你帮助陈静分析云盘访问日志、邮件附件审计记录、文件版本历史、IT安全报告和薪资表元数据——跨飞书IM（林小雅、张薇）和邮件（IT安全）进行多源交叉验证。
```

### SOUL.md
```markdown
# 工作原则
1. **证据链优先**：基于系统日志（云盘、邮件、文件版本）的客观记录。当事人的口头声明必须与系统记录交叉验证。
2. **跨源验证**：云盘日志、邮件审计、文件版本历史是三个独立的证据来源。IT安全报告也是独立来源但注意其检查范围。
3. **区分事件类型**：PREVIEW（预览）≠ DOWNLOAD（下载）≠ SHARE（分享）。每种操作在系统日志中有不同记录。
4. **来源可靠性排序**：系统日志（云盘、邮件服务器）> IT安全报告（注意检查范围）> 当事人陈述（利益相关方）。
5. **文件属性验证**：文件大小、哈希值、元数据（创建者、修改者）是辨别文件版本的客观依据。
6. **专业但有温度**：调查涉及同事关系，在保持客观的同时注意人的因素。
```

### USER.md
```markdown
# 人员和频道
## 主要用户
- **陈静 (Chen Jing)** — HR经理，25岁，北京科技公司。薪资泄露调查。偏好：(P1) 项目符号+标题分层，(P2) 中文习惯命名，(P3) 先执行摘要后证据，(P4) 定性+定量平衡，(P5) 专业但有温度。

## 关键人物
| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 林小雅 (P009) | HRBP，陈静师妹+朋友 | IM (飞书) | 嫌疑人，声称只下载脱敏版（虚假） |
| 张薇 (P002) | HR VP，直属上级 | 飞书 | 决策者 |
| IT安全 | IT安全部门 | 邮件 | 调查协助，报告范围有限 |
```

### TOOLS.md
```markdown
# 可用工具
| 工具 | 用途 |
|---|---|
| `sessions_list` | 列出历史会话 |
| `sessions_history` | 读取历史会话 |
| `read` | 读取 workspace 文件（只读） |
| `exec` | shell 命令 |
```

---

## 2. Scenario-Specific Workspace Files

### cloud-storage-access-log.md (Initial)
**Content key points:**
- Title: `公司云盘 — 文件访问日志 (2026-09-20 至 2026-09-30)`
- Format: Simulates cloud storage audit log with timestamp, user, action, file, size
- **Key entries (C1 baseline):**
  - 2026-09-25T10:00:03+08:00 | lxy@company.com (林小雅) | PREVIEW | 2026-Q3-salary-anonymized.xlsx | 0.8MB
  - **2026-09-25T14:22:17+08:00 | lxy@company.com (林小雅) | DOWNLOAD | 2026-Q3-salary-full.xlsx | 2.3MB** — THE KEY ENTRY
  - Other access: 陈静 regular access (EDIT, UPLOAD), 张薇 PREVIEW of anonymized version, etc.
- **C1 critical:** Two distinct events for 林小雅: PREVIEW of anonymized (10:00) AND DOWNLOAD of full version (14:22). The DOWNLOAD of the full version is the evidence.
- **Near-signal noise:** ~30 other cloud access events by various employees for different files.

**Length estimate:** ~800 words, ~1,200 tokens

---

### email-attachment-audit.md (Initial)
**Content key points:**
- Title: `邮件系统 — 附件审计日志 (2026-09-20 至 2026-09-30)`
- Format: Email audit log with timestamp, from, to, subject, attachment name, size
- **Key entry (C2 baseline):**
  - **2026-09-25T15:03:44+08:00 | FROM: lxy@company.com | TO: zhangling@headhunter-corp.com | SUBJECT: 薪资数据参考 | ATTACHMENT: salary-data-analysis.xlsx | SIZE: 2.3MB**
- **C2 critical:** (1) Recipient is external domain (headhunter-corp.com), (2) Attachment size 2.3MB = full version size (anonymized is 0.8MB), (3) Sent 41 minutes after cloud download.
- **Near-signal noise:** ~20 other email entries with various internal and external attachments.

**Length estimate:** ~700 words, ~1,050 tokens

---

### salary-spreadsheet-metadata.md (Update 3, before R9)
**Content key points:**
- Title: `薪资表文件元数据对比 — 2026年09月调查`
- **Key data:**
  - `2026-Q3-salary-full.xlsx` v1.1: SHA-256 hash prefix `a3f7b2c8e9d1...`, creator: 陈静, last modifier: 陈静, size: 2.3MB
  - `salary-data-analysis.xlsx` (email attachment): SHA-256 hash prefix `a3f7b2c8e9d1...` (MATCH), creator metadata: 陈静, size: 2.3MB
  - `2026-Q3-salary-anonymized.xlsx`: SHA-256 hash prefix `7b4c8f2d1a9e...` (DIFFERENT), size: 0.8MB
- **C2 definitive:** File hash match proves the email attachment IS the full version, not the anonymized version.

**Length estimate:** ~400 words, ~600 tokens

---

### file-version-history.md (Update 1, before R5)
**Content key points:**
- Title: `云盘文件版本历史 — 薪资相关文件 (2026-09)`
- **Key entries (C3 source):**
  - `2026-Q3-salary-full.xlsx`:
    - v1.0 | 2026-09-20T09:15:00 | Created by 陈静 | 2.1MB | "Q3薪资表初版"
    - v1.1 | 2026-09-24T16:30:00 | Modified by 陈静 | 2.3MB | "新增3名入职员工薪资"
  - `2026-Q3-salary-anonymized.xlsx`:
    - v1.0 | 2026-09-22T11:00:00 | Created by 陈静 | 0.8MB | "导出脱敏版本供HRBP使用"
    - (No further versions)
- **C3 source:** Timeline consistent: full created 9/20, updated 9/24 (size grows to 2.3MB), anonymized created 9/22 (0.8MB, no updates). 林小雅's download on 9/25 gets the v1.1 with 3 new employees.

**Length estimate:** ~350 words, ~525 tokens

---

### it-security-report.md (Update 2, before R6)
**Content key points:**
- Title: `IT安全部门 — 薪资数据泄露初步调查报告 (2026-09-30)`
- **Key content (C4 Source A):**
  - "调查范围：云盘外部分享功能、共享链接记录、外部访客权限"
  - "调查方法：检查了 2026-09-15 至 2026-09-30 期间所有云盘外部分享记录"
  - "调查结论：未发现通过云盘渠道的外部数据分享。文件共享链接功能在相关时间段内未被使用。所有薪资相关文件的分享权限仅限公司内部用户。"
  - "建议：继续监控云盘访问，加强权限管理。"
- **C4 critical:** IT report checks only cloud sharing channel. Does NOT check email channel. Conclusion is scope-limited but sounds comprehensive.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Visible | Via | Why |
|---|---|---|---|
| cloud-storage-access-log.md | Initial | Workspace | Cloud access log with DOWNLOAD event (C1) |
| email-attachment-audit.md | Initial | Workspace | Email to external domain (C2) |
| file-version-history.md | Update 1 (before R5) | updates/ | Version timeline (C3) |
| it-security-report.md | Update 2 (before R6) | updates/ | IT "no external shares" (C4) |
| salary-spreadsheet-metadata.md | Update 3 (before R9) | updates/ | File hash match proof (C2 definitive) |
| linxiaoya-partial-admission.md | Update 4 (before R11) | updates/ | 林小雅's partial admission |

---

## 4. Update-Added Workspace Files

### file-version-history.md (Update 1)
(Described above.)

### it-security-report.md (Update 2)
(Described above.)

### salary-spreadsheet-metadata.md (Update 3)
(Described above.)

### linxiaoya-partial-admission.md (Update 4, before R11)
**Content:**
- Title: `飞书导出 — 林小雅 -> 陈静: 关于薪资文件 (2026-10-03)`
- 林小雅 admits: "静姐，我承认我确实下载了完整版。但我发给张琳的时候删除了部分敏感信息，不是完整的原文件。"
- This claim is STILL contradicted by the file hash match (完整版哈希 = 邮件附件哈希).
- **Last defense before definitive evidence.**

**Length estimate:** ~300 words, ~450 tokens

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (2 files) | cloud-storage-access-log, email-attachment-audit | ~2,250 tokens |
| Update 1 (1 file) | file-version-history | ~525 tokens |
| Update 2 (1 file) | it-security-report | ~750 tokens |
| Update 3 (1 file) | salary-spreadsheet-metadata | ~600 tokens |
| Update 4 (1 file) | linxiaoya-partial-admission | ~450 tokens |
| **Total workspace** | **11 files** | **~6,575 tokens** |
