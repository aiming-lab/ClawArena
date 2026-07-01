"""Data validation — check command implementation."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.adapters.registry import get_adapter
from clawarena.core.io import load_json, load_tests_config
from clawarena.core.provider import VALID_PROVIDERS
from clawarena.qtypes.registry import get_qtype, registered_types


def run_check(
    tests_json_path: Path,
    frameworks: list[str] | None = None,
    test_ids: list[str] | None = None,
    strict: bool = False,
) -> bool:
    """Validate data integrity. Returns True if passed."""
    base_dir = tests_json_path.parent
    errors: list[str] = []
    warnings: list[str] = []

    # G-001: tests.json exists and valid
    try:
        tests_cfg = load_tests_config(tests_json_path)
    except Exception as e:
        print(f"[FAIL] G-001: {e}")
        return False

    # G-003: frameworks non-empty
    fw_cfg = tests_cfg.get("frameworks", {})
    if not fw_cfg:
        errors.append("G-003: tests.json.frameworks is empty")

    # G-004: manifest paths exist
    target_fws = frameworks or list(fw_cfg.keys())

    # G-002: eval_dir exists (only required when at least one framework uses it)
    eval_dir = base_dir / tests_cfg.get("eval_dir", "eval")
    _eval_dir_needed = _any_framework_uses_eval_dir(base_dir, fw_cfg, target_fws)
    if not eval_dir.exists():
        if _eval_dir_needed:
            errors.append(f"G-002: eval_dir not found: {eval_dir}")
        else:
            warnings.append(f"G-002: eval_dir not found: {eval_dir} (skipped — no framework requires it)")
    for fw in target_fws:
        if fw not in fw_cfg:
            errors.append(f"G-004: framework '{fw}' not in tests.json")
            continue
        manifest_rel = fw_cfg[fw].get("manifest", "")
        manifest_path = base_dir / manifest_rel
        if not manifest_path.exists():
            errors.append(f"G-004: manifest not found: {manifest_path}")

    # G-005: tests non-empty
    tests = tests_cfg.get("tests", [])
    if not tests:
        errors.append("G-005: tests.json.tests is empty")

    # G-007: model field validation
    _validate_model_field(tests_cfg, errors, warnings)

    # G-008: metaclaw field validation
    _validate_metaclaw_field(tests_cfg, base_dir, errors, warnings)

    # G-006: per-test validation (only for frameworks that use eval/)
    target_tests = [t for t in tests if not test_ids or t["id"] in test_ids]
    workspace_map = _build_workspace_map(base_dir, fw_cfg, target_fws)
    if _eval_dir_needed:
        for test in target_tests:
            _validate_test_entry(test, eval_dir, errors, warnings, workspace_map)

    # Framework-specific validation
    for fw in target_fws:
        if fw not in fw_cfg:
            continue
        manifest_rel = fw_cfg[fw].get("manifest", "")
        manifest_path = base_dir / manifest_rel
        if not manifest_path.exists():
            continue
        try:
            adapter = get_adapter(fw)
            manifest = adapter.data_handler.load_manifest(manifest_path)
            fw_errors = adapter.data_handler.validate(
                manifest, manifest_path.parent, eval_dir, target_tests,
            )
            errors.extend(f"[{fw}] {e}" for e in fw_errors)
        except ValueError:
            warnings.append(f"Framework '{fw}' not yet implemented, skipping validation")

    # Report
    for e in errors:
        print(f"  [ERROR] {e}")
    for w in warnings:
        print(f"  [WARN]  {w}")

    passed = len(errors) == 0 and (not strict or len(warnings) == 0)
    status = "PASS" if passed else "FAIL"
    print(f"\nCheck {status}: {len(errors)} errors, {len(warnings)} warnings")
    return passed


def _build_workspace_map(
    base_dir: Path, fw_cfg: dict, target_fws: list[str],
) -> dict[str, Path]:
    """Best-effort: load manifests to build a test_id → workspace_path mapping.

    Used to pass static workspace paths to validate_round so exec_check can
    optionally warn about missing workspace files (OMIT_WORKSPACE=0).
    Failures are silently ignored — the workspace map is only advisory.
    """
    workspace_map: dict[str, Path] = {}
    for fw in target_fws:
        if fw not in fw_cfg:
            continue
        manifest_rel = fw_cfg[fw].get("manifest", "")
        manifest_path = base_dir / manifest_rel
        if not manifest_path.exists():
            continue
        try:
            adapter = get_adapter(fw)
            manifest = adapter.data_handler.load_manifest(manifest_path)
            for tid, info in manifest.get("agents", {}).items():
                ws_rel = info.get("workspace")
                if ws_rel and tid not in workspace_map:
                    ws = manifest_path.parent / ws_rel
                    if ws.exists():
                        workspace_map[tid] = ws
        except Exception:
            pass
    return workspace_map


def _validate_test_entry(
    test: dict, eval_dir: Path, errors: list[str], warnings: list[str],
    workspace_map: dict[str, Path] | None = None,
) -> None:
    """Validate a single test entry (G-006)."""
    test_id = test.get("id", "")
    if not test_id:
        errors.append("G-006a: test entry missing 'id'")
        return

    eval_name = test.get("eval", "")
    if not eval_name:
        errors.append(f"G-006b: test '{test_id}' missing 'eval'")
        return

    if test_id != eval_name:
        warnings.append(f"G-006c: test '{test_id}': id != eval ('{eval_name}')")

    # G-006d-h: questions.json
    q_path = eval_dir / eval_name / "questions.json"
    if not q_path.exists():
        errors.append(f"G-006d: {test_id}: questions.json not found")
        return

    try:
        q_data = load_json(q_path)
    except Exception:
        errors.append(f"G-006d: {test_id}: questions.json not valid JSON")
        return

    rounds = q_data.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        errors.append(f"G-006e: {test_id}: questions.json 'rounds' missing or empty")
        return

    known_types = set(registered_types())
    for rnd in rounds:
        rid = rnd.get("id")
        if not rid:
            errors.append(f"G-006f: {test_id}: round missing 'id'")
        if "question" not in rnd:
            errors.append(f"G-006f: {test_id}/{rid}: missing 'question'")
        rtype = rnd.get("type", "multi_choice")
        if rtype not in known_types:
            errors.append(f"G-006g: {test_id}/{rid}: unknown type '{rtype}'")
        else:
            try:
                qtype = get_qtype(rtype)
                workspace = (workspace_map or {}).get(test_id)
                errs, warns = qtype.validate_round(rnd, test_id, eval_dir, workspace)
                errors.extend(errs)
                warnings.extend(warns)
            except Exception:
                pass
        update_ids = rnd.get("update_ids")
        if update_ids is not None and not isinstance(update_ids, list):
            errors.append(f"G-006h: {test_id}/{rid}: update_ids must be a list")

    # G-006i: each update_id must appear at most once across all rounds
    uid_rounds: dict[str, list[str]] = {}
    for rnd in rounds:
        rid = rnd.get("id", "?")
        for uid in rnd.get("update_ids") or []:
            if isinstance(uid, str):
                uid_rounds.setdefault(uid, []).append(rid)
    for uid, rids in uid_rounds.items():
        if len(rids) > 1:
            rounds_str = ", ".join(f"'{r}'" for r in rids)
            errors.append(
                f"G-006i: {test_id}: update_id '{uid}' appears in {len(rids)} rounds: {rounds_str}"
            )


def _any_framework_uses_eval_dir(
    base_dir: Path, fw_cfg: dict, target_fws: list[str],
) -> bool:
    """Return True if any of the target frameworks requires the eval/ directory."""
    for fw in target_fws:
        if fw not in fw_cfg:
            continue
        try:
            adapter = get_adapter(fw)
            if adapter.data_handler.uses_eval_dir():
                return True
        except Exception:
            return True  # unknown framework → assume it needs eval/
    return False


def _validate_model_field(
    tests_cfg: dict, errors: list[str], warnings: list[str],
) -> None:
    """G-007: Validate top-level and framework-level model fields."""
    def _check_model(model_raw: dict, label: str) -> None:
        if not isinstance(model_raw, dict):
            errors.append(f"G-007: {label}: model must be a dict")
            return
        provider = model_raw.get("provider", "openai")
        if isinstance(provider, str) and not provider.startswith("${"):
            if provider not in VALID_PROVIDERS:
                errors.append(
                    f"G-007: {label}: unknown provider '{provider}' "
                    f"(valid: {', '.join(sorted(VALID_PROVIDERS))})"
                )
        api_key = model_raw.get("api_key")
        if api_key and isinstance(api_key, str) and not api_key.startswith("${"):
            warnings.append(f"G-007: {label}: api_key is plaintext — use ${{ENV_VAR}}")

    top_model = tests_cfg.get("model")
    if top_model:
        _check_model(top_model, "top-level")

    for fw, fw_cfg in tests_cfg.get("frameworks", {}).items():
        fw_model = fw_cfg.get("model")
        if fw_model:
            _check_model(fw_model, f"frameworks.{fw}")


def _validate_metaclaw_field(
    tests_cfg: dict, base_dir: Path, errors: list[str], warnings: list[str],
) -> None:
    """G-008: Validate metaclaw section in tests.json."""
    mc = tests_cfg.get("metaclaw")
    if not mc:
        return
    if not isinstance(mc, dict):
        errors.append("G-008: metaclaw must be a dict")
        return
    if mc.get("enabled"):
        is_managed = mc.get("managed", True)
        config_path = mc.get("config_path", "")
        if not config_path and is_managed:
            errors.append("G-008: metaclaw.enabled=true (managed) but config_path missing")
        elif config_path:
            full = base_dir / config_path
            if not full.exists():
                errors.append(f"G-008: metaclaw config_path not found: {full}")
        for key in ("memory_trigger", "rl_trigger"):
            trigger = mc.get(key, {})
            if trigger and not isinstance(trigger, dict):
                errors.append(f"G-008: metaclaw.{key} must be a dict")
