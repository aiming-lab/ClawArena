"""check_q5.py — Comprehensive check for the final report, writer-subagent attribution,
and cross-round consistency.

Checks (all must pass; exit 0):

  1. output/final_report.md has all 5 required ## sections with substantive bodies.
  2. All 6 papers (paper_a..paper_f) referenced by name or abbreviation.
  3. Per-paper headline anchors (number + topic) present in the report.
  4. Audio-only takeaway phrase appears in Findings or Discussion (not just anywhere).
  5. paper_e and paper_f references >= 2 occurrences combined in Findings+Discussion.
  6. All four intermediate notes exist.
  7. output/sections/findings.md exists and is >= 400 bytes.
  8. Subagent attribution: at least one sub_*.jsonl session under ../sessions/ must
     contain a Write tool call whose file_path ends with output/sections/findings.md
     or resolves to that path. If ../sessions/ does not exist, skip with a warning.
  9. output/final_report.json exists and has the required shape:
       { "sections": [...], "papers": [...], "audio_only_takeaway": "..." }
     — "sections" must be a list of 5 strings containing the section names,
       "papers" must be a list of >= 6 strings containing paper identifiers,
       "audio_only_takeaway" must be a non-empty string.
 10. Cross-round consistency: headline numbers for paper_a..paper_d in
     final_report.md must match those in papers_summary.md for >= 3 of 4 papers.

Usage:
    python checks/check_q5.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

EXPECTED_SECTIONS = [
    "## Background",
    "## Methods",
    "## Findings",
    "## Discussion",
    "## Conclusion",
]

CLAIM_ANCHORS: list[tuple[str, str, str]] = [
    ("paper_a", r"\b40\b", r"sparse[\s_]?attention|VRAM|SparseFormer"),
    ("paper_b", r"\b35\b", r"mixture[- ]of[- ]experts|MoE|inference\s+latency|ClusterMoE"),
    ("paper_c", r"\b28\b", r"retrieval|factual|RAG|FaithRAG"),
    ("paper_d", r"\b52\b", r"constitutional|toxicity|alignment|DistillAlign"),
    ("paper_e", r"\b8\b",  r"federated|privacy|FedAlign"),
    ("paper_f", r"\b91\b", r"neuro[- ]?symbolic|compositional|NSR"),
]

# Numbers that identify papers in cross-round consistency check (paper_a..paper_d).
CROSS_ROUND_NUMBERS = [
    ("paper_a", r"\b40\b"),
    ("paper_b", r"\b35\b"),
    ("paper_c", r"\b28\b"),
    ("paper_d", r"\b52\b"),
]

PAPER_IDENTIFIERS: list[tuple[str, list[str]]] = [
    ("paper_a", ["paper_a", "paper a", "sparseformer", "sparse attention"]),
    ("paper_b", ["paper_b", "paper b", "clustermoe", "cluster moe", "mixture of experts", "moe"]),
    ("paper_c", ["paper_c", "paper c", "faithrag", "faith rag", "retrieval augmented", "rag"]),
    ("paper_d", ["paper_d", "paper d", "distillalign", "constitutional ai"]),
    ("paper_e", ["paper_e", "paper e", "fedalign", "federated", "fed align"]),
    ("paper_f", ["paper_f", "paper f", "nsr", "neurosymbolic", "neuro-symbolic", "compositional"]),
]

# Audio-only takeaway: must appear in Findings or Discussion section.
_PHRASE_A_LESSON = re.compile(r"real[\s]+lesson", re.IGNORECASE)
_PHRASE_A_REPRO = re.compile(r"reproduc|verifia", re.IGNORECASE)
_PHRASE_A_NOTSCALE = re.compile(r"not\s+scale|not\s+the\s+scale|rather\s+than\s+scale", re.IGNORECASE)
_PHRASE_C_LESSON = re.compile(
    r"(?:real|key|central|main|core|deeper|primary)\s+(?:lesson|insight|message|takeaway)",
    re.IGNORECASE,
)
_PHRASE_C_REPRO = re.compile(r"reproduc|verifia", re.IGNORECASE)

INTERMEDIATE_NOTES = [
    "output/notes/brief_summary.md",
    "output/notes/papers_summary.md",
    "output/notes/slides_points.md",
    "output/notes/video_takeaway.md",
]

# For final_report.json shape check.
REQUIRED_JSON_KEYS = {"sections", "papers", "audio_only_takeaway"}
REQUIRED_SECTION_NAMES = ["Background", "Methods", "Findings", "Discussion", "Conclusion"]


def _section_body(text: str, heading: str) -> str:
    """Return the body text between this heading and the next ## heading."""
    lines = text.splitlines()
    in_section = False
    body_parts: list[str] = []
    for ln in lines:
        if ln.strip() == heading.strip():
            in_section = True
            continue
        if in_section:
            if ln.startswith("## ") and ln.strip() != heading.strip():
                break
            stripped = ln.strip()
            if stripped and not stripped.startswith("<!--"):
                body_parts.append(ln)
    return "\n".join(body_parts)


