"""Email skill implementation with optional online provider side effects."""

from __future__ import annotations

import base64
import binascii
import copy
import json
import os
import shlex
import shutil
import subprocess
import urllib.parse
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from openclaw_env.backend.base import CommandResult
from openclaw_env.skills.base import Skill

_EMAIL_COUNTER = 0


def _new_email_id() -> str:
    global _EMAIL_COUNTER
    _EMAIL_COUNTER += 1
    return f"email_{_EMAIL_COUNTER:04d}"


def _get_arg(args: list[str], flag: str, default: str | None = None) -> str | None:
    for i, a in enumerate(args):
        if a == flag and i + 1 < len(args):
            return args[i + 1]
    return default


def _get_flag(args: list[str], flag: str) -> bool:
    return flag in args


_SEEDED_EMAILS: list[dict[str, Any]] = [
    {
        "id": "email_seed_1",
        "sender": "alice@example.com",
        "to": "me@example.com",
        "subject": "Project proposal",
        "body": "Hi, I wanted to share the project proposal for Q2. Please review.",
        "folder": "inbox",
        "read": False,
        "starred": False,
    },
    {
        "id": "email_seed_2",
        "sender": "bob@example.com",
        "to": "me@example.com",
        "subject": "Meeting notes",
        "body": "Attached are the notes from today's standup meeting.",
        "folder": "inbox",
        "read": False,
        "starred": False,
    },
    {
        "id": "email_seed_3",
        "sender": "carol@example.com",
        "to": "me@example.com",
        "subject": "Budget report",
        "body": "Please find the budget report for this quarter attached.",
        "folder": "inbox",
        "read": True,
        "starred": False,
    },
    {
        "id": "email_seed_4",
        "sender": "dave@example.com",
        "to": "me@example.com",
        "subject": "Follow-up on hackathon",
        "body": "Just following up on the hackathon registration. Did you sign up?",
        "folder": "inbox",
        "read": False,
        "starred": True,
    },
    {
        "id": "email_seed_5",
        "sender": "eve@example.com",
        "to": "me@example.com",
        "subject": "Quarterly review",
        "body": "The quarterly review is scheduled for next Friday at 2pm.",
        "folder": "inbox",
        "read": False,
        "starred": False,
    },
]


