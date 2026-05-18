"""Cleaning helpers for online trajectory stdout/stderr fields."""

from __future__ import annotations

import re


_NOISE_SUBSTRINGS = (
    "Compatibility config keys detected",
    "Doctor changes",
    "Run \"openclaw doctor --fix\"",
    "Legacy config keys detected",
    "Invalid config at",
    "Config invalid",
    "File: ~/openclaw.json",
    "Problem:",
    "agent.* was moved; use agents.defaults",
    "agent.model string was replaced by",
    "Migrated agent.model string",
    "Moved agent",
)


def clean_openclaw_output(stdout: str, stderr: str | None) -> tuple[str, str]:
    """Remove common compatibility noise while preserving actionable errors."""
    clean_stdout = _clean_text(stdout or "")
    clean_stderr = _clean_text(stderr or "")
    return clean_stdout, clean_stderr


def _clean_text(text: str) -> str:
    lines = text.splitlines()
    kept: list[str] = []
    for line in lines:
        stripped = line.strip()
        if _is_noise_line(stripped):
            continue
        if kept and kept[-1] == stripped:
            continue
        kept.append(stripped)

    # Collapse excessive blank lines.
    compact: list[str] = []
    previous_blank = False
    for line in kept:
        blank = line == ""
        if blank and previous_blank:
            continue
        compact.append(line)
        previous_blank = blank

    return "\n".join(compact).strip()


def _is_noise_line(stripped: str) -> bool:
    if not stripped:
        return False
    if any(s in stripped for s in _NOISE_SUBSTRINGS):
        return True
    # Box-drawing decorations emitted by OpenClaw doctor compatibility output.
    if re.fullmatch(r"[|\\-_/<>.=*`~#:\[\]{}()]+", stripped):
        return True
    if all(ch in "│├┤╭╮╰╯─◇◆○●◼◻" for ch in stripped):
        return True
    return False
