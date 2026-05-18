#!/usr/bin/env python3
"""
check_review_assessment.py — 验证 docs/review_quality_assessment.md。

用法：
    python check_review_assessment.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "review_quality_assessment.md"

    # 1. 文件存在且非空
    if not target.exists():
        print(f"FAILED: file does not exist: {target}")
        sys.exit(1)
    try:
        content = target.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)
    if not content:
        print("FAILED: file is empty")
        sys.exit(1)

    # 2. 至少 3 个 "###" 开头的标题
    h3_lines = [ln for ln in content.splitlines() if ln.strip().startswith("###")]
    if len(h3_lines) < 3:
        print(f"FAILED: expected >= 3 '###' headings, found {len(h3_lines)}")
        sys.exit(1)

    # 3. 包含 "15:30" 或 "T15:30"
    if not re.search(r'T?15:30', content):
        print("FAILED: file does not contain '15:30' or 'T15:30'")
        sys.exit(1)

    # 4. 包含 "LGTM"（区分大小写）
    if "LGTM" not in content:
        print("FAILED: file does not contain 'LGTM'")
        sys.exit(1)

    # 5. 包含 "127"
    if "127" not in content:
        print("FAILED: file does not contain '127'")
        sys.exit(1)

    # 6. 同时包含通过标记和未通过标记
    has_pass = bool(re.search(r'✓|通过|pass', content, re.IGNORECASE))
    has_fail = bool(re.search(r'✗|未|fail', content, re.IGNORECASE))
    if not (has_pass and has_fail):
        print(
            "FAILED: file must contain both pass markers (✓/通过/pass) "
            "and fail markers (✗/未/fail)"
        )
        sys.exit(1)

    # 7. 包含 "2026-01-15"
    if "2026-01-15" not in content:
        print("FAILED: file does not contain '2026-01-15'")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
