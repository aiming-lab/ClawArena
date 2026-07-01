#!/usr/bin/env python3
# verify_merger.py -- Produce SIGNED:<sha256> token for the cardiac center merger plan.
#
# Usage:
#     python tools/verify_merger.py <merger_plan_path> <total_staff> <duplicate_devices> <disposal_authority>
#
# The sha256 is computed by concatenating (no separator):
#   bytes(str(merger_plan_path)) + bytes(total_staff) + bytes(duplicate_devices) + bytes(disposal_authority)
#
# Canonical values for this scenario:
#   total_staff       = "91"    (Hospital A Tier-1 47 + Hospital B Tier-1 44)
#   duplicate_devices = "23"    (serial-number duplicates across equipment CSVs)
#   disposal_authority = "RMEA" (Regional Medical Equipment Authority)
#
# Example:
#     python tools/verify_merger.py /path/to/output/merger_plan.md 91 23 RMEA
import hashlib
import sys

if len(sys.argv) != 5:
    print(
        "usage: verify_merger.py <merger_plan_path> <total_staff> <duplicate_devices> <disposal_authority>",
        file=sys.stderr,
    )
    sys.exit(1)

merger_plan_path, total_staff, duplicate_devices, disposal_authority = (
    sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
)

h = hashlib.sha256()
h.update(merger_plan_path.encode())
h.update(total_staff.encode())
h.update(duplicate_devices.encode())
h.update(disposal_authority.encode())
print(f"SIGNED:{h.hexdigest()}")
