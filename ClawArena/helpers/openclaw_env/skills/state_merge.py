"""Helpers to normalize and merge backend/skill state for evaluation."""

from __future__ import annotations

from typing import Any


def as_named_mapping(raw: Any) -> dict[str, Any]:
    """Normalize backend entity containers to ``{name: payload}`` mappings."""
    if isinstance(raw, dict):
        out: dict[str, Any] = {}
        for key, value in raw.items():
            if isinstance(value, dict):
                name = value.get("name") or value.get("id") or key
                if isinstance(name, str) and name:
                    out[name] = dict(value)
                continue
            if isinstance(value, list):
                for item in value:
                    if not isinstance(item, dict):
                        continue
                    name = item.get("name") or item.get("id") or key
                    if isinstance(name, str) and name:
                        out[name] = dict(item)
        if out:
            return out
        return dict(raw)
    if isinstance(raw, list):
        out: dict[str, Any] = {}
        for item in raw:
            if not isinstance(item, dict):
                continue
            name = item.get("name") or item.get("id")
            if isinstance(name, str) and name:
                out[name] = dict(item)
        return out
    return {}


def merge_named_entities(dst: dict[str, Any], entries: Any) -> None:
    """Merge effect entries that carry a ``name`` field into ``dst``."""
    if not isinstance(entries, list):
        return
    for item in entries:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name:
            continue
        current = dst.get(name)
        if isinstance(current, dict):
            merged = dict(current)
            merged.update(item)
            dst[name] = merged
        else:
            dst[name] = dict(item)


def merge_backend_state_into_eval(
    state: dict[str, Any],
    effects: dict[str, list[dict[str, Any]]],
    backend_state: dict[str, Any],
) -> None:
    """Apply backend state to evaluator-visible state.

    Backend state represents the current world snapshot, including resources loaded
    from an initial config. Evaluation effects must remain episode-local deltas,
    so this helper must not backfill `*_created` effect lists from the snapshot.
    """
    state.update(backend_state)

    calendar_events = _as_list(backend_state.get("calendar_events"))
    emails = _as_list(backend_state.get("emails"))
    tasks_list = _as_list(backend_state.get("tasks"))
    messages = _as_list(backend_state.get("messages"))
    cron_jobs = _as_list(backend_state.get("cron_jobs"))
    plugins = _as_list(backend_state.get("plugins"))
    files_raw = backend_state.get("files")

    if "calendar_events" in backend_state:
        state["calendar_events"] = calendar_events
    if "emails" in backend_state:
        state["emails"] = emails
    if "tasks" in backend_state:
        state["tasks_list"] = tasks_list
    if "messages" in backend_state:
        state["messages"] = messages
    if "cron_jobs" in backend_state:
        state["cron_jobs"] = cron_jobs
    if "plugins" in backend_state:
        state["plugins"] = plugins

    if isinstance(files_raw, dict):
        state["files"] = dict(files_raw)
    elif isinstance(files_raw, list):
        state["files"] = list(files_raw)

    agents = as_named_mapping(backend_state.get("agents"))
    channels = as_named_mapping(backend_state.get("channels"))
    if agents:
        state["agents"] = agents
    if channels:
        state["channels"] = channels


def _as_list(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []
