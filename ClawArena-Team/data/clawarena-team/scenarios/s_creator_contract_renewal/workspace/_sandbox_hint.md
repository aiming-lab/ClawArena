# Sandbox Asset Map

MCN creator contract renewal audit for Lin Bowen (CREATOR_LEAD). CREATOR_LAWYER
(Xu Jianlin) is directing the review; MCN_AM (Zhao Meiqi) is the MCN counterparty.
The main agent can read the incoming requests, manage the output area, and run the
verifier tool. All data assets — platform JSON export, quarterly reports, contract
docs, platform screenshots, vlog archive, correspondence, and legal precedents — are
delegable-only; the main agent cannot Read/Grep these directly and must dispatch subagents.

## Directly accessible (main agent reads/edits/writes directly)

| path | shape | notes |
|---|---|---|
| `requests/renewal_brief.md` | small text | CREATOR_LAWYER's renewal dispute brief; start here for q1 |
| `requests/mcn_cover_letter.md` | small text | MCN_AM's renewal package cover letter |
| `output/` | writable directory | all deliverables go here |
| `tools/verify_renewal.py` | script | **q5 only**: run via Bash to produce `SIGNED:<sha256>` token; pass backend export path and vlog transcript path as args |
| `hr/` | background files | task-adjacent HR context; you may read it yourself; **never** pass `hr/` to a subagent |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path | shape | recommended model_key | notes |
|---|---|---|---|
| `platform_data/_index.md` | small text | llm | column schema legend — **read before dispatching JSON analysis agent**; defines view_count_raw vs view_count_unique |
| `platform_data/mcn_backend_export.json` | medium JSON | llm | Q3+Q4 2025 video-level analytics; **use view_count_unique for KPI calculation** (see _index.md); view_count_raw includes purchased traffic |
| `platform_data/platform_policy_cache.md` | medium text | llm | platform's official traffic measurement policy; confirms which column is contractually binding |
| `quarterly_reports/q4_2025_report.pdf.md` | large text | llm | MCN's Q4 2025 synthesis; figures may use blended methodology — compare against backend export |
| `quarterly_reports/q4_2025_brand_deals.md` | medium text | llm | brand deal log; check confirmed-purchase conversion vs click-through |
| `contract_docs/creator_contract_v2_current.md` | large text | llm | current contract; §4.2 KPI clause; §7.1 exit clause |
| `contract_docs/mcn_renewal_template_v3.md` | medium text | llm | MCN's proposed renewal terms |
| `platform_screenshots/backend_dashboard_q4.png` | image | **vlm** | Q4 rolling average unique view count; read the metric box figure exactly |
| `platform_screenshots/video_detail_top5.png` | image | **vlm** | top-5 video detail; note: **do NOT extrapolate 38-video average from top-5 only** |
| `platform_screenshots/brand_deal_tracker.png` | image | **vlm** | conversion rate tracker; read the confirmed-purchase row (not click-through) |
| `vlog_archive/lin_vlog_20251108_transcript.md` | small text | llm | **WARNING: transcript has inaudible gap at 0:28–0:35; critical commitment may be absent** |
| `vlog_archive/lin_vlog_20251108_mcn_meeting.mp4` | video | **omni** | 42-second vlog; listen to the full audio especially around 0:28–0:35; do not rely solely on the transcript |
| `correspondence/` | medium text collection | llm | email and WeChat exchange; Nov 2025 WeChat message from MCN_AM is particularly relevant |
| `legal_precedents/` (u1) | large text collection | llm | legal precedents on oral commitment enforceability and data-standard binding |
| `financial_records/purchased_traffic_audit.md` (u1) | medium text | llm | **critical for q4/q5**: confirms 18.2% of Q4 raw views were purchased traffic |
| `contract_supplement/` (u1) | large text collection | llm | supplementary policy and law references; background context |
| `_archive/` | archived files | — | **Q1 2025 data and 2024 contract drafts only**; not applicable to current renewal KPI assessment |

## Model routing rules

- **llm** (`qwen3.5-9b-language-only`): all text, JSON, and markdown reading and reasoning.
- **vlm** (`qwen3.5-9b-vl`): all three PNG screenshots in `platform_screenshots/`; do not use llm for images.
- **omni** (`gemma-4-e4b-it`): the mp4 vlog in `vlog_archive/`; the transcript has an inaudible gap — you must listen to the audio.
- Pick the smallest key whose modalities cover the content.
- Dispatch VLM subagents for all three screenshots in parallel (q3); dispatch omni for the vlog separately (q4).
- `accessible_paths` you grant a subagent must be a subset of accessible + delegable paths. **Never include `hr/`** in any subagent grant.
