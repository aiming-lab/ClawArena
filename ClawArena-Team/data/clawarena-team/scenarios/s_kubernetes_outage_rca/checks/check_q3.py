"""check_q3.py — Wave3 s_kubernetes_outage_rca q3 checker.

Verifies output/code_and_dashboard.md:
- validateNamespace mentioned
- webhook.go line 87 (or at line 87 / line87)
- 512 in dashboard/memory context (from mp4 frame)
- helm version 1.18.3

Session reuse audit (I dimension) — FATAL gate on the REAL resume signal:
- Parse sessions/main.jsonl and count non-empty session_id values threaded into
  RunSubagent calls. The harness only continues a subagent session when the same
  session_id is passed back (new_session = session_id is None or session_id not
  in harnesses); a subagent_id alone spawns a fresh session every round.
- Require some non-empty session_id to appear >= 2 times — the only genuine
  "keep the same subagent session running" signal. Otherwise FAIL. All other
  content checks below remain fatal.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Session reuse parsing
# ---------------------------------------------------------------------------

def _extract_subagent_sessions(jsonl_path: Path) -> list[dict]:
    """Extract CreateSubagent or RunSubagent call records from main.jsonl.

    Each record expected shape (harness-dependent):
    {
      "round_id": "q2",          # or "s2"
      "tool": "CreateSubagent" | "RunSubagent",
      "session_id": "...",
      "subagent_id": "...",
      ...
    }
    We look for round hints near each tool call to correlate with q2/q3.
    """
    records = []
    try:
        text = jsonl_path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            records.append(obj)
    except Exception:
        pass
    return records


def _find_session_ids(records: list[dict], round_hint: str) -> list[str]:
    """Find session/subagent IDs associated with a given round hint."""
    ids = []
    for r in records:
        # Look for round markers in various fields
        r_str = json.dumps(r)
        if round_hint not in r_str:
            continue
        # Extract session_id or subagent_id from common harness fields
        for key in ("session_id", "subagent_id", "agent_id", "id"):
            val = r.get(key) or r.get("params", {}).get(key) if isinstance(r, dict) else None
            if val and isinstance(val, str) and len(val) > 4:
                ids.append(val)
    return ids


def _run_subagent_session_id_counts(records: list[dict]) -> dict[str, int]:
    """Count non-empty RunSubagent ``session_id`` args — the real resume signal."""
    def _calls(ev: dict) -> list[dict]:
        out: list[dict] = []
        if isinstance(ev.get("tool_calls"), list):
            out.extend(t for t in ev["tool_calls"] if isinstance(t, dict))
        content = ev.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    out.append(block)
        if out:
            return out
        if ev.get("tool") or ev.get("name") or ev.get("type") == "tool_use":
            return [ev]
        return []

    counts: dict[str, int] = {}
    for ev in records:
        for tc in _calls(ev):
            name = tc.get("tool") or tc.get("name") or (tc.get("function") or {}).get("name", "")
            if name != "RunSubagent":
                continue
            args = tc.get("args")
            if args is None:
                args = tc.get("arguments")
            if args is None:
                args = (tc.get("function") or {}).get("arguments")
            if args is None and tc.get("type") == "tool_use":
                args = tc.get("input")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            if not isinstance(args, dict):
                continue
            sid = args.get("session_id")
            if isinstance(sid, str) and sid:
                counts[sid] = counts.get(sid, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def main(workspace: Path) -> int:
    out = workspace / "output" / "code_and_dashboard.md"
    if not out.exists():
        print("FAIL: output/code_and_dashboard.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. validateNamespace
    if not re.search(r"validateNamespace", text, re.IGNORECASE):
        print("FAIL: 'validateNamespace' not found in code_and_dashboard.md")
        return 1

    # 2. webhook.go line 87 reference (accept various phrasings)
    if not re.search(r"webhook\.go", text, re.IGNORECASE):
        print("FAIL: 'webhook.go' not found in code_and_dashboard.md")
        return 1
    if not re.search(r"\b87\b", text):
        print("FAIL: line number 87 not found in code_and_dashboard.md")
        return 1

    # 3. 512 in memory/dashboard context (from mp4 frame)
    if not re.search(r"\b512\b", text):
        print("FAIL: memory value 512 (from grafana mp4 frame) not found")
        return 1

    # 4. Helm version 1.18.3
    if not re.search(r"1\.18\.3", text):
        print("FAIL: helm version 1.18.3 not found in code_and_dashboard.md")
        return 1

    # 5. Session reuse audit (I dimension) — FATAL on the REAL resume signal.
    #    The harness only continues a subagent session when the same session_id is
    #    threaded back into RunSubagent; a subagent_id alone spawns a fresh
    #    session each round. We require some non-empty session_id to recur >= 2x.
    sessions_path = workspace / "sessions" / "main.jsonl"
    records = _extract_subagent_sessions(sessions_path) if sessions_path.exists() else []
    session_id_counts = _run_subagent_session_id_counts(records)
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    if not session_id_counts or max(session_id_counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue the same "
            "subagent session (thread the same session_id), not spawn a fresh one each round"
        )
        return 1

    print(
        f"PASS: validateNamespace + webhook.go:87 + memory=512(mp4) + helm=1.18.3 "
        f"+ genuine session reuse (same session_id threaded)"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
