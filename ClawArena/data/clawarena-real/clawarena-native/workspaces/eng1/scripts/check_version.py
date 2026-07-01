#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check whether the installed requests version is affected by CVE-2024-47081."""
import sys
import pkg_resources


def check():
    try:
        version = pkg_resources.get_distribution("requests").version
        parts = version.split(".")
        major, minor, patch_ = int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0
        is_affected = (major == 2 and minor == 32 and patch_ < 4) or (major == 2 and minor < 32)
        if is_affected:
            print(f"[AFFECTED] requests=={version} is vulnerable to CVE-2024-47081")
            print(f"  Affected range: < 2.32.4")
            print(f"  Fixed version: 2.32.4")
            print(f"  Workaround: set trust_env=False on Session objects")
            sys.exit(1)
        else:
            print(f"[OK] requests=={version} is not affected by CVE-2024-47081")
            sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Could not determine requests version: {e}")
        sys.exit(2)


if __name__ == "__main__":
    check()
