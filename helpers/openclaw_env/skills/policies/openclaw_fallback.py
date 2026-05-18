"""Fallback policy for OpenClaw real->mock execution."""

from __future__ import annotations

from openclaw_env.backend.base import CommandResult


def should_fallback_to_mock(
    *,
    enabled: bool,
    command: str,
    result: CommandResult,
) -> bool:
    """Return True when real openclaw failure should be retried in mock backend."""
    if not enabled:
        return False
    if result.exit_code == 0:
        return False

    text = f"{result.stdout}\n{result.stderr}".lower()
    error_tags = [t.lower() for t in (result.meta or {}).get("error_tags", [])]

    if "command_not_found" in error_tags:
        return True
    if "unknown_channel" in error_tags:
        return True
    if "unsupported_channel" in error_tags:
        return True
    if "plugin_not_found" in error_tags:
        return True

    markers = (
        "gateway connect failed",
        "gateway closed (1008): unauthorized",
        "token mismatch",
        "unauthorized",
        "unknown channel:",
        "unsupported channel:",
        "eai_again",
        "enotfound",
        "etimedout",
        "econnreset",
        "econnrefused",
        "failed to fetch",
        "network error",
        "npm error 404 not found - get https://registry.npmjs.org",
        "no api key found for provider",
    )
    return any(m in text for m in markers)
