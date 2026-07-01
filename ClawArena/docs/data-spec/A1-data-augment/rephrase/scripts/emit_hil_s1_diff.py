"""Emit side-by-side diff doc for hil_s1 exec_check rephrases."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
A = ROOT / "data/clawarena/eval/hil_s1/questions.json"
B = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_s1/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/diff/hil_s1.md"

a = json.loads(A.read_text())
b = json.loads(B.read_text())
by_id_a = {r["id"]: r for r in a["rounds"]}
by_id_b = {r["id"]: r for r in b["rounds"]}

lines = ["# hil_s1 — exec_check rephrase diff (v1)\n"]
for qid, ra in by_id_a.items():
    if ra.get("type") != "exec_check":
        continue
    rb = by_id_b[qid]
    lines.append(f"\n## {qid}\n")
    lines.append("**ORIGINAL**\n")
    lines.append("> " + ra["question"].replace("\n", "\n> ") + "\n")
    lines.append("**REPHRASED (v1)**\n")
    lines.append("> " + rb["question"].replace("\n", "\n> ") + "\n")
    lines.append("---\n")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines))
print(f"OK → {OUT}")
