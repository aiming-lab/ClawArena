# Submitting a New Result to the Leaderboard

This guide explains how to run a ClawArena evaluation, package the artifacts, and open a Pull Request to add the run to the [Leaderboard in the main README](../README.md#-leaderboard).

## TL;DR

1. Run the full benchmark — 12 scenarios / 337 rounds — with `clawarena run` (or the three-step `infer + score + report`).
2. Place the artifacts under `submissions/<provider>_<model>_<framework>[_<variant>]/{infer,scoring,report}/`.
3. Fork the repo, drop your directory into `submissions/`, and open a PR that includes a summary of `report.md` plus reproduction details.
4. Once a maintainer validates the run, it is merged and added to the README Leaderboard table.

Reference layouts are available under [`result_example/codex_gpt-5.5_openclaw/`](../result_example/codex_gpt-5.5_openclaw/) and [`result_example/vllm_gemma-4-31b-it_openclaw/`](../result_example/vllm_gemma-4-31b-it_openclaw/).

---

## 1. Run the evaluation

### 1.1 Built-in framework

```bash
clawarena run \
  --data data/clawarena/tests.json \
  --frameworks openclaw \
  --out runs/my_submission \
  --provider <provider> \
  --model-id <model-id>
```

When it finishes, `runs/my_submission/openclaw/` contains `infer/`, `scoring/`, and `report/`. That directory is the entire submission payload.

### 1.2 Custom agent (plugin)

If you are evaluating a framework that is not shipped in the repo, write an adapter plugin following the [Plugin Guide](plugin.md), then:

```bash
clawarena run \
  --data data/clawarena/tests.json \
  --frameworks my_agent \
  --plugin path/to/my_agent_plugin.py \
  --out runs/my_submission
```

### 1.3 Step-by-step (optional)

```bash
clawarena check  --data data/clawarena/tests.json --framework openclaw
clawarena infer  --data data/clawarena/tests.json --framework openclaw --out runs/my_submission/openclaw/infer
clawarena score  --infer-dir runs/my_submission/openclaw/infer --out runs/my_submission/openclaw/scoring
clawarena report --data data/clawarena/tests.json --score-dir runs/my_submission/openclaw/scoring --out runs/my_submission/openclaw/report
```

See the [CLI Reference](cli.md) for every option.

---

## 2. Artifact layout

Submission directory name: `<provider>_<model>_<framework>[_<variant>]`

- `provider` — the channel used to call the LLM, e.g. `azure`, `openrouter`, `codex`, `vllm`, `bedrock`, `claude-oauth`.
- `model` — the model ID, preserving the official hyphenation and version, e.g. `gpt-5.5`, `gemma-4-31b-it`, `claude-haiku-4-5`.
- `framework` — the agent harness; must match the value passed to `clawarena run --frameworks`, e.g. `openclaw`, `claude-code`, `nanobot`, `picoclaw`.
- `variant` (optional) — extra modifier such as `metaclaw-skills`, used to disambiguate different configurations of the same model + framework.

The directory must keep the structure produced by `clawarena run`:

```
submissions/<your_dir>/
├── infer/
│   └── <test_id>/<round_id>/infer_result.json
├── scoring/
│   └── <test_id>/<round_id>/scoring.json
└── report/
    ├── report.json
    └── report.md
```

Do not hand-edit `infer_result.json` / `scoring.json` / `report.*`. Submissions must consist of raw CLI output.

---

## 3. Validation checklist

The following must hold before a submission can be merged:

- [ ] `clawarena check --data data/clawarena/tests.json --framework <framework>` passes with no errors.
- [ ] Both `report/report.md` and `report/report.json` exist and were produced by `clawarena report`.
- [ ] The report shows `Tests = 12` and `Rounds = 337`, matching the official `data/clawarena/tests.json`. If `--test-id` was used to filter, you must call this out in the PR description and label the submission as unofficial.
- [ ] The directory name follows the convention in section 2.
- [ ] The PR does not include unrelated artifacts such as debug logs or workspace snapshots.

---

## 4. Metric definitions (see [CLI Reference](cli.md#clawarena-report--generate-report))

All metrics are in the range `[0, 1]` and are shown as percentages in the README:

- **TCR** — Task Completion Rate, mean per-round correctness, macro-averaged across the 12 scenarios. Splits into `MC` (multi_choice) and `EC` (exec_check) sub-scores.
- **SC** — Success Cohesion = `(S − k) / (N − 1)`, rewarding successes that form long unbroken runs.
- **FD** — Failure Dispersion = `1 − (S_fail − k_fail) / (N − 1)`, penalising prolonged failure runs.
- **Robustness** — `SC · FD`, a multiplicative measure of streak health.
- **CRS** — Composite Reliability Score = `(TCR + Robustness) / 2`. This is the primary sort key in the Leaderboard.

---

## 5. PR template

Paste the following block into the Pull Request description (please use markdown, not screenshots, so maintainers can copy the numbers straight into the Leaderboard table):

```markdown
### Submission

- Provider: <provider>
- Model: <model id>
- Framework: <framework>[, variant: <variant>]
- Submission dir: submissions/<dir name>

### Headline metrics (from report/report.md)

| TCR | MC | EC | SC | FD | CRS | Total Tokens |
|---:|---:|---:|---:|---:|---:|---:|
| xx.xx | xx.xx | xx.xx | xx.xx | xx.xx | **xx.xx** | x,xxx,xxx |

### Reproduction

- ClawArena commit: <git rev-parse HEAD>
- CLI version: `clawarena --version`
- tests.json hash: `sha256sum data/clawarena/tests.json`
- Concurrency / timeout / retry: `--concurrency N --timeout S --retry R`
- Other environment notes (GPU, vLLM version, Claude Code Router config, ...)

### Notes

Document any deviation from the default pipeline here: `--overlay` usage, skipped tests, ad-hoc patches, and so on.
```

---

## 6. Maintainer workflow

On a compliant PR, maintainers will:

1. Diff-check the directory name and layout.
2. Load `report/report.json` and verify that `Tests`, `Rounds`, and `CRS` match the numbers in the PR description.
3. Optionally re-run a sample of rounds locally (or in a trusted environment) to confirm reproducibility.
4. Append the submission to the [Leaderboard](../README.md#-leaderboard) and merge the directory into `submissions/`.

For questions on evaluation internals, please read the [CLI Reference](cli.md) and the [Plugin Guide](plugin.md) first, then ping a maintainer in the PR if anything is still unclear.
