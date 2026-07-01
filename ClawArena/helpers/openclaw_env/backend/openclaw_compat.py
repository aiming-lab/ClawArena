"""Compatibility helpers for running legacy OpenClaw commands."""

from __future__ import annotations

import hashlib
import re
import shlex
from dataclasses import dataclass, field


@dataclass
class CompatDecision:
    """Compatibility decision for a single command."""

    original_action: str
    executed_action: str
    compat_status: str = "ok"  # ok | rewritten | skipped_incompatible
    error_tags: list[str] = field(default_factory=list)
    skip_reason: str = ""


def rewrite_command(command: str, skip_incompatible: bool = True) -> CompatDecision:
    """Rewrite legacy OpenClaw commands to improve runtime compatibility."""
    decision = CompatDecision(original_action=command, executed_action=command)

    normalized_command, normalized_cron = _normalize_cron_command_quoting(command)
    if normalized_cron:
        decision.error_tags.append("rewritten_cron_command_quoting")
        command = normalized_command

    try:
        tokens = shlex.split(command)
    except ValueError:
        decision.error_tags.append("parse_error")
        return decision

    if not tokens or tokens[0] != "openclaw":
        return decision

    changed = False

    # openclaw message poll --question ... -> --poll-question ...
    if tokens[:3] == ["openclaw", "message", "poll"]:
        if "--question" in tokens and "--poll-question" not in tokens:
            idx = tokens.index("--question")
            tokens[idx] = "--poll-question"
            changed = True
            decision.error_tags.append("rewritten_poll_question")

    # openclaw cron add ... (new CLI may require --name)
    if tokens[:3] == ["openclaw", "cron", "add"]:
        has_schedule = any(flag in tokens for flag in ("--cron", "--schedule", "--every"))
        has_message = any(flag in tokens for flag in ("--message", "--command"))
        if not (has_schedule and has_message) and skip_incompatible:
            decision.compat_status = "skipped_incompatible"
            decision.error_tags.append("incomplete_cron_add")
            decision.skip_reason = (
                "Skipped incompatible openclaw command: "
                "cron add requires a schedule and a message/command."
            )
            return decision
        if "--name" not in tokens:
            job_name = f"job_{hashlib.sha1(command.encode('utf-8')).hexdigest()[:8]}"
            tokens = tokens[:3] + ["--name", job_name] + tokens[3:]
            changed = True
            decision.error_tags.append("rewritten_cron_add_name")

    # openclaw agents add --name X -> openclaw agents add X
    if tokens[:3] == ["openclaw", "agents", "add"] and "--name" in tokens:
        name = _flag(tokens, "--name")
        if name:
            tokens = _remove_flag(tokens, "--name")
            tokens = tokens[:3] + [name] + tokens[3:]
            changed = True
            decision.error_tags.append("rewritten_agents_add_name")

    # openclaw agents set-identity --name X ... -> --agent X ...
    if tokens[:3] == ["openclaw", "agents", "set-identity"]:
        if "--name" in tokens and "--agent" not in tokens:
            name = _flag(tokens, "--name")
            if name:
                tokens = _remove_flag(tokens, "--name")
                tokens = tokens[:3] + ["--agent", name] + tokens[3:]
                changed = True
                decision.error_tags.append("rewritten_agents_set_identity_name")

    # openclaw configure key=value -> openclaw config set key value
    if tokens[:2] == ["openclaw", "configure"] and len(tokens) == 3:
        arg = tokens[2]
        if "=" in arg and not arg.startswith("-"):
            key, value = arg.split("=", 1)
            if key and value:
                tokens = ["openclaw", "config", "set", key, value]
                changed = True
                decision.error_tags.append("rewritten_configure_key_value")

    # Best-effort command alias rewrites from observed failures.
    if tokens[:3] == ["openclaw", "plugins", "remove"]:
        tokens[2] = "uninstall"
        changed = True
        decision.error_tags.append("rewritten_plugins_remove")

    if tokens[:3] == ["openclaw", "channels", "config"]:
        tokens[2] = "set"
        changed = True
        decision.error_tags.append("rewritten_channels_config")

    if tokens[:3] == ["openclaw", "webhooks", "add"]:
        tokens[2] = "create"
        changed = True
        decision.error_tags.append("rewritten_webhooks_add")

    if tokens[:3] == ["openclaw", "security", "set-token"]:
        tokens = tokens[:2] + ["token", "set"] + tokens[3:]
        changed = True
        decision.error_tags.append("rewritten_security_set_token")

    # Explicitly unsupported legacy forms: keep collection running, mark skipped.
    if tokens[:3] == ["openclaw", "message", "react"]:
        if "--target" in tokens and "--message-id" not in tokens and skip_incompatible:
            decision.compat_status = "skipped_incompatible"
            decision.error_tags.append("incompatible_message_react_target_only")
            decision.skip_reason = (
                "Skipped incompatible openclaw command: "
                "message react requires --message-id in current CLI."
            )
            return decision

    if tokens[:3] == ["openclaw", "message", "search"]:
        if "--channel" in tokens and "--guild-id" not in tokens and skip_incompatible:
            decision.compat_status = "skipped_incompatible"
            decision.error_tags.append("incompatible_message_search_missing_guild_id")
            decision.skip_reason = (
                "Skipped incompatible openclaw command: "
                "message search requires --guild-id in current CLI."
            )
            return decision

    decision.executed_action = shlex.join(tokens)
    if changed and decision.compat_status == "ok":
        decision.compat_status = "rewritten"
    return decision


