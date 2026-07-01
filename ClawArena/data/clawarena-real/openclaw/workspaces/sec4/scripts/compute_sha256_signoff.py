#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_sha256_signoff.py — Compute SHA-256 sign-off for a file.

Computes the SHA-256 digest of the exact bytes of a specified file and
outputs a single line: VERIFIED:<sha256hex>

Usage: python scripts/compute_sha256_signoff.py <target_file>
"""
import hashlib
import sys
from pathlib import Path


def compute_signoff(path: str) -> str:
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    return f"VERIFIED:{digest}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute_sha256_signoff.py <target_file>")
        sys.exit(1)
    result = compute_signoff(sys.argv[1])
    print(result)