class EmailSkill(Skill):
    """Email skill with deterministic local state and optional online side effects."""

    def __init__(self) -> None:
        super().__init__(prefixes=("email",))
        self._emails: list[dict[str, Any]] = []
        self._initialized = False
        self._enable_online_data = False
        self._strict_online_data = False
        self._email_provider_preference = "auto"
        self._google_settings: dict[str, Any] = {}
        self._himalaya_settings: dict[str, Any] = {}
        self._online_ids_by_local_id: dict[str, str] = {}

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        del state_dir
        global _EMAIL_COUNTER
        _EMAIL_COUNTER = 100
        self._emails = [copy.deepcopy(e) for e in _SEEDED_EMAILS]
        self._online_ids_by_local_id = {}
        self._initialized = True

        val = str(env_vars.get("OPENCLAW_ENV_ENABLE_ONLINE_DATA", "")).lower()
        self._enable_online_data = val in {"1", "true", "yes", "on"}
        strict_val = str(env_vars.get("OPENCLAW_ENV_STRICT_ONLINE_DATA", "")).lower()
        self._strict_online_data = strict_val in {"1", "true", "yes", "on"}

        provider = str(env_vars.get("OPENCLAW_ENV_EMAIL_PROVIDER", "auto")).strip().lower()
        if provider in {"auto", "google_api", "himalaya", "mock"}:
            self._email_provider_preference = provider
        else:
            self._email_provider_preference = "auto"

        self._google_settings = _build_google_gmail_settings(env_vars)
        self._himalaya_settings = _build_himalaya_settings(env_vars)

    def execute(self, command: str) -> CommandResult:
        parts = shlex.split(command.strip())
        if not parts or parts[0] != "email":
            return CommandResult(stdout="", stderr="Not an email command", exit_code=1)

        if len(parts) < 2:
            return CommandResult(
                stdout=(
                    "email <subcommand> [options]\n"
                    "Subcommands: list, read, send, reply, search, move, delete, mark"
                ),
                stderr="",
                exit_code=0,
            )

        sub = parts[1]
        args = parts[2:]

        handlers = {
            "list": self._cmd_list,
            "read": self._cmd_read,
            "send": self._cmd_send,
            "reply": self._cmd_reply,
            "search": self._cmd_search,
            "move": self._cmd_move,
            "delete": self._cmd_delete,
            "mark": self._cmd_mark,
        }

        handler = handlers.get(sub)
        if handler is None:
            return CommandResult(stdout="", stderr=f"Unknown email subcommand: {sub}", exit_code=1)
        return handler(args)

    def cleanup(self) -> None:
        self._emails = []
        self._online_ids_by_local_id = {}
        self._initialized = False

    def get_state(self) -> dict[str, Any]:
        return {"emails": list(self._emails)}

    def _cmd_list(self, args: list[str]) -> CommandResult:
        folder = _get_arg(args, "--folder", "inbox") or "inbox"
        unread_only = _get_flag(args, "--unread")
        from_filter = _get_arg(args, "--from")

        execution_trace: list[dict[str, Any]] = []
        ok, err, _ = self._online_side_effect(
            execution_trace,
            action="list",
            folder=folder,
            unread_only=unread_only,
            from_filter=from_filter,
        )
        if not ok and self._strict_online_data:
            return CommandResult(
                stdout="",
                stderr=(
                    f"Online email action 'list' failed: {err}. "
                    "Strict online mode is enabled, so local fallback is disabled."
                ),
                exit_code=1,
                execution_trace=execution_trace or None,
            )

        emails = [e for e in self._emails if e["folder"] == folder]
        if unread_only:
            emails = [e for e in emails if not e["read"]]
        if from_filter:
            emails = [e for e in emails if from_filter.lower() in e["sender"].lower()]

        if not emails:
            return CommandResult(
                stdout=f"No emails in {folder}.",
                stderr="",
                exit_code=0,
                execution_trace=execution_trace or None,
            )

        lines = [f"Emails in {folder}:"]
        for em in emails:
            unread_marker = "●" if not em["read"] else " "
            star_marker = "★" if em["starred"] else " "
            lines.append(
                f"  [{em['id']}] {unread_marker}{star_marker} "
                f"From: {em['sender']} | Subject: {em['subject']}"
            )
        return CommandResult(
            stdout="\n".join(lines),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_send(self, args: list[str]) -> CommandResult:
        to = _get_arg(args, "--to")
        subject = _get_arg(args, "--subject")
        body = _get_arg(args, "--body")
        cc = _get_arg(args, "--cc")

        if not to:
            return CommandResult(stdout="", stderr="--to is required", exit_code=1)
        if not subject:
            return CommandResult(stdout="", stderr="--subject is required", exit_code=1)
        if not body:
            return CommandResult(stdout="", stderr="--body is required", exit_code=1)

        execution_trace: list[dict[str, Any]] = []
        ok, err, meta = self._online_side_effect(
            execution_trace,
            action="send",
            to=to,
            subject=subject,
            body=body,
            cc=cc,
        )
        if not ok and self._strict_online_data:
            return CommandResult(
                stdout="",
                stderr=(
                    f"Online email action 'send' failed: {err}. "
                    "Strict online mode is enabled, so local fallback is disabled."
                ),
                exit_code=1,
                execution_trace=execution_trace or None,
            )

        email_id = _new_email_id()
        email: dict[str, Any] = {
            "id": email_id,
            "sender": "me@example.com",
            "to": to,
            "cc": cc,
            "subject": subject,
            "body": body,
            "folder": "sent",
            "read": True,
            "starred": False,
        }
        self._emails.append(email)
        remote_id = str(meta.get("message_id", "")).strip()
        if remote_id:
            self._online_ids_by_local_id[email_id] = remote_id

        return CommandResult(
            stdout=f"Email sent to {to} | Subject: {subject} | ID: {email_id}",
            stderr="",
            exit_code=0,
            state_changes={"emails_sent": [email]},
            execution_trace=execution_trace or None,
        )

    def _cmd_reply(self, args: list[str]) -> CommandResult:
        email_id = _get_arg(args, "--id")
        body = _get_arg(args, "--body")

        if not email_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)
        if not body:
            return CommandResult(stdout="", stderr="--body is required", exit_code=1)

        original = next((e for e in self._emails if e["id"] == email_id), None)
        if original is None:
            return CommandResult(
                stdout="", stderr=f"Email not found: {email_id}", exit_code=1
            )

        execution_trace: list[dict[str, Any]] = []
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(email_id)
            if mapped:
                ok, err, _ = self._online_side_effect(
                    execution_trace,
                    action="reply",
                    online_message_id=mapped,
                    to=original["sender"],
                    subject=original["subject"],
                    body=body,
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online email action 'reply' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )
            else:
                reason = "unmapped_seed_id" if email_id.startswith("email_seed_") else "unmapped_local_id"
                execution_trace.append(_trace_reason(reason=reason, provider="none", error=f"id={email_id}"))
                if self._strict_online_data and not email_id.startswith("email_seed_"):
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"No online message mapping for '{email_id}'. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        new_id = _new_email_id()
        reply: dict[str, Any] = {
            "id": new_id,
            "sender": "me@example.com",
            "to": original["sender"],
            "subject": f"Re: {original['subject']}",
            "body": body,
            "folder": "sent",
            "read": True,
            "starred": False,
            "in_reply_to": email_id,
        }
        self._emails.append(reply)

        return CommandResult(
            stdout=f"Reply sent to {original['sender']} | Subject: Re: {original['subject']}",
            stderr="",
            exit_code=0,
            state_changes={"emails_sent": [reply]},
            execution_trace=execution_trace or None,
        )

    def _cmd_search(self, args: list[str]) -> CommandResult:
        query = _get_arg(args, "--query")
        from_filter = _get_arg(args, "--from")

        if not query:
            return CommandResult(stdout="", stderr="--query is required", exit_code=1)

        execution_trace: list[dict[str, Any]] = []
        ok, err, _ = self._online_side_effect(
            execution_trace,
            action="search",
            query=query,
            from_filter=from_filter,
        )
        if not ok and self._strict_online_data:
            return CommandResult(
                stdout="",
                stderr=(
                    f"Online email action 'search' failed: {err}. "
                    "Strict online mode is enabled, so local fallback is disabled."
                ),
                exit_code=1,
                execution_trace=execution_trace or None,
            )

        q = query.lower()
        results = [
            e for e in self._emails
            if q in e["subject"].lower() or q in e["body"].lower()
        ]
        if from_filter:
            results = [e for e in results if from_filter.lower() in e["sender"].lower()]

        if not results:
            return CommandResult(
                stdout=f"No emails matching '{query}'.",
                stderr="",
                exit_code=0,
                execution_trace=execution_trace or None,
            )

        lines = [f"Emails matching '{query}':"]
        for em in results:
            lines.append(
                f"  [{em['id']}] From: {em['sender']} | Subject: {em['subject']}"
            )
        return CommandResult(
            stdout="\n".join(lines),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_read(self, args: list[str]) -> CommandResult:
        email_id = _get_arg(args, "--id")
        if not email_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)

        email = next((e for e in self._emails if e["id"] == email_id), None)
        if email is None:
            return CommandResult(
                stdout="", stderr=f"Email not found: {email_id}", exit_code=1
            )

        execution_trace: list[dict[str, Any]] = []
        remote_email: dict[str, Any] | None = None
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(email_id)
            if mapped:
                ok, err, meta = self._online_side_effect(
                    execution_trace,
                    action="read",
                    online_message_id=mapped,
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online email action 'read' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )
                remote_email = meta.get("email")
            else:
                reason = "unmapped_seed_id" if email_id.startswith("email_seed_") else "unmapped_local_id"
                execution_trace.append(_trace_reason(reason=reason, provider="none", error=f"id={email_id}"))
                if self._strict_online_data and not email_id.startswith("email_seed_"):
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"No online message mapping for '{email_id}'. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        source_email = remote_email or email
        return CommandResult(
            stdout=_format_email_read_output(source_email),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_move(self, args: list[str]) -> CommandResult:
        email_id = _get_arg(args, "--id")
        folder = _get_arg(args, "--folder")

        if not email_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)
        if not folder:
            return CommandResult(stdout="", stderr="--folder is required", exit_code=1)

        email = next((e for e in self._emails if e["id"] == email_id), None)
        if email is None:
            return CommandResult(
                stdout="", stderr=f"Email not found: {email_id}", exit_code=1
            )

        execution_trace: list[dict[str, Any]] = []
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(email_id)
            if mapped:
                ok, err, _ = self._online_side_effect(
                    execution_trace,
                    action="move",
                    online_message_id=mapped,
                    folder=folder,
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online email action 'move' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )
            else:
                reason = "unmapped_seed_id" if email_id.startswith("email_seed_") else "unmapped_local_id"
                execution_trace.append(_trace_reason(reason=reason, provider="none", error=f"id={email_id}"))
                if self._strict_online_data and not email_id.startswith("email_seed_"):
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"No online message mapping for '{email_id}'. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        old_folder = email["folder"]
        email["folder"] = folder
        return CommandResult(
            stdout=f"Email {email_id} moved from {old_folder} to {folder}.",
            stderr="",
            exit_code=0,
            state_changes={"emails_moved": [{"id": email_id, "folder": folder}]},
            execution_trace=execution_trace or None,
        )

    def _cmd_delete(self, args: list[str]) -> CommandResult:
        email_id = _get_arg(args, "--id")
        if not email_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)

        execution_trace: list[dict[str, Any]] = []
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(email_id)
            if mapped:
                ok, err, _ = self._online_side_effect(
                    execution_trace,
                    action="delete",
                    online_message_id=mapped,
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online email action 'delete' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        before = len(self._emails)
        self._emails = [e for e in self._emails if e["id"] != email_id]
        if len(self._emails) == before:
            return CommandResult(
                stdout="", stderr=f"Email not found: {email_id}", exit_code=1
            )
        return CommandResult(
            stdout=f"Email {email_id} deleted.",
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_mark(self, args: list[str]) -> CommandResult:
        email_id = _get_arg(args, "--id")
        flag = _get_arg(args, "--flag")

        if not email_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)
        if not flag or flag not in ("read", "unread", "starred"):
            return CommandResult(
                stdout="", stderr="--flag must be one of: read, unread, starred", exit_code=1
            )

        email = next((e for e in self._emails if e["id"] == email_id), None)
        if email is None:
            return CommandResult(
                stdout="", stderr=f"Email not found: {email_id}", exit_code=1
            )

        execution_trace: list[dict[str, Any]] = []
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(email_id)
            if mapped:
                ok, err, _ = self._online_side_effect(
                    execution_trace,
                    action="mark",
                    online_message_id=mapped,
                    flag=flag,
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online email action 'mark' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )
            else:
                reason = "unmapped_seed_id" if email_id.startswith("email_seed_") else "unmapped_local_id"
                execution_trace.append(_trace_reason(reason=reason, provider="none", error=f"id={email_id}"))
                if self._strict_online_data and not email_id.startswith("email_seed_"):
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"No online message mapping for '{email_id}'. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        if flag == "read":
            email["read"] = True
        elif flag == "unread":
            email["read"] = False
        elif flag == "starred":
            email["starred"] = True

        return CommandResult(
            stdout=f"Email {email_id} marked as {flag}.",
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _online_side_effect(
        self,
        execution_trace: list[dict[str, Any]],
        *,
        action: str,
        **kwargs: Any,
    ) -> tuple[bool, str, dict[str, Any]]:
        if not self._enable_online_data:
            return True, "", {}

        ok, err, trace, meta = _run_email_online_action(
            action=action,
            provider_preference=self._email_provider_preference,
            google_settings=self._google_settings,
            himalaya_settings=self._himalaya_settings,
            **kwargs,
        )
        execution_trace.extend(trace)
        return ok, err, meta


def _trace_reason(reason: str, provider: str, error: str = "") -> dict[str, Any]:
    return {
        "action": "email.online.fallback",
        "provider": provider,
        "reason": reason,
        "error": error,
        "stdout": "",
        "stderr": error,
        "exit_code": 1 if error else 0,
    }


def _format_email_read_output(email: dict[str, Any]) -> str:
    cc = email.get("cc")
    cc_line = f"\nCC: {cc}" if cc else ""
    return (
        f"Email [{email.get('id', '')}]\n"
        f"From: {email.get('sender', '')}\n"
        f"To: {email.get('to', '')}"
        f"{cc_line}\n"
        f"Subject: {email.get('subject', '')}\n"
        f"Folder: {email.get('folder', '')}\n"
        f"Read: {bool(email.get('read', False))}\n"
        f"Starred: {bool(email.get('starred', False))}\n"
        f"Body:\n{email.get('body', '')}"
    )


def _build_google_gmail_settings(env_vars: dict[str, str]) -> dict[str, Any]:
    scopes = env_vars.get(
        "OPENCLAW_ENV_GOOGLE_GMAIL_SCOPES",
        "https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.send",
    )
    scopes_list = [s.strip() for s in scopes.split(",") if s.strip()]

    token_file = env_vars.get("OPENCLAW_ENV_GOOGLE_TOKEN_FILE", "").strip()
    if not token_file:
        token_file = os.path.expanduser("~/.openclaw/google_email_token.json")

    return {
        "user_id": env_vars.get("OPENCLAW_ENV_GOOGLE_GMAIL_USER", "me").strip() or "me",
        "token_file": token_file,
        "client_secret_file": env_vars.get("OPENCLAW_ENV_GOOGLE_CLIENT_SECRET_FILE", "").strip(),
        "scopes": scopes_list
        or [
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/gmail.send",
        ],
        "allow_interactive_auth": str(
            env_vars.get("OPENCLAW_ENV_GOOGLE_ALLOW_INTERACTIVE_AUTH", "")
        ).lower()
        in {"1", "true", "yes", "on"},
    }


def _build_himalaya_settings(env_vars: dict[str, str]) -> dict[str, Any]:
    config_file = env_vars.get("OPENCLAW_ENV_HIMALAYA_CONFIG_FILE", "").strip()
    if not config_file:
        config_file = os.path.expanduser("~/.config/himalaya/config.toml")
    return {
        "account": env_vars.get("OPENCLAW_ENV_HIMALAYA_ACCOUNT", "").strip(),
        "config_file": config_file,
    }


def _google_gmail_deps_available() -> bool:
    try:
        import google.oauth2.credentials  # noqa: F401
        import google_auth_oauthlib.flow  # noqa: F401
        import googleapiclient.discovery  # noqa: F401
    except Exception:
        return False
    return True


def _google_provider_available(settings: dict[str, Any], *, require_token: bool) -> bool:
    if not _google_gmail_deps_available():
        return False
    token_file = os.path.expanduser(str(settings.get("token_file", "")).strip())
    has_token = token_file and os.path.isfile(token_file)
    if has_token:
        return True
    if require_token:
        return False
    client_secret = str(settings.get("client_secret_file", "")).strip()
    return bool(client_secret and os.path.isfile(os.path.expanduser(client_secret)))


def _himalaya_provider_available(settings: dict[str, Any], *, require_config: bool) -> bool:
    if shutil.which("himalaya") is None:
        return False
    if not require_config:
        return True
    account = str(settings.get("account", "")).strip()
    if account:
        return True
    config_file = os.path.expanduser(str(settings.get("config_file", "")).strip())
    return bool(config_file and os.path.isfile(config_file))


def _resolve_email_provider(
    preference: str,
    google_settings: dict[str, Any],
    himalaya_settings: dict[str, Any],
) -> str | None:
    pref = preference.strip().lower()
    if pref == "mock":
        return None

    if pref == "google_api":
        return "google_api" if _google_provider_available(google_settings, require_token=False) else None
    if pref == "himalaya":
        return "himalaya" if _himalaya_provider_available(himalaya_settings, require_config=False) else None

    if _google_provider_available(google_settings, require_token=True):
        return "google_api"
    if _himalaya_provider_available(himalaya_settings, require_config=True):
        return "himalaya"
    return None


def _run_email_online_action(
    action: str,
    provider_preference: str,
    google_settings: dict[str, Any],
    himalaya_settings: dict[str, Any],
    **kwargs: Any,
) -> tuple[bool, str, list[dict[str, Any]], dict[str, Any]]:
    provider = _resolve_email_provider(provider_preference, google_settings, himalaya_settings)
    if not provider:
        trace = [
            _trace_reason(
                reason="online_unavailable",
                provider="none",
                error="No supported email provider found (google_api/himalaya).",
            )
        ]
        return False, "No supported email provider found (google_api/himalaya).", trace, {}

    if provider == "google_api":
        ok, err, trace, meta = _run_google_gmail_action(action, kwargs, google_settings)
    else:
        ok, err, trace, meta = _run_himalaya_action(action, kwargs, himalaya_settings)

    if not ok:
        trace.append(_trace_reason(reason="online_unavailable", provider=provider, error=err))
    return ok, err, trace, meta


def _build_google_gmail_service(
    settings: dict[str, Any],
    *,
    allow_interactive: bool | None = None,
):
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "google_api provider requires google-api-python-client, google-auth, "
            "google-auth-oauthlib. Install them first."
        ) from exc

    scopes = settings.get("scopes") or [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send",
    ]
    token_file = os.path.expanduser(str(settings.get("token_file", "")).strip())
    client_secret_file = os.path.expanduser(str(settings.get("client_secret_file", "")).strip())
    if allow_interactive is None:
        allow_interactive = bool(settings.get("allow_interactive_auth", False))

    creds = None
    if token_file and os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        if token_file:
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, "w", encoding="utf-8") as f:
                f.write(creds.to_json())

    if not creds or not creds.valid:
        if not allow_interactive:
            raise RuntimeError(
                f"Missing/invalid Google token at '{token_file}'. "
                "Run login bootstrap first or enable interactive auth."
            )
        if not client_secret_file or not os.path.isfile(client_secret_file):
            raise RuntimeError(
                "Missing OPENCLAW_ENV_GOOGLE_CLIENT_SECRET_FILE for interactive google_api auth."
            )
        # Google test apps sometimes return a narrower scope set than requested
        # (for example only gmail.modify). Allow that mismatch instead of hard-failing.
        prev_relax_scope = os.environ.get("OAUTHLIB_RELAX_TOKEN_SCOPE")
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
        try:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            if hasattr(flow, "run_console"):
                try:
                    creds = flow.run_console()
                except Exception:
                    creds = flow.run_local_server(port=0)
            else:
                creds = flow.run_local_server(port=0)
        finally:
            if prev_relax_scope is None:
                os.environ.pop("OAUTHLIB_RELAX_TOKEN_SCOPE", None)
            else:
                os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = prev_relax_scope
        if token_file:
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, "w", encoding="utf-8") as f:
                f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _build_gmail_query(kwargs: dict[str, Any]) -> str:
    parts: list[str] = []
    folder = str(kwargs.get("folder", "")).strip().lower()
    if folder == "inbox":
        parts.append("in:inbox")
    elif folder:
        parts.append(f"label:{folder}")
    if kwargs.get("unread_only"):
        parts.append("is:unread")
    from_filter = str(kwargs.get("from_filter", "")).strip()
    if from_filter:
        parts.append(f"from:{from_filter}")
    query = str(kwargs.get("query", "")).strip()
    if query:
        parts.append(query)
    return " ".join(p for p in parts if p)


