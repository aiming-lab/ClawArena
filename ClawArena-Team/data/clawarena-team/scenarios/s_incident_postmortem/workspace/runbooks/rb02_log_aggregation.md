# Log aggregation and remote search

## Symptoms

Operators usually encounter this scenario after a paging alert. The on-call
dashboard surfaces a sustained anomaly on the primary indicator metric.
Common precursors include heightened p99 latency, retries, or 5xx ratios.

## Containment

1. Confirm the alert with a cross-check against the platform-level dashboard.
2. Page the secondary on-call if the primary indicator does not subside within
   five minutes.
3. If user-facing endpoints are degraded, post a status-page update under the
   'investigating' severity. Avoid speculative root cause statements.

## Investigation

Engineers should follow these steps in order, falling back to the next when a
step does not yield a clear signal within ten minutes.

### Step 01 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 02 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 03 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 04 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 05 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 06 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 07 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 08 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 09 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 10 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 11 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 12 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 13 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 14 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 15 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 16 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 17 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 18 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 19 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 20 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 21 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 22 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 23 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

### Step 24 — observation and follow-up

Inspect the affected service's structured log stream for the relevant request id family. Cross-reference against the request graph stored in the trace store. Capture any anomalous spans for later review.

Note: this step occasionally surfaces a false positive on cache eviction metrics when the upstream caller experiences memory pressure; treat the eviction count as a downstream symptom, not the cause.

## Remediation

Once the immediate user-facing symptom subsides, capture the contributing
conditions in the post-incident note. The runbook author should review
this list quarterly.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

## Additional observations

Operators encountering a variant of this signature should add a note here.
Past incidents that touched this runbook are tracked in the postmortem
archive under `archive/`. Do not modify the canonical text without an
ADR review.