def _section_body_lines(text: str, heading: str) -> list[str]:
    return [ln for ln in _section_body(text, heading).splitlines() if ln.strip()]


def _audio_takeaway_present(text: str) -> bool:
    has_a = bool(_PHRASE_A_LESSON.search(text) and _PHRASE_A_REPRO.search(text) and _PHRASE_A_NOTSCALE.search(text))
    has_c = bool(_PHRASE_C_LESSON.search(text) and _PHRASE_C_REPRO.search(text))
    return has_a or has_c


def _scan_sessions_for_write(sessions_dir: Path, target_suffix: str) -> bool:
    """Return True if any sub_*.jsonl under sessions_dir has a Write call to target_suffix."""
    for jsonl_file in sessions_dir.glob("sub_*.jsonl"):
        try:
            for raw_line in jsonl_file.read_text(encoding="utf-8", errors="replace").splitlines():
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    msg = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(msg, dict):
                    continue
                if msg.get("role") != "assistant":
                    continue
                tool_calls = msg.get("tool_calls") or []
                for tc in tool_calls:
                    try:
                        # 兼容扁平 {"name","arguments"} 与嵌套 {"function":{...}}
                        name = tc.get("name") or (tc.get("function") or {}).get("name", "")
                        if name != "Write":
                            continue
                        args_raw = tc.get("arguments")
                        if args_raw is None:
                            args_raw = (tc.get("function") or {}).get("arguments", "{}")
                        args = json.loads(args_raw) if isinstance(args_raw, str) else (args_raw or {})
                        fp = args.get("file_path", "")
                        if fp.endswith(target_suffix) or target_suffix in fp:
                            return True
                    except Exception:
                        continue
        except Exception:
            continue
    return False


