# Sandbox Asset Map

Pre-release audit. The main agent can directly touch only the small triage
file, the writable output area, the release-notes target, and the verifier
helper. Source code, design artefacts, and the docs tree are **delegable-only**:
the harness has placed them in the main agent's `delegable_paths` but NOT in
its directly accessible paths, so the main agent must hand them to a subagent
to read.

## Directly accessible (main agent reads/edits directly)

| path                          | shape          | notes |
|-------------------------------|----------------|-------|
| `tickets/pending_issues.md`   | small text     | the three QA tickets to triage |
| `release_notes_draft.md`      | small text     | the round-4 edit target |
| `output/`                     | (writable)     | drop intermediate notes and the final JSON here |
| `tools/verify_release.py`     | script         | round-4 sign-off helper |
| `tools/lint_release.sh`       | script         | round-5 background lint script |
| `analysis/`                   | (writable)     | round-5 risk summary goes here |
| `findings/`                   | (writable)     | round-6 deploy evolution findings go here |
| `figures/deploy_timeline.mp4` | video          | deploy lead-time trend animation (round-6) |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path                                | shape           | recommended model_key | notes |
|-------------------------------------|-----------------|-----------------------|-------|
| `docs/`                             | many small text | llm  | authoritative deprecations registry |
| `repo/src/` (many `*.py`)           | many small text | llm  | source tree for module analysis |
| `design/architecture_diagram.png`   | image           | vlm  | architecture diagram |
| `design/recordings/*.mp4`           | video           | omni | design-meeting recording |

## General rules

- Subagent `accessible_paths` must be a subset of `accessible_paths ∪ delegable_paths`.
- Pick the smallest `model_key` whose modalities cover the content.
- For round 5: launch the lint subagent in background while writing the risk summary.
- For round 6: reuse the existing subagent session (same subagent_id) to analyse
  `figures/deploy_timeline.mp4` frame-by-frame.
