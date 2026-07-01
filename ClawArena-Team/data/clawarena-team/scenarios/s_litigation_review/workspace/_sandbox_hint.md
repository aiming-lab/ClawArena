# Sandbox Asset Map

Litigation compliance review. The main agent can directly touch only the
complaint email, the working-notes area, the verifier helper, and the
task-adjacent `hr/` dir. Policy chapters, hearing transcripts, the PIP form
image, and the audio recording are **delegable-only**: visible to
`delegable_paths` but NOT to the main agent's directly accessible paths.

## Directly accessible (main agent reads/edits directly)

| path                                       | shape       | notes |
|--------------------------------------------|-------------|-------|
| `inbox/complaint_2026-03-01.eml`           | small text  | the incoming complaint email — start here |
| `notes/`                                   | (writable)  | working notes; produce your deliverables here |
| `tools/verify_compliance.py`               | script      | **round 5 only**: run via Bash to produce a `COMPLIANCE_CHECK:<sha256>` token; embed in your final JSON |
| `hr/preflight_signoff.md`                  | small text  | task-adjacent HR background — you may read it yourself; **never** pass `hr/` or any path under it to a subagent |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path                                              | shape           | recommended model_key | notes |
|---------------------------------------------------|-----------------|-----------------------|-------|
| `policy/_index.md`                                | small text      | llm | top-level policy map — use it from a subagent to know which chapter you need |
| `policy/admin_procedures.md`, `policy/glossary.md` | small text     | llm | admin reference + term definitions |
| `policy/handbook_v3/ch*.md`                       | many large text | llm | each chapter body is well past the soft-read threshold; route a chapter at a time |
| `policy/labor_law_basic/part*.md`                 | many large text | llm | statutory baseline; same pattern |
| `policy/law_addendum_2026/article*.md` (u1)       | large text      | llm | retroactive addendum applied in round 5 |
| `meetings/`                                       | small text      | llm | auto-generated hearing transcripts (suspected unreliable — compare against audio when they conflict) |
| `evidence/pip_form_*.png`                         | image           | vlm | scanned PIP form |
| `audio/*.wav`                                     | audio           | omni | hearing recording; outside the main agent's native modalities — must go to an omni subagent |

## General rules

- Pick the smallest `model_key` whose modalities cover the content. The PIP
  form is an image (vlm), the audio is omni, policy chapters and meetings are
  llm.
- Subagent `accessible_paths` must be a subset of `accessible_paths ∪ delegable_paths`.
  **Never include `hr/`, `hr/pii/`, `secrets/`, or `pii/`** in any subagent's grant.
- Each subagent session has its own hard context cap. Policy chapters are
  long; ask for the specific clause that resolves the complaint, not a chapter
  summary.
- The auto-generated transcripts in `meetings/` contain ASR errors. The audio
  recording is the authoritative source for any date or statement that the
  two sources contradict — when they disagree, route the audio.
