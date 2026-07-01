# CLI Command Definitions

The entry point is `clawarena-team` (short aliases `cateam` / `ca-team`) (registered after the project is installed); you can also invoke it directly via `python -m clawarena_team.cli`.

## Parameter Precedence

Parameters for all subcommands are merged according to the following precedence (highest to lowest):

1. Explicit CLI flags (`-d`/`--model`/...)
2. The YAML/JSON override file pointed to by `--config`
3. Environment variables (`CATEAM_*`)
4. `src/clawarena_team/configs/default.yaml` (i.e. the "full set of valid parameters" example)
5. The in-code `CODE_DEFAULTS` fallback

`default.yaml` also serves as a complete example: copy it and edit only the items you need to use it as a `--config` input.

## `clawarena-team check`

```
clawarena-team check -d <data_dir> [-t scenario_id_csv] [-s/--strict] [--config path]
```

Strictly validates the dataset structure: missing required fields are errors; extra fields (except in `tests.json`) are errors; missing optional fields are warnings. With `--strict`, warnings are also treated as failures. A non-zero exit code indicates validation failure.

Any `tests.json` that passes this check is guaranteed to be runnable by `clawarena-team run` — that is the contract of `check`.

## `clawarena-team run`

```
clawarena-team run -d <data_dir> -o <out_dir> -m/--model '<json>'
            [-c N | --concurrency N] [-t scenario_id] [--retry N] [--skip-probe]
            [--config path]
```

Runs one complete benchmark: inference + real-time scoring + report.

### `--model` JSON

```json
{
  "main": {
    "provider": "openai_compat",
    "model_id": "gpt-5.4",
    "api_base": "https://...",
    "api_key": "sk-...",
    "modalities": {"text": true, "image": 4}
  },
  "llm":  {"provider": "...", "model_id": "...", "modalities": {"text": true}},
  "vlm":  {"provider": "...", "model_id": "...", "modalities": {"text": true, "image": 8, "video": 2}},
  "omni": {"provider": "...", "model_id": "...", "modalities": {"text": true, "image": 8, "audio": 4, "video": 2}}
}
```

The same string can also be supplied via the environment variable `CATEAM_MODEL_JSON`. If the `main` field is already configured in yaml/env, it may be omitted from the JSON. When `llm`/`vlm`/`omni` are given, they override the default pool entirely.

#### The `modalities` field (can be declared on every entry)

Declares which content types the model "claims" it can consume directly, **and explicitly specifies a count cap for each non-text modality**. `text` is always implicitly included. The allowed set is `{"text", "image", "audio", "video"}`.

Two forms:

