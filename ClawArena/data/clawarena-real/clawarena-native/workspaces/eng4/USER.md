# Team Members and Channels

## Primary User
- **Li Wei** — DBA Engineer (agent role). Owns the slow-query investigation and optimization.
  Writes all deliverables to `work/`. Prefers snake_case JSON, CONCURRENTLY on all production DDL.

## Key Stakeholders

| Name        | Role                   | Channel               | Notes |
|-------------|------------------------|-----------------------|-------|
| Sreedhar    | Senior DBA Consultant  | Slack DM              | Provides detailed optimization advice; occasionally suggests suboptimal approaches (double-check against official docs) |
| Alex Reeves | CTO                    | Email                 | Escalates performance SLAs; may issue directives that get superseded by architecture review |
| Maya Lin    | Principal Architect    | Email                 | Final technical authority; can supersede CTO directives on implementation approach |
| On-call     | On-call rotation       | Feishu #oncall-alerts | Night-time alert handling; includes tool_call traces |

## Channels
- **Slack #dba-alerts**: Group DBA channel — team-wide alerts and triage discussion
- **Slack DM (Li Wei ↔ Sreedhar)**: Detailed technical advice; Sreedhar sometimes quotes from Slack bot summaries (unreliable)
- **Email (Alex Reeves → DBA team)**: Executive performance directives
- **Email (Maya Lin → DBA team)**: Architecture review decisions (authoritative, may supersede CTO)
- **Feishu #oncall-alerts**: Night-shift operational notes
