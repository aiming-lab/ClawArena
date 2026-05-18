"""Real OpenClaw backend — executes openclaw CLI via subprocess."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult
from openclaw_env.backend.openclaw_compat import classify_error, rewrite_command


class RealOpenClawBackend(BaseBackend):
    """Backend that runs real `openclaw *` commands via subprocess.

    State inference is done by parsing the *command itself* rather than
    stdout, so evaluators can still track effects in real mode.
    """

    def __init__(self, skip_incompatible_openclaw: bool = True) -> None:
        self._state_dir: str = ""
        self._env: dict[str, str] = {}
        self._skip_incompatible_openclaw = skip_incompatible_openclaw

    # ------------------------------------------------------------------ #
    # BaseBackend interface                                                 #
    # ------------------------------------------------------------------ #

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._state_dir = state_dir
        self._env = {**os.environ, **env_vars}

    def execute_cli(self, command: str) -> CommandResult:
        decision = rewrite_command(
            command,
            skip_incompatible=self._skip_incompatible_openclaw,
        )
        executed_action = decision.executed_action
        injected_workspace = False
        executed_action, injected_workspace = self._inject_agents_workspace(executed_action)

        base_meta: dict[str, Any] = {
            "original_action": decision.original_action,
            "executed_action": executed_action,
            "compat_status": decision.compat_status,
            "error_tags": list(decision.error_tags),
        }
        if injected_workspace:
            tags = list(base_meta.get("error_tags", []))
            tags.append("rewritten_agents_add_workspace")
            base_meta["error_tags"] = list(dict.fromkeys(tags))
            if base_meta.get("compat_status") == "ok":
                base_meta["compat_status"] = "rewritten"

        if decision.compat_status == "skipped_incompatible":
            return CommandResult(
                stdout="",
                stderr=decision.skip_reason or "Skipped incompatible openclaw command.",
                exit_code=125,
                meta=base_meta,
            )

        try:
            args = shlex.split(executed_action)
        except ValueError as exc:
            base_meta["error_tags"] = list(base_meta.get("error_tags", [])) + ["parse_error"]
            return CommandResult(
                stdout="",
                stderr=f"Command parse error: {exc}",
                exit_code=1,
                meta=base_meta,
            )

        try:
            proc = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=30,
                env=self._env,
                cwd=self._workspace_cwd(),
            )
            merged_text = f"{proc.stdout}\n{proc.stderr}"
            tags = list(base_meta["error_tags"]) + classify_error(merged_text)
            deduped_tags = list(dict.fromkeys(tags))
            base_meta["error_tags"] = deduped_tags

            state_changes = self._infer_state_changes(
                executed_action,
                proc.returncode,
            )
            return CommandResult(
                stdout=proc.stdout,
                stderr=proc.stderr,
                exit_code=proc.returncode,
                state_changes=state_changes,
                meta=base_meta,
            )
        except FileNotFoundError:
            base_meta["error_tags"] = list(base_meta.get("error_tags", [])) + ["command_not_found"]
            return CommandResult(
                stdout="",
                stderr=f"Command not found: {args[0] if args else command}",
                exit_code=127,
                meta=base_meta,
            )
        except subprocess.TimeoutExpired:
            base_meta["error_tags"] = list(base_meta.get("error_tags", [])) + ["timeout"]
            return CommandResult(
                stdout="",
                stderr="Command timed out after 30 seconds.",
                exit_code=124,
                meta=base_meta,
            )

    def _inject_agents_workspace(self, command: str) -> tuple[str, bool]:
        """Inject `--workspace <state_dir>/workspace` for non-interactive agents add."""
        try:
            tokens = shlex.split(command)
        except ValueError:
            return command, False

        if tokens[:3] != ["openclaw", "agents", "add"]:
            return command, False
        if "--workspace" in tokens:
            return command, False
        if not self._state_dir:
            return command, False

        workspace = os.path.join(self._state_dir, "workspace")
        tokens.extend(["--workspace", workspace])
        return shlex.join(tokens), True

    def _workspace_cwd(self) -> str | None:
        if not self._state_dir:
            return None
        workspace = os.path.join(self._state_dir, "workspace")
        return workspace if os.path.isdir(workspace) else None

    def execute_python(self, code: str) -> CommandResult:
        return CommandResult(
            stdout="",
            stderr="Python execution is not supported in real backend mode.",
            exit_code=1,
        )

    def get_gateway_status(self) -> dict[str, Any] | None:
        try:
            proc = subprocess.run(
                ["openclaw", "status", "--json"],
                capture_output=True,
                text=True,
                timeout=10,
                env=self._env,
                cwd=self._workspace_cwd(),
            )
            if proc.returncode == 0:
                data = json.loads(proc.stdout)
                return data.get("gateway")
        except Exception:
            pass
        return None

    def get_config(self) -> dict[str, Any]:
        config_path = os.path.join(self._state_dir, "openclaw.json")
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception:
            return {}

    def get_state(self) -> dict[str, Any]:
        state: dict[str, Any] = {}
        try:
            proc = subprocess.run(
                ["openclaw", "agents", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=10,
                env=self._env,
                cwd=self._workspace_cwd(),
            )
            if proc.returncode == 0:
                state["agents"] = json.loads(proc.stdout)
        except Exception:
            state["agents"] = {}

        try:
            proc = subprocess.run(
                ["openclaw", "channels", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=10,
                env=self._env,
                cwd=self._workspace_cwd(),
            )
            if proc.returncode == 0:
                state["channels"] = json.loads(proc.stdout)
        except Exception:
            state["channels"] = {}

        return state

    def cleanup(self) -> None:
        self._env = {}
        self._state_dir = ""

    # ------------------------------------------------------------------ #
    # Internal helpers                                                      #
    # ------------------------------------------------------------------ #

    def _infer_state_changes(
        self, command: str, exit_code: int
    ) -> dict[str, Any] | None:
        """Infer state effects by parsing the command string."""
        if exit_code != 0:
            return None

        try:
            tokens = shlex.split(command)
        except ValueError:
            return None

        if len(tokens) < 2:
            return None

        changes: dict[str, Any] = {}

        # openclaw agents add --name X  OR openclaw agents add X
        if tokens[:3] == ["openclaw", "agents", "add"]:
            name = _flag(tokens, "--name")
            if not name and len(tokens) >= 4 and not tokens[3].startswith("-"):
                name = tokens[3]
            if name:
                changes["agents"] = {name: {"name": name}}

        # openclaw agents set-identity --agent X --emoji Y
        elif tokens[:3] == ["openclaw", "agents", "set-identity"]:
            name = _flag(tokens, "--agent") or _flag(tokens, "--name")
            if not name and len(tokens) >= 4 and not tokens[3].startswith("-"):
                name = tokens[3]
            emoji = _flag(tokens, "--emoji")
            if name:
                payload: dict[str, Any] = {"name": name}
                if emoji:
                    payload["emoji"] = emoji
                changes["agents"] = {name: payload}

        # openclaw message send --target T --message M
        elif tokens[:3] == ["openclaw", "message", "send"]:
            target = _flag(tokens, "--target")
            message = _flag(tokens, "--message")
            channel = _flag(tokens, "--channel")
            if target and message and channel:
                entry: dict[str, Any] = {
                    "target": target,
                    "content": message,
                    "message": message,
                    "channel": channel,
                }
                changes["messages"] = [entry]

        # openclaw channels login --channel C
        elif tokens[:3] == ["openclaw", "channels", "login"]:
            channel = _flag(tokens, "--channel")
            if channel:
                changes["channels"] = {channel: {"name": channel, "status": "connected"}}

        # openclaw plugins install P
        elif (
            tokens[:3] == ["openclaw", "plugins", "install"]
            or tokens[:3] == ["openclaw", "plugins", "enable"]
        ) and len(tokens) >= 4:
            changes["plugins"] = [{"name": tokens[3]}]

        elif tokens[:3] == ["openclaw", "plugins", "disable"] and len(tokens) >= 4:
            changes["plugins"] = [{"name": tokens[3], "status": "disabled"}]

        # openclaw cron add --cron S --message M (or legacy schedule/command)
        elif tokens[:3] == ["openclaw", "cron", "add"]:
            schedule = _flag(tokens, "--cron") or _flag(tokens, "--schedule")
            every = _flag(tokens, "--every")
            cmd = _flag(tokens, "--message") or _flag(tokens, "--command")
            name = _flag(tokens, "--name")
            has_schedule = bool(schedule or every)
            if name and has_schedule and cmd:
                entry = {"name": name}
                if schedule:
                    entry["schedule"] = schedule
                if every:
                    entry["every"] = every
                entry["command"] = cmd
                changes["cron_jobs"] = [entry]

        return changes if changes else None


def _flag(tokens: list[str], name: str) -> str | None:
    """Return the value after a --flag in a token list, or None."""
    try:
        idx = tokens.index(name)
        return tokens[idx + 1] if idx + 1 < len(tokens) else None
    except ValueError:
        return None
