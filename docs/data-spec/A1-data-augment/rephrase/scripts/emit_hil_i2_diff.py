"""Emit side-by-side ORIGINAL vs REPHRASED diff for hil_i2 exec_check rounds."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_i2/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_i2/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_i2.md"


def quote(s: str) -> str:
    return "\n".join("> " + line if line else ">" for line in s.split("\n"))


def main() -> None:
    src = {r["id"]: r for r in json.loads(SRC.read_text())["rounds"]}
    new = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}

    lines: list[str] = ["# hil_i2 — exec_check rephrase diff (v1)\n\n"]
    for qid, sr in src.items():
        if sr.get("type") != "exec_check":
            continue
        nr = new.get(qid, sr)
        lines.append(f"\n## {qid}\n\n**ORIGINAL**\n\n{quote(sr['question'])}\n\n")
        lines.append(f"**REPHRASED (v1)**\n\n{quote(nr['question'])}\n\n---\n\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines))
    print(f"OK: diff written → {OUT}")


if __name__ == "__main__":
    main()
