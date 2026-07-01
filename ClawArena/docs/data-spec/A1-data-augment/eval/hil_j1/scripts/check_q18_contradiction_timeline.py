#!/usr/bin/env python3
"""
check_q18_contradiction_timeline.py — Verify q18 outputs (M1+M3):
  1. analysis/矛盾演化时间线.md — C1-C4 nodes, '内部估算', >= 4 headings
  2. analysis/矛盾注册.json — 4 objects, all favors_fraud_claim == true
"""
import sys
import json
from pathlib import Path


def check_md(workspace: Path):
    target = workspace / "analysis" / "矛盾演化时间线.md"
    if not target.exists():
        return ["analysis/矛盾演化时间线.md not found"]
    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        return [f"cannot read analysis/矛盾演化时间线.md: {e}"]

    errors = []

    # Must contain all four contradiction nodes (C1-C4 or equivalent descriptions)
    # Check for explicit labels or equivalent descriptions
    c_labels = ["C1", "C2", "C3", "C4"]
    alt_keywords = [
        ["MCN报告", "官方后台", "数据差异", "夸大"],  # C1
        ["口径", "API", "官方文档"],                   # C2
        ["内部估算", "承认"],                            # C3
        ["合同", "截图", "verified"],                   # C4
    ]

    # If explicit C1-C4 labels exist, check for them
    has_labels = all(label in content for label in c_labels)
    if not has_labels:
        # Check for alternative descriptions
        missing = []
        for i, alts in enumerate(alt_keywords):
            if not any(kw in content for kw in alts):
                missing.append(f"C{i+1} equivalent (expected one of: {alts})")
        if missing:
            for m in missing:
                errors.append(f"MD: contradiction node {m}")

    # Must contain '内部估算'
    if "内部估算" not in content:
        errors.append("MD: '内部估算' not found (required admission reference)")

    # Check heading count >= 4
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(f"MD: '##' headings: {len(headings)} (expected >= 4)")

    return errors


def check_json(workspace: Path):
    target = workspace / "analysis" / "矛盾注册.json"
    if not target.exists():
        return ["analysis/矛盾注册.json not found"]
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"analysis/矛盾注册.json parse error: {e}"]

    errors = []

    if not isinstance(data, list):
        return ["JSON: expected array at top level"]

    if len(data) != 4:
        errors.append(f"JSON: array length expected 4, got {len(data)}")
        return errors

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"JSON: element {i} is not an object")
            continue
        if item.get("favors_fraud_claim") is not True:
            errors.append(
                f"JSON: element {i} favors_fraud_claim expected true, got {item.get('favors_fraud_claim')!r}"
            )

    return errors


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    if not workspace.exists():
        print(f"FAILED: workspace path does not exist: {workspace}")
        sys.exit(1)

    errors = []
    errors.extend(check_md(workspace))
    errors.extend(check_json(workspace))

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