def classify_error(text: str) -> list[str]:
    """Classify stderr/stdout text into coarse error tags."""
    tags: list[str] = []
    lowered = text.lower()

    if "compatibility config keys detected" in lowered:
        tags.append("compatibility_banner")
    if "invalid config at" in lowered:
        tags.append("invalid_config")
    if "unknown command" in lowered:
        tags.append("unknown_command")
    if "unknown option" in lowered:
        tags.append("unknown_option")
    if "required option" in lowered:
        tags.append("required_option")
    if "unknown channel:" in lowered:
        tags.append("unknown_channel")
    if "unsupported channel:" in lowered:
        tags.append("unsupported_channel")
    if "channel is required (no configured channels detected)" in lowered:
        tags.append("channel_required")
        tags.append("channel_not_configured")
    if "requires at least one configured channel" in lowered:
        tags.append("channel_required")
        tags.append("channel_not_configured")
    if "plugin not found:" in lowered:
        tags.append("plugin_not_found")
    if "command timed out" in lowered:
        tags.append("timeout")
    if "command not found" in lowered:
        tags.append("command_not_found")

    # Preserve insertion order while removing duplicates.
    deduped: list[str] = []
    for tag in tags:
        if tag not in deduped:
            deduped.append(tag)
    return deduped


def _flag(tokens: list[str], name: str) -> str | None:
    try:
        idx = tokens.index(name)
        return tokens[idx + 1] if idx + 1 < len(tokens) else None
    except ValueError:
        return None


def _remove_flag(tokens: list[str], name: str) -> list[str]:
    try:
        idx = tokens.index(name)
    except ValueError:
        return tokens
    if idx + 1 < len(tokens):
        return tokens[:idx] + tokens[idx + 2 :]
    return tokens[:idx]


def _normalize_cron_command_quoting(command: str) -> tuple[str, bool]:
    """Normalize legacy nested quotes inside `openclaw cron add --command '...'`.

    Some generated GT commands embed a quoted message inside a single-quoted
    `--command` argument, which breaks shell parsing in real CLI mode.
    """
    if not command.strip().startswith("openclaw cron add "):
        return command, False

    match = re.search(r"--command\s+'(.*)'\s*$", command)
    if not match:
        return command, False

    prefix = command[: match.start()].rstrip()
    inner = match.group(1)
    rebuilt = f"{prefix} --command {shlex.quote(inner)}"
    return rebuilt, rebuilt != command
