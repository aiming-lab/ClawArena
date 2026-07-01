# Running ClawArena-Team Experiments

This guide describes a reproducible workflow for evaluating one or more **main agent**
models on ClawArena-Team. It covers the fixed subagent pool, how to bring up the local
serving endpoints, how to attach the model under test (cloud API or local vLLM), how to
run / resume / summarize evaluations, and the key environment variables.

All commands assume you are in the project root and the CLI is installed
(`pip install -e .` exposes `clawarena-team` plus the short aliases `cateam` and `ca-team`).

---

## 1. Core idea: one fixed subagent pool, shared by every main model

ClawArena-Team measures a **text-only main agent** that must orchestrate a **fixed pool of
local subagents**. Holding the subagent pool constant across every model under test is
what makes scores comparable: differences reflect the main model's management ability,
not a different helper stack.

The pool is defined in `configs/eval_base.yaml`:

| Pool role | Modalities          | Default endpoint           | Served by                     |
|-----------|---------------------|----------------------------|-------------------------------|
| `llm`     | text                | `http://127.0.0.1:8900/v1` | `scripts/serve_gemma-4-31b.py` |
| `vlm`     | text + image + video| `http://127.0.0.1:8900/v1` | `scripts/serve_gemma-4-31b.py` |
| `omni`    | text + image + audio + video | `http://127.0.0.1:8902/v1` | `scripts/serve_gemma-4-omni.py` |

The 31B endpoint (`:8900`) backs both `llm` and `vlm` (the logical split is done by the
`modalities` field, not separate servers). The E4B omni endpoint (`:8902`) handles audio.

The main agent only declares the `text` modality: any image / audio / video content in a
scenario is handled by delegating to the `vlm` / `omni` subagents. This is by design --
it is precisely the management skill under test.

`serve_gemma-4-31b.py` runs the 31B endpoint with **data parallelism** (`--dp 4` by
default): a single endpoint that round-robin load-balances across replicas. A single
evaluation run with `concurrency=1` keeps roughly one replica busy, so the extra replicas
exist to let **several main-model experiments share the same pool** at once (see §5).

> `scripts/serve_qwen3.5-9b.py` is an **optional** lighter-weight alternative llm/vlm pool
> backbone. The default and reference configuration uses the gemma pool above.

---

## 2. Bring up the subagent pool

The serve scripts locate weights under `$CATEAM_MODELS_ROOT` (default `~/models`) and use
the `vllm` binary from `$CATEAM_VLLM_BIN` (default: `vllm` on `PATH`). Set these to match
your machine, then start the two endpoints:

```bash
export CATEAM_MODELS_ROOT=/path/to/models      # holds google/gemma-4-31B-it, etc.
# optional: export CATEAM_VLLM_BIN=/path/to/venv/bin/vllm

# 31B pool (llm + vlm) -- defaults to GPUs 0-3, DP=4, port 8900
nohup python scripts/serve_gemma-4-31b.py > serve_gemma31b.log 2>&1 &

# E4B omni pool (audio) -- defaults to GPU 4, port 8902
nohup python scripts/serve_gemma-4-omni.py > serve_gemma_omni.log 2>&1 &
```

Both scripts accept `--gpus`, `--port`, `--dp`, `--max-model-len`, `--no-spec`,
`--dry-run`, etc. Use `--dry-run` to print the exact `vllm serve` command without
launching. Adjust `--gpus`/`--dp` for your hardware (each DP replica needs one GPU).

### Health check

Wait until both endpoints answer `/v1/models`:

```bash
for p in 8900 8902; do
  curl -s -m5 "http://127.0.0.1:$p/v1/models" >/dev/null && echo ":$p up" || echo ":$p DOWN"
done
```

---

## 3. Attach the model under test (the main agent)

You can point `main` at either a cloud API or a locally served model. The model is passed
to the CLI as a JSON object via `-m/--model` (or `CATEAM_MODEL_JSON`). The subagent pool is
supplied separately by `--config configs/eval_base.yaml`.

