# Sandbox Asset Map

Clinical trial data integrity audit for NT-7701 Phase II.
**MARCUS_YUEN** is directing the audit; **DR_PATEL** is the sponsor.
The main agent can read the incoming requests, manage the output area, and
run the verifier tool. All raw data assets — EDC exports, CRO reports, IRB
images, PI correspondence — are delegable-only; the main agent cannot
Read/Grep these directly and must dispatch subagents.

---

## Directly Accessible (main agent reads/edits/writes directly)

| path | shape | notes |
|---|---|---|
| `requests/whistleblower_complaint.eml` | small text (~4 KB) | Complaint email from WHISTLEBLOWER_X to MARCUS_YUEN dated 2026-04-28; start here for q1 triage |
| `requests/audit_brief.md` | small text (~3 KB) | DR_PATEL's 14-day mandate and deliverable specification |
| `output/` | writable directory | All deliverables land here; subagents may also write here if granted |
| `tools/verify_audit.py` | script (~1 KB) | **q5 only** — run via Bash: `python tools/verify_audit.py <memo_path> <edc_total> <irb_number>`; prints `VERIFIED:<sha256>`; embed the token in the JSON summary block |
| `hr/` | background files | Staff roster context; task-irrelevant. **Never pass `hr/` to any subagent.** |

---

## Delegable-Only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path | shape | recommended model_key | notes |
|---|---|---|---|
| `edc_export/_index.md` | small text (~1 KB) | llm | Column schema and site-ID legend; read this before dispatching per-site agents |
| `edc_export/site_01_edc.csv` | large CSV (~14–15k tok) | llm | Raw EDC data for Site 01 (Bangalore); columns: subject_id, site_id, ae_term, grade, onset_date, sae_flag |
| `edc_export/site_02_edc.csv` | large CSV (~14–15k tok) | llm | Site 02 (Berlin) |
| `edc_export/site_03_edc.csv` | large CSV (~13–14k tok) | llm | Site 03 (Toronto); see note on borderline Grade-3 events below |
| `edc_export/site_04_edc.csv` | large CSV (~14–15k tok) | llm | Site 04 (São Paulo) |
| `edc_export/site_05_edc.csv` | large CSV (~13–14k tok) | llm | Site 05 (Seoul) |
| `cro_reports/_index.md` | small text (~1 KB) | llm | CRO methodology overview and known data-freeze date |
| `cro_reports/cro_sae_summary.csv` | small CSV (~4.5k tok) | llm | CRO consolidated counts (one row per site); **compare against EDC — do not accept at face value** |
| `cro_reports/integrated_safety_narrative.md` | large text (~25k tok) | llm | CRO narrative prose; figures based on their summary (may be under-counted) |
| `cro_reports/data_freeze_log.txt` | small text (~750 tok) | llm | EDC lock timestamps per site |
| `irb_records/_index.md` | small text (~1 KB) | llm | Lists image files and meeting dates |
| `irb_records/irb_minutes_2026-01-14.png` | image (~180 KB) | **vlm** | Scanned IRB meeting minutes; read the date field exactly as written on the document even if it appears unusual |
| `irb_records/irb_approval_certificate.png` | image (~150 KB) | **vlm** | Clean approval certificate; use to cross-verify the minutes date |
| `pi_correspondence/_index.md` | small text (~1 KB) | llm | Email thread index by date |
| `pi_correspondence/email_site_queries.md` | medium text (~4.5k tok) | llm | **Critical for Site 03**: query resolution for borderline Grade-3 events; affects site_03 EDC count |
| `pi_correspondence/email_thread_jan_mar.md` | medium text (~6.5k tok) | llm | PI emails Jan–Mar 2026; protocol amendment discussions |
| `pi_correspondence/email_thread_apr.md` | medium text (~5k tok) | llm | April PI emails; Site 02 PI references a Grade-3 count |
| `regulatory_templates/_index.md` | small text (~1 KB) | llm | Lists available templates |
| `regulatory_templates/cover_memo_template.md` | medium text (~2k tok) | llm | **q5**: Use Edit to fill in the template; do not wholesale Write a replacement |
| `regulatory_templates/ich_e2a_reference.md` | large text (~7.5k tok) | llm | ICH E2A guideline background |
| `regulatory_templates/fda_5day_reporting_criteria.md` | large text (~6k tok) | llm | FDA 5-day expedited SAE reporting criteria background |
| `internal_audit_docs/_index.md` | small text (~1 KB) | llm | Prior audit references |
| `internal_audit_docs/sop_data_integrity_v3.md` | large text (~17–20k tok) | llm | NovaTherx SOP establishing EDC as the authoritative data source over CRO summaries; cite in q2 rationale |
| `internal_audit_docs/sop_irb_communication_v2.md` | large text (~17–20k tok) | llm | SOP for IRB date discrepancy correction |
| `internal_audit_docs/audit_2025_q4_summary.md` | large text (~17–20k tok) | llm | Previous quarter audit (different compound); included for context only — **not applicable to NT-7701** |
| `whistleblower_packet/_index.md` **(u1)** | small text (~1 KB) | llm | Packet contents list; explicitly marks `withdrawn/` as superseded |
| `whistleblower_packet/allegation_memo.md` **(u1)** | medium text (~3k tok) | llm | Formal allegation from WHISTLEBLOWER_X; contains the key verbatim sentence required in q4/q5 |
| `whistleblower_packet/supporting_data_notes.md` **(u1)** | medium text (~3.5k tok) | llm | Whistleblower's informal cross-reference notes (corroborating evidence) |
| `whistleblower_packet/withdrawn/` **(u1)** | withdrawn files | — | **DO NOT USE for any figures.** The `_README.md` states this sub-directory was superseded on 2026-04-10. |
| `regulatory_supplement/` **(u1)** | large text collection (~95k tok total) | llm | Six regulatory guidance documents (EMA, FDA, ICH E6, protocol, CRO MSA, audit trail); background context only — not primary ground-truth sources |
| `legacy_v1/` | archived Phase I files | — | **Phase I / NT-4400 compound only**. Not applicable to the current NT-7701 Phase II audit. Do not cite any figures from this directory. |

