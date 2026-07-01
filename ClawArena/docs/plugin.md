# clawarena Plugin System

clawarena plugins are `.py` files that register external framework adapters, enabling `--framework` to reference frameworks defined outside the core codebase.

## Overview

The plugin system serves one purpose: **extending clawarena with new framework adapters**. Each plugin file is a Python script that calls `register_adapter()` to make a new framework available.

Framework-specific inference hooks (post-round logic like feedback override, score override, early termination) are handled by the **engine's `on_round_complete()` method**, not by plugins.

## Writing a Plugin

A plugin file registers one or more adapters:

```python
# my_framework.py
from clawarena.adapters.registry import register_adapter
from clawarena.adapters.base import FrameworkAdapter
from clawarena.engines.base import AgentEngine
from clawarena.data_handlers.base import DataHandler
from clawarena.core.types import AgentResult, WorkCopy

class MyEngine(AgentEngine):
    async def run_agent(self, session_id, message, work_copy, **kwargs):
        # ... your framework invocation logic ...
        return AgentResult(status="success", answer="...")

class MyDataHandler(DataHandler):
    # ... implement all abstract methods ...
    pass

register_adapter("my_framework", lambda: FrameworkAdapter(
    name="my_framework",
    engine=MyEngine(),
    data_handler=MyDataHandler(),
    # qtype_overrides: optional dict mapping question type names to custom QuestionType
    # instances. Omit to use the built-in multi_choice / exec_check / command_check handlers.
))
```

## CLI Usage

```bash
# Load plugin and use the registered framework
clawarena infer --data tests.json --framework my_framework --out results/ \
    --plugin my_framework.py

# Multiple plugins
clawarena run --data tests.json --frameworks openclaw,my_framework --out results/ \
    --plugin my_framework.py another_plugin.py
```

The `--plugin` flag is available on `infer` and `run` commands. Plugin files are executed before the framework is resolved, so any adapter registered during loading is immediately available.

## Engine Round Hooks

Post-round logic (previously handled by the old plugin/callback system) is now part of the engine. Override `on_round_complete()` in your engine subclass:

```python
from clawarena.engines.base import AgentEngine
from clawarena.core.types import RoundContext, RoundResult

class MyEngine(AgentEngine):
    async def run_agent(self, session_id, message, work_copy, **kwargs):
        ...

    async def on_round_complete(self, ctx: RoundContext) -> RoundResult | None:
        # Custom post-round logic
        if ctx.inline_score.get("passed"):
            return None  # No intervention
        return RoundResult(
            override_feedback="Custom feedback for next round",
            extra_data={"custom_metric": 42},
        )
```

### RoundContext Fields

| Field | Type | Description |
|-------|------|-------------|
| `framework` | `str` | Framework name |
| `test_id` | `str` | Test scenario ID |
| `round_id` | `str` | Current round ID |
| `round_index` | `int` | Zero-based round index |
| `total_rounds` | `int` | Total rounds in this test |
| `is_last_round` | `bool` | Whether this is the final round |
| `round_record` | `dict` | Raw round data from questions.json |
| `query` | `str` | Actual query sent to the agent |
| `result` | `dict` | Full infer_result.json content |
| `inline_score` | `dict` | Inline scoring result |
| `prev_inline_score` | `dict \| None` | Previous round's score |
| `all_results` | `list \| None` | All results (only on last round) |
| `all_inline_scores` | `list \| None` | All scores (only on last round) |
| `result_path` | `Path` | Path to infer_result.json |
| `workspace_path` | `Path \| None` | Agent's workspace directory |
| `out_dir` | `Path` | Output directory |
| `session_id` | `str` | Agent session ID (empty string if new) |
| `work_copy` | `WorkCopy \| None` | Working copy with config and state |

### RoundResult Fields

All fields are optional — return `None` for no intervention:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `skip_remaining` | `bool` | `False` | Stop after this round |
| `override_feedback` | `str \| None` | `None` | Replace feedback for next round |
| `override_inline_score` | `dict \| None` | `None` | Replace inline score (must include `passed`) |
| `extra_data` | `dict \| None` | `None` | Attach to `infer_result["hook_data"]` |
| `skip_standalone_feedback` | `bool` | `False` | Skip final standalone feedback |

### Processing Priority

1. `override_inline_score` — Replaces scoring, rewrites result file
2. `extra_data` — Written to `infer_result.json["hook_data"]`
3. `override_feedback` — Stored for the next round's query
4. `skip_standalone_feedback` — Checked after the last round
5. `skip_remaining` — Breaks out of the round loop

## Gateway Lifecycle (Advanced)

For frameworks that require a long-running gateway process (e.g., a local API server), override the three gateway methods in your engine subclass. The base class provides no-op defaults.

```python
from clawarena.engines.cli_subprocess import CLISubprocessEngine
from clawarena.core.types import GatewayHandle, WorkCopy

class MyEngine(CLISubprocessEngine):
    def build_gateway_cmd(self, work_copy: WorkCopy, port: int) -> list[str] | None:
        # Return the command to start the gateway, or None to skip.
        return ["my-gateway", "--port", str(port)]

    async def wait_for_gateway(self, handle: GatewayHandle, timeout: float = 120.0) -> None:
        # Poll until the gateway is ready (default: TCP connect probe).
        await super().wait_for_gateway(handle, timeout)

    async def stop_gateway(self, handle: GatewayHandle) -> None:
        # Terminate the gateway process.
        await super().stop_gateway(handle)
```

`CLISubprocessEngine.start_gateway` automatically captures stdout/stderr from the gateway process into `handle.stdout_chunks` / `handle.stderr_chunks`, which are included in error messages when `wait_for_gateway` times out or detects an early exit.
