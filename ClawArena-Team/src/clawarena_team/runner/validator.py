"""Deep dataset validation (``clawarena-team check``).

Design goal: **any tests.json that passes this validation must run under
``clawarena-team run`` without failing due to data structure, missing paths, or
update-sequence conflicts**.

Validation layers (stop-on-error or accumulate):

1. **Field strictness**: every JSON file is checked against a whitelist.
   - missing required field → error;
   - missing optional field → warning (falls back to a default at runtime);
   - unknown field → error (**tests.json is the only exception**, which allows
     custom metadata).
2. **Type checks**: ``timeout`` must be a positive number; ``expect_exit`` must be
   an integer; ``main_agent_accessible_paths`` must be a list of strings;
   ``update_ids`` must be a list of strings; etc.
3. **Relative-path existence**: ``manifests_ref`` / each scenario ``manifest.json`` /
   ``workspace_template`` / ``scripts`` / ``rounds_ref`` /
   ``updates[*].files[*].src`` must all physically exist; ``scripts`` must be a
   directory.
4. **Intra-scenario consistency**: ``scenario_id`` matches the directory name;
   ``accessible_paths`` fall within workspace_template; every id in
   ``round.update_ids`` is in the ``updates`` dict; each update_id appears at most
   once across rounds (to avoid conflicts from repeated apply).
5. **Update virtual-FS simulation**: starting from the workspace_template file
   listing, apply updates in round order:
   - ``new``: dst must **not exist** in the current FS view;
   - ``replace``: dst must **already exist** in the current FS view (whether from
     the template or a previous update).
   Any conflict raises an error.
6. **``eval.command`` placeholder resolution**:
   - for ``type == "exec_check"`` rounds, ``command`` must contain at least one
     ``${scripts}/...`` reference (forcing the use of external scripts; inline
     shell validation logic is not allowed);
   - each ``${scripts}/<rel>`` reference is resolved under the ``scripts`` directory
     and the physical file must exist;
   - if a ``${workspace}/<rel>`` reference is not present in workspace_template, a
     warning is emitted (the agent may create it during run; not enforced);
   - if a placeholder outside the known set (workspace/scripts/scenario_dir/
     scenario_id) appears and does not look like a shell variable (e.g. ``${HOME}``),
     a warning is emitted to flag the naming.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Schema definitions
# ---------------------------------------------------------------------------

TESTS_REQUIRED = {"name", "manifests_ref", "scenario_ids"}
TESTS_OPTIONAL = {"desc"}

MANIFESTS_REQUIRED = {"scenarios"}
MANIFESTS_OPTIONAL: set[str] = set()

SCENARIO_REQUIRED = {
    "scenario_id",
    "workspace_template",
    "scripts",
    "main_agent_accessible_paths",
    "updates",
    "rounds_ref",
}
SCENARIO_OPTIONAL = {"desc", "main_agent_delegable_paths"}

UPDATE_GROUP_REQUIRED = {"op", "files"}
UPDATE_GROUP_OPTIONAL: set[str] = set()

UPDATE_FILE_REQUIRED = {"src", "dst"}
UPDATE_FILE_OPTIONAL: set[str] = set()

ROUND_REQUIRED = {"id", "type", "question", "eval", "feedback"}
ROUND_OPTIONAL = {"update_ids"}
# Pure-metadata optional field: no warning if missing, but if present its type must
# still be list[str].
ROUND_QUIET_OPTIONAL = {"tags"}

EVAL_REQUIRED = {"command"}
EVAL_OPTIONAL = {"expect_exit", "timeout", "expect_stdout", "expect_stdout_regex"}

FEEDBACK_REQUIRED: set[str] = set()
FEEDBACK_OPTIONAL = {"correct", "incorrect"}

KNOWN_ROUND_TYPES = {"exec_check"}
KNOWN_UPDATE_OPS = {"new", "replace"}
KNOWN_PLACEHOLDERS = {"workspace", "scripts", "scenario_dir", "scenario_id"}

# ${scripts}/some/path —— stops at shell metacharacters
SCRIPTS_PATH_RE = re.compile(r"\$\{scripts\}[^\s'\"`;&|><()\$]*")
WORKSPACE_PATH_RE = re.compile(r"\$\{workspace\}[^\s'\"`;&|><()\$]*")
ANY_PLACEHOLDER_RE = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Shell-style uppercase variables (e.g. ${HOME}) are kept without warning, so
# commands can use real environment variables
_SHELL_LIKE = re.compile(r"^[A-Z][A-Z0-9_]*$")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_json(path: Path, ctx: str, errors: list[str]) -> Any | None:
    if not path.exists():
        errors.append(f"{ctx}: file not found: {path}")
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{ctx}: not valid JSON ({e})")
        return None


def _check_keys(
    data: Any,
    required: set[str],
    optional: set[str],
    *,
    allow_extra: bool,
    ctx: str,
    errors: list[str],
    warnings: list[str],
    quiet_optional: set[str] | None = None,
) -> bool:
    """quiet_optional: fields that are valid but produce no warning when missing
    (used for pure-metadata optional fields, e.g. round.tags). Type checking when
    present is still the caller's responsibility."""
    quiet_optional = quiet_optional or set()
    if not isinstance(data, dict):
        errors.append(f"{ctx}: must be a JSON object, got {type(data).__name__}")
        return False
    keys = set(data.keys())
    miss_req = required - keys
    if miss_req:
        errors.append(f"{ctx}: missing required keys {sorted(miss_req)}")
    miss_opt = optional - keys
    for o in sorted(miss_opt):
        warnings.append(f"{ctx}: optional key '{o}' missing (will fall back to default)")
    if not allow_extra:
        extras = keys - required - optional - quiet_optional
        if extras:
            errors.append(f"{ctx}: unexpected keys {sorted(extras)}")
    return not miss_req


