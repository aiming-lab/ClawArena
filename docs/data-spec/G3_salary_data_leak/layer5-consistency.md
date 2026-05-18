# Layer 5 -- Cross-Layer Consistency Checks

> Validates internal consistency across all layers for trace_g3.

---

## 1. File and Data Consistency

| Figure | L0 | L1 (workspace) | L2 (sessions) | L3 (eval) | L4 (updates) | Status |
|---|---|---|---|---|---|---|
| Full version filename | 2026-Q3-salary-full.xlsx | cloud-storage-access-log.md | 林小雅 IM Loop 2 | R1 opt B | U1 version history | ✅ |
| Full version size | 2.3MB | cloud-storage-access-log.md (DOWNLOAD entry) | — | R1 opt E, R13 | U1, U3 | ✅ |
| Anonymized filename | 2026-Q3-salary-anonymized.xlsx | cloud-storage-access-log.md | 林小雅 IM Loop 2 | R1 opt A | U1 version history | ✅ |
| Anonymized size | 0.8MB | cloud-storage-access-log.md (PREVIEW entry) | — | R1 opt E, R13 | U1 | ✅ |
| Email attachment name | salary-data-analysis.xlsx | email-attachment-audit.md | — | R1 opt F | U3 metadata | ✅ |
| Email attachment size | 2.3MB | email-attachment-audit.md | — | R1 opt F, R13 | U3 metadata | ✅ |
| Full version hash prefix | a3f7b2c8e9d1... | salary-spreadsheet-metadata.md (U3) | — | R7 opt A | U3 | ✅ |
| Email attachment hash prefix | a3f7b2c8e9d1... (MATCH) | salary-spreadsheet-metadata.md (U3) | — | R7 opt A | U3 | ✅ |
| Anonymized hash prefix | 7b4c8f2d1a9e... (DIFFERENT) | salary-spreadsheet-metadata.md (U3) | — | R7 opt B | U3 | ✅ |
| 林小雅 email | lxy@company.com | cloud-storage-access-log, email-attachment-audit | — | R1 | — | ✅ |
| External recipient | zhangling@headhunter-corp.com | email-attachment-audit.md | 林小雅 IM Loop 5 | R1 opt F | — | ✅ |
| File creator (metadata) | 陈静 | salary-spreadsheet-metadata.md | — | R7 opt E | U3 | ✅ |

---

## 2. Timestamp Consistency

| Event | Date/Time | Cross-layer | Status |
|---|---|---|---|
| Full version v1.0 created | 2026-09-20T09:15:00 | L0, L1 file-version-history | ✅ |
| Anonymized version created | 2026-09-22T11:00:00 | L0, L1 file-version-history | ✅ |
| Full version v1.1 updated | 2026-09-24T16:30:00 | L0, L1 file-version-history | ✅ |
| 林小雅 PREVIEW anonymized | 2026-09-25T10:00:03 | L0, L1 cloud-storage-access-log | ✅ |
| 林小雅 DOWNLOAD full | 2026-09-25T14:22:17 | L0, L1 cloud-storage-access-log | ✅ |
| 林小雅 email to headhunter | 2026-09-25T15:03:44 | L0, L1 email-attachment-audit | ✅ |
| Gap: download to email | 41 minutes | L0 §2, L3 R1 opt H | ✅ |
| Anonymous report received | ~2026-09-28 (W1D1) | L0 §2 | ✅ |
| IT security report | 2026-09-30 | L0, L1 it-security-report | ✅ |

---

## 3. Contradiction Trace Matrix

| Contradiction | L0 | L1 sources | L2 sessions | L3 rounds | L4 updates |
|---|---|---|---|---|---|
| C1 (cloud "full downloaded" vs "only anonymized") | §4 C1 | cloud-storage-access-log, file-version-history | 林小雅 IM Loops 2-4 | R1, R2, R5, R14 | U1 (version history) |
| C2 (email external forward vs "internal only") | §4 C2 | email-attachment-audit, salary-spreadsheet-metadata | 林小雅 IM Loop 5 | R3, R7, R13, R24 | U3 (metadata hash) |
| C3 (file version timeline, NON-CONFLICT) | §4 C3 | cloud-storage-access-log, file-version-history, email-attachment-audit | — | R5, R22 | U1 |
| C4 (IT "no external shares" vs email metadata) | §4 C4 | it-security-report, email-attachment-audit | IT email Loops 7-8 | R6, R8, R18 | U2 (IT report + scope clarification) |

