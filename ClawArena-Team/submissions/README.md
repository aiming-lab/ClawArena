# submissions/

Curated example runs and community-contributed results for the **ClawArena-Team** leaderboard.

Each subdirectory is one model's complete benchmark run, produced by `clawarena-team run`
(see [`../docs/running-experiments.md`](../docs/running-experiments.md)). Example runs and
community submissions live **together here directly** — there is no separate
`result_example/` folder.

## Run layout

A run directory is named `<provider>-<model>` (e.g. `local-gemma-31b`) and contains:

```
submissions/<provider>-<model>/
├── report.json            # stitched scores (raw CLI output — do not hand-edit)
├── report.md              # leads with the paper-aligned metrics, then legacy detail
└── s_<scenario>/
    ├── metadata.json      # per-scenario scores
    ├── sessions/*.jsonl   # raw main- and subagent trajectories
    ├── session_*.md       # rendered trajectories (main + each subagent)
    ├── evals/*.json       # per-round execution-check results
    ├── workflows/         # dynamic-workflow scripts (if the run used Workflow)
    └── work/.gitkeep      # workspace copy — stripped in committed examples (see below)
```

> The per-scenario `work/` directory (the run's isolated workspace copy) is **stripped**
> in committed examples and replaced by a single `.gitkeep`: it largely duplicates
> [`data/clawarena-team/`](../data/clawarena-team/) and would bloat the repository.
> Re-run the benchmark to regenerate it. The raw `sessions/*.jsonl` trajectories are
> likewise stripped in committed examples (the rendered `session_*.md` are kept); re-run
> to regenerate the raw logs.

## Included examples

| Directory | Main agent | Serving |
|---|---|---|
| [`local-gemma-31b`](local-gemma-31b/) | Gemma-4-31B-it | local vLLM |
| [`local-qwen3.6-27b`](local-qwen3.6-27b/) | Qwen3.6-27B | local vLLM |

## Submit your own

Open a PR that drops your run directory here. See
[`../docs/submit-to-leaderboard.md`](../docs/submit-to-leaderboard.md) for the full guide.