def _is_str_list(v: Any) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def _resolve_rel(base_file: Path, rel: str) -> Path:
    return (base_file.parent / rel).resolve(strict=False)


def _enumerate_files_rel(root: Path) -> set[str]:
    """Enumerate all files under root, returning a set of relative paths (posix
    style, without a trailing ``/``)."""
    out: set[str] = set()
    if not root.exists() or not root.is_dir():
        return out
    for p in root.rglob("*"):
        if p.is_file():
            out.add(p.relative_to(root).as_posix())
    return out


def _enumerate_src_rel(src: Path) -> set[str]:
    """Enumerate the relative paths of files under src (which may be a file or a
    directory).

    - src is a file: returns a single-element set (empty string); the caller must
      prepend dst to the prefix itself;
    - src is a directory: returns the posix paths of all files under src.rglob,
      relative to src.
    """
    if src.is_file():
        return {""}  # single-file marker
    out: set[str] = set()
    if src.is_dir():
        for p in src.rglob("*"):
            if p.is_file():
                out.add(p.relative_to(src).as_posix())
    return out


def _join_rel(dst_rel: str, sub: str) -> str:
    dst_rel = dst_rel.lstrip("/").rstrip("/")
    if not sub:
        return dst_rel
    return f"{dst_rel}/{sub}"


def _has_prefix(view: set[str], prefix: str) -> bool:
    """Whether view contains a path == prefix or a path under prefix/."""
    if prefix in view:
        return True
    p = prefix.rstrip("/") + "/"
    return any(x.startswith(p) for x in view)


def _remove_prefix(view: set[str], prefix: str) -> None:
    """Remove from view the prefix itself and all paths under prefix/."""
    p = prefix.rstrip("/") + "/"
    to_drop = {x for x in view if x == prefix or x.startswith(p)}
    view.difference_update(to_drop)


# ---------------------------------------------------------------------------
# Per-file schema validators
# ---------------------------------------------------------------------------


