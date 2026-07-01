#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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

import subprocess

def main():
    ws = Path(sys.argv[1]); fails = []
    script = ws / "scripts" / "power_analysis_fixed.py"
    if not script.exists():
        _finish(["file not found: scripts/power_analysis_fixed.py"])
    txt = script.read_text(encoding="utf-8")
    # Check correct z values present
    if "1.96" not in txt:
        fails.append("script does not contain z_alpha/2 = 1.96 (for alpha=0.05 two-sided)")
    if "0.84" not in txt:
        fails.append("script does not contain z_beta = 0.84 (for power=0.80)")
    # Verify it does NOT use the wrong deprecated values
    # 2.33 or 2.576 would indicate deprecated runbook usage
    if re.search(r"z[_a-z]*\s*=\s*2\.33", txt) or re.search(r"z[_a-z]*\s*=\s*2\.576", txt):
        fails.append("script contains deprecated z-value (2.33 or 2.576 from old runbook) — must use 1.96")
    if fails: _finish(fails)
    # Execute script and capture output to verify n≈1764 for p1=0.10, p2=0.12
    try:
        result = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        # Correct two-proportion per-group sample size for p1=.10,p2=.12 is ~3834
        nums = re.findall(r"\b(3[0-9]{3})\b", output)
        found_valid = any(3800 <= int(n) <= 3870 for n in nums)
        if not found_valid:
            fails.append(
                "script output does not contain n in [3800,3870] for p1=0.10,p2=0.12 "
                "(got numbers: %s; output: %r)" % (nums[:5], output[:200])
            )
    except subprocess.TimeoutExpired:
        fails.append("script timed out (>30s)")
    except Exception as e:
        fails.append("script execution error: %s" % e)
    _finish(fails)
main()
