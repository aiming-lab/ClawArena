# Provider Integration Guide

ClawArena-Team abstracts all model calls behind `BaseProvider`, which uniformly exposes the async `chat(messages, tools, **kwargs) -> dict` and returns standardized fields:

```python
{
    "content": str,
    "tool_calls": [{"id": str, "name": str, "arguments": dict}, ...],
    "usage": {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int},
    "finish_reason": str,
}
```

## Built-in providers

| name | class | description |
|---|---|---|
| `openai` / `openai_compat` / `vllm` / `ollama` / `openrouter` | `OpenAICompatProvider` | OpenAI-compatible interface (`/v1/chat/completions`). Local vLLM serve, Ollama's OpenAI interface, and various routers can all use this path |
| `anthropic` | `AnthropicProvider` | Anthropic Messages API |

## ModelConfig fields

| field | meaning |
|---|---|
| `provider` | provider name (used for lookup) |
| `model_id` | model id |
| `api_base` | API endpoint |
| `api_key` | API key; can also be specified via the `api_key_env` field as an environment variable name (only available in manifests.json) |
| `modalities` | list of content types natively supported by the model, a subset of `{"text", "image", "audio", "video"}`. `"text"` is always implicitly included. Only the `main` entry accepts manual specification; `llm`/`vlm`/`omni` in the pool are derived from their key |
| `extra` | extra parameters passed through to the underlying provider (e.g. anthropic's `anthropic_version`) |

## Registering a custom provider

```python
from clawarena_team.provider import BaseProvider, register_provider


class MyProvider(BaseProvider):
    name = "my_provider"

    async def chat(self, *, messages, tools=None, **kwargs):
        ...
        return self.normalise_response(content=..., tool_calls=..., usage=...)


register_provider("my_provider", MyProvider)
```

`register_provider` must be called early in CLI startup (e.g. via the entry_points plugin mechanism; `src/clawarena_team/plugins/` may be added later for this).

## tools / tool_calls protocol

A tool's schema follows the same form as OpenAI function calling:

```python
{"name": "...", "description": "...", "parameters": {"type": "object", ...}}
```

OpenAI-compatible providers internally wrap this as `[{"type": "function", "function": <schema>}]`; the Anthropic provider passes it through directly. The `tool_calls` field in the response must be normalised to `{id, name, arguments(dict)}`, with the provider implementation responsible for parsing JSON strings.

## Relationship to the main agent

The main agent and each subagent hold their own independent `Provider` instances; `ModelBundle.main` is used by the main agent, and `ModelBundle.pool[Modality.X]` is used by the subagent of the corresponding modality. Subagents cannot see provider/api_base/api_key, only `{key, name, modality}`.
