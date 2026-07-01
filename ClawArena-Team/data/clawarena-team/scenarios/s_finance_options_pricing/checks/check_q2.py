"""q2: notes/data_load.md exists + contains K=52.50 + row count "200" magnitude
    + a subagent was CreateSubagent'd (evidence of delegation for parquet load).

Pass conditions (all required):
  1. notes/data_load.md exists and is >= 80 chars.
  2. Contains the strike price "52.50" (or "52.5").
  3. Contains a number in the 190_000–220_000 range (the ~200k row count).
  4. ADVISORY ONLY (non-gating): CreateSubagent / delegation evidence no longer gates.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    _tool_calls,
    _tool_name,
    fail,
    iter_main_events,
    passed,
    workspace_root,
)


def _has_create_subagent(ws: Path) -> bool:
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            if _tool_name(tc) == "CreateSubagent":
                return True
    return False


def main() -> int:
    ws = workspace_root()
    note = ws / "notes" / "data_load.md"
    if not note.exists():
        fail("missing notes/data_load.md")
    text = note.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("notes/data_load.md is too short (< 80 chars)")

    # strike price check (schema-by-shape: look for the value, not the key name)
    if not re.search(r"\b52\.5(?:0)?\b", text):
        fail("notes/data_load.md does not mention K=52.50 (strike price)")

    # row count magnitude: any integer 190000–220000 or text like "200k" / "200,000"
    row_ok = (
        re.search(r"\b(?:19[0-9]|20[0-9]|21[0-9]|22[0-0])[0-9]{3}\b", text)
        or re.search(r"\b200[\s,]?[kK]\b", text)
        or re.search(r"\b200,000\b", text)
        or re.search(r"\b~?\s*200\s*k\b", text, re.IGNORECASE)
    )
    if not row_ok:
        fail("notes/data_load.md missing row count in ~200k range (190k–220k)")

    # delegation evidence — ADVISORY ONLY (non-gating)
    print(
        "NOTE: parallel/delegated subagent count not verified — advisory only, non-gating",
        file=sys.stderr,
    )
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
