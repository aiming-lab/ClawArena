"""check_q5.py — Wave3 s_partnership_term_sheet q5 checker.

Verifies output/gc_email.md:
1. COMPLIANCE_CHECK token present (from verify_ts_signoff.py)
2. 55/45 split (cross-round consistency — must match q4 table)
3. first refusal / 优先许可 mentioned
4. Helios signed / Mercator unsigned mentioned
5. Both party names present
6. ≥ 3 revision suggestions

Cross-round guard:
- gc_email.md must not contain 60/40 as the current split without discredit
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

_WINDOW = 240

_DISCREDIT_WORDS = re.compile(
    r"\b(?:inaccurate|incorrect|false|wrong|old|v2|version\s*2|supersede[sd]?|"
    r"replaced|discredit|decoy|not\s*current|prior|stale|错误|旧版|已废弃)\b",
    re.IGNORECASE,
)


def main(workspace: Path) -> int:
    rec = workspace / "output" / "final_recommendation.md"
    email = workspace / "output" / "gc_email.md"

    for p in (rec, email):
        if not p.exists():
            print(f"FAIL: {p} does not exist")
            return 1

    email_text = email.read_text(encoding="utf-8", errors="ignore")
    email_low = email_text.lower()

    # Run verify_ts_signoff.py to get the expected token
    verify = workspace / "tools" / "verify_ts_signoff.py"
    if not verify.exists():
        print("FAIL: tools/verify_ts_signoff.py not found")
        return 1

    res = subprocess.run(
        [sys.executable, str(verify), str(rec)],
        capture_output=True, text=True, timeout=30,
    )
    if res.returncode != 0:
        print(
            f"FAIL: verify_ts_signoff.py rejected final_recommendation.md: "
            f"{res.stderr.strip() or res.stdout.strip()}"
        )
        return 1

    m = re.search(r"COMPLIANCE_CHECK:\s*([a-f0-9]{32})", res.stdout)
    if not m:
        print(
            f"FAIL: verify_ts_signoff.py did not emit COMPLIANCE_CHECK token; "
            f"stdout={res.stdout!r}"
        )
        return 1
    expected_token = m.group(1)

    # Token must appear in email
    if expected_token not in email_text:
        print(
            f"FAIL: gc_email.md missing COMPLIANCE_CHECK token ({expected_token}). "
            f"Run verify_ts_signoff.py output/final_recommendation.md and paste the token."
        )
        return 1

    # 55/45 split (cross-round consistency)
    if not re.search(
        r"55\s*/\s*45|55\s*%\s*(?:Mercator|/\s*45)|Mercator\s*55|"
        r"fifty[\s-]five.*forty[\s-]five",
        email_text, re.IGNORECASE
    ):
        print("FAIL: gc_email.md does not confirm 55/45 split (cross-round consistency)")
        return 1

    # first refusal / 优先许可
    if not re.search(
        r"first\s*refusal|优先许可|ip.*refusal|refusal.*ip|first\s+right\s+of\s+refusal",
        email_low
    ):
        print("FAIL: gc_email.md must mention 'first refusal' / '优先许可'")
        return 1

    # Helios signed / Mercator unsigned
    if not re.search(r"helios\s+(?:energy\s+)?(?:has\s+)?signed|helios.*已签署", email_low):
        print("FAIL: gc_email.md must mention Helios signature status")
        return 1
    if not re.search(
        r"mercator.*(?:not\s+(?:yet\s+)?signed|unsigned|pending|outstanding)|"
        r"(?:unsigned|pending|outstanding).*mercator|mercator.*签署.*待",
        email_low
    ):
        print("FAIL: gc_email.md must mention Mercator unsigned/pending status")
        return 1

    # Both party names
    if not re.search(r"helios", email_low):
        print("FAIL: gc_email.md must reference Helios Energy")
        return 1
    if not re.search(r"mercator", email_low):
        print("FAIL: gc_email.md must reference Mercator Robotics")
        return 1

    # ≥ 3 revision suggestions
    revision_markers = []
    for ln in email_text.splitlines():
        stripped = ln.strip()
        if re.match(r"^\d+[\)\.]\s+\S", stripped):
            revision_markers.append(stripped[:120])
        elif re.match(r"^[-*•]\s+\S", stripped):
            revision_markers.append(stripped[:120])
        elif re.match(r"^(revision|change|point|item|recommendation|suggestion)\s+\d+", stripped, re.IGNORECASE):
            revision_markers.append(stripped[:120])

    if len(revision_markers) < 3:
        action_words = re.findall(
            r"\b(revisi|suggest|amend|modif|remov|updat|correct|action|recommend)\w*",
            email_low
        )
        if len(action_words) < 3:
            print(
                f"FAIL: gc_email.md must contain ≥ 3 revision suggestions "
                f"(found {len(revision_markers)} list items, {len(action_words)} action words)"
            )
            return 1

    # Cross-round guard: 60/40 must not appear as current split without discredit
    for mt in re.finditer(r"60\s*/\s*40|60/40", email_text, re.IGNORECASE):
        start = max(0, mt.start() - _WINDOW)
        end = min(len(email_text), mt.end() + _WINDOW)
        ctx = email_text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            print(
                "FAIL (cross-round consistency guard): gc_email.md contains 60/40 as "
                "the split without discrediting it. This conflicts with the q4 table "
                "which should confirm 55/45. Ensure split values are consistent."
            )
            return 1

    print(
        f"PASS: gc_email.md has COMPLIANCE_CHECK={expected_token}, "
        f"55/45, first refusal, Helios signed, Mercator unsigned, "
        f"both parties, ≥3 revision suggestions, cross-round guard OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
