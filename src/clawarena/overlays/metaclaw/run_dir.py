"""MetaClaw run directory management — isolated dirs for memory, skills, temp config."""

from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from clawarena.overlays.metaclaw.config import MetaClawConfig

BENCH_POLICY = {
    "retrieval_mode": "hybrid",
    "max_injected_units": 10,
    "max_injected_tokens": 1500,
    "keyword_weight": 1.0,
    "metadata_weight": 0.6,
    "importance_weight": 0.7,
    "recency_weight": 0.1,
    "recent_bonus_hours": 168,
    "type_boosts": {
        "semantic": 1.3, "preference": 1.2, "project_state": 1.1,
        "procedural_observation": 1.1, "working_summary": 1.0, "episodic": 0.7,
    },
}


@dataclass
class MetaClawRunDir:
    run_id: str
    root: Path
    memory_store_dir: Path | None
    skills_snapshot_dir: Path | None
    tmp_config_path: Path

    @classmethod
    def create(
        cls,
        config: MetaClawConfig,
        work_root: Path,
        run_id: str,
        skills_src_override: Path | None = None,
    ) -> MetaClawRunDir:
        root = work_root / f"metaclaw_{run_id}"
        root.mkdir(parents=True, exist_ok=True)

        # Memory directory
        memory_dir: Path | None = None
        if config.memory.enabled:
            memory_dir = root / "memory"
            memory_dir.mkdir(exist_ok=True)
            policy_path = memory_dir / "policy.json"
            policy_path.write_text(json.dumps(BENCH_POLICY, indent=2))

        # Skills snapshot
        skills_dir: Path | None = None
        if config.skills.enabled:
            src = Path(skills_src_override) if skills_src_override else (
                Path(config.skills.dir) if config.skills.dir else None
            )
            skills_dir = root / "skills"
            if src and src.exists():
                shutil.copytree(src, skills_dir, dirs_exist_ok=True)
            else:
                skills_dir.mkdir(exist_ok=True)
            # Record count_before for report
            count = sum(1 for _ in skills_dir.rglob("*") if _.is_file())
            (root / "skills_meta.json").write_text(
                json.dumps({"count_before": count})
            )

        # Temp config YAML
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".yaml", prefix="metaclaw_")
        import os
        os.close(tmp_fd)

        return cls(
            run_id=run_id,
            root=root,
            memory_store_dir=memory_dir,
            skills_snapshot_dir=skills_dir,
            tmp_config_path=Path(tmp_path),
        )

    def cleanup_tmp(self) -> None:
        """Remove only the temp config file. Memory/skills dirs are preserved."""
        if self.tmp_config_path.exists():
            self.tmp_config_path.unlink()