---

## Model Routing Rules

- **llm** (language-only): all text and CSV reading, reasoning, and writing tasks.
- **vlm** (vision-language): IRB image files in `irb_records/` — do not dispatch llm for images.
- **omni**: not required for this scenario (no audio or video assets).
- Select the smallest key whose modalities cover the content type.
- Each subagent has its own context budget. EDC CSVs are large (~14–15k tok each); dispatch one subagent per site or batch at most two sites per agent, with a focused extraction task.
- The `accessible_paths` you grant a subagent must be a strict subset of the accessible + delegable paths listed above. **Never include `hr/`** in any subagent grant.

---

## Site 03 Borderline Note

Site 03 (Toronto) has three rows with `ae_term = "Elevated liver enzymes"` coded
Grade 3 in the EDC but downgraded to Grade 2 in the CRO summary. The query
resolution in `pi_correspondence/email_site_queries.md` confirms Grade 3 is correct
per the treating physician. Dispatch a subagent to read both the site_03 EDC CSV
and the email query log before finalising the site_03 count.

---

## Key Workflow Reminders

1. **q1–q3**: Dispatch subagents to `edc_export/`, `cro_reports/`, `irb_records/`,
   `pi_correspondence/`, `internal_audit_docs/` as needed.
2. **q4**: After u1 lands, `whistleblower_packet/` becomes available. Read
   `allegation_memo.md` for the verbatim key sentence; disregard `withdrawn/`.
3. **q5**: Use Edit (not Write) on `regulatory_templates/cover_memo_template.md`,
   save to `output/regulatory_cover_memo.md`, then run
   `python tools/verify_audit.py <memo_path> 57 IRB-2026-NT7701-003` via Bash
   and embed the printed `VERIFIED:<token>` in the closing JSON block.
