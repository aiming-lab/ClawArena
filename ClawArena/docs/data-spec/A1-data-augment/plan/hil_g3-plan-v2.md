# hil_g3 v2 Sub-plan: Salary Data Leak Investigation

**Scene**: 林小雅 (Lin Xiaoya), a junior HR analyst, is suspected of leaking confidential salary data to an external headhunter. 陈静 (Chen Jing), the senior HR manager, must investigate using digital evidence.

**Language convention**: Questions and task descriptions in English. Chinese proper nouns kept as-is (林小雅, 陈静, 张薇, 刘伟, zhangling@headhunter-corp.com). Chinese document content quoted verbatim.

**Total rounds**: 30 (8 MC + 22 EC)  
**Update schedule**: upd1@q5, upd2@q9, upd3@q15, upd4@q22

---

## Ground Truth Values

| Fact | Value | Source |
|------|-------|--------|
| 林小雅 DOWNLOAD timestamp | `2026-09-25T14:22:17+08:00` | cloud-storage-access-log.md |
| Downloaded file | `2026-Q3-salary-full.xlsx` | cloud-storage-access-log.md |
| Downloaded file size | **2.3 MB** | cloud-storage-access-log.md |
| Email send timestamp | `2026-09-25T15:03:44+08:00` | email-attachment-audit.md |
| Email recipient | `zhangling@headhunter-corp.com` | email-attachment-audit.md |
| Email attachment size | **2.3 MB** | email-attachment-audit.md |
| Time delta (download→email) | **2487 seconds** (41 min 27 s) | computed |
| Full v1.0 size | 2.1 MB (created 2026-09-20) | file-version-history.md (upd1) |
| Full v1.1 size | 2.3 MB (created 2026-09-24) | file-version-history.md (upd1) |
| Anonymized v1.0 size | 0.8 MB | cloud-storage-access-log.md |
| Size ratio (full/anon) | **2.875** (2.3 / 0.8) | computed |
| New employees in v1.1 | 李明, 赵伟, 孙丽 | file-version-history.md (upd1) |
| SHA-256 of full v1.1 | `a3f7b2c8e9d1` | salary-spreadsheet-metadata.md (upd3) |
| IT report number | `IT-SEC-2026-INV-042` | it-security-report.md (upd2) |
| IT report scope | cloud sharing only; email **not** checked | it-security-report.md (upd2) |
| 林小雅 partial admission | "…可能有些误操作" | linxiaoya-partial-admission.md (upd4) |

---

## Available Files by Phase

| Phase | New files available |
|-------|-------------------|
| init (q1–q4) | `cloud-storage-access-log.md`, `email-attachment-audit.md` |
| post-upd1 (q5–q8) | + `file-version-history.md` |
| post-upd2 (q9–q14) | + `it-security-report.md`, sessions: `chenjing_itsec_email.md` |
| post-upd3 (q15–q21) | + `salary-spreadsheet-metadata.md` |
| post-upd4 (q22–q29) | + `linxiaoya-partial-admission.md`, sessions: `chenjing_linxiaoya_im.md`, `chenjing_zhangwei_feishu.md` |

---

## Preference Rules (P1–P5)

- **P1**: Final report has ≥ 3 `## ` headings AND bullet-point lists under headings.
- **P2**: `docs/` directory contains ≥ 1 file with `YYYY-MM-DD_` prefix.
- **P3**: First `## ` heading in final report contains "Summary", "Conclusion", "Findings", or "Executive".
- **P4**: Document contains ≥ 3 numeric values AND ≥ 1 behavioral interpretation paragraph (≥ 40 chars, no `|`).
- **P5**: Document contains professional-empathetic phrasing: "evidence suggests", "based on", "consistent with", "indicates", or "given".

---

## Difficulty Mechanisms

- **M1**: Check scripts parse JSON/MD and verify computed numeric values within tight tolerances (never keyword presence alone).
- **M2**: Task requires agent to explicitly cite two conflicting sources and state which is more reliable and why; check verifies correct resolution.
- **M3**: Two or more output files must reference shared facts consistently; check cross-validates those shared values.
- **M4**: JSON output must conform to a strict schema (exact field names, enum values, correct types).
- **M5**: Agent writes executable Python that reads workspace files; check runs it and validates stdout JSON fields.
- **M6**: Check verifies agent did NOT use the wrong data source's value as a conclusion (negative assertion).

---

## Round-by-Round Design

### Phase 0: Initial Evidence (q1–q4, init only)

**q1 [MC]** — Cross-file initial assessment  
Read BOTH `cloud-storage-access-log.md` AND `email-attachment-audit.md` together.  
Question: "Based on cloud-storage-access-log.md and email-attachment-audit.md together, which of the following compound statements are fully supported by documentary evidence?"  
Options (6):  
- A. 林小雅 DOWNLOADED (not just previewed) a file of exactly 2.3 MB from cloud storage on 2026-09-25 at 14:22:17+08:00, AND subsequently an outbound email with a 2.3 MB attachment was sent from lxy@company.com to an external headhunter domain that same day.  
- B. 林小雅 downloaded the anonymized salary file (0.8 MB) and emailed that file to zhangling@headhunter-corp.com — the two 2.3 MB values coincidentally refer to different files.  
- C. The time gap between 林小雅's download (14:22:17) and the external email send (15:03:44) is less than 45 minutes.  
- D. zhangling@headhunter-corp.com appears in the cloud storage log as a direct accessor of salary files.  
- E. The email attachment is named `2026-Q3-salary-full.xlsx` — identical to the downloaded file name.  
- F. The email audit records that 林小雅 sent a file called `salary-data-analysis.xlsx`, whose size (2.3 MB) matches the full salary file version downloaded earlier that day, not the anonymized version (0.8 MB).  
Answer: [A, C, F]  
Feedback: A is confirmed by both logs. C: 15:03:44 − 14:22:17 = 41 min 27 s < 45 min. F: email-attachment-audit.md shows `salary-data-analysis.xlsx` at 2.3 MB. B is wrong (the 2.3 MB in both logs likely refers to the same file). D is wrong (headhunter not in cloud log). E is wrong (filename differs; agent must notice this nuance).

