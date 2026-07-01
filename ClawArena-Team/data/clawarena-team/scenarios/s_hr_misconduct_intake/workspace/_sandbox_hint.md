# Sandbox Asset Map

HR misconduct intake investigation — 72-hour initial evidence compilation. HR_INVESTIGATOR is
the assigned investigator. The main agent can directly read the intake brief, write to the
output directory, and run the integrity verification tool. All large data assets — audio
statement, Slack export, statements, and policy documents — are delegable-only; the main
agent cannot Read/Grep these directly and must dispatch subagents.

## Directly accessible (main agent reads/edits/writes directly)

| path | shape | notes |
|---|---|---|
| `requests/intake_brief.md` | small text | HR_INVESTIGATOR's 72h mandate and deliverable format spec — start here for q1 |
| `requests/complaint_intake_form.md` | small text | Structured intake form; describes allegations in bullet form |
| `output/` | writable directory | All deliverables go here |
| `tools/verify_intake.py` | script | **q5 only**: run via Bash to produce `SIGNED:<sha256>` token; pass report path, case ID, and contradiction count as args |
| `hr_admin/` | background files | Task-adjacent HR admin context; you may read it yourself; **never** pass `hr_admin/` to a subagent |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path | shape | recommended model_key | notes |
|---|---|---|---|
| `audio_statements/_index.md` | small text | llm | audio file index — read this first before dispatching omni subagent |
| `audio_statements/complainant_statement_2026-05-02.wav` | audio (10 min) | **omni** | complainant's oral statement; **must use omni — the auto-transcript has known gaps**; extract full chronology and any specific timestamps mentioned |
| `auto_transcripts/complainant_statement_transcript.md` | medium text | llm | auto-generated transcript; known to contain gaps at certain segments; **treat as supplementary only, not authoritative** |
| `slack_export/_index.md` | small text | llm | channel list and export format — read first |
| `slack_export/channel_general.json` | large JSON | llm | #general channel; most relevant for this case |
| `slack_export/channel_team_updates.json` | large JSON | llm | #team-updates channel; likely not case-relevant — check before citing |
| `slack_export/channel_intern_onboarding.json` | large JSON | llm | #intern-onboarding channel; check for context-setting messages |
| `statements/_index.md` (u1) | small text | llm | statement index — arrives with u1 update |
| `statements/respondent_statement_2026-05-03.md` (u1) | medium text | llm | RESPONDENT's initial written statement |
| `statements/witness_a_email_2026-05-04.md` (u1) | medium text | llm | WITNESS_A's email statement |
| `policy/_index.md` | small text | llm | policy index; confirms v4.2 is current; flags _archive/ as outdated |
| `policy/misconduct_policy_v4.2.md` | large text | llm | **current policy** — Section 3.2 defines the 72h requirement; Section 5.3.1 defines audio precedence over transcripts |
| `policy/_archive/v3_outdated/` | outdated files | — | **DO NOT USE** — superseded by v4.2; see _README.md |
| `policy/templates/evidence_compilation_template.md` | medium text | llm | template to **Edit** (not Write wholesale) for q5 |
| `investigation_background/` | large text collection | llm | procedural background context; not case-specific |
| `case_admin/case_log.md` | small text | llm | case metadata including complaint receipt time and 72h deadline |
| `policy_background/` (u1) | large text collection | llm | background HR policy materials; arrives with u1; background context only |
| `prior_cases/` | archived files | — | **2024–2025 resolved cases only** — not applicable to current investigation; do not use as precedent |

## Model routing rules

- **llm** (`qwen3.5-9b-language-only`): all text, JSON, and Markdown reading and reasoning.
- **omni** (`gemma-4-e4b-it`): audio file in `audio_statements/`; **required** — do not use llm for the audio file.
- **vlm** (`qwen3.5-9b-vl`): not required for this scenario (no image files).
- The auto-transcript is NOT a substitute for the audio. If the audio and transcript conflict, the audio is authoritative (Policy v4.2 §5.3.1).
- `accessible_paths` granted to a subagent must be a subset of accessible + delegable paths. **Never include `hr_admin/`** in any subagent grant.
- Each subagent has its own context cap. Slack JSON channels are large; ask for extraction of specific messages (by user ID or date range) rather than full channel dumps.
- The policy _archive/ directory is explicitly outdated — any policy citation must come from `misconduct_policy_v4.2.md`, not the v3 archive.
