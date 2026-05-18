# MetaClaw Integration Guide

## Overview

MetaClaw is an OpenAI-compatible API proxy layer that provides three enhancement mechanisms: Memory, Skills, and RL. clawarena supports two integration modes:

- **Managed mode** (default): clawarena automatically starts, configures, and stops the MetaClaw proxy
- **Unmanaged mode**: the user manages the MetaClaw instance independently; clawarena only fires trigger hooks

---

## Quick Start

### 1. Managed Mode

Add a `metaclaw` field to `tests.json`:

```json
{
  "metaclaw": {
    "enabled": true,
    "managed": true,
    "config_path": "metaclaw/memory.yaml",
    "memory_trigger": {
      "every_n_rounds": 6,
      "on_last_round": true
    }
  }
}
```

Then run as usual:

```bash
clawarena infer --data tests.json --framework openclaw --out results/
```

clawarena will:
1. Load the `metaclaw/memory.yaml` configuration
2. Automatically start the MetaClaw proxy
3. Route all framework API requests through the proxy
4. Send memory ingest / RL train requests according to the trigger policy
5. Automatically shut down the proxy when evaluation completes

### 2. Unmanaged Mode

Start MetaClaw (or any OpenAI-compatible proxy chain) yourself, then pass the API address via the `model` field:

```json
{
  "model": {
    "provider": "openai",
    "model_id": "gpt-4o",
    "api_base": "http://127.0.0.1:30000/v1",
    "api_key": "${MY_API_KEY}"
  },
  "metaclaw": {
    "enabled": true,
    "managed": false,
    "memory_trigger": {
      "every_n_rounds": 6,
      "on_last_round": true
    }
  }
}
```

In this mode clawarena does not start any proxy; `model.api_base` is passed directly to the framework and also used as the trigger target address for hooks.

Applicable scenarios:
- MetaClaw is already running externally (e.g., Docker, remote server)
- Custom MetaClaw startup parameters are required

---

## tests.json Field Reference

```json
{
  "metaclaw": {
    "enabled": true,
    "managed": true,
    "config_path": "metaclaw/memory.yaml",
    "per_scene_isolation": false,
    "memory_trigger": {
      "every_n_rounds": 6,
      "every_n_scenes": 0,
      "on_last_round": true
    },
    "rl_trigger": {
      "every_n_rounds": 0,
      "every_n_scenes": 0,
      "on_last_round": false
    }
  }
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | — | Whether to enable MetaClaw |
| `managed` | bool | `true` | `true`: clawarena manages the proxy lifecycle; `false`: user-managed |
| `config_path` | string | — | Path to the MetaClaw YAML config (relative to tests.json); required in managed mode |
| `per_scene_isolation` | bool | `false` | Use a separate proxy instance per scene (managed mode only) |
| `memory_trigger` | object | — | Memory ingest trigger policy |
| `rl_trigger` | object | — | RL train trigger policy |

### Trigger Policy Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `every_n_rounds` | int | `0` | Trigger once every N rounds (0 = disabled) |
| `every_n_scenes` | int | `0` | Trigger once every N completed scenes (0 = disabled; ignored in isolation mode) |
| `on_last_round` | bool | `false` | Trigger on the last round of each scene, but **skip scenes with no subsequent interaction** (global mode skips the final scene; isolation mode always skips, since each scene is independent) |

---

## MetaClaw YAML Configuration

Configuration files are located in the `data/clawarena/metaclaw/` directory. Preset templates:

| File | Mode | Memory | Skills | RL |
|------|------|--------|--------|-----|
| `dummy.yaml` | skills_only | ✗ | ✗ | ✗ |
| `memory.yaml` | skills_only | ✓ | ✗ | ✗ |
| `skills-only.yaml` | skills_only | ✗ | ✓ | ✗ |
| `synergy.yaml` | skills_only | ✓ | ✓ | ✗ |
| `rl-only.yaml` | rl | ✗ | ✗ | ✓ |
| `rl-only-memory.yaml` | rl | ✓ | ✗ | ✓ |
| `rl.yaml` | rl | ✗ | ✓ | ✓ |
| `madmax.yaml` | rl | ✓ | ✓ | ✓ |

### Key YAML Fields

```yaml
# Upstream LLM configuration — supports ${CLAWARENA_*} environment variable interpolation
llm:
  provider: custom
  api_base: ${CLAWARENA_API_BASE}
  api_key: ${CLAWARENA_API_KEY}
  model_id: ${CLAWARENA_MODEL_ID}

# Run mode
mode: skills_only    # "skills_only" | "rl" | "madmax"

# Memory configuration
memory:
  enabled: true
  scope: default
  retrieval_mode: hybrid         # "keyword" | "hybrid" | "embedding"
  manual_trigger: true           # clawarena controls trigger timing
  max_injected_units: 10
  max_injected_tokens: 1500

# Skills configuration
skills:
  enabled: true
  dir: ${METACLAW_ROOT}/memory_data/skills
  retrieval_mode: template       # "template" | "embedding"
  auto_evolve: true
  top_k: 6

