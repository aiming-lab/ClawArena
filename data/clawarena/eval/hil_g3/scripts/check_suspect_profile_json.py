#!/usr/bin/env python3
"""check_suspect_profile_json.py — Validates analysis/suspect_profile.json for q13."""
import sys
import json
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "suspect_profile.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    if not isinstance(data, dict):
        print("FAILED: suspect_profile.json must be a JSON object")
        sys.exit(1)

    # Required top-level fields and types
    required_fields = {
        "suspect": str,
        "download_confirmed": bool,
        "download_version": str,
        "download_timestamp": str,
        "download_size_mb": (int, float),
        "email_sent": bool,
        "email_recipient": str,
        "email_timestamp": str,
        "email_attachment_size_mb": (int, float),
        "delta_seconds": int,
        "data_exposed_employees": list,
        "defense_claims": list,
        "it_report_exoneration_scope": str,
        "hash_match_confirmed": bool,
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            errors.append(f"Missing required field '{field}'")
        else:
            val = data[field]
            if isinstance(expected_type, tuple):
                if not isinstance(val, expected_type):
                    errors.append(
                        f"Field '{field}' must be numeric, got {type(val).__name__}"
                    )
            elif not isinstance(val, expected_type):
                # bool is subclass of int, handle carefully
                if expected_type is int and isinstance(val, bool):
                    errors.append(f"Field '{field}' must be int (not bool)")
                elif expected_type is bool and not isinstance(val, bool):
                    errors.append(
                        f"Field '{field}' must be boolean, got {type(val).__name__}"
                    )
                elif not isinstance(val, expected_type):
                    errors.append(
                        f"Field '{field}' must be {expected_type.__name__}, "
                        f"got {type(val).__name__}"
                    )

    if not errors:
        # Numeric value checks
        delta = data.get("delta_seconds", 0)
        if not (2480 <= delta <= 2494):
            errors.append(f"delta_seconds={delta} not in expected range [2480, 2494]")

        dl_size = data.get("download_size_mb", 0)
        if abs(dl_size - 2.3) > 0.05:
            errors.append(f"download_size_mb expected 2.3, got {dl_size}")

        em_size = data.get("email_attachment_size_mb", 0)
        if abs(em_size - 2.3) > 0.05:
            errors.append(f"email_attachment_size_mb expected 2.3, got {em_size}")

        # hash_match_confirmed must be false at this stage
        if data.get("hash_match_confirmed") is not False:
            errors.append(
                f"hash_match_confirmed must be boolean false at this stage "
                f"(hash evidence not yet confirmed), got {repr(data.get('hash_match_confirmed'))}"
            )

        # defense_claims: exactly 3 items, all status == "refuted"
        claims = data.get("defense_claims", [])
        if len(claims) != 3:
            errors.append(f"defense_claims must have exactly 3 items, got {len(claims)}")
        else:
            for i, claim in enumerate(claims):
                if not isinstance(claim, dict):
                    errors.append(f"defense_claims[{i}] must be an object")
                    continue
                if "status" not in claim:
                    errors.append(f"defense_claims[{i}] missing 'status' field")
                elif claim["status"] != "refuted":
                    errors.append(
                        f"defense_claims[{i}].status must be 'refuted', "
                        f"got '{claim['status']}'"
                    )

        # data_exposed_employees: must have all three names
        employees = data.get("data_exposed_employees", [])
        for name in ["李明", "赵伟", "孙丽"]:
            if name not in employees:
                errors.append(
                    f"data_exposed_employees must include '{name}'"
                )

        # Timestamps
        dl_ts = data.get("download_timestamp", "")
        if "2026-09-25T14:22:17" not in dl_ts:
            errors.append(
                f"download_timestamp must contain '2026-09-25T14:22:17', got '{dl_ts}'"
            )

        em_ts = data.get("email_timestamp", "")
        if "2026-09-25T15:03:44" not in em_ts:
            errors.append(
                f"email_timestamp must contain '2026-09-25T15:03:44', got '{em_ts}'"
            )

        # email_recipient
        recipient = data.get("email_recipient", "")
        if "headhunter" not in recipient:
            errors.append(
                f"email_recipient must contain 'headhunter', got '{recipient}'"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
