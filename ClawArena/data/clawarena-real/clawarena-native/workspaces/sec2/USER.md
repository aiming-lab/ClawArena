# People and Channels

## Primary User
- **Li Wei** — Security Engineer at NovaBridge. Leads the API key leak incident response.
  Prefers precise, concise deliverables with proper metadata fields (extracted_at, operator).
  Reviews by checking JSON schema shapes and cross-referencing sources.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Huang Min | Developer (key owner) | Slack DM | Made the leaking commit; claims he "already revoked" the key (unverified) |
| Manager Chen | Security Manager | Slack #security-incidents | Explicitly requested three-section Slack summary format |
| CTO Zhang | CTO | Feishu Group | Authorized scope expansion; requires Rationale sections in technical docs |
| DevOps Lead Wang | DevOps Lead | Feishu Group | Manages AWS credentials and CI/CD pipeline |
| Raj Kumar | External Security Consultant | Feishu DM | Provided authoritative advice on STS temporary credential handling |

## Channels
- **Slack #security-incidents**: Main incident coordination (Li Wei, Manager Chen, Huang Min)
- **Slack DM (Li Wei ↔ Huang Min)**: Technical details, Huang Min's unverified revocation claim
- **Feishu Group (incident-response)**: Management escalation (CTO, DevOps Lead)
- **Feishu DM (Li Wei ↔ Raj)**: STS credential handling consultation
- **Email (Li Wei → Manager Chen → CTO Zhang)**: Formal reporting chain