# RL configuration
rl:
  enabled: false
  backend: tinker                # "auto" | "tinker" | "mint" | "weaver"
  manual_train_trigger: true     # clawarena controls trigger timing
  batch_size: 4

# Proxy listener
proxy:
  host: 0.0.0.0
  port: 30000
```

> `manual_trigger: true` (Memory) and `manual_train_trigger: true` (RL) are essential for clawarena integration. When set to `true`, MetaClaw no longer triggers automatically; instead, clawarena's trigger hooks send HTTP POST requests at the appropriate time.

---

## Run Modes and Concurrency

### Global Mode (default)

```json
"per_scene_isolation": false
```

- All scenes share a single MetaClaw proxy
- Concurrency is forced to `concurrency=1` (Memory/Skills are stateful and cannot run concurrently)
- `every_n_scenes` triggers based on cumulative completion count across scenes

### Isolation Mode

```json
"per_scene_isolation": true
```

- Each scene is assigned an independent MetaClaw proxy instance (proxy pool)
- Multiple scenes can run concurrently
- `every_n_scenes` is ignored (each scene is independent)
- `on_last_round` semantics become "the last round of this scene"

---

## Interaction with the Provider Platform

### Managed Mode

After MetaClaw starts, clawarena automatically generates a `ModelConfig` pointing to the proxy address, overriding all user-configured model parameters. The priority chain becomes:

```
MetaClaw proxy address (highest)
  > CLI --api-base / --model-id / ...
    > Environment variables CLAWARENA_*
      > tests.json model field
```

### Unmanaged Mode

No interception occurs. The `model` field is resolved through the normal priority chain; the user must ensure `api_base` points to the correct proxy address.

---

## Trigger Hooks Mechanism

clawarena calls `MetaClawHooks.on_round_complete()` after each round and determines whether to send an HTTP POST based on the trigger policy:

| Request | Method | Trigger Condition |
|---------|--------|-------------------|
| Memory Ingest | `POST {proxy_url}/v1/memory/ingest` (JSON `{}`) | `memory.enabled && memory.manual_trigger` + trigger policy match |
| RL Train | CLI: `metaclaw train-step --port <port>` | `rl.enabled && rl.manual_train_trigger` + trigger policy match |

> **Important**: All triggers follow the "no subsequent interaction, no trigger" rule. In global mode, the last round of the final scene is skipped; in isolation mode, the last round of every scene is skipped, because there is no subsequent interaction that could benefit from the updated state.

In unmanaged mode, if no MetaClaw config is provided (no `config_path`), hooks assume both memory and RL are enabled by default and rely entirely on the trigger policy for control.

### Trigger Example

Global mode, 2 scenes, configured with `every_n_rounds: 6, on_last_round: true`. Scene 1 has 20 rounds, scene 2 has 10 rounds:

```
Scene 1:
  Round  1-5:  no trigger
  Round  6:    memory ingest ✓
  Round  7-11: no trigger
  Round 12:    memory ingest ✓
  Round 13-17: no trigger
  Round 18:    memory ingest ✓
  Round 19:    no trigger
  Round 20:    memory ingest ✓ (on_last_round, not the final scene)

Scene 2 (final scene):
  Round  1-5:  no trigger
  Round  6:    memory ingest ✓
  Round  7-9:  no trigger
  Round 10:    skipped (last round of final scene, no subsequent interaction)
```

---

## Reports

In managed mode, the following files are automatically generated in the output directory after a run completes:

- `metaclaw_report.json` — complete raw data
- `metaclaw_report.md` — human-readable Markdown report

Contents include: trigger statistics (ingest count, train count), Memory state, Skills snapshot comparison, RL training estimates, and run duration.

---

## Code Structure

```
src/clawarena/overlays/metaclaw/
├── __init__.py    — exports MetaClawManager
├── config.py      — YAML loading + trigger config parsing
├── proxy.py       — ProxyProcess + MetaClawProxyPool (isolation mode)
├── run_dir.py     — isolation directory management + policy.json presets
├── hooks.py       — trigger logic (global / isolation / unmanaged)
├── report.py      — report collection and generation
└── manager.py     — managed mode lifecycle orchestration

data/clawarena/metaclaw/
├── memory.yaml         — Memory-only config
├── skills-only.yaml    — Skills-only config
├── synergy.yaml        — Memory + Skills + Synergy
├── rl-only.yaml        — RL-only config
├── rl.yaml             — RL + Skills config
├── madmax.yaml         — Full-feature config
├── dummy.yaml          — Empty config (baseline)
└── example.yaml        — Complete reference config (all fields annotated)
```

---

## FAQ

**Q: Concurrency is forced to 1 in managed mode. How do I work around this?**
A: Use `per_scene_isolation: true` to lift the concurrency restriction. Each scene gets its own independent proxy instance.

**Q: Hooks are not firing in unmanaged mode?**
A: Verify that `model.api_base` correctly points to the MetaClaw proxy address. Hooks derive the proxy URL from `effective_model.api_base`.

**Q: How do I enable hooks only, without model interception?**
A: Set `managed: false` and fill in the `model` field with your pre-configured API address. clawarena will not modify any API configuration; it will only send trigger requests at the appropriate times.
