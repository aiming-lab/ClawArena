# NebulaTech Ticket Operations Handbook
## Jira Service Management Operations Guide

**Version:** 1.4
**Effective Date:** 2024-06-01
**Owner:** Support Operations

---

## Chapter 1: Ticket Lifecycle

### 1.1 Ticket States

```
[New] → [In Progress] → [Pending Customer] → [Resolved] → [Closed]
           ↓                                       ↑
       [Escalated] ────────────────────────────────┘
```

### 1.2 State Definitions

| State | Description | SLA Clock |
|---|---|---|
| New | Created, awaiting first response | Running |
| In Progress | Engineer assigned, response sent | Stopped for first response |
| Pending Customer | Awaiting customer information | Paused |
| Resolved | Solution delivered | Final |
| Closed | Confirmed resolved by customer | Final |
| Escalated | Escalated to senior/management | Running (separate escalation SLA) |

### 1.3 SLA Clock Rules

The response SLA clock runs from `created_at` to `first_response_at`.

**Clock starts:** Immediately at ticket creation (no grace period)
**Clock stops:** First substantive response from a NebulaTech engineer
**Auto-ACK:** System acknowledgment emails do NOT stop the SLA clock
**Pending pause:** When ticket moves to "Pending Customer" state, the clock pauses

---

## Chapter 2: Severity Classification Guide

### 2.1 Decision Matrix

Use this matrix to assign severity:

```
Is the system completely unavailable for ALL users?
  YES → L1 (Production Down)
  NO  → Continue...

Are CORE features unavailable for SOME users?
  YES → L2 (Serious Degradation)
  NO  → Continue...

Is there a moderate impact with a workaround?
  YES → L3 (Moderate Impact)
  NO  → L4 (Limited Impact)
```

### 2.2 L1 Qualifying Scenarios

**Must classify as L1:**
- All ticket submissions failing (server error or timeout)
- Authentication system down
- Customer portal returning 500 for all users
- Data loss occurring or imminent
- Payments processing failing

**Do NOT classify as L1:**
- Single user unable to access (investigate individual issue)
- Intermittent errors affecting < 10% of users
- Non-production/staging environment issues
- Scheduled maintenance (planned downtime)

### 2.3 L2 Qualifying Scenarios

**Must classify as L2:**
- Ticket search returning incorrect results (all users)
- Email notifications failing for 30%+ of users
- Critical workflow blocked (e.g., approval process)
- Dashboard timeouts affecting all users

**Borderline L2/L3 cases:**
- Email notifications failing for < 10% of users → L3
- Intermittent API failures (< 5% error rate) → L3

---

## Chapter 3: Ticket Data Format

### 3.1 JSON Ticket Schema

All tickets are stored in the standardised JSON format:

```json
{
  "ticket_id": "STRING — unique identifier, format: {BATCH}-{SEVERITY}-{TYPE}-{NNN}",
  "severity": "ENUM: L1|L2|L3|L4",
  "status": "ENUM: open|in_progress|resolved|closed",
  "created_at": "ISO8601: YYYY-MM-DDTHH:MM:SSZ",
  "first_response_at": "ISO8601: YYYY-MM-DDTHH:MM:SSZ",
  "resolved_at": "ISO8601: YYYY-MM-DDTHH:MM:SSZ",
  "response_minutes": "INTEGER: ceil((first_response_at - created_at) / 60)"
}
```

### 3.2 Ticket ID Conventions

Format: `{BATCH}-{SEVERITY}-{TYPE}-{NNN}`

Examples:
- `Q4-L1-BREACH-001` — Q4 batch, L1 ticket, SLA breach, first ticket
- `Q4-L2-OK-005` — Q4 batch, L2 ticket, within SLA, fifth ticket
- `Q1-L3-BREACH-003` — Q1 batch, L3 ticket, SLA breach, third ticket
- `Q4-L2-NEARV2-001` — Q4 batch, L2 ticket, near threshold under v2 policy

### 3.3 Timestamp Standards

All timestamps in NebulaTech ticket data:
- **Format:** ISO 8601, always UTC, always with 'Z' suffix
- **Pattern:** `YYYY-MM-DDTHH:MM:SSZ`
- **Example:** `2024-10-15T14:23:00Z`

Non-conforming formats cause validation errors:
- `2024-10-15 14:23:00` (space separator) → INVALID
- `2024-10-15T14:23:00+05:30` (non-UTC) → INVALID (must convert to UTC)
- `2024-10-15` (date only) → INVALID

