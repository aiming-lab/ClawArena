"""Emit side-by-side ORIGINAL vs REPHRASED markdown diff for hil_e4."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_e4/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_e4/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_e4.md"


def quote(text: str) -> str:
    return "\n".join("> " + ln if ln else ">" for ln in text.splitlines())


def main() -> None:
    src = {r["id"]: r for r in json.loads(SRC.read_text())["rounds"]}
    new = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}

    lines = ["# hil_e4 — exec_check rephrase diff (v1)", ""]
    for qid, r in src.items():
        if r.get("type") != "exec_check":
            continue
        if src[qid]["question"] == new[qid]["question"]:
            continue
        lines.append(f"\n## {qid}\n")
        lines.append("**ORIGINAL**\n")
        lines.append(quote(src[qid]["question"]))
        lines.append("\n**REPHRASED (v1)**\n")
        lines.append(quote(new[qid]["question"]))
        lines.append("\n---\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
