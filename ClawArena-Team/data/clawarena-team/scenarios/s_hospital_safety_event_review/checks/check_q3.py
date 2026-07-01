"""check_q3.py — wave3 s_hospital_safety_event_review q3 checker.

Verifies output/timeline_evidence.md:
  1. File exists
  2. CCTV alarm timestamp 2026-06-14T23:48:07 present (F dimension)
  3. ALARM_RED status present (F dimension)
  4. Telemetry cross-reference mentioned

Session reuse audit (I dimension) — FATAL gate on the REAL resume signal:
  - Parse sessions/main.jsonl and count non-empty session_id values threaded into
    RunSubagent calls. The harness only continues a session when the same
    session_id is passed back (new_session = session_id is None or session_id not
    in harnesses); a subagent_id alone spawns a fresh session every round.
  - Require some non-empty session_id to appear >= 2 times — that is the only
    genuine "continue the same subagent session" signal. Otherwise FAIL.
  - 其它内容校验（文件存在 / CCTV 时间戳 / ALARM_RED / telemetry 交叉引用）
    保持致命不变。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Session parsing helpers
# ---------------------------------------------------------------------------

def _extract_records(jsonl_path: Path) -> list[dict]:
    records = []
    try:
        text = jsonl_path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                records.append(obj)
            except json.JSONDecodeError:
                continue
    except Exception:
        pass
    return records


def _iter_call_args(r: dict):
    """Yield each tool call's arguments dict, regardless of on-disk shape.

    Handles flat OpenAI-style ({"tool_calls":[{"name":..,"arguments":{..}}]}),
    nested-function ({"function":{"arguments": "<json str>"}}), Anthropic
    content-block ({"content":[{"type":"tool_use","input":{..}}]}) and the
    legacy flat single-event ({"tool"|"name":.., "params"|"input":{..}}) forms.
    """
    content = r.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name", "") or "", block.get("input")

    tcs = r.get("tool_calls")
    if isinstance(tcs, list):
        for tc in tcs:
            if not isinstance(tc, dict):
                continue
            name = tc.get("name") or (tc.get("function") or {}).get("name", "") or ""
            args = tc.get("arguments")
            if args is None:
                args = (tc.get("function") or {}).get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            yield name, args
        return

    name = r.get("tool") or r.get("name")
    if name:
        args = r.get("params") or r.get("input") or r.get("arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {}
        yield name, args


def _find_session_ids(records: list[dict], round_hint: str) -> list[str]:
    ids = []
    for r in records:
        r_str = json.dumps(r)
        if round_hint not in r_str:
            continue
        # 1. top-level identifiers on the event itself
        for key in ("session_id", "subagent_id", "agent_id"):
            val = r.get(key)
            if val and isinstance(val, str) and len(val) > 4:
                ids.append(val)
        # 2. identifiers carried inside each tool call's arguments
        for _name, args in _iter_call_args(r):
            if not isinstance(args, dict):
                continue
            for key in ("subagent_id", "session_id", "agent_id", "id"):
                val = args.get(key)
                if val and isinstance(val, str) and len(val) > 4:
                    ids.append(val)
    return ids


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def main(workspace: Path) -> int:
    out = workspace / "output" / "timeline_evidence.md"
    if not out.exists():
        print("FAIL: output/timeline_evidence.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. CCTV alarm timestamp 2026-06-14T23:48:07
    if not re.search(r"2026-06-14T23:48:07", text):
        print(
            "FAIL: CCTV alarm timestamp '2026-06-14T23:48:07' not found. "
            "This appears in the corridor_cctv mp4 visual frames at t≈11 s — "
            "use a vision-capable subagent to read the on-screen timestamp."
        )
        return 1

    # 2. ALARM_RED status
    if not re.search(r"ALARM_RED", text, re.IGNORECASE):
        print(
            "FAIL: ALARM_RED status not found in timeline_evidence.md. "
            "The alarm status appears in the CCTV video frames from t=11 s onward."
        )
        return 1

    # 3. Telemetry cross-reference (some mention of ndjson / telemetry / pump)
    #    收紧：原列表含裸 '23:48:07'，它是检查 #1 已强制要求的 CCTV 时间戳
    #    '2026-06-14T23:48:07' 的子串，因此无需任何 telemetry 提及即满足该条，
    #    使 telemetry 交叉引用形同虚设。改用 telemetry 专属标识（词边界，避免
    #    CCTV 时间戳子串误命中），要求 timeline 真正引用 device_telemetry/ 资产。
    telem_keywords = [
        r"\btelemetry\b",
        r"\bndjson\b",
        r"\bpump\b",
        r"device_telemetry",
        r"pump_telemetry",
        r"vital_signs_trend",
        r"firmware_event",
        r"device_audit_trail",
        r"\bMV7-ICU\b",  # device serial prefix MV7-ICU-2208-0047
    ]
    telem_hit = any(re.search(kw, text, re.IGNORECASE) for kw in telem_keywords)
    if not telem_hit:
        print(
            "FAIL: timeline_evidence.md does not mention a telemetry cross-reference. "
            "Cross-check the CCTV timestamp against device_telemetry/ NDJSON records "
            "(e.g., pump_telemetry.ndjson / vital_signs_trend.ndjson) — citing the "
            "CCTV timestamp alone does not satisfy the telemetry cross-reference."
        )
        return 1

    # Session reuse audit (I dimension) — FATAL gate on the REAL resume signal.
    # The harness only continues a subagent session when the SAME session_id is
    # threaded back into RunSubagent (new_session = session_id is None or
    # session_id not in harnesses). Passing a subagent_id without a session_id
    # spawns a fresh session every round, so we key solely on a non-empty
    # session_id appearing >= 2 times across RunSubagent calls.
    sessions_path = workspace / "sessions" / "main.jsonl"
    session_id_counts: dict[str, int] = {}
    if sessions_path.exists():
        for r in _extract_records(sessions_path):
            for name, args in _iter_call_args(r):
                if name != "RunSubagent" or not isinstance(args, dict):
                    continue
                sid = args.get("session_id")
                if isinstance(sid, str) and sid:
                    session_id_counts[sid] = session_id_counts.get(sid, 0) + 1

    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    if not session_id_counts or max(session_id_counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue the same "
            "subagent session (thread the same session_id), not spawn a fresh one each round"
        )
        return 1

    print(
        "PASS: timeline_evidence.md has 2026-06-14T23:48:07 + ALARM_RED + "
        "telemetry cross-reference + genuine session reuse (same session_id threaded)"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
