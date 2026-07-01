"""Emit hil_g1 diff (V1 vs V2 hardened) for every exec_check round.

Note: SRC (`data/clawarena/eval/hil_g1/questions.json`) was overwritten with v1
during the v1 pass, so SRC == V1. NEW is the v2 hardened output. The original
pre-v1 prompts live in `data-augment/rephrase/diff/hil_g1.md` (the v1 diff).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_g1/questions.json"
NEW = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_g1/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_g1.md"


def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def main() -> int:
    src = {r["id"]: r for r in json.loads(SRC.read_text())["rounds"]}
    new = {r["id"]: r for r in json.loads(NEW.read_text())["rounds"]}

    parts = [
        "# hil_g1 — exec_check rephrase diff (v2 hardened)\n\n"
        "Shows V1 (already in SRC since v1 was applied to disk) vs V2 hardened "
        "rephrase. The original pre-v1 text is preserved in the v1 commit "
        "history of this file; v2 changes target the v1 baseline.\n\n"
    ]
    for qid, r in src.items():
        if r.get("type") != "exec_check":
            continue
        v1 = r["question"]
        v2 = new[qid]["question"]
        parts.append(f"\n## {qid}\n\n")
        parts.append("**V1 (previous)**\n\n")
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
