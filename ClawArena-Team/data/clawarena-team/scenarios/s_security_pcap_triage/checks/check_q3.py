"""q3: findings/network_anomaly.md contains anomalous src IP and dest port.

Pass conditions (all required):
  1. findings/network_anomaly.md exists.
  2. Contains the anomalous source IP '10.42.7.183' as a complete dotted-quad
     token (not embedded inside a longer IP / numeric string).
  3. Contains the anomalous destination port '4444' as a standalone integer
     token (not embedded inside a longer number such as 14444 / 44440).

C3 hardening: the previous implementation used bare `"10.42.7.183" in text`
and `"4444" in text` substring checks. Those over-match:
  * `"4444"` is a substring of `14444`, `44440`, `144440`, ...
  * `"10.42.7.183"` is a substring of `110.42.7.1830`, `10.42.7.1831`, ...
The pcap also ships a syslog decoy (network_data/syslog_dump.log) full of
unrelated `DPT=4444` lines from external SRC IPs, so the port must be tied to
a clean boundary match rather than any loose digit run. We therefore require
boundary-anchored matches so only the true ground-truth values pass.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


ANOMALOUS_SRC_IP = "10.42.7.183"
ANOMALOUS_DEST_PORT = "4444"

# IP must appear as a full dotted-quad: not preceded/followed by a digit or a
# dot, so it is not a prefix/suffix of a longer IP-like or numeric token.
SRC_IP_RE = re.compile(
    r"(?<![\d.])" + re.escape(ANOMALOUS_SRC_IP) + r"(?![\d.])"
)

# Port must appear as a standalone integer: not flanked by other digits, so
# 14444 / 44440 / 144440 do not satisfy the check.
DEST_PORT_RE = re.compile(
    r"(?<!\d)" + re.escape(ANOMALOUS_DEST_PORT) + r"(?!\d)"
)


def main() -> int:
    ws = workspace_root()
    anomaly = ws / "findings" / "network_anomaly.md"
    if not anomaly.exists():
        fail("missing findings/network_anomaly.md")

    text = anomaly.read_text(encoding="utf-8", errors="ignore")

    if not SRC_IP_RE.search(text):
        fail(
            f"findings/network_anomaly.md does not contain the anomalous src IP "
            f"({ANOMALOUS_SRC_IP}) as a complete dotted-quad. The subagent must "
            f"parse the pcap binary to find it."
        )

    if not DEST_PORT_RE.search(text):
        fail(
            f"findings/network_anomaly.md does not contain the anomalous dest port "
            f"({ANOMALOUS_DEST_PORT}) as a standalone port number. Verify the "
            f"subagent actually parsed the pcap."
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