A minimal `main` declares text only (non-text is delegated to the pool):

```json
{"main": {"provider": "openai_compat", "model_id": "<id>",
          "api_base": "https://...", "api_key": "...",
          "modalities": {"text": true}, "max_tokens": 24000}}
```

### 3a. Cloud API main

Set the provider fields directly, or use the target registry (§4). Examples:

- **OpenAI-compatible** (OpenRouter, etc.): `provider: openai_compat`, `api_base`,
  `api_key_env: OPENROUTER_API_KEY`.
- **Gemini**: `provider: gemini`, `api_key_env: GEMINI_API_KEY`.
- **Anthropic**: `provider: anthropic`, `api_key_env: ANTHROPIC_API_KEY`.
- **AWS Bedrock Claude**: bridge it to an OpenAI-compatible endpoint with litellm. Export
  `AWS_BEARER_TOKEN_BEDROCK` (and region), edit the model list in
  `scripts/litellm_bedrock.yaml` to the models your account can call, then:

  ```bash
  bash scripts/serve_litellm.sh           # serves :4000, OpenAI-compatible
  ```

  and point `main.api_base` at `http://127.0.0.1:4000/v1`.

Export any `api_key_env` keys in your shell before running, e.g.
`export GEMINI_API_KEY=...  OPENROUTER_API_KEY=...  ANTHROPIC_API_KEY=...`.

### 3b. Local vLLM main

Serve the model under test on a dedicated GPU (separate from the pool) with
`scripts/serve_main_agent.py`, which ships tuned configs for a few candidate models:

```bash
# defaults to GPU 7, port 8910
nohup python scripts/serve_main_agent.py --model gemma-31b > serve_main.log 2>&1 &
until curl -s -m5 http://127.0.0.1:8910/v1/models | grep -q gemma; do sleep 10; done
```

Then set `main.api_base` to `http://127.0.0.1:8910/v1` and `main.model_id` to the
served-name (run with `--dry-run` to see it). Use `--model {gemma-31b|qwen3.6-27b|glm-4.7-flash}`,
`--no-spec` to disable MTP, `--max-model-len` to override context, etc. Because the
candidate local models are large, serve them one at a time on the dedicated GPU.

---

## 4. Target registry (optional convenience)

`scripts/eval_targets.json` is a registry of ready-made `main` definitions, driven by
`scripts/run_eval_targets.py`. It saves you from hand-writing the `-m` JSON and supports a
fast **validation mode** (stop as soon as round `q1` completes) plus a full benchmark
mode.

```bash
python scripts/run_eval_targets.py --list                      # list targets
python scripts/run_eval_targets.py --target gemini-3.5-flash   # q1 validation
python scripts/run_eval_targets.py --group openrouter          # validate a whole group
python scripts/run_eval_targets.py --target codex-gpt-5.5 --full-bench  # full run
```

