"""Helpers for resolving per-round update references."""

from __future__ import annotations

import re
from collections.abc import Iterable

_SHORTHAND_RE = re.compile(r"^(?:[Uu]|upd)?(\d+)$")


def resolve_update_entries(
    test_updates: dict[str, dict],
    update_ref: str | int,
) -> list[tuple[str, dict]]:
    """Resolve a round-level update reference to concrete manifest entries.

    Benchmark questions may refer to updates in either of two forms:

    1. Direct manifest keys such as ``upd1_workspace``.
    2. Shorthand references such as ``1``, ``"2"``, ``"U1"``, or ``"upd3"``,
       which should expand to all matching concrete updates (for example both
       ``upd2_sessions`` and ``upd2_workspace``) in manifest order.
    """
    if not test_updates:
        return []

    if update_ref in test_updates:
        key = str(update_ref)
        return _expand_update_entry(test_updates, key)

    ref = str(update_ref).strip()
    if not ref:
        return []
    if ref in test_updates:
        return _expand_update_entry(test_updates, ref)

    match = _SHORTHAND_RE.fullmatch(ref)
    if not match:
        return []

    prefix = f"upd{int(match.group(1))}"
    matches: list[tuple[str, dict]] = []
    for key, meta in test_updates.items():
        if key == prefix or key.startswith(f"{prefix}_"):
            matches.extend(_expand_update_entry(test_updates, key))
    return matches


def iter_resolved_update_keys(
    test_updates: dict[str, dict],
    update_ids: Iterable[str | int],
) -> list[str]:
    """Resolve update refs and return unique concrete keys in manifest order."""
    seen: set[str] = set()
    resolved: list[str] = []
    for update_ref in update_ids:
        for key, _meta in resolve_update_entries(test_updates, update_ref):
            if key in seen:
                continue
            seen.add(key)
            resolved.append(key)
    return resolved


def _expand_update_entry(
    test_updates: dict[str, dict],
    key: str,
    *,
    _stack: tuple[str, ...] = (),
) -> list[tuple[str, dict]]:
    """Expand nested group updates into concrete leaf updates."""
    if key not in test_updates:
        return []
    if key in _stack:
        return []

    meta = test_updates[key]
    if meta.get("type") != "group":
        return [(key, meta)]

    expanded: list[tuple[str, dict]] = []
    for child in meta.get("children", []):
        expanded.extend(
            _expand_update_entry(
                test_updates, str(child), _stack=_stack + (key,),
            )
        )
    return expanded
