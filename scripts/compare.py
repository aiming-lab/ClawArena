#!/usr/bin/env python3
"""Find all report.json files under a directory and run clawarena compare."""

import argparse
import os
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Compare benchmark reports")
    parser.add_argument("target_dir", help="Directory containing report.json files")
    args = parser.parse_args()

    target_dir = args.target_dir

    # Recursively find all report.json files
    reports = []
    for root, _, files in os.walk(target_dir):
        for f in files:
            if f == "report.json":
                reports.append(os.path.join(root, f))

    if len(reports) < 2:
        print(f"Found {len(reports)} report.json file(s), need at least 2. Exiting.")
        exit(1)

    cmd = [
        "clawarena", "compare",
        "--reports", *reports,
        "--out", target_dir,
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