def _validate_tests_schema(
    data: Any, tests_path: Path, errors: list[str], warnings: list[str]
) -> bool:
    """tests.json: allows custom extra fields."""
    ctx = f"{tests_path.name}"
    if not _check_keys(
        data, TESTS_REQUIRED, TESTS_OPTIONAL,
        allow_extra=True, ctx=ctx, errors=errors, warnings=warnings,
    ):
        return False
    if not isinstance(data.get("name"), str) or not data["name"]:
        errors.append(f"{ctx}: 'name' must be a non-empty string")
    if not isinstance(data.get("manifests_ref"), str) or not data["manifests_ref"]:
        errors.append(f"{ctx}: 'manifests_ref' must be a non-empty string")
    if not _is_str_list(data.get("scenario_ids")):
        errors.append(f"{ctx}: 'scenario_ids' must be a list of strings")
    elif not data["scenario_ids"]:
        errors.append(f"{ctx}: 'scenario_ids' is empty")
    return True


def _validate_manifests_schema(
    data: Any, manifests_path: Path, errors: list[str], warnings: list[str]
) -> bool:
    ctx = f"{manifests_path.name}"
    if not _check_keys(
        data, MANIFESTS_REQUIRED, MANIFESTS_OPTIONAL,
        allow_extra=False, ctx=ctx, errors=errors, warnings=warnings,
    ):
        return False
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, dict) or not scenarios:
        errors.append(f"{ctx}: 'scenarios' must be a non-empty dict")
        return False
    for sid, rel in scenarios.items():
        if not isinstance(sid, str) or not sid:
            errors.append(f"{ctx}: scenario id must be non-empty string, got {sid!r}")
        if not isinstance(rel, str) or not rel:
            errors.append(f"{ctx}: scenario '{sid}' path must be non-empty string")
    return True


def _validate_eval_schema(
    eval_obj: Any, ctx: str, errors: list[str], warnings: list[str]
) -> None:
    if not _check_keys(
        eval_obj, EVAL_REQUIRED, EVAL_OPTIONAL,
        allow_extra=False, ctx=ctx, errors=errors, warnings=warnings,
    ):
        return
    cmd = eval_obj.get("command")
    if not isinstance(cmd, str) or not cmd.strip():
        errors.append(f"{ctx}: 'command' must be a non-empty string")
    # Fix (fix/audit-top10 W3 NEW-2): bool is a subclass of int; the original check
    # let True/False through, then the loader's int() coerced them to 1/0, silently
    # changing the scoring criterion to "expected exit code 1". Aligned with the
    # timeout check.
    if "expect_exit" in eval_obj and (
        not isinstance(eval_obj["expect_exit"], int) or isinstance(eval_obj["expect_exit"], bool)
    ):
        errors.append(f"{ctx}: 'expect_exit' must be an integer (bool not accepted)")
    if "timeout" in eval_obj:
        to = eval_obj["timeout"]
        if not isinstance(to, (int, float)) or isinstance(to, bool) or to <= 0:
            errors.append(f"{ctx}: 'timeout' must be a positive number")
    if "expect_stdout" in eval_obj:
        es = eval_obj["expect_stdout"]
        if es is not None and not isinstance(es, str):
            errors.append(f"{ctx}: 'expect_stdout' must be string or null")
    if "expect_stdout_regex" in eval_obj and not isinstance(
        eval_obj["expect_stdout_regex"], bool
    ):
        errors.append(f"{ctx}: 'expect_stdout_regex' must be a boolean")


def _validate_feedback_schema(
    fb_obj: Any, ctx: str, errors: list[str], warnings: list[str]
) -> None:
    if not _check_keys(
        fb_obj, FEEDBACK_REQUIRED, FEEDBACK_OPTIONAL,
        allow_extra=False, ctx=ctx, errors=errors, warnings=warnings,
    ):
        return
    for k in ("correct", "incorrect"):
        if k in fb_obj and not isinstance(fb_obj[k], str):
            errors.append(f"{ctx}: feedback.{k} must be string")


def _validate_update_file_schema(
    f_obj: Any, ctx: str, errors: list[str], warnings: list[str]
) -> None:
    if not _check_keys(
        f_obj, UPDATE_FILE_REQUIRED, UPDATE_FILE_OPTIONAL,
        allow_extra=False, ctx=ctx, errors=errors, warnings=warnings,
    ):
        return
    if not isinstance(f_obj.get("src"), str) or not f_obj["src"]:
        errors.append(f"{ctx}: 'src' must be non-empty string")
    if not isinstance(f_obj.get("dst"), str) or not f_obj["dst"]:
        errors.append(f"{ctx}: 'dst' must be non-empty string")