It reads cloud keys from the environment, finds the CLI via `$CATEAM_BIN` or `PATH`, and
uses `$CATEAM_HOME` (default: the project root) for paths. Each target's dependent service
must be up first (see the registry's `_README`).

---

## 5. Run / resume / summarize with the CLI

The core CLI verbs (use `clawarena-team` or `cateam`):

```bash
# Full run over the merged dataset
clawarena-team run -d data/clawarena-team --config configs/eval_base.yaml \
  -m '<main json>' -o results/exp/<target>

# Run selected scenarios by id (comma-separated) via -t
clawarena-team run -d data/clawarena-team -t s_finance_options_pricing \
  --config configs/eval_base.yaml -m '<main json>' -o results/exp/<target>-one

# Resume only the unfinished scenarios into a fresh output dir
clawarena-team resume -d data/clawarena-team -O results/exp/<target>/<run_id> \
  -o results/exp/<target>-resume --config configs/eval_base.yaml -m '<main json>'

# Dataset stats (scenario/round counts; with -o emits STATS.md + charts)
clawarena-team stats -d data/clawarena-team

# Compare multiple finished reports
clawarena-team compare -r results/exp/a/<run>/report.json \
  -r results/exp/b/<run>/report.json -o results/compare
```

Each run writes `<out>/<run_id>/<scenario>/{evals,sessions,work,metadata.json}` plus a
top-level `report.json` / `report.md`. A scenario counts as complete when its
`metadata.json` exists; `resume` re-runs everything else. Because scenarios are
independent, you can stitch a complete report from several runs with `clawarena-team report`
(see `docs/cli.md`).

The convenience script `scripts/run_all_datasets.sh` runs the wave subsets sequentially
on whatever endpoints are currently up.

---

## 6. Running several experiments in parallel

Because the pool exposes `--dp` replicas and a single `concurrency=1` experiment only
keeps about one replica busy, you can run **multiple main-model experiments concurrently**
against the same pool; vLLM load-balances across the DP replicas.

- Keep `concurrency=1` **inside** each experiment (`-c 1`, the default) -- parallelism
  should happen at the experiment level, not the scenario level.
- Cloud-API mains are the easiest to fan out: launch a batch of them in the background and
  `wait`. A good rule of thumb is to keep the number of concurrent experiments at or below
  the pool's DP replica count to avoid queueing.
- A locally served main occupies its own dedicated GPU and can run **alongside** the
  cloud-API batch, since they all share the same pool. Serve local mains one at a time.
- Give each experiment its own `-o` output directory so results never collide.

Monitor pool load and progress, e.g.:

```bash
# how many engines are actively running on the pool
curl -s 127.0.0.1:8900/metrics | grep num_requests_running | grep -v '#'

# per-target progress (scenario count + success rate)
for r in results/exp/*/*/report.json; do
  python3 -c "import json;d=json.load(open('$r'));print('$r',d.get('scenarios_count'),d.get('avg_task_success_rate'))"
done
```

---

## 7. Key environment variables

Serving / orchestration (used by the scripts in this guide):

| Variable            | Purpose                                                        |
|---------------------|---------------------------------------------------------------|
| `CATEAM_MODELS_ROOT`  | Root dir holding model weights (default `~/models`)           |
| `CATEAM_VLLM_BIN`     | Path to the `vllm` binary (default: `vllm` on `PATH`)         |
| `CATEAM_HOME`         | Project root used by `run_eval_targets.py` (default: repo root) |
| `CATEAM_BIN`          | Path to the `clawarena-team` CLI (default: found on `PATH`)     |
| `CATEAM_BEDROCK_ENV`  | Optional file sourced by `serve_litellm.sh` to set AWS creds  |
| `AWS_BEARER_TOKEN_BEDROCK` | Bedrock auth token (for litellm)                       |
| `GEMINI_API_KEY` / `OPENROUTER_API_KEY` / `ANTHROPIC_API_KEY` | Cloud keys, read from the environment |

CLI / runtime (a frequently used subset; see `docs/cli.md` for the full list):

| Variable                       | Purpose                                                     |
|--------------------------------|-------------------------------------------------------------|
| `CATEAM_MODEL_JSON`              | Fallback value for `--model`                                |
| `CATEAM_PROVIDER_TIMEOUT_SEC`    | Per-request httpx timeout for openai-compat providers (def. 600) |
| `CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC` | Hard total timeout per request (`0` = disabled)          |
| `CATEAM_SCENARIO_RETRY`          | Max attempts per scenario, including the first (default 3)  |
| `CATEAM_SCENARIO_TIMEOUT_SEC`    | Wall-clock hard timeout per scenario (`0` = disabled)       |
| `CATEAM_MAIN_TOKEN_LIMIT` / `CATEAM_SUB_TOKEN_LIMIT` | Token limits for main / subagents         |

> `max_tokens: 24000` is already set per pool entry in `configs/eval_base.yaml` and per
> target in `scripts/eval_targets.json`; it caps runaway generation so a stuck model fails
> within the timeout rather than hanging.
