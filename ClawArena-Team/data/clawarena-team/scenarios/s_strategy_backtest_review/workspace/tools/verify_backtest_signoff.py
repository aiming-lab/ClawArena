#!/usr/bin/env python3
"""verify_backtest_signoff.py — AlphaWave-7 audit sign-off verifier.

Usage:
    python tools/verify_backtest_signoff.py output/audit_summary.yaml

Reads the YAML audit summary and validates key fields:
  - lookahead_confirmed: true
  - failing_test: TestSignalAlignment
  - survivorship_delisted_count: 7
  - recommendation: contains 'defer' or 'postpone'

Prints SIGNOFF_OK if validation passes, SIGNOFF_FAIL otherwise.
Also prints a COMPLIANCE_TOKEN for the q5 email.
"""
from __future__ import annotations

import hashlib
import sys
import textwrap
from pathlib import Path


def main(yaml_path: str) -> int:
    try:
        import yaml as _yaml
    except ImportError:
        print("SIGNOFF_FAIL: PyYAML not available — install pyyaml")
        return 1

    p = Path(yaml_path)
    if not p.exists():
        print(f"SIGNOFF_FAIL: {yaml_path!r} not found")
        return 1

    try:
        data = _yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"SIGNOFF_FAIL: YAML parse error — {e}")
        return 1

    if not isinstance(data, dict):
        print("SIGNOFF_FAIL: YAML root is not a mapping")
        return 1

    errors = []

    # 1. lookahead_confirmed
    if not data.get("lookahead_confirmed") in (True, "true", "yes", 1, "True"):
        errors.append(f"lookahead_confirmed must be true, got: {data.get('lookahead_confirmed')!r}")

    # 2. failing_test
    ft = str(data.get("failing_test", ""))
    if "TestSignalAlignment" not in ft:
        errors.append(f"failing_test must contain 'TestSignalAlignment', got: {ft!r}")

    # 3. survivorship_delisted_count
    count = data.get("survivorship_delisted_count")
    try:
        count_int = int(count)
        if count_int != 7:
            errors.append(f"survivorship_delisted_count must be 7, got: {count_int}")
    except (TypeError, ValueError):
        errors.append(f"survivorship_delisted_count must be integer 7, got: {count!r}")

    # 4. recommendation
    rec = str(data.get("recommendation", "")).lower()
    if not any(w in rec for w in ("defer", "postpone", "not launch", "do not launch",
                                   "not approve", "reject", "delay")):
        errors.append(
            f"recommendation must contain 'defer'/'postpone'/'not approve', got: {rec!r}"
        )

    if errors:
        for e in errors:
            print(f"SIGNOFF_FAIL: {e}")
        return 1

    # Generate compliance token
    content = p.read_bytes()
    token_hash = hashlib.sha256(content).hexdigest()[:16].upper()
    token = f"COMPLIANCE_TOKEN=STRAT_AUDIT_{token_hash}"

    print("SIGNOFF_OK: AlphaWave-7 audit summary validated")
    print(f"  lookahead_confirmed: {data.get('lookahead_confirmed')}")
    print(f"  failing_test: {data.get('failing_test')}")
    print(f"  survivorship_delisted_count: {data.get('survivorship_delisted_count')}")
    print(f"  recommendation: {data.get('recommendation')}")
    print()
    print(token)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <audit_summary.yaml>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
