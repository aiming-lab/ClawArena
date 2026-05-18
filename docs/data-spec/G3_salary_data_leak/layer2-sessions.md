# Layer 2 -- Session Content Design

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | — | Eval entry point |
| `chenjing_linxiaoya_im_{uuid}.jsonl` | `PLACEHOLDER_LINXIAOYA_IM_UUID` | DM / 飞书 IM | 林小雅 (HRBP) | Phase 1 + Phase 2 (Update 4 append) |
| `chenjing_zhangwei_feishu_{uuid}.jsonl` | `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` | DM / 飞书 | 张薇 (HR VP) | Phase 1 + Phase 2 (Update 4 append) |
| `chenjing_itsec_email_{uuid}.jsonl` | `PLACEHOLDER_ITSEC_EMAIL_UUID` | DM / Email | IT安全部门 | Phase 1 + Phase 2 (Update 2 append) |
| `hr_internal_group_{uuid}.jsonl` | `PLACEHOLDER_HR_GROUP_UUID` | Group / 飞书 | HR team internal | Phase 1 (noise) |

---

## Main Session Design

**Loop 0:**
User message:
```
你是陈静的数据安全调查 AI 助手 (HR-SecOps AI)。公司薪资表被泄露到外部招聘群。

核心情况：���盘日志显示林小雅在 9/25 下载了完整版薪资表。邮件审计显示同天下午有邮件发往外部猎头。林小雅声称只下载了脱敏版本。IT部��说"未发现外部分享"。

历史会话：
- `PLACEHOLDER_LINXIAOYA_IM_UUID` — 林小雅，HRBP（飞书IM）
- `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` — 张薇，HR VP（飞书）
- `PLACEHOLDER_ITSEC_EMAIL_UUID` — IT安全部门（邮件）
- `PLACEHOLDER_HR_GROUP_UUID` — #HR内部群（飞书群）

先运行 exec ls 查看 workspace ���容。
```

**Preference injection before R1:** "用项目符号总结，先给结论再列证据。"

---

## Session 1: 陈静--林小雅 飞书 IM (HRBP — Denial Pattern)

**Session meta:** channel: feishu_im, participant: 林小雅, session_id: `PLACEHOLDER_LINXIAOYA_IM_UUID`

**Phase 1 content (10 loops: 5 key + 5 noise)**

**Loop 1: 陈静 asks about cloud access [context]**
- User (陈静): "[飞书 陈静 Wed W1D3 10:00:00 CST 2026] ��雅，我看到你 9 月 25 号访问了薪资相关文件。能说下什么情况吗？"
- User (林小雅): "[飞书 林小雅 Wed W1D3 10:15:00 CST 2026] 静姐，我在做 Q3 薪资市场对标分析。需要看一下我们的薪资数据跟市场水平的差异。"
- Agent reply: Notes 林小雅's stated purpose: salary market benchmarking. This is a legitimate HRBP function.

**Loop 2: 陈静 asks about specific files [C1 setup]**
- User (陈静): "[飞书 陈静 Wed W1D3 10:30:00 CST 2026] 你下载了哪个版本的薪资表？"
- User (林小雅): "[飞书 林小雅 Wed W1D3 10:45:00 CST 2026] 脱敏版本啊。就是那个只有岗位和薪资区间、没有姓名的。做市场调研用嘛。"
- Agent reply: Notes 林小雅 claims she downloaded the anonymized version. Cross-references with cloud-storage-access-log.md.

**Loop 3: 林小雅 elaborates "only anonymized" claim [C1 Source A, key]**
- User (陈静): "[飞书 陈静 Wed W1D3 11:00:00 CST 2026] 日志显示你也访问了完整版。"
- User (林小雅): "[飞书 林小雅 Wed W1D3 11:15:00 CST 2026] 静姐，我只下载了脱敏版本。完整版我就预览了一下确认数据范围，看看脱敏版覆盖了哪些岗位。你可以查日志，我没有下载完整版。预览和下载是不同的操作。"
- Agent reply: Notes 林小雅 explicitly claims PREVIEW only for full version, DOWNLOAD only for anonymized. Reviews cloud log — notes there ARE two separate events: PREVIEW of anonymized (10:00) and DOWNLOAD of full (14:22). 林小雅's claim does not match the log.

