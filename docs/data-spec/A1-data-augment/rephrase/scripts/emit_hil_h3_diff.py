"""Emit hil_h3 exec_check rephrase diff (ORIGINAL vs REPHRASED) as markdown."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_h3/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_h3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_h3.md"


def quote(s: str) -> str:
    return "\n".join("> " + ln if ln else ">" for ln in s.splitlines())


def main() -> int:
    src_data = json.loads(SRC.read_text())
    new_data = json.loads(NEW.read_text())
    src_by_id = {r["id"]: r for r in src_data["rounds"]}
    new_by_id = {r["id"]: r for r in new_data["rounds"]}

    parts = ["# hil_h3 — exec_check rephrase diff (v2 hardening)\n"]
    for r in src_data["rounds"]:
        if r.get("type") != "exec_check":
            continue
        qid = r["id"]
        orig = src_by_id[qid]["question"]
        new = new_by_id[qid]["question"]
        parts.append(f"\n## {qid}\n")
        parts.append("**v1 (previous)**\n")
        parts.append(quote(orig))
        parts.append("\n**v2 (hardened)**\n")
        parts.append(quote(new))
        parts.append("\n---\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts) + "\n")
    print(f"OK: wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
