"""Emit hil_d3 diff (ORIGINAL vs REPHRASED) for every exec_check round."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_d3/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_d3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_d3.md"


def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def main() -> int:
    src = {r["id"]: r for r in json.loads(SRC.read_text())["rounds"]}
    new = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}

    parts = ["# hil_d3 — exec_check rephrase diff (v1)\n\n"]
    for qid, r in src.items():
        if r.get("type") != "exec_check":
            continue
        original = r["question"]
        rephrased = new[qid]["question"]
        parts.append(f"\n## {qid}\n\n")
        parts.append("**ORIGINAL**\n\n")
        parts.append(quote(original) + "\n\n")
        parts.append("**REPHRASED (v1)**\n\n")
        parts.append(quote(rephrased) + "\n\n")
        parts.append("---\n\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(parts))
    print(f"OK: diff written → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
