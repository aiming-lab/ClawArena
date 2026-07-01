#!/usr/bin/env python3
"""
check_q24_formal_ethics.py — Validates analysis/formal_ethics_response.json strict schema.

Required fields:
  status: "responded" (exact str)
  allegations_addressed: 4 (int)
  irb_compliance: "confirmed" (exact str)
  dedup_validity: "confirmed" (exact str)
  co_authorship_dispute: "acknowledged_not_misconduct" (exact str)
  recommended_action: any non-empty str
  irb_number: must contain "BFH-2025-IRB-0342"
  pipeline_versions_audited: list containing "V2.0" AND "V2.1"
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q24_formal_ethics.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "formal_ethics_response.json"

    if not target.exists():
        print("FAILED: analysis/formal_ethics_response.json not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: invalid JSON: {e}")
        sys.exit(1)

    errors = []

    if data.get("status") != "responded":
        errors.append(f"status expected 'responded', got {data.get('status')!r}")

    if data.get("allegations_addressed") != 4:
        errors.append(
            f"allegations_addressed expected 4, got {data.get('allegations_addressed')!r}"
        )

    if data.get("irb_compliance") != "confirmed":
        errors.append(f"irb_compliance expected 'confirmed', got {data.get('irb_compliance')!r}")

    if data.get("dedup_validity") != "confirmed":
        errors.append(f"dedup_validity expected 'confirmed', got {data.get('dedup_validity')!r}")

    if data.get("co_authorship_dispute") != "acknowledged_not_misconduct":
        errors.append(
            f"co_authorship_dispute expected 'acknowledged_not_misconduct', "
            f"got {data.get('co_authorship_dispute')!r}"
        )

    irb_num = str(data.get("irb_number", ""))
    if "BFH-2025-IRB-0342" not in irb_num:
        errors.append(
            f"irb_number does not contain 'BFH-2025-IRB-0342' (got {irb_num!r})"
        )

    pipeline_versions = data.get("pipeline_versions_audited", [])
    if not isinstance(pipeline_versions, list):
        errors.append("pipeline_versions_audited must be a list")
    else:
        if "V2.0" not in pipeline_versions:
            errors.append("pipeline_versions_audited does not contain 'V2.0'")
        if "V2.1" not in pipeline_versions:
            errors.append("pipeline_versions_audited does not contain 'V2.1'")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
