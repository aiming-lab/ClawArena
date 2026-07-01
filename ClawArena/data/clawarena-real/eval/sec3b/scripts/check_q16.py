#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "final_submission_signoff.txt")
    if sign is None:
        _finish(["file not found: output/final_submission_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["final_submission_signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    # Recompute: SHA-256 of backtest_result.json bytes + corrective_action_plan.md bytes
    f1 = ws / "output" / "backtest_result.json"
    f2 = ws / "output" / "corrective_action_plan.md"
    if not f1.exists():
        _finish(["cannot verify: output/backtest_result.json missing"])
    if not f2.exists():
        _finish(["cannot verify: output/corrective_action_plan.md missing"])
    # C★ Pre-check: backtest_result.json must have schema_version="1.0" before hash is valid
    bt_data, bt_err = _load_json(f1)
    if bt_err:
        _finish(["backtest_result.json is not valid JSON: " + bt_err])
    sv = bt_data.get("schema_version") if bt_data else None
    if sv is None or str(sv) != "1.0":
        fails.append(
            "backtest_result.json missing/wrong schema_version (found %r, expected '1.0') — "
            "the final hash is computed over the exact file bytes; if backtest_result.json "
            "lacks schema_version, the hash will not match the validator's recomputation" % sv
        )
    # C★ Pre-check: CAP must cite Rule 15c3-5(b) sub-clause (detects q13 drift)
    cap_txt = _read(f2)
    if cap_txt and not re.search(r"15c3-5\s*\(b\)", cap_txt, re.IGNORECASE):
        fails.append(
            "corrective_action_plan.md does not contain '15c3-5(b)' — "
            "the CAP must cite Rule 15c3-5(b) sub-clause before the final hash is computed "
            "(C★ cross-round: if CAP is incomplete, the combined hash will be wrong)"
        )
    combined = f1.read_bytes() + f2.read_bytes()
    digest = hashlib.sha256(combined).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s... != recomputed %s... (hash of backtest_result.json + corrective_action_plan.md)" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