def _validate_update_group_schema(
    ug_obj: Any, ctx: str, errors: list[str], warnings: list[str]
) -> None:
    if not _check_keys(
        ug_obj, UPDATE_GROUP_REQUIRED, UPDATE_GROUP_OPTIONAL,
        allow_extra=False, ctx=ctx, errors=errors, warnings=warnings,
    ):
        return
    op = ug_obj.get("op")
    if op not in KNOWN_UPDATE_OPS:
        errors.append(f"{ctx}: unknown op '{op}'; allowed {sorted(KNOWN_UPDATE_OPS)}")
    files = ug_obj.get("files")
    if not isinstance(files, list) or not files:
        errors.append(f"{ctx}: 'files' must be a non-empty list")
        return
    for i, f in enumerate(files):
        _validate_update_file_schema(f, f"{ctx}.files[{i}]", errors, warnings)


def _validate_round_schema(
    rnd_obj: Any, ctx: str, errors: list[str], warnings: list[str]
) -> None:
    if not _check_keys(
        rnd_obj, ROUND_REQUIRED, ROUND_OPTIONAL,
        allow_extra=False, ctx=ctx, errors=errors, warnings=warnings,
        quiet_optional=ROUND_QUIET_OPTIONAL,
    ):
        return
    if not isinstance(rnd_obj.get("id"), str) or not rnd_obj["id"]:
        errors.append(f"{ctx}: 'id' must be non-empty string")
    rtype = rnd_obj.get("type")
    if rtype not in KNOWN_ROUND_TYPES:
        errors.append(f"{ctx}: unknown type '{rtype}'; allowed {sorted(KNOWN_ROUND_TYPES)}")
    if not isinstance(rnd_obj.get("question"), str) or not rnd_obj["question"]:
        errors.append(f"{ctx}: 'question' must be non-empty string")
    if "update_ids" in rnd_obj and not _is_str_list(rnd_obj["update_ids"]):
        errors.append(f"{ctx}: 'update_ids' must be a list of strings")
    if "tags" in rnd_obj and not _is_str_list(rnd_obj["tags"]):
        errors.append(f"{ctx}: 'tags' must be a list of strings")
    if "eval" in rnd_obj:
        _validate_eval_schema(rnd_obj["eval"], f"{ctx}.eval", errors, warnings)
    if "feedback" in rnd_obj:
        _validate_feedback_schema(rnd_obj["feedback"], f"{ctx}.feedback", errors, warnings)


def _validate_scenario_schema(
    data: Any, manifest_path: Path, errors: list[str], warnings: list[str]
) -> bool:
    ctx = f"{manifest_path.parent.name}/manifest.json"
    if not _check_keys(
        data, SCENARIO_REQUIRED, SCENARIO_OPTIONAL,
        allow_extra=False, ctx=ctx, errors=errors, warnings=warnings,
    ):
        return False
    sid = data.get("scenario_id")
    dir_name = manifest_path.parent.name
    if sid != dir_name:
        errors.append(
            f"{ctx}: scenario_id '{sid}' must match parent directory name '{dir_name}'"
        )
    if not isinstance(data.get("workspace_template"), str) or not data["workspace_template"]:
        errors.append(f"{ctx}: 'workspace_template' must be non-empty string")
    if not isinstance(data.get("scripts"), str) or not data["scripts"]:
        errors.append(f"{ctx}: 'scripts' must be non-empty string")
    if not isinstance(data.get("rounds_ref"), str) or not data["rounds_ref"]:
        errors.append(f"{ctx}: 'rounds_ref' must be non-empty string")
    if not _is_str_list(data.get("main_agent_accessible_paths")):
        errors.append(f"{ctx}: 'main_agent_accessible_paths' must be a list of strings")
    if "main_agent_delegable_paths" in data and not _is_str_list(data.get("main_agent_delegable_paths")):
        errors.append(f"{ctx}: 'main_agent_delegable_paths' must be a list of strings")
    updates = data.get("updates")
    if not isinstance(updates, dict):
        errors.append(f"{ctx}: 'updates' must be a dict")
    else:
        for uid, ug in updates.items():
            _validate_update_group_schema(ug, f"{ctx}.updates['{uid}']", errors, warnings)
    return True


