"""Dataset loading and validation.

Convention: all paths in the persisted JSON files are relative to the file in
which they appear; at load time they are uniformly resolved to absolute paths on
the local machine. tests.json may contain extra fields (used for custom subsets
and notes). Extra fields in the other files are treated as errors.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..provider import ProviderError
from ..types import (
    DatasetManifests,
    EvalSpec,
    Feedback,
    Round,
    ScenarioManifest,
    TestsConfig,
    UpdateFile,
    UpdateGroup,
)

REQUIRED_TESTS_KEYS = {"name", "manifests_ref", "scenario_ids"}
REQUIRED_MANIFESTS_KEYS = {"scenarios"}
REQUIRED_SCENARIO_KEYS = {
    "scenario_id",
    "workspace_template",
    "scripts",
    "main_agent_accessible_paths",
    "updates",
    "rounds_ref",
}
# Fix (fix/audit-top10 #10 / W3 NEW-1): previously update_ids was OPTIONAL in the
# validator but REQUIRED in dataset, so a questions.json could "pass check yet crash
# run". Unified to optional; the loader falls back to an empty list when missing
# (see list(r.get("update_ids") or []) below, already compatible).
REQUIRED_ROUND_KEYS = {"id", "type", "question", "eval", "feedback"}
OPTIONAL_ROUND_KEYS = {"update_ids"}


class DatasetError(ValueError):
    """Dataset validation failed."""


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


# ---------------------------------------------------------------------------
# Single-file loaders
# ---------------------------------------------------------------------------


def _read_json(path: Path) -> Any:
    if not path.exists():
        raise DatasetError(f"missing file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_rel(base_file: Path, rel: str) -> Path:
    return (base_file.parent / rel).resolve(strict=False)


def load_tests(tests_path: Path) -> TestsConfig:
    data = _read_json(tests_path)
    missing = REQUIRED_TESTS_KEYS - set(data.keys())
    if missing:
        raise DatasetError(f"tests.json missing keys: {missing}")
    return TestsConfig(
        tests_path=tests_path.resolve(),
        name=data["name"],
        desc=data.get("desc", ""),
        manifests_ref=_resolve_rel(tests_path, data["manifests_ref"]),
        scenario_ids=list(data["scenario_ids"]),
        extras={k: v for k, v in data.items() if k not in REQUIRED_TESTS_KEYS | {"desc"}},
    )


def load_manifests(manifests_path: Path) -> DatasetManifests:
    data = _read_json(manifests_path)
    missing = REQUIRED_MANIFESTS_KEYS - set(data.keys())
    if missing:
        raise DatasetError(f"manifests.json missing keys: {missing}")
    extras = set(data.keys()) - REQUIRED_MANIFESTS_KEYS
    if extras:
        raise DatasetError(f"manifests.json has unexpected keys: {extras}")
    scenarios = {sid: _resolve_rel(manifests_path, rel) for sid, rel in data["scenarios"].items()}
    return DatasetManifests(manifests_path=manifests_path.resolve(), scenarios=scenarios)


def load_scenario(manifest_path: Path) -> ScenarioManifest:
    data = _read_json(manifest_path)
    missing = REQUIRED_SCENARIO_KEYS - set(data.keys())
    if missing:
        raise DatasetError(f"{manifest_path}: missing keys {missing}")
    extras = set(data.keys()) - REQUIRED_SCENARIO_KEYS - {"desc", "main_agent_delegable_paths"}
    if extras:
        raise DatasetError(f"{manifest_path}: unexpected keys {extras}")
    scenario_dir = manifest_path.parent.resolve()
    workspace_template = _resolve_rel(manifest_path, data["workspace_template"])
    scripts_dir = _resolve_rel(manifest_path, data["scripts"])
    updates: dict[str, UpdateGroup] = {}
    for uid, spec in data["updates"].items():
        files = [
            UpdateFile(src=_resolve_rel(manifest_path, f["src"]), dst_rel=f["dst"])
            for f in spec["files"]
        ]
        updates[uid] = UpdateGroup(update_id=uid, op=spec["op"], files=files)
    rounds_path = _resolve_rel(manifest_path, data["rounds_ref"])
    rounds_raw = _read_json(rounds_path)
    if not isinstance(rounds_raw, list):
        raise DatasetError(f"{rounds_path}: top-level must be a list")
    rounds: list[Round] = []
    for r in rounds_raw:
        missing_r = REQUIRED_ROUND_KEYS - set(r.keys())
        if missing_r:
            raise DatasetError(f"{rounds_path}: round missing keys {missing_r}")
        ev = r["eval"]
        rounds.append(
            Round(
                id=r["id"],
                type=r["type"],
                update_ids=list(r.get("update_ids") or []),
                question=r["question"],
                eval=EvalSpec(
                    command=ev["command"],
                    expect_exit=int(ev.get("expect_exit", 0)),
                    timeout=int(ev.get("timeout", 60)),
                    expect_stdout=ev.get("expect_stdout"),
                    expect_stdout_regex=bool(ev.get("expect_stdout_regex", False)),
                ),
                feedback=Feedback(
                    correct=(r["feedback"].get("correct") or ""),
                    incorrect=(r["feedback"].get("incorrect") or ""),
                ),
                tags=[t for t in (r.get("tags") or []) if isinstance(t, str)],
            )
        )
    return ScenarioManifest(
        scenario_id=data["scenario_id"],
        desc=data.get("desc", ""),
        scenario_dir=scenario_dir,
        workspace_template=workspace_template,
        scripts_dir=scripts_dir,
        main_agent_accessible_paths=list(data["main_agent_accessible_paths"]),
        main_agent_delegable_paths=list(data.get("main_agent_delegable_paths") or []),
        updates=updates,
        rounds=rounds,
    )


# ---------------------------------------------------------------------------
# Dataset-level API
# ---------------------------------------------------------------------------


def load_dataset(
    data_dir: Path, tests_filename: str = "tests.json"
) -> tuple[TestsConfig, DatasetManifests, dict[str, ScenarioManifest]]:
    """Load a dataset. ``tests_filename`` selects which tests file to read (defaults
    to the full ``tests.json`` set); the merged dataset ``clawarena-team`` also
    contains ``tests-<wave>.json`` subsets, which can be selected via this parameter
    to run only a given wave.
    """
    tests = load_tests(data_dir / tests_filename)
    manifests = load_manifests(tests.manifests_ref)
    scenarios: dict[str, ScenarioManifest] = {}
    for sid in tests.scenario_ids:
        if sid not in manifests.scenarios:
            raise DatasetError(
                f"{tests_filename} references unknown scenario_id {sid}"
            )
        scenarios[sid] = load_scenario(manifests.scenarios[sid])
    return tests, manifests, scenarios


def validate_dataset(data_dir: Path) -> "ValidationReport":
    """Deep validation (schema + path + update virtual-FS simulation).

    The implementation lives in ``validator.py``; this function only adapts the
    ``ValidationReport`` type to avoid changing the public API.
    """
    from .validator import validate_dataset_strict, ValidationReport as _StrictReport

    strict = validate_dataset_strict(data_dir)
    report = ValidationReport()
    report.errors.extend(strict.errors)
    report.warnings.extend(strict.warnings)
    return report
