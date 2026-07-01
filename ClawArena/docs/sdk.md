# ClawArena Python SDK

ClawArena can be used as a Python library in addition to the `clawarena` CLI. The
`ClawArena` class exposes every CLI command as a method, so you can drive the full
benchmark pipeline — inference, scoring, reporting, comparison, stats — directly
from Python.

```python
from clawarena import ClawArena

ca = ClawArena(
    data="clawarena-real",            # dataset name or path to a tests.json
    out="results",
    concurrency=8,
    timeout=600,
    model={"provider": "anthropic", "model_id": "claude-opus-4-8"},
)

ca.check(framework="clawarena-native")
infer_dir = ca.infer("clawarena-native", out="results/run1")
ca.score(infer_dir)
ca.report(infer_dir / "score")
ca.run(["openclaw", "clawarena-native"], test_id="eng1")
ca.stats(framework="openclaw", out="results/stats")
```

---

## 1. Installation

```bash
# From a Git checkout (bundles the datasets — see Installation Guide)
pip install git+https://github.com/aiming-lab/ClawArena.git

# Or, in a local checkout
pip install -e .
```

After installation, `import clawarena` exposes `ClawArena`, `download_data`, and
`data_root`. See the [Installation Guide](installation.md) for how the benchmark
data is bundled or fetched on demand.

---

## 2. Configuration model

Configuration is split into two layers:

- **Common config** — passed to the `ClawArena(...)` constructor and shared by all
  methods.
- **Per-call config** — passed to a method (`run`, `infer`, `stats`, …) to override
  the instance default for that call only.

The override rule mirrors the CLI: **an explicit method argument wins over the
instance default, which wins over each core function's built-in default.** A method
argument left unset inherits the instance value.

### 2.1 Constructor (`ClawArena.__init__`)

| Parameter     | Type                          | Default        | Description |
|---------------|-------------------------------|----------------|-------------|
| `data`        | `str \| Path \| None`         | `None`         | Default dataset. A `tests.json` path, a dataset directory, or a bare dataset name (resolved via `data_root()`). |
| `out`         | `str \| Path \| None`         | `None`         | Default output directory. |
| `concurrency` | `int`                         | `4`            | Parallel test workers. |
| `timeout`     | `float`                       | `300`          | Per-test timeout (seconds). |
| `retry`       | `int`                         | `1`            | Retry attempts per test. |
| `model`       | `dict \| ModelConfig \| None` | `None`         | Default model override (see [§4](#4-model-configuration)). |
| `overlay`     | `str \| None`                 | `None`         | JSON string overriding `metaclaw` / `mm_metaclaw` sections of `tests.json`. |
| `plugins`     | `list[str] \| str \| None`    | `None`         | External adapter plugin `.py` files, loaded once at construction. |
| `tokenizer`   | `str`                         | `cl100k_base`  | Tokenizer for `stats`. |

### 2.2 Override example

```python
ca = ClawArena(data="clawarena-real", out="results", concurrency=4, timeout=300)

# Inherits concurrency=4, timeout=300 from the instance:
ca.run("clawarena-native")

# Overrides concurrency for this call only; timeout still inherited:
ca.run("clawarena-native", concurrency=16)
```

---

## 3. Methods

Each method maps one-to-one to a CLI command. Method arguments that default to the
instance value are marked *(inherits)*.

### `check(*, framework=None, test_id=None, strict=False, data=(inherits)) -> bool`
Validate dataset integrity. Returns `True` if all checks pass. `framework` and
`test_id` accept a comma string or a list.

### `infer(framework, *, out=(inherits), test_id=None, concurrency=(inherits), timeout=(inherits), retry=(inherits), model=(inherits), overlay=(inherits), data=(inherits)) -> Path`
Run agent inference for one framework. Returns the directory the results were
written to. If the chosen output directory is non-empty, results land in a unique
`infer_<hash>` subdirectory (same behaviour as the CLI).

### `resume_infer(framework, infer_dir, state_dir, *, workspace_dir=None, concurrency=(inherits), timeout=(inherits), retry=(inherits), inplace=False, data=(inherits)) -> None`
Resume an interrupted inference run from existing results/state/workspace dirs.

### `score(infer_dir, *, out=None) -> None`
Score inference results. `out=None` scores in place.

### `report(score_dir, *, out=(inherits), data=(inherits)) -> None`
Generate a report from scoring results.

### `compare(reports, *, out=(inherits)) -> None`
Compare two or more `report.json` files.

### `run(frameworks, *, out=(inherits), test_id=None, concurrency=(inherits), timeout=(inherits), retry=(inherits), clean_temp=False, model=(inherits), overlay=(inherits), data=(inherits)) -> None`
Run the full pipeline (infer → score → report, plus compare for multiple
frameworks). `frameworks` accepts a comma string or a list.

### `clean(*, out=(inherits), targets=None) -> None`
Remove temporary files. `targets` accepts `"work"`, `"logs"`, `"all"` (comma string
or list).

### `stats(*, framework=None, out=(inherits), tokenizer=(inherits), data=(inherits)) -> None`
Generate token and structural statistics. `framework=None` covers every framework
in `tests.json`.

### Async variants
`infer` and `resume_infer` are synchronous wrappers around the coroutines
`ainfer(...)` and `aresume_infer(...)`. Use the async forms when you are already
inside an event loop:

```python
infer_dir = await ca.ainfer("clawarena-native", out="results/run1")
```

---

## 4. Model configuration

The `model` parameter accepts either a `ModelConfig` instance or a plain dict:

```python
ClawArena(model={
    "provider": "anthropic",      # default "openai"
    "model_id": "claude-opus-4-8",  # required ("model" is also accepted)
    "api_base": "https://...",    # optional
    "api_key": "sk-...",          # optional; prefer environment variables
    "extra": {"reasoning": True}, # optional ("model_config" is also accepted)
})
```

Resolution follows the same precedence chain as the CLI:

```
method/instance model  >  environment variables (CLAWARENA_MODEL_ID / _PROVIDER /
                          _API_BASE / _API_KEY)  >  tests.json frameworks[fw].model
                          >  tests.json top-level model
```

See the [Provider Guide](provider-usage-guide.md) for the full list of providers
and per-provider field semantics.

---

## 5. Data access

The SDK resolves benchmark data through `data_root()`, in priority order:

1. `CLAWARENA_DATA_DIR` environment variable.
2. Data bundled inside the installed package (`clawarena/_data`).
3. The source-tree `data/` directory (when running from a checkout).
4. The download cache (`~/.cache/clawarena/data`).

```python
from clawarena import data_root
print(data_root())  # -> directory containing clawarena/, clawarena-real/, ...
```

### Downloading datasets

For a code-only install (e.g. from PyPI) you can fetch datasets on demand. You can
target a single dataset, which is useful when a dataset is updated independently.

```python
from clawarena import download_data

download_data()                          # all datasets
download_data(["clawarena-real"])        # one dataset
download_data(["clawarena"], ref="v1.0.0", force=True)
```

The equivalent CLI command:

```bash
clawarena fetch-data --list                       # list remote datasets
clawarena fetch-data --dataset clawarena-real     # download one
clawarena fetch-data                              # download all
```

Downloads use a sparse checkout that fetches only `data/<dataset>`, so unrelated
top-level directories are never downloaded.

---

## 6. CLI parity

The `clawarena` CLI is a thin wrapper: every command constructs a `ClawArena`
instance and calls the corresponding method. The CLI and SDK therefore share
identical behaviour and override semantics. See the [CLI Reference](cli.md) for the
command-line form of each method.
