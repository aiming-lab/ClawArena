#!/usr/bin/env python3
"""
check_q22_case_strength.py — Verify q22 outputs (M3+M4):
  1. analysis/四重矛盾总结.md — four contradictions, >= 4 headings
  2. analysis/case_strength.json — allegations_supported==4,
     abs(data_manipulation_ratio-2.386)<0.01,
     recommended_action=="legal_proceedings"
"""
import sys
import json
from pathlib import Path


def check_md(workspace: Path):
    target = workspace / "analysis" / "四重矛盾总结.md"
    if not target.exists():
        return ["analysis/四重矛盾总结.md not found"]
    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        return [f"cannot read analysis/四重矛盾总结.md: {e}"]

    errors = []

    # Check four contradictions appear
    # Use broad keywords for each of the 4 expected contradictions
    contradiction_keywords = [
        ["数据差异", "夸大", "MCN报告", "官方"],      # C1: data mismatch
        ["口径", "API", "官方文档", "全渠道"],          # C2: caliber vs API
        ["内部估算", "承认", "估算"],                   # C3: admission
        ["合同", "截图", "verified", "违约"],           # C4: contract breach
    ]
    for i, keywords in enumerate(contradiction_keywords):
        if not any(kw in content for kw in keywords):
            errors.append(
                f"MD: contradiction {i+1} not found (expected one of: {keywords})"
            )

    # Check heading count >= 4
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(f"MD: '##' headings: {len(headings)} (expected >= 4)")

    return errors


def check_json(workspace: Path):
    target = workspace / "analysis" / "case_strength.json"
    if not target.exists():
        return ["analysis/case_strength.json not found"]
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"analysis/case_strength.json parse error: {e}"]

    errors = []

    if data.get("allegations_supported") != 4:
        errors.append(
            f"JSON: allegations_supported expected 4, got {data.get('allegations_supported')}"
        )

    ratio = data.get("data_manipulation_ratio", 0)
    try:
        ratio_f = float(ratio)
        if abs(ratio_f - 2.386) > 0.01:
            errors.append(
                f"JSON: data_manipulation_ratio expected ~2.386 (±0.01), got {ratio_f}"
            )
    except (TypeError, ValueError):
        errors.append(f"JSON: data_manipulation_ratio is not a number: {ratio!r}")

    if data.get("recommended_action") != "legal_proceedings":
        errors.append(
            f"JSON: recommended_action expected 'legal_proceedings', got {data.get('recommended_action')!r}"
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
