"""check_q3.py — Strict schema-by-shape verification of the 10-slide JSON list.

Pass conditions (all must hold; exit 0):
  1. output/notes/slides_points.md exists and contains a valid top-level JSON list
     (extracted from the first '[ ... ]' block in the file).
  2. The list has EXACTLY 10 entries (not just >= 10).
  3. Each entry is a JSON object (dict).
  4. Each entry carries a slide identifier: an integer 1..10 OR a string
     containing such a number (e.g. "slide_number": 3, or "slide": "3", etc.).
  5. Each entry carries a substantive argument string: at least one string value
     >= 20 characters that is not merely a slide-id token.
  6. The 10 slide identifiers collectively cover exactly {1, 2, ..., 10} —
     no duplicates and no gaps.

Usage: python checks/check_q3.py <workspace_path>
Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

SLIDE_NUM_RE = re.compile(r"\b(10|[1-9])\b")


def _extract_slide_number(value: Any) -> int | None:
    """Return the slide number (1..10) from an int or string value, or None."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and 1 <= value <= 10:
        return value
    if isinstance(value, str):
        m = SLIDE_NUM_RE.search(value)
        if m:
            return int(m.group(1))
    return None


def _is_substantive_argument(value: Any) -> bool:
    """Return True iff value is a non-trivial string of >= 20 characters."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if len(stripped) < 20:
        return False
    # Reject pure slide-id tokens.
    if re.fullmatch(r"slide[-_\s]?\d{1,2}", stripped, re.IGNORECASE):
        return False
    if re.fullmatch(r"\d{1,2}", stripped):
        return False
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q3.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    note_path = ws / "output" / "notes" / "slides_points.md"

    if not note_path.exists():
        print(f"FAIL: {note_path} does not exist")
        return 1

    raw = note_path.read_text(encoding="utf-8").strip()
    json_match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not json_match:
        print("FAIL: slides_points.md does not contain a JSON list (no '[...]' found)")
        return 1

    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"FAIL: slides_points.md JSON parse error: {e}")
        return 1

    if not isinstance(data, list):
        print("FAIL: slides_points.md JSON top level is not a list")
        return 1

    # Condition 2: exactly 10 entries.
    if len(data) != 10:
        print(
            f"FAIL: slides_points.md has {len(data)} entries (need exactly 10, "
            f"one per slide)"
        )
        return 1

    errors: list[str] = []
    seen_slide_numbers: list[int] = []

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            errors.append(f"Entry {i}: not a JSON object — got {type(entry).__name__}")
            continue

        values = list(entry.values())

        # Condition 4: slide identifier.
        # Prefer a value carried under a dedicated slide-number key (e.g.
        # "slide_number" / "slide" / "slide_id" / "slide_no" / "number").
        # Falling back to "first value that yields a digit" is order-sensitive:
        # if an 'argument' field precedes 'slide_number' and itself contains a
        # standalone digit, the wrong value is picked (over-strict).
        slide_num = None
        for key in ("slide_number", "slide_no", "slide_num", "slide_id",
                    "slide_index", "slide", "number", "index", "id"):
            for k, v in entry.items():
                if str(k).lower() == key:
                    extracted = _extract_slide_number(v)
                    if extracted is not None:
                        slide_num = extracted
                        break
            if slide_num is not None:
                break
        if slide_num is None:
            # No dedicated key matched — scan all values as a last resort.
            for v in values:
                extracted = _extract_slide_number(v)
                if extracted is not None:
                    slide_num = extracted
                    break
        if slide_num is None:
            errors.append(
                f"Entry {i}: no slide identifier found (expected an integer 1..10 "
                f"or a string containing one)"
            )
        else:
            seen_slide_numbers.append(slide_num)

        # Condition 5: substantive argument string >= 20 chars.
        if not any(_is_substantive_argument(v) for v in values):
            errors.append(
                f"Entry {i}: no substantive argument string found "
                f"(need a string >= 20 characters that is not just a slide id)"
            )

    # Condition 6: complete coverage of 1..10, no duplicates.
    if len(seen_slide_numbers) == 10:
        if sorted(seen_slide_numbers) != list(range(1, 11)):
            duplicates = [n for n in set(seen_slide_numbers) if seen_slide_numbers.count(n) > 1]
            missing_nums = sorted(set(range(1, 11)) - set(seen_slide_numbers))
            if duplicates:
                errors.append(
                    f"Duplicate slide numbers: {duplicates} — each slide must appear exactly once"
                )
            if missing_nums:
                errors.append(
                    f"Missing slide numbers: {missing_nums} — all 10 slides must be covered"
                )

    if errors:
        print("FAIL: slides_points.md has structural errors:")
        for e in errors[:8]:
            print(f"  - {e}")
        return 1

    print(
        f"PASS: check_q3 — slides_points.md has exactly 10 entries covering "
        f"slides 1–10, each with a slide number and a substantive argument"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