### 3.4 response_minutes Calculation

```python
def calc_response_minutes(created_at: str, first_response_at: str) -> int:
    from datetime import datetime
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    t_created = datetime.strptime(created_at, fmt)
    t_first = datetime.strptime(first_response_at, fmt)
    delta = t_first - t_created
    return int(delta.total_seconds() / 60)  # floor division
```

---

## Chapter 4: SLA Breach Report Format

### 4.1 Breach Ticket Entry Format

Each entry in breach_tickets_*.json:

```json
{
  "ticket_id": "string",
  "severity": "L1|L2|L3|L4",
  "expected_response_min": "int (30|90|120|480|1440 depending on version)",
  "actual_response_min": "int",
  "breach_delta_min": "int — must equal actual - expected"
}
```

**Critical:** `breach_delta_min = actual_response_min - expected_response_min`
If this arithmetic does not close, the entry fails validation.

### 4.2 Compliance Summary Format

```json
{
  "schema_version": "1.0",
  "metadata": {
    "generated_at": "ISO8601",
    "agent_id": "string",
    "schema_version": "1.0"
  },
  "sla_policy_version": "v1|v2|v3",
  "batch": "2024Q4|2025Q1",
  "total_tickets": "int",
  "by_severity": {
    "L1": {
      "total_count": "int",
      "breach_count": "int",
      "compliance_rate": "float (2 decimal places)"
    }
  }
}
```

### 4.3 Patch Application Process

When applying a patch (tickets_patch_NNN.json):

1. For each patch entry, update the ticket record:
   - `first_response_at` → use `corrected_first_response_at`
   - `response_minutes` → use `corrected_response_minutes`
2. Re-evaluate SLA breach status for patched tickets
3. Regenerate breach report with suffix `_v{N+1}` (e.g., breach_tickets_Q4_v3.json)

---

## Chapter 5: Escalation Report Requirements

### 5.1 Mandatory Fields

The monthly escalation report (escalation_report_YYYY_MM.json) MUST include:

1. `metadata` block (generated_at, agent_id, schema_version)
2. `report_period` (YYYY-MM format)
3. `sla_policy_version` (exact version in force during period)
4. `breach_summary` (total + by_severity breakdown)
5. `top_breached_tickets` (top 5 worst breaches)
6. `credit_recommendations` (with source URLs)
7. `reviewer_signature` (empty string or name)

### 5.2 sla_policy_version Accuracy

The `sla_policy_version` field must reflect the policy version **in force during
the reporting period**, not the current version.

Example:
- November 2024 tickets → use `sla_matrix_v1.json` (in effect until 2025-02-01)
- `sla_policy_version: "v1"` (correct)
- `sla_policy_version: "v2"` (WRONG — v2 was not in effect in November 2024)

### 5.3 Credit Recommendation Format

```json
{
  "service": "atlassian_cloud | ec2 | lambda",
  "actual_uptime_pct": "float (2 decimal places)",
  "applicable_tier": "string — verbatim tier description",
  "credit_pct": "int",
  "source_url": "string — exact URL from official documentation"
}
```

Source URLs must be exact:
- Atlassian: `https://www.atlassian.com/legal/sla`
- EC2: `https://aws.amazon.com/ec2/sla/`
- Lambda: `https://aws.amazon.com/lambda/sla/`

---

## Chapter 6: SHA-256 Sign-off Procedure

### 6.1 Purpose

All final deliverable sets are signed with a SHA-256 digest to ensure integrity.
This provides an audit trail that the filed report matches what was computed.

### 6.2 Sign-off Format

The sign-off file (`output/signoff.txt`) contains exactly one line:

```
VERIFIED:<64-character lowercase hex SHA-256 digest>
```

Example:
```
VERIFIED:a3f2c1d4e5b6a7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3
```

### 6.3 Computing the Digest

**Method:** SHA-256 of all JSON output files (sorted by path), concatenated:

```python
import hashlib
from pathlib import Path
import json

def compute_signoff(output_dir: Path) -> str:
    json_files = sorted(output_dir.glob("*.json"))
    hasher = hashlib.sha256()
    for f in json_files:
        hasher.update(f.read_bytes())
    return "VERIFIED:" + hasher.hexdigest()
```

**IMPORTANT:** The digest must be computed by actually executing the script.
Hand-typed or placeholder hashes will not match and will fail validation.

---

*End of Ticket Operations Handbook*
