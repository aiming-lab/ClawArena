"""
Nanobot runner used by clawarena NanobotEngine.

Applies compatibility patches before delegating to the nanobot CLI.
Patches are gated by env vars so this script is safe to distribute
and won't affect users who run it outside of clawarena.

Usage (by clawarena engine, not directly):
    python nanobot_runner.py agent -m <msg> -s <session> -w <ws> -c <cfg>
"""

from __future__ import annotations

import os
import sys


# ---------------------------------------------------------------------------
# Patch: strip legacy max_tokens for newer OpenAI-compatible endpoints
# ---------------------------------------------------------------------------
# Some endpoints (e.g. gpt-5.1 via compatible proxies) reject max_tokens
# and require max_completion_tokens only.  Nanobot currently sends both.
# Enable by setting CLAWARENA_NANOBOT_NO_MAX_TOKENS=1.

def _patch_strip_max_tokens() -> None:
    try:
        from nanobot.providers import openai_compat_provider as _m  # type: ignore

        _orig = _m.OpenAICompatProvider._build_kwargs

        def _patched(
            self,
            messages,
            tools,
            model,
            max_tokens,
            temperature,
            reasoning_effort,
            tool_choice,
        ):
            kw = _orig(
                self, messages, tools, model, max_tokens,
                temperature, reasoning_effort, tool_choice,
            )
            kw.pop("max_tokens", None)
            return kw

        _m.OpenAICompatProvider._build_kwargs = _patched
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Patch: agent_end LLM log — capture full message snapshot after each turn
# ---------------------------------------------------------------------------
# Writes a JSON file per agent turn to CLAWARENA_NANOBOT_LOG_DIR/<session_key>/.
# Format matches openclaw's llm-prompt-logger agent_end event so that
# clawarena's read_llm_log / trim_llm_log_messages pipeline works unchanged.
# Enable by setting CLAWARENA_NANOBOT_LOG_DIR=<path>.

def _patch_log_llm() -> None:
    import contextvars
    import json
    import time
    from datetime import datetime, timezone
    from pathlib import Path

    log_root = Path(os.environ["CLAWARENA_NANOBOT_LOG_DIR"])

    # Carries the active session_key through the async call chain so that
    # the _run_agent_loop patch can identify which session is being served
    # without any explicit parameter threading.
    _session_key_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
        "hbench_nanobot_session_key", default=None
    )

    def _iso_now() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

    def _filename_ts() -> str:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%dT%H-%M-%S-") + f"{now.microsecond // 1000:03d}Z"

    def _write_agent_end(
        session_key: str,
        messages: list,
        duration_s: float,
        usage: dict,
        success: bool,
    ) -> None:
        session_dir = log_root / session_key
        try:
            session_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            return
        data = {
            "stage": "agent_end",
            "timestamp": _iso_now(),
            "sessionKey": session_key,
            "success": success,
            "durationMs": round(duration_s * 1000, 1),
            "messageCount": len(messages),
            "messages": messages,
            "usage": usage,
        }
        fname = f"{_filename_ts()}_agent-end.json"
        try:
            (session_dir / fname).write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

    try:
        from nanobot.agent import loop as _loop_mod  # type: ignore

        _orig_process = _loop_mod.AgentLoop._process_message
        _orig_run = _loop_mod.AgentLoop._run_agent_loop

        async def _patched_process(self, msg, session_key=None, **kw):
            key = session_key or msg.session_key
            token = _session_key_var.set(key)
            try:
                return await _orig_process(self, msg, session_key=session_key, **kw)
            finally:
                _session_key_var.reset(token)

        async def _patched_run_agent_loop(self, initial_messages, **kw):
            t0 = time.monotonic()
            result = await _orig_run(self, initial_messages, **kw)
            final_content, _tools_used, messages = result
            session_key = _session_key_var.get()
            if session_key:
                _write_agent_end(
                    session_key=session_key,
                    messages=messages,
                    duration_s=time.monotonic() - t0,
                    usage=dict(self._last_usage),
                    success=final_content is not None,
                )
            return result

        _loop_mod.AgentLoop._process_message = _patched_process
        _loop_mod.AgentLoop._run_agent_loop = _patched_run_agent_loop
    except Exception:
        pass


if os.environ.get("CLAWARENA_NANOBOT_NO_MAX_TOKENS") == "1":
    _patch_strip_max_tokens()

if os.environ.get("CLAWARENA_NANOBOT_LOG_DIR"):
    _patch_log_llm()


# ---------------------------------------------------------------------------
# Delegate to nanobot CLI — sys.argv passes through unchanged
# ---------------------------------------------------------------------------

from nanobot.cli.commands import app  # noqa: E402  # type: ignore

app()
