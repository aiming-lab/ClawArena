"""Safety guard to prevent agents from executing dangerous operations."""

from __future__ import annotations

import re


class SafetyViolation(Exception):
    """Raised when an agent attempts a blocked action."""


BLOCKED_PATTERNS = [
    re.compile(r"rm\s+-rf\s+/"),
    re.compile(r"rm\s+-rf\s+~"),
    re.compile(r"openclaw\s+reset\s+--hard"),
    re.compile(r"openclaw\s+uninstall"),
    re.compile(r"sudo\s+"),
    re.compile(r"chmod\s+777"),
    re.compile(r">\s*/dev/"),
    re.compile(r"mkfs"),
    re.compile(r"dd\s+if="),
    re.compile(r":\(\)\s*\{"),  # fork bomb
]

ALLOWED_COMMAND_PREFIXES = [
    "openclaw status",
    "openclaw health",
    "openclaw agents",
    "openclaw agent ",
    "openclaw message",
    "openclaw channels",
    "openclaw config",
    "openclaw configure",
    "openclaw setup",
    "openclaw onboard",
    "openclaw logs",
    "openclaw sessions",
    "openclaw doctor",
    "openclaw models",
    "openclaw plugins",
    "openclaw skills",
    "openclaw cron",
    "openclaw webhooks",
    "openclaw security",
    "openclaw devices",
    "openclaw nodes",
    "openclaw dns",
    "openclaw hooks",
    "openclaw system",
    "openclaw sandbox",
    "openclaw tui",
    "openclaw completion",
    "openclaw acp",
    "openclaw gateway",
    "openclaw pairing",
    "openclaw directory",
    "openclaw approvals",
    # New app command prefixes
    "calendar ",
    "gcalcli ",
    "email ",
    "weather ",
    "file ",
    "tasks ",
    "curl ",
    # Allow basic inspection commands
    "cat ",
    "ls ",
    "echo ",
    "grep ",
    "head ",
    "tail ",
    "wc ",
    "jq ",
    "pwd",
    "whoami",
    "env",
    "printenv",
]


def check_command_safety(command: str, strict: bool = True) -> None:
    """Validate that a CLI command is safe to execute.

    Raises SafetyViolation if the command matches a blocked pattern.
    When strict=True (default), also enforces the allowed-prefix allowlist.
    When strict=False, only blocked patterns are checked (for real backends).
    """
    command = command.strip()

    for pattern in BLOCKED_PATTERNS:
        if pattern.search(command):
            raise SafetyViolation(
                f"Blocked dangerous command pattern: {pattern.pattern}"
            )

    if strict and not any(command.startswith(prefix) for prefix in ALLOWED_COMMAND_PREFIXES):
        raise SafetyViolation(
            f"Command not in allowed list. Must start with one of: "
            f"{', '.join(p for p in ALLOWED_COMMAND_PREFIXES[:10])}..."
        )


def check_python_safety(code: str) -> None:
    """Validate that Python code is safe to execute.

    Raises SafetyViolation for dangerous operations.
    """
    dangerous_patterns = [
        re.compile(r"os\.system\("),
        re.compile(r"subprocess\.(run|call|Popen|check_output)\("),
        re.compile(r"shutil\.rmtree\("),
        re.compile(r"os\.remove\("),
        re.compile(r"os\.unlink\("),
        re.compile(r"__import__\("),
        re.compile(r"exec\("),
        re.compile(r"eval\("),
        re.compile(r"open\(.*(w|a)\)"),
    ]

    for pattern in dangerous_patterns:
        if pattern.search(code):
            raise SafetyViolation(
                f"Blocked dangerous Python pattern: {pattern.pattern}"
            )
