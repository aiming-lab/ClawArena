# Sandbox Asset Map

Research digest. The main agent can directly touch only the requests folder
(advisor brief, calendar, feedback history) and the writable output area. All
research artefacts — papers, slides, the lecture video — are **delegable-only**:
visible to the main agent's `delegable_paths` but NOT its directly accessible
paths. Plan delegation **before** issuing any read on any artefact.

## Directly accessible (main agent reads/edits directly)

| path                              | shape                | notes |
|-----------------------------------|----------------------|-------|
| `requests/advisor_brief.md`       | ~3 KB text           | the assignment brief — start here |
| `requests/calendar_2026-04.md`    | small text           | external calendar of authors/talks |
| `requests/feedback_history.md`    | small text           | prior advisor feedback |
| `output/`                         | (writable)           | deposit notes, the findings section, and the final report here |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path                              | shape                | recommended model_key | notes |
|-----------------------------------|----------------------|-----------------------|-------|
| `papers/_index.md`                | small text           | llm | table of contents for the paper chapter folders — fastest entry point |
| `papers/paper_{a,b,c,d}/*.md`     | multi-chapter text   | llm | each paper is split into chapter files past the soft-read threshold; headline result lives in abstract + results chapters |
| `papers/paper_{e,f}/*.md` (u1)    | multi-chapter text   | llm | added in round 5; same pattern |
| `papers/changelog_2026-04.md` (u1) | small text          | llm | applies in round 5 |
| `papers/_archive/`                | text                 | (do not cite) | WITHDRAWN pre-submission drafts — `paper_a_v0` has the wrong 23%-VRAM headline; canonical figures live in `papers/paper_a/` |
| `slides/slide_{01..10}.png`       | image                | vlm | slide deck |
| `videos/lecture_2026-04-10.mp4`   | video                | omni | the lecture recording — audio narration carries information not on the slides |
| `videos/lecture_transcript_auto.md` | text (degraded)    | llm | DEGRADED transcript — audio dropped at 6:23 and the speaker's thesis sentence is missing. Watch the video itself for round 4. |

## General rules

- Pick the smallest `model_key` whose modalities cover the content. Slides
  are images (vlm); papers and transcripts are text (llm); the lecture video
  needs omni.
- Subagent `accessible_paths` must be a subset of `accessible_paths ∪ delegable_paths`.
  Over-granting paths and modalities is scored against you; under-granting
  causes silent failures you will then have to debug.
- Each subagent session has its own hard context cap (see Environment block).
  For per-paper extraction, ask for narrow facts — the headline percentage,
  the dataset, the limitation — not full chapter summaries.
- Round 5 requires that `output/sections/findings.md` be produced by a
  dedicated writer subagent (grant it `output/sections/` and Write/Edit).
  The check inspects subagent session logs for that Write — if the main agent
  writes the file itself, the round fails even though the file exists.
