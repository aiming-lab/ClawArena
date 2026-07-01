#!/usr/bin/env python3
"""verify_agenda.py — Produce SIGNED:<sha256> token for the board governance pack.

Usage:
  python tools/verify_agenda.py <charter_v3.2_path> <revised_agenda_path>

Example:
  python tools/verify_agenda.py charter_docs/charter_v3.2.md output/revised_agenda.md

The sha256 is computed by concatenating (no separator):
  bytes(str(charter_v3.2_path)) + bytes(str(revised_agenda_path))

Per design_spec §7, check_q5 recomputes the token using:
  ws / "charter_docs" / "charter_v3.2.md"
  ws / "output" / "revised_agenda.md"
as string-encoded bytes. Pass the same path strings to obtain a matching token.
"""
import hashlib
import sys


def main() -> None:
    if len(sys.argv) != 3:
        print(
            "usage: verify_agenda.py <charter_v3.2_path> <revised_agenda_path>",
            file=sys.stderr,
        )
        sys.exit(1)

    charter_path = sys.argv[1]
    agenda_path = sys.argv[2]

    h = hashlib.sha256()
    h.update(charter_path.encode())
    h.update(agenda_path.encode())
    print(f"SIGNED:{h.hexdigest()}")


if __name__ == "__main__":
    main()
