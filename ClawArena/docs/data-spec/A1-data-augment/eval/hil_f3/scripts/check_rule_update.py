#!/usr/bin/env python3
"""
check_rule_update.py — 检查 alert-rules-config.md 及 docs/rule_007_postmortem.md。

用法：
    python check_rule_update.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def find_alert_rules_config(workspace: Path):
    """在 workspace 内查找 alert-rules-config.md（不限层级）。"""
    candidates = sorted(workspace.rglob("alert-rules-config.md"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    # 1. alert-rules-config.md 包含 "2025-12-25"
    config_file = find_alert_rules_config(workspace)
    if config_file is None:
        print("FAILED: alert-rules-config.md not found in workspace")
        sys.exit(1)
    try:
        config_content = config_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {config_file}: {e}")
        sys.exit(1)
    if "2025-12-25" not in config_content:
        print(
            f"FAILED: {config_file} does not contain '2025-12-25' "
            "(rule_007 expiry update)"
        )
        sys.exit(1)

    # 2. docs/rule_007_postmortem.md 存在且非空
    postmortem = workspace / "docs" / "rule_007_postmortem.md"
    if not postmortem.exists():
        print(f"FAILED: file does not exist: {postmortem}")
        sys.exit(1)
    try:
        pm_content = postmortem.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"FAILED: cannot read {postmortem}: {e}")
        sys.exit(1)
    if not pm_content:
        print("FAILED: docs/rule_007_postmortem.md is empty")
        sys.exit(1)

    # 3. postmortem 包含 "7" 或 "七"
    if not re.search(r'\b7\b|七', pm_content):
        print("FAILED: postmortem does not contain '7' (7-day impact)")
        sys.exit(1)

    # 4. postmortem 包含 "5"
    if not re.search(r'\b5\b', pm_content):
        print("FAILED: postmortem does not contain '5' (5 silenced alerts)")
        sys.exit(1)

    # 5. postmortem 包含 "过期" 或 "expires" 或 "null"
    if not re.search(r'过期|expires|null', pm_content, re.IGNORECASE):
        print(
            "FAILED: postmortem does not mention expiry mechanism "
            "('过期'/'expires'/'null')"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
