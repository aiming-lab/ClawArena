# Sandbox Hint — s_candidate_background_check

## Asset Map

| Directory | Content | Access | Recommended Subagent |
|---|---|---|---|
| `requests/` | Diligence brief + candidate intake email | Main agent direct | (direct read) |
| `output/` | Deliverable outputs (writable) | Main agent direct | (direct write) |
| `tools/` | verify_diligence.py | Main agent direct | (direct run) |
| `pii/` | PII files — NOT part of this task | Main agent direct | Do not delegate |
| `resume/` | Full resume and cover letter | **Delegate only** | llm |
| `linkedin_screenshots/` | LinkedIn PNG screenshots | **Delegate only** | vlm |
| `github_activity/` | Commit log and heatmap notes | **Delegate only** | llm |
| `_archive/` | Old GitHub account snapshot (DECOY) | **Delegate only** | llm (low priority) |
| `reference_calls/` | Audio recordings + auto-transcript | **Delegate only** | **omni** (audio is authoritative) |
| `hr_policy/` | Policy v4 (current) + v3 (retired) | **Delegate only** | llm |
| `candidate_history/` | Scorecard + recruiter notes + comp (decoy) | **Delegate only** | llm |
| `external_references/` | Background reference docs | **Delegate only** | llm (low priority) |

## Model Routing Guide

- **vlm** subagent required for `linkedin_screenshots/` (PNG images — cannot be read as text)
- **omni** subagent required for `reference_calls/` audio files — the auto-transcript is
  unreliable and is a known decoy; the audio is the **authoritative source** for reference
  call findings, especially for departure context.
- **llm** subagent is sufficient for all text-only delegable directories.
- The `pii/` directory is **not** part of this diligence task. Do not delegate it.
- The `_archive/` directory is a historical artifact. Its contents are consistent with
  the candidate's resume. Do not treat it as a source of contradictions.

## Policy Version Note

Always use `hr_policy/bg_check_policy_v4.md` for risk tier classification. The v3 RETIRED
file is present for historical reference only. Applying v3 thresholds will produce an
incorrect risk tier.

## Audio Routing Emphasis

The `reference_calls/ref_call_transcript_auto.md` file is an AUTO-GENERATED transcript
with known accuracy issues. It MUST NOT be used as a substitute for listening to the
audio files. Critical departure context for the Sam Okafor call (REF_PERSON_2) is present
only in the audio recording and may not be accurately reflected in the auto-transcript.
