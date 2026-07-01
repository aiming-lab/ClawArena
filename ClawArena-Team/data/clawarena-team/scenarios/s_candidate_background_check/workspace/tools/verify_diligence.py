#!/usr/bin/env python3
"""verify_diligence.py — Produce SIGNED:<sha256> token for candidate background diligence.

Usage:
    python tools/verify_diligence.py <report_path> <risk_tier> <pip_disclosed>

Arguments:
    report_path   Absolute path to output/diligence_report.md (as written by the agent).
    risk_tier     Risk tier string, e.g. "High".
    pip_disclosed Whether the candidate self-disclosed the PIP, e.g. "false".

Output:
    SIGNED:<sha256hex>

The sha256 is computed by concatenating (no separator):
    bytes(str(report_path)) + bytes(risk_tier) + bytes(pip_disclosed)

Example:
    python tools/verify_diligence.py /path/to/output/diligence_report.md High false
    SIGNED:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
"""
import hashlib
import sys

if len(sys.argv) != 4:
    print(
        "usage: verify_diligence.py <report_path> <risk_tier> <pip_disclosed>",
        file=sys.stderr,
    )
    sys.exit(1)

report_path = sys.argv[1]
risk_tier = sys.argv[2]
pip_disclosed = sys.argv[3]

h = hashlib.sha256()
h.update(report_path.encode())
h.update(risk_tier.encode())
h.update(pip_disclosed.encode())

print(f"SIGNED:{h.hexdigest()}")