---

## 4. Bias Trace Matrix

| Bias | L0 | L2 location | L3 identification | L3 correction | L4 trigger |
|---|---|---|---|---|---|
| B1 ("only anonymized" plausible) | §5 B1 | 林小雅 IM Loop 4, assistant reply | R12 | R5 | U1 (version history) |
| B2 (IT "no external shares" comprehensive) | §5 B2 | Main session Loop 7, assistant reply | R23 | R8 | U2 (IT scope clarification) |

---

## 5. Preference Consistency (陈静's P1-P5)

| Pref | L0 §7.9 | L1 USER.md | L2 calibration | L3 test rounds |
|---|---|---|---|---|
| P1 (项目符号+标题分层) | ✅ | ✅ | "用项目符号总结" | R4, R9, R16, R20, R25 |
| P2 (中文习惯命名) | ✅ | ✅ | Implicit from profile | R4, R9, R25 |
| P3 (先执行摘要后证据) | ✅ | ✅ | "先给结论再列证据" | R4, R9, R16, R20, R25 |
| P4 (定性+定量平衡) | ✅ | ✅ | Implicit | R4, R9, R16, R25 |
| P5 (专业但有温度) | ✅ | ✅ | Implicit from profile | R4, R16, R19, R20, R25 |

Note: 陈静's preferences differ from 赵磊's — she prefers executive summary BEFORE evidence (P3), not evidence-first. Bullet points rather than JSON/tables. Professional but warm tone, not terse. This is consistent with her HR personality profile.

---

## 6. Update-Round Alignment

| Update | Trigger | Rounds affected | New workspace | New sessions | Status |
|---|---|---|---|---|---|
| U1 | Before R5 | R5, R22 | file-version-history.md | — | ✅ |
| U2 | Before R6 | R6, R8, R18, R23 | it-security-report.md | IT email Phase 2 | ✅ |
| U3 | Before R7 | R7, R27 | salary-spreadsheet-metadata.md | — | ✅ |
| U4 | Before R11 | R11, R15, R17 | linxiaoya-partial-admission.md | 林小雅 IM + 张薇 飞书 Phase 2 | ✅ |

---

## 7. 林小雅 Narrative Evolution Consistency

| Denial # | Claim | Session location | Refuted by | Refutation round |
|---|---|---|---|---|
| 1st | "Only downloaded anonymized version" | 林小雅 IM Loop 3 | cloud-storage-access-log.md: DOWNLOAD full 2.3MB | R5 |
| 2nd | "Sent anonymized to internal" | 林小雅 IM Loop 5 | email-attachment-audit.md: external domain + 2.3MB size | R7 |
| 3rd | "Downloaded full but modified before sending" | 林小雅 IM Loop 11 (Update 4) | salary-spreadsheet-metadata.md: hash match (unmodified) | R11 |

Each denial narrows the scope but maintains falsehood. Each is triggered by evidence pressure. The pattern is consistent across L0 (§3), L2 (session loops), and L3 (eval rounds).

---

## 8. Channel/Scope Distinction Consistency

| Investigation Channel | What it detects | What it misses | Who checks it | Consistent? |
|---|---|---|---|---|
| Cloud sharing (IT scope) | Share links, external shares, access permissions | Email attachments, IM forwards, USB copies | IT security | ✅ (L0, L1 IT report, L2 IT email Loop 8) |
| Email audit (陈静's scope) | Email attachments, recipients, sizes | Cloud shares, IM forwards, USB copies | 陈静 (as HR manager) | ✅ (L0, L1 email-attachment-audit) |
| Cloud access log | File PREVIEW, DOWNLOAD, EDIT, UPLOAD events | Post-download distribution | System automatic | ✅ (L0, L1 cloud-storage-access-log) |
| File metadata | Hash values, creator, modifier, size | Intent, authorization | 陈静 (via IT tools) | ✅ (L0, L1 salary-spreadsheet-metadata) |

The C4 contradiction arises precisely because IT checked only one channel (cloud sharing) while the actual leak used a different channel (email). This scope distinction is the key analytical insight.
