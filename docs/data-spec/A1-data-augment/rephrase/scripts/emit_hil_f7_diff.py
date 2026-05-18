"""Emit side-by-side diff doc for hil_f7 exec_check rephrases."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
A = ROOT / "data/clawarena/eval/hil_f7/questions.json"
B = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_f7/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_f7.md"

a = json.loads(A.read_text())
b = json.loads(B.read_text())
by_id_a = {r["id"]: r for r in a["rounds"]}
by_id_b = {r["id"]: r for r in b["rounds"]}

lines = ["# hil_f7 — exec_check rephrase diff (v1 → v2 hardened)\n"]
for qid, ra in by_id_a.items():
    if ra.get("type") != "exec_check":
        continue
    rb = by_id_b[qid]
    lines.append(f"\n## {qid}\n")
    lines.append("**v1 (previous)**\n")
    lines.append("> " + ra["question"].replace("\n", "\n> ") + "\n")
    lines.append("**v2 (hardened)**\n")
    lines.append("> " + rb["question"].replace("\n", "\n> ") + "\n")
    lines.append("---\n")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines))
print(f"OK → {OUT}")
