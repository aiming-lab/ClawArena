"""I/O helpers — load tests.json and questions.json."""

from __future__ import annotations

import json
from pathlib import Path

_OVERLAY_ALLOWED_KEYS = frozenset({"metaclaw", "mm_metaclaw"})


def load_json(path: Path) -> dict:
    """Load and parse a JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def load_tests_config(tests_json_path: Path) -> dict:
    """Load tests.json and validate minimal structure."""
    cfg = load_json(tests_json_path)
    if "frameworks" not in cfg:
        raise ValueError(f"tests.json missing 'frameworks': {tests_json_path}")
    if "tests" not in cfg:
        raise ValueError(f"tests.json missing 'tests': {tests_json_path}")
    return cfg


def load_questions(eval_dir: Path, eval_name: str) -> dict:
    """Load questions.json for a given eval scenario.

    Returns dict with 'rounds' key.
    """
    path = eval_dir / eval_name / "questions.json"
    if not path.exists():
        return {"rounds": []}
    data = load_json(path)
    if "rounds" not in data:
        raise ValueError(f"questions.json missing 'rounds': {path}")
    return data


def apply_overlay(tests_cfg: dict, overlay_json: str | None) -> dict:
    """Shallow-merge a JSON string into the metaclaw section."""
    if not overlay_json:
        return tests_cfg
    try:
        patch = json.loads(overlay_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"--overlay: invalid JSON — {exc}") from exc
    if not isinstance(patch, dict):
        raise ValueError("--overlay: top-level value must be a JSON object")
    unknown = set(patch) - _OVERLAY_ALLOWED_KEYS
    if unknown:
        raise ValueError(
            f"--overlay: only {sorted(_OVERLAY_ALLOWED_KEYS)} keys are allowed; "
            f"got: {sorted(unknown)}"
        )

    result = dict(tests_cfg)
    for key in _OVERLAY_ALLOWED_KEYS:
        if key in patch:
            base = dict(result.get(key) or {})
            base.update(patch[key])
            result[key] = base
    return result


def write_json(path: Path, data: dict) -> None:
    """Write dict as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
