#!/usr/bin/env python3
"""check_q5.py — wave3 s_tax_filing_reconciliation q5 checker.

Verifies output/client_letter.md and output/irs_disclosure.md:
1. client_letter.md exists, ≥ 400 chars.
2. client_letter.md contains valid COMPLIANCE_CHECK token (matches fresh tool run).
3. client_letter.md contains: "PFIC", "18,420" / "18420", "1.0913".
4. client_letter.md USD rental amount in [20100, 20103] (cross-round consistency).
5. irs_disclosure.md exists, ≥ 200 chars.
6. irs_disclosure.md mentions PFIC and 18,420 / 18420.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    letter = workspace / "output" / "client_letter.md"
    disclosure = workspace / "output" / "irs_disclosure.md"
    verify_tool = workspace / "tools" / "verify_tax_signoff.py"

    # 1. client_letter.md exists
    if not letter.exists():
        print("FAIL: output/client_letter.md not found")
        return 1
    letter_text = letter.read_text(encoding="utf-8", errors="ignore")

    if len(letter_text.strip()) < 400:
        print(f"FAIL: client_letter.md too short ({len(letter_text)} chars)")
        return 1

    # 2. COMPLIANCE_CHECK token present and valid
    token_m = re.search(r"COMPLIANCE_CHECK:\s*([0-9a-f]{32})", letter_text)
    if not token_m:
        print("FAIL: COMPLIANCE_CHECK token not found in client_letter.md")
        return 1

    claimed_token = token_m.group(1)

    if not verify_tool.exists():
        print(f"FAIL: {verify_tool} does not exist")
        return 1

    result = subprocess.run(
        [sys.executable, str(verify_tool), str(letter)],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        print(f"FAIL: verify_tax_signoff.py returned non-zero: {result.stderr.strip()[:200]}")
        return 1

    expected_line = next(
        (line for line in result.stdout.splitlines() if line.startswith("COMPLIANCE_CHECK:")), ""
    )
    if not expected_line:
        print("FAIL: verify_tax_signoff.py produced no COMPLIANCE_CHECK line")
        return 1

    expected_token = expected_line.split()[1]
    if claimed_token != expected_token:
        print(
            f"FAIL: COMPLIANCE_CHECK token mismatch. "
            f"claimed={claimed_token!r}, expected={expected_token!r}"
        )
        return 1

    # 3. client_letter.md content anchors
    if not re.search(r"\bPFIC\b", letter_text, re.IGNORECASE):
        print("FAIL: 'PFIC' not mentioned in client_letter.md")
        return 1

    if not re.search(r"18[,.]?420", letter_text):
        print("FAIL: '18,420' rental income not mentioned in client_letter.md")
        return 1

    if not re.search(r"1[,.]0913", letter_text):
        print("FAIL: FX rate '1.0913' not mentioned in client_letter.md")
        return 1

    # 4. Cross-round consistency: USD rental amount in [20100, 20103]
    # german_rental_usd = 18420 × 1.0913 = 20101.746（tax_agg.sh bc scale=2 → 20101.74）
    # → accept range [20100, 20103]（容 20101.74 及四舍五入到 20102 等写法）
    usd_matches = re.findall(r"20[,.]?\d{3}(?:[.,]\d{1,2})?", letter_text)
    found_in_range = False
    for raw in usd_matches:
        clean = raw.replace(",", "").replace(".", "")
        try:
            val = float(raw.replace(",", ""))
        except ValueError:
            try:
                val = float(clean) / 100  # e.g. "2011363" → not valid
            except ValueError:
                continue
        if 20100 <= val <= 20103:
            found_in_range = True
            break

    if not found_in_range:
        print(
            "FAIL (cross-round consistency): USD rental amount not in [20112, 20115] "
            "in client_letter.md. Expected ~$20,113.63 (18420 EUR × 1.0913). "
            "This must match the german_rental_usd field in output/lacerte_update.yaml."
        )
        return 1

    # 5. irs_disclosure.md exists
    if not disclosure.exists():
        print("FAIL: output/irs_disclosure.md not found")
        return 1

    disc_text = disclosure.read_text(encoding="utf-8", errors="ignore")
    if len(disc_text.strip()) < 200:
        print(f"FAIL: irs_disclosure.md too short ({len(disc_text)} chars)")
        return 1

    # 6. irs_disclosure.md anchors
    if not re.search(r"\bPFIC\b", disc_text, re.IGNORECASE):
        print("FAIL: 'PFIC' not mentioned in irs_disclosure.md")
        return 1

    if not re.search(r"18[,.]?420", disc_text):
        print("FAIL: '18,420' rental figure not mentioned in irs_disclosure.md")
        return 1

    print(
        "PASS: client_letter.md has PFIC, 18,420, 1.0913, valid COMPLIANCE_CHECK token, "
        "USD rental in [20112, 20115]; irs_disclosure.md has PFIC and 18,420."
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
