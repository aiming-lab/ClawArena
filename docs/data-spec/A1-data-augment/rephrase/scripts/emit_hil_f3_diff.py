"""Emit side-by-side ORIGINAL vs REPHRASED diff for hil_f3 exec_check rounds."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_f3/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_f3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_f3.md"


def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def main() -> None:
    src = {r["id"]: r for r in json.loads(SRC.read_text())["rounds"]}
    new = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}

    parts = ["# hil_f3 — exec_check rephrase diff (v1)\n"]
    for qid, r in src.items():
        if r.get("type") != "exec_check":
            continue
        orig = r["question"]
        rep = new[qid]["question"]
        if orig == rep:
            continue
        parts.append(f"\n## {qid}\n")
        parts.append("\n**ORIGINAL**\n\n" + quote(orig) + "\n")
        parts.append("\n**REPHRASED (v1)**\n\n" + quote(rep) + "\n")
        parts.append("\n---\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts) + "\n")
    print(f"OK: diff written → {OUT}")


if __name__ == "__main__":
    main()
