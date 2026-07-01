#!/usr/bin/env python3
"""verify_rca.py — Produce a RCA_VERIFIED:<sha256> sign-off token for the postmortem RCA.

Usage:
  python tools/verify_rca.py output/rca_summary.json postmortem_template.md

The token is computed as:
  sha256( canonical_rca_json_bytes || postmortem_template_bytes )
where:
  canonical_rca_json = json.dumps(rca, sort_keys=True, ensure_ascii=False), encoded utf-8,
                       with the 'audit_signoff' field removed first.

The 'audit_signoff' field is excluded so the printed token can be written back into that
same field without creating a circular dependency. check_q5.py recomputes the token using
exactly this rule and rejects a mismatch — embed the printed line verbatim into
rca_summary.json's 'audit_signoff' field.

The two arguments may be given in either order; the '.json' file is detected by suffix.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def _split_args(a: str, b: str) -> tuple[Path, Path]:
    """Return (json_path, template_path); detect the JSON file by suffix, order-independent."""
    pa, pb = Path(a), Path(b)
    if pb.suffix.lower() == ".json" and pa.suffix.lower() != ".json":
        return pb, pa
    return pa, pb


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: verify_rca.py <rca_summary.json> <postmortem_template.md>",
            file=sys.stderr,
        )
        return 2

    json_path, pm_path = _split_args(sys.argv[1], sys.argv[2])

    for p in (json_path, pm_path):
        if not p.exists():
            print(f"ERROR: missing input file: {p}", file=sys.stderr)
            return 1

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: {json_path} is not valid JSON: {exc}", file=sys.stderr)
        return 1

    if isinstance(data, dict):
        data = {k: v for k, v in data.items() if k != "audit_signoff"}

    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    pm_bytes = pm_path.read_bytes()

    h = hashlib.sha256()
    h.update(canonical)
    h.update(pm_bytes)
    print(f"RCA_VERIFIED:{h.hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
