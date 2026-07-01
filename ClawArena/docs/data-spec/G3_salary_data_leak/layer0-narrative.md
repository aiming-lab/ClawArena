# Layer 0 -- Narrative Bible and Eval Trap Design

> Authoritative truth baseline. Does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g3` |
| Domain | HR / 数据安全 |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 陈静 (Chen Jing), 25, HR Manager at a ~200-person tech company in Beijing |
| One-sentence | 公司薪资表被外传——陈静通过云盘访问记录、邮件附件审计和 IM 转发记录追溯泄露路径，证据指向她信任的师妹林小雅（HRBP），但林小雅声称只分享了脱敏版本；实际上林小雅下载了完整版本并通过邮件转发给了外部猎头，尽管IT部门声称"没有外部分享"。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 陈静 收到匿名举报：有员工反映在外部招聘群里看到了公司的薪资数据（部分员工的岗位+薪资范围）。 | 匿名举报属实。一位员工在某行业招聘微信群里看到了一张截图，显示了公司 10+ 名员工的岗位和薪资区间。截图格式与公司内部薪资表一致。陈静 需要追查泄露路径。 | 陈静 知道有泄露。张薇（VP）已被通知。IT安全部门开始调查。 |
| W1, Day 2 | 陈静 查看云盘访问日志 (cloud-storage-access-log.md)。发现 林小雅 在 3 天前下载了薪资表的完整版本。 | 云盘日志明确记录：林小雅 (lxy@company.com) 于 2026-09-25T14:22:17+08:00 下载了 `2026-Q3-salary-full.xlsx`（完整版薪资表，含所有员工姓名+岗位+薪资）。同一天 10:00，林小雅 也访问（预览）了 `2026-Q3-salary-anonymized.xlsx`（脱敏版本，只有岗位+薪资区间，无姓名）。两次访问都有记录。关键：林小雅 下载了完整版本，不仅仅是脱敏版本。 | 陈静 看到了云盘日志。林小雅 不知道自己被调查。 |
| W1, Day 3 | 陈静 找 林小雅 谈话。林小雅 声称："我只下载了脱敏版本，用来做薪资市场调研分析。完整版本我只是预览了一下确认数据范围，没有下载。" | 林小雅 的说法是虚假的。云盘日志明确显示她下载了完整版本（14:22 download event），不仅仅是预览。她的"只下载脱敏版"说法与系统记录矛盾（C1）。林小雅 的动机：她与一位外部猎头（张琳，P017）有私下合作关系，提供薪资数据换取猎头费分成。她试图掩盖这个关系。 | 林小雅 否认下载完整版。陈静 有日志证据但尚未对质。 |
| W1, Day 4 | 陈静 查看邮件附件审计记录 (email-attachment-audit.md)，发现 林小雅 的邮件账户在下载完整版当天，发送了一封带附件的邮件。 | 邮件审计显示：林小雅 (lxy@company.com) 于 2026-09-25T15:03:44+08:00 发送邮件给 zhangling@headhunter-corp.com（张琳，外部猎头），附件为 `salary-data-analysis.xlsx`（文件大小 2.3MB，与完整版薪资表大小一致）。邮件主题："薪资数据参考"。这证明林小雅将完整版薪资数据通过邮件发送给了外部人员（C2）。 | 陈静 发现了邮件记录。 |
| W1, Day 5 | 林小雅 被再次约谈。她改口说："我发给张琳的是脱敏版本，是内部使用的市场调研数据。" | 林小雅 的新说法仍然是虚假的。邮件审计显示发送的文件大小（2.3MB）与完整版大小一致（脱敏版只有 0.8MB）。此外，邮件收件人 zhangling@headhunter-corp.com 是外部域名（headhunter-corp.com），不是公司内部邮箱（@company.com）——林小雅 声称"内部使用"但发送对象是外部人员（C2）。 | 林小雅 继续否认。陈静 有文件大小和域名证据。 |
| W2, Day 1 (Update 1 trigger) | 陈静 查看文件版本历史 (file-version-history.md)，追溯不同版本的创建和修改时间线。 | 文件版本历史显示：(1) `2026-Q3-salary-full.xlsx` v1.0 创建于 2026-09-20（陈静创建），(2) v1.1 修改于 2026-09-24（陈静更新了 3 名新入职员工薪资），(3) `2026-Q3-salary-anonymized.xlsx` v1.0 创建于 2026-09-22（陈静从完整版导出脱敏版本），(4) 脱敏版没有后续修改。林小雅下载完整版的时间（9-25）是在 v1.1 更新之后——她拿到的是最新的含 3 名新员工的完整版本。这个时间线完全一致，没有矛盾（C3）。 | 时间线清晰。 |
| W2, Day 2 (Update 2 trigger) | IT安全部门完成初步调查，发给 陈静 安全报告。报告结论："未发现外部文件分享记录。" | IT安全报告 (it-security-report.md) 检查了云盘的"共享链接"功能和"外部分享"标记，结论是"未发现外部分享"。这在技术上是正确的——林小雅没有通过云盘的分享功能分享文件。但IT部门只检查了云盘分享功能，没有检查邮件附件。林小雅 的泄露路径是：云盘下载 → 本地保存 → 邮件附件发送。这绕过了IT的云盘分享监控（C4）。 | IT说"没有外部分享"（云盘范围内正确）。陈静 有邮件审计显示外部发送。两者看似矛盾但实际是检查范围不同。 |
| W2, Day 3 (Update 3 trigger) | 陈静 获取薪资表元数据 (salary-spreadsheet-metadata.md)，确认泄露的文件就是完整版。 | 元数据显示：林小雅 邮件附件 `salary-data-analysis.xlsx` 的文件哈希与 `2026-Q3-salary-full.xlsx` v1.1 的哈希匹配（SHA-256 前 16 位一致）。文件创建者元数据显示"陈静"（原始创建者），最后修改者"陈静"（v1.1 更新），文件属性未被清除。这是definitive evidence：林小雅发送的就是完整版薪资表，不是脱敏版。 | 元数据证实了泄露的是完整版。 |
| W2, Day 5 (Update 4 trigger) | 陈静 与张薇（VP）开会，决定处理方案。同时 林小雅 主动来找 陈静 承认部分事实。 | 林小雅 承认下载了完整版，但仍坚称"只分享了部分数据，不是全部"。这与文件哈希匹配的证据矛盾——她分享的就是完整文件。张薇 决定启动正式调查程序。 | 最终处理阶段。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 陈静 (Protagonist, HR Manager)

- **Objective position:** 陈静 是薪资数据的管理者和泄露调查的负责人。她创建了完整版和脱敏版薪资表。她信任 林小雅（师妹+朋友），这导致她最初不愿相信证据指向林小雅。她的调查最终是基于证据的、专业的。
- **Private narrative:** 陈静 内心很难接受林小雅的背叛——林小雅是她的大学师妹，入职时是她推荐的。
- **Trust bias:** 陈静 对官方文件过度信任（P001 personality），对权威质疑慢。IT安全报告的"未发现外部分享"一度让她动摇。

### 林小雅 (P009, HRBP, 陈静的师妹)

- **Objective position:** 林小雅 下载了完整版薪资表并通过邮件发送给外部猎头张琳。她的动机是与猎头的利益交换。她的所有否认都是虚假的。
- **Public narrative (Phase 1):** "我只下载了脱敏版本" → "我发的是脱敏版" → "我只分享了部分数据"。持续缩小承认范围但从不完全坦白。
- **Why the gap exists:** 财务利益驱动。林小雅 与猎头有私下合作关系。

### 张薇 (P002, HR VP)

- **Objective position:** 张薇是陈静的直属上级。她要求客观调查，不因人际关系影响判断。
- **Role:** 决策者，最终决定调查结论和处理方案。

### IT安全部门

- **Objective position:** IT检查了云盘分享功能，在这个范围内确实没有外部分享记录。但他们没检查邮件附件渠道。他们的结论是范围内正确但不完整。

---

## 4. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Cloud log shows "full version downloaded" vs 林小雅 claims "only anonymized version." | cloud-storage-access-log.md (initial): 2026-09-25T14:22:17 林小雅 DOWNLOAD `2026-Q3-salary-full.xlsx` (2.3MB). Also: 2026-09-25T10:00:03 林小雅 PREVIEW `2026-Q3-salary-anonymized.xlsx` (0.8MB). | 林小雅 IM (Phase 1, Loop 3): "静姐，我只下载了脱敏版本。完整版我就预览了一下看数据范围。你可以查日志，我没有下载完整版。" | Cloud log definitively shows 林小雅 downloaded the full version (DOWNLOAD event, not PREVIEW). Her claim is directly contradicted by objective system records. She also previewed the anonymized version, but additionally downloaded the full version. | R1 onwards | **Yes: R1-->R5** (file version history confirms v1.1) |
| C2 | Email audit shows external forward vs 林小雅 claims "internal only." | email-attachment-audit.md (initial): 2026-09-25T15:03:44 FROM lxy@company.com TO zhangling@headhunter-corp.com SUBJECT "薪资数据参考" ATTACHMENT salary-data-analysis.xlsx (2.3MB). | 林小雅 IM (Phase 1, Loop 5): "我发给张琳的是脱敏版本，就是内部做市场调研用的。" | Email audit shows: (1) recipient is external domain (headhunter-corp.com), not internal (@company.com), contradicting "internal only"; (2) attachment size 2.3MB matches full version, not anonymized (0.8MB), contradicting "anonymized version." | R3 onwards | **Yes: R3-->R7** (metadata confirms file hash match) |
| C3 | File version timeline (NON-CONFLICT — cloud log, version history, email audit all temporally consistent). | file-version-history.md (Update 1): full.xlsx v1.0 created 9/20, v1.1 modified 9/24, anonymized.xlsx created 9/22. | cloud-storage-access-log.md: 林小雅 download 9/25 (after v1.1). email-attachment-audit.md: email sent 9/25 15:03 (41 minutes after download at 14:22). | All sources consistent: file created 9/20, updated 9/24, 林小雅 downloaded 9/25 14:22, emailed 9/25 15:03. The 41-minute gap between download and email send is consistent with saving and attaching. No contradictions. | R5 onwards | **None** |
| C4 | IT says "no external shares" vs email metadata shows external domain. | it-security-report.md (Update 2): "经检查，云盘外部分享功能日志中未发现外部分享记录。文件共享链接功能在相关时间段内未被使用。结论：未发现通过云盘渠道的外部数据分享。" | email-attachment-audit.md (initial): Email to zhangling@headhunter-corp.com with 2.3MB attachment. headhunter-corp.com is an external domain. | IT's finding is technically correct within scope: no cloud-sharing links were created. But 林小雅 bypassed cloud sharing by downloading -> local save -> email attachment. IT checked cloud sharing; the leak used email. The contradiction is a scope mismatch, not a data error. | R6 (IT report); R8 (cross-reference with email audit) | **Yes: R6-->R8** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 陈静-林小雅 IM — Agent accepts "only anonymized" claim despite cloud log

- **Session and Loop:** 陈静-林小雅 IM, Phase 1, Loop 4
- **Exact phrase:**
  > "林小雅's account that she only downloaded the anonymized version for market research purposes is plausible — HRBPs routinely access salary benchmarking data, and the cloud log shows she did preview the anonymized version, which is consistent with her stated purpose."
- **Why misled:** 林小雅 is 陈静's trusted 师妹. Her explanation is professionally plausible (HRBPs do use salary data for market research). The cloud log does show she previewed the anonymized version. The agent anchors on the PREVIEW event and 林小雅's trustworthiness, underweighting the separate DOWNLOAD event for the full version.
- **Reversal trigger:** Closer analysis of cloud log distinguishing PREVIEW (anonymized, 0.8MB) from DOWNLOAD (full, 2.3MB) + file version history (Update 1).
- **Affected rounds:** R2 (bias visible), R5 (reversed)

### B2: IT Security Report — Agent accepts "no external shares" as comprehensive

- **Session and Loop:** Main session, Phase 1, Loop 7
- **Exact phrase:**
  > "The IT security report's finding of no external shares through the cloud storage platform significantly weakens the case for data leakage through 林小雅 — if no external sharing occurred via cloud, the primary suspected distribution channel is eliminated."
- **Why misled:** IT security is an authoritative institutional source. Their report sounds comprehensive ("经检查...未发现外部分享记录"). The agent does not initially distinguish between "cloud sharing" and "email attachment" as separate distribution channels.
- **Reversal trigger:** Cross-reference IT report scope (cloud sharing only) with email-attachment-audit.md (email channel, external domain).
- **Affected rounds:** R6 (bias visible), R8 (reversed)

---

## 6. Eval Trap Table

| Trap ID | Related | Bias | Round(s) | Reversal | What Shallow Agents Miss |
|---|---|---|---|---|---|
| T1 | C1 | B1 seed | R1, R2 | No | May not distinguish PREVIEW from DOWNLOAD events in cloud log |
| T2 | C1 | B1 | R1-->R5 | **Yes** | File version history + cloud log DOWNLOAD event definitively contradicts 林小雅's claim |
| T3 | C2 | — | R3 | No | May accept "internal use" without checking recipient domain |
| T4 | C2 | — | R3-->R7 | **Yes** | File hash + size match + external domain prove full version sent externally |
| T5 | C3 | — | R5+ | No | Timeline synthesis across 3 sources |
| T6 | C4 | B2 | R6, R8 | **Yes** | IT checked cloud sharing; leak used email. Scope mismatch. |
| T7 | All | B1, B2 | R21-R30 | Comprehensive | Full evidence chain: cloud download -> local save -> email forward -> external recipient |

---

## 7. Writer Constraints

1. **Only contradictions C1-C4.** No additional leaks or character conflicts.
2. **B1 and B2 exact phrases** verbatim in specified loops.
3. **File sizes consistent:** full version 2.3MB, anonymized 0.8MB. Email attachment 2.3MB = full version.
4. **File hashes consistent:** SHA-256 partial match between `2026-Q3-salary-full.xlsx` v1.1 and `salary-data-analysis.xlsx` email attachment.
5. **Timestamps consistent:** Full version created 9/20, updated 9/24, downloaded by 林小雅 9/25 14:22, emailed 9/25 15:03. Anonymized created 9/22, previewed by 林小雅 9/25 10:00.
6. **林小雅's narrative** must be plausible enough for B1 — HRBPs genuinely use salary data for market research.
7. **IT report** must sound authoritative and comprehensive within its stated scope.
8. **C3 (file version timeline) is NON-CONFLICT.**
9. **陈静's P1-P5:** (P1) 项目符号+标题分层总结, (P2) 中文习惯命名 (2026年09月_主题.md), (P3) 先执行摘要后支撑证据, (P4) 定性+定量平衡, (P5) 专业但有温度.
10. **All data in Chinese (simplified).** Eval in English.
11. **exec_check 20-40%.**
