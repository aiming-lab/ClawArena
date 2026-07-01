"""File system app backend — virtual in-memory file system."""

from __future__ import annotations
import shlex

import posixpath
from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult


def _get_arg(args: list[str], flag: str, default: str | None = None) -> str | None:
    for i, a in enumerate(args):
        if a == flag and i + 1 < len(args):
            return args[i + 1]
    return default


class FileSystemBackend(BaseBackend):
    """Mock virtual file system backend."""

    def __init__(self) -> None:
        self._files: dict[str, str] = {}  # path -> content
        self._initialized = False

    # ------------------------------------------------------------------ #
    # BaseBackend interface                                                 #
    # ------------------------------------------------------------------ #

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._files = {}
        self._initialized = True

    def execute_cli(self, command: str) -> CommandResult:
        parts = shlex.split(command.strip())
        if not parts or parts[0] != "file":
            return CommandResult(stdout="", stderr="Not a file command", exit_code=1)

        if len(parts) < 2:
            return CommandResult(
                stdout="file <subcommand> [options]\n"
                       "Subcommands: create, read, delete, list, move, append",
                stderr="",
                exit_code=0,
            )

        sub = parts[1]
        args = parts[2:]

        handlers = {
            "create": self._cmd_create,
            "read": self._cmd_read,
            "delete": self._cmd_delete,
            "list": self._cmd_list,
            "move": self._cmd_move,
            "append": self._cmd_append,
        }

        handler = handlers.get(sub)
        if handler is None:
            return CommandResult(stdout="", stderr=f"Unknown file subcommand: {sub}", exit_code=1)
        return handler(args)

    def execute_python(self, code: str) -> CommandResult:
        return CommandResult(stdout="", stderr="Python interface not supported for FileSystemBackend", exit_code=1)

    def get_gateway_status(self) -> dict[str, Any] | None:
        return None

    def get_config(self) -> dict[str, Any]:
        return {}

    def cleanup(self) -> None:
        self._files = {}
        self._initialized = False

    def get_state(self) -> dict[str, Any]:
        return {"files": {k: v for k, v in self._files.items()}}

    # ------------------------------------------------------------------ #
    # Command handlers                                                      #
    # ------------------------------------------------------------------ #

    def _cmd_create(self, args: list[str]) -> CommandResult:
        path = _get_arg(args, "--path")
        content = _get_arg(args, "--content", "")

        if not path:
            return CommandResult(stdout="", stderr="--path is required", exit_code=1)

        path = _normalize(path)
        self._files[path] = content or ""

        return CommandResult(
            stdout=f"File created: {path}",
            stderr="",
            exit_code=0,
            state_changes={"files_created": [{"path": path}]},
        )

    def _cmd_read(self, args: list[str]) -> CommandResult:
        path = _get_arg(args, "--path")

        if not path:
            return CommandResult(stdout="", stderr="--path is required", exit_code=1)

        path = _normalize(path)
        if path not in self._files:
            return CommandResult(
                stdout="", stderr=f"File not found: {path}", exit_code=1
            )

        return CommandResult(stdout=self._files[path], stderr="", exit_code=0)

    def _cmd_delete(self, args: list[str]) -> CommandResult:
        path = _get_arg(args, "--path")

        if not path:
            return CommandResult(stdout="", stderr="--path is required", exit_code=1)

        path = _normalize(path)
        if path not in self._files:
            return CommandResult(
                stdout="", stderr=f"File not found: {path}", exit_code=1
            )

        del self._files[path]
        return CommandResult(
            stdout=f"File deleted: {path}",
            stderr="",
            exit_code=0,
            state_changes={"files_deleted": [{"path": path}]},
        )

    def _cmd_list(self, args: list[str]) -> CommandResult:
        prefix = _get_arg(args, "--path", "/")
        prefix = _normalize(prefix)

        matches = sorted(
            p for p in self._files if p.startswith(prefix)
        )

        if not matches:
            return CommandResult(
                stdout=f"No files under {prefix}.", stderr="", exit_code=0
            )

        lines = [f"Files under {prefix}:"]
        for p in matches:
            size = len(self._files[p])
            lines.append(f"  {p}  ({size} bytes)")
        return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

    def _cmd_move(self, args: list[str]) -> CommandResult:
        src = _get_arg(args, "--src")
        dst = _get_arg(args, "--dst")

        if not src:
            return CommandResult(stdout="", stderr="--src is required", exit_code=1)
        if not dst:
            return CommandResult(stdout="", stderr="--dst is required", exit_code=1)

        src = _normalize(src)
        dst = _normalize(dst)

        if src not in self._files:
            return CommandResult(stdout="", stderr=f"File not found: {src}", exit_code=1)

        self._files[dst] = self._files.pop(src)
        return CommandResult(
            stdout=f"File moved: {src} → {dst}",
            stderr="",
            exit_code=0,
        )

    def _cmd_append(self, args: list[str]) -> CommandResult:
        path = _get_arg(args, "--path")
        content = _get_arg(args, "--content")

        if not path:
            return CommandResult(stdout="", stderr="--path is required", exit_code=1)
        if content is None:
            return CommandResult(stdout="", stderr="--content is required", exit_code=1)

        path = _normalize(path)
        if path not in self._files:
            return CommandResult(stdout="", stderr=f"File not found: {path}", exit_code=1)

        self._files[path] += content
        return CommandResult(
            stdout=f"Content appended to {path}.",
            stderr="",
            exit_code=0,
        )


def _normalize(path: str) -> str:
    """Normalize a virtual path (ensure leading /)."""
    if not path.startswith("/"):
        path = "/" + path
    return posixpath.normpath(path)
