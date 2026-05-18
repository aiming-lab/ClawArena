# clawarena CLI Reference

clawarena is a multi-framework AI Agent benchmark evaluation platform. It provides a unified interface for running benchmarks across different agent frameworks.

## Installation

```bash
pip install -e .
```

## Commands

### `clawarena check` — Validate Data Integrity

Validates that all data files are properly structured and consistent before running the benchmark.

```bash
clawarena check --data <tests.json>
             [--framework <names>]    # Comma-separated (default: all)
             [--test-id <ids>]        # Comma-separated (default: all)
             [--strict]               # Treat warnings as errors
             [--plugin <path>...]     # External adapter plugin .py files
```

Performs two levels of validation:
1. **Generic checks (G-001 to G-006)**: tests.json structure, eval directory, questions.json format
2. **Framework-specific checks**: manifest structure, session files, workspace integrity, update file completeness

**Plugin loading**: Frameworks shipped inside clawarena are registered automatically. To validate an externally-defined framework (e.g. one provided by another project), pass its plugin path via `--plugin`; without it, framework-specific checks for that framework are skipped with a warning. Example:

```bash
clawarena check --data data/tests.json --framework aha \
                --plugin /path/to/aha/clawarena_plugin.py
```

### `clawarena infer` — Run Agent Inference

Executes the agent on all test scenarios, producing `infer_result.json` files.

```bash
clawarena infer --data <tests.json>
             --framework <name>       # Single framework (e.g., "openclaw")
             --out <path>             # Output directory
             [--test-id <ids>]        # Comma-separated (default: all)
             [--concurrency <n>]      # Parallel tests (default: 4)
             [--timeout <seconds>]    # Per-agent timeout (default: 300)
             [--retry <n>]            # Retry count (default: 1)
             [--plugin <path>...]     # External adapter plugin .py files
             [--overlay <JSON>]       # Shallow-merge override for metaclaw fields in tests.json
             [--provider <name>]      # LLM provider override
             [--model-id <id>]        # Model name override
             [--api-base <url>]       # API endpoint override
             [--api-key <key>]        # API key override
             [--model-config <JSON>]  # Extra model-entry fields forwarded to framework config
```

**Output behavior**: If `--out` directory exists and is non-empty, creates an `infer_<uuid>` subdirectory.

**Output structure**:
```
<out>/
└── <test_id>/
    └── <round_id>/
        └── infer_result.json
```

### `clawarena resume-infer` — Resume Interrupted Inference

Resumes an interrupted `infer` run by reusing existing results, state, and workspace directories. Completed rounds are skipped; only pending rounds are executed.

```bash
clawarena resume-infer --data <tests.json>
                    --framework <name>
                    --out <path>              # Existing infer results directory (written in-place)
                    -S/--state-dir <path>     # Existing state directory (e.g. state_20240101_120000)
                    [-W/--workspace-dir <path>]  # Existing workspace directory
                    [--concurrency <n>]
                    [--timeout <seconds>]
                    [--retry <n>]
                    [-i/--inplace]            # Use original state/workspace dirs in-place (backup first)
                    [--plugin <path>...]
```

**Skip logic**: For each test scenario, all rounds that already have `infer_result.json` are skipped. Their scores are loaded from disk to provide correct feedback context for subsequent rounds. A scenario where all rounds are complete is skipped entirely.

**State continuity**: The provided `--state-dir` must be the same directory used by the original run (e.g. `manifest_dir/work/state_<timestamp>`). Session JSONL files already contain prior conversation history, so `--framework claude-code` resumes the session transparently.

**Example**:
```bash
clawarena resume-infer \
  --data data/clawarena/tests.json \
  --framework claude-code \
  --out results/hil_test/claude-code \
  -S data/clawarena/claude-code/work/state_20240101_120000 \
  -W data/clawarena/claude-code/work/workspaces_20240101_120000
```

### `clawarena score` — Score Infer Results

Scores all `infer_result.json` files against ground truth from `questions.json`.

```bash
clawarena score --infer-dir <path>       # Directory with infer results
             [--out <path>]           # Output directory (default: in-place)
```

Does not require `--data` or `--framework` — scoring reads `eval_question_path` from each `infer_result.json` to locate the corresponding `questions.json`.

### `clawarena report` — Generate Report

Aggregates scoring results into `report.json` and `report.md`.

```bash
clawarena report --data <tests.json>     # Required: tests.json (used to pull
                                         #   the canonical round order from
                                         #   eval/<sid>/questions.json so streak
                                         #   metrics reflect true sequence)
              --score-dir <path>      # Directory with scoring.json files
              --out <path>            # Report output directory
```

Headline metrics (range `[0, 1]`):

- **TCR** — Task Completion Rate (per-round mean correctness, macro-averaged across tests).
- **SC** — Success Cohesion `(S − k) / (N − 1)` over success run-lengths.
- **FD** — Failure Dispersion `1 − (S_fail − k_fail) / (N − 1)` over failure run-lengths.
- **Robustness** — `SC · FD` (multiplicative streak health).
- **CRS** — Composite Reliability Score `(TCR + Robustness) / 2`.

Always generates both `report.json` (machine-readable) and `report.md` (human-readable).

