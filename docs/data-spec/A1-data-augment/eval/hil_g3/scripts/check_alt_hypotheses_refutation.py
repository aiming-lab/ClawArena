#!/usr/bin/env python3
"""check_alt_hypotheses_refutation.py — Validates analysis/alternative_hypotheses_refutation.md for q19 (M6)."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "alternative_hypotheses_refutation.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # Must contain the hash for defense 1 refutation (exact string match is correct for a hex hash)
    if "a3f7b2c8e9d1" not in content:
        errors.append(
            "alternative_hypotheses_refutation.md must contain 'a3f7b2c8e9d1' "
            "(SHA-256 hash refuting the 'different file' defense)"
        )

    # Must contain both file sizes as standalone numeric values (defense 2 refutation).
    # Use word-boundary regex to avoid false positives (e.g. "10.8", "12.3").
    if not re.search(r'\b0\.8\b', content):
        errors.append(
            "alternative_hypotheses_refutation.md must contain '0.8' as a standalone value "
            "(anonymized file size for defense 2 refutation)"
        )
    if not re.search(r'\b2\.3\b', content):
        errors.append(
            "alternative_hypotheses_refutation.md must contain '2.3' as a standalone value "
            "(full file size for defense 2 refutation)"
        )

    # Numeric proximity check: 0.8 and 2.3 must appear within 200 chars of each other
    # to confirm the size-mismatch argument is actually made (not just mentioned separately).
    pos_08 = content.find("0.8")
    pos_23 = content.find("2.3")
    if pos_08 != -1 and pos_23 != -1:
        if abs(pos_08 - pos_23) > 200:
            errors.append(
                "alternative_hypotheses_refutation.md: '0.8' and '2.3' must appear within "
                "200 characters of each other to demonstrate the size-mismatch comparison "
                f"(currently {abs(pos_08 - pos_23)} chars apart)"
            )

    # Must have >= 2 ## headings (document must have structure)
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(
            f"alternative_hypotheses_refutation.md must have >= 2 '## ' headings, "
            f"found {len(headings)}"
        )

    # Must contain headhunter domain for defense 3 refutation
    if "headhunter-corp.com" not in content and "headhunter" not in lower:
        errors.append(
            "alternative_hypotheses_refutation.md must contain 'headhunter-corp.com' "
            "(external recipient for defense 3 refutation)"
        )

    # Must contain email subject for defense 3 refutation
    if "薪资数据参考" not in content:
        errors.append(
            "alternative_hypotheses_refutation.md must contain '薪资数据参考' "
            "(email subject for defense 3 refutation)"
        )

    # M6 negative check: must NOT contain language suggesting any defense is viable
    bad_patterns = [
        r"possible defense",
        r"cannot be ruled out",
        r"plausible.{0,40}(defense|explanation|claim)",
        r"(defense|explanation|claim).{0,40}plausible",
        r"not yet (refuted|ruled|disproven)",
        r"remains possible",
        r"could still be",
    ]
    for pat in bad_patterns:
        if re.search(pat, lower):
            errors.append(
                "alternative_hypotheses_refutation.md must NOT use language suggesting "
                f"any defense is viable. Found: '{re.search(pat, lower).group()}'"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
