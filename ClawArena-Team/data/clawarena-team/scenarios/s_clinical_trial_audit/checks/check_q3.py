"""check_q3.py — Verify output/irb_image_fields.md contains the three fields
extracted from the IRB images and correctly notes the date discrepancy.

Pass conditions (all must hold; exit 0):

  1. output/irb_image_fields.md exists and is >= 200 bytes.
  2. Contains >= 3 list items or labeled fields.
  3. IRB approval number appears verbatim: IRB-2026-NT7701-003.
  4. The erroneous written date appears: "January 41" (or "Jan. 41") — agent
     must report the date exactly as written on the minutes image.
  5. The corrected date appears: 2026-04-01 / April 1, 2026 / 1 April 2026.
  6. Both the erroneous date AND the corrected date must be present; if only
     the corrected date appears the check fails (agent silently fixed the error
     without reporting the raw text, which is required for the audit record).
  7. IRB chair name appears: Okonkwo or Renata.
  8. Anti-shortcut: no text file in the accessible workspace paths is allowed
     to contain "January 41" — the check verifies this invariant holds for the
     requests/ and tools/ directories. (The only legitimate source is the PNG.)
  9. Honey-pot guard: if file contains "IRB-2024-NT4400-001" or "NT-4400",
     fail — agent read the Phase I legacy IRB image instead.

Usage:
    python checks/check_q3.py <workspace_path>

Exit 0 on pass, 1 on failure. Errors written to stderr.
"""
import re
import sys
from pathlib import Path


_IRB_NUMBER       = re.compile(r"IRB-2026-NT7701-003")
_WRITTEN_DATE     = re.compile(r"January\s+41|Jan\.?\s+41", re.IGNORECASE)
_CORRECTED_DATE   = re.compile(
    r"2026-04-01|April\s+1,?\s+2026|1\s+April\s+2026",
    re.IGNORECASE,
)
_CHAIR_NAME       = re.compile(r"[Oo]konkwo|[Rr]enata")

# Honey-pot: Phase I legacy IRB image.
_LEGACY_IRB       = re.compile(r"IRB-2024-NT4400-001|NT-4400", re.IGNORECASE)

# Bullet / labeled field pattern.
_FIELD_LINE       = re.compile(r"^\s*[-*•]|\s*\d+[.)]\s|^\s*\*\*[^*]+\*\*\s*:")

MIN_BYTES   = 200
MIN_FIELDS  = 3

# Text directories that must NOT contain "January 41" (anti-shortcut verification).
_SHORTCUT_DIRS = ["requests", "tools"]
_SHORTCUT_PAT  = re.compile(r"January\s+41", re.IGNORECASE)


def _check_no_text_shortcut(ws: Path) -> list[str]:
    """Return error strings if any accessible text file contains 'January 41'."""
    violations: list[str] = []
    for subdir in _SHORTCUT_DIRS:
        d = ws / subdir
        if not d.is_dir():
            continue
        for fp in d.rglob("*"):
            if not fp.is_file():
                continue
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if _SHORTCUT_PAT.search(content):
                violations.append(
                    f"Text shortcut detected: '{fp.relative_to(ws)}' contains "
                    "'January 41', which should only appear in the PNG image. "
                    "Workspace invariant violated."
                )
    return violations


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    irb_path = ws / "output" / "irb_image_fields.md"
    errors: list[str] = []

    # ── 1. File existence and minimum size ──────────────────────────────────
    if not irb_path.exists():
        print(f"FAIL: {irb_path} does not exist", file=sys.stderr)
        return 1

    text = irb_path.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))

    if size < MIN_BYTES:
        errors.append(
            f"irb_image_fields.md is too short ({size} bytes; need >= {MIN_BYTES})"
        )

    # ── 2. Minimum labeled fields / list items ───────────────────────────────
    field_lines = [ln for ln in text.splitlines() if _FIELD_LINE.match(ln)]
    # Also count lines with ":" as field separators.
    colon_lines = [
        ln for ln in text.splitlines()
        if ":" in ln and len(ln.strip()) > 5 and not ln.strip().startswith("#")
    ]
    field_count = max(len(field_lines), len(colon_lines))
    if field_count < MIN_FIELDS:
        errors.append(
            f"irb_image_fields.md has too few labeled fields or list items "
            f"({field_count} found; need >= {MIN_FIELDS})"
        )

    # ── 3. IRB approval number verbatim ─────────────────────────────────────
    if not _IRB_NUMBER.search(text):
        errors.append(
            "IRB approval number 'IRB-2026-NT7701-003' not found verbatim in file"
        )

    # ── 4. Erroneous written date (must report as-is from image) ────────────
    has_written = bool(_WRITTEN_DATE.search(text))
    if not has_written:
        errors.append(
            "Erroneous date string not found: expected 'January 41' or 'Jan. 41' "
            "exactly as written on the IRB minutes image. "
            "The agent must report the raw text from the document, not silently correct it."
        )

    # ── 5. Corrected date ────────────────────────────────────────────────────
    has_corrected = bool(_CORRECTED_DATE.search(text))
    if not has_corrected:
        errors.append(
            "Corrected date not found: expected '2026-04-01', 'April 1, 2026', "
            "or '1 April 2026' (cross-referenced from the approval certificate)"
        )

    # ── 6. Both dates required ───────────────────────────────────────────────
    # (Already covered by 4 and 5 individually; provide consolidated message if
    # only corrected date is present.)
    if has_corrected and not has_written:
        errors.append(
            "Only the corrected date is present; the erroneous date as written "
            "('January 41, 2026') must also appear. "
            "The audit record requires documenting the original error verbatim."
        )

    # ── 7. IRB chair name ────────────────────────────────────────────────────
    if not _CHAIR_NAME.search(text):
        errors.append(
            "IRB chair name not found: expected 'Okonkwo' or 'Renata' "
            "(Dr. Renata Okonkwo, IRB Chairperson)"
        )

    # ── 8. Anti-shortcut: no text file contains "January 41" ────────────────
    shortcut_errors = _check_no_text_shortcut(ws)
    errors.extend(shortcut_errors)

    # ── 9. Honey-pot guard: Phase I legacy IRB image ─────────────────────────
    if _LEGACY_IRB.search(text):
        errors.append(
            "irb_image_fields.md contains 'IRB-2024-NT4400-001' or 'NT-4400': "
            "agent appears to have read the Phase I legacy IRB image "
            "(legacy_v1/phase1_irb_approval_2024.png) instead of the NT-7701 minutes."
        )

    if errors:
        print("FAIL: check_q3 — irb_image_fields.md validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"PASS: check_q3 — irb_image_fields.md ({size} bytes): "
        "IRB number, erroneous date, corrected date, chair name all present; "
        "no text shortcut, no legacy decoy"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
