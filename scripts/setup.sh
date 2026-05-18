#!/usr/bin/env bash
# ============================================================
#  ClawArena — dependency installer
#  Installs: clawarena (editable) + supported framework CLIs
#            + MetaClaw proxy
# ============================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[clawarena]${NC} $*"; }
warn()  { echo -e "${YELLOW}[clawarena]${NC} $*"; }
fail()  { echo -e "${RED}[clawarena]${NC} $*"; exit 1; }

# ── locate project root ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── pre-flight checks ──
command -v python3 >/dev/null 2>&1 || fail "python3 not found"
command -v pip     >/dev/null 2>&1 || fail "pip not found"

# ============================================================
#  1. ClawArena itself (editable install with dev extras)
# ============================================================
info "Installing clawarena (editable) ..."
pip install -e "$PROJECT_ROOT[dev]"

# ============================================================
#  2. Python framework dependencies
# ============================================================
info "Installing Python framework SDKs ..."

# Claude Code Python SDK (claude_agent_sdk)
pip install claude-agent-sdk

# Nanobot CLI + library
pip install nanobot-ai

# Gemini SDK (new unified `google-genai`, exposes `from google import genai`)
pip install google-genai

# ============================================================
#  3. MetaClaw (Python — editable install, source must persist)
# ============================================================
# Override METACLAW_SRC to point at an existing checkout; otherwise MetaClaw
# is cloned fresh into ~/.local/share/metaclaw (source must persist for
# editable install).
METACLAW_REPO_URL="${METACLAW_REPO_URL:-https://github.com/aiming-lab/MetaClaw.git}"
METACLAW_SRC="${METACLAW_SRC:-$HOME/.local/share/metaclaw}"

_install_metaclaw() {
    if [ -d "$METACLAW_SRC/.git" ]; then
        info "MetaClaw source found at $METACLAW_SRC — pulling latest ..."
        git -C "$METACLAW_SRC" pull --ff-only 2>/dev/null \
            || warn "git pull failed (non-fatal); using existing checkout"
    else
        info "Cloning MetaClaw from $METACLAW_REPO_URL into $METACLAW_SRC ..."
        mkdir -p "$(dirname "$METACLAW_SRC")"
        if ! git clone --depth 1 "$METACLAW_REPO_URL" "$METACLAW_SRC"; then
            warn "MetaClaw clone failed (non-fatal); set METACLAW_SRC=/path/to/MetaClaw to use a local copy"
            return
        fi
    fi
    info "Installing MetaClaw [evolve] from $METACLAW_SRC ..."
    # [evolve] only — skills_only mode does not require [rl] (PyTorch/CUDA).
    pip install -e "$METACLAW_SRC[evolve]" \
        || warn "MetaClaw install failed (non-fatal); check pip output above"
}

_install_metaclaw

# ============================================================
#  4. Node.js / npm CLIs
# ============================================================
if command -v npm >/dev/null 2>&1; then
    info "Installing npm-based CLIs ..."

    # Claude Code CLI
    npm ls -g @anthropic-ai/claude-code >/dev/null 2>&1 \
        || npm install -g @anthropic-ai/claude-code

    # Claude Code Router (ccr) — required by claude-code engine
    # when routing through OpenAI-compatible / third-party providers.
    npm ls -g @musistudio/claude-code-router >/dev/null 2>&1 \
        || npm install -g @musistudio/claude-code-router

    # OpenClaw CLI (from public npm registry; ~791 transitive packages)
    npm ls -g openclaw >/dev/null 2>&1 \
        || npm install -g openclaw
else
    warn "npm not found — skipping Claude Code CLI, claude-code-router, openclaw"
fi

# ============================================================
#  5. Go + PicoClaw
# ============================================================
GO_REQUIRED="1.25.9"
GO_SDK_DIR="$HOME/.local/go-sdk"
GOBIN_DIR="$HOME/.local/bin"
# PicoClaw source: by default clone fresh from upstream into a temp dir and
# remove it after install. Set PICOCLAW_SRC to re-use an existing checkout.
PICOCLAW_REPO_URL="${PICOCLAW_REPO_URL:-https://github.com/sipeed/picoclaw.git}"
PICOCLAW_SRC="${PICOCLAW_SRC:-}"

# Pick up a previously downloaded Go SDK before running `command -v go`
if ! command -v go >/dev/null 2>&1 && [ -x "$GO_SDK_DIR/bin/go" ]; then
    export PATH="$GO_SDK_DIR/bin:$PATH"
fi

_need_go_install() {
    command -v go >/dev/null 2>&1 || return 0
    local ver
    ver=$(go version | grep -oP 'go\K[0-9]+\.[0-9]+(\.[0-9]+)?') || return 0
    ! printf '%s\n%s\n' "$GO_REQUIRED" "$ver" | sort -V -C
}

if _need_go_install; then
    ARCH=$(uname -m)
    case $ARCH in
        x86_64)  GOARCH="amd64" ;;
        aarch64) GOARCH="arm64" ;;
        *) warn "Unsupported arch $ARCH — cannot auto-install Go; skipping PicoClaw"; GOARCH="" ;;
    esac

    if [ -n "$GOARCH" ]; then
        GO_TARBALL="go${GO_REQUIRED}.linux-${GOARCH}.tar.gz"
        GO_URL="https://go.dev/dl/${GO_TARBALL}"
        info "Go ${GO_REQUIRED} not found — downloading to ${GO_SDK_DIR} ..."
        rm -rf "$GO_SDK_DIR"
        mkdir -p "$GO_SDK_DIR"
        curl -fsSL "$GO_URL" | tar -xz -C "$GO_SDK_DIR" --strip-components=1
        export PATH="$GO_SDK_DIR/bin:$PATH"
        info "Go installed: $(go version)"
    fi
