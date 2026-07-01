# Installation Guide

This guide covers the installation of ClawArena, the four supported agent frameworks (OpenClaw, Claude Code, PicoClaw, Nanobot), and MetaClaw.

---

## Quick Setup (Recommended)

The setup script installs ClawArena and all supported framework CLIs in one command:

```bash
bash scripts/setup.sh
```

It will:
1. Install ClawArena in editable mode with dev dependencies (`google-genai` ships as a clawarena dependency)
2. Install Python framework SDKs: claude-agent-sdk, nanobot-ai (pinned)
3. Install npm CLIs (pinned): Claude Code, claude-code-router (ccr), openclaw
4. Install PicoClaw: by default the script clones `sipeed/picoclaw`
   into a temp directory, runs `make install`, and removes the clone. Override
   by exporting `PICOCLAW_SRC=/path/to/picoclaw` to reuse an existing checkout;
   auto-installs Go ≥ 1.25.9 if needed
5. Verify all installations and report status

After setup, verify:

```bash
clawarena --help
```

If you need more control, follow the manual steps below.

---

## Manual Installation

### 1. ClawArena

**Requirements**: Python ≥ 3.10, pip

```bash
# Basic install
pip install -e .

# With development tools (pytest, etc.)
pip install -e ".[dev]"
```

ClawArena's core depends only on `pandas` and `scipy`. Framework-specific SDKs are optional:

```bash
pip install -e ".[claude-code]"    # Claude Code Python SDK
pip install -e ".[nanobot]"        # Nanobot Python SDK
pip install -e ".[all]"            # All optional dependencies
```

Both the `clawarena` CLI and the `ClawArena` [Python SDK](sdk.md) are available after install (`from clawarena import ClawArena`).

#### Install as a package (with bundled datasets)

Installing directly from Git builds a wheel that **bundles the benchmark datasets**
under the package (the `data/` directory is force-included; `result_example/` is
not). This makes `pip install` self-contained:

```bash
pip install git+https://github.com/aiming-lab/ClawArena.git
```

For a code-only install (e.g. from a future PyPI release), fetch datasets on demand:

```bash
clawarena fetch-data --list                    # list available datasets
clawarena fetch-data --dataset clawarena-real  # download one
clawarena fetch-data                           # download all
```

At run time, datasets are resolved in priority order: `CLAWARENA_DATA_DIR` → data
bundled in the installed package → source-tree `data/` → download cache
(`~/.cache/clawarena/data`). See the [Python SDK Guide](sdk.md#5-data-access) for
`download_data()` and `data_root()`.

### 2. Framework CLIs

Install only the frameworks you plan to evaluate.

#### OpenClaw

[OpenClaw](https://openclaw.ai) is a Node.js-based CLI agent, installed from the public npm registry.

```bash
# Requires Node.js and npm (pinned for reproducibility)
npm install -g openclaw@2026.3.13
```

#### Claude Code

[Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) is Anthropic's agentic coding tool. The ClawArena engine invokes it via the Python SDK.

```bash
npm install -g @anthropic-ai/claude-code@2.1.126
pip install claude-agent-sdk
claude login
```

For non-Anthropic providers (OpenAI-compatible, Gemini, OpenRouter, ...) the claude-code engine routes through **claude-code-router (ccr)**, which must also be installed:

```bash
npm install -g @musistudio/claude-code-router
```

The router is spawned automatically per-run; no manual config is needed.

#### PicoClaw

[PicoClaw](https://github.com/sipeed/picoclaw) is a Go-based CLI agent. The public `go install ...@latest` route is broken because the upstream `go.mod` contains `replace` directives; build from source instead. `scripts/setup.sh` does this automatically by cloning into a temp dir and running `make install`; to do it manually:

```bash
# Requires Go ≥ 1.25.9 and make. PicoClaw has no version tag; pin a commit for reproducibility.
git clone https://github.com/sipeed/picoclaw.git /tmp/picoclaw
cd /tmp/picoclaw && git checkout 6126ede9
INSTALL_PREFIX="$HOME/.local" make install   # → $HOME/.local/bin/picoclaw
rm -rf /tmp/picoclaw
```

Set `PICOCLAW_SRC=/path/to/existing/checkout` before running `setup.sh` to reuse a local clone instead of fetching.

If Go is not installed, the setup script auto-installs it to `~/.local/go-sdk`. Make sure the binary directory is in your PATH:

```bash
export PATH="$HOME/.local/go-sdk/bin:$HOME/.local/bin:$PATH"
```

#### Nanobot

[Nanobot](https://github.com/qwibitai/nanoclaw) is a Python-native CLI agent.

```bash
pip install nanobot-ai==0.1.4.post6
```

#### ClawArena Native

The built-in [`clawarena-native`](clawarena-native.md) harness needs **no separate
install** — it ships with ClawArena and runs in-process. Select it with
`--framework clawarena-native`. Use it when the external framework CLIs above cannot
be installed or version-pinned in your environment.

---

## 3. MetaClaw (Optional)

[MetaClaw](https://github.com/aiming-lab/MetaClaw) is an optional proxy layer that enhances agents with memory, skills, and RL during evaluation. ClawArena supports MetaClaw with **OpenClaw** and **Nanobot**.

### Install

```bash
git clone https://github.com/aiming-lab/MetaClaw.git
cd MetaClaw
pip install -e .
```

### Configure

```bash
metaclaw setup
```

The interactive wizard will ask for your LLM provider, API key, and preferred agent.

### Use with ClawArena

Add the `metaclaw` field to your `tests.json`:

```json
{
  "metaclaw": {
    "enabled": true,
    "managed": true,
    "config_path": "metaclaw/memory.yaml"
  }
}
```

Then run as usual — ClawArena manages the MetaClaw proxy lifecycle automatically:

```bash
clawarena run --data data/clawarena/tests.json --frameworks openclaw --out output/
```

See [MetaClaw Guide](metaclaw-guide.md) for managed/unmanaged modes and trigger configuration.

---

## Environment Variables

ClawArena uses `CLAWARENA_*` environment variables for LLM provider configuration:

| Variable | Description |
|----------|-------------|
| `CLAWARENA_PROVIDER` | LLM provider type (openai, anthropic, claude, etc.) |
| `CLAWARENA_MODEL_ID` | Model name (e.g., `gpt-4o`, `claude-opus-4.6`) |
| `CLAWARENA_API_BASE` | API endpoint URL |
| `CLAWARENA_API_KEY` | Authentication key |

These can also be set via CLI flags (`--provider`, `--model-id`, `--api-base`, `--api-key`) or in `tests.json`. See [Provider Guide](provider-usage-guide.md) for the full priority chain.