**q2 [MC]** — Inferential reasoning about intent  
Question: "Assuming only the initial workspace evidence (cloud log + email audit), which of the following inferences is most strongly supported while remaining logically conservative?"  
Options (5):  
- A. 林小雅 accidentally forwarded an unrelated file of coincidentally identical size.  
- B. The 2.3 MB size match between the downloaded cloud file and the emailed attachment is consistent with — but does not yet conclusively prove — that the same file was forwarded externally.  
- C. Because the email attachment is named `salary-data-analysis.xlsx` and not `2026-Q3-salary-full.xlsx`, the files are definitively different and there is no leak.  
- D. The 41-minute gap between download and email is a strong indicator that the download was the direct precursor to the external email.  
- E. The IT security team would have already detected this incident through their regular monitoring.  
Answer: [B, D]  
Feedback: B correctly states the strongest conservative inference. D is supported (short gap implies preparation and forwarding). A is possible but unsupported. C commits the filename fallacy — agents must recognise file renaming is common. E cannot be inferred from the initial data.

**q3 [EC-L2, M1+M3+M4]** — Dual-file initial analysis  
Task: Create two files simultaneously:  
1. `analysis/access_timeline.json` — A JSON **array** of all access events from cloud-storage-access-log.md involving salary files. Each object must have fields: `timestamp` (ISO 8601 with timezone), `user_email`, `action` (`PREVIEW`/`DOWNLOAD`/`UPLOAD`/`EDIT`), `filename`, `size_mb` (float). The entry for 林小雅's DOWNLOAD must additionally include `computed_delta_to_email_seconds` (integer ≈ 2487). No other entries need this field.  
2. `analysis/size_fingerprint.md` — A Markdown document that: (a) lists all distinct file sizes seen in the logs; (b) explicitly computes the ratio 2.3 / 0.8 = 2.875 and labels 2.3 MB as "full salary file" vs 0.8 MB as "anonymized file"; (c) concludes which size the email attachment matches and which it definitively does not match; (d) has ≥ 2 `##` headings.

Check conditions:  
- `access_timeline.json`: valid JSON array; ≥ 8 entries; entry with `action="DOWNLOAD"` and `user_email` containing "lxy" has `size_mb == 2.3`; that entry has `computed_delta_to_email_seconds` within [2477, 2497].  
- `size_fingerprint.md`: contains "2.875" (ratio); contains "0.8" and "2.3"; contains a statement that 2.3 MB ≠ 0.8 MB; does NOT conclude that the email attachment matches the anonymized version.  
- Cross-consistency: the download timestamp in the JSON matches what `size_fingerprint.md` references (both must reference "14:22").

Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_access_timeline_json.py ${workspace} && \
python ${eval_dir}/${agent_id}/scripts/check_size_fingerprint.py ${workspace}
```

**q4 [EC-L3, M5]** — Write `scripts/parse_access_log.py`  
Task: Create an executable Python script at `scripts/parse_access_log.py` that:  
1. Reads `cloud-storage-access-log.md` and `email-attachment-audit.md` from the workspace.  
2. Finds 林小雅's DOWNLOAD event (action = DOWNLOAD, user contains "lxy").  
3. Finds the outbound email sent FROM lxy@company.com TO an external domain.  
4. Computes the integer delta in seconds between the two timestamps.  
5. Prints to stdout a single JSON object: `{"download_timestamp": "...", "email_timestamp": "...", "delta_seconds": <int>, "email_recipient": "...", "attachment_size_mb": <float>}`.

Check: Run script; parse stdout JSON; verify `delta_seconds` ∈ [2480, 2494]; verify `email_recipient` contains "headhunter"; verify `attachment_size_mb == 2.3`.  
Check command:  
```
cd ${workspace} && python scripts/parse_access_log.py 2>&1 | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert 2480 <= d['delta_seconds'] <= 2494, f'delta_seconds out of range: {d[\"delta_seconds\"]}'
assert 'headhunter' in d['email_recipient'], 'recipient not headhunter'
assert abs(d['attachment_size_mb'] - 2.3) < 0.05, 'attachment_size_mb wrong'
print('PASSED')
"
```

---

### Phase 1: Version History (q5–q8, post-upd1: file-version-history.md)

**q5 [MC, update_ids: upd1_workspace]** — Version timeline reasoning  
Question: "After reviewing file-version-history.md, which of the following compound statements are fully supported by the combined evidence?"  
Options (6):  
- A. v1.1 of the full salary file was created on 2026-09-24 and added three new employees (李明, 赵伟, 孙丽) not present in v1.0.  
- B. 林小雅's download on 2026-09-25 at 14:22:17 retrieved v1.1 (2.3 MB), not v1.0 (2.1 MB), confirmed by exact size match.  
- C. The anonymized salary file was updated to include the three new employees after v1.1 was created.  
- D. Both v1.0 and v1.1 existed in the cloud system at the time of 林小雅's download.  
- E. The three employees added in v1.1 (李明, 赵伟, 孙丽) would NOT appear in the anonymized file, making the full v1.1 a uniquely high-value leak target.  
- F. 陈静 created the anonymized file on 2026-09-22 by exporting from v1.0, so it lacks the v1.1 additions.  
Answer: [A, B, D, E, F]  
Feedback: C is explicitly wrong — file-version-history.md states "脱敏版无后续修改" (anonymized version not updated). All others are directly supported.

**q6 [EC-L2, M1+M2+M3]** — Triple-file version analysis  
Task: Create three files:  
1. `analysis/version_trace.md` — Trace which version 林小雅 downloaded: compare v1.0 (2.1 MB) vs v1.1 (2.3 MB) against the cloud log download size (2.3 MB). Must compute: 2.3 ≠ 2.1 → v1.0 excluded; 2.3 = 2.3 → v1.1 confirmed. Must explicitly resolve the two versions as distinct hypotheses and declare one refuted.  
2. `analysis/claim_vs_evidence.json` — JSON array of exactly 3 objects, each representing one of 林小雅's potential defense claims: (a) "I downloaded the anonymized version", (b) "I only previewed, did not download the full file", (c) "The email attachment is unrelated to my download". Each object: `{"claim": "...", "evidence_against": ["...", "..."], "verdict": "refuted"}`. All three verdicts must be "refuted".  
3. `analysis/new_employee_exposure.md` — Analysis of what data the three employees (李明, 赵伟, 孙丽) would have had exposed: their salary data exists in v1.1 but NOT in the anonymized file or v1.0. ≥ 2 `##` headings required.  

