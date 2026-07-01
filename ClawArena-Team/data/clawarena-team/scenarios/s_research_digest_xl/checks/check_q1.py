"""check_q1.py — Verify output/notes/brief_summary.md enumerates ALL five named
deliverables from requests/advisor_brief.md.

The advisor brief explicitly names five deliverables:
  1. Brief summary        → output/notes/brief_summary.md
  2. Papers summary       → output/notes/papers_summary.md
  3. Slides key points    → output/notes/slides_points.md
  4. Video takeaway       → output/notes/video_takeaway.md
  5. Final report         → output/final_report.md

The check requires all five deliverable keywords to appear by name in the
brief_summary.md note, and that the note contains at least 5 bullet lines.
The "source materials" check (papers/slides/video) is now subsumed by the
deliverable-name check.

Usage:
    python checks/check_q1.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
import sys
from pathlib import Path


# Deliverable labels and the keyword variants that prove the model named them.
# Each tuple is (deliverable_label, [acceptable_keyword_variants...]).
REQUIRED_DELIVERABLES: list[tuple[str, list[str]]] = [
    (
        "brief summary",
        ["brief summary", "brief_summary", "summary of the brief"],
    ),
    (
        "papers summary",
        ["papers summary", "papers_summary", "paper summary", "per-paper", "per paper"],
    ),
    (
        "slides key points",
        ["slides key points", "slides_points", "slide points", "slide key points", "key points"],
    ),
    (
        "video takeaway",
        ["video takeaway", "video_takeaway", "lecture takeaway", "audio takeaway"],
    ),
    (
        "final report",
        ["final report", "final_report"],
    ),
]

MIN_BULLETS = 5


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q1.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    note_path = ws / "output" / "notes" / "brief_summary.md"

    if not note_path.exists():
        print(f"FAIL: {note_path} does not exist")
        return 1

    text = note_path.read_text(encoding="utf-8")
    lower = text.lower()

    # 1. All five named deliverables must be referenced.
    missing: list[str] = []
    for label, variants in REQUIRED_DELIVERABLES:
        if not any(v in lower for v in variants):
            missing.append(label)

    if missing:
        print(
            f"FAIL: brief_summary.md is missing references to the following "
            f"named deliverables: {missing}"
        )
        print(
            "  The advisor brief lists five deliverables by name; all five must "
            "appear in the summary."
        )
        return 1

    # 2. Must have at least MIN_BULLETS bullet-style lines.
    bullet_lines = [
        ln for ln in text.splitlines()
        if ln.strip().startswith(("-", "*", "•", "1.", "2.", "3.", "4.", "5."))
    ]
    if len(bullet_lines) < MIN_BULLETS:
        print(
            f"FAIL: brief_summary.md has only {len(bullet_lines)} bullet points "
            f"(need >= {MIN_BULLETS} — one per deliverable)"
        )
        return 1

    print(
        f"PASS: check_q1 — brief_summary.md names all 5 deliverables and has "
        f"{len(bullet_lines)} bullet points"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
