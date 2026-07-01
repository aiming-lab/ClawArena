"""Extract per-question pass/fail map from a rephrase run.

Usage:
    python3 extract_per_q_pass.py <infer-dir>

<infer-dir> is the openclaw inference output, typically
results/<run-name>/openclaw/infer/, produced by
`clawarena infer --framework openclaw --out results/<run-name>`.

Output: per-task summary with separate ec / mc fail lines.
"""
import json
import os
import sys
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("Usage: extract_per_q_pass.py <path-to-openclaw-infer-dir>")
ROOT = Path(sys.argv[1])

tasks = sorted(d for d in os.listdir(ROOT) if d.startswith("hil_"))
for task in tasks:
    rounds = sorted((ROOT / task).iterdir(), key=lambda p: int(p.name[1:]))
    line_pass = []
    line_fail = []
    for r in rounds:
        ir = r / "infer_result.json"
        if not ir.exists():
            continue
        d = json.loads(ir.read_text())
        meta = d.get("meta", {})
        qtype = meta.get("question_type")
        sc = d.get("inline_score") or {}
        passed = sc.get("passed")
        token = f"{r.name}({qtype[:2]})"  # ec or mc
        if passed is True:
            line_pass.append(token)
        elif passed is False:
            line_fail.append(token)
    n_total = len(line_pass) + len(line_fail)
    n_fail = len(line_fail)
    print(f"\n== {task}  ({n_total} rounds, {n_fail} failed) ==")
    if line_fail:
        # group by type
        ec_fail = [t for t in line_fail if "(ex" in t]
        mc_fail = [t for t in line_fail if "(mu" in t]
        if ec_fail:
            print(f"  ec fail ({len(ec_fail)}): {' '.join(t[:-4] for t in ec_fail)}")
        if mc_fail:
            print(f"  mc fail ({len(mc_fail)}): {' '.join(t[:-4] for t in mc_fail)}")
