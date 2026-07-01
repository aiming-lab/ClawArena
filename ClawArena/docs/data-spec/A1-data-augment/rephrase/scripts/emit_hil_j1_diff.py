"""Emit ORIGINAL vs v2-REPHRASED diff for hil_j1 exec_check rounds.

Note: the eval/hil_j1/questions.json file has been overwritten with v1 (and now v2),
so the only place we still have the pre-rephrase ORIGINAL text is the existing
v1 diff doc on disk. This script parses that file's "**ORIGINAL**" blocks and
splices them with the latest rephrased questions.json to produce a fresh
ORIGINAL-vs-v2 diff document.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_j1/questions.json"
DIFF_DOC = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_j1.md"


def parse_originals(diff_text: str) -> dict[str, str]:
    """Parse the existing diff doc, extracting q-id -> ORIGINAL text."""
    originals: dict[str, str] = {}
    # Split on "## qN" headers
    sections = re.split(r"\n## (q\d+)\n", diff_text)
    # sections[0] is preamble, then alternating qid, body
    for i in range(1, len(sections), 2):
        qid = sections[i]
        body = sections[i + 1]
        # extract block between **ORIGINAL** and **REPHRASED**
        m = re.search(
            r"\*\*ORIGINAL\*\*\n\n(.*?)\n\n\*\*REPHRASED",
            body,
            re.DOTALL,
        )
        if not m:
            continue
        quoted = m.group(1)
        # strip leading "> " from each line
        lines = []
        for ln in quoted.splitlines():
            if ln.startswith("> "):
                lines.append(ln[2:])
            elif ln == ">":
                lines.append("")
            else:
                lines.append(ln)
        originals[qid] = "\n".join(lines)
    return originals


def quote(s: str) -> str:
    return "\n".join("> " + line if line else ">" for line in s.split("\n"))


def main() -> None:
    new = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}
    originals = parse_originals(DIFF_DOC.read_text())

    lines: list[str] = ["# hil_j1 — exec_check rephrase diff (v2)\n\n"]
    # iterate in question.json order
    for qid, nr in new.items():
        if nr.get("type") != "exec_check":
            continue
        orig = originals.get(qid, "<<ORIGINAL not recoverable>>")
        lines.append(f"\n## {qid}\n\n**ORIGINAL**\n\n{quote(orig)}\n\n")
        lines.append(f"**REPHRASED (v2)**\n\n{quote(nr['question'])}\n\n---\n\n")

    DIFF_DOC.parent.mkdir(parents=True, exist_ok=True)
    DIFF_DOC.write_text("".join(lines))
    print(f"OK: diff written → {DIFF_DOC}")


if __name__ == "__main__":
    main()
