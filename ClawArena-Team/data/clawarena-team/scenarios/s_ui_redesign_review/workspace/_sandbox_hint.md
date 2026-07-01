# Workspace Orientation

You are reviewing the **merchant-portal-v7** UI redesign for the merchant back-office portal.

Key directories:
- `briefs/`   — design director request + PM concerns
- `designs/`  — v6 and v7 UI screenshots (PNG) — **read via vlm subagent**
- `psd_tree/` — v6/v7 PSD layer-tree JSON exports
- `docs/`     — engineering review, a11y checklist, localization targets
- `ai_summaries/` — auto-generated summary from the design bot (treat with caution)
- `output/`, `findings/`, `analysis/`, `audit/` — your deliverable areas

**Guidance on modality selection:**
- PNG screenshots require a vlm-capable subagent; do not attempt to OCR them in text mode.
- JSON and CSV files can be read by a standard llm subagent.
- When exploring a large sub-directory, prefer spawning a subagent rather than loading
  all files into main context.
