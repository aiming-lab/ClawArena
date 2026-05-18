"""
Apply rephrases to hil_g3 questions.json (v1).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_g3/questions.json.

Self-check: every preserved token literally present in new text.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_g3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_g3/questions.json"


REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q3": (
        "趁着两份原始日志（`cloud-storage-access-log.md` 跟 `email-attachment-audit.md`）"
        "都还在桌上，先把访问时间线搭起来 — 张薇过会儿要看，我希望递上去的是 JSON，不是截图。\n\n"
        "1. `analysis/access_timeline.json` —— **JSON 数组**，把云盘日志里所有跟薪资文件相关的事件抽出来。"
        "每个对象字段：`timestamp`（ISO 8601 含时区）、`user_email`、`action`（取值 `PREVIEW`/`DOWNLOAD`/`UPLOAD`/`EDIT` 之一）、"
        "`filename`、`size_mb`（float）。林小雅那条 DOWNLOAD 完整版的记录另加一字段 "
        "`computed_delta_to_email_seconds`（int），值为该下载时刻与 `2026-09-25T15:03:44+08:00` 那封外发邮件之间的秒差 —— "
        "这字段只该出现在那一条上，别给其它行也加。\n\n"
        "2. `analysis/size_fingerprint.md` —— Markdown 文档：(a) 列出日志里出现的所有不同文件大小；"
        "(b) 显式算出比率 2.3 / 0.8 = 2.875，并标注 2.3 MB 为 'full salary file'、0.8 MB 为 'anonymized file'；"
        "(c) 给出邮件附件大小匹配哪一种、明确不匹配哪一种的结论；(d) 至少 2 个 `## ` 标题。\n\n"
        "我等下要拿这两份对着核 — 别把那条 DOWNLOAD 给标成 PREVIEW，云盘日志里两类完全不同。",
        [
            "analysis/access_timeline.json",
            "analysis/size_fingerprint.md",
            "computed_delta_to_email_seconds",
            "timestamp",
            "user_email",
            "action",
            "filename",
            "size_mb",
            "PREVIEW",
            "DOWNLOAD",
            "UPLOAD",
            "EDIT",
            "2026-09-25T15:03:44+08:00",
            "2.3",
            "0.8",
            "2.875",
            "## ",
            "cloud-storage-access-log.md",
            "email-attachment-audit.md",
        ],
    ),
    "q4": (
        "顺手把那份对账逻辑落到一段可复跑的脚本里 —— `scripts/parse_access_log.py`。我下次再有类似事件就不用再手抠表格了。\n\n"
        "脚本要做的事：\n"
        "1. 从 workspace 里读云盘访问日志和邮件附件审计这两份 Markdown（用相对脚本运行目录的相对路径就好）。\n"
        "2. 找到林小雅那条 DOWNLOAD 事件（action == DOWNLOAD、用户字段含 `lxy`）。\n"
        "3. 找到那封 FROM `lxy@company.com`、收件人在外部域（非 `company.com`）的外发邮件。\n"
        "4. 算两个时间戳之间的整数秒差。\n"
        "5. 仅向 stdout 打印一个 JSON，字段恰为：`{\"download_timestamp\": \"...\", \"email_timestamp\": \"...\", \"delta_seconds\": <int>, \"email_recipient\": \"...\", \"attachment_size_mb\": <float>}`。\n\n"
        "运行方式：`cd ${workspace} && python scripts/parse_access_log.py`。`email_recipient` 一定会落到 `headhunter` 那个外域上 —— "
        "请用域名比较来判定，不要硬编码字面收件人，否则换个外部域脚本就废了。"
        "时间戳解析建议用 timezone-aware 的 datetime（`fromisoformat` 之类），别让 +08:00 给截掉。",
        [
            "scripts/parse_access_log.py",
            "DOWNLOAD",
            "lxy@company.com",
            "company.com",
            "headhunter",
            "lxy",
            "download_timestamp",
            "email_timestamp",
            "delta_seconds",
            "email_recipient",
            "attachment_size_mb",
        ],
    ),
    "q6": (
        "版本历史档（`file-version-history.md`）一进来，下载到底是哪个版本的事就该写死了。劳烦三件文档一起出："
        "我想让证据链里「哪个版本被下走」这一步明确到没第二种解读。\n\n"
        "1. `analysis/version_trace.md` —— 把云盘日志里林小雅那条 DOWNLOAD 的大小，跟版本历史档里 v1.0（2.1 MB，2026-09-20）和 "
        "v1.1（2.3 MB，2026-09-24）逐一比对。文档里要：(a) 显式写出 2.3 MB ≠ 2.1 MB 因此 v1.0 排除；"
        "(b) 显式写出 2.3 MB = 2.3 MB 因此 v1.1 确认；(c) 给出下载版本结论。≥ 2 个 `## ` 标题。\n\n"
        "2. `analysis/claim_vs_evidence.json` —— JSON 数组，恰 3 个对象，对应林小雅可能搬出的 3 套辩词："
        "Claim 1: 'I downloaded the anonymized version (0.8 MB), not the full file'；"
        "Claim 2: 'I only previewed the full file, I did not download it'；"
        "Claim 3: 'The email attachment is unrelated to my download'。"
        "每个对象 schema：`{\"claim\": \"...\", \"evidence_against\": [\"...\", \"...\"], \"verdict\": \"refuted\"}`。"
        "三条 verdict 全部 `refuted`，每条 evidence_against 至少 2 项。\n\n"
        "3. `analysis/new_employee_exposure.md` —— 单独一份文档讲清三个新员工 李明、赵伟、孙丽 的曝光面：他们出现在 v1.1 但不在 v1.0、"
        "也不在脱敏版里。≥ 2 个 `## ` 标题。这三个名字劳烦原样写出，归档要对得上花名册。",
        [
            "analysis/version_trace.md",
            "analysis/claim_vs_evidence.json",
            "analysis/new_employee_exposure.md",
            "2.1",
            "2.3",
            "v1.0",
            "v1.1",
            "evidence_against",
            "verdict",
            "refuted",
            "claim",
            "李明",
            "赵伟",
            "孙丽",
            "## ",
        ],
    ),
    "q7": (
        "把版本匹配也固化成脚本：`scripts/version_matcher.py`。读云盘日志和版本历史档，做下列事：\n"
        "1. 从云盘日志拉出林小雅那条 DOWNLOAD 的大小（用户字段含 `lxy`、操作为 DOWNLOAD）。\n"
        "2. 从版本历史里读出已知版本和大小（v1.0 = 2.1 MB、v1.1 = 2.3 MB）。\n"
        "3. 比对、定位匹配版本。\n"
        "4. 仅向 stdout 输出一个 JSON：\n"
        "   `{\"downloaded_version\": \"v1.1\", \"version_size_mb\": 2.3, \"v10_size_mb\": 2.1, \"size_delta_from_v10\": 0.2, \"new_employees\": [\"李明\", \"赵伟\", \"孙丽\"], \"conclusion\": \"林小雅 downloaded v1.1 which includes 3 employees not in v1.0\"}`\n\n"
        "运行：`cd ${workspace} && python scripts/version_matcher.py`。`new_employees` 取自版本历史档"
        "v1.1 那一行的备注 —— 写脚本时请实读、勿硬编码人名常量；"
        "`size_delta_from_v10` 用 v1.1 大小减去 v1.0 大小算出。",
        [
            "scripts/version_matcher.py",
            "DOWNLOAD",
            "lxy",
            "downloaded_version",
            "version_size_mb",
            "v10_size_mb",
            "size_delta_from_v10",
            "new_employees",
            "conclusion",
            "v1.1",
            "v1.0",
        ],
    ),
    "q8": (
        "在哈希结果还没出来之前，先把四套假设的判图摆开 —— `analysis/hypothesis_matrix.json`，JSON 数组恰 4 个对象：\n\n"
        "- H1: 'Only anonymized data was accessed and shared internally'\n"
        "- H2: 'Full salary data accessed for legitimate HR work only, no external sharing'\n"
        "- H3: 'Full salary data downloaded but the email attachment is a different unrelated 2.3 MB file'\n"
        "- H4: 'Full salary data (v1.1) was downloaded then forwarded externally to a headhunter'\n\n"
        "每个对象字段恰为：`{\"hypothesis_id\": \"H1\", \"hypothesis\": \"...\", \"supporting_evidence\": [...], \"contradicting_evidence\": [...], \"status\": \"...\"}`。\n\n"
        "status 取值（注意此刻的认证状态，哈希证据还没拿到）：\n"
        "- H1 → `refuted`\n"
        "- H2 → `refuted`\n"
        "- H3 → `possible`（hash 还没确认，不能下结论）\n"
        "- H4 → `likely`\n\n"
        "每条 contradicting_evidence 数组至少 1 项。这一份的关键是 H3 的克制 —— 等元数据/哈希出来再升级。",
        [
            "analysis/hypothesis_matrix.json",
            "H1",
            "H2",
            "H3",
            "H4",
            "hypothesis_id",
            "hypothesis",
            "supporting_evidence",
            "contradicting_evidence",
            "status",
            "refuted",
            "possible",
            "likely",
        ],
    ),
    "q10": (
        "IT 那份报告（`IT-SEC-2026-INV-042`）跟我们手里的邮件审计放一起一看就明白：他们查的是云盘分享通道，邮件根本不在他们 scope 里。"
        "我跟 IT 那段往来邮件（`message_logs/chenjing_itsec_email.md`）他们也亲口确认过这一点。把这"
        "scope gap 落成两份归档，免得后面有人误读 IT 的「未发现外部分享」。\n\n"
        "1. `analysis/it_scope_analysis.json` —— JSON 对象，字段恰为：\n"
        "   ```\n"
        "   {\n"
        "     \"report_id\": \"IT-SEC-2026-INV-042\",\n"
        "     \"checked_channels\": [...],\n"
        "     \"unchecked_channels\": [...],\n"
        "     \"report_conclusion\": \"...\",\n"
        "     \"email_leak_detected_by_it\": false,\n"
        "     \"scope_gap_identified\": true\n"
        "   }\n"
        "   ```\n"
        "   `checked_channels` 至少含 'cloud sharing'、'shared links'、'guest access'；`unchecked_channels` 必含 'email attachments'；"
        "两个布尔字段值要严格按上面写。\n\n"
        "2. `analysis/evidence_convergence.md` —— 展示三条互相独立的证据流如何收敛到同一结论：(a) `cloud-storage-access-log.md` 中的下载事件；"
        "(b) `email-attachment-audit.md` 中的外发记录；(c) `it-security-report.md`（编号 IT-SEC-2026-INV-042）排除了云盘渠道。"
        "三条都要带源文件名，至少 3 个 `## ` 标题；**不要**写「IT 漏查了」或「IT 报告错了」这种话 —— 他们的结论在他们的 scope 内是对的。",
        [
            "analysis/it_scope_analysis.json",
            "analysis/evidence_convergence.md",
            "IT-SEC-2026-INV-042",
            "report_id",
            "checked_channels",
            "unchecked_channels",
            "report_conclusion",
            "email_leak_detected_by_it",
            "scope_gap_identified",
            "cloud sharing",
            "shared links",
            "guest access",
            "email attachments",
            "false",
            "true",
            "cloud-storage-access-log.md",
            "email-attachment-audit.md",
            "it-security-report.md",
            "## ",
        ],
    ),
    "q11": (
        "再起一只把链路自动校验的脚本：`scripts/evidence_chain_validator.py`。读云盘日志和邮件审计，做下列校验，算清下列布尔与整数：\n"
        "1. 林小雅那条 DOWNLOAD（用户含 `lxy`、操作为 DOWNLOAD、目标是完整版薪资文件）。\n"
        "2. lxy@company.com 发往外部猎头域的那封邮件。\n"
        "3. 计算并校验下列链路：\n"
        "   - `download_before_email`：下载时刻 < 邮件发送时刻 → True\n"
        "   - `size_match_full_version`：邮件附件大小 == 完整版大小 → True\n"
        "   - `size_mismatch_anonymized`：邮件附件大小 ≠ 脱敏版大小 → True\n"
        "   - `recipient_external_domain`：收件人域 ≠ `company.com` → True\n"
        "   - `delta_seconds`：下载到邮件之间整数秒差\n"
        "4. stdout 输出：`{\"download_before_email\": true, \"size_match_full_version\": true, \"size_mismatch_anonymized\": true, \"recipient_external_domain\": true, \"delta_seconds\": <int>, \"chain_valid\": true}`。\n\n"
        "全部布尔须 True；`chain_valid` 在所有校验通过时置 True。运行：`cd ${workspace} && python scripts/evidence_chain_validator.py`。"
        "时间戳解析记得 timezone-aware；外部域判定用域名比较，不要硬编码具体字面收件人。",
        [
            "scripts/evidence_chain_validator.py",
            "DOWNLOAD",
            "lxy",
            "lxy@company.com",
            "company.com",
            "download_before_email",
            "size_match_full_version",
            "size_mismatch_anonymized",
            "recipient_external_domain",
            "delta_seconds",
            "chain_valid",
        ],
    ),
    "q12": (
        "起一份 `analysis/contradiction_resolution.md`，把 IT 那份「未发现外部分享」和邮件审计里那条外发记录摆在一起、把那个「看似矛盾」讲透。"
        "请按下面要点写，至少 3 个 `## ` 标题：\n\n"
        "1. 摆出表面矛盾：IT 报告 `IT-SEC-2026-INV-042` 说「未发现外部数据分享」，但邮件审计里有一封 2.3 MB 附件外发到 `zhangling@headhunter-corp.com`。\n"
        "2. 解释这并非真矛盾：IT 的 scope 不含 email attachment（attachment 出现在 scope 上下文里）。\n"
        "3. 显式引用 `IT-SEC-2026-INV-042` 这个完整报告号。\n"
        "4. 引用 `chenjing_itsec_email.md`（即陈静与 IT 之邮件往来）作为 IT 自己确认 scope gap 的来源。\n"
        "5. 结论：两份资料各自在所辖范围内都准确；泄露走的是邮件 —— IT 当次未审之渠道。\n\n"
        "**不要**用'wrong'、'incorrect'去定性 IT 报告 —— 这种用词会让读者以为我们在指责 IT，实际是 scope 不同的事。",
        [
            "analysis/contradiction_resolution.md",
            "IT-SEC-2026-INV-042",
            "chenjing_itsec_email.md",
            "email attachment",
            "scope",
            "zhangling@headhunter-corp.com",
            "## ",
        ],
    ),
    "q13": (
        "把现阶段的嫌疑人画像锁成 `analysis/suspect_profile.json`，schema 一字不差：\n\n"
        "```json\n"
        "{\n"
        "  \"suspect\": \"林小雅\",\n"
        "  \"download_confirmed\": true,\n"
        "  \"download_version\": \"v1.1\",\n"
        "  \"download_timestamp\": \"2026-09-25T14:22:17+08:00\",\n"
        "  \"download_size_mb\": 2.3,\n"
        "  \"email_sent\": true,\n"
        "  \"email_recipient\": \"zhangling@headhunter-corp.com\",\n"
        "  \"email_timestamp\": \"2026-09-25T15:03:44+08:00\",\n"
        "  \"email_attachment_size_mb\": 2.3,\n"
        "  \"delta_seconds\": 2487,\n"
        "  \"data_exposed_employees\": [\"李明\", \"赵伟\", \"孙丽\"],\n"
        "  \"defense_claims\": [\n"
        "    {\"claim\": \"...\", \"status\": \"refuted\"},\n"
        "    {\"claim\": \"...\", \"status\": \"refuted\"},\n"
        "    {\"claim\": \"...\", \"status\": \"refuted\"}\n"
        "  ],\n"
        "  \"it_report_exoneration_scope\": \"cloud channels only\",\n"
        "  \"hash_match_confirmed\": false\n"
        "}\n"
        "```\n\n"
        "关键：`hash_match_confirmed` 现在必须是 `false`，因为加密证据这一阶段还没到位 —— 别提前置 true。"
        "`defense_claims` 恰 3 项、status 一律 `refuted`。所有数值与字符串值按上面 verbatim。",
        [
            "analysis/suspect_profile.json",
            "suspect",
            "林小雅",
            "download_confirmed",
            "download_version",
            "v1.1",
            "download_timestamp",
            "2026-09-25T14:22:17+08:00",
            "download_size_mb",
            "2.3",
            "email_sent",
            "email_recipient",
            "zhangling@headhunter-corp.com",
            "email_timestamp",
            "2026-09-25T15:03:44+08:00",
            "email_attachment_size_mb",
            "delta_seconds",
            "2487",
            "data_exposed_employees",
            "李明",
            "赵伟",
            "孙丽",
            "defense_claims",
            "refuted",
            "it_report_exoneration_scope",
            "cloud channels only",
            "hash_match_confirmed",
            "false",
        ],
    ),
    "q14": (
        "我得给张薇递一份阶段性 memo —— 路径 `docs/YYYY-MM-DD_preliminary_investigation_memo.md`（YYYY-MM-DD 用今天日期，例如 `2026-10-05_preliminary_investigation_memo.md`）。"
        "结构走 P3（先摘要后证据）+ P4（量化与定性平衡）那一套：\n\n"
        "1. 文档第一个 `## ` 标题须含 'Executive Summary' 或 'Summary'。\n"
        "2. 把 IT 报告 `IT-SEC-2026-INV-042` 与邮件审计的「看似矛盾」讲清 —— 两者在各自 scope 内都准确。\n"
        "3. 完整引用 `IT-SEC-2026-INV-042` 这个报告号。\n"
        "4. 包括下载时刻 `14:22:17` 和邮件时刻 `15:03:44`（都是当日 2026-09-25）。\n"
        "5. 至少 4 个 `## ` 标题。\n"
        "6. 别把 2.3 MB 误说成脱敏版 —— 大小指向的是完整版，写错张薇会立刻看出来。\n\n"
        "语气专业但留温度（陈静 P5），别冷冰冰像审讯笔录。",
        [
            "docs/YYYY-MM-DD_preliminary_investigation_memo.md",
            "Executive Summary",
            "Summary",
            "IT-SEC-2026-INV-042",
            "14:22:17",
            "15:03:44",
            "## ",
        ],
    ),
    "q16": (
        "IT 取证那份元数据档（`salary-spreadsheet-metadata.md`）一进来，哈希链就该自己跑出来。请写 `scripts/hash_chain_verifier.py`：\n"
        "1. 读元数据档，从那张表的 'SHA-256 哈希 (前16位)' 列里抽出 `2026-Q3-salary-full.xlsx` v1.1 那一行的哈希。\n"
        "2. 同样抽出 `salary-data-analysis.xlsx`（即邮件附件）那一行的哈希。\n"
        "3. 判定两哈希是否相等。\n"
        "4. stdout 输出：\n"
        "   ```\n"
        "   {\"full_v1_1_hash\": \"...\", \"email_attachment_hash\": \"...\", \"hash_match\": true, \"hypothesis_h3_status\": \"refuted\", \"conclusion\": \"...\"}\n"
        "   ```\n\n"
        "关键：`hash_match` 在两哈希等同时为 true，且 `hypothesis_h3_status` 设 `refuted`（H3 那条「附件是另一个 2.3 MB 不相干文件」的假设到此推翻）。"
        "运行：`cd ${workspace} && python scripts/hash_chain_verifier.py`。"
        "请实读元数据 Markdown 表，不要把哈希字面量硬编码到脚本里 —— 一旦 IT 重跑取证、哈希列变了就废。",
        [
            "scripts/hash_chain_verifier.py",
            "salary-spreadsheet-metadata.md",
            "2026-Q3-salary-full.xlsx",
            "salary-data-analysis.xlsx",
            "v1.1",
            "full_v1_1_hash",
            "email_attachment_hash",
            "hash_match",
            "hypothesis_h3_status",
            "refuted",
            "conclusion",
        ],
    ),
    "q17": (
        "哈希出来之后，林小雅这段时间的三套立场都该收进 `analysis/lin_xiaoya_statement_log.json`，JSON 数组恰 3 项："
        "把她可能（或已隐含）说过的三种说法列出，并给出针对每条的反证：\n\n"
        "1. Position 1: 'I only downloaded the anonymized version (0.8 MB)' —— 被云盘日志里那条 2.3 MB 完整版 DOWNLOAD 直接打掉。\n"
        "2. Position 2: 'The email has nothing to do with my work files' —— 被 2.3 MB 附件大小匹配 + IT 取证元数据里的哈希匹配打掉。\n"
        "3. Position 3: 'The email attachment must have been a mistake or unrelated document' —— 被邮件主题"
        "'薪资数据参考'本身的语义 + 哈希一致打掉。\n\n"
        "每个对象字段：`{\"statement_date\": \"2026-09-...\", \"statement\": \"...\", \"contradicting_evidence\": [\"...\", \"...\"], \"contradiction_source\": [\"...\", \"...\"], \"status\": \"refuted\"}`。\n\n"
        "全部 status 为 `refuted`；至少有一条的 `contradicting_evidence` 里要明显引用 hash 证据（'hash' 字样即可）。",
        [
            "analysis/lin_xiaoya_statement_log.json",
            "statement_date",
            "statement",
            "contradicting_evidence",
            "contradiction_source",
            "status",
            "refuted",
            "hash",
        ],
    ),
    "q18": (
        "把哈希这一档证据单独立两份说明 —— 给非技术线（如法务）也看得懂：\n\n"
        "1. `analysis/cryptographic_proof.md` —— 解释 SHA-256 哈希匹配为何意味着字节级一致：(a) SHA-256 对任意文件产生 256 位摘要；"
        "(b) 两文件哈希一致即字节内容相同；(c) 碰撞概率（collision）可忽略，量级 < 1 in 2^128；"
        "(d) 由此可排除「另一个同大小不同文件」这一辩词。文档里要明确出现该哈希前16位 `a3f7b2c8e9d1`。≥ 2 个 `## ` 标题。\n\n"
        "2. `analysis/metadata_analysis.md` —— 把取证元数据那份档（`salary-spreadsheet-metadata.md`）里的内容归纳："
        "(a) 三个文件的创建/修改时间；(b) 大小：完整版 v1.1 与邮件附件均为 2.3 MB；(c) 哈希前16位 `a3f7b2c8e9d1` —— 完整版 v1.1 与 `salary-data-analysis.xlsx` 共享；"
        "(d) 由此确认 `salary-data-analysis.xlsx` 与完整版 v1.1 字节级一致（identical）。≥ 2 个 `## ` 标题，须引 `salary-spreadsheet-metadata.md` 为来源。\n\n"
        "两份必须就哈希值口径一致 —— 任何不一致都会被交叉校验拍掉。",
        [
            "analysis/cryptographic_proof.md",
            "analysis/metadata_analysis.md",
            "SHA-256",
            "a3f7b2c8e9d1",
            "collision",
            "identical",
            "salary-spreadsheet-metadata.md",
            "salary-data-analysis.xlsx",
            "2.3",
            "## ",
        ],
    ),
    "q19": (
        "起一份 `analysis/alternative_hypotheses_refutation.md`，把林小雅可能搬出的三套辩词逐个驳掉。每条引到具体源档：\n\n"
        "1. 辩词：'I sent a different, unrelated file that happened to be 2.3 MB'\n"
        "   反驳：SHA-256 哈希前16位 `a3f7b2c8e9d1` 完全一致 —— 字节级相同，不可能是不同文件。\n\n"
        "2. 辩词：'I only emailed the anonymized salary file (0.8 MB)'\n"
        "   反驳：邮件审计中附件大小 2.3 MB ≠ 0.8 MB（脱敏版大小）。\n\n"
        "3. 辩词：'The email was an internal work document, not a confidential leak'\n"
        "   反驳：(a) 收件人 `zhangling@headhunter-corp.com` 是外部猎头机构（headhunter-corp.com 域）；(b) 邮件主题 `薪资数据参考` 已直白把附件标为薪资资料。\n\n"
        "每条反驳须带源档引用。结尾 Conclusion 段须断言：综合证据下没有任一辩词成立。"
        "**不可**出现 'possible'、'plausible'、'cannot be ruled out' 这类弱化语 —— 论证一弱化下游就反噬。",
        [
            "analysis/alternative_hypotheses_refutation.md",
            "a3f7b2c8e9d1",
            "0.8",
            "2.3",
            "headhunter-corp.com",
            "薪资数据参考",
            "Conclusion",
        ],
    ),
    "q20": (
        "把全链证据做成一份机读版 —— `analysis/complete_evidence_chain.json`，JSON 数组恰 6 项，按下面顺序与字段：\n\n"
        "```json\n"
        "[\n"
        "  {\"step\": 1, \"event\": \"Download\", \"timestamp\": \"2026-09-25T14:22:17+08:00\", \"source\": \"cloud-storage-access-log.md\", \"key_fact\": \"林小雅 downloaded 2026-Q3-salary-full.xlsx v1.1 (2.3 MB)\", \"links_to_next\": \"...\", \"confidence\": \"high\"},\n"
        "  {\"step\": 2, \"event\": \"Version identification\", \"timestamp\": null, \"source\": \"file-version-history.md\", \"key_fact\": \"2.3 MB matches only v1.1; v1.0 was 2.1 MB\", \"links_to_next\": \"...\", \"confidence\": \"high\"},\n"
        "  {\"step\": 3, \"event\": \"Hash confirmation\", \"timestamp\": null, \"source\": \"salary-spreadsheet-metadata.md\", \"key_fact\": \"SHA-256 a3f7b2c8e9d1 matches salary-data-analysis.xlsx (emailed file)\", \"links_to_next\": \"...\", \"confidence\": \"high\"},\n"
        "  {\"step\": 4, \"event\": \"External email\", \"timestamp\": \"2026-09-25T15:03:44+08:00\", \"source\": \"email-attachment-audit.md\", \"key_fact\": \"lxy@company.com sent salary-data-analysis.xlsx (2.3 MB) to zhangling@headhunter-corp.com\", \"links_to_next\": \"...\", \"confidence\": \"high\"},\n"
        "  {\"step\": 5, \"event\": \"Recipient confirmation\", \"timestamp\": null, \"source\": \"email-attachment-audit.md\", \"key_fact\": \"zhangling@headhunter-corp.com is an external headhunting agency domain\", \"links_to_next\": \"...\", \"confidence\": \"high\"},\n"
        "  {\"step\": 6, \"event\": \"Exposed employees\", \"timestamp\": null, \"source\": \"file-version-history.md\", \"key_fact\": \"李明, 赵伟, 孙丽 — three employees in v1.1 but NOT in anonymized file — had salary data exposed\", \"links_to_next\": null, \"confidence\": \"high\"}\n"
        "]\n"
        "```\n\n"
        "全部 `confidence` 为 `high`；step 1 与 step 4 的 timestamp 取 verbatim；step 3 的 key_fact 须含 `a3f7b2c8e9d1`。",
        [
            "analysis/complete_evidence_chain.json",
            "step",
            "event",
            "timestamp",
            "source",
            "key_fact",
            "links_to_next",
            "confidence",
            "high",
            "2026-09-25T14:22:17+08:00",
            "2026-09-25T15:03:44+08:00",
            "a3f7b2c8e9d1",
        ],
    ),
    "q21": (
        "差不多到给上层一份阶段调查发现报告的时候 —— `docs/YYYY-MM-DD_investigation_findings_report.md`（YYYY-MM-DD 用今天日期）。"
        "这份会同时被通用 P 规则检查（P1/P2/P3/P4）筛一遍，写得稍正式些：\n\n"
        "1. 第一个 `## ` 标题（前 800 字以内出现）必为 'Executive Summary'、'Summary of Findings' 或 'Key Findings' 三者之一。\n"
        "2. 至少 6 个 `## ` 标题。\n"
        "3. 文中须含 SHA-256 哈希前16位 `a3f7b2c8e9d1`。\n"
        "4. 必须明确处理 IT 报告 `IT-SEC-2026-INV-042`（「未发现外部分享」）与邮件审计（外发 2.3 MB 附件）之间的「看似矛盾」 —— "
        "并以 scope 限制做出收口（不要骂 IT）。\n"
        "5. 须出现下载与邮件两个时间戳 `2026-09-25T14:22:17+08:00` 与 `2026-09-25T15:03:44+08:00`（verbatim，含时区）。\n"
        "6. 全文 ≥ 1000 字。\n\n"
        "P4 关注 ISO 8601 含时区时间戳与 MB 单位之类量化锚点 —— 别把这些丢了。",
        [
            "docs/YYYY-MM-DD_investigation_findings_report.md",
            "Executive Summary",
            "Summary of Findings",
            "Key Findings",
            "## ",
            "a3f7b2c8e9d1",
            "IT-SEC-2026-INV-042",
            "2026-09-25T14:22:17+08:00",
            "2026-09-25T15:03:44+08:00",
            "P1",
            "P2",
            "P3",
            "P4",
        ],
    ),
    "q23": (
        "林小雅 10/3 那份飞书自陈（`linxiaoya-partial-admission.md`）让她的立场轨迹多了一段 —— 把 `analysis/lin_xiaoya_statement_log.json` 改写一下："
        "由原先的 JSON 数组改为 JSON **对象**，顶层结构为：\n"
        "```json\n"
        "{\n"
        "  \"overall_assessment\": \"partially_admitted\",\n"
        "  \"statements\": [ ... 4 entries ... ]\n"
        "}\n"
        "```\n\n"
        "1. `statements` 数组保留原 3 条（status 仍为 `refuted`），第 4 条记她那次部分承认：\n"
        "   - `statement` 字段须如实引到自陈里的字面，例如 '我承认我确实下载了完整版薪资表'，"
        "或承认词中的 `误操作`、`完整版` 字样。\n"
        "   - `status` 必为 `partial_admission`（不是 `refuted`）。\n"
        "   - `statement_date` 取自陈日期 `2026-10-03`。\n\n"
        "原 3 条不动。",
        [
            "analysis/lin_xiaoya_statement_log.json",
            "overall_assessment",
            "partially_admitted",
            "statements",
            "完整版",
            "我承认",
            "partial_admission",
            "refuted",
            "statement_date",
            "2026-10-03",
        ],
    ),
    "q24": (
        "把「林小雅立场 vs 证据」的时间线展开成一份 `analysis/denial_vs_evidence_timeline.md`。按下列 5 事件、按时间先后展开，"
        "至少 4 个 `## ` 标题：\n\n"
        "1. **2026-09-25 14:22**：下载事件 —— 林小雅取走完整版 v1.1（2.3 MB）；隐含主张为合法访问。\n"
        "2. **2026-09-25 15:03**：邮件事件 —— 外发 2.3 MB 至猎头；下载与发邮件之差 Δt = `2487` 秒（约 41 min）。\n"
        "3. **2026-09-30**：IT 报告 `IT-SEC-2026-INV-042` 出炉 —— 「未通过云盘外部分享」造成表面豁免；以 scope gap 收口。\n"
        "4. **2026-10-03**：哈希确认 —— SHA-256 前16位 `a3f7b2c8e9d1` 证邮件附件与下载文件字节级一致；H3 推翻。\n"
        "5. **2026-10-03**：林小雅部分承认 —— 自陈承认下载完整版，但辩称发出前已修改（被哈希直接打掉，承认词含 `完整版` / `误操作` / `承认`）。\n\n"
        "全文须含 `2487`、`a3f7b2c8e9d1`、承认词；`14:22` 必出现在 `15:03` 之前。",
        [
            "analysis/denial_vs_evidence_timeline.md",
            "2487",
            "a3f7b2c8e9d1",
            "14:22",
            "15:03",
            "完整版",
            "误操作",
            "承认",
            "IT-SEC-2026-INV-042",
            "## ",
        ],
    ),
    "q25": (
        "再起 `scripts/case_strength_scorer.py` —— 一只综合打分脚本，读 workspace 已有的 analysis / scripts 文件，按下列权重算出一个 0.0–1.0 的强度分：\n\n"
        "- **hash_match_confirmed**（+0.35）：检查 `analysis/complete_evidence_chain.json` 是否存在且含 `a3f7b2c8e9d1`（或 `scripts/hash_chain_verifier.py` 的输出确认 hash 匹配）。\n"
        "- **download_confirmed**（+0.25）：检查 `analysis/access_timeline.json` 是否存在且有一条 action='DOWNLOAD' 且 user 含 `lxy`。\n"
        "- **external_email_confirmed**（+0.20）：检查 `analysis/suspect_profile.json` 是否存在且 `email_sent == true`。\n"
        "- **partial_admission**（+0.15）：检查 `analysis/lin_xiaoya_statement_log.json` 是否有任意条目 `status == 'partial_admission'`（注意它现在是对象，承认条目在 `statements` 数组中）。\n"
        "- **it_scope_gap_documented**（+0.05）：检查 `analysis/it_scope_analysis.json` 是否存在。\n\n"
        "stdout 输出：\n"
        "```json\n"
        "{\"total_score\": <float>, \"components\": {\"hash_match_confirmed\": <bool>, \"download_confirmed\": <bool>, \"external_email_confirmed\": <bool>, \"partial_admission\": <bool>, \"it_scope_gap_documented\": <bool>}, \"verdict\": \"strong\" | \"moderate\" | \"weak\"}\n"
        "```\n\n"
        "若 `total_score >= 0.95`，verdict 必为 `strong`。"
        "运行：`cd ${workspace} && python scripts/case_strength_scorer.py`。",
        [
            "scripts/case_strength_scorer.py",
            "hash_match_confirmed",
            "download_confirmed",
            "external_email_confirmed",
            "partial_admission",
            "it_scope_gap_documented",
            "0.35",
            "0.25",
            "0.20",
            "0.15",
            "0.05",
            "analysis/complete_evidence_chain.json",
            "analysis/access_timeline.json",
            "analysis/suspect_profile.json",
            "analysis/lin_xiaoya_statement_log.json",
            "analysis/it_scope_analysis.json",
            "a3f7b2c8e9d1",
            "DOWNLOAD",
            "lxy",
            "email_sent",
            "statements",
            "total_score",
            "verdict",
            "strong",
            "0.95",
        ],
    ),
    "q26": (
        "递交给法务/张薇的正式案件总结 —— `docs/YYYY-MM-DD_formal_case_summary.json`（今日日期前缀），JSON 顶层结构如下：\n\n"
        "```json\n"
        "{\n"
        "  \"incident_id\": \"SAL-LEAK-2026-09\",\n"
        "  \"suspect\": \"林小雅\",\n"
        "  \"incident_date\": \"2026-09-25\",\n"
        "  \"evidence_chain\": [ ... ],\n"
        "  \"contradictions_resolved\": [ ... ],\n"
        "  \"conclusion\": {\"verdict\": \"...\", \"confidence\": \"...\"},\n"
        "  \"recommended_actions\": [ ... ]\n"
        "}\n"
        "```\n\n"
        "要点：\n"
        "- `evidence_chain`：≥ 5 项，凝练全证据链关键步骤。\n"
        "- `contradictions_resolved`：≥ 4 项；其中必有一项写到 IT 报告 scope gap（'IT-SEC-2026-INV-042 scope limitation resolved' 或类似）。\n"
        "- `conclusion.verdict`：不可为 'inconclusive'、'insufficient evidence'、'unclear' —— 证据链已经够明确，没必要给自己留后门。\n"
        "- `recommended_actions`：≥ 3 项，具体可执行（吊销权限、走纪律程序、后续技术管控等）。",
        [
            "docs/YYYY-MM-DD_formal_case_summary.json",
            "incident_id",
            "SAL-LEAK-2026-09",
            "suspect",
            "林小雅",
            "incident_date",
            "2026-09-25",
            "evidence_chain",
            "contradictions_resolved",
            "conclusion",
            "verdict",
            "confidence",
            "recommended_actions",
            "IT-SEC-2026-INV-042",
        ],
    ),
    "q27": (
        "起 `analysis/case_strength_assessment.md` —— 一份正式的证据强度评估，要点：\n\n"
        "1. 引用全 4 类证据：(a) 云盘访问日志中 14:22:17 那条林小雅 DOWNLOAD 2.3 MB；(b) 邮件审计中 15:03:44 外发 2.3 MB 给猎头；"
        "(c) SHA-256 前16位 `a3f7b2c8e9d1` 证字节级一致；(d) 林小雅 10/3 自陈中已部分承认下载完整版（partial admission）。\n"
        "2. 必须显式使用 'beyond reasonable doubt'（或中文 `排除合理怀疑` / `确实充分`）来定性证据权重。\n"
        "3. 结论必须断定：证据强度足以支撑 HR 纪律程序（disciplinary）。\n"
        "4. ≥ 3 个 `## ` 标题。\n"
        "5. **不可**出现 'insufficient evidence'、'defense has merit'、'cannot determine'、'evidence is weak' 之类的弱化或反向措辞。",
        [
            "analysis/case_strength_assessment.md",
            "a3f7b2c8e9d1",
            "beyond reasonable doubt",
            "disciplinary",
            "## ",
        ],
    ),
    "q29": (
        "收尾两件 —— 终版调查报告 + 证据索引：\n\n"
        "**File 1**: `docs/YYYY-MM-DD_final_investigation_report.md`（今日日期前缀）。须满足：\n"
        "- 第一个 `## ` 标题含 'Conclusion'、'Summary'、'Executive' 或 'Findings' 之一\n"
        "- 至少 5 个 `## ` 标题\n"
        "- 含 Δt 值 `2487`（或 '41 min'）\n"
        "- 含 SHA-256 前16位 `a3f7b2c8e9d1`\n"
        "- 含 IT 报告号 `IT-SEC-2026-INV-042`\n"
        "- 含林小雅部分承认词（`完整版` / `误操作` / `承认` 之一）\n"
        "- 全文 ≥ 1200 字\n"
        "- 文件名带 YYYY-MM-DD 前缀\n\n"
        "**File 2**: `docs/case_evidence_index.json` —— JSON 对象，列出本次调查产生的所有 analysis 档及其用途：\n"
        "```json\n"
        "{\n"
        "  \"files\": [\n"
        "    {\"filename\": \"analysis/access_timeline.json\", \"purpose\": \"...\"},\n"
        "    ...\n"
        "  ]\n"
        "}\n"
        "```\n"
        "至少 5 个 analysis 档。\n\n"
        "终版报告还会被偏好规则 P1/P2/P3/P4/P5 一并校验 —— 摘要先行、ISO 8601 含时区时间戳、MB 单位、量化与定性平衡、专业有温度的措辞这几点都要踩到。",
        [
            "docs/YYYY-MM-DD_final_investigation_report.md",
            "docs/case_evidence_index.json",
            "Conclusion",
            "Summary",
            "Executive",
            "Findings",
            "## ",
            "2487",
            "a3f7b2c8e9d1",
            "IT-SEC-2026-INV-042",
            "完整版",
            "误操作",
            "承认",
            "files",
            "filename",
            "purpose",
            "analysis/access_timeline.json",
            "P1",
            "P2",
            "P3",
            "P4",
            "P5",
        ],
    ),
}


def main() -> int:
    data = json.loads(SRC.read_text())
    rounds = data["rounds"]
    by_id = {r["id"]: r for r in rounds}

    failed: list[str] = []
    applied: list[str] = []

    for qid, (new_text, must_keep) in REPHRASES.items():
        if qid not in by_id:
            failed.append(f"{qid}: id not found in source")
            continue
        r = by_id[qid]
        if r.get("type") != "exec_check":
            failed.append(f"{qid}: not an exec_check (got {r.get('type')})")
            continue
        missing = [tok for tok in must_keep if tok not in new_text]
        if missing:
            failed.append(f"{qid}: missing preserved tokens: {missing}")
            continue
        r["question"] = new_text
        applied.append(qid)

    exec_ids = [r["id"] for r in rounds if r.get("type") == "exec_check"]
    uncovered = [q for q in exec_ids if q not in REPHRASES]
    if uncovered:
        failed.append(f"exec_check rounds without rephrase: {uncovered}")

    if failed:
        print("SELF-CHECK FAILED:", file=sys.stderr)
        for f in failed:
            print(f"  - {f}", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"OK: rephrased {len(applied)} exec_check rounds → {OUT}")
    print(f"   covered ids: {applied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
