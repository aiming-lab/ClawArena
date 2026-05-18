#!/usr/bin/env python3
"""
check_q23.py -- Verify analysis/complete_evidence_chain.json.

Usage:
    python check_q23.py <workspace_path>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "complete_evidence_chain.json"
    if not json_path.exists():
        print("FAILED: analysis/complete_evidence_chain.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/complete_evidence_chain.json: {e}")
        sys.exit(1)

    # Check top-level keys
    required_keys = ["fraud_evidence", "seller_claims", "conclusion"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        errors.append(f"FAILED: missing top-level keys: {missing}")
        for e in errors:
            print(e)
        sys.exit(1)

    # Check fraud_evidence
    fraud_ev = data.get("fraud_evidence", [])
    if not isinstance(fraud_ev, list) or len(fraud_ev) < 4:
        errors.append(
            f"FAILED: fraud_evidence must be a list with >= 4 entries, "
            f"got {len(fraud_ev) if isinstance(fraud_ev, list) else type(fraud_ev)}"
        )
    else:
        valid_reliability = {"high", "medium", "low"}
        for i, entry in enumerate(fraud_ev):
            if not isinstance(entry, dict):
                errors.append(f"FAILED: fraud_evidence[{i}] is not an object")
                continue
            for field in ["source_file", "evidence_type", "reliability", "key_finding"]:
                if field not in entry:
                    errors.append(f"FAILED: fraud_evidence[{i}] missing field '{field}'")
            if "reliability" in entry and entry["reliability"] not in valid_reliability:
                errors.append(
                    f"FAILED: fraud_evidence[{i}].reliability must be one of {valid_reliability}, "
                    f"got {entry['reliability']!r}"
                )

        # At least one entry must cite courier-evidence.md
        sources = [e.get("source_file", "") for e in fraud_ev if isinstance(e, dict)]
        if not any("courier" in s.lower() for s in sources):
            errors.append(
                "FAILED: no fraud_evidence entry cites 'courier-evidence.md' — "
                "courier evidence is required at Phase 3"
            )

    # Check seller_claims
    seller_claims = data.get("seller_claims", [])
    if not isinstance(seller_claims, list) or len(seller_claims) < 2:
        errors.append(
            f"FAILED: seller_claims must be a list with >= 2 entries, "
            f"got {len(seller_claims) if isinstance(seller_claims, list) else type(seller_claims)}"
        )
    else:
        for i, claim in enumerate(seller_claims):
            if not isinstance(claim, dict):
                errors.append(f"FAILED: seller_claims[{i}] is not an object")
                continue
            if "supported_by_evidence" not in claim:
                errors.append(f"FAILED: seller_claims[{i}] missing 'supported_by_evidence' field")
            elif claim["supported_by_evidence"] is not False:
                errors.append(
                    f"FAILED: seller_claims[{i}].supported_by_evidence must be false, "
                    f"got {claim['supported_by_evidence']!r}"
                )

    # Check conclusion
    if not isinstance(data.get("conclusion"), str) or not data["conclusion"].strip():
        errors.append("FAILED: 'conclusion' must be a non-empty string")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
