#!/usr/bin/env python3
"""check_access_timeline_json.py — Validates analysis/access_timeline.json for q3."""
import sys
import json
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "access_timeline.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    # Must be a JSON array
    if not isinstance(data, list):
        print("FAILED: access_timeline.json must be a JSON array")
        sys.exit(1)

    # Must have >= 8 entries
    if len(data) < 8:
        errors.append(f"Expected >= 8 entries, got {len(data)}")

    # Find the 林小雅 DOWNLOAD entry
    download_entry = None
    for entry in data:
        user_email = entry.get("user_email", "")
        action = entry.get("action", "")
        if "lxy" in user_email and action == "DOWNLOAD" and entry.get("size_mb") == 2.3:
            download_entry = entry
            break

    if download_entry is None:
        errors.append(
            "No DOWNLOAD entry found with user_email containing 'lxy' and size_mb == 2.3"
        )
    else:
        # Check required fields on all entries
        required_fields = ["timestamp", "user_email", "action", "filename", "size_mb"]
        for entry in data:
            for field in required_fields:
                if field not in entry:
                    errors.append(f"Entry missing required field '{field}': {entry}")
                    break

        # Check size_mb type for download entry
        size_mb = download_entry.get("size_mb")
        if not isinstance(size_mb, (int, float)) or abs(size_mb - 2.3) > 0.05:
            errors.append(f"Download entry size_mb expected 2.3, got {size_mb}")

        # Check computed_delta_to_email_seconds
        delta = download_entry.get("computed_delta_to_email_seconds")
        if delta is None:
            errors.append(
                "Download entry missing 'computed_delta_to_email_seconds' field"
            )
        elif not isinstance(delta, int):
            errors.append(
                f"computed_delta_to_email_seconds must be int, got {type(delta).__name__}"
            )
        elif not (2480 <= delta <= 2494):
            errors.append(
                f"computed_delta_to_email_seconds={delta} not in range [2480, 2494] "
                "(ground truth: 2487 s; tolerance ±7)"
            )

        # Check action enum values
        valid_actions = {"PREVIEW", "DOWNLOAD", "UPLOAD", "EDIT", "SHARE"}
        for entry in data:
            act = entry.get("action", "")
            if act not in valid_actions:
                errors.append(f"Invalid action value '{act}', must be one of {valid_actions}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
