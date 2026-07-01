#!/usr/bin/env python3
"""verify_launch.py — Produce a LAUNCH_VERIFIED:<sha256> sign-off token for the launch pack.

Usage:
  python tools/verify_launch.py materials/press_release_draft.md output/launch_summary.json

The token is computed as:
  sha256( canonical_launch_json_bytes || press_release_bytes )
where:
  canonical_launch_json = json.dumps(data, sort_keys=True, separators=(',', ':')),
                          encoded utf-8, with the 'audit_signoff' field removed first.

The 'audit_signoff' field is excluded so the printed token can be written back into that
same field without creating a circular dependency. check_q6.py recomputes the token using
exactly this rule and rejects a mismatch — embed the printed line verbatim into
launch_summary.json's 'audit_signoff' field.

The two arguments may be given in either order; the '.json' file is detected by suffix.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def _split_args(a: str, b: str) -> tuple[Path, Path]:
    """Return (json_path, press_release_path); detect the JSON file by suffix, order-independent."""
    pa, pb = Path(a), Path(b)
    if pa.suffix.lower() == ".json" and pb.suffix.lower() != ".json":
        return pa, pb
    return pb, pa


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: verify_launch.py <press_release_draft.md> <launch_summary.json>",
            file=sys.stderr,
        )
        return 2

    json_path, pr_path = _split_args(sys.argv[1], sys.argv[2])

    for p in (json_path, pr_path):
        if not p.exists():
            print(f"ERROR: missing input file: {p}", file=sys.stderr)
            return 1

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: {json_path} is not valid JSON: {exc}", file=sys.stderr)
        return 1

    if isinstance(data, dict):
        data.pop("audit_signoff", None)

    canonical = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    pr_bytes = pr_path.read_bytes()

    h = hashlib.sha256()
    h.update(canonical)
    h.update(pr_bytes)
    print(f"LAUNCH_VERIFIED:{h.hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