def _run_google_gmail_action(
    action: str,
    kwargs: dict[str, Any],
    settings: dict[str, Any],
) -> tuple[bool, str, list[dict[str, Any]], dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    try:
        service = _build_google_gmail_service(settings)
    except Exception as exc:
        return False, str(exc), trace, {}

    user_id = str(settings.get("user_id") or "me")
    meta: dict[str, Any] = {}

    try:
        if action in {"list", "search"}:
            q = _build_gmail_query(kwargs)
            resp = (
                service.users()
                .messages()
                .list(userId=user_id, q=q or None, maxResults=20)
                .execute()
            )
            ids = [m.get("id") for m in resp.get("messages", []) if isinstance(m, dict)]
            meta["remote_ids"] = [i for i in ids if isinstance(i, str)]
            trace.append(
                {
                    "action": f"google_api.gmail.messages.{action}",
                    "provider": "google_api",
                    "request": {
                        "user_id": user_id,
                        "query": q or None,
                        "max_results": 20,
                    },
                    "replay_cmd": _google_gmail_replay_cmd(
                        action=action,
                        user_id=user_id,
                        request_params={"q": q or None, "maxResults": 20},
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "read":
            online_id = str(kwargs.get("online_message_id") or "").strip()
            if not online_id:
                return False, "online_message_id required for read", trace, {}
            resp = (
                service.users()
                .messages()
                .get(userId=user_id, id=online_id, format="full")
                .execute()
            )
            meta["email"] = _gmail_message_to_email(resp)
            trace.append(
                {
                    "action": "google_api.gmail.messages.read",
                    "provider": "google_api",
                    "request": {
                        "user_id": user_id,
                        "online_message_id": online_id,
                        "format": "full",
                    },
                    "replay_cmd": _google_gmail_replay_cmd(
                        action="read",
                        user_id=user_id,
                        message_id=online_id,
                        request_params={"format": "full"},
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "send":
            to = str(kwargs.get("to") or "").strip()
            subject = str(kwargs.get("subject") or "").strip()
            body = str(kwargs.get("body") or "").strip()
            if not to or not subject or not body:
                return False, "to/subject/body required for send", trace, {}

            msg = EmailMessage()
            msg["To"] = to
            cc = str(kwargs.get("cc") or "").strip()
            if cc:
                msg["Cc"] = cc
            msg["Subject"] = subject
            msg.set_content(body)
            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")

            resp = (
                service.users()
                .messages()
                .send(userId=user_id, body={"raw": raw})
                .execute()
            )
            meta["message_id"] = resp.get("id")
            trace.append(
                {
                    "action": "google_api.gmail.messages.send",
                    "provider": "google_api",
                    "request": {
                        "user_id": user_id,
                        "to": to,
                        "cc": cc or None,
                        "subject": subject,
                    },
                    "replay_cmd": _google_gmail_replay_cmd(
                        action="send",
                        user_id=user_id,
                        body={"raw": raw},
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "reply":
            online_id = str(kwargs.get("online_message_id") or "").strip()
            if not online_id:
                return False, "online_message_id required for reply", trace, {}
            to = str(kwargs.get("to") or "").strip()
            subject = str(kwargs.get("subject") or "").strip()
            body = str(kwargs.get("body") or "").strip()
            if not to or not body:
                return False, "to/body required for reply", trace, {}

            original = service.users().messages().get(
                userId=user_id, id=online_id, format="metadata"
            ).execute()
            thread_id = original.get("threadId")
            subj = subject if subject.lower().startswith("re:") else f"Re: {subject}"

            msg = EmailMessage()
            msg["To"] = to
            msg["Subject"] = subj
            msg["In-Reply-To"] = online_id
            msg["References"] = online_id
            msg.set_content(body)
            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")

            body_obj: dict[str, Any] = {"raw": raw}
            if thread_id:
                body_obj["threadId"] = thread_id

            resp = (
                service.users()
                .messages()
                .send(userId=user_id, body=body_obj)
                .execute()
            )
            meta["message_id"] = resp.get("id")
            trace.append(
                {
                    "action": "google_api.gmail.messages.reply",
                    "provider": "google_api",
                    "request": {
                        "user_id": user_id,
                        "online_message_id": online_id,
                        "to": to,
                        "subject": subj,
                    },
                    "replay_cmd": _google_gmail_replay_cmd(
                        action="reply",
                        user_id=user_id,
                        body=body_obj,
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "move":
            online_id = str(kwargs.get("online_message_id") or "").strip()
            folder = str(kwargs.get("folder") or "").strip().lower()
            if not online_id or not folder:
                return False, "online_message_id/folder required for move", trace, {}

            add_labels, remove_labels = _gmail_label_changes_for_move(folder)
            if not add_labels and not remove_labels:
                return True, "", trace, {}

            resp = (
                service.users()
                .messages()
                .modify(
                    userId=user_id,
                    id=online_id,
                    body={"addLabelIds": add_labels, "removeLabelIds": remove_labels},
                )
                .execute()
            )
            trace.append(
                {
                    "action": "google_api.gmail.messages.modify(move)",
                    "provider": "google_api",
                    "request": {
                        "user_id": user_id,
                        "online_message_id": online_id,
                        "folder": folder,
                        "add_labels": add_labels,
                        "remove_labels": remove_labels,
                    },
                    "replay_cmd": _google_gmail_replay_cmd(
                        action="modify",
                        user_id=user_id,
                        message_id=online_id,
                        body={"addLabelIds": add_labels, "removeLabelIds": remove_labels},
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "mark":
            online_id = str(kwargs.get("online_message_id") or "").strip()
            flag = str(kwargs.get("flag") or "").strip().lower()
            if not online_id or not flag:
                return False, "online_message_id/flag required for mark", trace, {}
            add_labels: list[str] = []
            remove_labels: list[str] = []
            if flag == "read":
                remove_labels.append("UNREAD")
            elif flag == "unread":
                add_labels.append("UNREAD")
            elif flag == "starred":
                add_labels.append("STARRED")
            else:
                return False, f"unsupported mark flag: {flag}", trace, {}

            resp = (
                service.users()
                .messages()
                .modify(
                    userId=user_id,
                    id=online_id,
                    body={"addLabelIds": add_labels, "removeLabelIds": remove_labels},
                )
                .execute()
            )
            trace.append(
                {
                    "action": "google_api.gmail.messages.modify(mark)",
                    "provider": "google_api",
                    "request": {
                        "user_id": user_id,
                        "online_message_id": online_id,
                        "flag": flag,
                        "add_labels": add_labels,
                        "remove_labels": remove_labels,
                    },
                    "replay_cmd": _google_gmail_replay_cmd(
                        action="modify",
                        user_id=user_id,
                        message_id=online_id,
                        body={"addLabelIds": add_labels, "removeLabelIds": remove_labels},
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "delete":
            online_id = str(kwargs.get("online_message_id") or "").strip()
            if not online_id:
                return False, "online_message_id required for delete", trace, {}
            resp = (
                service.users()
                .messages()
                .trash(userId=user_id, id=online_id)
                .execute()
            )
            trace.append(
                {
                    "action": "google_api.gmail.messages.trash",
                    "provider": "google_api",
                    "request": {
                        "user_id": user_id,
                        "online_message_id": online_id,
                    },
                    "replay_cmd": _google_gmail_replay_cmd(
                        action="trash",
                        user_id=user_id,
                        message_id=online_id,
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        return False, f"unsupported google_api action: {action}", trace, {}
    except Exception as exc:  # pragma: no cover - external API surface
        return False, str(exc), trace, {}


def _gmail_label_changes_for_move(folder: str) -> tuple[list[str], list[str]]:
    folder_norm = folder.strip().lower()
    if folder_norm in {"archive", "archived"}:
        return [], ["INBOX"]
    if folder_norm == "inbox":
        return ["INBOX"], []
    if folder_norm == "important":
        return ["IMPORTANT"], []
    if folder_norm == "starred":
        return ["STARRED"], []
    return [], []


def _google_gmail_replay_cmd(
    *,
    action: str,
    user_id: str,
    message_id: str | None = None,
    body: dict[str, Any] | None = None,
    request_params: dict[str, Any] | None = None,
) -> str:
    user_id_enc = urllib.parse.quote(user_id or "me", safe="")
    base = f"https://gmail.googleapis.com/gmail/v1/users/{user_id_enc}/messages"
    auth_header = "Authorization: Bearer <ACCESS_TOKEN>"

    if action in {"list", "search"}:
        cmd = ["curl", "-sS", "--get", base, "-H", auth_header]
        params = request_params or {}
        if params.get("q"):
            cmd.extend(["--data-urlencode", f"q={params['q']}"])
        max_results = params.get("maxResults")
        if max_results is not None:
            cmd.extend(["--data-urlencode", f"maxResults={max_results}"])
        return shlex.join(cmd)

    if action == "read":
        message_id_enc = urllib.parse.quote(message_id or "", safe="")
        cmd = [
            "curl",
            "-sS",
            f"{base}/{message_id_enc}?format={(request_params or {}).get('format', 'full')}",
            "-H",
            auth_header,
        ]
        return shlex.join(cmd)

    if action in {"send", "reply"}:
        payload = json.dumps(body or {}, ensure_ascii=False, separators=(",", ":"))
        cmd = [
            "curl",
            "-sS",
            "-X",
            "POST",
            f"{base}/send",
            "-H",
            auth_header,
            "-H",
            "Content-Type: application/json",
            "--data-raw",
            payload,
        ]
        return shlex.join(cmd)

    if action == "modify":
        message_id_enc = urllib.parse.quote(message_id or "", safe="")
        payload = json.dumps(body or {}, ensure_ascii=False, separators=(",", ":"))
        cmd = [
            "curl",
            "-sS",
            "-X",
            "POST",
            f"{base}/{message_id_enc}/modify",
            "-H",
            auth_header,
            "-H",
            "Content-Type: application/json",
            "--data-raw",
            payload,
        ]
        return shlex.join(cmd)

    if action == "trash":
        message_id_enc = urllib.parse.quote(message_id or "", safe="")
        cmd = [
            "curl",
            "-sS",
            "-X",
            "POST",
            f"{base}/{message_id_enc}/trash",
            "-H",
            auth_header,
        ]
        return shlex.join(cmd)

    return ""


def _himalaya_base_cmd(settings: dict[str, Any]) -> list[str]:
    cmd = ["himalaya"]
    account = str(settings.get("account", "")).strip()
    if account:
        cmd.extend(["-a", account])
    config_file = os.path.expanduser(str(settings.get("config_file", "")).strip())
    if config_file and os.path.isfile(config_file):
        cmd.extend(["--config", config_file])
    return cmd


def _run_himalaya_action(
    action: str,
    kwargs: dict[str, Any],
    settings: dict[str, Any],
) -> tuple[bool, str, list[dict[str, Any]], dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    base_cmd = _himalaya_base_cmd(settings)

    if action == "list":
        cmd = base_cmd + ["message", "list"]
    elif action == "search":
        query = str(kwargs.get("query") or "").strip()
        if not query:
            return False, "query required for search", trace, {}
        cmd = base_cmd + ["message", "search", query]
    elif action == "read":
        online_id = str(kwargs.get("online_message_id") or "").strip()
        if not online_id:
            return False, "online_message_id required for read", trace, {}
        cmd = base_cmd + ["message", "read", online_id]
    elif action == "send":
        to = str(kwargs.get("to") or "").strip()
        subject = str(kwargs.get("subject") or "").strip()
        body = str(kwargs.get("body") or "").strip()
        if not to or not subject or not body:
            return False, "to/subject/body required for send", trace, {}
        cmd = base_cmd + ["message", "send", "--to", to, "--subject", subject, "--body", body]
    else:
        return False, f"himalaya action not supported in v1: {action}", trace, {}

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception as exc:
        return False, str(exc), trace, {}

    trace.append(
        {
            "action": shlex.join(cmd),
            "provider": "himalaya",
            "stdout": proc.stdout or "",
            "stderr": proc.stderr or "",
            "exit_code": proc.returncode,
        }
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip() or f"himalaya exited {proc.returncode}"
        return False, err, trace, {}
    if action == "read":
        return True, "", trace, {"email": _parse_himalaya_read_output(online_id, proc.stdout or "")}
    return True, "", trace, {}


def _gmail_message_to_email(message: dict[str, Any]) -> dict[str, Any]:
    headers = {
        str(h.get("name", "")).lower(): str(h.get("value", ""))
        for h in (message.get("payload", {}) or {}).get("headers", [])
        if isinstance(h, dict)
    }
    label_ids = set(str(v) for v in message.get("labelIds", []) if isinstance(v, str))
    return {
        "id": str(message.get("id", "")),
        "sender": headers.get("from", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "subject": headers.get("subject", ""),
        "body": _gmail_extract_body_text(message.get("payload", {}) or {}),
        "folder": "inbox" if "INBOX" in label_ids else "sent" if "SENT" in label_ids else "",
        "read": "UNREAD" not in label_ids,
        "starred": "STARRED" in label_ids,
    }


def _gmail_extract_body_text(payload: dict[str, Any]) -> str:
    plain = _gmail_extract_body_text_for_mime(payload, "text/plain")
    if plain:
        return plain
    html = _gmail_extract_body_text_for_mime(payload, "text/html")
    if html:
        return html
    body = (payload.get("body") or {}) if isinstance(payload, dict) else {}
    data = body.get("data")
    if isinstance(data, str):
        return _gmail_decode_body_data(data)
    return ""


def _gmail_extract_body_text_for_mime(payload: dict[str, Any], mime_type: str) -> str:
    if not isinstance(payload, dict):
        return ""
    if payload.get("mimeType") == mime_type:
        data = (payload.get("body") or {}).get("data")
        if isinstance(data, str):
            return _gmail_decode_body_data(data)
    for part in payload.get("parts", []) or []:
        text = _gmail_extract_body_text_for_mime(part, mime_type)
        if text:
            return text
    return ""


def _gmail_decode_body_data(data: str) -> str:
    padding = "=" * (-len(data) % 4)
    try:
        decoded = base64.urlsafe_b64decode((data + padding).encode("ascii"))
    except (ValueError, binascii.Error):
        return ""
    return decoded.decode("utf-8", errors="replace")


def _parse_himalaya_read_output(message_id: str, stdout: str) -> dict[str, Any]:
    headers: dict[str, str] = {}
    body_lines: list[str] = []
    in_body = False
    for raw_line in stdout.splitlines():
        line = raw_line.rstrip()
        if not in_body and not line.strip():
            in_body = True
            continue
        if not in_body and ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
        else:
            in_body = True
            body_lines.append(raw_line)
    return {
        "id": message_id,
        "sender": headers.get("from", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "subject": headers.get("subject", ""),
        "body": "\n".join(body_lines).strip(),
        "folder": headers.get("folder", ""),
        "read": headers.get("read", "").lower() in {"true", "yes", "1"},
        "starred": headers.get("starred", "").lower() in {"true", "yes", "1"},
    }
