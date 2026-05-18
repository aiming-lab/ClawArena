"""Emit hil_c7 diff (v1 vs v2) for every exec_check round.

Note: the source questions.json under data/clawarena/eval/hil_c7/ has already
been overwritten with the v1 rephrased text in an earlier pass. So for v2
hardening, this emitter compares v1 (SRC) vs v2 (NEW under rephrased/).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_c7/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_c7/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_c7.md"


def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def main() -> int:
    src = {r["id"]: r for r in json.loads(SRC.read_text())["rounds"]}
    new = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}

    parts = ["# hil_c7 — exec_check rephrase diff (v2 hardening)\n\n"]
    for qid, r in src.items():
        if r.get("type") != "exec_check":
            continue
        v1 = r["question"]
        v2 = new[qid]["question"]
        parts.append(f"\n## {qid}\n\n")
        parts.append("**V1 (prior rephrase, now baseline)**\n\n")
        parts.append(quote(v1) + "\n\n")
        parts.append("**V2 (hardened)**\n\n")
        parts.append(quote(v2) + "\n\n")
        parts.append("---\n\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(parts))
    print(f"OK: diff written → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
