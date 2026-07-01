"""Calendar skill implementation with optional real provider calls."""

from __future__ import annotations

import datetime as dt
import json
import os
import shlex
import shutil
import subprocess
import urllib.parse
from pathlib import Path
from typing import Any

from openclaw_env.backend.base import CommandResult
from openclaw_env.skills.base import Skill

_EVENT_COUNTER = 0
_LAST_ONLINE_TIME_TRACE: list[dict[str, Any]] = []
_PLACEHOLDER_VALUES = {"TIMEZONE", "LOCATION", "TITLE", "DATETIME", "DATE", "NAME", "SCHEDULE", "QUERY", "N"}


class _StrictOnlineCalendarError(RuntimeError):
    pass


def _new_event_id() -> str:
    global _EVENT_COUNTER
    _EVENT_COUNTER += 1
    return f"evt_{_EVENT_COUNTER:04d}"


def _get_arg(args: list[str], flag: str, default: str | None = None) -> str | None:
    for i, a in enumerate(args):
        if a == flag and i + 1 < len(args):
            return args[i + 1]
    return default


def _get_flag(args: list[str], flag: str) -> bool:
    return flag in args


def _looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().strip("`'\"[](){}.,:;")
    return normalized in _PLACEHOLDER_VALUES


class CalendarSkill(Skill):
    """Calendar skill with local event state + optional online provider side effects."""

    def __init__(self) -> None:
        super().__init__(prefixes=("calendar", "gcalcli"))
        self._events: list[dict[str, Any]] = []
        self._state_dir: str = ""
        self._initialized = False
        self._enable_online_data = False
        self._strict_online_data = False
        self._calendar_provider_preference = "google_api"
        self._google_settings: dict[str, Any] = {}

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        global _EVENT_COUNTER
        _EVENT_COUNTER = 0
        self._state_dir = state_dir
        self._events = []
        self._initialized = True
        preload_path = Path(state_dir) / "calendar_events.json"
        if preload_path.exists():
            try:
                payload = json.loads(preload_path.read_text(encoding="utf-8"))
                if isinstance(payload, list):
                    self._events = payload
            except Exception:
                self._events = []
        val = str(env_vars.get("OPENCLAW_ENV_ENABLE_ONLINE_DATA", "")).lower()
        self._enable_online_data = val in {"1", "true", "yes", "on"}
        strict_val = str(env_vars.get("OPENCLAW_ENV_STRICT_ONLINE_DATA", "")).lower()
        self._strict_online_data = strict_val in {"1", "true", "yes", "on"}
        provider = str(env_vars.get("OPENCLAW_ENV_CALENDAR_PROVIDER", "google_api")).strip().lower()
        if provider in {"auto", "gcalcli", "khal", "mock", "google_api"}:
            self._calendar_provider_preference = provider
        else:
            self._calendar_provider_preference = "google_api"
        self._google_settings = _build_google_settings(env_vars)

    def execute(self, command: str) -> CommandResult:
        parts = shlex.split(command.strip())
        if not parts:
            return CommandResult(stdout="", stderr="Not a calendar command", exit_code=1)

        if parts[0] not in {"calendar", "gcalcli"}:
            return CommandResult(stdout="", stderr="Not a calendar command", exit_code=1)

        parse = self._parse_calendar_command(parts)
        if isinstance(parse, CommandResult):
            return parse
        sub, args = parse

        if not sub:
            return CommandResult(
                stdout=(
                    "calendar <subcommand> [options]\n"
                    "Subcommands: list, add-event, delete-event, update-event, search, today\n"
                    "gcalcli <subcommand> [options]\n"
                    "Subcommands: agenda, add, edit, delete, search, now"
                ),
                stderr="",
                exit_code=0,
            )

        handlers = {
            "list": self._cmd_list,
            "add-event": self._cmd_add_event,
            "delete-event": self._cmd_delete_event,
            "update-event": self._cmd_update_event,
            "search": self._cmd_search,
            "today": self._cmd_today,
        }

        handler = handlers.get(sub)
        if handler is None:
            return CommandResult(
                stdout="", stderr=f"Unknown calendar subcommand: {sub}", exit_code=1
            )
        try:
            return handler(args)
        except _StrictOnlineCalendarError as exc:
            return CommandResult(stdout="", stderr=str(exc), exit_code=1)

    def cleanup(self) -> None:
        self._events = []
        self._initialized = False

    def get_state(self) -> dict[str, Any]:
        return {"calendar_events": list(self._events)}

    def _parse_calendar_command(
        self, parts: list[str]
    ) -> tuple[str, list[str]] | CommandResult:
        if parts[0] == "calendar":
            if len(parts) < 2:
                return ("", [])
            return (parts[1], parts[2:])
        return self._translate_gcalcli(parts[1:])

    def _translate_gcalcli(
        self, args: list[str]
    ) -> tuple[str, list[str]] | CommandResult:
        if not args:
            return ("", [])

        sub = args[0]
        rest = args[1:]

        if sub in {"agenda", "list"}:
            from_date = rest[0] if len(rest) >= 1 and not rest[0].startswith("-") else None
            to_date = rest[1] if len(rest) >= 2 and not rest[1].startswith("-") else None
            mapped_args: list[str] = []
            if from_date:
                mapped_args.extend(["--from", from_date])
            if to_date:
                mapped_args.extend(["--to", to_date])
            return ("list", mapped_args)

        if sub in {"add", "quick"}:
            title = _get_arg(rest, "--title")
            when = _get_arg(rest, "--when")
            end = _get_arg(rest, "--end")
            where = _get_arg(rest, "--where")
            attendees = _get_arg(rest, "--who")
            mapped_args = []
            if title:
                mapped_args.extend(["--title", title])
            if when:
                mapped_args.extend(["--start", when])
            if end:
                mapped_args.extend(["--end", end])
            if where:
                mapped_args.extend(["--location", where])
            if attendees:
                mapped_args.extend(["--attendees", attendees])
            return ("add-event", mapped_args)

        if sub in {"edit", "update"}:
            event_id = _get_arg(rest, "--id")
            title = _get_arg(rest, "--title")
            when = _get_arg(rest, "--when")
            where = _get_arg(rest, "--where")
            mapped_args = []
            if event_id:
                mapped_args.extend(["--id", event_id])
            if title:
                mapped_args.extend(["--title", title])
            if when:
                mapped_args.extend(["--start", when])
            if where:
                mapped_args.extend(["--location", where])
            return ("update-event", mapped_args)

        if sub in {"delete", "remove"}:
            event_id = _get_arg(rest, "--id")
            if event_id:
                return ("delete-event", ["--id", event_id])
            return ("delete-event", [])

        if sub == "search":
            query = _get_arg(rest, "--query")
            if query:
                return ("search", ["--query", query])
            if rest and not rest[0].startswith("-"):
                return ("search", ["--query", rest[0]])
            return ("search", [])

        if sub in {"today", "now"}:
            timezone = _get_arg(rest, "--timezone")
            mapped_args = []
            if timezone:
                mapped_args.extend(["--timezone", timezone])
            if _get_flag(rest, "--online"):
                mapped_args.append("--online")
            return ("today", mapped_args)

        return CommandResult(
            stdout="",
            stderr=f"Unknown gcalcli subcommand: {sub}",
            exit_code=1,
        )

    def _cmd_list(self, args: list[str]) -> CommandResult:
        from_date = _get_arg(args, "--from")
        to_date = _get_arg(args, "--to")
        execution_trace = self._online_side_effect_or_fail(
            "list",
            from_date=from_date,
            to_date=to_date,
        )

        events = self._events
        if from_date:
            events = [e for e in events if e["start"] >= from_date]
        if to_date:
            events = [e for e in events if e["start"] <= to_date]

        if not events:
            return CommandResult(
                stdout="No events found.",
                stderr="",
                exit_code=0,
                execution_trace=execution_trace or None,
            )

        lines = ["Upcoming events:"]
        for ev in sorted(events, key=lambda e: e["start"]):
            attendees_str = ""
            if ev.get("attendees"):
                attendees_str = f" | Attendees: {', '.join(ev['attendees'])}"
            location_str = f" @ {ev['location']}" if ev.get("location") else ""
            lines.append(
                f"  [{ev['id']}] {ev['title']} — {ev['start']}{location_str}{attendees_str}"
            )
        return CommandResult(
            stdout="\n".join(lines),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_add_event(self, args: list[str]) -> CommandResult:
        title = _get_arg(args, "--title")
        start = _get_arg(args, "--start")
        end = _get_arg(args, "--end")
        location = _get_arg(args, "--location")
        attendees_raw = _get_arg(args, "--attendees")

        if not title:
            return CommandResult(stdout="", stderr="--title is required", exit_code=1)
        if not start:
            return CommandResult(stdout="", stderr="--start is required", exit_code=1)

        attendees: list[str] = []
        if attendees_raw:
            attendees = [a.strip() for a in attendees_raw.split(",")]
        execution_trace = self._online_side_effect_or_fail(
            "add",
            title=title,
            start=start,
            end=end or start,
            location=location,
            attendees=attendees,
        )

        event_id = _new_event_id()
        event: dict[str, Any] = {
            "id": event_id,
            "title": title,
            "start": start,
            "end": end or start,
            "location": location,
            "attendees": attendees,
        }
        self._events.append(event)

        return CommandResult(
            stdout=f"Event created: [{event_id}] {title} at {start}",
            stderr="",
            exit_code=0,
            state_changes={"calendar_events_created": [event]},
            execution_trace=execution_trace or None,
        )

    def _cmd_delete_event(self, args: list[str]) -> CommandResult:
        event_id = _get_arg(args, "--id")
        if not event_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)

        before = len(self._events)
        self._events = [e for e in self._events if e["id"] != event_id]
        if len(self._events) == before:
            return CommandResult(
                stdout="", stderr=f"Event not found: {event_id}", exit_code=1
            )
        return CommandResult(
            stdout=f"Event {event_id} deleted.",
            stderr="",
            exit_code=0,
            state_changes={"calendar_events_deleted": [{"id": event_id}]},
        )

    def _cmd_update_event(self, args: list[str]) -> CommandResult:
        event_id = _get_arg(args, "--id")
        if not event_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)

        event = next((e for e in self._events if e["id"] == event_id), None)
        if event is None:
            return CommandResult(
                stdout="", stderr=f"Event not found: {event_id}", exit_code=1
            )

        title = _get_arg(args, "--title")
        start = _get_arg(args, "--start")
        location = _get_arg(args, "--location")

        if title:
            event["title"] = title
        if start:
            event["start"] = start
        if location:
            event["location"] = location

        return CommandResult(
            stdout=f"Event {event_id} updated.",
            stderr="",
            exit_code=0,
            state_changes={"calendar_events_updated": [event]},
        )

    def _cmd_search(self, args: list[str]) -> CommandResult:
        query = _get_arg(args, "--query")
        if not query:
            return CommandResult(stdout="", stderr="--query is required", exit_code=1)
        execution_trace = self._online_side_effect_or_fail("search", query=query)

        q = query.lower()
        results = [
            e for e in self._events
            if q in e["title"].lower()
            or q in (e.get("location") or "").lower()
        ]

        if not results:
            return CommandResult(
                stdout=f"No events matching '{query}'.",
                stderr="",
                exit_code=0,
                execution_trace=execution_trace or None,
            )

        lines = [f"Events matching '{query}':"]
        for ev in results:
            lines.append(f"  [{ev['id']}] {ev['title']} — {ev['start']}")
        return CommandResult(
            stdout="\n".join(lines),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_today(self, args: list[str]) -> CommandResult:
        timezone = _get_arg(args, "--timezone", "UTC") or "UTC"
        if _looks_like_placeholder(timezone):
            return CommandResult(
                stdout="",
                stderr=f"Invalid timezone value: {timezone}",
                exit_code=1,
            )
        use_online = _get_flag(args, "--online") or self._enable_online_data

        now_iso: str | None = None
        source = "mock"
        execution_trace: list[dict[str, Any]] = []
        if use_online and self._enable_online_data:
            _clear_last_online_time_trace()
            now_iso = _get_online_time(timezone)
            execution_trace = _consume_last_online_time_trace()
            if now_iso:
                source = "online"

        if not now_iso:
            if use_online and self._enable_online_data and self._strict_online_data:
                return CommandResult(
                    stdout="",
                    stderr=(
                        f"Online time data unavailable for timezone '{timezone}'. "
                        "Strict online mode is enabled, so mock fallback is disabled."
                    ),
                    exit_code=1,
                )
            now_iso = _mock_time_for_timezone(timezone)
            if use_online and self._enable_online_data:
                source = "mock-fallback"

        return CommandResult(
            stdout=(
                f"Current date-time for {timezone}: {now_iso}\n"
                f"Source: {source}"
            ),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _online_side_effect_or_fail(self, action: str, **kwargs: Any) -> list[dict[str, Any]]:
        if not self._enable_online_data:
            return []
        ok, err, trace = _try_online_calendar_action(
            action=action,
            provider_preference=self._calendar_provider_preference,
            google_settings=self._google_settings,
            **kwargs,
        )
        if ok or not self._strict_online_data:
            return trace
        raise _StrictOnlineCalendarError(
            f"Online calendar action '{action}' failed: {err}. "
            "Strict online mode is enabled, so mock fallback is disabled."
        )


def _mock_time_for_timezone(timezone: str) -> str:
    base = dt.datetime(2026, 3, 1, 9, 0, 0)
    offsets = {
        "utc": 0,
        "asia/shanghai": 8,
        "america/new_york": -5,
        "europe/london": 0,
        "asia/tokyo": 9,
    }
    offset = offsets.get(timezone.strip().lower(), 0)
    value = base + dt.timedelta(hours=offset)
    return value.isoformat()


def _try_online_calendar_action(
    action: str,
    provider_preference: str,
    google_settings: dict[str, Any] | None = None,
    **kwargs: Any,
) -> tuple[bool, str, list[dict[str, Any]]]:
    provider = _resolve_calendar_provider(provider_preference)
    if not provider:
        return (
            False,
            "No supported calendar provider found (gcalcli/khal).",
            [],
        )

    if provider == "google_api":
        exit_code, stdout, stderr, trace = _run_google_api_action(
            action=action,
            kwargs=kwargs,
            settings=google_settings or {},
        )
    else:
        cmd = _build_calendar_provider_command(provider, action, **kwargs)
        if not cmd:
            return (
                False,
                f"Provider '{provider}' does not support action '{action}' for these arguments.",
                [],
            )
        exit_code, stdout, stderr = _run_calendar_provider_command(cmd, timeout=20)
        trace = [
            {
                "action": shlex.join(cmd),
                "provider": provider,
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": exit_code,
            }
        ]
    if exit_code == 0:
        return True, "", trace
    err_text = (stderr or "").strip() or "unknown error"
    return False, f"{provider} exited with code {exit_code}: {err_text}", trace


def _resolve_calendar_provider(preference: str) -> str | None:
    pref = preference.strip().lower()
    if pref == "mock":
        return None
    if pref == "google_api":
        return "google_api"
    if pref in {"gcalcli", "khal"}:
        return pref if shutil.which(pref) else None
    for candidate in ("gcalcli", "khal"):
        if shutil.which(candidate):
            return candidate
    return None


def _build_google_settings(env_vars: dict[str, str]) -> dict[str, Any]:
    scopes = env_vars.get(
        "OPENCLAW_ENV_GOOGLE_SCOPES",
        "https://www.googleapis.com/auth/calendar",
    )
    scopes_list = [s.strip() for s in scopes.split(",") if s.strip()]
    token_file = env_vars.get("OPENCLAW_ENV_GOOGLE_TOKEN_FILE", "").strip()
    if not token_file:
        token_file = os.path.expanduser("~/.openclaw/google_calendar_token.json")
    client_secret_file = env_vars.get("OPENCLAW_ENV_GOOGLE_CLIENT_SECRET_FILE", "").strip()
    return {
        "calendar_id": env_vars.get("OPENCLAW_ENV_GOOGLE_CALENDAR_ID", "primary").strip() or "primary",
        "timezone": env_vars.get("OPENCLAW_ENV_GOOGLE_TIMEZONE", "UTC").strip() or "UTC",
        "token_file": token_file,
        "client_secret_file": client_secret_file,
        "scopes": scopes_list or ["https://www.googleapis.com/auth/calendar"],
    }


def _run_google_api_action(
    action: str,
    kwargs: dict[str, Any],
    settings: dict[str, Any],
) -> tuple[int, str, str, list[dict[str, Any]]]:
    trace: list[dict[str, Any]] = []
    try:
        service = _build_google_calendar_service(settings)
    except Exception as exc:
        return 1, "", str(exc), trace

    calendar_id = str(settings.get("calendar_id") or "primary")
    timezone = str(settings.get("timezone") or "UTC")
    try:
        if action == "add":
            title = str(kwargs.get("title") or "").strip()
            start = str(kwargs.get("start") or "").strip()
            end = str(kwargs.get("end") or "").strip() or start
            location = str(kwargs.get("location") or "").strip()
            attendees = kwargs.get("attendees") if isinstance(kwargs.get("attendees"), list) else []
            if not title or not start:
                return 1, "", "title/start missing", trace
            body: dict[str, Any] = {
                "summary": title,
                "start": {"dateTime": _google_iso_datetime(start), "timeZone": timezone},
                "end": {"dateTime": _google_iso_datetime(end), "timeZone": timezone},
            }
            if location:
                body["location"] = location
            if attendees:
                body["attendees"] = [{"email": str(a)} for a in attendees if str(a).strip()]
            resp = (
                service.events()
                .insert(calendarId=calendar_id, body=body)
                .execute()
            )
            stdout = json.dumps(resp, ensure_ascii=False)
            trace.append(
                {
                    "action": "google_api.events.insert",
                    "provider": "google_api",
                    "request": {
                        "calendar_id": calendar_id,
                        "title": title,
                        "start": start,
                        "end": end,
                        "timezone": timezone,
                        "location": location or None,
                        "attendees_count": len(attendees),
                    },
                    "replay_cmd": _google_calendar_replay_cmd(
                        action="insert",
                        calendar_id=calendar_id,
                        body=body,
                    ),
                    "stdout": stdout,
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return 0, stdout, "", trace

        if action == "list":
            from_date = str(kwargs.get("from_date") or "").strip()
            to_date = str(kwargs.get("to_date") or "").strip()
            req: dict[str, Any] = {
                "calendarId": calendar_id,
                "singleEvents": True,
                "orderBy": "startTime",
                "maxResults": 50,
            }
            if from_date:
                req["timeMin"] = _google_iso_datetime(from_date + "T00:00:00")
            if to_date:
                req["timeMax"] = _google_iso_datetime(to_date + "T23:59:59")
            resp = service.events().list(**req).execute()
            stdout = json.dumps(resp, ensure_ascii=False)
            trace.append(
                {
                    "action": "google_api.events.list",
                    "provider": "google_api",
                    "request": {
                        "calendar_id": calendar_id,
                        "from_date": from_date or None,
                        "to_date": to_date or None,
                        "max_results": req.get("maxResults"),
                    },
                    "replay_cmd": _google_calendar_replay_cmd(
                        action="list",
                        calendar_id=calendar_id,
                        request_params=req,
                    ),
                    "stdout": stdout,
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return 0, stdout, "", trace

        if action == "search":
            query = str(kwargs.get("query") or "").strip()
            if not query:
                return 1, "", "query missing", trace
            resp = (
                service.events()
                .list(
                    calendarId=calendar_id,
                    q=query,
                    singleEvents=True,
                    orderBy="startTime",
                    maxResults=25,
                )
                .execute()
            )
            stdout = json.dumps(resp, ensure_ascii=False)
            trace.append(
                {
                    "action": "google_api.events.list?q",
                    "provider": "google_api",
                    "request": {
                        "calendar_id": calendar_id,
                        "query": query,
                        "max_results": 25,
                    },
                    "replay_cmd": _google_calendar_replay_cmd(
                        action="search",
                        calendar_id=calendar_id,
                        request_params={
                            "calendarId": calendar_id,
                            "q": query,
                            "singleEvents": True,
                            "orderBy": "startTime",
                            "maxResults": 25,
                        },
                    ),
                    "stdout": stdout,
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return 0, stdout, "", trace

        return 1, "", f"unsupported action for google_api: {action}", trace
    except Exception as exc:  # pragma: no cover - external API surface
        return 1, "", str(exc), trace


def _build_google_calendar_service(settings: dict[str, Any]):
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

    scopes = settings.get("scopes") or ["https://www.googleapis.com/auth/calendar"]
    token_file = os.path.expanduser(str(settings.get("token_file") or "~/.openclaw/google_calendar_token.json"))
    client_secret_file = str(settings.get("client_secret_file") or "").strip()

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not client_secret_file:
            raise RuntimeError(
                "Missing OPENCLAW_ENV_GOOGLE_CLIENT_SECRET_FILE for google_api provider."
            )
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
        try:
            creds = flow.run_console()
        except Exception:
            creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(token_file), exist_ok=True)
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def _google_calendar_replay_cmd(
    *,
    action: str,
    calendar_id: str,
    body: dict[str, Any] | None = None,
    request_params: dict[str, Any] | None = None,
) -> str:
    calendar_id_enc = urllib.parse.quote(calendar_id, safe="")
    base_url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id_enc}/events"
    auth_header = "Authorization: Bearer <ACCESS_TOKEN>"

    if action == "insert":
        payload = json.dumps(body or {}, ensure_ascii=False, separators=(",", ":"))
        cmd = [
            "curl",
            "-sS",
            "-X",
            "POST",
            base_url,
            "-H",
            auth_header,
            "-H",
            "Content-Type: application/json",
            "--data-raw",
            payload,
        ]
        return shlex.join(cmd)

    cmd = [
        "curl",
        "-sS",
        "--get",
        base_url,
        "-H",
        auth_header,
    ]
    params = request_params or {}
    for key in ("singleEvents", "orderBy", "maxResults", "timeMin", "timeMax", "q"):
        if key not in params:
            continue
        value = params.get(key)
        if value is None:
            continue
        cmd.extend(["--data-urlencode", f"{key}={value}"])
    return shlex.join(cmd)


def _google_iso_datetime(raw: str) -> str:
    text = raw.strip()
    if not text:
        raise ValueError("datetime is empty")
    if text.endswith("Z") or "+" in text[10:] or "-" in text[10:]:
        return text
    dt_value = dt.datetime.fromisoformat(text)
    return dt_value.isoformat()


def _build_calendar_provider_command(
    provider: str,
    action: str,
    **kwargs: Any,
) -> list[str] | None:
    if provider == "gcalcli":
        if action == "add":
            title = str(kwargs.get("title") or "").strip()
            start = _format_cli_datetime(str(kwargs.get("start") or "").strip())
            if not title or not start:
                return None
            cmd = ["gcalcli", "add", "--title", title, "--when", start]
            end_value = _format_cli_datetime(str(kwargs.get("end") or "").strip())
            if end_value:
                cmd.extend(["--end", end_value])
            location = str(kwargs.get("location") or "").strip()
            if location:
                cmd.extend(["--where", location])
            attendees = kwargs.get("attendees")
            if isinstance(attendees, list) and attendees:
                cmd.extend(["--who", ",".join(str(a) for a in attendees if str(a).strip())])
            return cmd
        if action == "list":
            cmd = ["gcalcli", "agenda"]
            from_date = str(kwargs.get("from_date") or "").strip()
            to_date = str(kwargs.get("to_date") or "").strip()
            if from_date:
                cmd.append(from_date)
            if to_date:
                cmd.append(to_date)
            return cmd
        if action == "search":
            query = str(kwargs.get("query") or "").strip()
            if not query:
                return None
            return ["gcalcli", "search", query]
        return None

    if provider == "khal":
        if action == "add":
            title = str(kwargs.get("title") or "").strip()
            start = _parse_iso_datetime(str(kwargs.get("start") or "").strip())
            end = _parse_iso_datetime(str(kwargs.get("end") or "").strip())
            if not title or start is None:
                return None
            if end is None:
                end = start + dt.timedelta(hours=1)
            return [
                "khal",
                "new",
                start.strftime("%Y-%m-%d"),
                start.strftime("%H:%M"),
                end.strftime("%H:%M"),
                title,
            ]
        if action == "list":
            cmd = ["khal", "list"]
            from_date = str(kwargs.get("from_date") or "").strip()
            to_date = str(kwargs.get("to_date") or "").strip()
            if from_date:
                cmd.append(from_date)
            if to_date:
                cmd.append(to_date)
            return cmd
        if action == "search":
            query = str(kwargs.get("query") or "").strip()
            if not query:
                return None
            return ["khal", "search", query]
        return None

    return None


def _run_calendar_provider_command(cmd: list[str], timeout: int) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except Exception as exc:  # pragma: no cover
        return 1, "", str(exc)


def _format_cli_datetime(value: str) -> str:
    parsed = _parse_iso_datetime(value)
    if parsed is None:
        return value
    return parsed.strftime("%Y-%m-%d %H:%M")


def _parse_iso_datetime(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value)
    except Exception:
        return None


def _get_online_time(timezone: str) -> str | None:
    tz = timezone.strip()
    tz_path = urllib.parse.quote(tz, safe="/")
    commands = [
        ["curl", "-s", f"https://worldtimeapi.org/api/timezone/{tz_path}"],
        ["curl", "-s", f"http://worldtimeapi.org/api/timezone/{tz_path}"],
        [
            "curl",
            "-sG",
            "https://timeapi.io/api/Time/current/zone",
            "--data-urlencode",
            f"timeZone={tz}",
        ],
    ]

    trace: list[dict[str, Any]] = []
    for cmd in commands:
        rc, stdout, stderr = _run_calendar_provider_command(cmd, timeout=6)
        trace.append(
            {
                "action": shlex.join(cmd),
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": rc,
            }
        )
        if rc != 0:
            continue
        payload = _safe_json(stdout)
        if not isinstance(payload, dict):
            continue

        dt_value = payload.get("datetime")
        if isinstance(dt_value, str) and dt_value:
            _set_last_online_time_trace(trace)
            return dt_value

        y = payload.get("year")
        m = payload.get("month")
        d = payload.get("day")
        hh = payload.get("hour", 0)
        mm = payload.get("minute", 0)
        ss = payload.get("seconds", 0)
        try:
            result = dt.datetime(
                int(y), int(m), int(d), int(hh), int(mm), int(ss)
            ).isoformat()
            _set_last_online_time_trace(trace)
            return result
        except Exception:
            continue

    _set_last_online_time_trace(trace)
    return None


def _safe_json(text: str) -> Any:
    try:
        return json.loads((text or "").strip() or "{}")
    except Exception:
        return None


def _set_last_online_time_trace(trace: list[dict[str, Any]]) -> None:
    global _LAST_ONLINE_TIME_TRACE
    _LAST_ONLINE_TIME_TRACE = list(trace)


def _consume_last_online_time_trace() -> list[dict[str, Any]]:
    global _LAST_ONLINE_TIME_TRACE
    value = list(_LAST_ONLINE_TIME_TRACE)
    _LAST_ONLINE_TIME_TRACE = []
    return value


def _clear_last_online_time_trace() -> None:
    global _LAST_ONLINE_TIME_TRACE
    _LAST_ONLINE_TIME_TRACE = []
