# Dataset Format Definition

Dataset root directory layout (merged dataset `data/clawarena-team/`):

```
data/clawarena-team/
├── tests.json            # Full set: 41 scenarios
├── manifests.json        # id → manifest path mapping for all 41 scenarios
└── scenarios/<scenario_id>/
    ├── manifest.json
    ├── questions.json
    ├── workspace/
    ├── updates/
    └── checks/
```

**Dataset composition**: all 41 scenarios live under a single `scenarios/` directory in `clawarena-team`, sharing one `manifests.json` and one `tests.json`. The set spans 41 independent domains. (An early `wave2` iteration was later superseded by the nine-dimension `wave3` and is intentionally not included.)

**Running selected scenarios**: pass `-t/--scenario-id <id1,id2,...>` to limit a `run`/`check` to specific scenarios. To run a custom subset, author your own `tests-*.json` next to `tests.json` and point at it with `--tests <file>` (`load_dataset(data_dir, tests_filename=...)`, CLI `clawarena-team run/resume/stats --tests <file>`, default `tests.json`). `clawarena-team check` validates the entire library structure.

**Path conventions**: every path field in the JSON is filled in as a path **relative to that file's own location**; after loading, the harness uniformly resolves them to local absolute paths and never writes absolute paths back to disk.

## tests.json

| Field | Required | Meaning |
|---|---|---|
| `name` | ✓ | Test set name |
| `desc` |   | Description |
| `manifests_ref` | ✓ | Relative path to manifests.json |
| `scenario_ids` | ✓ | The subset of scenario ids enabled for this test set |

The **only** file allowed to contain extra fields (custom subsets, notes, debug markers are all permitted).

## manifests.json

```json
{
  "scenarios": {
    "<scenario_id>": "<path to manifest.json relative to manifests.json>"
  }
}
```

`model_pool` (subagent candidate models `llm`/`vlm`/`omni`) is **no longer written into manifests.json**; defaults are now provided by `src/clawarena_team/configs/default.yaml`, with runtime precedence (highest to lowest):

1. CLI `--model` JSON: if any of the `llm`/`vlm`/`omni` keys is given, it overrides that entry entirely;
2. The yaml/json override file pointed to by `-c/--config`;
3. Environment variable `CATEAM_MODEL_<KEY>_<FIELD>` (KEY ∈ `LLM`/`VLM`/`OMNI`, FIELD ∈ `PROVIDER`/`MODEL_ID`/`API_BASE`/`API_KEY`/`API_KEY_ENV`/`NAME`/`MODALITIES`): overrides a single field; `MODALITIES` is comma-separated;
4. The `model_pool` section in `default.yaml`: fallback.

When the pool is exposed to the main agent, only `{key, name, effective_modalities}` is shown; sensitive fields do not enter the prompt. The `api_key_env` field is also supported (reads the key from an environment variable).

Each entry may explicitly declare `modalities` (default `["text"]`, text is always implicit). Pool rules are trimmed at init, then trimmed empirically by the probe at `clawarena-team run` startup:

| Pool | Must include | Allowed |
|---|---|---|
| `llm`  | text       | text |
| `vlm`  | text+image | text/image/video (audio auto-removed) |
| `omni` | text+audio | text/image/audio/video |

Missing required modality or empirical failure → error; missing optional modality or empirical failure → warn and remove from the effective set.

Any extra field is treated as an error.

## scenarios/<id>/manifest.json

| Field | Required | Meaning |
|---|---|---|
| `scenario_id` | ✓ | Must match the directory name |
| `desc` |   | Scenario description |
| `workspace_template` | ✓ | Relative path to the original workspace directory, copied to an isolated copy at run time |
| `scripts` | ✓ | Relative path to the scoring scripts directory (relative to manifest.json), resolved as the `${scripts}` placeholder. The code does not hard-code any naming for the scripts directory; the directory must be explicitly declared by the manifest |
| `main_agent_accessible_paths` | ✓ | Subpaths accessible to the main agent (relative to the workspace root) |
| `main_agent_delegable_paths` |   | Paths that can only be granted to a subagent (the main agent's own Read/Edit/Write/Grep/Glob cannot reach them, but the main agent can include them in a subagent's `accessible_paths` when calling `CreateSubagent`). Used to force delegation: requiring main to use a subagent for large files, multimodal content, and red-herring directories. Defaults to an empty list |
| `updates` | ✓ | dict[update_id, {op: "new"\|"replace", files: [{src, dst}]}] |
| `rounds_ref` | ✓ | Relative path to questions.json |

`updates[*].files[*].src` is relative to manifest.json; `dst` is relative to the workspace root.

## scenarios/<id>/questions.json

**The outer level is a list**:

```json
[
  {
    "id": "q1",
    "type": "exec_check",
    "update_ids": ["u1"],
    "question": "...",
    "eval": {
      "command": "python ${scripts}/check_q1.py ${workspace}",
      "expect_exit": 0,
      "timeout": 60,
      "expect_stdout": null,
      "expect_stdout_regex": false
    },
    "feedback": {"correct": "Well done", "incorrect": "Direction for correction..."},
    "tags": ["triage_planning", "verbatim_citation"]
  }
]
```

Field descriptions:

| Field | Required | Meaning |
|---|---|---|
| `id` | ✓ | round id (unique within the scenario) |
| `type` | ✓ | Currently only `exec_check` is supported |
| `question` | ✓ | The prompt presented to the main agent |
| `eval` | ✓ | Scoring configuration: `command` is required; `expect_exit`/`timeout`/`expect_stdout`/`expect_stdout_regex` are optional (defaults 0 / 60 / null / false) |
| `feedback` | ✓ | `{correct, incorrect}` dictionary; both keys are optional (default empty string) |
| `update_ids` |   | List of updates triggered by this round; defaults to an empty list |
| `tags` |   | Capability-dimension labels (controlled vocabulary in `src/clawarena_team/stats/tag_vocab.py::CONTROLLED_TAGS`); metadata only, does not affect runtime scheduling or scoring. `clawarena-team stats` gives the distribution and uncovered dimensions in STATS.md §10. Silently ignored if missing |

**`tags` field examples** (taken from active scenarios; can be cross-referenced against the actual usage in wave3 / wave4):

```jsonc
// q1 — triage / planning type (first round brief → plan)
"tags": ["triage_planning", "verbatim_citation", "numerical_extraction"]

// q3 — contains update merge + cross-source synthesis
"tags": ["multimodal_audio", "modality_decoy", "update_merge",
         "json_schema", "cross_source_synthesis"]

// q5 — final-chapter synthesis + real test run
"tags": ["code_execution", "stderr_parsing", "final_synthesis",
         "compliance_token", "bash_tool_run"]

// wave4 additions: background tasks + long tasks + session reuse
"tags": ["background_subagent", "async_long_running",
         "partial_result_handling", "stateful_subagent"]
```

Usage conventions (repeated here so authors can copy directly):

- **2–6 tags** per round, labeling only that round's main examination points
- Use only values from the controlled vocabulary in `stats/tag_vocab.py` (spelling inconsistencies will be reported by STATS §10.5)
- Add a new dimension to the controlled vocabulary in `stats/tag_vocab.py` before using it

Supported placeholders (their values are resolved by the current run within the harness and injected; all path values are safely quoted with `shlex.quote` and can be embedded directly into shell commands):

| Placeholder | Meaning |
|---|---|
| `${workspace}` | Absolute path to this run's workspace copy. The cwd of `eval.command` is this directory. |
| `${scripts}` | Absolute path resolved from the `scripts` field of manifest.json, for invocation in the form `python ${scripts}/check_q1.py`. |
| `${scenario_dir}` | Absolute path to the directory containing the scenario manifest. |
| `${scenario_id}` | The scenario ID string. |

Unrecognized `${VAR}` is preserved as-is, allowing the shell itself to expand it (e.g. `${HOME}`).

After each round completes, `eval.command` is run immediately (cwd = `${workspace}`, shell=True); pass is jointly determined by `expect_exit` (and optionally `expect_stdout` / `expect_stdout_regex`).

## update operations

Only two `op` values are supported:

- `new`: dst must not exist;
- `replace`: if dst exists, delete it first (recursively), then copy.

## workspace naming conventions

The inside of a workspace should simulate a real working scenario, **avoiding** names like `accessible_zone/` `restricted/` that expose the evaluation intent. The actual accessible scope is determined by `main_agent_accessible_paths`.

## Asset Guidance: `_sandbox_hint.md` and `_index.md`

To avoid the main agent blindly Reading large asset files, scenario authors should provide a `_sandbox_hint.md` in the workspace root and add it to `main_agent_accessible_paths` as the asset map that the main agent must read on its first round. This file should list:

- which directories/files the main agent can `Read` directly (small text, natively supported multimodal content);
- which directories/files should be routed via `CreateSubagent` to the corresponding `model_key` (`llm` / `vlm` / `omni`), and why;
- heuristic rules such as "a single file ≥ 24 KiB should be preferentially delegated".

For long documents split by chapter/article, it is recommended to place an `_index.md` at the subdirectory root, listing each chapter file's path, approximate tokens, and a one-sentence summary, so the main agent can choose which chapters to delegate without reading the body text.

`main_agent_accessible_paths` must still cover all paths that any subagent might be granted (a subagent's scope is a subset of its creator's), but the `ReadTool` itself adds a `[notice: ...]` hint to files exceeding `read.notice_bytes` (default 32 KiB), and errors out directly with a pagination-or-delegation hint for files exceeding `read.hard_bytes` (default 256 KiB). These two thresholds are configured in the `read:` section of `configs/default.yaml`.

## update two-group form

When a single update_id needs to both add a non-existent file (`op=new`) and replace an existing index/manifest (`op=replace`), it should be split into two update groups (e.g. `u1_add` and `u1_idx`), listed in `questions.json` as `"update_ids": ["u1_add", "u1_idx"]`. The Runner applies them in list order.

## Alignment with the Code

Adding or removing fields must be kept in sync across:

- `src/clawarena_team/types.py`: dataclass definitions;
- `src/clawarena_team/runner/dataset.py`: loading and field mapping;
- `src/clawarena_team/runner/validator.py`: the strict validation of `clawarena-team check` (missing required → error, unknown field → error except for tests.json, missing optional → warn, pure-metadata optional fields such as `tags` go through quiet_optional and are silenced);
- `tests/test_dataset.py`: unit tests.