- **dict (recommended)**: `{"text": true, "image": 4, "video": 1}` — keys are modalities, and the value for any non-`text` key is the **cap on the number of most-recent attachments of that modality retained in context** (a positive integer). When exceeded, the oldest attachments are stripped to text placeholders and the most recent N are kept (aligned with claude-code's `stripExcessMediaItems` strip-oldest-first), and a `<system-reminder>` listing the stripped files is appended to the next tool result; the agent can re-Read to retrieve them. This cap must be **≤ the corresponding serving `--limit-mm-per-prompt`**, thereby completely avoiding accumulated historical multimodal content hitting the server-side limit and being rejected with a 400.
- **list (legacy / backward-compatible)**: `["text", "image"]` — no count caps; **the probe stage will error out due to the missing caps**, forcing a switch to the dict form for explicit declaration.

> probe validation: after probe-based trimming, every still-effective non-text modality must have a positive-integer cap, otherwise it exits with `modality probe failed`. `--skip-probe` skips this validation (debugging only).

Rules applied per pool type (static trimming at init, followed by probe-based empirical trimming):

| Pool | Must include | Allowed | Rule |
|---|---|---|---|
| `main` | text | text/image/audio/video | All take effect; audio/video only warn, not removed |
| `llm`  | text | text | Declaring other items → warn and remove, keeping only text |
| `vlm`  | text+image | text/image/video | audio → warn and remove; missing video → warn but keep usable items |
| `omni` | text+audio | text/image/audio/video | All declarations take effect, no warning |

The final effective set is recorded in `metadata.json.models.pool[*].effective_modalities`, and drives the generation of the Read tool and CreateSubagent tool descriptions.

### Other Parameters

- `-c/--concurrency`: scenario parallelism, default 1.
- `-t/--scenario-id`: run only the specified scenario.
- `-m/--model`: see above.
- `--retry N`: maximum number of attempts per scenario (including the first), default 3 (`scenario.retry`). Only retries on execution-time exceptions (provider errors, etc.); a check failure is a normal result and is not retried. Each retry rebuilds work/sessions/evals and is idempotent. If it still fails after exhausting retries, the scenario is skipped (it can be backfilled by `clawarena-team resume`) without dragging down the entire run.
- `--skip-probe`: skip the init-time modality empirical test (for debugging; do not use in production).
- `--config`: custom yaml/json override file.

### Output Layout

```
<out_dir>/<run_id>/
├── <scenario_id>/
│   ├── session_main.md
│   ├── session_<sub_id>_<sess>.md
│   ├── sessions/
│   ├── evals/
│   ├── work/
│   └── metadata.json
├── report.json
└── report.md
```

## `clawarena-team resume`

```
clawarena-team resume -d <data_dir> -O <old_run_path> -o <new_run_path> -m/--model '<json>'
               [-c N] [--retry N] [--skip-probe] [--config path]
```

Re-runs only the unfinished scenarios. `-O/--old` receives the output **path** of the previous run (not the run id); `-o/--out` must not exist and will be created. Criterion: if any `<run_id>/<scenario_id>/metadata.json` exists under the old directory, that scenario is considered finished and its results are copied to the new directory; otherwise the half-finished artifacts are discarded and the scenario is re-run.

## `clawarena-team report`

```
clawarena-team report -i <results_dir> [-i <results_dir> ...] -o <out_dir>
               [--run-id NAME] [-d <data_dir>]
```

**Stitches and regenerates** `report.json` + `report.md` from the `metadata.json` files of finished scenarios, using the same `build_run_report` logic that `clawarena-team run` uses at finalization.

- **Finished criterion**: the scenario result root directory contains `metadata.json` (written by scenario_runner only after all of that scenario's background subagents have finalized; failed/unfinished scenarios do not have it). **Note**: this command only checks whether `metadata.json` exists; it **does not judge whether the API errored** — the latter requires separate manual inspection.
- **Stitching**: because scenarios are independent of one another, you can stitch a complete test run from finished scenarios across **different runs** (the original plus multiple `resume`/re-runs). `-i` can be repeated and recursively scans all `metadata.json` files beneath it; when the same `scenario_id` appears in multiple copies, the one with the latest `finished_at` is kept (and the output lists which scenarios came from multiple runs).
- `--run-id` is only used as a label in the report (default `stitched`).
- `-d/--data` is optional: if a dataset directory is given, it additionally reports **coverage** (`N/41` scenarios) and lists missing scenarios, making it easy to determine which ones still need to be backfilled.

Typical usage (a given model is scattered across multiple runs, stitched into one complete 41-scenario run before generating the report):

```
clawarena-team report -i results/exp/codex-gpt-5.4 -o results/final/codex-gpt-5.4 \
               --run-id codex-gpt-5.4 -d data/clawarena-team
```

## `clawarena-team stats`

```
clawarena-team stats -d <data_dir> [-o <out_dir>] [-t tokenizer_source] [--config path]
```

- Without `-o`, prints a brief summary (number of scenarios / number of rounds) to stdout.
- With `-o`, outputs a complete `STATS.md` + a set of `chart_*.png` (rendered by matplotlib).
- `-t/--tokenizer` overrides `tokenizer.source`; accepts an HF repo id / short name / local path.

## `clawarena-team clean`

```
clawarena-team clean -o <out_dir> [-t targets_csv] [--config path]
```

`-t/--targets` accepts `work` / `logs` / `sessions` / `all`, comma-separated, default `work`. Recursively deletes matching items by directory name.

## `clawarena-team compare`

```
clawarena-team compare -r <report.json> -r <report.json> [-r ...] -o <out_dir> [--config path]
```

Takes multiple `report.json` files (at least two, each corresponding to the output of one `clawarena-team run`), sorts them by **SMS** descending, and emits `<out_dir>/comparison.json` and `comparison.md`.

`comparison.md` is structurally isomorphic to `report.md`:

1. **Composite & Scored — by run**: one row per run, listing SMS / TCS / MQS / TCR / SCR / SFR / TPS / ROS / WPS / MCS / Pass.
2. **Statistics — by run**: one row per run, listing SUB / MKD / INV / TGC / MAF / SAFt / SAFa / MTT / MTP / SST / SLT.
3. **SMS — per scenario × run**: a scenario_id × run label pivot table, making it easy to see which run is stronger on which scenario.
4. **Notation**: the full meaning and formula of every abbreviation.

Composite scoring system:

```
SMS = 0.5 · TCS + 0.5 · MQS              Subagent Management Score (final composite score)
TCS = (TCR + SCR + SFR) / 3              Task Correctness Subscore
MQS = mean over scenarios of (TPS+ROS+WPS+MCS)/4   Management Quality Subscore
```

`report.md` also uses the same abbreviation system and provides a Notation section at the end; for detailed formulas, see the Notation section at the end of `report.md`.

## `clawarena-team test`

Equivalent to `pytest tests/`; pytest arguments can be passed through.

## Supported Environment Variables

| Variable | Effect |
|---|---|
| `CATEAM_MODEL_JSON` | Fallback value for `--model` |
| `CATEAM_MAIN_<FIELD>` | Single-field override for the main agent (`FIELD` ∈ `PROVIDER`/`MODEL_ID`/`API_BASE`/`API_KEY`/`API_KEY_ENV`/`MODALITIES`) |
| `CATEAM_MODEL_<KEY>_<FIELD>` | Single-field override for a pool entry (`KEY` ∈ `LLM`/`VLM`/`OMNI`) |
| `CATEAM_MAIN_TOKEN_LIMIT` | main agent token cap |
| `CATEAM_SUB_TOKEN_LIMIT` | subagent token cap |
| `CATEAM_BASH_TIMEOUT` | bash tool default timeout (seconds) |
| `CATEAM_LOG_LEVEL` | Log level |
| `CATEAM_TOKENIZER` | tokenizer source |
| `CATEAM_CHAT_TEMPLATE` | chat template source |
| `CATEAM_FINAL_FEEDBACK_MODE` | `skip` / `extra_turn` / `cross_scenario` |
| `CATEAM_SCENARIO_RETRY` | Maximum number of attempts per scenario (including the first), default 3 |
| `CATEAM_SCENARIO_TIMEOUT_SEC` | Per-scenario wall-clock hard timeout (seconds), `0`=disabled (default). When >0, wraps the entire scenario with `asyncio.wait_for`: on heavy/very-long-context scenarios, some models permanently hang at unbounded await points — provider slow streaming, in-turn `asyncio.gather` parallel subagents, or `wait_for_backgrounds` (GPU at 0%, runlog making zero progress) — which a single-point timeout cannot catch; this wall-clock fallback timeout cancels the scenario → does not write metadata.json → cleanly marks it failed and lets it be backfilled by `clawarena-team resume`, while the remaining scenarios still flow into the report normally. Must be > the legitimate duration of the slowest model's heavy scenario on that hardware (a slow local model can take hours on a single scenario), otherwise it will kill slow-but-normal scenarios by mistake |
| `CATEAM_PROVIDER_TIMEOUT_SEC` | The httpx timeout for a single request from the openai-compat provider (seconds), default 600. Note this is httpx's **per-socket-read** timeout — if upstream trickles bytes intermittently (e.g. ChatMock buffering a reasoning model's streaming output) it keeps resetting it, so the full request body never completes and the read timeout never fires; this needs the next item, a total time limit, as a backstop |
| `CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC` | The **total time limit** for a single request from the openai-compat provider (seconds), `0`=disabled (default, preserving the original semantics). When >0, uses `asyncio.wait_for` to put a real total time limit on every `client.post`: when upstream stalls (a trickle-stall that the per-read timeout cannot catch), it times out, cancels the request, and retries with backoff as a retryable transient error, instead of main freezing the whole scenario permanently at `ep_poll`. Should be > the legitimate slowest single-response duration, otherwise it will kill slow-but-normal requests by mistake |
| `CATEAM_PROVIDER_MAX_RETRIES` | Bounded retry count for provider transport-layer errors / 5xx / total-timeout timeouts (including the first), default 3; 4xx is not retried |
| `CATEAM_PROVIDER_RATELIMIT_RETRIES` | Independent retry budget for 429 rate limiting, default 8 (not counted toward `MAX_RETRIES`, prioritizes honoring `Retry-After`) |
| `CATEAM_BACKGROUND_WAIT_TIMEOUT_SEC` | Wall-clock timeout for `wait_for_backgrounds` waiting for background subagents to finalize (seconds), default 900; on timeout, cancels the pending backgrounds and marks the scenario failed, which can be retried via resume |
| `CATEAM_PROBE_ENABLED` | `0`/`false` disables init probing |
| `CATEAM_PROBE_TIMEOUT` | Single-probe timeout (seconds) |

In environment variables, the `modalities` field is comma-separated (e.g. `CATEAM_MODEL_VLM_MODALITIES=text,image,video`) — this is the **list form, without count caps**, and for a pool containing non-text modalities it will error at the probe stage due to the missing caps; to give per-modality caps, use the dict form of the `--model` JSON or yaml instead (`{text: true, image: N, ...}`).

## ReadTool Large-File Thresholds

The `read:` section of `configs/default.yaml` provides two thresholds:

| key | Default | Behavior |
|---|---|---|
| `read.notice_bytes` | 32 KiB | File ≥ this value and no `offset`/`limit` passed → a `[notice: ...]` line is prepended to the result, suggesting pagination or delegating to an llm subagent |
| `read.hard_bytes` | 256 KiB | File ≥ this value and not paginated → errors out directly, with delegation guidance attached |
| `read.max_text_bytes` | 512 KiB | Final read cap (truncation protection; under normal conditions `hard_bytes` is triggered first) |

These three thresholds cannot yet be overridden directly via `--config /path/to.yaml` or env (`CATEAM_*`); you can edit the `read:` section in the `--config` file.

## Scenario Asset Guidance

On its first turn, the main agent sees `_sandbox_hint.md` (if the workspace contains this file and it is covered by `main_agent_accessible_paths`), which tells it where the large assets are and the suggested `model_key`. When long documents are split by chapter/article, an `_index.md` is provided alongside; after reading the index, the main agent can pick chapters to delegate to llm subagents. For the detailed specification, see the "Asset Guidance" subsection of `docs/dataset.md`.
