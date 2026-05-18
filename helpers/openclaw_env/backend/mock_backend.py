"""Mock backend that simulates openclaw CLI behavior without real infrastructure."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult


class MockBackend(BaseBackend):
    """Simulates openclaw CLI commands using in-memory state.

    No real gateway or external services are needed. Command responses
    are generated based on the current mock state.
    """

    def __init__(self) -> None:
        self._state_dir: Path | None = None
        self._config: dict[str, Any] = {}
        self._agents: dict[str, dict[str, Any]] = {}
        self._channels: dict[str, dict[str, Any]] = {}
        self._messages: list[dict[str, Any]] = []
        self._cron_jobs: list[dict[str, Any]] = []
        self._plugins: list[dict[str, Any]] = []
        self._sessions: list[dict[str, Any]] = []
        self._gateway_running: bool = False
        self._gateway_port: int = 18789

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._state_dir = Path(state_dir)
        config_path = self._state_dir / "openclaw.json"
        if config_path.exists():
            with open(config_path) as f:
                self._config = json.load(f)
        cron_jobs_path = self._state_dir / "cron_jobs.json"
        if cron_jobs_path.exists():
            with open(cron_jobs_path) as f:
                payload = json.load(f)
            if isinstance(payload, list):
                self._cron_jobs = payload
        # Initialize channels from config
        for ch_name, ch_config in self._config.get("channels", {}).items():
            self._channels[ch_name] = {
                "name": ch_name,
                "status": "connected",
                "config": ch_config,
            }

    def execute_cli(self, command: str) -> CommandResult:
        import shlex

        command = command.strip()
        if not command.startswith("openclaw"):
            return CommandResult(
                stdout="", stderr="Unknown command", exit_code=127
            )

        try:
            parts = shlex.split(command)
        except ValueError:
            parts = command.split()

        if len(parts) < 2:
            return self._help_output()

        subcmd = parts[1]
        args = parts[2:]

        handler = self._COMMAND_HANDLERS.get(subcmd)
        if handler:
            return handler(self, args)
        return CommandResult(
            stdout="",
            stderr=f"Unknown subcommand: {subcmd}",
            exit_code=1,
        )

    def execute_python(self, code: str) -> CommandResult:
        # Simple mock: extract intent from code and delegate
        if "client.status" in code:
            return self._cmd_status([])
        if "client.agents.add" in code:
            match = re.search(r"name=['\"](\w+)['\"]", code)
            name = match.group(1) if match else "default"
            return self._cmd_agents(["add", "--name", name])
        if "client.agents.list" in code:
            return self._cmd_agents(["list"])
        return CommandResult(
            stdout="Mock Python execution: OK",
            stderr="",
            exit_code=0,
        )

    def get_gateway_status(self) -> dict[str, Any] | None:
        if not self._gateway_running:
            return None
        return {
            "running": True,
            "port": self._gateway_port,
            "uptime_seconds": 3600,
            "channels": len(self._channels),
            "sessions": len(self._sessions),
        }

    def get_config(self) -> dict[str, Any]:
        return dict(self._config)

    def get_state(self) -> dict[str, Any]:
        return {
            "agents": dict(self._agents),
            "channels": dict(self._channels),
            "messages": list(self._messages),
            "cron_jobs": list(self._cron_jobs),
            "plugins": list(self._plugins),
        }

    def cleanup(self) -> None:
        self._agents.clear()
        self._channels.clear()
        self._messages.clear()
        self._cron_jobs.clear()
        self._plugins.clear()
        self._sessions.clear()
        self._gateway_running = False

    # ---- Command Handlers ----

    def _help_output(self) -> CommandResult:
        return CommandResult(
            stdout=(
                "openclaw - Personal AI Assistant\n\n"
                "Commands:\n"
                "  status        Show system status\n"
                "  health        Check gateway health\n"
                "  agents        Manage agents\n"
                "  agent         Run an agent turn\n"
                "  message       Send and manage messages\n"
                "  channels      Manage channels\n"
                "  config        Non-interactive configuration\n"
                "  configure     Interactive configuration\n"
                "  setup         Initialize workspace\n"
                "  gateway       Gateway management\n"
                "  plugins       Plugin management\n"
                "  skills        Skill management\n"
                "  cron          Cron job scheduler\n"
                "  webhooks      Webhook management\n"
                "  security      Security settings\n"
                "  devices       Device management\n"
                "  doctor        Diagnostic tool\n"
                "  logs          View logs\n"
                "  sessions      List sessions\n"
            ),
            stderr="",
            exit_code=0,
        )

    def _cmd_status(self, args: list[str]) -> CommandResult:
        use_json = "--json" in args
        status = {
            "gateway": {
                "running": self._gateway_running,
                "port": self._gateway_port,
            },
            "channels": {
                name: {"status": ch["status"]}
                for name, ch in self._channels.items()
            },
            "agents": list(self._agents.keys()),
            "sessions": len(self._sessions),
        }
        if use_json:
            return CommandResult(
                stdout=json.dumps(status, indent=2), stderr="", exit_code=0
            )
        lines = [
            f"Gateway: {'running' if self._gateway_running else 'stopped'} "
            f"(port {self._gateway_port})",
            f"Channels: {len(self._channels)} configured",
        ]
        for name, ch in self._channels.items():
            lines.append(f"  - {name}: {ch['status']}")
        lines.append(f"Agents: {len(self._agents)}")
        lines.append(f"Sessions: {len(self._sessions)}")
        return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

    def _cmd_health(self, args: list[str]) -> CommandResult:
        if not self._gateway_running:
            return CommandResult(
                stdout="",
                stderr="Gateway is not running. Start it with: openclaw gateway start",
                exit_code=1,
            )
        return CommandResult(
            stdout="Gateway health: OK\nUptime: 1h 0m\nMemory: 128MB",
            stderr="",
            exit_code=0,
        )

    def _cmd_agents(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout="Usage: openclaw agents <add|delete|list|set-identity>",
                stderr="",
                exit_code=0,
            )

        action = args[0]

        if action == "list":
            if not self._agents:
                return CommandResult(
                    stdout="No agents configured.", stderr="", exit_code=0
                )
            lines = ["Agents:"]
            for name, agent in self._agents.items():
                model = agent.get("model", "default")
                lines.append(f"  - {name} (model: {model})")
            return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

        if action == "add":
            name = _get_arg(args, "--name")
            if not name and len(args) > 1 and not args[1].startswith("-"):
                name = args[1]
            if not name:
                name = "agent-" + uuid.uuid4().hex[:6]
            model = _get_arg(args, "--model", "anthropic/claude-sonnet-4-5-20250929")
            if name in self._agents:
                return CommandResult(
                    stdout="",
                    stderr=f"Agent '{name}' already exists.",
                    exit_code=1,
                )
            self._agents[name] = {"name": name, "model": model}
            return CommandResult(
                stdout=f"Agent '{name}' created with model {model}.",
                stderr="",
                exit_code=0,
                state_changes={"agents": {name: self._agents[name]}},
            )

        if action == "delete":
            name = _get_arg(args, "--name") or (args[1] if len(args) > 1 else None)
            if not name or name not in self._agents:
                return CommandResult(
                    stdout="",
                    stderr=f"Agent '{name}' not found.",
                    exit_code=1,
                )
            del self._agents[name]
            return CommandResult(
                stdout=f"Agent '{name}' deleted.",
                stderr="",
                exit_code=0,
            )

        if action == "set-identity":
            name = _get_arg(args, "--agent") or _get_arg(args, "--name")
            if not name and len(args) > 1 and not args[1].startswith("-"):
                name = args[1]
            if not name or name not in self._agents:
                return CommandResult(
                    stdout="",
                    stderr=f"Agent '{name}' not found.",
                    exit_code=1,
                )
            emoji = _get_arg(args, "--emoji")
            if emoji:
                self._agents[name]["emoji"] = emoji
            return CommandResult(
                stdout=f"Agent '{name}' identity updated.",
                stderr="",
                exit_code=0,
            )

        return CommandResult(
            stdout="", stderr=f"Unknown agents action: {action}", exit_code=1
        )

    def _cmd_agent(self, args: list[str]) -> CommandResult:
        message = _get_arg(args, "--message", "")
        agent_name = _get_arg(args, "--agent", "default")
        if not message:
            return CommandResult(
                stdout="", stderr="--message is required", exit_code=1
            )
        # Deterministic mock response patterns for online-read tasks.
        location_match = re.search(r"location '([^']+)'", message, flags=re.IGNORECASE)
        day_match = re.search(r"day '([^']+)'", message, flags=re.IGNORECASE)

        if "weather_result:" in message.lower():
            location = location_match.group(1) if location_match else "the requested location"
            response = (
                f"WEATHER_RESULT: Current weather in {location} is clear with a mild temperature."
            )
        elif "calendar_result:" in message.lower():
            day = day_match.group(1) if day_match else "today"
            response = f"CALENDAR_RESULT: You have 2 scheduled events for {day}."
        else:
            response = f"[{agent_name}] Response to: {message}"

        session_id = uuid.uuid4().hex[:8]
        return CommandResult(
            stdout=f"{response}\nSession: {session_id}",
            stderr="",
            exit_code=0,
        )

    def _cmd_message(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout="Usage: openclaw message <send|broadcast|poll|react|search|read|edit|delete|pin>",
                stderr="",
                exit_code=0,
            )

        action = args[0]

        if action == "send":
            target = _get_arg(args, "--target", "")
            message = _get_arg(args, "--message", "")
            channel = _get_arg(args, "--channel", "")
            media = _get_arg(args, "--media")

            if not channel:
                return CommandResult(
                    stdout="", stderr="--channel is required", exit_code=1
                )
            if not target:
                return CommandResult(
                    stdout="", stderr="--target is required", exit_code=1
                )
            if not message and not media:
                return CommandResult(
                    stdout="",
                    stderr="--message or --media is required",
                    exit_code=1,
                )

            msg_record = {
                "id": uuid.uuid4().hex[:8],
                "target": target,
                "message": message,
                "channel": channel,
                "media": media,
                "type": "media" if media else "text",
            }
            self._messages.append(msg_record)
            return CommandResult(
                stdout=f"Message sent to {target}" + (f" via {channel}" if channel else "") + ".",
                stderr="",
                exit_code=0,
                state_changes={"messages": [msg_record]},
            )

        if action == "broadcast":
            message = _get_arg(args, "--message", "")
            target_list: list[str] = []
            if "--targets" in args:
                idx = args.index("--targets") + 1
                while idx < len(args) and not args[idx].startswith("--"):
                    target_list.append(args[idx])
                    idx += 1
            if len(target_list) == 1 and "," in target_list[0]:
                target_list = _split_csv(target_list[0])
            for t in target_list:
                self._messages.append(
                    {"id": uuid.uuid4().hex[:8], "target": t, "message": message}
                )
            return CommandResult(
                stdout=f"Broadcast sent to {len(target_list)} targets.",
                stderr="",
                exit_code=0,
            )

        if action == "search":
            query = _get_arg(args, "--query", "")
            channel = _get_arg(args, "--channel", "")
            results = [
                m for m in self._messages
                if query.lower() in m.get("message", "").lower()
                and (not channel or m.get("channel", "") == channel)
            ]
            if not results:
                return CommandResult(
                    stdout=f"No messages found matching '{query}'.", stderr="", exit_code=0
                )
            lines = [f"Found {len(results)} message(s):"]
            for m in results:
                lines.append(f"  [{m['id']}] to {m['target']}: {m['message']}")
            return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

        if action == "poll":
            question = _get_arg(args, "--poll-question") or _get_arg(args, "--question", "")
            poll_options = _get_multi_arg(args, "--poll-option")
            options = poll_options if poll_options else _split_csv(_get_arg(args, "--options", ""))
            target = _get_arg(args, "--target", "")
            msg_record = {
                "id": uuid.uuid4().hex[:8],
                "target": target,
                "type": "poll",
                "question": question,
                "options": options,
            }
            self._messages.append(msg_record)
            return CommandResult(
                stdout=f"Poll created: {question}", stderr="", exit_code=0
            )

        if action == "react":
            target = _get_arg(args, "--target", "")
            emoji = _get_arg(args, "--emoji", "👍")
            channel = _get_arg(args, "--channel", "")
            return CommandResult(
                stdout=f"Reacted with {emoji} to message from {target}"
                + (f" on {channel}" if channel else "") + ".",
                stderr="",
                exit_code=0,
            )

        return CommandResult(
            stdout="", stderr=f"Unknown message action: {action}", exit_code=1
        )

    def _cmd_channels(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout="Usage: openclaw channels <login|config|list|status>",
                stderr="",
                exit_code=0,
            )

        action = args[0]

        if action in ("list", "status"):
            if not self._channels:
                return CommandResult(
                    stdout="No channels configured.", stderr="", exit_code=0
                )
            if "--json" in args:
                payload = {
                    name: {
                        "status": ch.get("status", "unknown"),
                        "config": ch.get("config", {}),
                    }
                    for name, ch in self._channels.items()
                }
                return CommandResult(
                    stdout=json.dumps(payload, indent=2),
                    stderr="",
                    exit_code=0,
                )
            lines = ["Channels:"]
            for name, ch in self._channels.items():
                lines.append(f"  - {name}: {ch['status']}")
            return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

        if action == "add":
            channel = _get_arg(args, "--channel", "")
            if not channel:
                return CommandResult(
                    stdout="", stderr="--channel is required", exit_code=1
                )
            self._channels[channel] = {
                "name": channel,
                "status": "connected",
                "config": {},
            }
            return CommandResult(
                stdout=f"Channel '{channel}' added.",
                stderr="",
                exit_code=0,
            )

        if action == "login":
            channel = _get_arg(args, "--channel")
            if not channel:
                return CommandResult(
                    stdout="", stderr="--channel is required", exit_code=1
                )
            self._channels[channel] = {
                "name": channel,
                "status": "connected",
                "config": {},
            }
            return CommandResult(
                stdout=f"Logged in to {channel}.", stderr="", exit_code=0
            )

        if action == "config":
            channel = _get_arg(args, "--channel") or (args[1] if len(args) > 1 else "")
            if channel not in self._channels:
                return CommandResult(
                    stdout="",
                    stderr=f"Channel '{channel}' not found.",
                    exit_code=1,
                )
            key = _get_arg(args, "--key")
            value = _get_arg(args, "--value")
            if key is not None and value is not None:
                # Set a config value
                self._channels[channel].setdefault("config", {})[key] = value
                return CommandResult(
                    stdout=f"Channel '{channel}' config updated: {key}={value}",
                    stderr="",
                    exit_code=0,
                )
            # Read config
            return CommandResult(
                stdout=json.dumps(self._channels[channel]["config"], indent=2),
                stderr="",
                exit_code=0,
            )

        if action == "remove":
            channel = _get_arg(args, "--channel") or (args[1] if len(args) > 1 else "")
            if not channel:
                return CommandResult(
                    stdout="", stderr="Channel name required", exit_code=1
                )
            self._channels.pop(channel, None)
            return CommandResult(
                stdout=f"Channel '{channel}' removed.", stderr="", exit_code=0
            )

        return CommandResult(
            stdout="", stderr=f"Unknown channels action: {action}", exit_code=1
        )

    def _cmd_gateway(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout="Usage: openclaw gateway <start|stop|restart|status>",
                stderr="",
                exit_code=0,
            )

        action = args[0]

        if action == "start":
            if self._gateway_running:
                return CommandResult(
                    stdout="Gateway is already running.",
                    stderr="",
                    exit_code=0,
                )
            self._gateway_running = True
            return CommandResult(
                stdout=f"Gateway started on port {self._gateway_port}.",
                stderr="",
                exit_code=0,
            )

        if action == "stop":
            self._gateway_running = False
            return CommandResult(
                stdout="Gateway stopped.", stderr="", exit_code=0
            )

        if action == "restart":
            self._gateway_running = True
            return CommandResult(
                stdout=f"Gateway restarted on port {self._gateway_port}.",
                stderr="",
                exit_code=0,
            )

        if action == "status":
            return self._cmd_status(args[1:])

        return CommandResult(
            stdout="", stderr=f"Unknown gateway action: {action}", exit_code=1
        )

    def _cmd_configure(self, args: list[str]) -> CommandResult:
        # Mock interactive configuration by parsing key=value args
        updates: dict[str, Any] = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                keys = key.split(".")
                d = updates
                for k in keys[:-1]:
                    d = d.setdefault(k, {})
                d[keys[-1]] = value

        if updates:
            _deep_merge(self._config, updates)
            if self._state_dir:
                config_path = self._state_dir / "openclaw.json"
                with open(config_path, "w") as f:
                    json.dump(self._config, f, indent=2)
            return CommandResult(
                stdout="Configuration updated.", stderr="", exit_code=0
            )

        return CommandResult(
            stdout=json.dumps(self._config, indent=2), stderr="", exit_code=0
        )

    def _cmd_config(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout=json.dumps(self._config, indent=2), stderr="", exit_code=0
            )

        action = args[0]
        if action == "get":
            if len(args) < 2:
                return CommandResult(stdout="", stderr="config path required", exit_code=1)
            value = _get_path(self._config, args[1])
            if value is None:
                return CommandResult(stdout="", stderr="path not found", exit_code=1)
            return CommandResult(stdout=str(value), stderr="", exit_code=0)

        if action == "set":
            if len(args) < 3:
                return CommandResult(stdout="", stderr="path and value required", exit_code=1)
            path = args[1]
            value = args[2]
            _set_path(self._config, path, value)
            if self._state_dir:
                config_path = self._state_dir / "openclaw.json"
                with open(config_path, "w") as f:
                    json.dump(self._config, f, indent=2)
            return CommandResult(
                stdout=f"Updated {path}.",
                stderr="",
                exit_code=0,
                state_changes={"config": {path: value}},
            )

        if action == "unset":
            if len(args) < 2:
                return CommandResult(stdout="", stderr="path required", exit_code=1)
            path = args[1]
            _unset_path(self._config, path)
            if self._state_dir:
                config_path = self._state_dir / "openclaw.json"
                with open(config_path, "w") as f:
                    json.dump(self._config, f, indent=2)
            return CommandResult(stdout=f"Unset {path}.", stderr="", exit_code=0)

        return CommandResult(stdout="", stderr=f"Unknown config action: {action}", exit_code=1)

    def _cmd_setup(self, args: list[str]) -> CommandResult:
        return CommandResult(
            stdout="Workspace initialized successfully.",
            stderr="",
            exit_code=0,
        )

    def _cmd_doctor(self, args: list[str]) -> CommandResult:
        checks = [
            ("Config file", "OK"),
            ("Gateway", "running" if self._gateway_running else "stopped"),
            ("Channels", f"{len(self._channels)} configured"),
            ("Agents", f"{len(self._agents)} configured"),
            ("Workspace", "OK"),
        ]
        lines = ["OpenClaw Doctor\n"]
        for name, status in checks:
            icon = "+" if status == "OK" or "configured" in status or status == "running" else "!"
            lines.append(f"  [{icon}] {name}: {status}")
        return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

    def _cmd_logs(self, args: list[str]) -> CommandResult:
        return CommandResult(
            stdout="[2025-01-01 12:00:00] Gateway started\n"
            "[2025-01-01 12:00:01] Channel telegram connected\n"
            "[2025-01-01 12:00:02] Agent turn processed",
            stderr="",
            exit_code=0,
        )

    def _cmd_sessions(self, args: list[str]) -> CommandResult:
        if not self._sessions:
            return CommandResult(
                stdout="No active sessions.", stderr="", exit_code=0
            )
        lines = [f"Sessions ({len(self._sessions)}):"]
        for s in self._sessions:
            lines.append(f"  [{s['id']}] {s.get('channel', 'unknown')} - {s.get('status', 'active')}")
        return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

    def _cmd_plugins(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout="Usage: openclaw plugins <enable|disable|install|uninstall|list|update>",
                stderr="",
                exit_code=0,
            )

        action = args[0]

        if action == "list":
            if not self._plugins:
                return CommandResult(
                    stdout="No plugins installed.", stderr="", exit_code=0
                )
            lines = ["Installed plugins:"]
            for p in self._plugins:
                lines.append(f"  - {p['name']} v{p.get('version', '1.0.0')}")
            return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

        if action in {"install", "enable"}:
            name = args[1] if len(args) > 1 else ""
            if not name:
                return CommandResult(
                    stdout="", stderr="Plugin name required", exit_code=1
                )
            if any(p["name"] == name for p in self._plugins):
                already_word = "installed" if action == "install" else "enabled"
                return CommandResult(
                    stdout=f"Plugin '{name}' is already {already_word}.",
                    stderr="",
                    exit_code=0,
                )
            plugin = {"name": name, "version": "1.0.0", "status": "active"}
            self._plugins.append(plugin)
            action_word = "installed" if action == "install" else "enabled"
            return CommandResult(
                stdout=f"Plugin '{name}' {action_word}.",
                stderr="",
                exit_code=0,
                state_changes={"plugins": [plugin]},
            )

        if action == "update":
            name = args[1] if len(args) > 1 else ""
            for p in self._plugins:
                if p["name"] == name:
                    p["version"] = "2.0.0"
                    return CommandResult(
                        stdout=f"Plugin '{name}' updated to v2.0.0.", stderr="", exit_code=0
                    )
            return CommandResult(
                stdout="", stderr=f"Plugin '{name}' not installed.", exit_code=1
            )

        if action in {"remove", "uninstall", "disable"}:
            name = args[1] if len(args) > 1 else ""
            self._plugins = [p for p in self._plugins if p["name"] != name]
            verb = "disabled" if action == "disable" else "uninstalled"
            return CommandResult(
                stdout=f"Plugin '{name}' {verb}.", stderr="", exit_code=0
            )

        return CommandResult(
            stdout="", stderr=f"Unknown plugins action: {action}", exit_code=1
        )

    def _cmd_cron(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout="Usage: openclaw cron <add|list|delete>",
                stderr="",
                exit_code=0,
            )

        action = args[0]

        if action == "list":
            if not self._cron_jobs:
                return CommandResult(
                    stdout="No cron jobs configured.", stderr="", exit_code=0
                )
            lines = ["Cron jobs:"]
            for job in self._cron_jobs:
                schedule = job.get("schedule") or job.get("cron") or job.get("every", "")
                message = job.get("message") or job.get("command", "")
                lines.append(f"  [{job['id']}] {schedule} - {message}")
            return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

        if action == "add":
            schedule = _get_arg(args, "--cron") or _get_arg(args, "--schedule", "")
            every = _get_arg(args, "--every", "")
            message = _get_arg(args, "--message", "")
            command = _get_arg(args, "--command", "")
            name = _get_arg(args, "--name", f"job-{uuid.uuid4().hex[:6]}")
            normalized_message = message or command
            if not name:
                return CommandResult(stdout="", stderr="--name is required", exit_code=1)
            if not schedule and not every:
                return CommandResult(
                    stdout="",
                    stderr="--cron or --schedule is required",
                    exit_code=1,
                )
            if not normalized_message:
                return CommandResult(
                    stdout="",
                    stderr="--message or --command is required",
                    exit_code=1,
                )
            payload: dict[str, Any] = {
                "id": uuid.uuid4().hex[:6],
                "name": name,
                "status": "active",
            }
            if schedule:
                payload["schedule"] = schedule
            if every:
                payload["every"] = every
            if message:
                payload["message"] = message
            elif command:
                payload["command"] = command
            self._cron_jobs.append(payload)
            return CommandResult(
                stdout=f"Cron job created: {payload['id']}",
                stderr="",
                exit_code=0,
                state_changes={"cron_jobs": [payload]},
            )

        if action in {"delete", "rm"}:
            job_id = args[1] if len(args) > 1 else ""
            self._cron_jobs = [j for j in self._cron_jobs if j["id"] != job_id]
            return CommandResult(
                stdout=f"Cron job '{job_id}' deleted.", stderr="", exit_code=0
            )

        return CommandResult(
            stdout="", stderr=f"Unknown cron action: {action}", exit_code=1
        )

    def _cmd_security(self, args: list[str]) -> CommandResult:
        auth = self._config.get("gateway", {}).get("auth", {})
        if not args:
            return CommandResult(
                stdout=f"Auth mode: {auth.get('mode', 'none')}\n"
                f"Token configured: {'yes' if auth.get('token') else 'no'}",
                stderr="",
                exit_code=0,
            )

        if args[0] == "audit":
            return CommandResult(
                stdout="Security audit summary: 0 critical · 0 warn · 1 info",
                stderr="",
                exit_code=0,
            )

        if args[0] == "set-token":
            token = args[1] if len(args) > 1 else uuid.uuid4().hex
            self._config.setdefault("gateway", {}).setdefault("auth", {})["token"] = token
            self._config["gateway"]["auth"]["mode"] = "token"
            return CommandResult(
                stdout="Security token updated.", stderr="", exit_code=0
            )

        return CommandResult(
            stdout="", stderr=f"Unknown security action: {args[0]}", exit_code=1
        )

    def _cmd_models(self, args: list[str]) -> CommandResult:
        current = (
            _get_path(self._config, "agents.defaults.model.primary")
            or self._config.get("agent", {}).get("model", "not set")
        )
        if not args:
            return CommandResult(
                stdout=f"Current model: {current}\n\n"
                "Available models:\n"
                "  - anthropic/claude-opus-4-6\n"
                "  - anthropic/claude-sonnet-4-5-20250929\n"
                "  - openai/gpt-4o\n"
                "  - google/gemini-2.0-flash",
                stderr="",
                exit_code=0,
            )

        if args[0] == "set":
            model = args[1] if len(args) > 1 else ""
            self._config.setdefault("agent", {})["model"] = model
            _set_path(self._config, "agents.defaults.model.primary", model)
            return CommandResult(
                stdout=f"Model set to {model}.", stderr="", exit_code=0
            )

        return CommandResult(stdout="", stderr=f"Unknown models action: {args[0]}", exit_code=1)

    def _cmd_devices(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                stdout="Usage: openclaw devices <pair|list|remove>",
                stderr="",
                exit_code=0,
            )
        if args[0] == "list":
            return CommandResult(
                stdout="No devices paired.", stderr="", exit_code=0
            )
        if args[0] == "pair":
            return CommandResult(
                stdout="Device pairing initiated. Follow instructions on your device.",
                stderr="",
                exit_code=0,
            )
        return CommandResult(
            stdout="", stderr=f"Unknown devices action: {args[0]}", exit_code=1
        )

    def _cmd_webhooks(self, args: list[str]) -> CommandResult:
        if not args or args[0] == "list":
            return CommandResult(
                stdout="No webhooks configured.", stderr="", exit_code=0
            )
        if args[0] == "add":
            url = _get_arg(args, "--url", "")
            return CommandResult(
                stdout=f"Webhook added: {url}", stderr="", exit_code=0
            )
        return CommandResult(
            stdout="", stderr=f"Unknown webhooks action: {args[0]}", exit_code=1
        )

    def _cmd_skills(self, args: list[str]) -> CommandResult:
        if not args or args[0] == "list":
            return CommandResult(
                stdout="Skills:\n  - healthcheck\n  - skill-creator\n  - tmux\n  - weather",
                stderr="",
                exit_code=0,
            )
        if args[0] == "info":
            name = args[1] if len(args) > 1 else ""
            return CommandResult(
                stdout=f"Skill: {name}\nDescription: mock skill details",
                stderr="",
                exit_code=0,
            )
        return CommandResult(
            stdout="", stderr=f"Unknown skills action: {args[0]}", exit_code=1
        )

    # Command routing table
    _COMMAND_HANDLERS = {
        "status": _cmd_status,
        "health": _cmd_health,
        "agents": _cmd_agents,
        "agent": _cmd_agent,
        "message": _cmd_message,
        "channels": _cmd_channels,
        "gateway": _cmd_gateway,
        "config": _cmd_config,
        "configure": _cmd_configure,
        "setup": _cmd_setup,
        "doctor": _cmd_doctor,
        "logs": _cmd_logs,
        "sessions": _cmd_sessions,
        "plugins": _cmd_plugins,
        "cron": _cmd_cron,
        "security": _cmd_security,
        "models": _cmd_models,
        "devices": _cmd_devices,
        "webhooks": _cmd_webhooks,
        "skills": _cmd_skills,
    }


def _get_arg(args: list[str], flag: str, default: str = "") -> str | None:
    """Extract a flag value from args list."""
    for i, arg in enumerate(args):
        if arg == flag and i + 1 < len(args):
            return args[i + 1]
    return default


def _get_multi_arg(args: list[str], flag: str) -> list[str]:
    values: list[str] = []
    for i, arg in enumerate(args):
        if arg == flag and i + 1 < len(args):
            values.append(args[i + 1])
    return values


def _split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def _set_path(cfg: dict[str, Any], path: str, value: Any) -> None:
    cur = cfg
    keys = path.split(".")
    for key in keys[:-1]:
        nxt = cur.get(key)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[key] = nxt
        cur = nxt
    cur[keys[-1]] = value


def _get_path(cfg: dict[str, Any], path: str) -> Any:
    cur: Any = cfg
    for key in path.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _unset_path(cfg: dict[str, Any], path: str) -> None:
    cur: Any = cfg
    keys = path.split(".")
    for key in keys[:-1]:
        if not isinstance(cur, dict):
            return
        cur = cur.get(key)
    if isinstance(cur, dict):
        cur.pop(keys[-1], None)


def _deep_merge(base: dict, updates: dict) -> None:
    for key, value in updates.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
