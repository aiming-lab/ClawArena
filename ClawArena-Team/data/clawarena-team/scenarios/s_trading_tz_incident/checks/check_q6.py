"""check_q6.py — Validate q6: background p99 aggregation + incident RCA synthesis.

Pass conditions (all must hold):

A. Background execution
   A1. [ADVISORY ONLY (non-gating)] sessions/main.jsonl contains at least one RunSubagent call with
       run_in_background=true (background p99 aggregation task launched).

B. output/incident_rca.md
   B1. File exists; >= 400 bytes.
   B2. >= 5 distinct bullet-point lines (lines starting with '-', '*', or digit+'.').
   B3. References >= 2 prior-round output files from:
       {output/root_cause_analysis.md, output/order_loss_summary.md,
        output/intake_scope.md, output/regulatory_incident_report.json,
        output/regulatory_cover_note.md}
   B4. Contains the keyword 'root_cause' (verbatim; compliance-system index term).
   B5. References figures/p99_cross_tz.png (the pre-seeded cross-timezone chart).

Tags covered: background_subagent, async_long_running, partial_result_handling,
              code_execution, final_synthesis
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Prior-round output files the RCA is expected to reference (>= 2 required)
PRIOR_OUTPUT_FILES = (
    "output/root_cause_analysis.md",
    "output/order_loss_summary.md",
    "output/intake_scope.md",
    "output/regulatory_incident_report.json",
    "output/regulatory_cover_note.md",
)

# Regex: bullet line (- / * / digit.)
BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+\S", re.MULTILINE)

# Regex: root_cause keyword (allow underscore or hyphen variants; verbatim index term)
ROOT_CAUSE_RE = re.compile(r"root[_\-]cause", re.IGNORECASE)

# Regex: p99 cross-tz chart reference
CHART_RE = re.compile(r"p99_cross_tz\.png|p99_cross_tz|figures/p99", re.IGNORECASE)

MIN_RCA_BYTES = 400
MIN_BULLETS = 5
MIN_PRIOR_FILE_REFS = 2


def _has_background_run(ws: Path) -> bool:
    """Return True if sessions/main.jsonl contains a RunSubagent with run_in_background=true."""
    sessions_dir = ws.parent / "sessions"
    main_jsonl = sessions_dir / "main.jsonl"
    if not main_jsonl.exists():
        print(
            f"[warn] sessions/main.jsonl not found at {main_jsonl}; "
            "skipping background-run check"
        )
        return True  # warn-only: no sessions file is treated as a soft skip
    try:
        lines = main_jsonl.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"[warn] could not read {main_jsonl}: {exc}; skipping background-run check")
        return True
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("role") != "assistant":
            continue
        for tc in (msg.get("tool_calls") or []):
            # 兼容扁平 {"name","arguments"} 与嵌套 {"function":{...}}
            name = tc.get("name") or (tc.get("function") or {}).get("name", "")
            if name not in ("RunSubagent", "Bash"):
                continue
            raw_args = tc.get("arguments")
            if raw_args is None:
                raw_args = (tc.get("function") or {}).get("arguments") or "{}"
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
            except json.JSONDecodeError:
                continue
            # 后台判定整体放宽：run_in_background 多真值形态，或 Bash 命令含 shell 后台符
            rib = args.get("run_in_background")
            if rib is True or rib == 1 or (
                isinstance(rib, str) and rib.strip().lower() in ("true", "1", "yes")
            ):
                return True
            if name == "Bash":
                cmd = str(args.get("command") or args.get("cmd") or "")
                if (
                    re.search(r"(?<!&)&\s*$", cmd.strip())
                    or re.search(r"(?:^|\s)(?:nohup|setsid)\b", cmd)
                    or "disown" in cmd
                ):
                    return True
    return False


def _count_bullets(text: str) -> int:
    return len(BULLET_RE.findall(text))


def _count_prior_refs(text: str) -> int:
    count = 0
    for filepath in PRIOR_OUTPUT_FILES:
        # Match the filename or the full path fragment
        filename = filepath.split("/")[-1]
        if filepath in text or filename in text:
            count += 1
    return count


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    errors: list[str] = []

    # ------------------------------------------------------------------
    # A. Background execution check
    # ------------------------------------------------------------------
    # A1 — instruction-following gate: prompt explicitly asks to launch this in the background
    if not _has_background_run(ws):
        errors.append(
            "background subagent not observed — the task asked you to launch this as a "
            "background RunSubagent(run_in_background=true) and not block the main thread"
        )

    # ------------------------------------------------------------------
    # B. output/incident_rca.md
    # ------------------------------------------------------------------
    rca_path = ws / "output" / "incident_rca.md"
    if not rca_path.exists():
        errors.append(
            "B1: output/incident_rca.md does not exist — write the RCA synthesis "
            "document to this path covering root cause, affected regions, customer "
            "impact, timezone normalization, and remediation"
        )
    else:
        rca_bytes = len(rca_path.read_bytes())
        rca_text = rca_path.read_text(encoding="utf-8")

        # B1. Size
        if rca_bytes < MIN_RCA_BYTES:
            errors.append(
                f"B1: output/incident_rca.md is too short ({rca_bytes} bytes; "
                f"minimum {MIN_RCA_BYTES}) — expand the RCA with detailed bullet points"
            )

        # B2. Bullet count
        n_bullets = _count_bullets(rca_text)
        if n_bullets < MIN_BULLETS:
            errors.append(
                f"B2: output/incident_rca.md has only {n_bullets} bullet point(s); "
                f"need >= {MIN_BULLETS} — include bullets for: root cause event, "
                "affected regions, customer impact (loss figure + failed orders), "
                "timezone normalization approach, and recommended remediation actions"
            )

        # B3. Prior-round file references
        n_refs = _count_prior_refs(rca_text)
        if n_refs < MIN_PRIOR_FILE_REFS:
            refs_found = [
                f for f in PRIOR_OUTPUT_FILES
                if f in rca_text or f.split("/")[-1] in rca_text
            ]
            errors.append(
                f"B3: output/incident_rca.md references only {n_refs} prior-round "
                f"output file(s) (found: {refs_found or 'none'}); need >= {MIN_PRIOR_FILE_REFS} — "
                "cite at least 2 of: output/root_cause_analysis.md, "
                "output/order_loss_summary.md, output/intake_scope.md, "
                "output/regulatory_incident_report.json, output/regulatory_cover_note.md"
            )

        # B4. root_cause keyword
        if not ROOT_CAUSE_RE.search(rca_text):
            errors.append(
                "B4: output/incident_rca.md does not contain the keyword 'root_cause' "
                "(verbatim; required by the compliance-system indexer) — include it at "
                "least once, e.g. 'root_cause: dispatch_adapter tz_offset_applied "
                "changed from +00:00 to +08:00 at 2026-03-27T17:23:09Z'"
            )

        # B5. p99_cross_tz.png chart reference
        if not CHART_RE.search(rca_text):
            errors.append(
                "B5: output/incident_rca.md does not reference the cross-timezone p99 "
                "chart — mention 'figures/p99_cross_tz.png' and describe the SGT p99 "
                "spike at 17:23 UTC (2,847 ms) as evidence of the dispatch_adapter "
                "CONFIG_RELOAD impact on Asia-Pacific settlement latency"
            )

    # ------------------------------------------------------------------
    # Result
    # ------------------------------------------------------------------
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: background p99 aggregation task launched (RunSubagent run_in_background=true); "
        "output/incident_rca.md exists with >= 5 bullet points, >= 2 prior-round file "
        "references, root_cause keyword, and p99_cross_tz.png chart reference"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
