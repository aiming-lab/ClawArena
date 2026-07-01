#!/usr/bin/env python3
"""lint_scenario.py — Offline sanity check for an SMbench scenario directory.

This is **not** a graded check; it is a developer aid that flags common authoring
mistakes before runtime:

  1. Every relative path mentioned inside `questions.json` (in question / feedback /
     eval.command) resolves under either the workspace template or the scripts
     directory.
  2. Every path required for the round either falls under
     `main_agent_accessible_paths` (so the main agent can read it directly) or is
     explicitly designated as subagent-only material in `_sandbox_hint.md`. Paths
     that are listed in `_sandbox_hint.md` AND reachable to main are flagged as
     "main should not read these directly".
  3. `feedback.incorrect` does not regurgitate values that look like ground-truth
     answers (e.g. "March 15", "45", "30 calendar days", quoted multi-word phrases
     that look like plant sentences). Light heuristic; false positives possible.

Usage:
    python helper/lint_scenario.py data/smbench-demo/scenarios/s_<id>
    python helper/lint_scenario.py data/smbench-demo/scenarios/*

Exit codes:
    0 — no issues
    1 — one or more warnings emitted
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PATH_RE = re.compile(r"`([A-Za-z0-9_\-./]+(?:\.[A-Za-z0-9]+|/))`")
SUSPICIOUS_LEAK_RE = re.compile(
    r"""
    (?:\b\d{1,3}\s*(?:days?|calendar\s+days?)\b)         # "45 days"
    | (?:\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\b)
    | (?:\b\d{4}-\d{2}-\d{2}\b)                          # ISO date
    | (?:expected\s+\w+\s*=\s*\S+)                       # "expected legal_min_days=45"
    """,
    re.IGNORECASE | re.VERBOSE,
)


class LintIssue:
    def __init__(self, scenario: str, kind: str, message: str):
        self.scenario = scenario
        self.kind = kind
        self.message = message

    def __str__(self) -> str:
        return f"[{self.scenario}] {self.kind}: {self.message}"


def _collect_paths(text: str) -> set[str]:
    return {m.group(1).rstrip("/") for m in PATH_RE.finditer(text)}


def _reachable_to_main(rel_path: str, accessible: list[str], workspace: Path) -> bool:
    norm = rel_path.lstrip("./")
    for prefix in accessible:
        p = prefix.lstrip("./")
        if norm == p or norm.startswith(p + "/"):
            return True
    # Heuristic: if the bare token names a file/folder that lives under one
    # of the accessible roots, treat it as reachable. E.g. question mentions
    # `paper_e/` while accessible contains `papers/` and `papers/paper_e/` exists.
    candidate = workspace / norm
    if candidate.exists():
        for prefix in accessible:
            full_prefix = workspace / prefix.lstrip("./")
            try:
                candidate.resolve().relative_to(full_prefix.resolve())
                return True
            except (ValueError, OSError):
                continue
        # fall through — exists but not under any prefix
    # also try matching the leaf name against children of accessible dirs
    leaf = norm.rstrip("/").split("/")[-1]
    for prefix in accessible:
        full_prefix = workspace / prefix.lstrip("./")
        if not full_prefix.is_dir():
            continue
        for child in full_prefix.iterdir():
            if child.name == leaf:
                return True
    return False


def _update_dst_leaves(manifest: dict, scenario_dir: Path) -> set[str]:
    """Collect leaf names that updates will install (so the lint can recognise
    paths like `paper_e/` referenced in round 5 even though they live under
    `updates/u1/...` before the update applies)."""
    leaves: set[str] = set()
    for u in (manifest.get("updates") or {}).values():
        for f in u.get("files", []) or []:
            dst = (f.get("dst") or "").rstrip("/")
            if not dst:
                continue
            leaves.add(dst)
            leaves.add(dst.split("/")[-1])
    return leaves


def lint_scenario(scenario_dir: Path) -> list[LintIssue]:
    issues: list[LintIssue] = []
    sid = scenario_dir.name

    manifest_path = scenario_dir / "manifest.json"
    questions_path = scenario_dir / "questions.json"
    workspace = scenario_dir / "workspace"
    hint_path = workspace / "_sandbox_hint.md"

    if not manifest_path.exists():
        issues.append(LintIssue(sid, "manifest", "manifest.json missing"))
        return issues
    if not questions_path.exists():
        issues.append(LintIssue(sid, "questions", "questions.json missing"))
        return issues

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    accessible: list[str] = manifest.get("main_agent_accessible_paths", [])
    update_leaves = _update_dst_leaves(manifest, scenario_dir)

    hint_text = hint_path.read_text(encoding="utf-8") if hint_path.exists() else ""

    if not hint_path.exists():
        issues.append(LintIssue(sid, "hint", "workspace/_sandbox_hint.md missing"))

    # Collect paths the main agent is expected to interact with, by parsing
    # backticked tokens in every question / feedback string.
    for q in questions:
        qid = q.get("id", "?")
        question_text = q.get("question", "")
        feedback = q.get("feedback", {}) or {}

        # ── leak heuristic on feedback.incorrect ─────────────────────────
        incorrect = feedback.get("incorrect", "") or ""
        for m in SUSPICIOUS_LEAK_RE.finditer(incorrect):
            issues.append(LintIssue(
                sid, "leak",
                f"{qid}: feedback.incorrect contains possible ground-truth leak: "
                f"{m.group(0)!r}"
            ))
        # detect quoted multi-word plant sentences (only check double quotes
        # to avoid false positives on possessives like "the paper's")
        for m in re.finditer(r'"([^"\n]{20,})"', incorrect):
            phrase = m.group(1)
            if len(phrase.split()) >= 4:
                issues.append(LintIssue(
                    sid, "leak",
                    f"{qid}: feedback.incorrect quotes a long phrase that may be the answer: "
                    f"{phrase!r}"
                ))

        # ── path reachability ────────────────────────────────────────────
        question_paths = _collect_paths(question_text)
        for raw_path in question_paths:
            if raw_path.startswith(("http", "python", "${")):
                continue
            if raw_path in {".", ".."} or len(raw_path) <= 2:
                continue
            target = workspace / raw_path
            # path exists under workspace template (now or after some update)?
            scenario_has_it = target.exists() or any(
                (scenario_dir / "updates" / u / raw_path).exists()
                for u in (d.name for d in (scenario_dir / "updates").iterdir())
                if (scenario_dir / "updates").exists()
            )
            if not scenario_has_it:
                # could still be the literal name of an update directory entry
                pass
            reachable = _reachable_to_main(raw_path, accessible, workspace)
            # treat paths that updates install as reachable (their dst falls under
            # an accessible prefix per the manifest contract).
            if not reachable and (raw_path in update_leaves or raw_path.rstrip("/") in update_leaves):
                reachable = True
            mentioned_in_hint = raw_path in hint_text
            # If the question expects main to do something with `path/`, then either
            # main must reach it, OR the hint must explain it is subagent-only.
            if not reachable and not mentioned_in_hint:
                issues.append(LintIssue(
                    sid, "scope",
                    f"{qid}: question references `{raw_path}` which is not in "
                    f"main_agent_accessible_paths and is not mentioned in "
                    f"_sandbox_hint.md (so main has no way to discover it)."
                ))

    return issues


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    targets: list[Path] = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"skip: {p} does not exist", file=sys.stderr)
            continue
        if (p / "manifest.json").exists():
            targets.append(p)
        else:
            for sub in sorted(p.iterdir()):
                if (sub / "manifest.json").exists():
                    targets.append(sub)

    all_issues: list[LintIssue] = []
    for t in targets:
        all_issues.extend(lint_scenario(t))

    if not all_issues:
        print(f"OK — {len(targets)} scenarios linted, no issues")
        return 0
    for issue in all_issues:
        print(issue)
    print(f"\n{len(all_issues)} issue(s) across {len(targets)} scenario(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