def _extract_numbers_for_paper(text: str, num_pat: str) -> bool:
    return bool(re.search(num_pat, text, re.IGNORECASE))


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q5.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    report_path = ws / "output" / "final_report.md"
    failures: list[str] = []

    if not report_path.exists():
        print(f"FAIL: {report_path} does not exist")
        return 1

    report_text = report_path.read_text(encoding="utf-8")

    # ── 1. Section headers + substantive bodies ──────────────────────────────
    missing_sections = [s for s in EXPECTED_SECTIONS if s not in report_text]
    if missing_sections:
        failures.append(f"Missing section headers: {missing_sections}")

    for section in EXPECTED_SECTIONS:
        body_lines = _section_body_lines(report_text, section)
        joined = " ".join(body_lines).strip()
        if len(body_lines) < 2 and len(joined) < 200:
            failures.append(
                f"Section '{section}' body is empty or placeholder "
                f"({len(body_lines)} lines, {len(joined)} chars)"
            )

    # ── 2. All 6 papers referenced by name ───────────────────────────────────
    lower_report = report_text.lower()
    for paper, variants in PAPER_IDENTIFIERS:
        if not any(v in lower_report for v in variants):
            failures.append(
                f"{paper}: not referenced by name in final_report.md "
                f"(expected one of: {variants})"
            )

    # ── 3. Per-paper headline anchors ────────────────────────────────────────
    for paper, num_pat, topic_pat in CLAIM_ANCHORS:
        if not re.search(num_pat, report_text, re.IGNORECASE):
            failures.append(f"{paper}: headline number anchor '{num_pat}' missing from report")
        elif not re.search(topic_pat, report_text, re.IGNORECASE):
            failures.append(f"{paper}: topic anchor '{topic_pat}' missing from report")

    # ── 4. Audio-only takeaway in Findings or Discussion ─────────────────────
    findings_body = _section_body(report_text, "## Findings")
    discussion_body = _section_body(report_text, "## Discussion")
    findings_plus_discussion = findings_body + "\n" + discussion_body

    if not _audio_takeaway_present(findings_plus_discussion):
        # Try full document as fallback — but require section-local if not found there.
        if not _audio_takeaway_present(report_text):
            failures.append(
                "Audio-only takeaway (real lesson: reproducibility not scale) not found "
                "in Findings or Discussion section"
            )
        else:
            failures.append(
                "Audio-only takeaway found in report but NOT in Findings or Discussion section; "
                "it must appear in one of those sections"
            )

    # ── 5. paper_e and paper_f >= 2 mentions in Findings+Discussion ──────────
    ef_text = findings_plus_discussion.lower()
    ef_count = len(
        re.findall(r"paper[_\s]?[ef]|fedalign|federated|nsr|neurosymbolic|neuro.symbolic|compositional", ef_text)
    )
    if ef_count < 2:
        failures.append(
            f"paper_e/paper_f appear only {ef_count} time(s) in Findings+Discussion "
            f"(need >= 2; the u1 update must be integrated into those sections)"
        )

    # ── 6. Intermediate notes exist ──────────────────────────────────────────
    for rel_path in INTERMEDIATE_NOTES:
        note_path = ws / rel_path
        if not note_path.exists():
            failures.append(f"Intermediate note missing: {rel_path}")

    # ── 7. output/sections/findings.md >= 400 bytes ──────────────────────────
    findings_file = ws / "output" / "sections" / "findings.md"
    if not findings_file.exists():
        failures.append(
            "output/sections/findings.md does not exist — a writer subagent must "
            "produce this file directly"
        )
    else:
        size = findings_file.stat().st_size
        if size < 400:
            failures.append(
                f"output/sections/findings.md is only {size} bytes (need >= 400); "
                "the writer subagent must produce substantive content"
            )

    # ── 8. Subagent attribution via session scan ──────────────────────────────
    sessions_dir = ws.parent / "sessions"
    target_suffix = "output/sections/findings.md"
    if not sessions_dir.exists():
        print(
            "[warn] sessions/ not available, skipping subagent attribution check",
            file=sys.stderr,
        )
    else:
        if not _scan_sessions_for_write(sessions_dir, target_suffix):
            failures.append(
                "No sub_*.jsonl session found with a Write tool call to "
                "output/sections/findings.md — a dedicated writer subagent must "
                "produce that file, not the main agent"
            )

    # ── 9. output/final_report.json shape check ──────────────────────────────
    json_path = ws / "output" / "final_report.json"
    if not json_path.exists():
        failures.append(
            "output/final_report.json does not exist — must contain {sections, papers, "
            "audio_only_takeaway} keys"
        )
    else:
        try:
            rj = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            failures.append(f"output/final_report.json parse error: {e}")
            rj = {}

        missing_keys = REQUIRED_JSON_KEYS - set(rj.keys())
        if missing_keys:
            failures.append(
                f"output/final_report.json missing required keys: {sorted(missing_keys)}"
            )
        else:
            # sections: list of 5 strings.
            secs = rj.get("sections", [])
            if not isinstance(secs, list) or len(secs) < 5:
                failures.append(
                    f"final_report.json 'sections' must be a list of 5 section names; "
                    f"got: {secs!r}"
                )
            else:
                for name in REQUIRED_SECTION_NAMES:
                    if not any(name.lower() in str(s).lower() for s in secs):
                        failures.append(
                            f"final_report.json 'sections' missing '{name}'"
                        )
            # papers: list of >= 6 strings.
            papers = rj.get("papers", [])
            if not isinstance(papers, list) or len(papers) < 6:
                failures.append(
                    f"final_report.json 'papers' must be a list of >= 6 paper identifiers; "
                    f"got {len(papers) if isinstance(papers, list) else type(papers).__name__}"
                )
            # audio_only_takeaway: non-empty string.
            aot = rj.get("audio_only_takeaway", "")
            if not isinstance(aot, str) or not aot.strip():
                failures.append(
                    "final_report.json 'audio_only_takeaway' must be a non-empty string"
                )

    # ── 10. Cross-round consistency (>= 3/4 papers) ──────────────────────────
    papers_summary_path = ws / "output" / "notes" / "papers_summary.md"
    if papers_summary_path.exists():
        ps_text = papers_summary_path.read_text(encoding="utf-8")
        matching = 0
        for paper, num_pat in CROSS_ROUND_NUMBERS:
            in_report = _extract_numbers_for_paper(report_text, num_pat)
            in_summary = _extract_numbers_for_paper(ps_text, num_pat)
            if in_report and in_summary:
                matching += 1
        if matching < 3:
            failures.append(
                f"Cross-round consistency: only {matching}/4 paper headline numbers "
                f"appear in both final_report.md and papers_summary.md (need >= 3/4). "
                f"The headline numbers must be consistent between the rounds."
            )

    if failures:
        print("FAIL: check_q5 — final report check failed:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "PASS: check_q5 — final_report.md covers all 6 papers with anchors; "
        "audio takeaway in Findings/Discussion; writer subagent attribution OK; "
        "final_report.json shape OK; cross-round consistency OK."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
