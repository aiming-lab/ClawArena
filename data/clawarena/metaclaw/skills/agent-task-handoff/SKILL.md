---
name: agent-task-handoff
description: Use this skill when delegating a subtask to a sub-agent, spawning a parallel worker, or handing off work across sessions. Write a self-contained task description so the receiving agent needs no prior context.
category: agentic
---

# Agent Task Handoff

When delegating work to a sub-agent or across sessions, make the handoff self-contained.

**Handoff package must include:**
1. **Goal:** What the sub-agent must produce (one clear sentence).
2. **Context:** The minimum background the agent needs — no more, no less.
3. **Constraints:** Explicit rules (don't modify X, use library Y, output format Z).
4. **Inputs:** File paths, API endpoints, or data the agent needs to start.
5. **Success criteria:** How to verify the result is correct.

**For parallel agents:**
- Clearly state which parts of the codebase/data each agent owns.
- Define how outputs will be merged back.

**Anti-pattern:** Sending a vague "continue where we left off" with no context — sub-agents start from zero.
