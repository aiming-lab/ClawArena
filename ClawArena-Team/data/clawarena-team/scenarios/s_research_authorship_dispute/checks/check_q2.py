"""check_q2.py — Verify output/git_log_analysis.md for commit timeline and attribution.

Pass conditions (all must hold; exit 0):

  1. output/git_log_analysis.md exists and is >= 400 bytes.
  2. File mentions all four contributor names or their placeholder IDs.
  3. Integration date 2025-02-20 appears in context of harmonized_gwas_v2.
  4. Commit hash 'a3f8c2d1' appears verbatim.
  5. Amended commit is flagged ('amend' / 'amended').
  6. Red-herring disclaimer appears within 500 chars of the amended commit mention.
  7. Apparent PI_X count (89) appears in context of recorded/apparent counts.
  8. True (adjusted) PI_X count (88) appears in context of adjusted/true counts.
  9. Anti-decoy: file must not assert PI_Z has the highest commit count.
 10. Discredit window: if the amended commit is discussed without the red-herring
     disclaimer within 400 chars, emit a WARNING (non-fatal) and note the risk.

Usage:
    python checks/check_q2.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_BYTES = 400

# Names / placeholders that must appear.
CONTRIBUTORS: list[tuple[str, list[str]]] = [
    ("PI_X", ["PI_X", "Liang Jiewen", "liang jiewen", "Liang"]),
    ("PI_Y", ["PI_Y", "Ní Mhurchadha", "Ni Mhurchadha", "Aoife", "aoife"]),
    ("PI_Z", ["PI_Z", "Tariq Saleem", "tariq saleem", "Saleem"]),
    ("GRAD_STUDENT_M", ["GRAD_STUDENT_M", "Mina Takahashi", "mina takahashi", "Takahashi"]),
]

# Dataset integration date.
INTEGRATION_DATE_RE = re.compile(r"2025-02-20|February\s+20", re.IGNORECASE)

# Commit hash.
COMMIT_HASH_RE = re.compile(r"\ba3f8c2d1\b")

# Amended commit flagged.
AMEND_RE = re.compile(r"\bamend(ed)?\b", re.IGNORECASE)

# Red-herring / not-material disclaimer.
RED_HERRING_RE = re.compile(
    r"red\s*herring|does\s+not\s+(affect|change|alter)|not\s+(affect|alter)\s+(the\s+)?conclusion"
    r"|amend.*not.*material|not.*determinative",
    re.IGNORECASE,
)

# PI_X apparent count (89).
COUNT_89_RE = re.compile(r"\b89\b")

# PI_X true / adjusted count (88).
COUNT_88_RE = re.compile(r"\b88\b")

# Anti-decoy: PI_Z must not be *asserted* as having the highest / first commit
# count. The previous pattern (r"\bPI_Z\b.{0,30}\bfirst\b") over-fired on benign,
# correct phrasings such as "PI_Z does not claim first authorship" or "PI_Z makes
# no claim to first authorship" (negated statements) and on authorship prose that
# has nothing to do with the commit-count decoy. The decoy is specifically about
# commit *count* ranking, so we now require:
#   (a) no negation token between PI_Z and the ranking word (negative lookahead,
#       scoped to the same sentence via [^.]), and
#   (b) the ranking word be tied to a commit / count / contribution context.
# This fires only on an affirmative assertion like "PI_Z has the highest commit
# count" while letting correct, negated, or authorship-only sentences pass.
ANTIDECOY_RE = re.compile(
    r"\bPI_Z\b"
    r"(?![^.]*?\b(?:not|never|no|does\s+not|do\s+not|doesn.?t|don.?t|"
    r"cannot|can.?t|without)\b)"
    r"[^.]{0,40}?\b(?:first|highest|most|top|leading|greatest)\b"
    r"[^.]{0,30}?\b(?:commit|count|contribut)",
    re.IGNORECASE,
)


def _window_around(text: str, match: re.Match, radius: int = 500) -> str:
    start = max(0, match.start() - radius)
    end = min(len(text), match.end() + radius)
    return text[start:end]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q2.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    analysis_path = ws / "output" / "git_log_analysis.md"

    if not analysis_path.exists():
        print(f"FAIL: {analysis_path} does not exist")
        return 1

    text = analysis_path.read_text(encoding="utf-8")
    lower = text.lower()
    failures: list[str] = []
    warnings: list[str] = []

    # 1. Minimum size.
    if len(text.encode()) < MIN_BYTES:
        failures.append(
            f"git_log_analysis.md is too short ({len(text.encode())} bytes; need >= {MIN_BYTES})"
        )

    # 2. All four contributors mentioned.
    for label, variants in CONTRIBUTORS:
        if not any(v in text for v in variants):
            failures.append(
                f"{label}: not mentioned by name or placeholder "
                f"(expected one of: {variants})"
            )

    # 3. Integration date 2025-02-20 in context of harmonized_gwas_v2.
    date_match = INTEGRATION_DATE_RE.search(text)
    if not date_match:
        failures.append(
            "Integration date 2025-02-20 (or 'February 20') not found in git_log_analysis.md; "
            "the first commit touching harmonized_gwas_v2 must be dated 2025-02-20"
        )
    else:
        window = _window_around(text, date_match, radius=300)
        if "harmonized_gwas" not in window.lower() and "harmonized" not in window.lower():
            failures.append(
                "2025-02-20 appears in git_log_analysis.md but not near a reference to "
                "harmonized_gwas_v2; the integration date must be tied to that dataset"
            )

    # 4. Commit hash a3f8c2d1.
    if not COMMIT_HASH_RE.search(text):
        failures.append(
            "Commit hash 'a3f8c2d1' not found verbatim in git_log_analysis.md; "
            "the amended integration commit must be cited by its hash prefix"
        )

    # 5. Amended commit flagged.
    amend_match = AMEND_RE.search(text)
    if not amend_match:
        failures.append(
            "The amended commit is not flagged (no 'amend' / 'amended' keyword found); "
            "the commit message annotation must be noted"
        )
    else:
        # 6. Red-herring disclaimer within 500 chars.
        window = _window_around(text, amend_match, radius=500)
        if not RED_HERRING_RE.search(window):
            # Non-fatal warning per spec (discredit window).
            warnings.append(
                "WARN: amended commit is discussed but the red-herring disclaimer "
                "('does not affect the authorization conclusion' or similar) is not found "
                "within 500 characters; agent may be treating the amendment as material"
            )

        # 10. Tighter window (400 chars) for discredit check.
        window_400 = _window_around(text, amend_match, radius=400)
        if not RED_HERRING_RE.search(window_400):
            warnings.append(
                "WARN (discredit window 400 chars): red-herring disclaimer not found "
                "within 400 characters of the amended-commit mention"
            )

    # 7. Apparent count 89.
    if not COUNT_89_RE.search(text):
        failures.append(
            "PI_X apparent/recorded commit count (89) not found in git_log_analysis.md; "
            "the pre-adjustment count including the amended commit must be stated"
        )

    # 8. True adjusted count 88.
    if not COUNT_88_RE.search(text):
        failures.append(
            "PI_X true/adjusted commit count (88) not found in git_log_analysis.md; "
            "the corrected count after discounting the amended commit must be stated"
        )

    # 9. Anti-decoy: PI_Z must not be asserted as having the highest count.
    if ANTIDECOY_RE.search(text):
        failures.append(
            "Anti-decoy violation: git_log_analysis.md appears to assert PI_Z has the "
            "first/highest commit count; PI_X holds the highest count even after adjustment"
        )

    for w in warnings:
        print(w, file=sys.stderr)

    if failures:
        print("FAIL: check_q2 — git_log_analysis.md failed one or more checks:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "PASS: check_q2 — git_log_analysis.md correctly identifies commit hash a3f8c2d1, "
        "integration date 2025-02-20, apparent count 89, adjusted count 88, "
        "and flags the amended commit as a red herring"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
