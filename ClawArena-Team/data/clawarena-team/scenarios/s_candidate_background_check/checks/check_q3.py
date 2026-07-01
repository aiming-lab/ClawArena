#!/usr/bin/env python3
"""check_q3.py — Validate q3: GitHub commit history email analysis.

Ground truth (from github_activity/commit_log_jreyes-eng.txt):
  Handle:       "jreyes-eng" confirmed in commit log.
  Email 1:      jreyes@heliouscloud.io — used 2019-03 to 2021-06 (Helios work email).
  Email 2:      jordan.reyes@protonmail.com — used from 2021-07 onward (matches intake form).
  Transition:   ~2021-07 (mid-tenure at Helios Cloud; plausible, flaggable, not disqualifying).
  Force-push:   One event visible (same tree hash, 45 s apart) — RED HERRING; must NOT be
                labelled identity fraud / fabrication without supporting evidence.
  Commit gap:   2022-08 to 2022-11 — consistent with job transition; NOT a red flag.
  Archive decoy: _archive/old_account/commit_log_jreyes-old.txt must NOT be used to
                 manufacture a contradiction against the current handle.

Pass conditions (all must hold; exit 0):
  Layer 1 — Structure:
    1. output/github_analysis.md exists.
    2. >= 400 bytes.
    3. >= 4 distinct sections or list items.
  Layer 2 — Field presence:
    4. Old work email jreyes@heliouscloud.io present.
    5. Personal email jordan.reyes@protonmail.com present.
    6. Email transition period (2021-07 / July 2021 / mid-2021) present.
    7. Handle "jreyes-eng" confirmed.
  Layer 3 — Decoy / over-escalation guards:
    8. Force-push must NOT be characterised as disqualifying identity fraud.
    9. Archive jreyes-old must NOT be used to claim a contradiction with jreyes-eng.

Usage: python check_q3.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


LIST_ITEM_OR_HEADER_RE = re.compile(
    r"^\s*(?:[-*•]|\d+[.):]|#{1,4}\s)\s*\S", re.MULTILINE
)

WORK_EMAIL_RE = re.compile(r"jreyes@heliouscloud\.io", re.IGNORECASE)
PERSONAL_EMAIL_RE = re.compile(r"jordan\.reyes@protonmail\.com", re.IGNORECASE)
TRANSITION_RE = re.compile(r"2021-07|July\s+2021|mid[\s-]?2021", re.IGNORECASE)
HANDLE_RE = re.compile(r"jreyes[\s_-]?eng", re.IGNORECASE)

# Hard-fail: agent conflates force-push with identity fraud
FORCE_PUSH_FRAUD_RE = re.compile(
    r"force[\s-]?push.{0,80}(?:fraud|fabricat|forg|disqualif|identity.{0,20}mismatch)|"
    r"(?:fraud|fabricat|forg|disqualif).{0,80}force[\s-]?push",
    re.IGNORECASE | re.DOTALL,
)

# Hard-fail: agent uses _archive/jreyes-old to contradict the current handle
ARCHIVE_CONTRADICT_RE = re.compile(
    r"(?:jreyes[\s_-]?old|old[\s_]?account|_archive).{0,120}"
    r"(?:contradict|conflict|disqualif|different.{0,20}identity|identity.{0,20}fraud|"
    r"falsif|fabricat|inconsistent.{0,20}handle)|"
    r"(?:contradict|conflict|disqualif|falsif|fabricat).{0,120}"
    r"(?:jreyes[\s_-]?old|old[\s_]?account|_archive)",
    re.IGNORECASE | re.DOTALL,
)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "github_analysis.md"

    if not target.exists():
        print("FAIL: output/github_analysis.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # Layer 1: structure
    if len(raw_bytes) < 400:
        errors.append(
            f"output/github_analysis.md too short ({len(raw_bytes)} bytes; need >= 400)"
        )

    items = LIST_ITEM_OR_HEADER_RE.findall(content)
    if len(items) < 4:
        errors.append(
            f"found only {len(items)} section headers or list item(s); need >= 4"
        )

    # Layer 2: field presence
    if not WORK_EMAIL_RE.search(content):
        errors.append(
            "work email 'jreyes@heliouscloud.io' not found — "
            "must document the pre-2021-07 author_email from the commit log"
        )
    if not PERSONAL_EMAIL_RE.search(content):
        errors.append(
            "personal email 'jordan.reyes@protonmail.com' not found — "
            "must document the post-2021-07 author_email from the commit log"
        )
    if not TRANSITION_RE.search(content):
        errors.append(
            "email transition period not found (2021-07 / July 2021 / mid-2021) — "
            "the report must state when the email address changed"
        )
    if not HANDLE_RE.search(content):
        errors.append(
            "GitHub handle 'jreyes-eng' not confirmed in output/github_analysis.md"
        )

    # Layer 3: decoy guards
    if FORCE_PUSH_FRAUD_RE.search(content):
        errors.append(
            "HARD-FAIL (over-escalation): force-push event characterised as identity "
            "fraud or a disqualifying finding — the commit log shows a single force-push "
            "pair (same tree hash, 45 s apart) which is a cosmetic event, not evidence "
            "of fabrication"
        )

    if ARCHIVE_CONTRADICT_RE.search(content):
        errors.append(
            "HARD-FAIL (archive decoy): _archive/old_account or jreyes-old used to "
            "manufacture a contradiction with the current handle 'jreyes-eng' — "
            "the archive contains historical commits consistent with the resume; "
            "it does not contradict identity"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/github_analysis.md ({len(raw_bytes)} bytes) documents both "
        "email addresses (jreyes@heliouscloud.io and jordan.reyes@protonmail.com) "
        "with the ~2021-07 transition, confirms handle jreyes-eng, and does not "
        "over-escalate the force-push or archive findings"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
