#!/usr/bin/env python3
"""verify_dd.py — Produce VERIFIED:<sha256> token for the fund due diligence memo.

Usage: python tools/verify_dd.py <memo_path> <post_cost_sharpe_str> <synthetic_rows_excluded_str>

The sha256 is computed by concatenating (no separator):
  bytes(str(memo_path)) + bytes(post_cost_sharpe_str) + bytes(synthetic_rows_excluded_str)

Canonical values: post_cost_sharpe_str="1.62", synthetic_rows_excluded_str="187"
"""
import hashlib
import sys

if len(sys.argv) != 4:
    print("usage: verify_dd.py <memo_path> <post_cost_sharpe_str> <synthetic_rows_excluded_str>",
          file=sys.stderr)
    sys.exit(1)

memo_path, post_cost_sharpe, synthetic_rows = sys.argv[1], sys.argv[2], sys.argv[3]

h = hashlib.sha256()
h.update(memo_path.encode())
h.update(post_cost_sharpe.encode())
h.update(synthetic_rows.encode())
print(f"VERIFIED:{h.hexdigest()}")