### `clawarena compare` — Compare Frameworks

Compares report results across multiple frameworks.

```bash
clawarena compare --reports <path> [<path>...]   # report.json files (>=2)
               --out <path>                   # Comparison output directory
```

Generates `comparison.json` and `comparison.md` with per-test score comparisons.

### `clawarena run` — Full Pipeline

Runs the complete pipeline: infer → score → report (→ compare for multiple frameworks).

```bash
clawarena run --data <tests.json>
           --frameworks <names>       # Comma-separated framework names
           --out <path>               # Top-level output directory
           [--test-id <ids>]          # Comma-separated (default: all)
           [--concurrency <n>]
           [--timeout <seconds>]
           [--retry <n>]
           [--plugin <path>...]       # External adapter plugin .py files
           [--clean-temp]             # Clean temp files after run
           [--overlay <JSON>]         # Shallow-merge override for metaclaw fields in tests.json
           [--provider <name>]        # LLM provider override
           [--model-id <id>]          # Model name override
           [--api-base <url>]         # API endpoint override
           [--api-key <key>]          # API key override
           [--model-config <JSON>]    # Extra model-entry fields forwarded to framework config
```

**Output structure** (even for single framework):
```
<out>/
├── openclaw/
│   ├── infer/
│   ├── scoring/
│   └── report/
│       ├── report.json
│       └── report.md
└── comparison/           # Only when >=2 frameworks
    ├── comparison.json
    └── comparison.md
```

### `clawarena clean` — Clean Temporary Files

Removes work copies and log directories.

```bash
clawarena clean --out <path>             # Target output directory
             [--targets <names>]      # Comma-separated: work, logs, all (default: all)
```

### `clawarena stats` — Benchmark Statistics

Comprehensive structural and token analysis of a benchmark dataset. When
`--framework` is omitted, every framework registered in `tests.json` is
analysed (multi-framework runs land under `<out>/<fw>/`, single-framework
runs land directly in `<out>`).

```bash
clawarena stats --data <tests.json>
             --out <path>             # Output directory
             [--framework <name>]     # Single framework (default: all registered)
             [--tokenizer <name>]     # Tokenizer (default: cl100k_base)
```

Supports tiktoken encoding names (e.g., `cl100k_base`) and HuggingFace model IDs.
The chosen tokenizer is recorded at the top of the generated `STATS.md`.

**Token categories (8)** — per-framework layouts (`stats/layouts/`) ensure
session-equivalent files transcribed into the workspace are classified as
session content rather than double-counted:

- `main_session`, `history_sessions`
- `workspace`
- `questions`, `feedback`, `pref`
- `update_session`, `update_workspace`

**Structural statistics** (parsed directly from `questions.json` + `manifest.json`):

- Round counts and per-type distribution (`multi_choice` / `exec_check`)
- MC shape: options & answers per question (mean / min / max + histograms,
  single- vs multi-answer split)
- EC features: `expect_exit` / `expect_stdout` / regex / `timeout` coverage
- Pref coverage, update coverage, files-per-update, update-action distribution
- Per-scenario breakdown + Top-N rankings

**Outputs**: `STATS.md` plus up to 13 `chart_*.png` figures (charts whose
underlying data is empty are skipped).

## Environment Variables

| Variable | Values | Description |
|---|---|---|
| `OMIT_WORKSPACE` | `0` | Enable workspace file existence warnings during `clawarena check`. By default workspace checks are **skipped** because workspace files may be created by the agent at runtime. Set `OMIT_WORKSPACE=0` to opt in to warnings for any `${workspace}/...` path referenced in `exec_check` commands that does not exist in the static workspace snapshot. Warnings do **not** cause check to fail unless `--strict` is also passed. |

**Example**:

```bash
# Enable workspace existence warnings
OMIT_WORKSPACE=0 clawarena check --data data/clawarena/tests.json

# Also fail on warnings
OMIT_WORKSPACE=0 clawarena check --data data/clawarena/tests.json --strict
```

## Data Format

### tests.json

```json
{
  "name": "Benchmark",
  "eval_dir": "eval",
  "frameworks": {
    "openclaw": { "manifest": "openclaw/manifest.json" }
  },
  "tests": [
    { "id": "trace_s1", "desc": "...", "eval": "trace_s1" }
  ]
}
```

### questions.json

```json
{
  "rounds": [
    {
      "id": "r1",
      "type": "multi_choice",
      "question": "...",
      "update_ids": [],
      "eval": { "options": {...}, "answer": ["A"] }
    }
  ]
}
```

### Framework Manifest (openclaw/manifest.json)

```json
{
  "framework": "openclaw",
  "config_file": "config/openclaw.json",
  "state_dir": "state",
  "agents": {
    "trace_s1": {
      "agent_id": "trace_s1",
      "agent_dir": "state/agents/trace_s1",
      "session": "main_...",
      "history_sessions": ["..."],
      "workspace": "workspaces/trace_s1"
    }
  },
  "updates": {
    "trace_s1": {
      "upd_r4_sessions": {
        "type": "session",
        "dir": "updates/trace_s1/upd_r4_sessions",
        "files": ["file1.jsonl", "file2.jsonl"]
      }
    }
  }
}
```
