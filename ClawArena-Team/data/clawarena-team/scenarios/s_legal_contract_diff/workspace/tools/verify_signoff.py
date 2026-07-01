#!/usr/bin/env python3
"""verify_signoff.py — emit a COMPLIANCE_CHECK token for a sign-off cover sheet.

Usage:
    python tools/verify_signoff.py output/signoff_cover.md

The token is a sha256 of the cover sheet's normalised content. The check
script will look for this token in the partner email and verify the same
hash, so the model cannot fabricate it.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def normalise(text: str) -> str:
    # 折叠空白；去除前后空格；统一换行
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_signoff.py <signoff_cover.md>", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"signoff cover sheet not found: {p}", file=sys.stderr)
        return 2
    content = p.read_text(encoding="utf-8")
    # 关键字段必须出现，否则拒签
    required_substrings = [
        "v3",
        "v4",
        "Mercator",
        "GoldenLeaf",
    ]
    missing = [s for s in required_substrings if s.lower() not in content.lower()]
    if missing:
        print(f"signoff cover sheet missing required substrings: {missing}",
              file=sys.stderr)
        return 2
    digest = hashlib.sha256(normalise(content).encode("utf-8")).hexdigest()[:32]
    print(f"COMPLIANCE_CHECK: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
