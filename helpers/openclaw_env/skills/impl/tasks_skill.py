"""Tasks skill implementation with optional online provider side effects."""

from __future__ import annotations

import copy
import datetime as dt
import json
import os
import shlex
from pathlib import Path
from typing import Any

from openclaw_env.backend.base import CommandResult
from openclaw_env.skills.base import Skill

_TASK_COUNTER = 0


_VALID_PRIORITIES = {"high", "medium", "low"}
_VALID_STATUSES = {"all", "pending", "done"}

# Seeded tasks for search/complete tasks
_SEEDED_TASKS: list[dict[str, Any]] = [
    {
        "id": "task_seed_1",
        "title": "Review project proposal",
        "due": "2026-03-05",
        "status": "pending",
        "priority": "high",
        "duration": 2,
    },
    {
        "id": "task_seed_2",
        "title": "Write quarterly report",
        "due": "2026-03-10",
        "status": "pending",
        "priority": "medium",
        "duration": 4,
    },
    {
        "id": "task_seed_3",
        "title": "Schedule team standup",
        "due": "2026-03-03",
        "status": "pending",
        "priority": "low",
        "duration": 1,
    },
]


class TasksSkill(Skill):
    """Tasks skill with deterministic local state and optional online side effects."""

    def __init__(self) -> None:
        super().__init__(prefixes=("tasks",))
        self._tasks: list[dict[str, Any]] = []
        self._initialized = False
        self._enable_online_data = False
        self._strict_online_data = False
        self._tasks_provider_preference = "auto"
        self._google_settings: dict[str, Any] = {}
        self._online_ids_by_local_id: dict[str, str] = {}

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        global _TASK_COUNTER
        _TASK_COUNTER = 100  # start above seed IDs
        self._tasks = [copy.deepcopy(t) for t in _SEEDED_TASKS]
        self._online_ids_by_local_id = {}
        self._initialized = True
        preload_path = Path(state_dir) / "tasks.json"
        if preload_path.exists():
            try:
                payload = json.loads(preload_path.read_text(encoding="utf-8"))
                if isinstance(payload, list):
                    self._tasks.extend(copy.deepcopy(payload))
            except Exception:
                pass

        val = str(env_vars.get("OPENCLAW_ENV_ENABLE_ONLINE_DATA", "")).lower()
        self._enable_online_data = val in {"1", "true", "yes", "on"}
        strict_val = str(env_vars.get("OPENCLAW_ENV_STRICT_ONLINE_DATA", "")).lower()
        self._strict_online_data = strict_val in {"1", "true", "yes", "on"}

        provider = str(env_vars.get("OPENCLAW_ENV_TASKS_PROVIDER", "auto")).strip().lower()
        if provider in {"auto", "google_api", "mock"}:
            self._tasks_provider_preference = provider
        else:
            self._tasks_provider_preference = "mock"

        self._google_settings = _build_google_tasks_settings(env_vars)

    def execute(self, command: str) -> CommandResult:
        parts = shlex.split(command.strip())
        if not parts or parts[0] != "tasks":
            return CommandResult(stdout="", stderr="Not a tasks command", exit_code=1)

        if len(parts) < 2:
            return CommandResult(
                stdout=(
                    "tasks <subcommand> [options]\n"
                    "Subcommands: list, add, complete, delete, update, search"
                ),
                stderr="",
                exit_code=0,
            )

        sub = parts[1]
        args = parts[2:]

        handlers = {
            "list": self._cmd_list,
            "add": self._cmd_add,
            "complete": self._cmd_complete,
            "delete": self._cmd_delete,
            "update": self._cmd_update,
            "search": self._cmd_search,
        }

        handler = handlers.get(sub)
        if handler is None:
            return CommandResult(
                stdout="", stderr=f"Unknown tasks subcommand: {sub}", exit_code=1
            )
        return handler(args)

    def cleanup(self) -> None:
        self._tasks = []
        self._online_ids_by_local_id = {}
        self._initialized = False

    def get_state(self) -> dict[str, Any]:
        return {"tasks": list(self._tasks)}

    def _cmd_list(self, args: list[str]) -> CommandResult:
        status = _get_arg(args, "--status", "pending")
        priority = _get_arg(args, "--priority")

        execution_trace: list[dict[str, Any]] = []
        ok, err, _ = self._online_side_effect(
            execution_trace,
            action="list",
            status=status,
            priority=priority,
        )
        if not ok and self._strict_online_data:
            return CommandResult(
                stdout="",
                stderr=(
                    f"Online tasks action 'list' failed: {err}. "
                    "Strict online mode is enabled, so local fallback is disabled."
                ),
                exit_code=1,
                execution_trace=execution_trace or None,
            )

        tasks = self._tasks
        if status != "all":
            if status == "done":
                tasks = [t for t in tasks if t["status"] == "done"]
            else:
                tasks = [t for t in tasks if t["status"] == "pending"]

        if priority:
            if priority not in _VALID_PRIORITIES:
                return CommandResult(
                    stdout="",
                    stderr=f"--priority must be one of: {', '.join(_VALID_PRIORITIES)}",
                    exit_code=1,
                )
            tasks = [t for t in tasks if t["priority"] == priority]

        if not tasks:
            return CommandResult(
                stdout="No tasks found.",
                stderr="",
                exit_code=0,
                execution_trace=execution_trace or None,
            )

        lines = ["Tasks:"]
        for task in sorted(tasks, key=lambda x: (x["due"] or "9999", x["priority"])):
            status_icon = "✓" if task["status"] == "done" else "○"
            lines.append(
                f"  [{task['id']}] {status_icon} [{task['priority']}] {task['title']}"
                + (f" (due {task['due']})" if task["due"] else "")
            )
        return CommandResult(
            stdout="\n".join(lines),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_add(self, args: list[str]) -> CommandResult:
        title = _get_arg(args, "--title")
        due = _get_arg(args, "--due")
        priority = _get_arg(args, "--priority", "medium")
        duration_str = _get_arg(args, "--duration")

        if not title:
            return CommandResult(stdout="", stderr="--title is required", exit_code=1)
        if priority not in _VALID_PRIORITIES:
            return CommandResult(
                stdout="",
                stderr=f"--priority must be one of: {', '.join(_VALID_PRIORITIES)}",
                exit_code=1,
            )

        duration: float | None = None
        if duration_str:
            try:
                duration = float(duration_str)
            except ValueError:
                return CommandResult(
                    stdout="", stderr="--duration must be a number", exit_code=1
                )

        execution_trace: list[dict[str, Any]] = []
        ok, err, meta = self._online_side_effect(
            execution_trace,
            action="add",
            title=title,
            due=due,
            priority=priority,
            duration=duration,
        )
        if not ok and self._strict_online_data:
            return CommandResult(
                stdout="",
                stderr=(
                    f"Online tasks action 'add' failed: {err}. "
                    "Strict online mode is enabled, so local fallback is disabled."
                ),
                exit_code=1,
                execution_trace=execution_trace or None,
            )

        task_id = _new_task_id()
        task: dict[str, Any] = {
            "id": task_id,
            "title": title,
            "due": due,
            "status": "pending",
            "priority": priority,
            "duration": duration,
        }
        self._tasks.append(task)

        remote_id = str(meta.get("task_id", "")).strip()
        if remote_id:
            self._online_ids_by_local_id[task_id] = remote_id

        return CommandResult(
            stdout=f"Task created: [{task_id}] {title}",
            stderr="",
            exit_code=0,
            state_changes={"tasks_created": [task]},
            execution_trace=execution_trace or None,
        )

    def _cmd_complete(self, args: list[str]) -> CommandResult:
        task_id = _get_arg(args, "--id")
        task_title = _get_arg(args, "--title")
        if not task_id and not task_title:
            return CommandResult(stdout="", stderr="--id or --title is required", exit_code=1)

        task = None
        if task_id:
            task = next((t for t in self._tasks if t["id"] == task_id), None)
        elif task_title:
            task = next((t for t in self._tasks if t["title"] == task_title), None)
        if task is None:
            lookup = task_id or task_title or ""
            return CommandResult(stdout="", stderr=f"Task not found: {lookup}", exit_code=1)

        execution_trace: list[dict[str, Any]] = []
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(task_id)
            if mapped:
                ok, err, _ = self._online_side_effect(
                    execution_trace,
                    action="complete",
                    task_id=mapped,
                    title=task["title"],
                    due=task.get("due"),
                    priority=task.get("priority"),
                    status="completed",
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online tasks action 'complete' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )
            else:
                reason = "unmapped_seed_id" if task_id.startswith("task_seed_") else "unmapped_local_id"
                execution_trace.append(_trace_reason(reason=reason, provider="none", error=f"id={task_id}"))
                if self._strict_online_data and not task_id.startswith("task_seed_"):
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"No online task mapping for '{task_id}'. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        task["status"] = "done"
        return CommandResult(
            stdout=f"Task {task_id} marked as done: {task['title']}",
            stderr="",
            exit_code=0,
            state_changes={"tasks_completed": [task]},
            execution_trace=execution_trace or None,
        )

    def _cmd_delete(self, args: list[str]) -> CommandResult:
        task_id = _get_arg(args, "--id")
        if not task_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)

        task = next((t for t in self._tasks if t["id"] == task_id), None)
        if task is None:
            return CommandResult(stdout="", stderr=f"Task not found: {task_id}", exit_code=1)

        execution_trace: list[dict[str, Any]] = []
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(task_id)
            if mapped:
                ok, err, _ = self._online_side_effect(
                    execution_trace,
                    action="delete",
                    task_id=mapped,
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online tasks action 'delete' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )
            else:
                reason = "unmapped_seed_id" if task_id.startswith("task_seed_") else "unmapped_local_id"
                execution_trace.append(_trace_reason(reason=reason, provider="none", error=f"id={task_id}"))
                if self._strict_online_data and not task_id.startswith("task_seed_"):
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"No online task mapping for '{task_id}'. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        self._tasks = [t for t in self._tasks if t["id"] != task_id]
        self._online_ids_by_local_id.pop(task_id, None)
        return CommandResult(
            stdout=f"Task {task_id} deleted.",
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_update(self, args: list[str]) -> CommandResult:
        task_id = _get_arg(args, "--id")
        if not task_id:
            return CommandResult(stdout="", stderr="--id is required", exit_code=1)

        task = next((t for t in self._tasks if t["id"] == task_id), None)
        if task is None:
            return CommandResult(stdout="", stderr=f"Task not found: {task_id}", exit_code=1)

        title = _get_arg(args, "--title")
        due = _get_arg(args, "--due")
        priority = _get_arg(args, "--priority")

        if priority and priority not in _VALID_PRIORITIES:
            return CommandResult(
                stdout="",
                stderr=f"--priority must be one of: {', '.join(_VALID_PRIORITIES)}",
                exit_code=1,
            )

        execution_trace: list[dict[str, Any]] = []
        if self._enable_online_data:
            mapped = self._online_ids_by_local_id.get(task_id)
            if mapped:
                next_title = title or task["title"]
                next_due = due or task.get("due")
                next_priority = priority or task.get("priority")
                status = "completed" if task.get("status") == "done" else "needsAction"
                ok, err, _ = self._online_side_effect(
                    execution_trace,
                    action="update",
                    task_id=mapped,
                    title=next_title,
                    due=next_due,
                    priority=next_priority,
                    status=status,
                )
                if not ok and self._strict_online_data:
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"Online tasks action 'update' failed: {err}. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )
            else:
                reason = "unmapped_seed_id" if task_id.startswith("task_seed_") else "unmapped_local_id"
                execution_trace.append(_trace_reason(reason=reason, provider="none", error=f"id={task_id}"))
                if self._strict_online_data and not task_id.startswith("task_seed_"):
                    return CommandResult(
                        stdout="",
                        stderr=(
                            f"No online task mapping for '{task_id}'. "
                            "Strict online mode is enabled, so local fallback is disabled."
                        ),
                        exit_code=1,
                        execution_trace=execution_trace or None,
                    )

        if title:
            task["title"] = title
        if due:
            task["due"] = due
        if priority:
            task["priority"] = priority

        return CommandResult(
            stdout=f"Task {task_id} updated.",
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_search(self, args: list[str]) -> CommandResult:
        query = _get_arg(args, "--query")
        if not query:
            return CommandResult(stdout="", stderr="--query is required", exit_code=1)

        execution_trace: list[dict[str, Any]] = []
        ok, err, _ = self._online_side_effect(
            execution_trace,
            action="search",
            query=query,
        )
        if not ok and self._strict_online_data:
            return CommandResult(
                stdout="",
                stderr=(
                    f"Online tasks action 'search' failed: {err}. "
                    "Strict online mode is enabled, so local fallback is disabled."
                ),
                exit_code=1,
                execution_trace=execution_trace or None,
            )

        q = query.lower()
        results = [t for t in self._tasks if q in t["title"].lower()]

        if not results:
            return CommandResult(
                stdout=f"No tasks matching '{query}'.",
                stderr="",
                exit_code=0,
                execution_trace=execution_trace or None,
            )

        lines = [f"Tasks matching '{query}':"]
        for task in results:
            lines.append(f"  [{task['id']}] {task['title']} ({task['status']})")
        return CommandResult(
            stdout="\n".join(lines),
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
        if self._tasks_provider_preference == "mock":
            return True, "", {}

        ok, err, trace, meta = _run_tasks_online_action(
            action=action,
            provider_preference=self._tasks_provider_preference,
            google_settings=self._google_settings,
            **kwargs,
        )
        execution_trace.extend(trace)
        return ok, err, meta


def _new_task_id() -> str:
    global _TASK_COUNTER
    _TASK_COUNTER += 1
    return f"task_{_TASK_COUNTER:04d}"


def _get_arg(args: list[str], flag: str, default: str | None = None) -> str | None:
    for i, arg in enumerate(args):
        if arg == flag and i + 1 < len(args):
            return args[i + 1]
    return default


def _trace_reason(reason: str, provider: str, error: str = "") -> dict[str, Any]:
    return {
        "action": "tasks.online.fallback",
        "provider": provider,
        "reason": reason,
        "error": error,
        "stdout": "",
        "stderr": error,
        "exit_code": 1 if error else 0,
    }


def _build_google_tasks_settings(env_vars: dict[str, str]) -> dict[str, Any]:
    scopes = env_vars.get(
        "OPENCLAW_ENV_GOOGLE_TASKS_SCOPES",
        "https://www.googleapis.com/auth/tasks",
    )
    scopes_list = [scope.strip() for scope in scopes.split(",") if scope.strip()]

    token_file = env_vars.get("OPENCLAW_ENV_GOOGLE_TASKS_TOKEN_FILE", "").strip()
    if not token_file:
        token_file = env_vars.get("OPENCLAW_ENV_GOOGLE_TOKEN_FILE", "").strip()
    if not token_file:
        token_file = os.path.expanduser("~/.openclaw/google_tasks_token.json")

    return {
        "tasklist_id": env_vars.get("OPENCLAW_ENV_GOOGLE_TASKS_LIST_ID", "@default").strip()
        or "@default",
        "token_file": token_file,
        "client_secret_file": env_vars.get("OPENCLAW_ENV_GOOGLE_CLIENT_SECRET_FILE", "").strip(),
        "scopes": scopes_list or ["https://www.googleapis.com/auth/tasks"],
        "allow_interactive_auth": str(
            env_vars.get("OPENCLAW_ENV_GOOGLE_ALLOW_INTERACTIVE_AUTH", "")
        ).lower()
        in {"1", "true", "yes", "on"},
    }


def _google_tasks_deps_available() -> bool:
    try:
        import google.oauth2.credentials  # noqa: F401
        import google_auth_oauthlib.flow  # noqa: F401
        import googleapiclient.discovery  # noqa: F401
    except Exception:
        return False
    return True


def _google_tasks_provider_available(settings: dict[str, Any], *, require_token: bool) -> bool:
    if not _google_tasks_deps_available():
        return False

    token_file = os.path.expanduser(str(settings.get("token_file", "")).strip())
    has_token = bool(token_file and os.path.isfile(token_file))
    if has_token:
        return True
    if require_token:
        return False

    client_secret = str(settings.get("client_secret_file", "")).strip()
    return bool(client_secret and os.path.isfile(os.path.expanduser(client_secret)))


def _resolve_tasks_provider(
    preference: str,
    google_settings: dict[str, Any],
) -> str | None:
    pref = preference.strip().lower()
    if pref == "mock":
        return None

    if pref == "google_api":
        return "google_api" if _google_tasks_provider_available(google_settings, require_token=False) else None

    # auto
    if _google_tasks_provider_available(google_settings, require_token=True):
        return "google_api"
    return None


def _run_tasks_online_action(
    action: str,
    provider_preference: str,
    google_settings: dict[str, Any],
    **kwargs: Any,
) -> tuple[bool, str, list[dict[str, Any]], dict[str, Any]]:
    provider = _resolve_tasks_provider(provider_preference, google_settings)
    if not provider:
        trace = [
            _trace_reason(
                reason="online_unavailable",
                provider="none",
                error="No supported tasks provider found (google_api).",
            )
        ]
        return False, "No supported tasks provider found (google_api).", trace, {}

    ok, err, trace, meta = _run_google_tasks_action(action, kwargs, google_settings)
    if not ok:
        trace.append(_trace_reason(reason="online_unavailable", provider=provider, error=err))
    return ok, err, trace, meta


def _build_google_tasks_service(
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

    scopes = settings.get("scopes") or ["https://www.googleapis.com/auth/tasks"]
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

    return build("tasks", "v1", credentials=creds, cache_discovery=False)


def _run_google_tasks_action(
    action: str,
    kwargs: dict[str, Any],
    settings: dict[str, Any],
) -> tuple[bool, str, list[dict[str, Any]], dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    try:
        service = _build_google_tasks_service(settings)
    except Exception as exc:
        return False, str(exc), trace, {}

    tasklist_id = str(settings.get("tasklist_id") or "@default")
    meta: dict[str, Any] = {}

    try:
        if action in {"list", "search"}:
            resp = (
                service.tasks()
                .list(
                    tasklist=tasklist_id,
                    maxResults=100,
                    showCompleted=True,
                    showHidden=True,
                )
                .execute()
            )
            items = resp.get("items", []) if isinstance(resp, dict) else []
            if action == "search":
                query = str(kwargs.get("query", "")).strip().lower()
                if query:
                    items = [
                        item
                        for item in items
                        if query in str(item.get("title", "")).lower()
                    ]
            remote_ids = [item.get("id") for item in items if isinstance(item, dict)]
            meta["remote_ids"] = [rid for rid in remote_ids if isinstance(rid, str)]
            trace.append(
                {
                    "action": f"google_api.tasks.{action}",
                    "provider": "google_api",
                    "request": {
                        "tasklist": tasklist_id,
                        "max_results": 100,
                        "show_completed": True,
                        "show_hidden": True,
                        "query": kwargs.get("query") if action == "search" else None,
                    },
                    "replay_cmd": _google_tasks_replay_cmd(
                        action="list",
                        tasklist_id=tasklist_id,
                        request_params={
                            "maxResults": 100,
                            "showCompleted": True,
                            "showHidden": True,
                        },
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "add":
            payload = {
                "title": str(kwargs.get("title") or "").strip(),
                "status": "needsAction",
            }
            due = _to_google_due(kwargs.get("due"))
            if due:
                payload["due"] = due

            resp = service.tasks().insert(tasklist=tasklist_id, body=payload).execute()
            task_id = str(resp.get("id") or "").strip()
            if task_id:
                meta["task_id"] = task_id
            trace.append(
                {
                    "action": "google_api.tasks.insert",
                    "provider": "google_api",
                    "request": {
                        "tasklist": tasklist_id,
                        "body": payload,
                    },
                    "replay_cmd": _google_tasks_replay_cmd(
                        action="insert",
                        tasklist_id=tasklist_id,
                        request_params={"body": payload},
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action in {"update", "complete"}:
            remote_id = str(kwargs.get("task_id") or "").strip()
            if not remote_id:
                return False, "Missing remote task id for update.", trace, meta

            payload = {
                "title": str(kwargs.get("title") or "").strip(),
                "status": str(kwargs.get("status") or "needsAction"),
            }
            due = _to_google_due(kwargs.get("due"))
            if due:
                payload["due"] = due

            resp = (
                service.tasks()
                .patch(tasklist=tasklist_id, task=remote_id, body=payload)
                .execute()
            )
            trace.append(
                {
                    "action": "google_api.tasks.patch",
                    "provider": "google_api",
                    "request": {
                        "tasklist": tasklist_id,
                        "task": remote_id,
                        "body": payload,
                    },
                    "replay_cmd": _google_tasks_replay_cmd(
                        action="patch",
                        tasklist_id=tasklist_id,
                        task_id=remote_id,
                        request_params={"body": payload},
                    ),
                    "stdout": json.dumps(resp, ensure_ascii=False),
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        if action == "delete":
            remote_id = str(kwargs.get("task_id") or "").strip()
            if not remote_id:
                return False, "Missing remote task id for delete.", trace, meta

            service.tasks().delete(tasklist=tasklist_id, task=remote_id).execute()
            trace.append(
                {
                    "action": "google_api.tasks.delete",
                    "provider": "google_api",
                    "request": {
                        "tasklist": tasklist_id,
                        "task": remote_id,
                    },
                    "replay_cmd": _google_tasks_replay_cmd(
                        action="delete",
                        tasklist_id=tasklist_id,
                        task_id=remote_id,
                    ),
                    "stdout": "",
                    "stderr": "",
                    "exit_code": 0,
                }
            )
            return True, "", trace, meta

        return False, f"Unsupported tasks action: {action}", trace, meta
    except Exception as exc:
        return False, str(exc), trace, meta


def _google_tasks_replay_cmd(
    *,
    action: str,
    tasklist_id: str,
    task_id: str | None = None,
    request_params: dict[str, Any] | None = None,
) -> str:
    payload: dict[str, Any] = {
        "action": action,
        "tasklist": tasklist_id,
    }
    if task_id:
        payload["task"] = task_id
    if request_params:
        payload["params"] = request_params
    compact = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f"python -m openclaw_env.skills.impl.tasks_skill --replay '{compact}'"


def _to_google_due(value: Any) -> str | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        if "T" in raw:
            parsed = dt.datetime.fromisoformat(raw)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
        parsed_date = dt.date.fromisoformat(raw)
        return dt.datetime.combine(parsed_date, dt.time(0, 0), tzinfo=dt.timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )
    except ValueError:
        return None
