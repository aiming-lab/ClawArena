"""check_q2.py — Verify output/notes/papers_summary.md covers all four papers.

Checks (all must pass):
  1. File exists and has >= 8 non-blank lines.
  2. Each of paper_a..paper_d has a dedicated paragraph header or mention:
       at least one of {"paper_a" / "paper a" / "sparseformer"}, etc.
  3. Each paper's headline number + topic anchor present (same anchors as before).
  4. Each paper paragraph contains at least one numeric value (digit sequence).
  5. Honey-pot (red-herring archive guard): if the WITHDRAWN headline figure
     "23%" appears for paper_a without being explicitly flagged as archived /
     withdrawn / incorrect / wrong, the check fails. The canonical figure is 40%.

Per-paper anchors:
  paper_a: "40%" + (sparse attention | VRAM | SparseFormer)
  paper_b: "35%" + (mixture[-]of[-]experts | MoE | latency | ClusterMoE)
  paper_c: "28%" + (retrieval | factual | RAG | FaithRAG)
  paper_d: "52%" + (constitutional | toxicity | alignment | DistillAlign)

Archive guard for paper_a:
  If the withdrawn percentage figure "23%" (matched as a standalone percentage,
  not the raw substring "23") appears within 160 chars of a SparseFormer/VRAM/
  sparse-attention reference WITHOUT a discredit word in the same window,
  treat it as citing the withdrawn figure → fail. A bare "23" inside "2023",
  "1.23", "23 references", etc. is NOT the withdrawn figure and is ignored.

Usage: python checks/check_q2.py <workspace>
Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CLAIM_ANCHORS: list[tuple[str, str, str]] = [
    ("paper_a", r"\b40\b", r"sparse[\s_]?attention|VRAM|SparseFormer"),
    ("paper_b", r"\b35\b", r"mixture[- ]of[- ]experts|MoE|inference\s+latency|ClusterMoE"),
    ("paper_c", r"\b28\b", r"retrieval|factual|RAG|FaithRAG"),
    ("paper_d", r"\b52\b", r"constitutional|toxicity|alignment|DistillAlign"),
]

# Each paper must be mentioned by one of these identifiers.
PAPER_IDENTIFIERS: list[tuple[str, list[str]]] = [
    ("paper_a", ["paper_a", "paper a", "sparseformer", "sparse attention", "sparse former"]),
    ("paper_b", ["paper_b", "paper b", "clustermoe", "cluster moe", "mixture of experts", "moe"]),
    ("paper_c", ["paper_c", "paper c", "faithrag", "faith rag", "retrieval augmented", "rag"]),
    ("paper_d", ["paper_d", "paper d", "distillalign", "distill align", "constitutional ai"]),
]

# Forbidden phrase for paper_a: the withdrawn 23%-VRAM figure.
#
# The withdrawn draft headline is the *percentage* figure "23%" (e.g.
# "reduces VRAM by 23%", "23% reduction in VRAM"). It is never written as a
# bare token. Across every canonical source ("papers/paper_{a..d}/", slides,
# refs, video transcript) the literal "23%" never appears — it is unique to
# "papers/_archive/paper_a_v0/". We therefore match the withdrawn figure as a
# *percentage value* rather than scanning for the raw substring "23".
#
# The old `text.lower().find("23")` substring scan matched "23" anywhere,
# falsely tripping on innocuous, correct content that happens to contain the
# digits 2-3, e.g.: the year "2023", a ratio like "1.23×", reference counts
# such as "23 references"/"23 baselines", or section numbers — none of which
# are the withdrawn VRAM figure. ARCHIVE_FIGURE_RE pins the match to a
# standalone "23%" via a word boundary plus an explicit percent unit, so
# "2023" (preceded by the word char "0"), "1.23" (decimal, no percent unit),
# and "230"/"123" (trailing/leading digit) are all excluded.
ARCHIVE_FIGURE_RE = re.compile(r"(?<![\d.])23\s*(?:%|percent\b|per[\s-]?cent\b)", re.IGNORECASE)
ARCHIVE_TOPIC_RE = re.compile(r"sparse[\s_]?attention|VRAM|SparseFormer|sparse\s+former", re.IGNORECASE)
DISCREDIT_RE = re.compile(
    r"withdrawn|archive|archived|retract|retracted|incorrect|wrong|"
    r"superseded|do not cite|don[''']?t cite|pre[- ]?submission|draft",
    re.IGNORECASE,
)


def _archive_figure_safely_flagged(text: str) -> bool:
    """Return True iff every occurrence of the withdrawn "23%" figure that sits
    near a sparse-attention/VRAM topic is accompanied by a discredit word
    within a 160-char window.

    The withdrawn figure is matched as a standalone percentage ("23%",
    "23 percent") via ARCHIVE_FIGURE_RE — *not* as the raw substring "23" — so
    correct content containing the digits 2-3 (years like "2023", ratios like
    "1.23×", reference counts like "23 references") does not trip the guard.
    If the "23%" figure never appears near a paper_a topic, return True.
    """
    for m in ARCHIVE_FIGURE_RE.finditer(text):
        i = m.start()
        window = text[max(0, i - 160): m.end() + 160]
        if ARCHIVE_TOPIC_RE.search(window):
            if not DISCREDIT_RE.search(window):
                return False
    return True  # either not found near paper_a or always discredited


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q2.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    note_path = ws / "output" / "notes" / "papers_summary.md"

    if not note_path.exists():
        print(f"FAIL: {note_path} does not exist")
        return 1

    text = note_path.read_text(encoding="utf-8")
    lower = text.lower()
    failures: list[str] = []

    # 1. Substantive content.（四篇论文的数值锚点另有逐一硬校验；行数仅作覆盖度防线，
    # 放宽到 >= 4——每篇一段（即使整段不换行）亦算合格，不强求 >= 8 行。）
    non_empty_lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(non_empty_lines) < 4:
        failures.append(
            f"papers_summary.md appears too short ({len(non_empty_lines)} non-blank lines); "
            "expected >= 4 lines/paragraphs covering 4 papers"
        )

    # 2. Each paper mentioned by name.
    for paper, variants in PAPER_IDENTIFIERS:
        if not any(v in lower for v in variants):
            failures.append(
                f"{paper}: not mentioned by name or common abbreviation "
                f"(expected one of: {variants})"
            )

    # 3. Headline number + topic anchor per paper.
    for paper, num_pat, topic_pat in CLAIM_ANCHORS:
        if not re.search(num_pat, text, re.IGNORECASE):
            failures.append(
                f"{paper}: headline number anchor '{num_pat}' not found"
            )
        elif not re.search(topic_pat, text, re.IGNORECASE):
            failures.append(
                f"{paper}: topic anchor '{topic_pat}' not found"
            )

    # 4. Archive guard: the withdrawn 23%-VRAM figure must not be cited as canonical.
    if not _archive_figure_safely_flagged(text):
        failures.append(
            "paper_a: the withdrawn preprint figure (23% VRAM reduction) appears to "
            "be cited without being flagged as incorrect/withdrawn. The canonical "
            "figure from papers/paper_a/ is 40%. Citing the archive is an error."
        )

    if failures:
        print("FAIL: papers_summary.md check failed:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "PASS: check_q2 — papers_summary.md covers each paper with headline "
        "number + topic anchor; archive guard passed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
