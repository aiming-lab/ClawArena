#!/usr/bin/env python3
"""verify_renewal.py — Produce SIGNED:<sha256> token for the MCN creator contract renewal.

Usage:
    python tools/verify_renewal.py <backend_export_path> <vlog_transcript_path>

The sha256 is computed by concatenating (no separator):
    bytes(str(backend_export_path)) + bytes(str(vlog_transcript_path))

Canonical inputs:
  1. backend_export_path  — path to platform_data/mcn_backend_export.json
  2. vlog_transcript_path — path to vlog_archive/lin_vlog_20251108_transcript.md

Example:
    python tools/verify_renewal.py \
        platform_data/mcn_backend_export.json \
        vlog_archive/lin_vlog_20251108_transcript.md

The check_q5 verifier recomputes the token using absolute workspace paths:
    ws / "platform_data" / "mcn_backend_export.json"
    ws / "vlog_archive" / "lin_vlog_20251108_transcript.md"
Ensure you pass the same path strings to reproduce the token.
"""
import hashlib
import sys

if len(sys.argv) != 3:
    print(
        "usage: verify_renewal.py <backend_export_path> <vlog_transcript_path>",
        file=sys.stderr,
    )
    sys.exit(1)

backend_path: str = sys.argv[1]
transcript_path: str = sys.argv[2]

h = hashlib.sha256()
h.update(backend_path.encode())
h.update(transcript_path.encode())
print(f"SIGNED:{h.hexdigest()}")
