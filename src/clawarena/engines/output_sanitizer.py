"""Helpers for normalizing CLI stdout into agent answers."""

from __future__ import annotations

import re

_ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
_HTTP_STATUS_RE = re.compile(r"^(?:4\d\d|5\d\d)\s+\S")
_STATUS_CODE_RE = re.compile(r"^\d{3}\s+status code\b", re.IGNORECASE)
_RATE_LIMIT_MARKERS = (
    "api rate limit reached",
    "rate_limit_exceeded",
    "insufficient_quota",
    "too many requests",
    "quota exceeded",
)
_PROVIDER_ERROR_MARKERS = (
    "invalid model name",
    "model is not supported when using codex with a chatgpt account",
    '"error":',
    "{'error':",
)
_FRAMEWORK_WARNING_MARKERS = (
    "session history",
    "session limit",
)


def strip_ansi(text: str) -> str:
    """Remove ANSI control sequences from a string."""
    return _ANSI_RE.sub("", text)


def normalize_agent_output(stdout: str, framework: str = "generic") -> tuple[str, str | None]:
    """Return (clean_answer, detected_error_text)."""
    if not stdout:
        return "", None

    lines = stdout.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if framework == "nanobot":
        lines = _strip_nanobot_output(lines)
    elif framework == "picoclaw":
        lines = _strip_picoclaw_output(lines)

    text = "\n".join(line.rstrip() for line in lines).strip()
    if framework == "picoclaw":
        text = strip_ansi(text).strip()

    error = detect_provider_error(text)
    if error:
        return "", error
    return text, None


def detect_provider_error(text: str) -> str | None:
    """Detect common provider/transport failures that leaked onto stdout."""
    cleaned = strip_ansi(text).strip()
    if not cleaned:
        return None

    first_line = next((line.strip() for line in cleaned.splitlines() if line.strip()), "")
    lowered = cleaned.lower()
    first_lower = first_line.lower()

    if first_lower.startswith("error:") and (
        any(marker in lowered for marker in _RATE_LIMIT_MARKERS)
        or any(marker in lowered for marker in _PROVIDER_ERROR_MARKERS)
    ):
        return cleaned
    if first_lower.startswith("⚠️") and (
        any(marker in lowered for marker in _RATE_LIMIT_MARKERS)
        or any(marker in lowered for marker in _FRAMEWORK_WARNING_MARKERS)
    ):
        return cleaned
    if _HTTP_STATUS_RE.match(first_line) or _STATUS_CODE_RE.match(first_line):
        return cleaned
    if any(marker in first_lower for marker in _RATE_LIMIT_MARKERS):
        return cleaned
    if any(marker in lowered for marker in _PROVIDER_ERROR_MARKERS):
        return cleaned
    return None


def _strip_nanobot_output(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    skipping_prelude = True

    for line in lines:
        stripped = line.strip()
        if skipping_prelude:
            if not stripped:
                continue
            if (
                stripped.startswith("Using config:")
                or stripped.startswith("/")
                or stripped.startswith("Created ")
                or stripped == "🐈 nanobot"
            ):
                continue
            skipping_prelude = False

        if stripped == "🐈 nanobot":
            continue
        cleaned.append(line)

    return _trim_blank_lines(cleaned)


def _strip_picoclaw_output(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    skipping_banner = True

    for line in lines:
        plain = strip_ansi(line).strip()
        if skipping_banner:
            if not plain:
                continue
            if "\x1b[" in line or any(ch in plain for ch in ("█", "╔", "╗", "╚", "╝", "║")):
                continue
            skipping_banner = False

        cleaned.append(strip_ansi(line))

    cleaned = _trim_blank_lines(cleaned)
    if cleaned:
        first = cleaned[0].lstrip()
        if first.startswith("🦞"):
            payload = first[1:].lstrip()
            if payload:
                cleaned[0] = payload
            else:
                cleaned = cleaned[1:]
    return cleaned


def _trim_blank_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]
