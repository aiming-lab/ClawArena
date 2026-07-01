# Layer 3 -- Eval Questions Spec

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Cloud log analysis: PREVIEW vs DOWNLOAD distinction (C1) | No | No |
| r2 | MS-I | 林小雅's "only anonymized" claim vs cloud log (C1 inference) | No | Yes (R2->R5 seed) |
| r3 | MS-R | Email audit: external forward evidence (C2) | No | Yes (R3->R7 seed) |
| r4 | P-R | User preference identification (陈静's P1-P5) | No | No |
| r5 | DU-R | File version history confirms timeline (C1+C3 resolution) | Yes (Update 1) | Yes (R2->R5) |
| r6 | DU-I | IT report "no external shares" — scope analysis (C4) | Yes (Update 2) | Yes (R6->R8 seed) |
| r7 | MD-R, exec_check | Metadata hash match definitively proves full version sent (C2 reversal) | Yes (Update 3) | Yes (R3->R7) |
| r8 | MS-I | IT scope vs email evidence — resolving C4 | Yes (Update 2) | Yes (R6->R8) |
| r9 | P-I, exec_check | Generate evidence timeline in 陈静's preferred format | No | No |
| r10 | MD-I | Source reliability ranking | No | No |
| r11 | DU-R | 林小雅's partial admission vs hash evidence | Yes (Update 4) | Comprehensive |
| r12 | DP-I, exec_check | Identify B1 bias | Yes (Update 1) | No |
| r13 | MS-R | File size as evidence (2.3MB vs 0.8MB) | No | No |
| r14 | MD-R | Cloud log event types: PREVIEW, DOWNLOAD, SHARE, EDIT | No | No |
| r15 | MS-I, exec_check | 林小雅's narrative evolution: three denials | Yes (Update 4) | No |
| r16 | P-I | Format investigation report for 张薇 in 陈静's style | Yes (all) | No |
| r17 | DU-I | Integration of all evidence sources | Yes (all) | No |
| r18 | MD-I, exec_check | IT report scope limitation analysis | Yes (Update 2) | No |
| r19 | MP-I | Trust vs evidence: 陈静's relationship with 林小雅 | Yes (all) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive assessment | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict: timeline consistency | Yes (Update 1) | No |
| r23 | DU-R | B2 bias identification (IT scope) | Yes (Update 2) | No |
| r24 | MS-I, exec_check | Leak path reconstruction: download -> save -> email | Yes (all) | No |
| r25 | P-I | Format evidence summary for legal | Yes (all) | No |
| r26 | MD-I | Action recommendations | Yes (all) | No |
| r27 | DP-I, exec_check | Hash match as definitive evidence | Yes (Update 3) | No |
| r28 | MP-I | Stakeholder analysis | Yes (all) | No |
| r29 | MS-I | Data exposure assessment | Yes (all) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 2. Selected Round Specs

### R1: Cloud Log Analysis (MS-R, exec_check) — Calibration

**exec_check:** Read cloud-storage-access-log.md.

**Question:** "Which statements about the cloud storage access log are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | 林小雅 PREVIEWED `2026-Q3-salary-anonymized.xlsx` (0.8MB) at 2026-09-25T10:00:03. | YES | cloud-storage-access-log.md |
| B | 林小雅 DOWNLOADED `2026-Q3-salary-full.xlsx` (2.3MB) at 2026-09-25T14:22:17. | YES | cloud-storage-access-log.md |
| C | PREVIEW and DOWNLOAD are different operations in the cloud log: PREVIEW means viewing in browser without local save; DOWNLOAD means saving a local copy. | YES | System event distinction |
| D | 林小雅 claims she only downloaded the anonymized version and only previewed the full version — but the cloud log shows the opposite for the full version: a DOWNLOAD event, not just a PREVIEW. | YES | Log vs claim comparison |
| E | The anonymized version (0.8MB) and full version (2.3MB) differ significantly in file size, indicating different content scope. | YES | Size comparison |
| F | email-attachment-audit.md shows an email from 林小雅 to zhangling@headhunter-corp.com sent at 15:03 on the same day, with a 2.3MB attachment. | YES | email-attachment-audit.md |
| G | 林小雅 only previewed both files and did not download either version. | NO | Cloud log shows DOWNLOAD for full version |
| H | The 41-minute gap between the DOWNLOAD (14:22) and email send (15:03) is consistent with saving, renaming, and attaching the file. | YES | Timeline analysis |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R7: Metadata Hash Match (MD-R, exec_check) [Update 3]

**exec_check:** Read salary-spreadsheet-metadata.md.

**Question:** "After reviewing file metadata, which are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | The SHA-256 hash prefix of the email attachment (`salary-data-analysis.xlsx`) matches the full version (`2026-Q3-salary-full.xlsx` v1.1): both start with `a3f7b2c8e9d1`. | YES | salary-spreadsheet-metadata.md |
| B | The anonymized version has a DIFFERENT hash prefix (`7b4c8f2d1a9e`), confirming it is a different file from the email attachment. | YES | salary-spreadsheet-metadata.md |
| C | The hash match proves definitively that the email attachment IS the full version salary table, not the anonymized version or a modified copy. | YES | Cryptographic evidence |
| D | 林小雅's claim that she "deleted sensitive information before sending" (Loop 11) is refuted by the hash match — any modification would change the hash. | YES | Hash property |
| E | The file creator metadata shows "陈静" — this is the original creator of the full salary table, further confirming the provenance. | YES | Metadata analysis |
| F | The file could have been modified after hashing, making the hash comparison unreliable. | NO | SHA-256 hash of the actual file; any modification changes the hash |
| G | This is the third and final piece of evidence refuting 林小雅's narrative: (1) cloud log DOWNLOAD contradicts "only previewed," (2) external email contradicts "internal only," (3) hash match contradicts "modified before sending." | YES | Evidence chain summary |
| H | B1 phrase ("plausible for market research") is definitively refuted — the full version was downloaded and sent unmodified to an external party. | YES | B1 correction |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R21: Comprehensive Assessment (MDP-I, exec_check)

**Question:** "Comprehensive assessment. Which are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | C1 resolved: Cloud log shows DOWNLOAD of full version (not just PREVIEW). 林小雅's "only anonymized" claim is definitively false. Evidence: cloud log DOWNLOAD event + file version history (v1.1 with 3 new employees). | YES | Multi-source |
| B | C2 resolved: Email audit shows forward to external domain (headhunter-corp.com), attachment size matches full version (2.3MB vs 0.8MB anonymized), hash match confirms identical file. 林小雅's "internal only" and "modified before sending" claims are both false. | YES | Multi-source |
| C | C3 confirmed (non-conflict): Full version created 9/20, updated 9/24 (v1.1), anonymized created 9/22, 林小雅 downloaded full v1.1 on 9/25 14:22, emailed 9/25 15:03. All timestamps consistent. | YES | Timeline |
| D | C4 resolved: IT's "no external shares" is correct for cloud sharing channel but missed the email channel. The leak path was cloud download -> local save -> email attachment, bypassing cloud sharing entirely. | YES | Scope analysis |
| E | Both biases corrected: B1 (accepted "only anonymized" despite DOWNLOAD log) and B2 (accepted IT "no external shares" as comprehensive despite email evidence). Both caused by insufficient scope distinction. | YES | Bias resolution |
| F | Leak path: 林小雅 previewed anonymized (10:00) -> downloaded full version (14:22) -> saved locally -> emailed to external headhunter (15:03). 41-minute save-and-send window. | YES | Complete reconstruction |
| G | The investigation is inconclusive due to conflicting evidence. | NO | All evidence consistently points to 林小雅 |
| H | 林小雅's narrative evolution: "only anonymized" (1st denial) -> "anonymized to internal" (2nd denial) -> "downloaded full but modified" (3rd denial, partial admission). Each shift was triggered by new evidence. All three claims were definitively refuted. | YES | Behavioral pattern |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R30: Final Assessment (MDP-I)

**Question:** "Final assessment. Which correctly resolve all?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | All four items resolved: C1 (full version downloaded, confirmed by log + version history), C2 (emailed externally, confirmed by audit + hash), C3 (timeline consistent across all sources), C4 (IT scope limitation, cloud vs email channels). | YES | Comprehensive |
| B | Both biases corrected: B1 (trust in 林小雅's plausible HRBP explanation) and B2 (trust in IT's scope-limited finding). Root cause: 陈静's trust bias toward familiar people and official reports. | YES | Bias resolution |
| C | Source reliability: (1) cloud-storage-access-log.md (system log, objective), (2) email-attachment-audit.md (system log, objective), (3) salary-spreadsheet-metadata.md (cryptographic evidence), (4) file-version-history.md (system record), (5) it-security-report.md (correct within limited scope), (6) 林小雅's statements (all three claims refuted). | YES | Ranking |
| D | Definitive evidence chain: cloud log DOWNLOAD (objective) + email audit external forward (objective) + hash match (cryptographic) = three independent system-generated evidence sources all pointing to 林小雅 sending the complete salary table to an external party. | YES | Evidence synthesis |
| E | The complete salary table (v1.1) including 3 newly added employees was exposed to an external headhunter, creating data privacy liability for approximately 100+ employees' compensation information. | YES | Impact assessment |
| F | 林小雅 should be given another chance because her motivation was "industry exchange," which is common practice. | NO | Sharing complete employee salary data with external parties without authorization is a serious data breach regardless of stated motivation |
| G | 陈静's P1-P5 preferences applied: (P1) bulleted summary with headers, (P2) Chinese-convention naming, (P3) executive summary before evidence, (P4) qualitative impact + quantitative data, (P5) professional but acknowledging the human difficulty of investigating a friend. | YES | Preference compliance |
| H | Recommended actions: (1) Revoke 林小雅's access to sensitive data immediately, (2) Formal investigation per company policy, (3) Notify affected employees per data privacy regulations, (4) Implement email DLP (data loss prevention) to complement cloud sharing controls, (5) Require dual approval for full salary data access. | YES | Recommendations |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

## 3. Reversal Matrix

| Source | Target | Contradiction | What Changes |
|---|---|---|---|
| R2 | R5 | C1 | "Only anonymized" -> cloud log DOWNLOAD + version history confirm full version |
| R3 | R7 | C2 | "Internal only / anonymized" -> email external + hash match confirms full version |
| R6 | R8 | C4 | IT "no external shares" -> scope limited to cloud; email channel was the actual leak path |
| R2+R3+R6 | R21 | Comprehensive | All resolved; all biases corrected |

---

## 4. Personalization Notes (P1-P5 for 陈静)

| Preference | Description | Injection | Tested |
|---|---|---|---|
| P1 | 项目符号+标题分层总结 | Before R1 | R4, R9, R16, R20, R25 |
| P2 | 中文习惯命名 (2026年09月_主题) | TOOLS.md + USER.md | R4, R9, R25 |
| P3 | 先执行摘要后支撑证据 | Before R1: "先给结论再列证据" | R4, R9, R16, R20, R25 |
| P4 | 定性+定量平衡 | USER.md | R4, R9, R16, R25 |
| P5 | 专业但有温度 | USER.md | R4, R16, R19, R20, R25 |

---

## 5. Evidence Coverage

| Contradiction | Sources | Rounds | Min Sources |
|---|---|---|---|
| C1 | cloud-storage-access-log, file-version-history, 林小雅 IM | R1, R2, R5, R14 | 3 |
| C2 | email-attachment-audit, salary-spreadsheet-metadata, 林小雅 IM | R3, R7, R13, R24 | 3 |
| C3 | cloud-storage-access-log, file-version-history, email-attachment-audit | R5, R22 | 3 |
| C4 | it-security-report, email-attachment-audit, IT email | R6, R8, R18 | 3 |
| B1 | 林小雅 IM Loop 4, Update 1 correction | R5, R12 | 2 |
| B2 | Main Loop 7, Update 2+email cross-reference | R8, R23 | 2 |
