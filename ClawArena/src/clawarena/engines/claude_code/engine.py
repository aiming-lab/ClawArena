"""Claude Code engine — Python SDK runner."""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import signal
from pathlib import Path
from typing import Any

from clawarena.utils import framework_line
from clawarena.core.types import (
    AgentResult, GatewayHandle, NoOpGatewayHandle, RoundContext, RoundResult, WorkCopy,
)
from clawarena.engines.base import AgentEngine

# Default: compact every 25 rounds.  Set CLAWARENA_COMPACT_INTERVAL=0 to disable.
_DEFAULT_COMPACT_INTERVAL = 25

# Injected into the CCR config for OpenAI-compat providers.
# Deletes `request.reasoning` (set by claude CLI via thinking) before forwarding
# to endpoints that reject unknown parameters.
_CCR_STRIP_REASONING_JS = """\
class StripReasoningTransformer {
  constructor() {
    this.name = "stripreasoning";
  }

  async transformRequestIn(request) {
    delete request.reasoning;
    return request;
  }
}

module.exports = StripReasoningTransformer;
"""


class ClaudeCodeEngine(AgentEngine):
    FRAMEWORK = "claude-code"

    def __init__(self) -> None:
        # Track sessions that have already received the one-time resume compact.
        self._compacted_sessions: set[str] = set()

    async def start_gateway(self, work_copy: WorkCopy, port: int) -> GatewayHandle:
        runtime = work_copy.extra.get("_claude_ccr_model")
        if not runtime:
            return NoOpGatewayHandle()
        if not shutil.which("ccr"):
            raise RuntimeError("claude-code-router (ccr) not found in PATH")

        # Resolve to absolute path: the CCR daemon detaches and changes its
        # working directory, so any relative paths embedded in config.json
        # (notably the transformer JS path) would fail with "Cannot find module".
        home_dir = Path(runtime["home_dir"]).resolve()
        cfg_dir = home_dir / ".claude-code-router"
        cfg_dir.mkdir(parents=True, exist_ok=True)
        token = runtime["token"]
        config_path = cfg_dir / "config.json"
        config = self._build_ccr_config(runtime, port, token, cfg_dir)
        config_path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        env = os.environ.copy()
        env["HOME"] = str(home_dir)
        proc = await asyncio.create_subprocess_exec(
            "ccr", "start",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        runtime_info = {
            "home_dir": str(home_dir),
            "port": port,
            "token": token,
            "config_path": str(config_path),
        }
        work_copy.extra["_claude_ccr_runtime"] = runtime_info
        work_copy.extra.setdefault("env_overrides", {}).update(
            self._build_ccr_env(port, token)
        )

        handle = GatewayHandle(
            process=proc,
            port=port,
        )
        handle.stdout_task = asyncio.create_task(
            self._capture_stream(proc.stdout, handle.stdout_chunks),
        )
        handle.stderr_task = asyncio.create_task(
            self._capture_stream(proc.stderr, handle.stderr_chunks),
        )
        handle.ccr_home_dir = home_dir
        handle.ccr_token = token
        return handle

    @staticmethod
    async def _capture_stream(
        stream: asyncio.StreamReader | None, sink: list[str],
    ) -> None:
        if stream is None:
            return
        while True:
            chunk = await stream.read(4096)
            if not chunk:
                return
            sink.append(chunk.decode("utf-8", errors="replace"))

    async def wait_for_gateway(
        self, handle: GatewayHandle, timeout: float = 30.0
    ) -> None:
        home_dir = getattr(handle, "ccr_home_dir", None)
        if home_dir is None:
            return

        deadline = asyncio.get_running_loop().time() + timeout
        last_error = ""
        while asyncio.get_running_loop().time() < deadline:
            if handle.process is not None and handle.process.returncode is not None:
                detail = handle.debug_output()
                raise RuntimeError(
                    "Claude Code router exited early with return code "
                    f"{handle.process.returncode}.\n{detail}".rstrip()
                )
            try:
                reader, writer = await asyncio.open_connection("127.0.0.1", handle.port)
                writer.close()
                await writer.wait_closed()
                return
            except Exception as exc:
                last_error = str(exc)
                await asyncio.sleep(0.2)

        detail = handle.debug_output()
        if last_error:
            detail = (detail + "\n\n" if detail else "") + f"last error: {last_error}"
        raise RuntimeError(
            f"Claude Code router on port {handle.port} did not become ready within {timeout}s.\n"
            f"{detail}".rstrip()
        )

    async def stop_gateway(self, handle: GatewayHandle) -> None:
        home_dir = getattr(handle, "ccr_home_dir", None)
        if home_dir is None:
            await super().stop_gateway(handle)
            return

        env = os.environ.copy()
        env["HOME"] = str(home_dir)
        if handle.process is not None and handle.process.returncode is None:
            handle.process.terminate()
            try:
                await asyncio.wait_for(handle.process.wait(), timeout=5)
            except asyncio.TimeoutError:
                handle.process.kill()
                await handle.process.wait()

        stop_proc = await asyncio.create_subprocess_exec(
            "ccr", "stop",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
        stdout, stderr = await stop_proc.communicate()
        stdout_text = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr.decode("utf-8", errors="replace")
        if stdout_text:
            handle.stdout_chunks.append(stdout_text)
        if stderr_text:
            handle.stderr_chunks.append(stderr_text)

        pid_path = home_dir / ".claude-code-router" / ".claude-code-router.pid"
        if pid_path.exists():
            try:
                pid = int(pid_path.read_text(encoding="utf-8").strip())
                os.kill(pid, signal.SIGTERM)
            except Exception:
                pass
            try:
                pid_path.unlink()
            except Exception:
                pass

        shutil.rmtree(home_dir, ignore_errors=True)
        await super().stop_gateway(handle)

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
        from claude_agent_sdk import (
            query,
            ClaudeAgentOptions,
            AssistantMessage,
            UserMessage,
            ResultMessage,
            TextBlock,
            ToolUseBlock,
            ToolResultBlock,
            CLINotFoundError,
            ProcessError,
        )

        cc = work_copy.extra.get("claude_config", {})
        workspace_path = self._resolve_workspace(work_copy, agent_id or "")

        stderr_lines: list[str] = []

        def _collect_stderr(line: str) -> None:
            stderr_lines.append(line)
            print(framework_line("  [stderr]", line, self.FRAMEWORK), flush=True)

        _cwd = (workspace_path if workspace_path else work_copy.project_root).resolve()
        opts = ClaudeAgentOptions(
            cwd=str(_cwd),
            env={
                "HOME": str(work_copy.state_dir.resolve()),
                "CLAUDE_CONFIG_DIR": str(work_copy.state_dir.resolve()),
                **(cc.get("env") or {}),
                **(work_copy.extra.get("env_overrides", {})),
                **(extra_env or {}),
            },
            permission_mode=cc.get("permission_mode"),
            allowed_tools=cc.get("allowed_tools", []),
            disallowed_tools=cc.get("disallowed_tools", []),
            model=cc.get("model"),
            max_turns=cc.get("max_turns"),
            stderr=_collect_stderr,
        )

        if session_id:
            opts.resume = session_id

        try:
            # One-time resume compact: only fire when explicitly resuming
            # a prior session (resume-infer), to work around proxies that
            # return zero usage fields.
            is_resume = work_copy.extra.get("_is_resume", False)
            resume_compact = os.environ.get("CLAWARENA_RESUME_COMPACT", "1") != "0"
            if is_resume and resume_compact and session_id and session_id not in self._compacted_sessions:
                self._compacted_sessions.add(session_id)
                print(framework_line("  [compact]", f"resume session={session_id}", self.FRAMEWORK), flush=True)
                async for _ in query(prompt="/compact", options=opts):
                    pass

            answer_parts: list[str] = []
            messages: list[dict] = []
            result_msg: ResultMessage | None = None

            async for msg in query(prompt=message, options=opts):
                if isinstance(msg, UserMessage):
                    messages.append(self._serialize_user(msg))
                elif isinstance(msg, AssistantMessage):
                    messages.append(self._serialize_assistant(msg))
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            answer_parts.append(block.text)
                elif isinstance(msg, ResultMessage):
                    result_msg = msg

            answer_text = "\n".join(answer_parts)
            llm_log = self._build_llm_log(
                messages, result_msg, session_id, agent_id,
            )

            if result_msg and result_msg.is_error:
                return AgentResult(
                    status="failed",
                    answer=answer_text,
                    error=result_msg.result,
                    raw=result_msg,
                    llm_log=llm_log,
                )

            return AgentResult(
                status="success",
                answer=answer_text,
                raw=result_msg,
                llm_log=llm_log,
            )

        except CLINotFoundError as e:
            return AgentResult(status="failed", answer="", error=str(e))
        except ProcessError as e:
            stderr_text = "\n".join(stderr_lines) if stderr_lines else e.stderr
            return AgentResult(
                status="failed", answer="",
                error=f"exit={e.exit_code}: {stderr_text}",
                returncode=e.exit_code,
            )
        except (asyncio.TimeoutError, TimeoutError):
            return AgentResult(
                status="timeout", answer="",
                error=f"Timeout after {timeout}s", returncode=-1,
            )
        except Exception as e:
            stderr_text = "\n".join(stderr_lines) if stderr_lines else ""
            diag = self._format_diagnostic(
                opts, session_id, agent_id, stderr_text, str(e),
            )
            print(diag, flush=True)
            return AgentResult(status="failed", answer="", error=diag)

    # ── periodic compaction via round hook ──

    async def on_round_complete(self, ctx: RoundContext) -> RoundResult | None:
        if not ctx.session_id or ctx.work_copy is None:
            return None

        cc = ctx.work_copy.extra.get("claude_config", {})

        # Priority: env var > claude_config > default
        env_val = os.environ.get("CLAWARENA_COMPACT_INTERVAL")
        if env_val is not None:
            interval = int(env_val)
        else:
            interval = int(cc.get("compact_interval", _DEFAULT_COMPACT_INTERVAL))
        if interval <= 0:
            return None

        # round_index is 0-based; compact after every `interval` rounds
        # e.g. interval=25 → compact after round 24, 49, 74, ...
        round_num = ctx.round_index + 1
        if round_num < interval or round_num % interval != 0:
            return None

        from claude_agent_sdk import query, ClaudeAgentOptions
        workspace_path = self._resolve_workspace(ctx.work_copy, ctx.test_id)

        _cwd = (workspace_path if workspace_path else ctx.work_copy.project_root).resolve()
        opts = ClaudeAgentOptions(
            cwd=str(_cwd),
            env={
                "HOME": str(ctx.work_copy.state_dir.resolve()),
                "CLAUDE_CONFIG_DIR": str(ctx.work_copy.state_dir.resolve()),
                **(cc.get("env") or {}),
            },
            permission_mode=cc.get("permission_mode"),
            model=cc.get("model"),
            max_turns=1,
            resume=ctx.session_id,
        )

        print(framework_line("  [compact]", f"periodic round={round_num} session={ctx.session_id}", self.FRAMEWORK), flush=True)
        async for _ in query(prompt="/compact", options=opts):
            pass

        return None

    # ── diagnostics ──

    @staticmethod
    def _format_diagnostic(
        opts, session_id: str | None, agent_id: str | None,
        stderr_text: str, error_msg: str,
    ) -> str:
        lines = [framework_line("  [error]", f"agent={agent_id} session={session_id}", ClaudeCodeEngine.FRAMEWORK)]
        lines.append(f"          cwd={opts.cwd}")
        lines.append(f"          CLAUDE_CONFIG_DIR={opts.env.get('CLAUDE_CONFIG_DIR', '?')}")
        if stderr_text:
            lines.append(f"          stderr: {stderr_text}")
        lines.append(f"          exception: {error_msg}")
        lines.append(
            f"          reproduce: CLAUDE_CONFIG_DIR={opts.env.get('CLAUDE_CONFIG_DIR', '')} "
            f"claude --resume {session_id or ''} -p '...' --cwd {opts.cwd}"
        )
        return "\n".join(lines)

    @staticmethod
    def _normalize_ccr_api_base(api_base: str) -> str:
        base = api_base.rstrip("/")
        if base.endswith("/chat/completions") or base.endswith("/v1/messages"):
            return base
        return base + "/chat/completions"

    def _build_ccr_config(self, runtime: dict, port: int, token: str, cfg_dir: Path) -> dict:
        provider_name = runtime["provider"]
        model_id = runtime["model_id"]
        provider_entry: dict[str, Any] = {
            "name": provider_name,
            "api_base_url": self._normalize_ccr_api_base(runtime["api_base"]),
            "api_key": runtime["api_key"],
            "models": [model_id],
        }
        transformers = self._ccr_transformer(provider_name)
        if transformers:
            provider_entry["transformer"] = {"use": list(transformers)}

        route_target = f"{provider_name},{model_id}"
        config: dict[str, Any] = {
            "PORT": port,
            "APIKEY": token,
            "LOG": False,
            "API_TIMEOUT_MS": 600000,
            "NON_INTERACTIVE_MODE": False,
            "Providers": [provider_entry],
            "Router": {
                "default": route_target,
                "background": route_target,
            },
        }

        if transformers and "stripreasoning" in transformers:
            js_path = cfg_dir / "strip_reasoning.js"
            js_path.write_text(_CCR_STRIP_REASONING_JS, encoding="utf-8")
            config["transformers"] = [{"path": str(js_path)}]

        return config

    # Providers that speak native OpenAI-compatible chat/completions.
    # `stripreasoning` strips the top-level `reasoning` field that claude CLI
    # injects and that OpenAI-compat endpoints reject with "Unknown parameter".
    # `maxcompletiontokens` renames `max_tokens` → `max_completion_tokens` for
    # o-series / gpt-5-style models.
    _OPENAI_COMPAT_PROVIDERS = frozenset({
        "openai", "azure", "ollama",
        "deepseek", "moonshot", "glm", "groq", "xai",
        "qwen", "minimax", "mistral",
    })

    @staticmethod
    def _ccr_transformer(provider_name: str) -> list[str] | None:
        if provider_name == "openrouter":
            return ["openrouter"]
        if provider_name == "google":
            return ["gemini"]
        if provider_name in ClaudeCodeEngine._OPENAI_COMPAT_PROVIDERS:
            return ["stripreasoning", "maxcompletiontokens"]
        return None

    @staticmethod
    def _build_ccr_env(port: int, token: str) -> dict[str, str]:
        return {
            "ANTHROPIC_BASE_URL": f"http://127.0.0.1:{port}",
            "ANTHROPIC_AUTH_TOKEN": token,
            "NO_PROXY": "127.0.0.1",
            "DISABLE_TELEMETRY": "true",
            "DISABLE_COST_WARNINGS": "true",
            "API_TIMEOUT_MS": str(600000),
        }

    # ── message serialization ──

    @staticmethod
    def _serialize_user(msg) -> dict:
        content = msg.content
        if isinstance(content, str):
            blocks = [{"type": "text", "text": content}]
        elif isinstance(content, list):
            blocks = [ClaudeCodeEngine._serialize_block(b) for b in content]
        else:
            blocks = [{"type": "text", "text": str(content)}]
        return {"role": "user", "content": blocks}

    @staticmethod
    def _serialize_assistant(msg) -> dict:
        blocks = [ClaudeCodeEngine._serialize_block(b) for b in msg.content]
        entry: dict = {"role": "assistant", "content": blocks}
        if msg.model:
            entry["model"] = msg.model
        if msg.usage:
            entry["usage"] = msg.usage
        if msg.stop_reason:
            entry["stopReason"] = msg.stop_reason
        return entry

    @staticmethod
    def _serialize_block(block) -> dict:
        from claude_agent_sdk import TextBlock, ToolUseBlock, ToolResultBlock, ThinkingBlock
        if isinstance(block, TextBlock):
            return {"type": "text", "text": block.text}
        if isinstance(block, ToolUseBlock):
            return {
                "type": "toolCall",
                "id": block.id,
                "name": block.name,
                "arguments": block.input,
            }
        if isinstance(block, ToolResultBlock):
            return {
                "type": "toolResult",
                "tool_use_id": block.tool_use_id,
                "content": block.content,
                "is_error": block.is_error,
            }
        if isinstance(block, ThinkingBlock):
            return {"type": "thinking", "thinking": block.thinking}
        return {"type": "unknown", "data": str(block)}

    @staticmethod
    def _trim_to_last_turn(messages: list[dict]) -> list[dict]:
        """Keep only the last user question (non-tool-result) and everything after it."""
        for i in range(len(messages) - 1, -1, -1):
            msg = messages[i]
            if msg.get("role") != "user":
                continue
            # skip pure tool-result user messages
            blocks = msg.get("content", [])
            if all(b.get("type") == "toolResult" for b in blocks):
                continue
            return messages[i:]
        return messages

    @staticmethod
    def _build_llm_log(
        messages: list[dict],
        result_msg,
        session_id: str | None,
        agent_id: str | None,
    ) -> dict:
        turn_messages = ClaudeCodeEngine._trim_to_last_turn(messages)
        log: dict = {
            "agentId": agent_id or "",
            "sessionId": session_id or "",
            "success": result_msg.subtype == "success" if result_msg else False,
            "messageCount": len(turn_messages),
            "messages": turn_messages,
        }
        if result_msg:
            log["durationMs"] = getattr(result_msg, "duration_ms", 0)
            log["numTurns"] = getattr(result_msg, "num_turns", 0)
            usage = getattr(result_msg, "usage", None)
            if usage:
                log["usage"] = usage
            cost = getattr(result_msg, "total_cost_usd", None)
            if cost is not None:
                log["totalCostUsd"] = cost
            model_usage = getattr(result_msg, "model_usage", None)
            if model_usage:
                log["modelUsage"] = model_usage
        return log

    @staticmethod
    def _resolve_workspace(work_copy: WorkCopy, agent_id: str) -> Path | None:
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.workspace_root