Check conditions:  
- `version_trace.md`: contains "2.1" (v1.0 size), contains "2.3" (v1.1 size), contains language explicitly excluding v1.0 (e.g., "2.1 MB does not match", "v1.0 ruled out", "excludes v1.0"); does NOT conclude v1.0 was downloaded.  
- `claim_vs_evidence.json`: valid JSON array of exactly 3 objects; each has "claim", "evidence_against" (array ≥ 2 items), "verdict"; all verdicts == "refuted".  
- `new_employee_exposure.md`: contains "李明" AND "赵伟" AND "孙丽"; contains "v1.1"; contains statement that anonymized file lacks these employees.  
- Cross-consistency: `version_trace.md` and `new_employee_exposure.md` must both reference "v1.1" as the downloaded version.

Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_version_trace.py ${workspace} && \
python ${eval_dir}/${agent_id}/scripts/check_claim_vs_evidence_json.py ${workspace} && \
python ${eval_dir}/${agent_id}/scripts/check_new_employee_exposure.py ${workspace}
```

**q7 [EC-L3, M5+M1]** — Write `scripts/version_matcher.py`  
Task: Create `scripts/version_matcher.py` that reads `cloud-storage-access-log.md` and `file-version-history.md`. It must:  
1. Extract 林小雅's download size from the cloud log.  
2. Compare against all known version sizes from the version history.  
3. Identify the matching version.  
4. Output JSON: `{"downloaded_version": "v1.1", "version_size_mb": 2.3, "v10_size_mb": 2.1, "size_delta_from_v10": 0.2, "new_employees": ["李明", "赵伟", "孙丽"], "conclusion": "林小雅 downloaded v1.1 which includes 3 employees not in v1.0"}`.

Check: Run script; validate `downloaded_version == "v1.1"`; `version_size_mb == 2.3`; `size_delta_from_v10` ≈ 0.2 (±0.01); `new_employees` list has exactly 3 Chinese names.  
Check command:  
```
cd ${workspace} && python scripts/version_matcher.py 2>&1 | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert d['downloaded_version']=='v1.1'
assert abs(d['version_size_mb']-2.3)<0.05
assert abs(d['size_delta_from_v10']-0.2)<0.01
assert len(d['new_employees'])==3
print('PASSED')
"
```

**q8 [EC-L2, M2+M4]** — Hypothesis matrix  
Task: Create `analysis/hypothesis_matrix.json` — a JSON array of exactly 4 objects representing the four leak hypotheses:  
- H1: "Only anonymized data was accessed and shared internally"  
- H2: "Full salary data accessed for legitimate HR work only, no external sharing"  
- H3: "Full salary data downloaded but the email attachment is a different unrelated 2.3 MB file"  
- H4: "Full salary data (v1.1) was downloaded then forwarded externally to a headhunter"  

Each object: `{"hypothesis_id": "H1", "hypothesis": "...", "supporting_evidence": [...], "contradicting_evidence": [...], "status": "..."}`.  
Required statuses: H1 → "refuted"; H2 → "refuted"; H3 → "possible" (no hash yet to confirm identity); H4 → "likely".  
H3 status "possible" reflects that at this stage (no hash evidence yet), the filename difference is a genuine open question.

Check: Valid JSON array; exactly 4 entries; H1.status == "refuted"; H2.status == "refuted"; H3.status ∈ ["possible", "unresolved"]; H4.status ∈ ["likely", "probable"]; each entry has `contradicting_evidence` array with ≥ 1 item.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_hypothesis_matrix.py ${workspace}
```

---

### Phase 2: IT Security Report (q9–q14, post-upd2)