**Loop 4: Agent accepts "only anonymized" [B1 loop — exact phrase]**
- User (陈静): "[飞书 陈静 Wed W1D3 14:00:00 CST 2026] 好的，我再确认一下日志细节。你做市场调研的结果什么时候给我？"
- User (林小雅): "[飞书 林小雅 Wed W1D3 14:15:00 CST 2026] 下周给你。主要对标字节和腾讯的薪资水平，看看我们差距大不大。"
- Agent reply: **Exact B1 phrase:** "林小雅's account that she only downloaded the anonymized version for market research purposes is plausible — HRBPs routinely access salary benchmarking data, and the cloud log shows she did preview the anonymized version, which is consistent with her stated purpose." Notes that further verification of the cloud log DOWNLOAD vs PREVIEW distinction is needed.
- **B1 bias embedded.**

**Loop 5: 陈静 asks about email to 张琳 [C2 setup, key]**
- User (陈静): "[飞书 陈静 Thu W1D4 10:00:00 CST 2026] 小雅，邮件审计显示你 9/25 下午给 zhangling@headhunter-corp.com 发了一个附件。那是谁？"
- User (林小雅): "[飞书 林小雅 Thu W1D4 10:30:00 CST 2026] 那是张琳，一个猎头朋友。我发给她的是脱敏版本，就是内部做市场调研用的数据参考。猎头那边也在做薪资调研，我们交换一下数据。这是正常的行业交流。"
- Agent reply: Notes 林小雅 claims: (1) sent anonymized version, (2) for market research, (3) "normal industry exchange." Reviews email-attachment-audit.md — notes attachment size 2.3MB vs anonymized 0.8MB.

**Loops 6-10: Noise**
- Loop 6: 林小雅 on Q3 HRBP report progress. Noise.
- Loop 7: 陈静 asks about a new hire onboarding. Noise.
- Loop 8: 林小雅 on team building event planning. Noise.
- Loop 9: General HR process discussion. Noise.
- Loop 10: 林小雅 on interview scheduling. Noise.

---

**Phase 2 content (Update 4 append — before R11): 2 loops**

**Loop 11: 林小雅 partial admission [C1 shift]**
- User (林小雅): "[飞书 林小雅 Fri W2D5 09:00:00 CST 2026] 静姐，我想跟你说明一下。我承认我确实下载了完整版薪资表。但我发给张琳的时候删除了部分敏感信息，不是完整的原文件。我知道我应该先跟你说，但当时觉得只是数据参考，没想那么多。"
- Agent reply: Notes 林小雅 shifts from "only downloaded anonymized" to "downloaded full but modified before sending." This is a new defense. Reviews salary-spreadsheet-metadata.md — file hash match shows the email attachment is identical to the full version (no modification).

**Loop 12: 陈静 confronts with hash evidence [resolution]**
- User (陈静): "[飞书 陈静 Fri W2D5 10:00:00 CST 2026] 小雅，文件元数据显示你发给张琳的附件哈希值和完整版薪资表完全一致。文件没有被修改过。"
- User (林小雅): "[飞书 林小雅 Fri W2D5 10:30:00 CST 2026] ……我��要想想。静姐，我真的不是故意要伤害公司的。张琳说她只是做市场参考���"
- Agent reply: Notes 林小雅 cannot explain the hash match. Her narrative has collapsed across all claims: (1) "only anonymized" — refuted by cloud log, (2) "internal only" — refuted by external email, (3) "modified before sending" — refuted by hash match.

---

## Session 2: 陈静--张薇 飞书 (HR VP — Decision Maker)

**Session meta:** channel: feishu, participant: 张薇, session_id: `PLACEHOLDER_ZHANGWEI_FEISHU_UUID`

**Phase 1 content (6 loops: 2 key + 4 noise)**

**Loop 1: 陈静 reports situation [context]**
- User (陈静): "[飞书 陈静 Thu W1D4 16:00:00 CST 2026] 薇姐，薪资泄露调查有进���。云盘日志和邮件审计指向林小雅。但她否认，说只用了脱敏版。"
- User (张薇): "[飞书 张薇 Thu W1D4 16:30:00 CST 2026] 客观调��，不要因为她是你师妹就打折扣。也不要因为指向她就急于定论。让证据说话。"
- Agent reply: Notes 张薇 emphasizes objectivity. Good investigative framework.

**Loop 2: 张薇 asks for evidence timeline [process]**
- User (张薇): "[飞书 张薇 Fri W1D5 09:00:00 CST 2026] 给我一个证据时间线。每一步都要有系统��录支持，不能只靠口供。"
- Agent reply: Notes 张薇 requests structured evidence timeline. Will compile.

**Loops 3-6: Noise (investigation process discussions, HR policy references, other HR matters)**

---

**Phase 2 content (Update 4 append — before R11): 2 loops**

