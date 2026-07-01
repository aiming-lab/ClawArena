"""check_q5.py — Wave3 s_oss_supply_chain_audit q5 checker.

Verifies output/security_report.md (C dimension — real test execution):
1. cargo failing test name: test_path_traversal_guard
2. cargo failing line: lib.rs:113
3. npm failing test name: test_input_sanitizer
4. npm failing line: sanitizer.test.js:47
5. ≥ 3 action items (pin lib-tinypath / drop colorz / coverage gate)
6. FAIL appears in the tail of the report (test output pasted)

No sha compliance token required (wave3 q5 spec: NOT signing sha).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "security_report.md"
    if not out.exists():
        print("FAIL: output/security_report.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. cargo failing test name
    if not re.search(r"test_path_traversal_guard", text):
        print(
            "FAIL: 'test_path_traversal_guard' not found in security_report.md. "
            "Run `bash tools/run_cargo_tests.sh` and look for the failing test name."
        )
        return 1

    # 2. cargo failing line
    if not re.search(r"lib\.rs:113", text):
        print(
            "FAIL: 'lib.rs:113' not found in security_report.md. "
            "Run `bash tools/run_cargo_tests.sh` and look for the file:line in the output."
        )
        return 1

    # 3. npm failing test name
    if not re.search(r"test_input_sanitizer", text):
        print(
            "FAIL: 'test_input_sanitizer' not found in security_report.md. "
            "Run `bash tools/run_npm_tests.sh` and look for the failing test name."
        )
        return 1

    # 4. npm failing line
    if not re.search(r"sanitizer\.test\.js:47", text):
        print(
            "FAIL: 'sanitizer.test.js:47' not found in security_report.md. "
            "Run `bash tools/run_npm_tests.sh` and look for the file:line in the output."
        )
        return 1

    # 5. ≥ 3 action items
    action_patterns = [
        r"pin.{0,50}1\.4\.1|1\.4\.1.{0,30}pin|pin.{0,30}lib.tinypath",
        r"(drop|remove|exclude|eliminate).{0,40}colorz|colorz.{0,30}(drop|remove)",
        r"(coverage|test\s+coverage).{0,50}(80|≥\s*80|gate)|coverage.gate",
        r"(block|halt|prevent).{0,30}release|release.{0,30}block",
        r"(action\s+item|action\s+\d+|AI-\d+)",
        r"upgrade.{0,40}1\.4\.1",
    ]
    hits = [p for p in action_patterns if re.search(p, text, re.IGNORECASE)]
    if len(hits) < 3:
        print(
            f"FAIL: only {len(hits)} action item topic(s) found (need ≥ 3). "
            "Required: pin lib-tinypath to 1.4.1, drop colorz typosquat, "
            "require ≥80% test coverage."
        )
        return 1

    # 6. FAIL in the tail of the report (last 40 lines)
    lines = text.splitlines()
    tail = lines[-40:] if len(lines) >= 40 else lines
    tail_text = "\n".join(tail)
    if not re.search(r"^\s*FAIL\b", tail_text, re.MULTILINE):
        print(
            "FAIL: 'FAIL' not found in the last ~40 lines of security_report.md. "
            "The agent must paste the last 5 lines of both test outputs at the end "
            "of the report. Both cargo and npm test suites produce a FAIL line."
        )
        return 1

    print(
        f"PASS: security_report.md has test_path_traversal_guard + lib.rs:113 + "
        f"test_input_sanitizer + sanitizer.test.js:47 + {len(hits)} action items + FAIL in tail"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
