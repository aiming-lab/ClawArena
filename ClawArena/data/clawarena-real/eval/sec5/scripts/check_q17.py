#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
from pathlib import Path
from datetime import date, timedelta

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
    sign_path = ws / "output" / "q17_signoff.txt"
    if not sign_path.exists():
        _finish(["file not found: output/q17_signoff.txt"])

    content = sign_path.read_text(encoding="utf-8").strip()

    if not content.startswith("VERIFIED:"):
        fails.append(f"q17_signoff.txt must start with 'VERIFIED:' (got {content[:30]!r})")
        _finish(fails)

    hexpart = content[len("VERIFIED:"):].strip()
    if not re.fullmatch(r"[0-9a-f]{64}", hexpart):
        fails.append(f"SHA-256 portion is not 64 lowercase hex chars: {hexpart!r}")
        _finish(fails)

    script_path = ws / "scripts" / "compute_vamp_ratio.py"
    if not script_path.exists():
        fails.append("scripts/compute_vamp_ratio.py not found — cannot verify hash")
        _finish(fails)

    try:
        result = subprocess.run(
            ["python", str(script_path), "--tc40", "42", "--tc15", "18", "--tc05", "3800",
             "--merchant-id", "MERCH-A"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            fails.append(f"compute_vamp_ratio.py exited {result.returncode}: {result.stderr[:200]}")
            _finish(fails)
        script_output = result.stdout
        script_output_stripped = script_output.rstrip("\n")
        expected_hash = hashlib.sha256(script_output_stripped.encode("utf-8")).hexdigest()
        if hexpart.lower() != expected_hash.lower():
            expected_hash2 = hashlib.sha256(script_output.encode("utf-8")).hexdigest()
            if hexpart.lower() != expected_hash2.lower():
                fails.append(
                    f"SHA-256 mismatch: got {hexpart[:16]}... expected {expected_hash[:16]}... "
                    f"(hash of compute_vamp_ratio.py output with TC40=42/TC15=18/TC05=3800)"
                )
    except subprocess.TimeoutExpired:
        fails.append("compute_vamp_ratio.py timed out (>15s)")
    except Exception as e:
        fails.append(f"error running compute_vamp_ratio.py: {e}")

    _finish(fails)
main()
