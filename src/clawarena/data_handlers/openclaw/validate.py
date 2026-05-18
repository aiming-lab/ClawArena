"""OpenClaw data validation."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.data_handlers.update_refs import resolve_update_entries
from clawarena.utils import get_project_root


def validate_openclaw(
    manifest: dict,
    manifest_dir: Path,
    eval_dir: Path,
    test_entries: list[dict],
) -> list[str]:
    """Validate OpenClaw manifest and data completeness.

    Returns list of error strings (empty = pass).
    """
    errors: list[str] = []

    # 1. Manifest structure
    if manifest.get("framework") != "openclaw":
        errors.append("manifest.framework != 'openclaw'")

    config_rel = manifest.get("config_file")
    if not config_rel:
        errors.append("manifest missing 'config_file'")
    else:
        config_path = manifest_dir / config_rel
        if not config_path.exists():
            errors.append(f"config_file not found: {config_path}")
        else:
            _validate_config(config_path, manifest, errors)

    state_rel = manifest.get("state_dir")
    if not state_rel:
        errors.append("manifest missing 'state_dir'")
    elif not (manifest_dir / state_rel).exists():
        errors.append(f"state_dir not found: {manifest_dir / state_rel}")

    # 2. Per-agent validation
    agents = manifest.get("agents", {})
    for test in test_entries:
        test_id = test["id"]
        if test_id not in agents:
            errors.append(f"test '{test_id}' not found in manifest.agents")
            continue

        agent_info = agents[test_id]
        if agent_info.get("agent_id") != test_id:
            errors.append(
                f"agent_id mismatch: {agent_info.get('agent_id')} != {test_id}"
            )

        # Agent dir
        agent_dir_rel = agent_info.get("agent_dir")
        if agent_dir_rel:
            agent_dir = manifest_dir / agent_dir_rel
            if not agent_dir.exists():
                errors.append(f"agent_dir not found: {agent_dir}")
            else:
                _validate_sessions(agent_dir, agent_info, test_id, errors)

        # Workspace
        ws_rel = agent_info.get("workspace")
        if ws_rel and not (manifest_dir / ws_rel).exists():
            errors.append(f"workspace not found: {manifest_dir / ws_rel}")

    # 3. Updates validation
    _validate_updates(manifest, manifest_dir, eval_dir, test_entries, errors)

    return errors


def _validate_config(
    config_path: Path, manifest: dict, errors: list[str]
) -> None:
    """Validate openclaw.json config file."""
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"config_file not valid JSON: {e}")
        return

    benchmark_root = str(get_project_root())
    agents_list = config.get("agents", {}).get("list", [])
    config_by_id = {a.get("id"): a for a in agents_list if a.get("id")}
    config_ids = set(config_by_id)

    for test_id in manifest.get("agents", {}):
        if test_id not in config_ids:
            errors.append(
                f"agent '{test_id}' in manifest but not in openclaw.json"
            )
            continue

        entry = config_by_id[test_id]

        workspace_raw = entry.get("workspace", "")
        if workspace_raw:
            workspace_path = Path(
                workspace_raw.replace("${BENCHMARK_ROOT}", benchmark_root)
            )
            if not workspace_path.exists():
                errors.append(
                    f"agent '{test_id}': openclaw.json workspace path not found: {workspace_path}"
                )

        agent_dir_raw = entry.get("agentDir", "")
        if agent_dir_raw:
            agent_dir_path = Path(
                agent_dir_raw.replace("${BENCHMARK_ROOT}", benchmark_root)
            )
            # agentDir may include a runtime-created subdirectory (e.g. /agent);
            # require at least the parent to exist on disk.
            check_path = agent_dir_path if agent_dir_path.exists() else agent_dir_path.parent
            if not check_path.exists():
                errors.append(
                    f"agent '{test_id}': openclaw.json agentDir parent not found: {agent_dir_path}"
                )


def _validate_sessions(
    agent_dir: Path, agent_info: dict, test_id: str, errors: list[str]
) -> None:
    """Validate session files exist."""
    sessions_dir = agent_dir / "sessions"
    if not sessions_dir.exists():
        errors.append(f"{test_id}: sessions directory not found")
        return

    # Main session
    main_session = agent_info.get("session", "")
    if main_session:
        session_file = sessions_dir / f"{main_session}.jsonl"
        if not session_file.exists():
            errors.append(f"{test_id}: main session file not found: {session_file.name}")
        else:
            _validate_session_message_order(session_file, test_id, errors)

    # History sessions
    for hsess in agent_info.get("history_sessions", []):
        hfile = sessions_dir / f"{hsess}.jsonl"
        if not hfile.exists():
            errors.append(f"{test_id}: history session not found: {hfile.name}")
        else:
            _validate_session_message_order(hfile, f"{test_id}/{hsess}", errors)

    # sessions.json
    sessions_json = sessions_dir / "sessions.json"
    if not sessions_json.exists():
        errors.append(f"{test_id}: sessions.json not found")
    else:
        try:
            json.loads(sessions_json.read_text(encoding="utf-8"))
        except Exception:
            errors.append(f"{test_id}: sessions.json not valid JSON")


def _validate_session_message_order(
    session_file: Path, label: str, errors: list[str]
) -> None:
    """Validate that a session JSONL file has no consecutive same-role messages.

    Replicates openclaw's readSessionMessages parsing then checks for patterns
    that would require provider-specific merging (validateAnthropicTurns /
    validateGeminiTurns).  repairToolUseResultPairing patterns are allowed.

    Parsing rules (consistent with openclaw readSessionMessages):
    - Lines with a ``message`` field: the nested message is extracted.
    - Lines with ``type == "compaction"``: treated as a synthetic ``system``
      message that acts as a chain-breaker (like openclaw does).
    - All other line types (``session``, ``model_change``, …): ignored
      completely, no effect on consecutive tracking.

    Consecutive-role rules:
    - consecutive ``role="user"`` → allowed. Upstream OpenClaw calls
      ``validateAnthropicTurns`` which merges consecutive user turns.
    - consecutive ``role="assistant"`` → error (requires validateGeminiTurns),
      EXCEPT when the previous assistant message contains ONLY thinking-type
      blocks (``type == "thinking"``): openclaw records thinking models by
      writing a thinking-only assistant line followed by a separate text/tool
      assistant line, and ``mergeConsecutiveAssistantTurns`` is designed to
      merge them — so this split is a valid on-disk representation.
    - consecutive ``role="toolResult"`` → allowed (repairToolUseResultPairing)
    - ``role="system"`` (compaction) updates lastRole and breaks the chain
      but never triggers an error itself.
    """
    try:
        content = session_file.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"{label}: cannot read session file: {e}")
        return

    last_role: str | None = None
    last_assistant_thinking_only: bool = False  # previous assistant was pure-thinking

    for line_num, raw in enumerate(content.splitlines(), 1):
        stripped = raw.strip()
        if not stripped:
            continue
        try:
            parsed = json.loads(stripped)
        except Exception:
            continue

        if not isinstance(parsed, dict):
            continue

        # Simulate readSessionMessages: determine role of this line
        if "message" in parsed:
            msg = parsed["message"]
            if not isinstance(msg, dict):
                continue
            role = msg.get("role")
            thinking_only = (
                role == "assistant"
                and isinstance(msg.get("content"), list)
                and bool(msg["content"])
                and all(
                    isinstance(b, dict) and b.get("type") == "thinking"
                    for b in msg["content"]
                )
            )
        elif parsed.get("type") == "compaction":
            # Becomes a synthetic system message — chain-breaker, not an error
            role = "system"
            thinking_only = False
        else:
            # session header, model_change, and any other types are ignored
            continue

        if not role:
            continue

        # Detect provider-specific-merge-required patterns.
        # Consecutive user turns are valid for OpenClaw because upstream
        # validateAnthropicTurns merges them before model invocation.
        if role == last_role and role == "assistant":
            # Allow thinking-only assistant followed by the real response:
            # openclaw writes them as two separate lines for thinking models.
            if not last_assistant_thinking_only:
                errors.append(
                    f"{label}: consecutive '{role}' messages at line {line_num}"
                )

        last_role = role
        last_assistant_thinking_only = thinking_only


def _validate_updates(
    manifest: dict,
    manifest_dir: Path,
    eval_dir: Path,
    test_entries: list[dict],
    errors: list[str],
) -> None:
    """Validate update declarations and files."""
    updates = manifest.get("updates", {})

    for test in test_entries:
        test_id = test["id"]
        test_updates = updates.get(test_id, {})

        # Load questions to check update_ids references
        eval_name = test.get("eval", test_id)
        questions_path = eval_dir / eval_name / "questions.json"
        if not questions_path.exists():
            continue

        try:
            q_data = json.loads(questions_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        rounds = q_data.get("rounds", [])
        for rnd in rounds:
            for uid in rnd.get("update_ids", []):
                resolved_updates = resolve_update_entries(test_updates, uid)
                if not resolved_updates:
                    errors.append(
                        f"{test_id}/{rnd['id']}: update_id '{uid}' "
                        f"not found in manifest.updates"
                    )
                else:
                    for resolved_id, umeta in resolved_updates:
                        udir = manifest_dir / umeta.get("dir", "")
                        utype = umeta.get("type", "")
                        files = umeta.get("files", [])

                        for item in files:
                            # Support both str and dict format
                            if isinstance(item, str):
                                fname = item
                                action = "new"
                            elif isinstance(item, dict):
                                fname = item.get("name", "")
                                action = item.get("action", "new")
                                target = item.get("target", fname)
                                channel = item.get("channel")

                                # Validate action
                                if action not in ("new", "append", "insert", "delete"):
                                    errors.append(
                                        f"{test_id}: invalid action '{action}' in update '{resolved_id}'"
                                    )

                                # Validate channel for session new actions
                                if utype == "session" and action == "new" and not channel:
                                    errors.append(
                                        f"{test_id}: session update '{resolved_id}' action=new "
                                        f"requires channel for file '{fname}'"
                                    )

                                # Validate target is provided
                                if not target:
                                    errors.append(
                                        f"{test_id}: update '{resolved_id}' file '{fname}' missing target"
                                    )
                            else:
                                errors.append(
                                    f"{test_id}: update '{resolved_id}' has invalid file entry (not str or dict)"
                                )
                                continue

                            # Check file exists (for actions that need source)
                            if action in ("new", "append", "insert"):
                                update_file = udir / fname
                                if not update_file.exists():
                                    errors.append(
                                        f"{test_id}: update file not found: {update_file}"
                                    )
                                elif utype == "session":
                                    label = f"{test_id}/update:{resolved_id}/{fname}"
                                    _validate_session_message_order(update_file, label, errors)
