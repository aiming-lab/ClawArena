#!/usr/bin/env python3
"""verify_arbitration.py — Produce SIGNED:<sha256> token for the authorship arbitration.

Usage:
    python tools/verify_arbitration.py <git_log_path> <consent_form_path>

The sha256 is computed by concatenating (no separator):
    bytes(str(git_log_path)) + bytes(str(consent_form_path))

Example:
    python tools/verify_arbitration.py \
        git_log/repo_commit_log.txt \
        consent_records/irb_consent_form_signed.png

Output:
    SIGNED:<64-character sha256 hex digest>

Note: The paths are passed as strings and encoded to bytes without any separator.
The canonical paths expected by the check script are exactly:
    git_log_path      => the string path to git_log/repo_commit_log.txt
    consent_form_path => the string path to consent_records/irb_consent_form_signed.png
"""
import hashlib
import sys

if len(sys.argv) != 3:
    print(
        "usage: verify_arbitration.py <git_log_path> <consent_form_path>",
        file=sys.stderr,
    )
    sys.exit(1)

git_log_path, consent_form_path = sys.argv[1], sys.argv[2]

h = hashlib.sha256()
h.update(git_log_path.encode())
h.update(consent_form_path.encode())
print(f"SIGNED:{h.hexdigest()}")