# ---------------------------------------------------------------------------
# eval.command placeholder & path validation
# ---------------------------------------------------------------------------


def _validate_eval_command(
    command: str,
    *,
    rtype: str,
    scripts_dir: Path,
    workspace_template: Path,
    ctx: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    # Force exec_check rounds to use external scripts
    scripts_refs = SCRIPTS_PATH_RE.findall(command)
    if rtype == "exec_check" and not scripts_refs:
        errors.append(
            f"{ctx}: exec_check command must invoke at least one ${{scripts}}/<script> "
            f"(no inline shell logic allowed); got: {command!r}"
        )

    # Every ${scripts}/<rel> must exist after resolution
    for raw in scripts_refs:
        rel = raw.replace("${scripts}", "")
        rel = rel.lstrip("/")
        if not rel:
            errors.append(f"{ctx}: bare ${{scripts}} reference without sub-path: {raw}")
            continue
        resolved = (scripts_dir / rel).resolve(strict=False)
        if not resolved.exists():
            errors.append(f"{ctx}: scripts reference not found on disk: {resolved}")

    # ${workspace}/<rel> not present in workspace_template → warn (the agent may
    # create it during run)
    for raw in WORKSPACE_PATH_RE.findall(command):
        rel = raw.replace("${workspace}", "").lstrip("/")
        if not rel:
            continue
        resolved = (workspace_template / rel).resolve(strict=False)
        if not resolved.exists():
            warnings.append(
                f"{ctx}: ${{workspace}}/{rel} not in template "
                f"(may be created by agent at runtime)"
            )

    # Unknown placeholder (not in the known set, not shell uppercase style) → warn
    for m in ANY_PLACEHOLDER_RE.finditer(command):
        name = m.group(1)
        if name in KNOWN_PLACEHOLDERS:
            continue
        if _SHELL_LIKE.match(name):
            continue
        warnings.append(
            f"{ctx}: unknown placeholder ${{{name}}} (kept verbatim); "
            f"known: {sorted(KNOWN_PLACEHOLDERS)}"
        )


# ---------------------------------------------------------------------------
# Update virtual FS simulation
# ---------------------------------------------------------------------------


def _simulate_updates(
    rounds: list[dict[str, Any]],
    updates: dict[str, dict[str, Any]],
    manifest_path: Path,
    workspace_template: Path,
    scenario_ctx: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    view: set[str] = _enumerate_files_rel(workspace_template)

    # Fix (fix/audit-top10 W3 v1#6): re-applying op='new' collides, but op='replace'
    # is idempotent (_remove_prefix then copy), so a legitimate "repeatedly replace
    # the same set of files across rounds" was previously false-flagged. Here we only
    # enforce cross-round uniqueness for 'new'; 'replace' is allowed.
    new_uids = {uid for uid, info in updates.items() if info.get("op") == "new"}
    uid_rounds: dict[str, list[str]] = {}
    for rnd in rounds:
        rid = rnd.get("id", "?")
        for uid in rnd.get("update_ids") or []:
            if isinstance(uid, str):
                uid_rounds.setdefault(uid, []).append(rid)
    for uid, rids in uid_rounds.items():
        if len(rids) > 1 and uid in new_uids:
            errors.append(
                f"{scenario_ctx}: update_id '{uid}' (op='new') appears in {len(rids)} rounds: "
                f"{rids} — re-applying 'new' will collide on existing path"
            )

    for rnd in rounds:
        rid = rnd.get("id", "?")
        for uid in rnd.get("update_ids") or []:
            if uid not in updates:
                errors.append(
                    f"{scenario_ctx}: round '{rid}' references unknown update_id '{uid}'"
                )
                continue
            ug = updates[uid]
            op = ug.get("op")
            if op not in KNOWN_UPDATE_OPS:
                continue  # already reported by schema
            files = ug.get("files") or []
            for i, f in enumerate(files):
                src_rel = f.get("src", "")
                dst_rel = f.get("dst", "")
                if not isinstance(src_rel, str) or not isinstance(dst_rel, str):
                    continue  # schema already reported
                src_abs = _resolve_rel(manifest_path, src_rel)
                ctx = f"{scenario_ctx}.updates['{uid}'].files[{i}]"
                if not src_abs.exists():
                    errors.append(f"{ctx}: src not found on disk: {src_abs}")
                    continue
                # simulate apply
                dst_norm = dst_rel.lstrip("/").rstrip("/")
                if op == "new":
                    if _has_prefix(view, dst_norm):
                        errors.append(
                            f"{ctx}: op='new' but dst '{dst_norm}' already exists in workspace "
                            f"after applying preceding updates (round '{rid}')"
                        )
                    # write: enumerate src sub-files and attach them under dst_norm
                    for sub in _enumerate_src_rel(src_abs):
                        view.add(_join_rel(dst_norm, sub))
                elif op == "replace":
                    if not _has_prefix(view, dst_norm):
                        errors.append(
                            f"{ctx}: op='replace' but dst '{dst_norm}' does not exist in workspace "
                            f"at round '{rid}' (template + earlier updates)"
                        )
                    _remove_prefix(view, dst_norm)
                    for sub in _enumerate_src_rel(src_abs):
                        view.add(_join_rel(dst_norm, sub))


# ---------------------------------------------------------------------------
# Top-level entry
# ---------------------------------------------------------------------------


def validate_dataset_strict(data_dir: Path) -> ValidationReport:
    """Main validation entry point. Returns a ``ValidationReport``.

    Validation order: tests.json → manifests.json → each scenario manifest →
    each questions.json → cross-file paths and update simulation.
    """
    rep = ValidationReport()
    errors, warnings = rep.errors, rep.warnings

    # 1) tests.json
    tests_path = data_dir / "tests.json"
    tests_data = _read_json(tests_path, "tests.json", errors)
    if tests_data is None:
        return rep
    if not _validate_tests_schema(tests_data, tests_path, errors, warnings):
        return rep

    # 2) manifests.json
    manifests_rel = tests_data.get("manifests_ref")
    if not isinstance(manifests_rel, str):
        return rep
    manifests_path = _resolve_rel(tests_path, manifests_rel)
    if not manifests_path.exists():
        errors.append(f"tests.json.manifests_ref: file not found: {manifests_path}")
        return rep
    manifests_data = _read_json(manifests_path, "manifests.json", errors)
    if manifests_data is None:
        return rep
    if not _validate_manifests_schema(manifests_data, manifests_path, errors, warnings):
        return rep

    # 3) tests.scenario_ids ⊆ manifests.scenarios  (subset check)
    scenarios_map = manifests_data.get("scenarios") or {}
    requested_ids = tests_data.get("scenario_ids") or []
    for sid in requested_ids:
        if sid not in scenarios_map:
            errors.append(
                f"tests.json: scenario_id '{sid}' not declared in manifests.json"
            )

    # 4) per scenario
    for sid in requested_ids:
        if sid not in scenarios_map:
            continue
        scenario_rel = scenarios_map[sid]
        if not isinstance(scenario_rel, str):
            continue
        manifest_path = _resolve_rel(manifests_path, scenario_rel)
        if not manifest_path.exists():
            errors.append(f"manifests.json: scenario '{sid}' manifest not found: {manifest_path}")
            continue
        scenario_data = _read_json(manifest_path, f"{sid}/manifest.json", errors)
        if scenario_data is None:
            continue
        if not _validate_scenario_schema(scenario_data, manifest_path, errors, warnings):
            continue
        scenario_ctx = f"{sid}/manifest.json"

        # 4a) workspace_template / scripts / rounds_ref paths
        ws_rel = scenario_data.get("workspace_template", "")
        ws_path = _resolve_rel(manifest_path, ws_rel) if isinstance(ws_rel, str) else None
        if ws_path is None or not ws_path.exists() or not ws_path.is_dir():
            errors.append(f"{scenario_ctx}: workspace_template not found or not a dir: {ws_path}")
            ws_path = manifest_path.parent  # fallback to avoid crash downstream

        scripts_rel = scenario_data.get("scripts", "")
        scripts_path = (
            _resolve_rel(manifest_path, scripts_rel) if isinstance(scripts_rel, str) else None
        )
        if scripts_path is None or not scripts_path.exists() or not scripts_path.is_dir():
            errors.append(f"{scenario_ctx}: scripts dir not found or not a dir: {scripts_path}")
            scripts_path = manifest_path.parent

        rounds_rel = scenario_data.get("rounds_ref", "")
        rounds_path = (
            _resolve_rel(manifest_path, rounds_rel) if isinstance(rounds_rel, str) else None
        )
        if rounds_path is None or not rounds_path.exists():
            errors.append(f"{scenario_ctx}: rounds_ref file not found: {rounds_path}")
            continue
        rounds_data = _read_json(rounds_path, f"{sid}/{rounds_path.name}", errors)
        if not isinstance(rounds_data, list):
            errors.append(f"{sid}/{rounds_path.name}: top-level must be a JSON list")
            continue

        # 4b) accessible_paths / delegable_paths must resolve within workspace_template.
        # Cross-reference updates: a directory created by an op=new / op=replace dst
        # that has this path as a prefix is not treated as an "orphan" and does not
        # warn (e.g. directories such as update_supplement / whistleblower_packet
        # injected by u1 in several wave1 scenarios).
        update_dsts: list[str] = []
        for ug in (scenario_data.get("updates") or {}).values():
            if not isinstance(ug, dict):
                continue
            for f in ug.get("files") or []:
                if isinstance(f, dict) and isinstance(f.get("dst"), str):
                    update_dsts.append(f["dst"].strip("/"))

        def _created_by_update(ap: str) -> bool:
            ap_norm = ap.strip("/")
            if not ap_norm:
                return False
            for dst in update_dsts:
                if dst == ap_norm or dst.startswith(ap_norm + "/"):
                    return True
            return False

        for field_name in ("main_agent_accessible_paths", "main_agent_delegable_paths"):
            for ap in scenario_data.get(field_name) or []:
                if not isinstance(ap, str):
                    continue
                resolved = (ws_path / ap).resolve(strict=False)
                try:
                    resolved.relative_to(ws_path.resolve())
                except ValueError:
                    errors.append(
                        f"{scenario_ctx}: {field_name} entry '{ap}' escapes workspace_template"
                    )
                    continue
                if not resolved.exists() and not _created_by_update(ap):
                    warnings.append(
                        f"{scenario_ctx}: {field_name} entry '{ap}' not present in template "
                        f"(may be created by an update or by agent)"
                    )

        # 4c) each round
        seen_ids: set[str] = set()
        for i, rnd in enumerate(rounds_data):
            r_ctx = f"{sid}/{rounds_path.name}[{i}]"
            _validate_round_schema(rnd, r_ctx, errors, warnings)
            if isinstance(rnd, dict):
                rid = rnd.get("id")
                if isinstance(rid, str):
                    if rid in seen_ids:
                        errors.append(f"{sid}: duplicate round id '{rid}'")
                    seen_ids.add(rid)
                if isinstance(rnd.get("eval"), dict) and isinstance(rnd["eval"].get("command"), str):
                    rtype = rnd.get("type", "")
                    _validate_eval_command(
                        rnd["eval"]["command"],
                        rtype=rtype,
                        scripts_dir=scripts_path,
                        workspace_template=ws_path,
                        ctx=f"{r_ctx}.eval.command",
                        errors=errors,
                        warnings=warnings,
                    )

        # 4d) update FS simulation
        updates_dict = scenario_data.get("updates") or {}
        if isinstance(updates_dict, dict):
            valid_rounds = [r for r in rounds_data if isinstance(r, dict)]
            _simulate_updates(
                valid_rounds, updates_dict, manifest_path, ws_path,
                scenario_ctx, errors, warnings,
            )

    return rep
