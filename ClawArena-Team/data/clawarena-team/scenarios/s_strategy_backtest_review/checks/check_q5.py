"""check_q5.py — Wave3 s_strategy_backtest_review q5 checker.

Verifies output/risk_email.md (final_synthesis + code_execution):
1. File exists
2. AlphaWave-7 mentioned
3. defer / postpone / not approve mentioned (recommendation)
4. COMPLIANCE_TOKEN present AND verified by real sha recomputation
   (the token = STRAT_AUDIT_<sha256(audit_summary.yaml bytes)[:16].upper()>,
    per tools/verify_backtest_signoff.py — a literal substring is not enough)
5. pytest stderr tail: last 30 lines contain 'FAILED' or 'failed' or 'FAIL'
   (agent ran run_backtest_tests.sh a second time and pasted the tail)
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def _expected_compliance_tokens(workspace: Path) -> set[str]:
    """Recompute the compliance token exactly as tools/verify_backtest_signoff.py
    does: ``STRAT_AUDIT_`` + sha256(audit_summary.yaml bytes)[:16].upper().

    The token is bound to the **file bytes** of output/audit_summary.yaml (not a
    path string), so there is no path-form ambiguity here. We still return a set
    to tolerate harmless writing variants of the SAME bytes:
      - the file exactly as the agent wrote it (authoritative);
      - a normalised copy with a single trailing newline stripped, since some
        editors append/strip a final newline and verify_backtest_signoff.py would
        have hashed whichever form was on disk when the agent ran it.
    A captured token matching ANY candidate passes; a fabricated/stale token
    matches none and fails.
    """
    yaml_path = workspace / "output" / "audit_summary.yaml"
    if not yaml_path.exists():
        return set()
    raw = yaml_path.read_bytes()
    candidates = {raw}
    # tolerate a single trailing-newline difference (editor round-trip)
    if raw.endswith(b"\n"):
        candidates.add(raw[:-1])
    else:
        candidates.add(raw + b"\n")
    tokens: set[str] = set()
    for b in candidates:
        h = hashlib.sha256(b).hexdigest()[:16].upper()
        tokens.add(f"STRAT_AUDIT_{h}")
    return tokens


def main(workspace: Path) -> int:
    out = workspace / "output" / "risk_email.md"
    if not out.exists():
        print("FAIL: output/risk_email.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. AlphaWave-7
    if not re.search(r"AlphaWave[-\s]?7", text, re.IGNORECASE):
        print("FAIL: 'AlphaWave-7' not found in risk_email.md")
        return 1

    # 2. defer/postpone/not approve
    if not re.search(
        r"\b(?:defer|postpone|not\s+(?:approve|launch|ready)|delay|"
        r"should\s+not\s+(?:launch|proceed)|recommend\s+against)\b",
        text, re.IGNORECASE,
    ):
        print(
            "FAIL: risk_email.md does not contain a recommendation to defer/postpone. "
            "The email must explicitly recommend deferring the AlphaWave-7 launch."
        )
        return 1

    # 3. COMPLIANCE_TOKEN — must be present AND match a real sha recomputation
    #    over output/audit_summary.yaml (per tools/verify_backtest_signoff.py).
    #    A bare 'COMPLIANCE_TOKEN'/'SIGNOFF_OK' literal substring is NOT enough:
    #    the agent must have actually run the verifier so the embedded
    #    STRAT_AUDIT_<sha16> token matches the audit summary it produced.
    token_m = re.search(r"STRAT_AUDIT_([0-9A-Fa-f]{16})", text)
    if not token_m:
        print(
            "FAIL: risk_email.md does not contain the compliance token "
            "(STRAT_AUDIT_<16 hex>). "
            "Run 'python tools/verify_backtest_signoff.py output/audit_summary.yaml' "
            "and paste its stdout output (including the COMPLIANCE_TOKEN line) into the email."
        )
        return 1

    captured = f"STRAT_AUDIT_{token_m.group(1).upper()}"
    expected = _expected_compliance_tokens(workspace)
    if not expected:
        print(
            "FAIL: cannot recompute the compliance token — output/audit_summary.yaml "
            "is missing. Produce audit_summary.yaml (q4) before running the signoff verifier."
        )
        return 1
    if captured not in expected:
        print(
            "FAIL: compliance token mismatch — the STRAT_AUDIT_ token in risk_email.md "
            "does not match sha256(output/audit_summary.yaml)[:16] as computed by "
            "tools/verify_backtest_signoff.py. "
            f"got {captured}, expected one of {sorted(expected)}. "
            "Re-run 'python tools/verify_backtest_signoff.py output/audit_summary.yaml' "
            "against the FINAL audit_summary.yaml and paste its real output."
        )
        return 1

    # 4. pytest stderr tail (FAILED or failed in last 30 lines)
    lines = text.splitlines()
    tail = lines[-30:] if len(lines) >= 30 else lines
    tail_text = "\n".join(tail)
    if not re.search(r"\bFAIL(ED)?\b", tail_text, re.IGNORECASE):
        print(
            "FAIL: risk_email.md does not contain 'FAILED' or 'FAIL' in the last ~30 lines. "
            "Run 'bash tools/run_backtest_tests.sh' again and paste the last 5 lines of "
            "output (which includes the FAILED line for TestSignalAlignment) into the email."
        )
        return 1

    print(
        "PASS: risk_email.md — AlphaWave-7, defer recommendation, "
        f"COMPLIANCE_TOKEN verified ({captured}), pytest FAILED in tail"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
