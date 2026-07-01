"""Example adapter plugin — demonstrates how to register an external framework.

Usage:
    clawarena infer --data tests.json --framework echo --out results/ \
        --plugin src/clawarena/plugins/example.py

This registers a minimal "echo" framework that simply echoes the query
back as the agent's answer. Useful for testing the pipeline end-to-end
without a real agent.
"""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.adapters.base import FrameworkAdapter
from clawarena.adapters.registry import register_adapter
from clawarena.core.types import AgentResult, RoundContext, RoundResult, WorkCopy
from clawarena.data_handlers.base import DataHandler
from clawarena.engines.base import AgentEngine


# ---------------------------------------------------------------------------
# Engine: echoes the message back as the answer
# ---------------------------------------------------------------------------

class EchoEngine(AgentEngine):

    async def run_agent(
        self, session_id, message, work_copy,
        agent_id=None, gateway_port=None, timeout=None,
    ) -> AgentResult:
        return AgentResult(status="success", answer=message)

    async def on_round_complete(self, ctx: RoundContext) -> RoundResult | None:
        """Optional hook — attach round metadata as extra data."""
        return RoundResult(extra_data={
            "echo_round": ctx.round_index,
            "echo_passed": ctx.inline_score.get("passed", False),
        })


# ---------------------------------------------------------------------------
# DataHandler: minimal no-op implementation
# ---------------------------------------------------------------------------

class EchoDataHandler(DataHandler):

    def load_manifest(self, manifest_path: Path) -> dict:
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def validate(self, manifest, manifest_dir, eval_dir, test_entries):
        return []

    def prepare_work_copy(self, manifest, manifest_dir, project_root):
        state = manifest_dir / "state"
        state.mkdir(parents=True, exist_ok=True)
        return WorkCopy(
            state_dir=state, config_path=None,
            project_root=project_root,
            extra={"manifest": manifest, "manifest_dir": manifest_dir},
        )

    def init_session(self, work_copy, test_id):
        return f"echo_{test_id}"

    def execute_update(self, update_id, work_copy, test_id, session_id):
        pass

    def resolve_workspace(self, work_copy, test_id):
        return None


# ---------------------------------------------------------------------------
# Registration — executed when the file is loaded via --plugin
# ---------------------------------------------------------------------------

register_adapter("echo", lambda: FrameworkAdapter(
    name="echo",
    engine=EchoEngine(),
    data_handler=EchoDataHandler(),
))
