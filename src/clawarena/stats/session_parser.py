"""Session-file parsers for per-framework token accounting.

Each framework stores its main/history sessions in a different on-disk
schema. If the stats pipeline counted those files as raw UTF-8 text,
JSON structural tokens (``{``, ``"type"``, per-event metadata, UUIDs)
would inflate the count well beyond what the underlying LLM actually
ingests. This module replaces that raw byte count with a
prompt-oriented estimate:

1. Parse the session file into an ordered list of
   :class:`ChatMessage` values (``role`` + ``text``), skipping
   control events (model/thinking changes, session headers, per-message
   UUIDs, etc.) that never reach the model.
2. Render the message list back into an approximate ChatML payload
   (``<|im_start|>role\\ncontent<|im_end|>\\n``). ChatML is the
   template used by GPT-4/4o and most Qwen-family models, so it is a
   reasonable cross-framework stand-in for the provider-specific wire
   format.
3. Count tokens on the rendered payload with the supplied
   :class:`~clawarena.stats.tokenizer.TokenCounter`.

If any step fails (malformed jsonl, unexpected payload shape) the
caller is expected to fall back to the raw byte count; this module
surfaces the error by returning ``None`` from the public helpers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from clawarena.stats.tokenizer import TokenCounter


# ---------------------------------------------------------------------------
# Common data shape
# ---------------------------------------------------------------------------

@dataclass
class ChatMessage:
    role: str
    text: str


# Canonical roles we keep; other values (e.g. ``system``) are retained
# as-is and rendered as-given, because the provider-side chat template
# also accepts arbitrary role strings.
_PROMPT_ROLES: frozenset[str] = frozenset(
    {"system", "user", "assistant", "tool"}
)


# ---------------------------------------------------------------------------
# Content coercion helpers
# ---------------------------------------------------------------------------

def _coerce_text_openai_chat(content) -> str:
    """Render an OpenAI-style ``content`` field into a flat string.

    Handles:
    - ``str`` → returned as-is.
    - ``list`` of parts where each part is ``{"type": "text", "text": ...}``
      or a tool-call variant. ``tool_use``/``toolCall`` parts are
      serialized as their name plus JSON-encoded arguments, since that
      payload is what is actually sent over the wire. ``tool_result``
      parts are serialized as their textual result.
    - Anything else → ``str(content)``.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks: list[str] = []
        for part in content:
            if not isinstance(part, dict):
                chunks.append(str(part))
                continue
            ptype = part.get("type", "")
            if ptype == "text":
                chunks.append(part.get("text", "") or "")
            elif ptype in ("tool_use", "toolCall"):
                name = part.get("name", "")
                args = part.get("arguments") or part.get("input") or {}
                try:
                    args_str = json.dumps(args, ensure_ascii=False)
                except (TypeError, ValueError):
                    args_str = str(args)
                chunks.append(f"{name}({args_str})")
            elif ptype == "tool_result":
                inner = part.get("content", "")
                if isinstance(inner, list):
                    chunks.append(_coerce_text_openai_chat(inner))
                else:
                    chunks.append(str(inner))
            else:
                # Unknown part type: fall back to a compact repr so we
                # at least account for its textual footprint.
                try:
                    chunks.append(json.dumps(part, ensure_ascii=False))
                except (TypeError, ValueError):
                    chunks.append(str(part))
        return "\n".join(c for c in chunks if c)
    return str(content)


# ---------------------------------------------------------------------------
# Per-framework parsers
# ---------------------------------------------------------------------------

