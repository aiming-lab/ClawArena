"""IronClaw engine — CLI subprocess (Rust binary with libSQL)."""

from __future__ import annotations

from pathlib import Path

from clawarena.core.types import WorkCopy
from clawarena.engines.cli_subprocess import CLISubprocessEngine


class IronClawEngine(CLISubprocessEngine):
    """IronClaw engine using ``ironclaw -m`` CLI.

    IronClaw outputs the agent reply as plain text on stdout.
    Data isolation via ``IRONCLAW_BASE_DIR`` + libSQL embedded database.
    No gateway required (``ironclaw -m`` is self-contained).
    """

    def build_cwd(self, work_copy: WorkCopy, agent_id: str | None) -> Path:
        """Use the agent's workspace dir as CWD so relative file paths resolve correctly."""
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.project_root

    def build_agent_cmd(self, session_id: str, message: str) -> list[str]:
        return ["ironclaw", "-m", message]

    def build_env(
        self, work_copy: WorkCopy, gateway_port: int | None
    ) -> dict[str, str]:
        cc = work_copy.extra.get("ironclaw_config", {})
        env: dict[str, str] = {
            "IRONCLAW_BASE_DIR": str(work_copy.state_dir),
            "DATABASE_BACKEND": "libsql",
            "LIBSQL_PATH": str(work_copy.state_dir / "ironclaw.db"),
        }
        master_key = cc.get("secrets_master_key")
        if master_key:
            env["SECRETS_MASTER_KEY"] = master_key
        env.update(cc.get("env", {}))
        return env
