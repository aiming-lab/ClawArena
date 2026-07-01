#!/usr/bin/env python3
"""check_q3.py — Validate q3: pip_form_fields.md from the scanned PIP form PNG.

Ground truth (from evidence/pip_form_signed.png, confirmed in manifest_gen.json):
  start_date         = 2026-03-15   (must appear in YYYY-MM-DD format)
  employee_signature = J. Morales   (must mention "Morales", non-empty)
  hr_signature       = K. Tan       (must mention "Tan", non-empty)
  The two signature names must be DISTINCT (different strings).

Pass conditions (all must hold; exit 0):
  1. notes/pip_form_fields.md exists and is >= 60 bytes.
  2. The start date is present in strict YYYY-MM-DD format: 2026-03-15.
     Loose formats (March 15, 2026 / 2026/03/15) are accepted only if the
     YYYY-MM-DD form also appears — the question explicitly asked for YYYY-MM-DD.
  3. The employee signature contains "Morales" (case-insensitive) and is non-empty.
  4. The HR signature contains "Tan" (case-insensitive) and is non-empty.
  5. The two extracted signature names are distinct (Morales ≠ Tan — trivially true
     but catches copy-paste stubs that repeat a single value).

Usage: python check_q3.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Strict YYYY-MM-DD for start date
DATE_STRICT_RE = re.compile(r"\b2026-03-15\b")

# Loose fallbacks — accepted only when the strict form is absent from the field
# but present elsewhere; we prefer strict form
DATE_LOOSE_PATTERNS = (
    re.compile(r"\b2026/03/15\b"),
    re.compile(r"\bMarch\s+15,?\s+2026\b", re.IGNORECASE),
    re.compile(r"\b15\s+March\s+2026\b", re.IGNORECASE),
)

EMPLOYEE_SIG_RE = re.compile(r"[Mm]orales")
HR_SIG_RE = re.compile(r"\bTan\b", re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    f = ws / "notes" / "pip_form_fields.md"

    if not f.exists():
        print("FAIL: notes/pip_form_fields.md does not exist")
        return 1

    content = f.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Minimum length (non-stub check)
    if len(raw_bytes) < 60:
        errors.append(
            f"notes/pip_form_fields.md too short ({len(raw_bytes)} bytes; need >= 60)"
        )

    # 2. Start date in strict YYYY-MM-DD form (or at least a recognised variant)
    has_strict = DATE_STRICT_RE.search(content) is not None
    has_loose = any(p.search(content) for p in DATE_LOOSE_PATTERNS)
    if not has_strict and not has_loose:
        errors.append(
            "start_date '2026-03-15' not found — must appear in YYYY-MM-DD or a "
            "recognised date format"
        )
    elif not has_strict and has_loose:
        # Accept but note that strict was not used as asked
        errors.append(
            "start_date is present but not in YYYY-MM-DD format (2026-03-15) as requested"
        )

    # 3. Employee signature contains "Morales"
    if not EMPLOYEE_SIG_RE.search(content):
        errors.append(
            "employee signature 'Morales' not found in notes/pip_form_fields.md"
        )

    # 4. HR signature contains "Tan"
    if not HR_SIG_RE.search(content):
        errors.append(
            "HR signature 'Tan' not found in notes/pip_form_fields.md"
        )

    # 5. Distinct names (anti-stub: both must appear and be different strings)
    emp_found = EMPLOYEE_SIG_RE.search(content)
    hr_found = HR_SIG_RE.search(content)
    if emp_found and hr_found:
        emp_text = emp_found.group(0).strip().lower()
        hr_text = hr_found.group(0).strip().lower()
        if emp_text == hr_text:
            errors.append(
                "employee_signature and hr_signature resolve to the same string — "
                "they must be distinct names"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: pip_form_fields.md ({len(raw_bytes)} bytes) contains start_date "
        "2026-03-15, employee signature Morales, HR signature Tan (distinct)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
