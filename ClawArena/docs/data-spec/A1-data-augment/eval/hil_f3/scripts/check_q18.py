#!/usr/bin/env python3
"""
check_q18.py -- Verify analysis/four_contradiction_matrix.md and analysis/contradiction_data.json (M3).

Usage:
    python check_q18.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: analysis/four_contradiction_matrix.md ---
    md_path = workspace / "analysis" / "four_contradiction_matrix.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # All 4 contradictions must be present (C1, C2, C3, C4 or their descriptions)
            has_c1 = bool(re.search(r'C1|CI.{0,30}pass|34.{0,10}test', content, re.IGNORECASE))
            has_c2 = bool(re.search(r'C2|rule_007.{0,30}temporary|expires.{0,30}null|null.{0,30}expires', content, re.IGNORECASE))
            has_c3 = bool(re.search(r'C3|LGTM.{0,30}DST|DST.{0,30}LGTM|didn.t.{0,20}think|knowledge.{0,20}gap', content, re.IGNORECASE))
            has_c4 = bool(re.search(r'C4|syntactic|semantic|appears.{0,20}correct|correct.{0,20}syntactic', content, re.IGNORECASE))

            if not has_c1:
                errors.append("FAILED: four_contradiction_matrix.md missing C1 (CI pass vs production violation)")
            if not has_c2:
                errors.append("FAILED: four_contradiction_matrix.md missing C2 (rule_007 temporary vs expires=null)")
            if not has_c3:
                errors.append("FAILED: four_contradiction_matrix.md missing C3 (LGTM vs DST knowledge gap)")
            if not has_c4:
                errors.append("FAILED: four_contradiction_matrix.md missing C4 (syntactically correct vs semantically wrong during DST)")

            # Must mention rule_007 and expires
            if "rule_007" not in content:
                errors.append("FAILED: four_contradiction_matrix.md does not mention 'rule_007'")
            if "expires" not in content.lower():
                errors.append("FAILED: four_contradiction_matrix.md does not mention 'expires'")

            # Must have >= 4 ## headings
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 4:
                errors.append(f"FAILED: four_contradiction_matrix.md has only {len(headings)} ## headings (need >= 4)")

    # --- File 2: analysis/contradiction_data.json ---
    json_path = workspace / "analysis" / "contradiction_data.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = []

        if data:
            if not isinstance(data, list):
                errors.append("FAILED: contradiction_data.json must be a JSON array")
            elif len(data) != 4:
                errors.append(f"FAILED: contradiction_data.json must have exactly 4 objects, got {len(data)}")
            else:
                for i, item in enumerate(data):
                    if item.get("resolved") is not True:
                        errors.append(f"FAILED: contradiction_data.json item {i} has resolved != true (got {item.get('resolved')!r})")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
