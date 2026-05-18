"""Emit a side-by-side diff for hil_g3 exec_check rephrases."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ORIG = ROOT / "data/clawarena/eval/hil_g3/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_g3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_g3.md"


def quote(s: str) -> str:
    return "\n".join("> " + line if line else ">" for line in s.split("\n"))


def main() -> None:
    o = {r["id"]: r for r in json.loads(ORIG.read_text())["rounds"]}
    n = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}
    parts = ["# hil_g3 — exec_check rephrase diff (v1)\n"]
    for qid, r in n.items():
        if r.get("type") != "exec_check":
            continue
        if o[qid]["question"] == r["question"]:
            continue
        parts.append(f"\n## {qid}\n")
        parts.append("\n**ORIGINAL**\n")
        parts.append(quote(o[qid]["question"]) + "\n")
        parts.append("\n**REPHRASED (v1)**\n")
        parts.append(quote(r["question"]) + "\n")
        parts.append("\n---\n")
    OUT.write_text("\n".join(parts) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
