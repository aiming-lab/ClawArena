#!/usr/bin/env python3
"""verify_audit.py — Produce VERIFIED:<sha256> token for the clinical trial audit.

Usage:
  python tools/verify_audit.py <memo_path> <edc_sae_total> <irb_approval_number>

Example:
  python tools/verify_audit.py output/regulatory_cover_memo.md 57 IRB-2026-NT7701-003

The sha256 is computed by concatenating (no separator):
  bytes(str(memo_path)) + bytes(edc_sae_total) + bytes(irb_approval_number)

The expected inputs for a passing check are:
  edc_sae_total    = "57"
  irb_approval_number = "IRB-2026-NT7701-003"
"""
import hashlib
import sys


def main() -> None:
    if len(sys.argv) != 4:
        print(
            "usage: verify_audit.py <memo_path> <edc_sae_total> <irb_approval_number>",
            file=sys.stderr,
        )
        sys.exit(1)

    memo_path = sys.argv[1]
    edc_total = sys.argv[2]
    irb_num = sys.argv[3]

    h = hashlib.sha256()
    h.update(memo_path.encode())
    h.update(edc_total.encode())
    h.update(irb_num.encode())
    print(f"VERIFIED:{h.hexdigest()}")


if __name__ == "__main__":
    main()
