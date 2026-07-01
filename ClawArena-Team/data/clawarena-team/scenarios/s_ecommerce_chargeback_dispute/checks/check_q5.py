"""check_q5.py — wave3 s_ecommerce_chargeback_dispute q5 checker.

Verifies:
  output/customer_email.md   — bilingual customer email
  output/representment_packet.md — Visa representment packet

Both files must contain:
  - COMPLIANCE_CHECK token (from running verify_dispute_signoff.py on decision_fields.csv)
  - Order id NW-2026-04-A188
  - replacement / 补发 (not full refund)
  - 48 reference (sla)

representment_packet.md additionally must contain:
  - reason code 4837
  - evidence_bundle filename (at least one of: delivery_proof_front.png / delivery_proof_label.png / payment_gateway.log)

C9 guard: representment_packet.md must NOT contain "full refund" as the agreed resolution.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    csv_decision = workspace / "output" / "decision_fields.csv"
    customer_email = workspace / "output" / "customer_email.md"
    packet = workspace / "output" / "representment_packet.md"

    for p in (csv_decision, customer_email, packet):
        if not p.exists():
            print(f"FAIL: {p} does not exist")
            return 1

    email_text  = customer_email.read_text(encoding="utf-8", errors="ignore")
    email_low   = email_text.lower()
    packet_text = packet.read_text(encoding="utf-8", errors="ignore")
    packet_low  = packet_text.lower()

    # Compute expected COMPLIANCE_CHECK token by running the wave3 tool
    verify = workspace / "tools" / "verify_dispute_signoff.py"
    if not verify.exists():
        print(f"FAIL: {verify} not found — cannot validate COMPLIANCE_CHECK token")
        return 1

    res = subprocess.run(
        [sys.executable, str(verify), str(csv_decision)],
        capture_output=True, text=True, timeout=30,
    )
    if res.returncode != 0:
        print(
            f"FAIL: verify_dispute_signoff.py rejected decision_fields.csv: "
            f"{res.stderr.strip()[:300]}"
        )
        return 1

    m = re.search(r"COMPLIANCE_CHECK:\s*([a-f0-9]{32})", res.stdout)
    if not m:
        stdout_preview = repr(res.stdout[:200])
        print(
            f"FAIL: verify_dispute_signoff.py did not emit COMPLIANCE_CHECK token; "
            f"stdout={stdout_preview}"
        )
        return 1
    expected_token = m.group(1)

    # Both files must contain the token
    if expected_token not in email_text:
        print(f"FAIL: customer_email.md missing COMPLIANCE_CHECK token ({expected_token})")
        return 1
    if expected_token not in packet_text:
        print(f"FAIL: representment_packet.md missing COMPLIANCE_CHECK token ({expected_token})")
        return 1

    # customer_email.md: order id + replacement
    if not re.search(r"nw-2026-04-a188", email_low):
        print("FAIL: customer_email.md must reference order id NW-2026-04-A188")
        return 1

    if not re.search(r"replacement|replace|补发|替换", email_low):
        print("FAIL: customer_email.md must reference the replacement resolution (补发/replacement)")
        return 1

    # customer_email.md: bilingual check (both Chinese and English expected)
    has_cn = bool(re.search(r"[一-鿿]", email_text))
    has_en = bool(re.search(r"\b(?:replacement|dear|customer|order)\b", email_text, re.IGNORECASE))
    if not (has_cn and has_en):
        # Soft warn only — bilingual preferred but not hard-fail
        print(
            f"  [warn] customer_email.md appears to be single-language "
            f"(Chinese={'yes' if has_cn else 'no'}, English={'yes' if has_en else 'no'}). "
            f"Bilingual preferred but not hard-failing."
        )

    # representment_packet.md: order id
    if not re.search(r"nw-2026-04-a188", packet_low):
        print("FAIL: representment_packet.md must reference order id NW-2026-04-A188")
        return 1

    # representment_packet.md: reason code
    if not re.search(r"4837", packet_low):
        print("FAIL: representment_packet.md must reference reason code 4837")
        return 1

    # representment_packet.md: 48-hour SLA reference
    if not re.search(r"\b48\b", packet_low):
        print("FAIL: representment_packet.md must reference the 48-hour SLA")
        return 1

    # representment_packet.md: evidence_bundle file mention (B 维度闭合)
    evidence_files = [
        r"delivery_proof_front\.png",
        r"delivery_proof_label\.png",
        r"payment_gateway\.log",
        r"evidence_bundle\.zip",
    ]
    if not any(re.search(pat, packet_low) for pat in evidence_files):
        print(
            "FAIL: representment_packet.md must mention at least one file from "
            "evidence_bundle.zip (e.g., delivery_proof_front.png, payment_gateway.log). "
            "This confirms the evidence bundle was reviewed."
        )
        return 1

    # C9 guard: NEITHER file may state "full refund" as the agreed resolution.
    # feedback.correct 明确要求 'Neither file contains full refund as the agreed
    # resolution'（含 customer_email.md），故该禁止校验同时覆盖 packet 与 email。
    # Allow "full refund" only if clearly discredited within a ±240-char window.
    # 注意：不得含 'replacement'/'rather'/'instead' —— 两份产物都题面强制提及
    # replacement agreement，这些词在任意 'full refund' 的 ±240 窗口内必然出现，
    # 会让错误锚定 'full refund' 被无条件放过。只保留真正表示“否定/纠正退款误读”的词。
    _discredit = re.compile(
        r"\b(?:not|no|decline|declined|denied|deny|reject|incorrect|wrong|"
        r"decoy|error|not.*agreed|did\s+not\s+agree|contrary|"
        r"refute|contradict)\b",
        re.IGNORECASE,
    )

    def _full_refund_undiscredited(text: str) -> bool:
        for m_fr in re.finditer(r"full\s+refund", text, re.IGNORECASE):
            start = max(0, m_fr.start() - 240)
            end   = min(len(text), m_fr.end() + 240)
            if not _discredit.search(text[start:end]):
                return True
        return False

    if _full_refund_undiscredited(packet_text):
        print(
            "FAIL (C9 guard): representment_packet.md contains 'full refund' "
            "without being discredited — that phrase is from the auto-generated "
            "ticket decoy. The customer accepted a replacement, not a cash refund. "
            "Do not propagate the decoy value."
        )
        return 1

    if _full_refund_undiscredited(email_text):
        print(
            "FAIL (C9 guard): customer_email.md contains 'full refund' "
            "without being discredited — the customer accepted a replacement (补发), "
            "not a cash refund. Neither output may present 'full refund' as the "
            "agreed resolution."
        )
        return 1

    print(
        f"PASS: COMPLIANCE_CHECK={expected_token[:8]}... + NW-2026-04-A188 + "
        f"replacement/补发 + 48h + evidence_bundle filename"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
