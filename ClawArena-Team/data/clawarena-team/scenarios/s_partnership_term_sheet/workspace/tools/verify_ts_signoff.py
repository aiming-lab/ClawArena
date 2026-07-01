#!/usr/bin/env python3
"""verify_ts_signoff.py — wave3 compliance verification tool.

Usage:
    python tools/verify_ts_signoff.py output/final_recommendation.md

Reads a Markdown file and checks for required compliance indicators.
Prints COMPLIANCE_CHECK: <32-char hex token> on success.
Exits non-zero on failure.
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: verify_ts_signoff.py <path-to-final_recommendation.md>")
    sys.exit(2)

path = Path(sys.argv[1])
if not path.exists():
    print(f"ERROR: file not found: {path}")
    sys.exit(1)

text = path.read_text(encoding="utf-8", errors="ignore")
low = text.lower()

# Required indicators
errors = []

if not re.search(r"55\s*/\s*45|55%\s*mercator|mercator\s*55%", low):
    errors.append("Missing 55/45 economic split confirmation")

if not re.search(r"5\s*%|5\s*percent|five\s*percent|奖励分成.*5|5.*奖励", low):
    errors.append("Missing 5% performance bonus")

if not re.search(r"first\s*refusal|优先许可|retain|保留|remove|remove per board|删除", low):
    errors.append("Missing IP first refusal action")

if not re.search(r"helios\s*sign|已签署|signed.*helios|helios.*signed", low):
    errors.append("Missing Helios signature confirmation")

# Forbidden: 60/40 as confirmed split (not discredited)
if re.search(r"\b60\s*/\s*40\b", low):
    context_ok = re.search(
        r"(inaccurate|incorrect|false|refute|discredit|decoy|supersede|不正确|已废弃).{0,200}60.{0,50}40"
        r"|60.{0,50}40.{0,200}(inaccurate|incorrect|false|refute|discredit)",
        low
    )
    if not context_ok:
        errors.append("FATAL: 60/40 split present without being discredited — use 55/45")

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)

# Generate deterministic compliance token from file content
token = hashlib.md5(text.encode("utf-8")).hexdigest()
print(f"COMPLIANCE_CHECK: {token}")
sys.exit(0)
