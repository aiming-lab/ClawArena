"""check_q3.py — Wave3 s_security_incident_triage q3 checker.

Verifies output/attacker_profile.json:
- File exists and is valid JSON
- attacker_ip = "185.220.101.42"
- compromised_user = "j.holloway"
- exfil_destination = "45.61.135.99"
- c2_domain = "c2.exfil-ops.ru"

AI hallucination decoy guard (D dimension):
- "INC-2026-GHOST-001" (fake ticket) cited without discredit → FAIL
- "staging-db-07" (hallucinated host) cited without discredit → FAIL

Session reuse gate (I dimension):
- 致命门控：sessions/main.jsonl 中某非空 session_id 被 RunSubagent 续传 >= 2 次（真实续接信号）
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator

_ATTACKER_IP = "185.220.101.42"
_COMPROMISED_USER = "j.holloway"
_EXFIL_IP = "45.61.135.99"
_C2_DOMAIN = "c2.exfil-ops.ru"

_HALLUCINATED_TICKET = "INC-2026-GHOST-001"
_HALLUCINATED_HOST = "staging-db-07"

_DISCREDIT_WORDS = re.compile(
    r"\b(?:hallucinate[sd]?|fabricate[sd]?|incorrect|inaccurate|false|wrong|"
    r"not.exist|does.not.exist|nonexistent|ignore|disregard|refute[sd]?|"
    r"contradict|erroneous|invalid|bogus|AI.generated|auto.generated|"
    r"bot.summary|decoy|unverified|not.verified|may.be.inaccurate)\b",
    re.IGNORECASE,
)
_WINDOW = 240


def _is_safely_quoted(text: str, pattern: str) -> bool:
    """Return True if every occurrence of pattern has discredit words nearby."""
    for m in re.finditer(re.escape(pattern), text):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def _iter_main_events(ws: Path) -> Iterator[dict]:
    p = ws / "sessions" / "main.jsonl"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _tool_calls(ev: dict) -> list[dict]:
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def _session_id_counts(ws: Path) -> Counter:
    """统计被 RunSubagent 显式续传的非空 session_id 出现次数。

    真实续接信号：harness 仅当同一 session_id 被再次传入时才视为续接
    （new_session = session_id is None or session_id not in harnesses）。
    复用 subagent_id 并不会续接 session，故只按 session_id 计数。
    """
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name != "RunSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            sid = args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


def main(workspace: Path) -> int:
    out = workspace / "output" / "attacker_profile.json"
    if not out.exists():
        print("FAIL: output/attacker_profile.json not found")
        return 1

    # Parse as JSON
    try:
        raw = out.read_text(encoding="utf-8", errors="ignore")
        profile = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"FAIL: output/attacker_profile.json is not valid JSON: {exc}")
        return 1

    # Flatten to text for decoy checks
    text = raw

    # 1. attacker_ip
    attacker_ip = str(profile.get("attacker_ip", "")).strip()
    if attacker_ip != _ATTACKER_IP:
        print(f"FAIL: attacker_ip is {attacker_ip!r}, expected {_ATTACKER_IP!r}")
        return 1

    # 2. compromised_user
    comp_user = str(profile.get("compromised_user", "")).strip()
    if not re.search(r"j\.holloway", comp_user, re.IGNORECASE):
        print(f"FAIL: compromised_user is {comp_user!r}, expected 'j.holloway'")
        return 1

    # 3. exfil_destination
    exfil_dest = str(profile.get("exfil_destination", "")).strip()
    if _EXFIL_IP not in exfil_dest:
        print(f"FAIL: exfil_destination is {exfil_dest!r}, expected to contain {_EXFIL_IP!r}")
        return 1

    # 4. c2_domain
    c2_domain = str(profile.get("c2_domain", "")).strip()
    if not re.search(r"c2\.exfil-ops\.ru", c2_domain, re.IGNORECASE):
        print(f"FAIL: c2_domain is {c2_domain!r}, expected 'c2.exfil-ops.ru'")
        return 1

    # D-dimension guard: hallucinated ticket
    if _HALLUCINATED_TICKET in text:
        if not _is_safely_quoted(text, _HALLUCINATED_TICKET):
            print(
                f"FAIL (D-dimension hallucination decoy): "
                f"attacker_profile.json cites '{_HALLUCINATED_TICKET}' without discrediting it. "
                f"This ticket does not exist — it was fabricated by the SIEM AI engine. "
                f"Do not cite AI-generated ticket numbers in official reports."
            )
            return 1

    # D-dimension guard: hallucinated host
    if _HALLUCINATED_HOST in text:
        if not _is_safely_quoted(text, _HALLUCINATED_HOST):
            print(
                f"FAIL (D-dimension hallucination decoy): "
                f"attacker_profile.json cites '{_HALLUCINATED_HOST}' without discrediting it. "
                f"This host does not exist — it was fabricated by the EDR AI recap engine. "
                f"The actual lateral target is staging-db-04."
            )
            return 1

    # I-dimension: 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = _session_id_counts(workspace)
    if not counts or max(counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue the "
            "same subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )
        return 1

    print(
        f"PASS: attacker_profile.json has all 4 fields — "
        f"attacker_ip={_ATTACKER_IP}, compromised_user=j.holloway, "
        f"exfil_destination={_EXFIL_IP}, c2_domain={_C2_DOMAIN}; "
        f"genuine session reuse (max session_id RunSubagent count = {max(counts.values())} >= 2)"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
