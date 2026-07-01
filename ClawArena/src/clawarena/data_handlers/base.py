"""Abstract base class for framework data handlers."""

from __future__ import annotations

import os
import logging
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

from clawarena.core.types import WorkCopy

logger = logging.getLogger(__name__)


class DataHandler(ABC):
    """Base class for framework-specific data handling."""

    # ── Manifest ──────────────────────────────────────

    @abstractmethod
    def load_manifest(self, manifest_path: Path) -> dict:
        """Load manifest.json. manifest_path is absolute."""

    # ── Validation ────────────────────────────────────

    @abstractmethod
    def validate(
        self,
        manifest: dict,
        manifest_dir: Path,
        eval_dir: Path,
        test_entries: list[dict],
    ) -> list[str]:
        """Validate framework data. Return list of errors (empty = pass)."""

    # ── Work Copy ─────────────────────────────────────

    @abstractmethod
    def prepare_work_copy(
        self,
        manifest: dict,
        manifest_dir: Path,
        project_root: Path,
    ) -> WorkCopy:
        """Create an isolated working copy."""

    def rebuild_work_copy(
        self,
        manifest: dict,
        manifest_dir: Path,
        project_root: Path,
        state_dir: Path,
        workspace_dir: Path | None,
        inplace: bool = False,
    ) -> WorkCopy:
        """Copy existing state/workspace dirs into an isolated work copy for resume.

        If *inplace* is True, back up the original dirs and use them directly.
        """
        from datetime import datetime

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
        work_dir = manifest_dir / "work"
        work_dir.mkdir(exist_ok=True)

        if inplace:
            # Backup originals, then use them in-place
            backup_state = work_dir / f"state_{run_id}_backup"
            shutil.copytree(state_dir, backup_state)
            print(f"  [backup] state -> {backup_state}")

            workspace_root = None
            if workspace_dir and workspace_dir.exists():
                backup_ws = work_dir / f"workspaces_{run_id}_backup"
                shutil.copytree(workspace_dir, backup_ws)
                print(f"  [backup] workspace -> {backup_ws}")
                workspace_root = workspace_dir

            return WorkCopy(
                state_dir=state_dir,
                config_path=None,
                project_root=project_root,
                workspace_root=workspace_root,
                extra={"manifest": manifest, "manifest_dir": manifest_dir},
            )

        state_dst = work_dir / f"state_{run_id}"
        shutil.copytree(state_dir, state_dst)

        workspace_dst = None
        if workspace_dir and workspace_dir.exists():
            workspace_dst = work_dir / f"workspaces_{run_id}"
            shutil.copytree(workspace_dir, workspace_dst)

        return WorkCopy(
            state_dir=state_dst,
            config_path=None,
            project_root=project_root,
            workspace_root=workspace_dst,
            extra={"manifest": manifest, "manifest_dir": manifest_dir},
        )

    def cleanup_work_copy(self, work_copy: WorkCopy) -> None:
        """Remove the working copy."""
        if work_copy.state_dir.exists():
            shutil.rmtree(work_copy.state_dir)
        if work_copy.workspace_root and work_copy.workspace_root.exists():
            shutil.rmtree(work_copy.workspace_root)

    # ── Session initialisation ────────────────────────

    @abstractmethod
    def init_session(
        self,
        work_copy: WorkCopy,
        test_id: str,
    ) -> str:
        """Uniquify + prepare + register. Return actual session_id."""

    # ── Update execution ──────────────────────────────

    @abstractmethod
    def execute_update(
        self,
        update_id: str,
        work_copy: WorkCopy,
        test_id: str,
        session_id: str,
    ) -> None:
        """Execute one update action."""

    # ── Path resolution ───────────────────────────────

    @abstractmethod
    def resolve_workspace(
        self, work_copy: WorkCopy, test_id: str
    ) -> Path | None:
        """Return the workspace path for a test, or None."""

    # ── Model config ─────────────────────────────────

    def apply_model_config(
        self, work_copy: WorkCopy, model: "ModelConfig"  # noqa: F821
    ) -> None:
        """Apply a ModelConfig to the prepared work_copy.

        Modifies framework config files inside work_copy to redirect LLM
        requests to model.api_base / model.model_id.

        Default implementation is a no-op with a warning.
        Frameworks should override as needed.
        """
        logger.warning(
            "[warn] %s has no apply_model_config — skipping LLM redirect",
            type(self).__name__,
        )

    def build_model_env(
        self, work_copy: WorkCopy, model: "ModelConfig"  # noqa: F821
    ) -> dict[str, str]:
        """Convert ModelConfig to per-invocation env var overrides.

        Unlike apply_model_config (which mutates config files on disk),
        this returns env vars that can be passed per-invocation via
        engine.run_agent(extra_env=...).

        Used by MetaClaw isolation mode where multiple scenes share one
        work_copy but need different proxy endpoints.

        Default: empty dict (framework does not support env-based override).
        """
        return {}

    # ── Questions loading ─────────────────────────────

    def load_questions(
        self,
        eval_dir: Path,
        eval_name: str,
        test_entry: dict,
        work_copy: "WorkCopy",
    ) -> dict:
        """Load questions for a test scenario.

        Default: reads ``eval/{eval_name}/questions.json``.
        Override to source questions from a different format (e.g. a native
        benchmark spec file) so that no eval directory is required.
        """
        from clawarena.core.io import load_questions as _load_questions
        return _load_questions(eval_dir, eval_name)

    def uses_eval_dir(self) -> bool:
        """Return True if this framework requires the eval/ directory.

        When False, ``clawarena check`` skips the G-002 eval_dir existence
        check and the G-006 questions.json checks for frameworks that override
        ``load_questions`` to read a native format.
        """
        return True

    # ── LLM log ───────────────────────────────────────

    def read_llm_log(
        self, work_copy: WorkCopy, session_id: str, after_ts: float
    ) -> dict | None:
        """Read LLM log for a session. Default: None."""
        return None

    def count_session_tokens(
        self, state_dir: Path, test_id: str
    ) -> int:
        """Count tokens in a session's state. Default: 0."""
        return 0
