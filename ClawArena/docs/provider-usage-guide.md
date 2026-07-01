# Provider Platform and MetaClaw Usage Guide

## 1. Provider Platform

### 1.1 Overview

clawarena provides a unified `ModelConfig` abstraction layer that allows configuring all frameworks' LLM providers through CLI arguments, environment variables, or tests.json fields. Each framework translates the common configuration into its framework-specific format via the `apply_model_config` method.

### 1.2 Configuration Precedence

```
CLI arguments (highest)
    > Environment variables CLAWARENA_MODEL_ID / CLAWARENA_API_BASE / CLAWARENA_PROVIDER / CLAWARENA_API_KEY
        > Framework-level model field in tests.json
            > Top-level model field in tests.json
                > Manifest built-in defaults (lowest)

Once MetaClaw starts, the proxy address automatically overrides all of the above.
```

### 1.3 CLI Arguments

Both `clawarena infer` and `clawarena run` support the following optional arguments:

```bash
clawarena infer --data tests.json --framework openclaw --out results/ \
  --provider openai \
  --model-id gpt-4o \
  --api-base https://api.openai.com/v1 \
  --api-key sk-xxx
```

| Argument | Description |
|---|---|
| `--provider` | LLM provider type. Core: `openai` / `anthropic` / `claude` / `bedrock` / `google` / `ollama` / `azure`. User-managed CCR: `ccr` / `claude-code-router`. Extended (OpenAI-compat, routed via auto-CCR for claude-code): `openrouter` / `groq` / `mistral` / `xai` / `qwen` / `moonshot` / `glm` / `minimax` |
| `--model-id` | Model name, e.g. gpt-4o, claude-opus-4.6 |
| `--api-base` | API endpoint URL; can be omitted for providers with built-in defaults |
| `--api-key` | Authentication key; recommended to pass via environment variables |
| `--model-config` | JSON object with extra model-entry fields forwarded to the framework config, e.g. `'{"reasoning": true, "contextWindow": 200000}'` |

### 1.4 Environment Variables

| Variable | Description |
|---|---|
| `CLAWARENA_MODEL_ID` | Model name |
| `CLAWARENA_API_BASE` | API endpoint |
| `CLAWARENA_PROVIDER` | Provider type (default: openai) |
| `CLAWARENA_API_KEY` | Authentication key |

### 1.5 tests.json model Field

```json
{
  "model": {
    "provider": "${CLAWARENA_PROVIDER:-openai}",
    "model_id": "${CLAWARENA_MODEL_ID}",
    "api_base": "${CLAWARENA_API_BASE}",
    "api_key": "${CLAWARENA_API_KEY}"
  },
  "frameworks": {
    "openclaw": {
      "manifest": "openclaw/manifest.json",
      "model": {
        "provider": "anthropic",
        "model_id": "claude-opus-4.6",
        "api_key": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

Framework-level model takes precedence over the top-level model. All fields support `${VAR}` and `${VAR:-default}` interpolation.

### 1.6 Provider Quick Reference

| provider | Typical model_id | api_base | api_key |
|---|---|---|---|
| `openai` | gpt-4o | Default `https://api.openai.com/v1` | `$OPENAI_API_KEY` |
| `anthropic` | claude-opus-4.6 | Default `https://api.anthropic.com` | `$ANTHROPIC_API_KEY` |
| `claude` | claude-opus-4.6 | Optional `.credentials.json` path for native-oauth | OAuth setup-token |
| `ollama` | llama3.2 | Default `http://localhost:11434/v1` | None |
| `google` | gemini-pro | Default Google GenAI URL | `$GOOGLE_API_KEY` |
| `azure` | gpt-4o | **Required** | `$AZURE_API_KEY` |
| `bedrock` | claude-v2 | AWS SDK automatic | AWS credential chain |

### 1.7 Framework Support Matrix

| Framework | openai | anthropic | claude | google | ollama | azure | bedrock | codex |
|---|---|---|---|---|---|---|---|---|
| OpenClaw | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Claude Code | ✓* | ✓ | ✓ | ✓* | ✓* | ✓* | ✗ | ✗ |
| PicoClaw | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| nanobot | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |

*Claude Code routes non-Anthropic providers through the **auto-CCR bridge** (the engine spawns a local `ccr start` subprocess per run; see `src/clawarena/data_handlers/claude_code/handler.py::_classify_claude_provider`). `claude` and `anthropic` use native paths; `ccr` / `claude-code-router` assumes a user-managed CCR instance; `bedrock` and `codex` are explicitly rejected with `ConfigError` because they cannot be bridged.

