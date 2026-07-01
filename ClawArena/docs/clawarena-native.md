# ClawArena Native Harness

`clawarena-native` is a built-in agent harness that ships inside ClawArena itself.
Unlike the external framework adapters (OpenClaw, Claude Code, Nanobot, PicoClaw),
which wrap separately-installed CLIs that evolve on their own release cadence, the
native harness is a fully self-contained, fixed Python implementation.

**Use it when:**

- Your environment cannot install the external framework CLIs, or cannot pin them
  to a fixed version.
- You want a deterministic, reproducible reference harness whose behaviour does not
  change underneath your benchmark across runs.
- You want a single agent loop that you fully control, with no external process or
  gateway to manage.

It requires no extra installation and no external runtime — it runs in-process and
connects directly to the LLM provider.

---

## 1. Using it

The framework name is `clawarena-native`, with aliases `native` and `clawnative`.

```bash
# CLI
clawarena infer --data data/clawarena-real/tests.json --framework clawarena-native --out results/
clawarena run   --data data/clawarena-real/tests.json --frameworks clawarena-native --out output/
```

```python
# SDK
from clawarena import ClawArena
ClawArena(data="clawarena-real", out="results").run("clawarena-native")
```

A dataset must provide a `clawarena-native` manifest (see
[§7](#7-data-layout)). To convert an existing OpenClaw-format dataset, see
[§8](#8-converting-an-existing-dataset).

---

## 2. Execution model

ClawArena drives a scenario one round at a time, calling the engine once per round.
The native engine runs the agent loop in-process: for each round it rebuilds the
harness over the agent's **active session** transcript and continues from where the
previous round left off. The transcript is the single source of truth — it is read
from disk at the start of every round, so multi-round conversations reconstruct
naturally without any in-memory carry-over between rounds.

The model is configured through ClawArena's standard `ModelConfig` (CLI flags,
`tests.json`, or the SDK `model=` argument). ClawArena providers map onto native
providers as follows:

| ClawArena provider                                            | Native provider  |
|---------------------------------------------------------------|------------------|
| `anthropic`, `claude`, `bedrock`                              | `anthropic`      |
| `google`, `gemini`                                            | `gemini`         |
| `openai`, `azure`, `ollama`, `openrouter`, `groq`, `qwen`, …  | `openai_compat`  |

---

## 3. Tools

The main agent is equipped with a fixed tool set:

| Tool             | Purpose |
|------------------|---------|
| `Read` / `Write` / `Edit` | Read and modify workspace files. |
| `Bash`           | Run shell commands in the workspace. |
| `Grep` / `Glob`  | Search file contents and names. |
| `LS`             | List directory contents. |
| `Agent`          | Spawn a subagent (see [§4](#4-subagents)). |
| `Workflow`       | Orchestrate multi-agent work (see [§5](#5-workflow-tool)). |
| `SessionHistory` | Read other sessions of the same agent (see [§6](#6-session-history)). |

All file tools are confined to the agent's workspace through an accessible-scope
guard; reads are tracked so that edits to unread files can be flagged.

---

## 4. Subagents

The `Agent` tool and the `Workflow` tool spawn subagents from a **fixed set of
subagent types**:

- `Explore` — a read-only search/exploration agent.
- `general-purpose` — a full-capability agent (the **default**).

There is no facility to define new subagent types at run time. Any request for an
unknown subagent type is rejected. Subagents run with their own token budget and
iteration cap, and (when given a schema) return validated structured output.

---

## 5. Workflow tool

The `Workflow` tool lets the main agent run a JavaScript orchestration script that
fans work out across subagents deterministically. The script runtime exposes:

- `agent(prompt, opts)` — spawn a subagent. `opts.subagent_type` may only be
  `"Explore"` or `"general-purpose"` (default `"general-purpose"`); an invalid value
  raises a script error. `opts.schema` forces validated structured output.
- `parallel(thunks)` — run tasks concurrently with a barrier.
- `pipeline(items, ...stages)` — stream each item through stages without a barrier.
- `phase(title)` / `log(message)` — progress reporting.

Workflows run **asynchronously in the background**. When a background workflow
finishes, its result is delivered to the main agent as a `<task-notification>`, so
the agent can launch long-running orchestration and keep working in the meantime.
Concurrency and total subagent count are bounded (defaults: 8 concurrent, 1000
total).

> Note: unlike some workflow runtimes, this harness has **no `defineAgent`** — a
> script can only choose among the fixed subagent types above.

---

## 6. Session history

A single agent can own several sessions: one **active** session (the transcript the
current round writes to) plus any number of **history** sessions — pre-authored
conversations from other channels or earlier timelines that the dataset ships.

The `SessionHistory` tool lets the main agent read those history sessions:

- `SessionHistory(action='list')` — list the available history sessions with their
  channel and message count.
- `SessionHistory(action='read', session_id=<id>)` — return the
  user/assistant/tool_result transcript of one history session.

An agent may only read sessions registered in its own index, and the active session
is not re-readable through the tool. History is kept as separate transcript files
indexed by `sessions.json` (rather than flattened into Markdown), which preserves
the "separate sessions, cross-session reads" structure that the benchmark relies on.

---

## 7. Data layout

The native data layout is intentionally compact:

```
manifest.json
state/
  {agent_id}/
    sessions.json              # session index for this agent
    {active_session}.jsonl     # active session (written at run time)
    {history_session}.jsonl    # pre-authored history session(s), read-only
workspaces/
  {agent_id}/                  # initial workspace files
updates/
  {agent_id}/{update_id}/      # round-driven session/workspace updates
```

`sessions.json` maps each `session_id` to `{session_file, channel, is_active,
updated_at}`. Transcripts use a compact JSONL format — one message per line as
`{role, content[, tool_calls][, subtype][, meta]}` with `role` in
`system | user | assistant | tool_result`. Compaction boundaries are recorded as
`system` messages with a `subtype`.

The full schema and field-by-field reference live in the
[Data Structure](data-structure.md) guide.

---

## 8. Converting an existing dataset

A dataset authored in the OpenClaw format can be converted to the native layout
with the bundled script:

```bash
python scripts/convert_openclaw_to_native.py \
    --src-root /path/to/ClawArena \
    --dst-root /path/to/output \
    --roots clawarena clawarena-real metaclaw-bench
```

The converter reads each `data/<root>/openclaw/` dataset (read-only) and writes a
`data/<root>/clawarena-native/` dataset: it rewrites the verbose OpenClaw session
records into the compact native JSONL, builds the `sessions.json` index, copies
workspaces, and translates the manifest and update entries.

---

## 9. Statistics

`clawarena stats` understands the native layout natively. Token and structural
statistics are computed directly from the compact session JSONL:

```bash
clawarena stats --data data/clawarena-real/tests.json --framework clawarena-native --out stats/
```