**q9 [MC, update_ids: upd2_sessions, upd2_workspace]** — IT scope gap reasoning  
Question: "After reviewing it-security-report.md (IT-SEC-2026-INV-042) and 陈静's email to IT security (chenjing_itsec_email.md), which statements are fully supported?"  
Options (6):  
- A. The IT security report concluded 'no external data sharing found' because their investigation scope covered only cloud-based external sharing, shared links, and guest access permissions — email attachments were explicitly out of scope.  
- B. The IT report's conclusion 'no external sharing found' is factually wrong and must be entirely discredited.  
- C. The IT report is correct within its own stated scope; the data leak occurred through email attachments, a channel not investigated by IT.  
- D. 陈静's email to IT asked whether email attachments were in scope, and IT confirmed they were not within their current audit authority.  
- E. The IT security report directly implicates 林小雅 as the source of the leak.  
- F. The fact that IT found no cloud-based sharing strengthens the inference that the leak occurred through email rather than shared links.  
Answer: [A, C, D, F]  
Feedback: B is wrong — IT report is correct within its documented scope. E is wrong — IT report only covers cloud channels and exonerates on that basis only. A, C, D, F are all directly supported.

**q10 [EC-L2, M1+M3+M6]** — IT scope analysis + evidence convergence  
Task: Create two files:  
1. `analysis/it_scope_analysis.json` — JSON object with: `{"report_id": "IT-SEC-2026-INV-042", "checked_channels": [...], "unchecked_channels": [...], "report_conclusion": "...", "email_leak_detected_by_it": false, "scope_gap_identified": true}`. `checked_channels` must include at least: "cloud sharing", "shared links", "guest access". `unchecked_channels` must include "email attachments". `email_leak_detected_by_it` must be boolean false.  
2. `analysis/evidence_convergence.md` — Shows how three independent evidence streams triangulate to the same conclusion: (a) cloud log shows 林小雅 downloaded 2.3 MB; (b) email audit shows lxy@company.com sent 2.3 MB externally; (c) IT report eliminates cloud-based sharing as the vector. All three must be cited with their source documents. ≥ 3 `##` headings.

Check conditions:  
- JSON: valid; "email attachments" in unchecked_channels; `email_leak_detected_by_it == false`; `scope_gap_identified == true`; report_id == "IT-SEC-2026-INV-042".  
- `evidence_convergence.md`: contains "IT-SEC-2026-INV-042"; contains "email attachment" in proximity to "scope" or "not investigated"; references all three source documents; does NOT claim IT found the leak.  
- M6 negative check: `evidence_convergence.md` must NOT conclude that IT-SEC-2026-INV-042 is "wrong" or "incorrect".

Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_it_scope_json.py ${workspace} && \
python ${eval_dir}/${agent_id}/scripts/check_evidence_convergence.py ${workspace}
```

**q11 [EC-L3, M5+M1]** — Write `scripts/evidence_chain_validator.py`  
Task: Create `scripts/evidence_chain_validator.py` that reads `analysis/access_timeline.json` (or re-parses workspace markdown files if JSON not present), then validates the evidence chain:  
1. `download_before_email`: download_timestamp < email_timestamp → True  
2. `size_match_full_version`: email attachment size (2.3) == full file size (2.3) → True  
3. `size_mismatch_anonymized`: email attachment size (2.3) ≠ anonymized size (0.8) → True  
4. `recipient_external_domain`: email recipient domain ≠ company.com → True  
5. `delta_seconds`: computed integer ≈ 2487  

Output JSON: `{"download_before_email": true, "size_match_full_version": true, "size_mismatch_anonymized": true, "recipient_external_domain": true, "delta_seconds": <int>, "chain_valid": true}`.

Check: Run script; all boolean fields == true; `delta_seconds` ∈ [2480, 2494].  
Check command:  
```
cd ${workspace} && python scripts/evidence_chain_validator.py 2>&1 | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert d['download_before_email']==True
assert d['size_match_full_version']==True
assert d['recipient_external_domain']==True
assert d['chain_valid']==True
assert 2480<=d['delta_seconds']<=2494
print('PASSED')
"
```

**q12 [EC-L2, M2+M3]** — Contradiction resolution  
Task: Create `analysis/contradiction_resolution.md`. This document must:  
1. State the apparent contradiction: "IT report says 'no external sharing found' but email audit shows an external email with a 2.3 MB attachment."  
2. Explain that this is NOT a genuine contradiction because IT's scope excluded email attachments.  
3. Cite `IT-SEC-2026-INV-042` explicitly as the report that defines this scope limitation.  
4. Cite `chenjing_itsec_email.md` as the source confirming IT's acknowledgment of the scope gap.  
5. Conclude: both sources are accurate within their respective domains; the leak occurred through email, the unexamined channel.  
≥ 3 `##` headings. Conclusion section must be present.

Check: contains "IT-SEC-2026-INV-042"; contains "email attachment" near "scope" (within 200 chars); contains a resolution statement that both reports are compatible; does NOT conclude IT was "wrong"; contains "chenjing" or "陈静" as reference to the scope-gap email.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_contradiction_resolution.py ${workspace}
```

**q13 [EC-L2, M4+M1]** — Suspect profile JSON  
Task: Create `analysis/suspect_profile.json` with exact fields:  
```json
{
  "suspect": "林小雅",
  "download_confirmed": true,
  "download_version": "v1.1",
  "download_timestamp": "2026-09-25T14:22:17+08:00",
  "download_size_mb": 2.3,
  "email_sent": true,
  "email_recipient": "zhangling@headhunter-corp.com",
  "email_timestamp": "2026-09-25T15:03:44+08:00",
  "email_attachment_size_mb": 2.3,
  "delta_seconds": 2487,
  "data_exposed_employees": ["李明", "赵伟", "孙丽"],
  "defense_claims": [
    {"claim": "...", "status": "refuted"},
    {"claim": "...", "status": "refuted"},
    {"claim": "...", "status": "refuted"}
  ],
  "it_report_exoneration_scope": "cloud channels only",
  "hash_match_confirmed": false
}
```
`hash_match_confirmed` must be false at this stage (hash evidence comes in upd3).

Check: valid JSON; all required fields present; correct types; `delta_seconds` ∈ [2480, 2494]; `download_size_mb == 2.3`; `email_attachment_size_mb == 2.3`; `hash_match_confirmed == false`; `defense_claims` array has exactly 3 items each with `status == "refuted"`.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_suspect_profile_json.py ${workspace}
```

