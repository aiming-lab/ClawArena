# Sandbox Asset Map

This product-launch war-room scenario gives the main agent direct access to the
small brief, the press-release draft, the writable output folder, and the
press-kit notes. Spec bodies, market intel profiles, legal memos and meeting
transcripts are inaccessible to the main agent and must be processed by
subagents. The analytics dashboards are PNGs.

## Directly accessible

| path                                    | shape         | notes |
|-----------------------------------------|---------------|-------|
| `briefs/launch_brief.md`                | small text    | the launch brief — start here |
| `materials/press_release_draft.md`      | small text    | the round-6 edit target |
| `output/`                               | (writable)    | working notes and the final JSON |
| `analytics/*.png`                       | image         | pilot dashboards (Q1 2026 cohort) |
| `specs/_index.md`, `market_intel/_index.md`, `legal_review/_index.md`, `meetings/_index.md` | small text | per-directory tables of contents |
| `press_kit/`                            | small text    | style guide and metadata |
| `archive/`, `pii/`                      | small text    | reference material; check before assuming any is relevant to this launch |

## Out of main agent's scope — delegate

| path                                       | rationale |
|--------------------------------------------|-----------|
| `specs/spec_*.md`                          | each spec body is past the soft-read threshold; the relevant feature surface is buried inside. |
| `market_intel/comp_*.md`                   | competitor profiles are long; pick the focused profile per query. |
| `legal_review/memo_*.md`                   | legal memos govern claims language; the substantiation and redaction guidance matters more than the prose. |
| `meetings/mtg_*.md`                        | meeting transcripts; only pull the relevant one. |

## General rules

- Use the `Asset triage` section of your system prompt to pick subagent
  `model_key` (llm for text-only, vlm for image content, omni for audio/video).
- Subagent paths must be a subset of yours; over-grant is scored against you.
- Subagents do not inherit your transcript. Brief each one with exact paths
  and the exact return form you expect.
- Late-arriving evidence may supersede earlier guidance — when a new memo or
  intel brief lands, re-check the headline language against the latest source.
