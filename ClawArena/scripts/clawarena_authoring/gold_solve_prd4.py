#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_prd4.py — prd4 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_prd4.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "prd4"
UPD = DS / "openclaw" / "updates" / "prd4"
SCRIPTS = DS / "eval" / "prd4" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/prd4_gold_ws")


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _now_iso() -> str:
    """Return current UTC time as ISO 8601 with Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


def prep_workspace() -> Path:
    """复制 workspace 到临时目录，应用所有 update workspace 文件。"""
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)

    # Apply Update-1 workspace files
    for name, target in [
        ("sla_matrix_v2.json", "policy/sla_matrix_v2.json"),
        ("escalation_policy_v2.md", "policy/escalation_policy_v2.md"),
        ("tickets_batch_2025Q1_extra.json", "tickets/tickets_batch_2025Q1_extra.json"),
    ]:
        src = UPD / "upd1_workspace" / name
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)

    # Apply Update-2 workspace files
    for name, target in [
        ("tickets_patch_001.json", "tickets/tickets_patch_001.json"),
        ("monthly_sla_report_2024_11_draft_v2.md", "reports/monthly_sla_report_2024_11_draft_v2.md"),
    ]:
        src = UPD / "upd2_workspace" / name
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)

    return GOLD


# ─── 金标数据计算 ─────────────────────────────────────────────────────────────

SLA_V1 = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}
SLA_V2 = {"L1": 30, "L2": 90, "L3": 480, "L4": 1440}
SLA_V3 = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}  # reverted


def _load_tickets(ws: Path, filename: str) -> list[dict]:
    """加载工单文件，返回 tickets list。"""
    data = json.loads((ws / "tickets" / filename).read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("tickets", [])


def _compute_breaches(tickets: list[dict], sla: dict) -> list[dict]:
    """计算违约工单列表，含 expected/actual/delta 字段。"""
    result = []
    for t in tickets:
        sev = t["severity"]
        expected = sla[sev]
        actual = t["response_minutes"]
        if actual > expected:
            result.append({
                "ticket_id": t["ticket_id"],
                "severity": sev,
                "expected_response_min": expected,
                "actual_response_min": actual,
                "breach_delta_min": actual - expected,
            })
    return result


def _apply_patch(tickets: list[dict], patches: list[dict]) -> list[dict]:
    """应用工单补丁，返回修改后的 tickets map → list。"""
    ticket_map = {t["ticket_id"]: dict(t) for t in tickets}
    for p in patches:
        tid = p["ticket_id"]
        if tid in ticket_map:
            ticket_map[tid]["first_response_at"] = p["corrected_first_response_at"]
            ticket_map[tid]["response_minutes"] = p["corrected_response_minutes"]
    return list(ticket_map.values())


def _make_metadata() -> dict:
    return {
        "generated_at": _now_iso(),
        "agent_id": "supportops-ai",
        "schema_version": "1.0",
    }


def solve(ws: Path) -> None:
    """写出全部金标产物到 ws/output/。"""
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # 加载工单数据
    q4_tickets = _load_tickets(ws, "tickets_batch_2024Q4.json")
    q1_tickets = _load_tickets(ws, "tickets_batch_2025Q1.json")
    patch_data = json.loads((ws / "tickets" / "tickets_patch_001.json").read_text())
    patches = patch_data.get("patches", [])

    # ── Q1: policy_summary.json ──────────────────────────────────────────────
    sla_v1_data = json.loads((ws / "policy" / "sla_matrix_v1.json").read_text())
    _wj(out / "policy_summary.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v1",
        "plan": sla_v1_data["plan"],
        "availability_commitment_pct": 99.95,
        "response_sla": {
            "L1": {"response_minutes": 30, "coverage": "24/7"},
            "L2": {"response_minutes": 120, "coverage": "24/7"},
            "L3": {"response_minutes": 480, "coverage": "weekdays"},
            "L4": {"response_minutes": 1440, "coverage": "weekdays"},
        },
        "credit_tiers": [
            {"tier": "tier0", "credit_pct": 5, "uptime_range": "99.90%–99.95%"},
            {"tier": "tier1", "credit_pct": 10, "uptime_range": "99.00%–99.90%"},
            {"tier": "tier2", "credit_pct": 25, "uptime_range": "95.00%–99.00%"},
            {"tier": "tier3", "credit_pct": 50, "uptime_range": "< 95.00%"},
        ],
        "reviewer_signature": "",
    })

    # ── Q2: archive_audit.json ────────────────────────────────────────────────
    _wj(out / "archive_audit.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "is_superseded": True,
        "superseded_date": "2024-01-01T00:00:00Z",
        "archived_file": "policy/ARCHIVED_sla_matrix_v0.json",
        "current_file": "policy/sla_matrix_v1.json",
        "incorrect_fields": [
            {
                "field_path": "response_sla.L1.response_minutes",
                "archived_value": 60,
                "correct_value": 30,
                "note": "Enterprise L1 is 30 min (24/7); 1h was erroneous legacy value from v0"
            }
        ],
        "reviewer_signature": "",
    })

    # ── Q3: breach_tickets_Q4.json (v1 policy) ────────────────────────────────
    breaches_q4_v1 = _compute_breaches(q4_tickets, SLA_V1)
    _wj(out / "breach_tickets_Q4.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v1",
        "batch": "2024Q4",
        "total_analyzed": len(q4_tickets),
        "breach_count": len(breaches_q4_v1),
        "tickets": breaches_q4_v1,
        "reviewer_signature": "",
    })

    # ── Q4: email_audit.json (honeypot detection) ─────────────────────────────
    _wj(out / "email_audit.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "honeypot_detected": True,
        "claimed_value": "1h",
        "correct_value": "30min",
        "discrepancy_note": "Email auto-summary (Carol Davis, 2026-04-03) stated L1=1h; "
                           "authoritative value is 30min per Atlassian Enterprise plan",
        "authoritative_source": "atlassian-support-offerings",
        "source_url": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html",
        "reviewer_signature": "",
    })

    # ── Q5: sla_compliance_Q4.json (cross-round closure with Q3) ─────────────
    q4_total = len(q4_tickets)
    q4_breach_count = len(breaches_q4_v1)

    # by_severity stats
    from collections import defaultdict
    sev_total: dict = defaultdict(int)
    sev_breach: dict = defaultdict(int)
    for t in q4_tickets:
        sev_total[t["severity"]] += 1
    for t in breaches_q4_v1:
        sev_breach[t["severity"]] += 1

    by_sev = {}
    for sev in ["L1", "L2", "L3", "L4"]:
        tot = sev_total[sev]
        brc = sev_breach[sev]
        rate = round((tot - brc) / tot * 100, 2) if tot > 0 else 100.00
        by_sev[sev] = {
            "total_count": tot,
            "breach_count": brc,
            "compliance_rate": rate,
        }

    overall_rate = round((q4_total - q4_breach_count) / q4_total * 100, 2) if q4_total > 0 else 100.00
    _wj(out / "sla_compliance_Q4.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "batch": "2024Q4",
        "total_count": q4_total,
        "breach_count": q4_breach_count,
        "compliance_rate": overall_rate,
        "by_severity": by_sev,
        "reviewer_signature": "",
    })

    # ── Q6: credit_calc_atlassian.json ────────────────────────────────────────
    # 99.92% uptime → Enterprise tier0 (99.90–99.95%) → 5% credit
    # monthly contract = 10000 USD → credit = 500.00
    _wj(out / "credit_calc_atlassian.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "service": "atlassian_cloud",
        "actual_uptime_pct": 99.92,
        "applicable_tier": "99.90%–99.95%",
        "credit_pct": 5,
        "credit_amount_usd": 500.00,
        "monthly_contract_value_usd": 10000.00,
        "source_url": "https://www.atlassian.com/legal/sla",
        "reviewer_signature": "",
    })

    # ── Q7: breach_tickets_Q4_v2.json (L2=90min, after Update-1) ──────────────
    breaches_q4_v2 = _compute_breaches(q4_tickets, SLA_V2)
    _wj(out / "breach_tickets_Q4_v2.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v2",
        "batch": "2024Q4",
        "total_analyzed": len(q4_tickets),
        "breach_count": len(breaches_q4_v2),
        "tickets": breaches_q4_v2,
        "reviewer_signature": "",
    })

    # ── Q8: conflict_resolution.json ──────────────────────────────────────────
    _wj(out / "conflict_resolution.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "topic": "L2 response SLA threshold",
        "alice_claimed": "2h (120min) — original v1 policy value",
        "bob_claimed": "90min — proposed tightening per draft v2",
        "adopted_value": "90min",
        "source_authority": "sla_matrix_v2",
        "resolution_basis": "Update-1 introduced sla_matrix_v2 which formally sets L2=90min; "
                           "this supersedes v1 L2=120min as of 2025-02-01",
        "reviewer_signature": "",
    })

    # ── Q9: breach_tickets_Q1.json (v2 policy: L2=90min) ─────────────────────
    breaches_q1_v2 = _compute_breaches(q1_tickets, SLA_V2)
    _wj(out / "breach_tickets_Q1.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v2",
        "batch": "2025Q1",
        "total_analyzed": len(q1_tickets),
        "breach_count": len(breaches_q1_v2),
        "tickets": breaches_q1_v2,
        "reviewer_signature": "",
    })

    # ── Q10: combined_breach_summary.json ─────────────────────────────────────
    # total_tickets = Q4(200) + Q1(150) = 350
    # total_breaches = Q7(31) + Q9(19) = 50
    total_all = len(q4_tickets) + len(q1_tickets)
    total_breach_all = len(breaches_q4_v2) + len(breaches_q1_v2)
    breach_pct_all = round(total_breach_all / total_all * 100, 2)

    # combined by_severity
    combined_sev_total: dict = defaultdict(int)
    combined_sev_breach: dict = defaultdict(int)
    for t in q4_tickets + q1_tickets:
        combined_sev_total[t["severity"]] += 1
    for t in breaches_q4_v2 + breaches_q1_v2:
        combined_sev_breach[t["severity"]] += 1

    combined_by_sev = {}
    for sev in ["L1", "L2", "L3", "L4"]:
        tot = combined_sev_total[sev]
        brc = combined_sev_breach[sev]
        rate = round((tot - brc) / tot * 100, 2) if tot > 0 else 100.00
        combined_by_sev[sev] = {
            "total_count": tot,
            "breach_count": brc,
            "compliance_rate": rate,
        }

    _wj(out / "combined_breach_summary.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "batches": ["2024Q4", "2025Q1"],
        "total_tickets": total_all,
        "total_breaches": total_breach_all,
        "breach_pct": breach_pct_all,
        "by_severity": combined_by_sev,
        "reviewer_signature": "",
    })

    # ── Q11: breach_tickets_Q4_v3.json (L2 reverted to 120, patch applied) ────
    # V10 supersede: Update-2 reverts L2 to 120min (supersedes Update-1's 90min)
    # Also apply tickets_patch_001 corrections
    q4_patched = _apply_patch(q4_tickets, patches)
    breaches_q4_v3 = _compute_breaches(q4_patched, SLA_V3)  # L2=120
    _wj(out / "breach_tickets_Q4_v3.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v3",
        "batch": "2024Q4",
        "total_analyzed": len(q4_patched),
        "breach_count": len(breaches_q4_v3),
        "supersede_notice": "FEISHU-PRD4-L2-REVERT: L2 reverted from 90min to 120min; "
                           "tickets_patch_001 corrections applied",
        "tickets": breaches_q4_v3,
        "reviewer_signature": "",
    })

    # ── Q12: escalation_report_2024_11.json ───────────────────────────────────
    # November 2024 tickets only, v1 policy (predates both updates)
    nov_tickets = [t for t in q4_tickets if "2024-11" in t.get("created_at", "")]
    nov_breach_v1 = _compute_breaches(nov_tickets, SLA_V1)

    nov_sev_total: dict = defaultdict(int)
    nov_sev_breach: dict = defaultdict(int)
    for t in nov_tickets:
        nov_sev_total[t["severity"]] += 1
    for t in nov_breach_v1:
        nov_sev_breach[t["severity"]] += 1

    nov_by_sev = {}
    for sev in ["L1", "L2", "L3", "L4"]:
        tot = nov_sev_total[sev]
        brc = nov_sev_breach[sev]
        rate = round((tot - brc) / tot * 100, 2) if tot > 0 else 100.00
        nov_by_sev[sev] = {
            "total_count": tot,
            "breach_count": brc,
            "compliance_rate": rate,
        }

    nov_total_tickets = len(nov_tickets)
    nov_total_breaches = len(nov_breach_v1)
    nov_breach_pct = round(nov_total_breaches / nov_total_tickets * 100, 2) if nov_total_tickets > 0 else 0.00

    top5 = sorted(nov_breach_v1, key=lambda t: t["breach_delta_min"], reverse=True)[:5]

    _wj(out / "escalation_report_2024_11.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "report_period": "2024-11",
        "sla_policy_version": "v1",
        "breach_summary": {
            "total_tickets": nov_total_tickets,
            "total_breaches": nov_total_breaches,
            "breach_pct": nov_breach_pct,
            "by_severity": nov_by_sev,
        },
        "top_breached_tickets": top5,
        "credit_recommendations": [
            {
                "service": "atlassian_cloud",
                "actual_uptime_pct": 99.92,
                "applicable_tier": "99.90%–99.95%",
                "credit_pct": 5,
                "source_url": "https://www.atlassian.com/legal/sla",
            }
        ],
        "reviewer_signature": "",
    })

    # ── Q13: incident_timeline.json ───────────────────────────────────────────
    # INC-2026-04-001: detected=07:45Z, first_response=08:12Z, resolved=10:45Z
    # mttd = 27 min, mttr = 153 min, sla_breach = false (27 < 30)
    _wj(out / "incident_timeline.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "incident_id": "INC-2026-04-001",
        "severity": "L1",
        "issue_detected_at": "2026-04-04T07:45:00Z",
        "first_response_at": "2026-04-04T08:12:00Z",
        "resolved_at": "2026-04-04T10:45:00Z",
        "mttd_min": 27,
        "mttr_min": 153,
        "sla_breach": False,
        "sla_threshold_min": 30,
        "notes": "mttd=27min (< L1 threshold 30min); SLA met. MTTR=153min.",
        "reviewer_signature": "",
    })

    # ── Q14: validation_result.json (run validate_ticket_sla.py) ─────────────
    # Run the validation script against breach_tickets_Q4_v3.json
    import subprocess as sp
    script = ws / "scripts" / "validate_ticket_sla.py"
    breach_v3_path = out / "breach_tickets_Q4_v3.json"
    result = sp.run(
        [sys.executable, str(script), str(breach_v3_path)],
        capture_output=True, text=True, timeout=30
    )
    try:
        script_out = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        script_out = {"validated_count": 0, "error_count": 0, "invalid_ticket_ids": [],
                      "error": result.stdout.strip()}

    _wj(out / "validation_result.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "validated_count": script_out.get("validated_count", 0),
        "error_count": script_out.get("error_count", 0),
        "invalid_ticket_ids": script_out.get("invalid_ticket_ids", []),
        "reviewer_signature": "",
    })

    # ── Q15: aws_credit_calc.json ─────────────────────────────────────────────
    # EC2 uptime 98.5% → 95.0-99.0% tier → 30% credit
    # Nov 2024 incident → second billing cycle ends 2025-01-31
    _wj(out / "aws_credit_calc.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "service": "ec2",
        "actual_uptime_pct": 98.5,
        "applicable_tier": "95.0%–99.0%",
        "credit_pct": 30,
        "claim_deadline": "2025-01-31",
        "incident_month": "2024-11",
        "source_url": "https://aws.amazon.com/ec2/sla/",
        "reviewer_signature": "",
    })

    # ── Q16: sla_comparison.json ──────────────────────────────────────────────
    comparison_items = [
        {
            "vendor": "Atlassian",
            "metric_name": "Premium Monthly Uptime Commitment",
            "value": "99.90%",
            "source_url": "https://www.atlassian.com/legal/sla",
        },
        {
            "vendor": "Atlassian",
            "metric_name": "Enterprise Monthly Uptime Commitment",
            "value": "99.95%",
            "source_url": "https://www.atlassian.com/legal/sla",
        },
        {
            "vendor": "AWS",
            "metric_name": "EC2 Region-Level Monthly Uptime Commitment",
            "value": "99.99%",
            "source_url": "https://aws.amazon.com/ec2/sla/",
        },
        {
            "vendor": "AWS",
            "metric_name": "Lambda Monthly Uptime Commitment",
            "value": "99.95%",
            "source_url": "https://aws.amazon.com/lambda/sla/",
        },
        {
            "vendor": "AWS",
            "metric_name": "EC2 Instance-Level Monthly Uptime Commitment",
            "value": "99.5%",
            "source_url": "https://aws.amazon.com/ec2/sla/",
        },
    ]
    _wj(out / "sla_comparison.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "comparison_items": comparison_items,
        "reviewer_signature": "",
    })

    # ── Q17: signoff.txt — SHA-256 of sorted output/*.json bytes ─────────────
    json_files = sorted(f for f in out.glob("*.json") if f.is_file())
    hasher = hashlib.sha256()
    for f in json_files:
        hasher.update(f.read_bytes())
    digest = hasher.hexdigest()
    _w(out / "signoff.txt", f"VERIFIED:{digest}\n")

    # Report stats
    q4_count = len(q4_tickets)
    q1_count = len(q1_tickets)
    v1_breaches = len(breaches_q4_v1)
    v2_breaches = len(breaches_q4_v2)
    q1_breaches = len(breaches_q1_v2)
    v3_breaches = len(breaches_q4_v3)
    print(f"  Q4 tickets={q4_count}, breaches@v1={v1_breaches}, @v2={v2_breaches}, @v3={v3_breaches}")
    print(f"  Q1 tickets={q1_count}, breaches@v2={q1_breaches}")
    print(f"  Combined total={total_all}, breaches={total_breach_all}, pct={breach_pct_all:.2f}%")
    print(f"  Nov2024 tickets={nov_total_tickets}, breaches={nov_total_breaches}")


# ─── 运行 check ──────────────────────────────────────────────────────────────

EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1,P2", "output/policy_summary.json")],
    "q2": ["check_q2.py", ("pref", "P1,P2", "output/archive_audit.json")],
    "q3": ["check_q3.py", ("pref", "P1,P2,P3", "output/breach_tickets_Q4.json")],
    "q4": ["check_q4.py", ("pref", "P1,P2", "output/email_audit.json")],
    "q5": ["check_q5.py", ("pref", "P1,P2,P4", "output/sla_compliance_Q4.json")],
    "q6": ["check_q6.py", ("pref", "P1,P2,P4,P5", "output/credit_calc_atlassian.json")],
    "q7": ["check_q7.py", ("pref", "P1,P2,P3,P4", "output/breach_tickets_Q4_v2.json")],
    "q8": ["check_q8.py", ("pref", "P1,P2", "output/conflict_resolution.json")],
    "q9": ["check_q9.py"],
    "q10": ["check_q10.py", ("pref", "P1,P2,P4", "output/combined_breach_summary.json")],
    "q11": ["check_q11.py", ("pref", "P1,P2,P3,P4", "output/breach_tickets_Q4_v3.json")],
    "q12": ["check_q12.py", ("pref", "P1,P2,P4,P5", "output/escalation_report_2024_11.json")],
    "q13": ["check_q13.py", ("pref", "P1,P2,P3", "output/incident_timeline.json")],
    "q14": ["check_q14.py", ("pref", "P1,P2,P4", "output/validation_result.json")],
    "q15": ["check_q15.py", ("pref", "P1,P2,P4,P5", "output/aws_credit_calc.json")],
    "q16": ["check_q16.py", ("pref", "P1,P2,P4,P5", "output/sla_comparison.json")],
    "q17": ["check_q17.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws),
               "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    last = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else ""
    return r.returncode == 0, last


def main():
    print("Preparing workspace copy with all updates applied...")
    ws = prep_workspace()
    print("Running gold solution...")
    solve(ws)

    print("\n=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                # print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ── 反例抽样（不过松验证）────────────────────────────────────────────────
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # Probe 1: Q1 wrong L1 (60min from archived v0 — the honeypot)
    _wj(ws / "output" / "policy_summary.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v1",
        "plan": "Atlassian Enterprise",
        "availability_commitment_pct": 99.95,
        "response_sla": {
            "L1": {"response_minutes": 60, "coverage": "24/7"},  # WRONG: archived v0 value
            "L2": {"response_minutes": 120, "coverage": "24/7"},
        },
        "credit_tiers": [{"tier": "tier0", "credit_pct": 5, "uptime_range": "99.90%–99.95%"}],
        "reviewer_signature": "",
    })
    ok, _ = run_check("check_q1.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q1 wrong L1=60min (archived v0) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 2: Q6 wrong credit_pct=10 (Premium tier, not Enterprise tier0)
    _wj(ws / "output" / "credit_calc_atlassian.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "service": "atlassian_cloud",
        "actual_uptime_pct": 99.92,
        "applicable_tier": "99.00%–99.90%",  # WRONG tier
        "credit_pct": 10,  # WRONG: should be 5 for 99.90-99.95%
        "credit_amount_usd": 1000.00,
        "source_url": "https://www.atlassian.com/legal/sla",
        "reviewer_signature": "",
    })
    ok, _ = run_check("check_q6.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q6 wrong credit_pct=10 (should be 5 for Enterprise tier0) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 3: Q7 L2 threshold still 120 (didn't apply v2 update)
    breaches_q4_v1_wrong = []
    q4_tickets = _load_tickets(ws, "tickets_batch_2024Q4.json")
    for t in q4_tickets:
        exp = SLA_V1[t["severity"]]  # Wrong: still using v1, not v2 (should be 90 for L2)
        act = t["response_minutes"]
        if act > exp:
            breaches_q4_v1_wrong.append({
                "ticket_id": t["ticket_id"],
                "severity": t["severity"],
                "expected_response_min": exp,
                "actual_response_min": act,
                "breach_delta_min": act - exp,
            })
    _wj(ws / "output" / "breach_tickets_Q4_v2.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v2",  # claims v2 but uses v1 thresholds
        "tickets": breaches_q4_v1_wrong,  # 28 entries, not 31
    })
    ok, _ = run_check("check_q7.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q7 L2 still 120min (v1 not updated) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4: Q11 L2 still 90 (didn't revert — supersede not applied)
    breaches_v2_wrong = _compute_breaches(q4_tickets, SLA_V2)  # still using 90min
    _wj(ws / "output" / "breach_tickets_Q4_v3.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v3",
        "supersede_notice": "FEISHU-PRD4-L2-REVERT applied",
        "tickets": breaches_v2_wrong,  # WRONG: still using 90min threshold
    })
    ok, _ = run_check("check_q11.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q11 L2 still 90min (supersede not applied) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 5: Q17 placeholder hash
    _w(ws / "output" / "signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q17.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q17 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 6: Q5 wrong total_count (wrong cross-round closure)
    _wj(ws / "output" / "sla_compliance_Q4.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "total_count": 200,
        "breach_count": 20,  # WRONG: does not match Q3 file
        "compliance_rate": 90.00,
        "by_severity": {},
        "reviewer_signature": "",
    })
    ok, _ = run_check("check_q5.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q5 wrong breach_count (cross-round closure fail) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 7: Q1 missing L3/L4 in response_sla (only L1/L2 provided)
    _wj(ws / "output" / "policy_summary.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "sla_policy_version": "v1",
        "plan": "Atlassian Enterprise",
        "availability_commitment_pct": 99.95,
        "response_sla": {
            "L1": {"response_minutes": 30, "coverage": "24/7"},
            "L2": {"response_minutes": 120, "coverage": "24/7"},
            # MISSING L3=480, L4=1440
        },
        "credit_tiers": [
            {"tier": "tier0", "credit_pct": 5, "uptime_range": "99.90%–99.95%"},
            {"tier": "tier1", "credit_pct": 10, "uptime_range": "99.00%–99.90%"},
            {"tier": "tier2", "credit_pct": 25, "uptime_range": "95.00%–99.00%"},
            {"tier": "tier3", "credit_pct": 50, "uptime_range": "< 95.00%"},
        ],
        "reviewer_signature": "",
    })
    ok, _ = run_check("check_q1.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q1 missing L3/L4 in response_sla -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 8: Q13 missing sla_threshold_min field
    _wj(ws / "output" / "incident_timeline.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "incident_id": "INC-2026-04-001",
        "severity": "L1",
        "issue_detected_at": "2026-04-04T07:45:00Z",
        "first_response_at": "2026-04-04T08:12:00Z",
        "resolved_at": "2026-04-04T10:45:00Z",
        "mttd_min": 27,
        "mttr_min": 153,
        "sla_breach": False,
        # MISSING sla_threshold_min
        "reviewer_signature": "",
    })
    ok, _ = run_check("check_q13.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q13 missing sla_threshold_min -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 9: Q16 wrong source_url for EC2 (missing trailing slash)
    _wj(ws / "output" / "sla_comparison.json", {
        "metadata": _make_metadata(),
        "schema_version": "1.0",
        "comparison_items": [
            {"vendor": "Atlassian", "metric_name": "Premium Uptime", "value": "99.90%",
             "source_url": "https://www.atlassian.com/legal/sla"},
            {"vendor": "Atlassian", "metric_name": "Enterprise Uptime", "value": "99.95%",
             "source_url": "https://www.atlassian.com/legal/sla"},
            {"vendor": "AWS", "metric_name": "EC2 Region Uptime", "value": "99.99%",
             "source_url": "https://aws.amazon.com/ec2/sla"},  # WRONG: missing trailing slash
            {"vendor": "AWS", "metric_name": "Lambda Uptime", "value": "99.95%",
             "source_url": "https://aws.amazon.com/lambda/sla/"},
        ],
        "reviewer_signature": "",
    })
    ok, _ = run_check("check_q16.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q16 EC2 source_url missing trailing slash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