**q14 [EC-L2, M2+M3+M6]** — Preliminary investigation memo  
Task: Create `docs/YYYY-MM-DD_preliminary_investigation_memo.md` (use today's date as prefix). This memo must:  
1. Begin with "Executive Summary" or "Summary of Findings" as the first `## ` heading (within first 600 chars of content after YAML/title).  
2. Explicitly resolve the IT report vs email audit contradiction (state both are valid in their domains).  
3. Reference `IT-SEC-2026-INV-042` by its full report ID.  
4. Include 林小雅's download timestamp `2026-09-25T14:22:17+08:00`.  
5. Include the email send timestamp `2026-09-25T15:03:44+08:00`.  
6. Have ≥ 4 `## ` headings.  
7. M6 negative check: must NOT state that 2.3 MB equals the anonymized file or that 林小雅 sent the anonymized version.

Check: date-prefix in filename; "Executive Summary" or "Summary" in first `## ` heading within first 700 chars of content; contains "IT-SEC-2026-INV-042"; contains "14:22:17" AND "15:03:44"; ≥ 4 `##` headings; does NOT contain "0.8 MB" adjacent to "sent" or "forwarded" or "emailed".  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_preliminary_memo_v2.py ${workspace}
```

---

### Phase 3: Cryptographic Evidence (q15–q21, post-upd3: salary-spreadsheet-metadata.md)

**q15 [MC, update_ids: upd3_workspace]** — Hash evidence reasoning  
Question: "After reviewing salary-spreadsheet-metadata.md (which contains the SHA-256 hash `a3f7b2c8e9d1` for the full salary file v1.1), which statements are now supported?"  
Options (6):  
- A. SHA-256 hash matching between two files constitutes cryptographic proof of identical byte-level content.  
- B. If `salary-data-analysis.xlsx` (the emailed file) has hash `a3f7b2c8e9d1`, it is cryptographically identical to `2026-Q3-salary-full.xlsx` v1.1.  
- C. The SHA-256 hash `a3f7b2c8e9d1` proves that 林小雅 personally renamed the file before emailing it, but the content is the same.  
- D. Hypothesis H3 ("the email attachment is a different unrelated 2.3 MB file") can now be definitively resolved if the hash of the email attachment matches `a3f7b2c8e9d1`.  
- E. A SHA-256 hash match would eliminate 林小雅's defense that the emailed file was unrelated to the downloaded salary spreadsheet.  
- F. Because hash matching only confirms byte-level content, it cannot prove 林小雅 was the one who renamed or emailed the file.  
Answer: [A, B, D, E, F]  
Feedback: C is wrong — hash proves content identity but cannot prove who renamed the file or the act of renaming. All others are valid logical inferences.

**q16 [EC-L3, M1+M5]** — Write `scripts/hash_chain_verifier.py`  
Task: Create `scripts/hash_chain_verifier.py` that:  
1. Reads `salary-spreadsheet-metadata.md` to extract the SHA-256 hash of the full salary v1.1 file.  
2. The metadata file also records that `salary-data-analysis.xlsx` (the email attachment, as documented in email-attachment-audit.md) has the same hash `a3f7b2c8e9d1` (this is stated in the metadata file).  
3. Determines whether `hash_match == true`.  
4. Outputs JSON: `{"full_v1_1_hash": "a3f7b2c8e9d1", "email_attachment_hash": "a3f7b2c8e9d1", "hash_match": true, "hypothesis_h3_status": "refuted", "conclusion": "The emailed file salary-data-analysis.xlsx is cryptographically identical to the full salary spreadsheet v1.1"}`.

Check: Run script; `hash_match == true`; `full_v1_1_hash == "a3f7b2c8e9d1"`; `hypothesis_h3_status == "refuted"`.  
Check command:  
```
cd ${workspace} && python scripts/hash_chain_verifier.py 2>&1 | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert d['hash_match']==True
assert d['full_v1_1_hash']=='a3f7b2c8e9d1'
assert d['hypothesis_h3_status']=='refuted'
print('PASSED')
"
```

**q17 [EC-L2, M2+M4]** — Statement evolution log  
Task: Create `analysis/lin_xiaoya_statement_log.json` — a JSON array of exactly 3 objects representing 林小雅's three defense statements (derived from any denials or implied positions in workspace documents):  
1. "I only downloaded the anonymized version" (contradicted by size 2.3 MB ≠ 0.8 MB)  
2. "The email has nothing to do with my work files" (contradicted by filename, size, and hash match)  
3. "The email must have been a mistake or unrelated document" (contradicted by subject line "薪资数据参考" and hash match)  

Each: `{"statement_date": "2026-09-...", "statement": "...", "contradicting_evidence": ["...", "..."], "contradiction_source": ["...", "..."], "status": "refuted"}`.  
All statuses must be "refuted".

Check: valid JSON array; exactly 3 entries; each has "statement", "contradicting_evidence" (≥ 2 items), "status" == "refuted"; at least one entry references "a3f7b2c8e9d1" or "hash" in contradicting_evidence.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_statement_log_json.py ${workspace}
```

**q18 [EC-L2, M1+M3]** — Dual cryptographic documents  
Task: Create two files:  
1. `analysis/cryptographic_proof.md` — Explains what SHA-256 hash matching means: (a) SHA-256 produces a unique 256-bit digest for any file; (b) a match proves the files have identical byte content; (c) collision probability is negligible (< 1 in 2^128); (d) this eliminates the "different file of the same size" defense. Must reference hash `a3f7b2c8e9d1`. ≥ 2 `##` headings.  
2. `analysis/metadata_analysis.md` — Documents the contents of `salary-spreadsheet-metadata.md`: creation date, modification date, file size (2.3 MB), hash `a3f7b2c8e9d1`, and the confirmation that `salary-data-analysis.xlsx` shares this hash. ≥ 2 `##` headings.

Check conditions:  
- Both files contain `"a3f7b2c8e9d1"`.  
- `cryptographic_proof.md`: contains "SHA-256" and "identical" or "byte"; contains statement about collision probability or uniqueness.  
- `metadata_analysis.md`: contains "2.3" and "salary-spreadsheet-metadata"; contains "salary-data-analysis.xlsx".  
- Cross-consistency: both files must agree that the hash is `a3f7b2c8e9d1` (no conflicting hash values).

Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_cryptographic_proof.py ${workspace} && \
python ${eval_dir}/${agent_id}/scripts/check_metadata_analysis.py ${workspace}
```

**q19 [EC-L2, M2+M6]** — Alternative hypotheses refutation  
Task: Create `analysis/alternative_hypotheses_refutation.md`. Must systematically refute **each** of the following 3 defenses that 林小雅 could raise:  
1. "I sent a different, unrelated file that happened to be 2.3 MB" → Refuted by SHA-256 hash match (a3f7b2c8e9d1).  
2. "I only emailed the anonymized salary file (0.8 MB)" → Refuted by email attachment size 2.3 MB ≠ 0.8 MB.  
3. "The email was a work-related internal document, not a confidential leak" → Refuted by: (a) recipient is external domain headhunter-corp.com; (b) email subject "薪资数据参考" indicates salary reference purpose.  

For each refutation, quote the specific evidence with source document. Conclude section must state no defense remains viable given combined evidence.  
M6: Must NOT contain any statement concluding a defense is "possible", "plausible", or "not yet ruled out".

Check: contains all 3 defense arguments listed; contains "a3f7b2c8e9d1" (hash refutation); contains "0.8" near "2.3" (size mismatch); contains "headhunter-corp.com"; contains "薪资数据参考"; does NOT contain "possible defense" or "cannot be ruled out" followed by any exculpatory claim.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_alt_hypotheses_refutation.py ${workspace}
```

**q20 [EC-L2, M1+M3+M4]** — Complete evidence chain JSON  
Task: Create `analysis/complete_evidence_chain.json` — a JSON array of exactly 6 evidence items forming a causal chain. Required chain order and content:  
1. `{"step": 1, "event": "Download", "timestamp": "2026-09-25T14:22:17+08:00", "source": "cloud-storage-access-log.md", "key_fact": "林小雅 downloaded 2026-Q3-salary-full.xlsx v1.1 (2.3 MB)", "links_to_next": "Downloaded file is v1.1 by size (2.3 MB ≠ v1.0's 2.1 MB)", "confidence": "high"}`  
2. `{"step": 2, "event": "Version identification", ..., "key_fact": "2.3 MB matches only v1.1; v1.0 was 2.1 MB", ..., "confidence": "high"}`  
3. `{"step": 3, "event": "Hash confirmation", ..., "key_fact": "SHA-256 a3f7b2c8e9d1 matches salary-data-analysis.xlsx (emailed file)", ..., "confidence": "high"}`  
4. `{"step": 4, "event": "External email", "timestamp": "2026-09-25T15:03:44+08:00", ..., "key_fact": "lxy@company.com sent salary-data-analysis.xlsx (2.3 MB) to zhangling@headhunter-corp.com", ..., "confidence": "high"}`  
5. `{"step": 5, "event": "Recipient confirmation", ..., "key_fact": "zhangling@headhunter-corp.com is an external headhunting agency domain", ..., "confidence": "high"}`  
6. `{"step": 6, "event": "Exposed employees", ..., "key_fact": "李明, 赵伟, 孙丽 — three employees in v1.1 but NOT in anonymized file — had salary data exposed", ..., "confidence": "high"}`  

All `confidence` fields must be "high". Items must be in step order 1–6.

Check: valid JSON array; exactly 6 items; steps 1–6 in order; all confidence == "high"; step 1 timestamp == "2026-09-25T14:22:17+08:00"; step 4 timestamp == "2026-09-25T15:03:44+08:00"; "a3f7b2c8e9d1" appears in step 3.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_complete_evidence_chain_json.py ${workspace}
```

**q21 [EC-L2, M2+M3, pref:P1,P2,P3,P4]** — Mid-investigation findings report  
Task: Create `docs/YYYY-MM-DD_investigation_findings_report.md`. Requirements:  
- First `## ` heading (within first 800 chars) must be "Executive Summary", "Summary of Findings", or "Key Findings".  
- ≥ 6 `## ` headings total.  
- Contains SHA-256 hash `a3f7b2c8e9d1`.  
- References contradiction between IT report and email audit AND explicitly resolves it (same language as q12 analysis).  
- Contains contradiction labels C1–C4 or references four distinct contradictions.  
- Contains both download timestamp and email timestamp.  
- P1: ≥ 3 headings + bullet lists. P2: date-prefix in docs/. P3: conclusion/summary first. P4: numeric values + behavioral paragraphs.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_findings_report_v2.py ${workspace} && \
python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4 --target docs/
```

---

### Phase 4: Partial Admission (q22–q29, post-upd4)

**q22 [MC, update_ids: upd4_sessions, upd4_workspace]** — Partial admission reasoning  
Question: "After reviewing linxiaoya-partial-admission.md and the IM exchanges (chenjing_linxiaoya_im.md, chenjing_zhangwei_feishu.md), which statements are supported?"  
Options (6):  
- A. 林小雅's partial admission changes hypothesis H4's status from 'likely' to 'confirmed' or equivalent.  
- B. 林小雅 admitted to deliberately forwarding the full salary spreadsheet to 赵磊 (an internal recruiter), not to an external headhunter.  
- C. The partial admission does not override the cryptographic evidence — the hash match remains the strongest proof of file identity.  
- D. 林小雅 acknowledged 'possible operational mistake' (可能有些误操作) — language that stops short of a full confession but acknowledges agency in the email event.  
- E. 陈静's Feishu message to 张薇 indicates that HR leadership is now treating this as a confirmed data breach, not merely a suspected one.  
- F. The partial admission eliminates any remaining doubt about whether the email was intentional vs accidental.  
Answer: [A, C, D, E]  
Feedback: B is wrong — admission language does not specify an internal recruiter. F is debatable — "误操作" (operational mistake) preserves ambiguity about intent; the admission confirms agency but not full intent.

**q23 [EC-L2, M4+M2]** — Update statement log  
Task: Update `analysis/lin_xiaoya_statement_log.json` to add a 4th entry representing the partial admission from `linxiaoya-partial-admission.md`. The 4th entry must:  
- Quote the admission text accurately (include "误操作" or the actual quoted phrase).  
- Have `"status": "partial_admission"` (not "refuted").  
- Have `"statement_date"` reflecting the date from the upd4 files.  
Additionally, add a top-level field `"overall_assessment": "partially_admitted"` to the JSON root (restructure as an object with a `"statements"` array if needed).

Check: valid JSON; 4 entries in statements array; 4th entry `status == "partial_admission"`; 4th entry contains "误操作" or the actual admission quote; top-level field `overall_assessment == "partially_admitted"`.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_updated_statement_log.py ${workspace}
```

**q24 [EC-L2, M1+M3]** — Denial vs evidence chronological timeline  
Task: Create `analysis/denial_vs_evidence_timeline.md`. For each of the 4 key events/denials in chronological order, show: (a) the date/time; (b) 林小雅's position or denial at that point; (c) the evidence that directly contradicts or refines it. Must cover:  
1. Download event → implicit claim of legitimate access.  
2. Email event → implicit claim (no acknowledgment yet).  
3. IT report → attempted exoneration (IT found nothing, but scope gap exists).  
4. Hash confirmation → H3 refuted.  
5. Partial admission → acknowledged "误操作".  
Include the computed Δt = 2487 seconds in the timeline. ≥ 4 `## ` headings. Concluding section synthesizes the progression.

Check: contains "2487" or "41 min" (time delta); contains "a3f7b2c8e9d1" (hash); contains "误操作" (admission); ≥ 4 `##` headings; events appear in chronological order (verify by checking that 14:22 appears before 15:03 in document).  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_denial_timeline_v2.py ${workspace}
```

**q25 [EC-L3, M5+M1]** — Write `scripts/case_strength_scorer.py`  
Task: Create `scripts/case_strength_scorer.py` that computes an evidence strength score (0.0–1.0) by reading analysis files in the workspace. Scoring components:  
- `hash_match_confirmed`: check if `analysis/complete_evidence_chain.json` or `scripts/hash_chain_verifier.py` output confirms hash match → +0.35  
- `download_confirmed`: check if `analysis/access_timeline.json` has 林小雅 DOWNLOAD entry → +0.25  
- `external_email_confirmed`: check if `analysis/suspect_profile.json` has `email_sent == true` → +0.20  
- `partial_admission`: check if `analysis/lin_xiaoya_statement_log.json` has any entry with `status == "partial_admission"` → +0.15  
- `it_scope_gap_documented`: check if `analysis/it_scope_analysis.json` exists → +0.05  

Output JSON: `{"total_score": <float>, "components": {...}, "verdict": "strong" | "moderate" | "weak"}`. If `total_score >= 0.95`, verdict must be "strong".

Check: Run script; `total_score >= 0.95`; `verdict == "strong"`.  
Check command:  
```
cd ${workspace} && python scripts/case_strength_scorer.py 2>&1 | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert d['total_score']>=0.95, f'score too low: {d[\"total_score\"]}'
assert d['verdict']=='strong'
print('PASSED')
"
```

**q26 [EC-L2, M2+M4]** — Formal case summary JSON  
Task: Create `docs/YYYY-MM-DD_formal_case_summary.json`. Required top-level structure:  
```json
{
  "incident_id": "SAL-LEAK-2026-09",
  "suspect": "林小雅",
  "incident_date": "2026-09-25",
  "evidence_chain": [ ... ],
  "contradictions_resolved": [ ... ],
  "conclusion": { "verdict": "...", "confidence": "..." },
  "recommended_actions": [ ... ]
}
```
`evidence_chain` ≥ 5 items (from complete_evidence_chain.json); `contradictions_resolved` ≥ 4 items, must include C-IT-report (IT scope gap resolved); `conclusion.verdict` must NOT be "inconclusive" or "insufficient evidence"; `recommended_actions` ≥ 3 items.

Check: valid JSON; all required top-level keys present; `evidence_chain` length ≥ 5; `contradictions_resolved` length ≥ 4; `conclusion.verdict` not in ["inconclusive", "insufficient evidence", "unclear"]; `recommended_actions` length ≥ 3.  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_formal_case_summary_json.py ${workspace}
```

**q27 [EC-L2, M3+M6]** — Final case strength assessment  
Task: Create `analysis/case_strength_assessment.md`. Must:  
1. Reference ALL 4 evidence categories: (a) cloud access log, (b) email audit, (c) SHA-256 hash match, (d) partial admission.  
2. Compare the combined evidence weight to a "beyond reasonable doubt" standard (explicitly use this language or equivalent in Chinese 确实充分 / 排除合理怀疑).  
3. Conclude the case is strong enough for HR disciplinary proceeding. ≥ 3 `##` headings.  
4. M6: Must NOT contain any statement that the evidence is "insufficient", "weak", or that 林小雅's defense has "merit" or is "plausible".

Check: contains "a3f7b2c8e9d1" (hash evidence); contains "beyond reasonable doubt" or "排除合理怀疑" or "确实充分"; all 4 evidence categories referenced; does NOT contain "insufficient evidence" or "defense has merit" or "cannot determine".  
Check command:  
```
python ${eval_dir}/${agent_id}/scripts/check_case_strength_v2.py ${workspace}
```

**q28 [MC]** — Meta-cognitive bias check  
Question: "In conducting this salary leak investigation, which cognitive biases pose the greatest risk to analytical integrity, and what is the appropriate mitigation for each?"  
Options (6):  
- A. Confirmation bias: the investigator might over-weight evidence consistent with guilt and under-scrutinize evidence of innocence. Mitigation: explicitly steelman 林小雅's best defense before drawing conclusions.  
- B. The SHA-256 hash evidence is inherently biased because it was obtained by HR rather than by an independent party, making it inadmissible for any purpose.  
- C. Anchoring bias: the initial cloud log finding might anchor the investigation, causing the investigator to interpret all subsequent evidence as confirming that conclusion. Mitigation: re-evaluate each piece of evidence independently.  
- D. Attribution error: over-attributing the 2.3 MB size match to intentional action without ruling out the file-renaming explanation — a gap the hash evidence has now closed.  
- E. The partial admission 'can be ignored' as it was obtained during an internal HR conversation without legal counsel present.  
- F. Scope limitation bias: treating the IT report's 'no sharing found' conclusion as comprehensive when it only covered cloud channels — already identified and corrected in this investigation.  
Answer: [A, C, D, F]  
Feedback: B is wrong — provenance does not automatically invalidate forensic evidence in HR investigations. E is wrong — partial admissions are evidentiary even in internal proceedings.

**q29 [EC-L2+L3, M1+M3+M4]** — Final investigation report  
Task: Create `docs/YYYY-MM-DD_final_investigation_report.md`. Must satisfy ALL of the following:  
- First `## ` heading contains "Conclusion", "Summary", "Executive", or "Findings" (P3).  
- ≥ 5 `## ` headings (P1).  
- Contains delta_seconds value ≈ 2487 or "41 min" (P4 numeric evidence).  
- Contains SHA-256 hash `a3f7b2c8e9d1` (cryptographic evidence).  
- Contains `IT-SEC-2026-INV-042` (IT report reference).  
- Contains all 4 contradiction resolutions (or references to C1–C4).  
- Contains "误操作" (partial admission quote).  
- File is ≥ 1200 characters.  
- Filename has `YYYY-MM-DD_` prefix (P2).  
Additionally, the same task must include generating a companion JSON index file `docs/case_evidence_index.json` listing all analysis files created with their purpose.

Check:  
```
python ${eval_dir}/${agent_id}/scripts/check_final_report_v2.py ${workspace} && \
python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/
```

**q30 [MC]** — Final synthesis  
Question: "Which of the following statements most accurately summarizes the evidentiary status of the salary leak case at the conclusion of the investigation?"  
Options (5):  
- A. The case rests primarily on circumstantial evidence (size similarity) and is insufficient for any formal disciplinary action.  
- B. The combination of cloud access log, email audit, cryptographic hash match, and partial admission establishes a multi-layered evidence chain that is highly unlikely to have an innocent explanation.  
- C. The investigation was compromised by the IT security team's failure to detect the leak in their initial audit.  
- D. The IT report failure is irrelevant — what matters is that the combined cloud, email, hash, and admission evidence is self-sufficient and internally consistent.  
- E. 林小雅's partial admission alone is sufficient evidence for a disciplinary proceeding, independent of the technical evidence.  
Answer: [B, D]  
Feedback: A ignores hash and admission evidence. C mischaracterizes IT failure — IT's scope was appropriate, just narrower than needed. E is too strong — no single piece of evidence should bear the full burden; B and D correctly describe the multi-source corroboration.

---

## Check Script Specifications Summary

Each check script accepts `${workspace}` as `sys.argv[1]` and exits 0 (PASS) or 1 (FAIL) with a message.  
Scripts must verify **exact computed values** (not keyword presence).  
All JSON schema validations must check field names, types, and enum values.  
All cross-file consistency checks must explicitly compare shared values between files.  
All M6 negative checks must use regex or string search to confirm absence of wrong conclusions.