fi

_build_picoclaw_from_dir() {
    # usage: _build_picoclaw_from_dir <src_dir>
    # Preconditions: go + make available, src_dir has cmd/picoclaw + Makefile.
    # Makefile runs `go generate` (embeds workspace/) then builds, and
    # installs to INSTALL_PREFIX/bin — default $HOME/.local/bin.
    local src="$1"
    ( cd "$src" && INSTALL_PREFIX="$HOME/.local" make install )
}

if command -v go >/dev/null 2>&1; then
    mkdir -p "$GOBIN_DIR"
    if ! command -v make >/dev/null 2>&1; then
        warn "'make' not found — skipping PicoClaw"
    elif [ -n "$PICOCLAW_SRC" ] && [ -d "$PICOCLAW_SRC/cmd/picoclaw" ] && [ -f "$PICOCLAW_SRC/Makefile" ]; then
        info "Building PicoClaw from PICOCLAW_SRC=$PICOCLAW_SRC ..."
        if _build_picoclaw_from_dir "$PICOCLAW_SRC"; then
            info "picoclaw installed → $GOBIN_DIR/picoclaw"
        else
            warn "PicoClaw local build failed (non-fatal); check that $PICOCLAW_SRC is a clean checkout"
        fi
    else
        # No override supplied — clone a fresh shallow copy into a temp dir,
        # build, then remove. Safe to re-run.
        PICOCLAW_TMP_DIR="$(mktemp -d -t picoclaw-XXXXXX)"
        trap 'rm -rf "$PICOCLAW_TMP_DIR"' EXIT
        info "Cloning PicoClaw from $PICOCLAW_REPO_URL into temp dir ..."
        if git clone --depth 1 "$PICOCLAW_REPO_URL" "$PICOCLAW_TMP_DIR" >/dev/null 2>&1; then
            if _build_picoclaw_from_dir "$PICOCLAW_TMP_DIR"; then
                info "picoclaw installed → $GOBIN_DIR/picoclaw"
            else
                warn "PicoClaw build failed (non-fatal); rerun with PICOCLAW_SRC=/path/to/picoclaw to debug"
            fi
        else
            warn "Failed to clone $PICOCLAW_REPO_URL (non-fatal); set PICOCLAW_SRC=/path/to/picoclaw or check network"
        fi
        rm -rf "$PICOCLAW_TMP_DIR"
        trap - EXIT
    fi
    export PATH="$GOBIN_DIR:$PATH"
else
    warn "go not found — skipping PicoClaw"
fi

# ============================================================
#  6. Verification
# ============================================================
info "Verifying Python imports ..."
VERIFY_OK=true

check_import() {
    local pkg="$1"
    local display="${2:-$1}"
    if python3 -c "import $pkg" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $display ($pkg)"
    else
        echo -e "  ${RED}✗${NC} $display ($pkg)"
        VERIFY_OK=false
    fi
}

check_import clawarena       "clawarena"
check_import claude_agent_sdk "claude-agent-sdk"
check_import pandas           "pandas"
check_import scipy            "scipy"

# google-genai exposes the `genai` sub-package under the `google` namespace
python3 -c "from google import genai" 2>/dev/null \
    && echo -e "  ${GREEN}✓${NC} google-genai (google.genai)" \
    || { echo -e "  ${RED}✗${NC} google-genai (google.genai)"; VERIFY_OK=false; }

# nanobot may register under different module names
python3 -c "import nanobot" 2>/dev/null \
    && echo -e "  ${GREEN}✓${NC} nanobot-ai (nanobot)" \
    || python3 -c "import nanobot_ai" 2>/dev/null \
        && echo -e "  ${GREEN}✓${NC} nanobot-ai (nanobot_ai)" \
        || { echo -e "  ${YELLOW}?${NC} nanobot-ai (import name unresolved — CLI may still work)"; }

info "Verifying CLI commands ..."
check_cmd() {
    local cmd="$1"
    if command -v "$cmd" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} $cmd"
    else
        echo -e "  ${YELLOW}-${NC} $cmd (not in PATH)"
    fi
}

check_cmd clawarena
check_cmd metaclaw
check_cmd claude
check_cmd ccr
check_cmd openclaw
check_cmd picoclaw
check_cmd nanobot

echo ""
if $VERIFY_OK; then
    info "Setup complete."
else
    warn "Some Python packages failed to import — check messages above."
fi

# ── PATH hint ──
NEEDS_PATH_HINT=false
command -v picoclaw >/dev/null 2>&1 || NEEDS_PATH_HINT=true
if $NEEDS_PATH_HINT; then
    echo ""
    warn "Add the following to ~/.bashrc to make CLI tools available in future sessions:"
    echo ""
    echo "    export PATH=\"\$HOME/.local/go-sdk/bin:\$HOME/.local/bin:\$PATH\""
    echo ""
fi
