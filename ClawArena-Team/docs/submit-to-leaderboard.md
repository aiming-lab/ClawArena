# Submitting a New Result to the Leaderboard

This guide explains how to run a ClawArena-Team evaluation, package the artifacts, and open a
Pull Request to add the run to the [Leaderboard in the main README](../README.md#-leaderboard).

## TL;DR

1. Run the full benchmark — 41 scenarios / 258 rounds — with `clawarena-team run`.
2. Place the output directory under `submissions/<provider>-<model>/`.
3. Strip each `s_<scenario>/work/` directory (replace its contents with a `.gitkeep`) to keep the repo small.
4. Fork the repo, drop your directory into `submissions/`, and open a PR summarizing `report.md`.
5. Once a maintainer validates the run, it is merged and added to the README Leaderboard.

Reference layouts: [`submissions/local-gemma-31b/`](../submissions/local-gemma-31b/) and
[`submissions/local-qwen3.6-27b/`](../submissions/local-qwen3.6-27b/).

---

## 1. Run the evaluation

```bash
# Validate first — anything that passes check is guaranteed to run
clawarena-team check -d data/clawarena-team/

# Run the full benchmark (inference + live scoring + report)
clawarena-team run -d data/clawarena-team/ -o runs/my_submission --model '<model-json>'
```

`runs/my_submission/` then contains `report.json`, `report.md`, and one `s_<scenario>/`
directory per scenario. That directory is the entire submission payload. See the
[CLI reference](cli.md), the [`--model` JSON format](cli.md#--model), and
[running experiments](running-experiments.md) for every option and for serving the fixed
subagent pool.

If a run was interrupted, finish only the missing scenarios with
`clawarena-team resume -O runs/my_submission -o runs/my_submission_v2 --model '<model-json>'`.

---

## 2. Artifact layout

Submission directory name: `<provider>-<model>`

- `provider` — how the main agent is served, e.g. `local` (vLLM), `codex`, `bedrock`, `or` (OpenRouter), `gemini`.
- `model` — the model ID, preserving official hyphenation and version, e.g. `gemma-31b`, `qwen3.6-27b`, `gpt-5.5`, `claude-fable-5`.

Keep the structure produced by `clawarena-team run`:

```
submissions/<provider>-<model>/
├── report.json            # raw scores — do not hand-edit
├── report.md              # regenerate with `clawarena-team report` if needed
└── s_<scenario>/
    ├── metadata.json
    ├── sessions/*.jsonl    # raw trajectories
    ├── session_*.md        # rendered trajectories
    ├── evals/*.json
    ├── workflows/
    └── work/.gitkeep       # see step 3
```

`report.json` / `metadata.json` / `evals/*.json` must be raw CLI output — do not hand-edit them.
You may regenerate `report.md` (and re-stitch `report.json`) from the per-scenario
`metadata.json` without re-running inference:

```bash
clawarena-team report -i submissions/<provider>-<model> -o submissions/<provider>-<model> --run-id <provider>-<model>
```

---

## 3. Strip the workspace copies

Each `s_<scenario>/work/` is the run's isolated copy of the scenario workspace; it largely
duplicates [`data/clawarena-team/`](../data/clawarena-team/). To keep the submission
small, remove its contents (leave a single `.gitkeep`) and, optionally, drop the raw
`sessions/*.jsonl` logs (the rendered `session_*.md` stay):

```bash
for wd in submissions/<provider>-<model>/s_*/work; do
  find "$wd" -mindepth 1 -delete
  echo "Workspace files removed: they duplicate data/clawarena-team/; re-run to regenerate." > "$wd/.gitkeep"
done
# optional: drop raw trajectories, keep the rendered session_*.md
find submissions/<provider>-<model> -type d -name sessions -prune -exec rm -rf {} +
```

---

## 4. Open the Pull Request

Fork, add `submissions/<provider>-<model>/`, and open a PR including:

- the headline numbers from `report.md` (the **Paper metrics** section: SMS, TCR, TPP, ROC, WPP, MCA);
- how the main agent was served and the exact `--model` JSON;
- any deviations from the standard setup.

A maintainer validates the run and adds it to the README Leaderboard.