For Claude Code `provider='claude'` (`native-oauth` route), auth field semantics are special:
- `api_key` means a Claude OAuth setup-token and is passed as `CLAUDE_CODE_OAUTH_TOKEN`
- `api_base` means a path to a customized `.credentials.json`, which is copied into the run state directory before launch
- `api_base` and `api_key` are mutually exclusive; setting both raises `ConfigError`
- if neither is set, clawarena warns and falls back to copying `~/.claude/.credentials.json`

**Extended OpenAI-compatible providers** (openrouter, groq, mistral, xai, qwen, moonshot, glm, minimax) are accepted by OpenClaw natively and by Claude Code via auto-CCR with the `["openai", "maxcompletiontokens"]` transformer chain (`max_tokens` → `max_completion_tokens` rewrite for gpt-5 / o1-style models). OpenRouter and google have dedicated CCR transformers (`openrouter`, `gemini` respectively).

---

## 2. MetaClaw Integration

### 2.1 Overview

MetaClaw is an OpenAI-compatible API proxy layer with three built-in enhancement mechanisms: Memory, Skills, and RL. clawarena manages the MetaClaw lifecycle at the `infer.py` level, making it fully transparent to downstream frameworks. Currently, openclaw and nanobot are supported as MetaClaw targets.

### 2.2 Enabling MetaClaw

Add a `metaclaw` field in tests.json:

```json
{
  "metaclaw": {
    "enabled": true,
    "config_path": "metaclaw/config.yaml",
    "per_scene_isolation": false,
    "memory_trigger": {
      "every_n_rounds": 0,
      "every_n_scenes": 1,
      "on_last_round": true
    },
    "rl_trigger": {
      "every_n_rounds": 0,
      "every_n_scenes": 5,
      "on_last_round": false
    }
  }
}
```

### 2.3 Run Modes

| Mode | memory | skills | rl | Concurrency Constraint |
|---|---|---|---|---|
| baseline | ✗ | ✗ | ✗ | None |
| memory | ✓ | ✗ | ✗ | concurrency=1 (global mode) |
| skills_only | ✗ | ✓ | ✗ | concurrency=1 (global mode) |
| rl | ✗ | ✓ | ✓ | concurrency=1 (global mode) |
| madmax | ✓ | ✓ | ✓ | concurrency=1 (global mode) |

The concurrency=1 constraint is enforced by `infer.py` only when `per_scene_isolation=false`; the isolation path (§2.4) lifts it at the cost of one proxy per scene.

### 2.4 Per-Scene Isolation Mode

When `per_scene_isolation: true`, each scene gets its own independent MetaClaw proxy instance:
- Removes the concurrency=1 constraint, allowing parallel execution
- `every_n_scenes` is ignored
- `on_last_round` semantics change to "last round of the current scene"

### 2.5 YAML Configuration Example

Memory only:
```yaml
llm:
  provider: custom
  api_base: ${CLAWARENA_API_BASE}
  api_key: ${CLAWARENA_API_KEY}
  model_id: ${CLAWARENA_MODEL_ID}

mode: skills_only
memory:
  enabled: true
  scope: default
  manual_trigger: true
skills:
  enabled: false
rl:
  enabled: false
```

### 2.6 Reports

After a run completes, the following are automatically generated in the output directory:
- `metaclaw_report.json` -- Complete raw data
- `metaclaw_report.md` -- Human-readable Markdown report

Reports include trigger statistics, Memory state, Skills snapshot comparisons, RL training estimates, and more.

---

## 3. Code Structure

### 3.1 Provider Platform

```
src/clawarena/core/provider.py          -- ModelConfig dataclass + parsing logic
src/clawarena/data_handlers/base.py     -- apply_model_config no-op default method
src/clawarena/data_handlers/*/handler.py -- Per-framework implementations
src/clawarena/cli.py                    -- --provider/--model-id/--api-base/--api-key
src/clawarena/core/infer.py             -- model_config parsing + call chain
src/clawarena/core/check.py             -- model/metaclaw field validation
```

### 3.2 MetaClaw Module

```
src/clawarena/overlays/metaclaw/
├── __init__.py    -- Exports MetaClawManager
├── config.py      -- YAML loading + trigger config parsing
├── proxy.py       -- ProxyProcess + MetaClawProxyPool
├── run_dir.py     -- Isolation directory management + policy.json setup
├── hooks.py       -- Trigger logic (global/isolated modes)
├── report.py      -- Report collection and generation
└── manager.py     -- Lifecycle orchestration main class
```

### 3.3 Tests

```
tests/test_provider.py   -- ModelConfig + per-framework apply_model_config + claude-code classifier
tests/test_metaclaw.py   -- Config/RunDir/Hooks/Report + Check integration
tests/test_engines.py    -- CCR config / transformer chain / gateway lifecycle
```
