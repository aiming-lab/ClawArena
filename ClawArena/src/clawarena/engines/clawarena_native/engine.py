"""clawarena-native engine —— 纯 Python、进程内 agent loop（移植自 ArcBench harness）。

与现有 engine 的根本区别：不 shell 调外部二进制，而是直接在进程内用 vendored harness
（``clawarena.native``）跑 agent loop，自己直连 LLM provider。harness、工具、system prompt、
compaction、<system-reminder> 全部由固定 Python 代码实现，benchmark 因此可复现、可公平比较。

ClawArena 按 round 调一次 :meth:`run_agent`；harness 的 :class:`SessionLog` 每次从磁盘
重读，故"每 round 用同一 active session jsonl 重建 harness"即可续接多 round 对话。
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from clawarena.core.types import AgentResult, WorkCopy
from clawarena.engines.base import AgentEngine

# ClawArena ModelConfig.provider → native provider 名映射。
_PROVIDER_MAP: dict[str, str] = {
    "anthropic": "anthropic",
    "claude": "anthropic",
    "bedrock": "anthropic",
    "google": "gemini",
    "gemini": "gemini",
    "openai": "openai_compat",
    "azure": "openai_compat",
    "ollama": "openai_compat",
    "openrouter": "openai_compat",
    "groq": "openai_compat",
    "mistral": "openai_compat",
    "xai": "openai_compat",
    "qwen": "openai_compat",
    "moonshot": "openai_compat",
    "glm": "openai_compat",
    "minimax": "openai_compat",
}


def native_model_json_from_claw(model: Any) -> dict[str, Any]:
    """把 ClawArena 的 ModelConfig 映射成 native ``parse_model_json`` 接受的扁平 dict。"""
    provider = _PROVIDER_MAP.get(getattr(model, "provider", "openai"), "openai_compat")
    try:
        api_base = model.resolved_api_base()
    except Exception:  # noqa: BLE001
        api_base = getattr(model, "api_base", "") or ""
    extra = getattr(model, "extra", {}) or {}
    modalities = extra.get("modalities") or ["text"]
    out: dict[str, Any] = {
        "provider": provider,
        "model_id": getattr(model, "model_id", ""),
        "modalities": list(modalities),
    }
    if api_base:
        out["api_base"] = api_base
    if getattr(model, "api_key", None):
        out["api_key"] = model.api_key
    return out


class ClawArenaNativeEngine(AgentEngine):
    """进程内 native harness engine。"""

    def __init__(self) -> None:
        self._config_dict: dict[str, Any] | None = None

    def _config(self) -> dict[str, Any]:
        if self._config_dict is None:
            from clawarena.native.config import load_config

            self._config_dict = load_config().as_dict()
        return self._config_dict

    def _agent_id(self, work_copy: WorkCopy, test_id: str | None) -> str:
        agents = work_copy.extra.get("manifest", {}).get("agents", {})
        return agents.get(test_id, {}).get("agent_id", test_id or "main")

    async def run_agent(
        self,
        session_id: str,
        message: str,
        work_copy: WorkCopy,
        agent_id: str | None = None,
        gateway_port: int | None = None,
        timeout: float | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> AgentResult:
        from clawarena.native.assembly import build_main_harness
        from clawarena.native.provider.registry import parse_model_json

        test_id = agent_id
        model_json = work_copy.extra.get("native_model")
        if not model_json:
            return AgentResult(
                status="failed",
                answer="",
                error="clawarena-native: no model configured (set --model-id / tests.json model).",
                returncode=-1,
                llm_log=None,
            )

        errors: list[str] = []
        bundle = parse_model_json(model_json, models_defaults={}, errors=errors)
        if errors:
            return AgentResult(
                status="failed", answer="", error="; ".join(errors), returncode=-1, llm_log=None
            )

        aid = self._agent_id(work_copy, test_id)
        sessions_dir = work_copy.state_dir / aid
        active_jsonl = sessions_dir / f"{session_id}.jsonl"
        workspace = work_copy.workspace_root / aid if work_copy.workspace_root else work_copy.state_dir
        config_dict = self._config()

        env_reminder = (
            "Environment\n"
            f"  benchmark: clawarena-native\n"
            f"  test_id: {test_id}\n"
            f"  session_id: {session_id}\n"
            f"  cwd: {workspace}\n"
            f"  accessible_paths (you can Read/Write/Edit/Bash here): {workspace}\n"
            f"  token_limit: {config_dict.get('token_limits', {}).get('main_agent', 200000)}"
        )

        try:
            harness = build_main_harness(
                bundle=bundle,
                config_dict=config_dict,
                workspace_root=Path(workspace),
                sessions_dir=sessions_dir,
                active_session_jsonl=active_jsonl,
                active_session_id=session_id,
                env_reminder=env_reminder,
            )
            coro = harness.send_user(message, is_real_question=True)
            answer = await (asyncio.wait_for(coro, timeout) if timeout else coro)
        except asyncio.TimeoutError:
            return AgentResult(
                status="timeout",
                answer="",
                error=f"Timeout after {timeout}s",
                returncode=-1,
                llm_log=None,
            )
        except Exception as e:  # noqa: BLE001
            return AgentResult(
                status="failed",
                answer="",
                error=f"{type(e).__name__}: {e}",
                returncode=-1,
                llm_log=None,
            )

        return AgentResult(
            status="success",
            answer=answer if isinstance(answer, str) else str(answer),
            error=None,
            returncode=0,
            llm_log=None,
        )
