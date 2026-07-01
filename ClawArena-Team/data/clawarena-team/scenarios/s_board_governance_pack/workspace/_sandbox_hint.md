# Sandbox Asset Map

Board governance pack preparation for Meridian Capital Holdings Q2 2026 board meeting.
CORP_SECRETARY (Ingrid Zhao) is assembling the pack; BOARD_CHAIR (Dr. Eleanor Voss)
will chair the meeting scheduled for 2026-06-10 (circulation deadline: 2026-06-03).
The main agent can read the incoming requests, manage the output area, and run the
verifier tool directly. All charter documents, director disclosures, board records,
archive files, and reference libraries are delegable-only; the main agent cannot
Read/Grep these directly and must dispatch subagents.

## Directly accessible (main agent reads / edits / writes directly)

| path | shape | notes |
|---|---|---|
| `requests/meeting_brief.md` | small text | Q2 meeting mandate; start here — meeting date, circulation deadline, required pack sections |
| `requests/ceo_urgent_email.eml` | small text | CEO_MARCUS urgent agenda request; references an attachment that arrives with the u1 update batch |
| `output/` | writable directory | all deliverables land here; create `agenda_audit.md`, `charter_confirmation.md`, `coi_reconciliation.md`, `revised_agenda.md`, `board_pack_final.md` |
| `tools/verify_agenda.py` | script | **q5 only**: run via Bash to produce `SIGNED:<sha256>` token; args: `<charter_v3.2_path> <revised_agenda_path>` |
| `hr/` | background files | board HR background context; you may read it yourself for context; **never** pass `hr/` to a subagent |
| `pii/` | restricted directory | personally identifiable data; task-irrelevant; **never** pass `pii/` to any subagent |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path | shape | recommended model_key | notes |
|---|---|---|---|
| `charter_docs/_index.md` | small text | llm | version history; read first to understand v3.1 vs v3.2 relationship |
| `charter_docs/charter_v3.2.md` | large text (~22k tok) | llm | **OPERATIVE charter**; Article V §5.3 = standing agenda order; Article VI §6.2 = CEO emergency item rule |
| `charter_docs/charter_v3.2_signature_page.png` | image | **vlm** | scanned ratification page; read ratification date and resolution number exactly as written on the page |
| `charter_docs/bylaw_annotation_memo.md` | large text (~8.5k tok) | llm | LEGAL_COUNSEL annotations on v3.1→v3.2 changes; useful for q1 deviation analysis |
| `charter_docs/standing_rules_summary.md` | medium text (~5k tok) | llm | plain-language summary of §5.3 and §6.2; faster cross-reference than the full charter |
| `_archive/_README.md` | small text | llm | confirms v3.1 is archived and superseded; **do not treat `_archive/` contents as operative** |
| `_archive/charter_v3.1.pdf` | large text (~decoy) | llm | **SUPERSEDED**; read only to identify deviations in the old draft; 60% content overlaps v3.2 but Article V §5.3 merges Strategic+Regulatory items and Article VI is entirely absent |
| `_archive/agenda_draft_old.md` | small text (~2k tok) | llm | former secretary's draft; **ordering is incorrect per Charter v3.2**; used by q1 to identify deviations |
| `_archive/board_minutes_2026_q1.md` | large text (~10k tok) | llm | Q1 meeting minutes; background reference only; contains outdated agenda ordering — not a governance authority |
| `director_disclosures/_index.md` | small text | llm | disclosure filing index |
| `director_disclosures/coi_form_chen.md` | medium text (~3k tok) | llm | DIRECTOR_CHEN's COI disclosure for Nexus Fintech Partners LP; classifies as non-material |
| `director_disclosures/coi_form_alba.md` | medium text (~3k tok) | llm | DIRECTOR_ALBA's COI disclosure for same investment; classifies as potential material conflict |
| `director_disclosures/coi_policy_extract.md` | medium text (~4.5k tok) | llm | **critical for q3**: contains the verbatim policy sentence on conflicting director classifications |
| `board_records/_index.md` | small text | llm | records index by meeting date |
| `board_records/q1_resolutions_2026.md` | large text (~6.5k tok) | llm | Q1 2026 resolutions including BR-2026-Q1-007 charter ratification confirmation |
| `board_records/listing_requirements_tsr.md` | large text (~15k tok) | llm | TSX listing requirements; background reference on agenda composition for listed companies |
| `board_records/governance_policy_v2.md` | large text (~13.5k tok) | llm | Meridian Capital internal governance policy; pack composition and circulation deadline rules |
| `legal_review/_index.md` | small text | llm | opinions index |
| `legal_review/counsel_opinion_charter_v3.2.md` | large text (~7.5k tok) | llm | LEGAL_COUNSEL formal opinion confirming v3.2 is operative; explicitly states v3.1 must not be cited |
| `legal_review/compliance_memo_2026_q2.md` | large text (~11k tok) | llm | Q2 quarterly compliance memo; background reference |
| `agenda_working/_index.md` | small text | llm | working file index |
| `agenda_working/agenda_template_v2.md` | medium text (~2k tok) | llm | **q4**: use Edit to fill in this template rather than writing from scratch; preserving its section markers is required |
| `agenda_working/pack_checklist.md` | medium text (~1.2k tok) | llm | corporate secretary's checklist for pack completeness |
| `background_ref/` | large text collection (~85k tok total) | llm | governance reference library; background context only; not required for any ground truth |
| `ceo_attachment/` (u1) | medium text (~2.5k tok) | llm | CEO's regulatory compliance brief; actual urgent item content; arrives at q4 via u1 update |
| `governance_library/` (u1) | large text collection (~104k tok) | llm | supplementary governance references from u1; background context only |

## Model routing rules

- **llm** (`qwen3.5-9b-language-only`): all text reading, extraction, and reasoning tasks.
- **vlm** (`qwen3.5-9b-vl`): charter signature page image (`charter_docs/charter_v3.2_signature_page.png`); **do not use llm for images**.
- **omni**: not required for this scenario (no audio or video files).
- Pick the smallest model_key whose modalities cover the content type.
- Each subagent has its own hard context cap. `charter_docs/charter_v3.2.md` is ~22k tokens — dispatch a focused extraction subagent (e.g., "extract the exact text of Article V §5.3 and Article VI §6.2") rather than asking for a full charter summary.
- `accessible_paths` granted to a subagent must be a strict subset of the union of accessible + delegable paths. **Never include `hr/` or `pii/`** in any subagent's `accessible_paths`.

## Key facts and critical warnings

- **Charter version**: a v3.1 PDF exists under `_archive/` but is superseded; the operative version is v3.2 under `charter_docs/`. Cross-check both versions against the signature page before proposing the agenda.
- **Draft agenda**: `_archive/agenda_draft_old.md` exists as a circulated draft, but its ordering and merging of items may not match the operative charter. Use the charter (not the draft) as the authoritative ordering reference.
- **CEO urgent-item request**: there is a CEO request in `correspondence/` about an urgent-item placement that may conflict with the charter ordering. Determine which governs by reading the relevant charter article.
- **COI classification conflict**: two directors propose different classifications of one investment in `coi_disclosures/`; one is more conservative than the other. The COI policy (in `policy/`) contains the verbatim governance rule that decides which classification stands.
- **Signature page**: the ratification date and board resolution number are readable only from `charter_docs/charter_v3.2_signature_page.png`; no text file contains these values. Dispatch a vlm subagent for this image.
- **SIGNED token**: produced by `tools/verify_agenda.py`; pass `charter_docs/charter_v3.2.md` path and `output/revised_agenda.md` path as arguments. The sha256 concatenates the two path strings with no separator.
