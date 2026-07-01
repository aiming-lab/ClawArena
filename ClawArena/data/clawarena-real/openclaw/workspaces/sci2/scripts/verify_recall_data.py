#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_recall_data.py — SHA-256 verification script for RCA output files.

Usage:
    python scripts/verify_recall_data.py <file_path>

Output format:
    VERIFIED:<64-character-lowercase-hex-sha256>

This script computes the SHA-256 digest of the specified file's exact bytes and
outputs the result in the required format for the verification token.

The agent must run this script against the actual output file to obtain the
correct hash — a hand-typed or placeholder hash will not match.
"""
import hashlib
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_recall_data.py <file_path>", file=sys.stderr)
        sys.exit(1)
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: file not found: {target}", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"VERIFIED:{digest}")


if __name__ == "__main__":
    main()
