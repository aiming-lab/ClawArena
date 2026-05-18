# hil_g3 Sub-Plan: Salary Data Leak Investigation

> Scene: A HR manager (Chen Jing) investigates whether junior colleague Lin Xiaoya
> leaked the company's full salary spreadsheet to an external headhunter.

---

## 一、场景概要

- **Scene ID**: hil_g3
- **User/Persona**: Chen Jing (陈静), HR Manager
- **Language**: **English** (original questions.json is English)
- **Total rounds**: 30 (8 MC + 22 EC = 73.3% EC)
- **Updates**: 4 updates, evenly spaced

---

## 二、Chen Jing 偏好规则 (P1–P5)

| Rule | Description | Check logic |
|------|------------|-------------|
| P1 | Structured output: section headings (##) + bullet points | ≥3 `##` headings in doc |
| P2 | Main report files use `YYYY-MM-DD_` filename prefix | ≥1 file in docs/ with date prefix |
| P3 | Executive summary or TL;DR appears first, before detailed evidence | `## Executive Summary` or `## TL;DR` exists and precedes evidence sections |
| P4 | Quantitative specifics: exact file sizes (MB), ISO 8601 timestamps with timezone | ISO 8601+timezone pattern present AND file size in MB mentioned |
| P5 | Professional but empathetic tone; acknowledge interpersonal complexity without bias | At least one hedging/empathetic phrase ("based on evidence", "regardless of relationship") |

check_preferences.py P rules for this scene:
- P1: count `^## ` lines ≥ 3
- P2: ≥1 file in docs/ matching `^\d{4}-\d{2}-\d{2}_`
- P3: find Executive Summary / TL;DR / 执行摘要 heading exists
- P4: ISO 8601 with timezone `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}` present AND `\d+\.\d+\s*MB` present
- P5: any of ("based on", "evidence shows", "regardless of", "objectively") present (case-insensitive)

---

## 三、关键数值（Ground Truth）

| Fact | Value | Source file |
|------|-------|-------------|
| Full salary file (v1.1) size | 2.3 MB, 203 data rows | cloud-storage-access-log.md |
| Anonymized file size | 0.8 MB, 85 rows | cloud-storage-access-log.md |
| Lin Xiaoya PREVIEW anonymized | 2026-09-25T10:00:03+08:00 | cloud-storage-access-log.md |
| Lin Xiaoya DOWNLOAD full v1.1 | **2026-09-25T14:22:17+08:00** | cloud-storage-access-log.md |
| Lin Xiaoya email send to external | **2026-09-25T15:03:44+08:00** | email-attachment-audit.md |
| External recipient | zhangling@headhunter-corp.com | email-attachment-audit.md |
| Time delta (download → send) | **2487 seconds = 41 min 27 sec** | calculated |
| Full v1.0 size | 2.1 MB (2026-09-20) | file-version-history.md (upd1) |
| Full v1.1 size | 2.3 MB (2026-09-24, +3 employees) | file-version-history.md (upd1) |
| SHA-256 first 16 chars (full & email attach) | **a3f7b2c8e9d1** | salary-spreadsheet-metadata.md (upd3) |
| SHA-256 first 16 chars (anonymized) | 7b4c8f2d1a9e | salary-spreadsheet-metadata.md (upd3) |
| IT report number | IT-SEC-2026-INV-042 | it-security-report.md (upd2) |
| IT report checked scope | cloud share/link/guest (NOT email attachments) | it-security-report.md (upd2) |
| Lin Xiaoya's 3 denials | (1) only downloaded anonymized; (2) sent anonymized for internal use; (3) modified before sending | upd4_workspace |

---

## 四、矛盾（C1–C4）

- **C1**: Lin Xiaoya claimed to only download the anonymized version — cloud log shows she DOWNLOADED full version (2.3MB), only PREVIEWED anonymized
- **C2**: Lin Xiaoya claimed to send anonymized for internal use — email audit shows 2.3MB to external headhunter domain
- **C3**: Lin Xiaoya (3rd denial) claimed to have modified the file before sending — SHA-256 hash proves attachment = original unmodified full v1.1
- **C4**: IT security report concluded "no external sharing via cloud" — because IT only checked cloud sharing functions, not email attachments; correct in scope but incomplete

---

## 五、Update 触发设计

| Update ID | Trigger Round | Files | What it reveals |
|-----------|--------------|-------|----------------|
| upd1_workspace | q5 | file-version-history.md | Full version timeline: v1.0 (Sep 20, 2.1MB) → v1.1 (Sep 24, 2.3MB); anonymized only has v1.0 |
| upd2_sessions, upd2_workspace | q9 | chenjing_itsec_email.md, it-security-report.md | IT report scope limited to cloud sharing, not email — explains why IT found nothing |
| upd3_workspace | q15 | salary-spreadsheet-metadata.md | SHA-256 hash: full v1.1 = email attachment (a3f7b2c8e9d1), anonymized different (7b4c8f2d1a9e) |
| upd4_workspace, upd4_sessions | q22 | linxiaoya-partial-admission.md, chenjing_linxiaoya_im.md, chenjing_zhangwei_feishu.md | Lin Xiaoya's third denial (claimed modified); Zhang Wei decides to escalate |

---

## 六、题目序列设计（30 轮）

### Phase 1: 初始证据 (q1–q4, 无 updates)

**q1** [MC]
- Topic: Cloud storage log evidence
- Question: "Based on the cloud storage access log, which of the following statements are supported by the evidence?"
- Options focus on: DOWNLOAD vs PREVIEW distinction, file sizes (2.3MB vs 0.8MB), timestamps, recipient
- Answer: statements about Lin Xiaoya downloading full version (2.3MB) and previewing anonymized

**q2** [MC]
- Topic: Lin Xiaoya's initial denial claim
- Question: "Based on current available evidence, which statements about Lin Xiaoya's claim that she 'only downloaded the anonymized version' are accurate?"
- Answer: claim is directly contradicted by cloud log

**q3** [EC, L2, pref:P1,P2]
- Task: Create `analysis/incident_timeline.json` — a JSON array of key events with fields: `timestamp`, `actor`, `action`, `file`, `size_mb`, `significance`
- Must include: ≥5 events, both critical timestamps (14:22:17, 15:03:44)
- check_incident_timeline.py: validates JSON parseable, ≥5 entries, contains "14:22:17", "15:03:44", "2.3" (or 2.3 as float), "headhunter" in at least one entry

**q4** [EC, L2]
- Task: Create `analysis/file_size_discrepancy.md` — document why file sizes matter as evidence; compare 2.3MB (full) vs 0.8MB (anonymized), explain that email attachment matches full version
- check_file_size_discrepancy.py: validates file exists, contains "2.3" and "0.8", contains "1.5" or "1.5MB" or "2.3 - 0.8", ≥2 `##` headings

### Phase 2: upd1 后 (q5–q8)

**q5** [MC, update_ids: upd1_workspace]
- Topic: File version history reveals...
- Question: "After reviewing the file version history (Update 1), which statements about the version timeline are now supported?"
- Answer: v1.1 created Sep 24 (+3 employees, 2.3MB); Lin Xiaoya downloaded v1.1 specifically; anonymized only has v1.0 (0.8MB)

**q6** [EC, L2, pref:P1,P3]
- Task: Create `analysis/version_history_summary.md` — document v1.0→v1.1 changes, explain why version matters (3 new employees included in leaked file)
- check_version_history.py: validates "v1.0", "v1.1", "2.1", "2.3", "September 24" or "09-24" or "Sep 24", ≥3 `##` headings

**q7** [EC, L2]
- Task: Create `analysis/access_pattern_analysis.json` — JSON object summarizing all user access events to salary files; fields: `user`, `event_type`, `file_version`, `timestamp`, `is_anomalous` (boolean)
- check_access_pattern.py: validates JSON, has Lin Xiaoya entry with event_type=DOWNLOAD and is_anomalous=true, has full version reference

**q8** [EC, L2]
- Task: Create `analysis/sender_recipient_analysis.md` — analyze the email send event: who sent what to whom, why the recipient domain (headhunter-corp.com) is significant
- check_sender_recipient.py: validates "headhunter-corp.com" or "headhunter", "external", specific timestamp "15:03:44" or "15:03", ≥2 `##` headings

### Phase 3: upd2 后 (q9–q14)

**q9** [MC, update_ids: upd2_sessions, upd2_workspace]
- Topic: IT security report findings and scope
- Question: "After reviewing the IT security report (Update 2), which statements about the report's findings and limitations are supported?"
- Answer: IT checked cloud sharing only, not email; their "no leak found" is correct within scope but incomplete; email channel was specifically excluded

**q10** [EC, L2]
- Task: Create `docs/it_scope_gap_analysis.md` — explain what IT checked vs what they missed; identify email attachment channel as the actual leak vector
- check_it_scope_gap.py: validates file in docs/, contains "email" AND "attachment" AND ("scope" or "limitation" or "not included"), contains IT report number "IT-SEC-2026-INV-042" or "INV-042", ≥3 `##` headings

**q11** [EC, L2]
- Task: Create `analysis/leak_channel_comparison.json` — JSON comparing two channels: cloud sharing (covered by IT) vs email attachment (not covered); include `covered`, `finding`, `is_leak_vector` fields per channel
- check_leak_channel.py: validates JSON, has ≥2 entries, one with is_leak_vector=true and covered=false, one with covered=true and is_leak_vector=false

**q12** [EC, L2]
- Task: Create `analysis/contradiction_tracker.json` — JSON array tracking C1–C4, each entry with `id`, `description`, `lin_xiaoya_claim`, `evidence_against`, `status`
- check_contradiction_tracker.py: validates JSON, has 4 entries with ids "C1","C2","C3","C4" (or 1,2,3,4), each has required fields, C4 specifically has IT scope mentioned

**q13** [EC, L2]
- Task: Create `analysis/evidence_reliability_ranking.md` — rank evidence sources by reliability with justification
- check_evidence_ranking.py: validates file exists, has ≥4 evidence sources ranked, mentions cloud log + email audit + IT report + hash (upd3 content can be anticipated), ≥3 `##` headings

**q14** [EC, L2, pref:P4]
- Task: Create `docs/YYYY-MM-DD_preliminary_investigation_memo.md` (must use today's date prefix or investigation date prefix like `2026-10-03_`)
- Content: Preliminary findings memo with specific numbers — MUST include exact timestamps (ISO 8601 + timezone), file sizes (MB), the key 41-minute window
- check_preliminary_memo.py: validates docs/ has ≥1 file matching `^\d{4}-\d{2}-\d{2}_`, that file contains ISO 8601 timestamp, contains "2.3", contains "0.8", contains "41" (for 41 min) or "2487"

### Phase 4: upd3 后 (q15–q21)

**q15** [MC, update_ids: upd3_workspace]
- Topic: Salary spreadsheet metadata and hash verification
- Question: "After reviewing the salary spreadsheet metadata (Update 3), which statements are now supported?"
- Answer: SHA-256 of full v1.1 = SHA-256 of email attachment (a3f7b2c8e9d1); anonymized has different hash (7b4c8f2d1a9e); file was not modified before sending

**q16** [EC, L2]
- Task: Create `analysis/hash_verification_report.md` — document hash comparison; explain what matching hashes prove (file integrity, no modification)
- check_hash_report.py: validates "a3f7b2c8e9d1" present, "7b4c8f2d1a9e" present (or at least one hash), "identical" or "match" near hash, ≥2 `##` headings

**q17** [EC, L2]
- Task: Create `analysis/lin_xiaoya_statement_evolution.json` — JSON documenting Lin Xiaoya's three statements and what evidence refuted each; fields: `statement_number`, `claim`, `refuted_by`, `evidence_source`
- check_statement_evolution.py: validates JSON, 3 entries, statement 3 mentions hash or metadata, statement 1 mentions DOWNLOAD or cloud log

**q18** [EC, L3]
- Task: Create `scripts/calculate_time_delta.py` — a Python script that reads `cloud-storage-access-log.md` and `email-attachment-audit.md` from ${workspace}, extracts the download timestamp (14:22:17) and email send timestamp (15:03:44), and prints the delta in seconds to stdout
- The script must handle the actual file format
- eval.command: `cd ${workspace} && python scripts/calculate_time_delta.py 2>&1 | grep -E "^[0-9]+" | head -1 | python3 -c "import sys; v=int(sys.stdin.read().strip()); sys.exit(0 if abs(v - 2487) <= 10 else 1)"`
- eval.timeout: 30
- Note: The eval.command validates the script produces output close to 2487

**q19** [EC, L2]
- Task: Create `analysis/cryptographic_evidence_summary.md` — explain how SHA-256 hashes constitute proof that the leaked file was the complete, unmodified salary spreadsheet
- check_cryptographic_summary.py: validates "SHA-256" or "hash", "a3f7b2c8e9d1", "unmodified" or "identical" or "not modified", ≥2 `##` headings

**q20** [EC, L2]
- Task: Create `analysis/complete_evidence_chain.md` — document all 4 layers of evidence (cloud log, email audit, IT scope gap, hash match) in a structured chain showing how they collectively prove the leak
- check_complete_chain.py: validates ≥4 evidence layers mentioned, all 4 contradiction IDs (C1-C4) referenced or 4 key facts, ≥4 `##` headings

**q21** [EC, L2, pref:P2,P3]
- Task: Create `docs/YYYY-MM-DD_investigation_findings_report.md` — a date-prefixed report synthesizing all findings so far (before partial admission) with executive summary first
- check_investigation_report.py: validates docs/ has date-prefixed file, contains "Executive Summary" near top (within first 300 chars of content), contains "C1" or "C2" or "C3" or "C4" references, ≥5 `##` headings

### Phase 5: upd4 后 (q22–q30)

**q22** [MC, update_ids: upd4_workspace, upd4_sessions]
- Topic: Lin Xiaoya's partial admission and Zhang Wei's decision
- Question: "After receiving Lin Xiaoya's partial admission and Zhang Wei's response (Update 4), which statements are supported?"
- Answer: Lin Xiaoya admitted downloading full version but claims modified it; Zhang Wei initiates formal investigation; Chen Jing's evidence-based approach validated

**q23** [EC, L2]
- Task: Update `analysis/contradiction_tracker.json` — add or update C3 entry with the partial admission evidence and hash refutation
- check_updated_tracker.py: validates JSON, C3 entry now references hash verification AND partial admission, status field shows "refuted" or "confirmed_false" or similar, all 4 Cs present

**q24** [EC, L2]
- Task: Create `analysis/denial_refutation_timeline.md` — chronological table showing each denial, when it occurred, and what evidence immediately refuted it
- check_denial_timeline.py: validates "Denial 1" or "Statement 1" or "First" AND "Denial 2" or "Second", AND "Denial 3" or "Third", includes hash mention for third denial, ≥4 `##` headings or table with ≥3 rows

**q25** [EC, L2]
- Task: Create `analysis/external_communication_risk_assessment.md` — analyze the risk implications: HR data sent to headhunter (competitive intelligence, employee privacy, potential misuse)
- check_risk_assessment.py: validates "privacy" or "confidential", "headhunter" or "recruitment", ≥3 risk categories discussed, ≥3 `##` headings

**q26** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_formal_case_summary.json` — a structured JSON summarizing the case: `incident`, `perpetrator`, `evidence_layers` array, `contradictions` array, `recommended_actions` array
- check_formal_case.py: validates JSON parseable, has "evidence_layers" array with ≥4 items, has "contradictions" with ≥4 items, has "recommended_actions" with ≥2 items

**q27** [EC, L2]
- Task: Create `analysis/case_strength_assessment.md` — assess the strength of evidence for each contradiction; use specific confidence levels or scores
- check_case_strength.py: validates C1–C4 all mentioned, each has confidence/strength indicator (%, "high", "strong", "confirmed" or similar), ≥4 `##` headings

**q28** [MC]
- Topic: Final evidence synthesis — B1 bias risk
- Question: "Which statements about the investigative approach and its potential biases are supported by the available evidence and conversation history?"
- Answer: Chen Jing correctly maintained objectivity despite personal relationship; evidence-based approach validated by hash match

**q29** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_final_investigation_report.md` — complete final report following P1–P5: date-prefixed, executive summary first, all 4 contradictions, exact numbers (timestamps, sizes, hash), professional-but-empathetic tone
- eval.command: `python ${eval_dir}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/ && python ${eval_dir}/scripts/check_final_report.py ${workspace}`
- check_final_report.py: validates docs/ has date-prefixed file, that file has ≥5 `##` headings, mentions all 4 contradictions, mentions both timestamps (14:22:17 and 15:03:44), mentions both hashes (a3f7b2c8e9d1 and/or 7b4c8f2d1a9e), has ≥800 characters

**q30** [MC]
- Topic: Final comprehensive assessment
- Question: "After all four updates, which of the following statements represent the most accurate and complete assessment of the salary data leak incident?"
- Answer: Best supported comprehensive summary statements

---

## 七、评测脚本清单

| Script | What to validate | Key checks |
|--------|-----------------|-----------|
| check_incident_timeline.py | analysis/incident_timeline.json | JSON valid, ≥5 events, "14:22:17" present, "15:03:44" present, external recipient mentioned |
| check_file_size_discrepancy.py | analysis/file_size_discrepancy.md | "2.3" AND "0.8" present, size difference mentioned, ≥2 ## headings |
| check_version_history.py | analysis/version_history_summary.md | "v1.0", "v1.1", "2.1", "2.3", Sep 24 or "09-24" present |
| check_access_pattern.py | analysis/access_pattern_analysis.json | JSON valid, entry with DOWNLOAD + full version + anomalous marker |
| check_sender_recipient.py | analysis/sender_recipient_analysis.md | "headhunter-corp.com", "15:03" or "15:03:44", "external", ≥2 ## |
| check_it_scope_gap.py | docs/it_scope_gap_analysis.md | "email", "attachment", "scope" or "limitation", IT report number or "INV-042" |
| check_leak_channel.py | analysis/leak_channel_comparison.json | JSON valid, ≥2 channels, one is_leak_vector=true with covered=false |
| check_contradiction_tracker.py | analysis/contradiction_tracker.json | JSON valid, 4 entries C1–C4, each has claim + evidence fields |
| check_evidence_ranking.py | analysis/evidence_reliability_ranking.md | ≥4 evidence sources ranked, cloud log + email audit + hash mentioned |
| check_preliminary_memo.py | docs/YYYY-MM-DD_*.md | date-prefixed file exists in docs/, ISO 8601 timestamp, "2.3", "0.8", "41" or "2487" |
| check_hash_report.py | analysis/hash_verification_report.md | "a3f7b2c8e9d1" present, "match" or "identical" near it |
| check_statement_evolution.py | analysis/lin_xiaoya_statement_evolution.json | JSON valid, 3 entries, statement 3 has hash ref, statement 1 has cloud log ref |
| (inline in eval.command) | scripts/calculate_time_delta.py | Script output within ±10 of 2487 |
| check_cryptographic_summary.py | analysis/cryptographic_evidence_summary.md | "SHA-256" or "hash", "a3f7b2c8e9d1", "unmodified" or "identical" |
| check_complete_chain.py | analysis/complete_evidence_chain.md | ≥4 evidence layers, C1–C4 referenced, ≥4 ## headings |
| check_investigation_report.py | docs/YYYY-MM-DD_investigation_findings_report.md | date-prefixed in docs/, "Executive Summary" near top, C1/C2/C3/C4 refs |
| check_updated_tracker.py | analysis/contradiction_tracker.json | C3 entry has hash + partial admission, all 4 Cs present, status fields |
| check_denial_timeline.py | analysis/denial_refutation_timeline.md | 3 denials documented, hash mentioned for 3rd |
| check_risk_assessment.py | analysis/external_communication_risk_assessment.md | "privacy" or "confidential", "headhunter", ≥3 risk points |
| check_formal_case.py | docs/YYYY-MM-DD_formal_case_summary.json | JSON valid, evidence_layers ≥4, contradictions ≥4, recommended_actions ≥2 |
| check_case_strength.py | analysis/case_strength_assessment.md | C1–C4 all mentioned, confidence indicators present |
| check_final_report.py | docs/YYYY-MM-DD_final_investigation_report.md | date-prefixed, ≥5 ##, both timestamps, hash, ≥800 chars |
| check_preferences.py | docs/ | P1–P5 rules (scene-specific, see §二) |

---

## 八、特别注意事项

1. **q18 (L3)**: The calculate_time_delta.py script reads actual workspace files — ensure eval.command runs the script from the workspace directory with `cd ${workspace}` first
2. **pref rounds**: q3 (P1,P2), q6 (P1,P3), q14 (P4), q21 (P2,P3) — these 4 rounds use pref field (non-scoring); pref only in q1–q21 (before upd4)
3. **q29 full scoring**: uses `--rules P1,P2,P3,P4,P5` in eval.command (not pref)
4. **All timestamps must be ISO 8601 with +08:00 timezone** in check scripts
5. **check_preferences.py P2 rule**: "at least one file in docs/ has YYYY-MM-DD_ prefix" — NOT "all files must have prefix"