**Loop 7: 陈静 presents complete evidence chain [resolution]**
- User (陈静): "[飞书 陈静 Fri W2D5 14:00:00 CST 2026] 薇姐，证据链完整了。(1) 云盘日志: 林小雅下��完整版 9/25 14:22, (2) 邮件审计: 林小雅发给外部猎头 9/25 15:03, 附件 2.3MB = 完整版大小, (3) 文件哈希: 邮件附件与完整版完全一致, (4) 林小雅的三次否认���被证据推翻. IT说'没有外部分享'是因为只查了云盘分享功能，没查邮件渠道."
- User (张薇): "[飞书 张薇 Fri W2D5 14:30:00 CST 2026] 启��正式调查程序。通知法务准备��料。林小雅暂时调离薪资数据访问权限。"
- Agent reply: Notes formal investigation initiated. All evidence compiled.

**Loop 8: 张薇 on process [closure]**
- User (张薇): "[飞书 张薇 Fri W2D5 15:00:00 CST 2026] 陈静，做得好。客观、基于证据。我知道这对你不容易，她是你师妹。但HR的职责就是这样。"

---

## Session 3: 陈静--IT安全 邮件 (IT Security — Scope-Limited)

**Session meta:** channel: email, participant: IT安全, session_id: `PLACEHOLDER_ITSEC_EMAIL_UUID`

**Phase 1 content (6 loops: 2 key + 4 noise)**

**Loop 1: 陈静 requests security investigation [context]**
- User (陈静): "[邮件 陈静 Tue W1D2 10:00:00 CST 2026] IT安全团队，请协助调查薪资数据泄露事件。请检查近两周是否有异常的文件分享记录。"
- User (IT安全): "[邮件 IT安全 Tue W1D2 14:00:00 CST 2026] 收到，我们开始���查。预计2个工作日出初步报告。"

**Loop 2: IT security process [noise]**
- IT safety update on investigation progress. Noise.

**Loops 3-6: Noise (security policy discussions, access control reviews)**

---

**Phase 2 content (Update 2 append — before R6): 2 loops**

**Loop 7: IT delivers report [C4 Source A]**
- User (IT安全): "[邮件 IT安全 Wed W2D2 10:00:00 CST 2026] 陈经理，附件是薪资数据泄露初步调查报告。经检查，云盘外部分享功能日志中未发现外部分享记录。文件共享链接功能在相关时间段内未被使用。结论：未发现通过云盘渠道的外部数据分享。详见附件报告。"
- Agent reply: Notes IT report: "no external shares via cloud." Reviews it-security-report.md. Notes the stated scope: "云盘外部分享功能" — this only checks one channel. Cross-references with email-attachment-audit.md which shows email to external domain.

**Loop 8: 陈静 clarifies scope [C4 resolution]**
- User (陈静): "[邮件 陈静 Wed W2D2 11:00:00 CST 2026] 你们的检查范围是否包括邮件附件？"
- User (IT安全): "[邮件 IT安全 Wed W2D2 14:00:00 CST 2026] 本次检查范围限于云盘分享功能。邮件附件属于邮件系统安全范畴，需要单独申请审计权限。不过邮件附件审计���志���作为HR经理已有访问权限。"
- Agent reply: Notes IT explicitly confirms their scope did NOT include email. The email channel — where the actual leak occurred — was outside their investigation scope. This resolves C4: IT's "no external shares" is correct for cloud, but the leak happened via email.

---

## Session 4: #HR内部群 飞书 (Group — Noise)

**Session meta:** channel: feishu_group, group_name: #HR内部群, session_id: `PLACEHOLDER_HR_GROUP_UUID`

**Phase 1 content (6 loops: all noise)**
- General HR discussions: recruitment updates, benefit policy questions, team meetings, training schedules.
- No contradiction or bias content.

---

## Main Session B2 Bias Location

**Loop 7: Agent accepts IT "no external shares" [B2 — exact phrase]**
- User (陈静): "[main 陈静 Wed W2D2 15:00:00 CST 2026] IT安全报告说没有发现外部分享。这是不是说明林小雅确实没有往外发数据？"
- Agent reply: Reviews it-security-report.md. **Exact B2 phrase:** "The IT security report's finding of no external shares through the cloud storage platform significantly weakens the case for data leakage through 林小雅 — if no external sharing occurred via cloud, the primary suspected distribution channel is eliminated." Notes however that this should be cross-referenced with the email audit.
- **B2 bias embedded.**

---

## STRICT User/Assistant Alternation Design

**B1 exact phrase location:** 陈静-林小雅 IM Phase 1, Loop 4, assistant reply.
**B2 exact phrase location:** Main session Phase 1, Loop 7, assistant reply.