def parse_openclaw_session(path: Path) -> list[ChatMessage] | None:
    """Parse an OpenClaw session jsonl.

    OpenClaw interleaves control events (``session``, ``model_change``,
    ``thinking_level_change``, ``custom``) with ``type == "message"``
    records. Only the latter contribute to the prompt; each carries
    ``message.role`` and ``message.content`` laid out like an OpenAI
    chat message (a list of typed parts).
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    out: list[ChatMessage] = []
    for raw in lines:
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if obj.get("type") != "message":
            continue
        msg = obj.get("message") or {}
        role = str(msg.get("role", "")).strip()
        if not role:
            continue
        text = _coerce_text_openai_chat(msg.get("content"))
        out.append(ChatMessage(role=role, text=text))
    return out


def parse_claude_code_session(path: Path) -> list[ChatMessage] | None:
    """Parse a Claude Code main-session jsonl.

    Each line is an event with ``type`` == role (``user`` /
    ``assistant``) and a nested ``message.content`` field that is
    either a flat string or a list of content parts.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    out: list[ChatMessage] = []
    for raw in lines:
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return None
        evt_type = obj.get("type")
        if evt_type not in ("user", "assistant", "system", "tool"):
            continue
        msg = obj.get("message") or {}
        role = str(msg.get("role") or evt_type).strip()
        text = _coerce_text_openai_chat(msg.get("content"))
        out.append(ChatMessage(role=role, text=text))
    return out


def parse_flat_role_jsonl(path: Path) -> list[ChatMessage] | None:
    """Parse flat ``{role, content, ...}`` jsonl used by NanoBot/PicoClaw.

    Non-prompt records (NanoBot writes a leading ``{"_type":"metadata",
    ...}`` header; stray ``meta`` rows without ``role`` are skipped).
    ``tool_calls`` / ``tool_call_id`` fields, when present, are folded
    into the text so the argument payload contributes to the count.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    out: list[ChatMessage] = []
    for raw in lines:
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if "role" not in obj:
            # Metadata / header line, skip.
            continue
        role = str(obj.get("role", "")).strip()
        if not role:
            continue
        text = _coerce_text_openai_chat(obj.get("content"))
        tool_calls = obj.get("tool_calls")
        if tool_calls:
            try:
                text = (text + "\n" if text else "") + json.dumps(
                    tool_calls, ensure_ascii=False,
                )
            except (TypeError, ValueError):
                text = (text + "\n" if text else "") + str(tool_calls)
        out.append(ChatMessage(role=role, text=text))
    return out


# Public alias so the layout registry can name a parser per framework.
parse_nanobot_session = parse_flat_role_jsonl
parse_picoclaw_session = parse_flat_role_jsonl


# ---------------------------------------------------------------------------
# ChatML rendering + token counting
# ---------------------------------------------------------------------------

_IM_START = "<|im_start|>"
_IM_END = "<|im_end|>"


def render_chatml(messages: list[ChatMessage]) -> str:
    """Render parsed messages as an approximate ChatML payload.

    The format (``<|im_start|>role\\ncontent<|im_end|>\\n``) matches
    the template used by GPT-4/4o and most Qwen-family tokenizers, and
    is a reasonable cross-framework approximation of the actual wire
    format that reaches the model.
    """
    parts: list[str] = []
    for m in messages:
        parts.append(f"{_IM_START}{m.role}\n{m.text}{_IM_END}\n")
    return "".join(parts)


# Type alias used by layouts to declare their parser.
SessionParser = Callable[[Path], Optional[list[ChatMessage]]]


def count_session_tokens(
    path: Path, parser: SessionParser, counter: TokenCounter,
) -> int:
    """Count prompt-oriented tokens for a session file.

    On any parse failure (unreadable file, malformed line, unexpected
    schema) we fall back to a raw byte count so that the overall stats
    run remains robust.
    """
    if not path.exists():
        return 0
    try:
        messages = parser(path)
    except Exception:
        messages = None
    if messages is None:
        return counter.count_file(path)
    payload = render_chatml(messages)
    # ``cl100k_base`` treats ``<|im_start|>`` / ``<|im_end|>`` as
    # special tokens by default and will refuse to encode them unless
    # we tell it they are allowed. We route through an internal helper
    # on the counter so the behaviour stays localized here.
    return counter.count_with_special(payload)
