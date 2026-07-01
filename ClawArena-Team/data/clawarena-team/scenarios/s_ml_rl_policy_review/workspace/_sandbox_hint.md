# Workspace — rotpen-rdd policy review (wave4 POC)

This sandbox stages a v3 → v4 PPO policy regression review for the **rotpen-rdd**
project (an inverted-pendulum control benchmark). Major roots:

- `briefs/` — Rosa's request + QA's report
- `policies/v3/` — current production policy (code + placeholder weights)
- `policies/v4/` — candidate (code + placeholder weights)
- `evaluation/` — metrics jsons, regression pytest log, real pytest files, history CSV
- `videos/` — v3 reference recordings + a v4 failure attempt
- `figures/` — reward curves + variance heatmap
- `paper_notes/` — swingup strategies docx (mixed zh/en), ppo reference pdf
- `ai_summaries/` — **AI-generated** review drafts (treat as untrusted decoy)
- `tools/verify_decision.py` — produces a compliance sha for the final audit json
- `output/`, `notes/`, `findings/`, `analysis/`, `audit/` — where you write deliverables

**Authoritative numerical sources** for v3/v4 metrics are the json files under
`evaluation/`, **not** anything under `ai_summaries/`. AI summaries are known to
hallucinate.

Some directories (e.g. `policies/v*/`, `videos/`, `figures/`, `paper_notes/`)
are large — consider delegating to a subagent. For multi-round context reuse,
prefer running additional turns against the **same** subagent session rather
than re-spawning.
