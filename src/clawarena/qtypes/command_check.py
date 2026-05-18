"""Shared command-check helpers for qtypes."""

from __future__ import annotations

import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any

from clawarena.core.types import TestContext

# Matches ${eval_dir}-prefixed path tokens in shell commands.
# Stops at whitespace and common shell metacharacters.
_EVAL_DIR_PATH_RE = re.compile(r"\$\{eval_dir\}[^\s'\";&|><()`]*")

# Matches ${workspace}-prefixed path tokens (for optional existence warning).
_WORKSPACE_PATH_RE = re.compile(r"\$\{workspace\}[^\s'\";&|><()`]*")

# Known placeholder names and how to resolve them from TestContext.
_PLACEHOLDER_RESOLVERS: dict[str, Any] = {
    "workspace": lambda ctx: ctx.get("workspace"),
    "eval_dir": lambda ctx: ctx.get("eval_dir"),
    "test_id": lambda ctx: ctx.get("test_id"),
    "agent_id": lambda ctx: ctx.get("agent_id"),
    "state_dir": lambda ctx: _resolve_state_dir(ctx),
}


def _resolve_state_dir(ctx: TestContext) -> Path | None:
    wc = ctx.get("work_copy")
    return wc.state_dir if wc is not None else None


def expand_placeholders(template: str, ctx: TestContext) -> str:
    """Replace known ``${var}`` placeholders with values from *ctx*."""

    def _replace(m: re.Match) -> str:
        name = m.group(1)
        resolver = _PLACEHOLDER_RESOLVERS.get(name)
        if resolver is None:
            return m.group(0)
        value = resolver(ctx)
        if value is None:
            return m.group(0)
        return shlex.quote(str(value))

    return re.sub(r"\$\{([^}]+)\}", _replace, template)


def workspace_check_enabled() -> bool:
    """Return True when OMIT_WORKSPACE=0 is explicitly set."""
    return os.environ.get("OMIT_WORKSPACE") == "0"


def check_workspace_files(command: str, workspace: Path, prefix: str) -> list[str]:
    """Warn about ${workspace}/... paths that don't exist in the static workspace."""
    warnings = []
    for m in _WORKSPACE_PATH_RE.finditer(command):
        raw = m.group(0)
        resolved = raw.replace("${workspace}", str(workspace))
        if not Path(resolved).exists():
            warnings.append(
                f"{prefix}: workspace file not found (may be agent-created): {resolved}"
            )
    return warnings


def check_eval_dir_files(
    command: str, eval_dir: Path, scenario: str, prefix: str
) -> list[str]:
    """Check that every ${eval_dir}/... path referenced in *command* exists."""
    errors = []
    for m in _EVAL_DIR_PATH_RE.finditer(command):
        raw = m.group(0)
        resolved = (
            raw
            .replace("${eval_dir}", str(eval_dir))
            .replace("${agent_id}", scenario)
            .replace("${test_id}", scenario)
        )
        if not Path(resolved).exists():
            errors.append(f"{prefix}: eval_dir file not found: {resolved}")
    return errors


def run_command_check(command_cfg: dict, ctx: TestContext) -> dict[str, Any]:
    """Execute a shell command check and return a normalized result dict."""
    raw_command = command_cfg.get("command", "")
    if not raw_command:
        return {"passed": False, "exit_code": -1, "stdout": "", "stderr": "no command"}

    command = expand_placeholders(raw_command, ctx)
    timeout = float(command_cfg.get("timeout", 30))
    expect_exit = command_cfg.get("expect_exit", 0)
    expect_stdout = command_cfg.get("expect_stdout")
    expect_stdout_regex = command_cfg.get("expect_stdout_regex", False)

    workspace = ctx.get("workspace")
    cwd = str(workspace) if workspace else None

    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        passed = proc.returncode == expect_exit
        if passed and expect_stdout is not None:
            if expect_stdout_regex:
                passed = bool(re.search(expect_stdout, proc.stdout))
            else:
                passed = expect_stdout in proc.stdout
        return {
            "passed": passed,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Timeout after {timeout}s",
        }
    except Exception as exc:
        return {"passed": False, "exit_code": -1, "stdout": "", "stderr": str(exc)}


def append_pref_feedback(text: str, pref: dict | None, pref_passed: bool) -> str:
    """Append preference feedback when present and non-empty."""
    if not isinstance(pref, dict):
        return text
    pref_fb = pref.get("feedback", {})
    if not isinstance(pref_fb, dict):
        return text
    pref_text = pref_fb.get("correct" if pref_passed else "incorrect", "")
    if not pref_text:
        return text
    return f"{text}\n{pref_text}".strip() if text else pref_text


def validate_pref_config(
    pref: dict | None,
    scenario: str,
    round_id: str,
    owner: str,
    eval_dir: Path | None = None,
    workspace: Path | None = None,
) -> tuple[list[str], list[str]]:
    """Validate a pref command config and referenced paths."""
    errors: list[str] = []
    warnings: list[str] = []
    if pref is None:
        return errors, warnings
    if not isinstance(pref, dict):
        errors.append(f"{scenario}: round '{round_id}': {owner} 'pref' must be a dict")
        return errors, warnings

    _PREF_REQUIRED = {"command", "feedback"}
    _PREF_OPTIONAL = {"rules", "expect_exit"}
    _PREF_ALLOWED = _PREF_REQUIRED | _PREF_OPTIONAL
    extra_pref = set(pref.keys()) - _PREF_ALLOWED
    if extra_pref:
        errors.append(
            f"{scenario}: round '{round_id}': {owner} pref has unexpected fields: {sorted(extra_pref)}"
        )

    pref_command = pref.get("command", "")
    if not isinstance(pref_command, str) or not pref_command:
        errors.append(
            f"{scenario}: round '{round_id}': {owner} pref.command must be non-empty string"
        )
        return errors, warnings

    pref_fb = pref.get("feedback", {})
    if not isinstance(pref_fb, dict):
        errors.append(f"{scenario}: round '{round_id}': {owner} pref.feedback must be a dict")
    else:
        extra_pref_fb = set(pref_fb.keys()) - {"correct", "incorrect"}
        if extra_pref_fb:
            errors.append(
                f"{scenario}: round '{round_id}': {owner} pref.feedback has unexpected fields: {sorted(extra_pref_fb)}"
            )
        for key in ("correct", "incorrect"):
            if key in pref_fb and not isinstance(pref_fb.get(key), str):
                errors.append(
                    f"{scenario}: round '{round_id}': {owner} pref.feedback.{key} must be string"
                )

    prefix = f"{scenario}: round '{round_id}'"
    if eval_dir is not None:
        errors.extend(check_eval_dir_files(pref_command, eval_dir, scenario, prefix))
    if workspace is not None and workspace_check_enabled():
        warnings.extend(check_workspace_files(pref_command, workspace, prefix))

    return errors, warnings
