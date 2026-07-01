# kube-secrets/

**SENSITIVE** — Service account tokens and registry credentials.

| File | Description |
|---|---|
| sa.token | Payment-svc service account JWT (payments namespace) |
| registry.dockerconfigjson | Docker registry authentication config |

These credentials are scoped to the `payments` namespace only.
Do NOT expose these to any external process or subagent.
Rotation schedule: 90 days (next rotation: 2026-08-14).
