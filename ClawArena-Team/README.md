<div align="center">

<h1>ClawArena-Team</h1>

### Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents

<p>
  🌐 <b>English</b> •
  <a href="docs/i18n/README.zh-Hans.md">简体中文</a> •
  <a href="docs/i18n/README.zh-Hant.md">繁體中文</a> •
  <a href="docs/i18n/README.ja.md">日本語</a> •
  <a href="docs/i18n/README.ko.md">한국어</a> •
  <a href="docs/i18n/README.fr.md">Français</a> •
  <a href="docs/i18n/README.de.md">Deutsch</a> •
  <a href="docs/i18n/README.es.md">Español</a> •
  <a href="docs/i18n/README.pt.md">Português</a> •
  <a href="docs/i18n/README.ru.md">Русский</a>
</p>

<p>
  <a href="https://arxiv.org/abs/2606.31174"><img src="https://img.shields.io/badge/arXiv-2606.31174-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="arXiv 2606.31174" /></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="License MIT" /></a>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Version-v1.0.0-blueviolet?style=flat&labelColor=555" alt="v1.0.0" />
</p>
<p>
  <img src="https://img.shields.io/badge/Scenarios-41-orange?style=flat&labelColor=555" alt="41 Scenarios" />
  <img src="https://img.shields.io/badge/Rounds-258-red?style=flat&labelColor=555" alt="258 Rounds" />
  <img src="https://img.shields.io/badge/Staged%20Updates-72-yellow?style=flat&labelColor=555" alt="72 Staged Updates" />
  <img src="https://img.shields.io/badge/Models-12-9cf?style=flat&labelColor=555" alt="12 Models" />
  <img src="https://img.shields.io/badge/Scoring-Execution--based-success?style=flat&labelColor=555" alt="Execution-based" />
</p>

<img src="assets/hero.png" alt="ClawArena-Team" width="900">

[🔭 Overview](#-overview) • [📈 Leaderboard](#-leaderboard) • [🔑 Key Findings](#-key-findings) • [🚀 Quick Start](#-quick-start) • [🧰 Capability Surface & Tools](#-capability-surface--tools) • [📊 Data & Evaluation](#-data--evaluation) • [🔍 Case Studies](#-case-studies) • [📖 Documentation](#-documentation) • [🏗️ Project Structure](#️-project-structure) • [📚 Citation](#-citation) • [📄 License](#-license)

</div>

---

## 🔭 Overview

LM agents are increasingly deployed as **managers** — one main model creates specialized subagents, delegates work, and orchestrates their parallel, asynchronous returns through dynamic workflows. Existing benchmarks score a policy's own task-solving or a fixed multi-agent system, but none isolate the **management ability** of the single LM acting as leader.

**ClawArena-Team** (the team-management variant in the ClawArena series) isolates exactly this. A **text-only main agent** must complete multi-turn, multimodal, multi-directory tasks it cannot do alone, by creating, empowering, scheduling, and integrating subagents from a **fixed, locally-served pool**. Every manager commands the same workers, so score differences reflect *management skill, not raw capability*.

- **41 scenarios · 258 evaluation rounds · 72 staged updates**, spanning **law, medicine, engineering, business, and science**.
- **Text-only, part-visible main agent** — it natively perceives only text and reaches only part of the workspace, so delegation is mandatory.
- **Fixed subagent pool** served locally via vLLM (`llm`/`vlm`/`omni`), held identical across every evaluated manager.
- **Execution-based scoring, no LLM judge** — every round ships a shell command whose exit code (with optional output matching) decides pass/fail.

---

## 📈 Leaderboard

We rank main-agent models by the composite **Subagent-Management Score (SMS)**, which multiplies task correctness by a least-privilege and modality-routing management factor:

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS ≤ TCR always:** management can only discount task correctness, never inflate it. A model that manages perfectly but fails the task scores zero.

| Model | TCR | TPP | ROC | WPP | MCA | **SMS** | Cost ($) | Rounds |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| claude-fable-5 | **74.4** | 76.4 | 98.8 | **49.2** | **97.9** | **60.0** | 92.8 | **192/258** |
| gemini-3.5-flash | 69.8 | 69.8 | 95.9 | 45.7 | 96.7 | 53.8 | 23.7 | 180/258 |
| gpt-5.5 | 63.6 | **79.9** | 98.7 | 47.5 | 95.2 | 51.0 | 43.3 | 164/258 |
| glm-5.2 | 66.3 | 67.4 | 95.4 | 44.4 | 96.7 | 50.4 | 22.9 | 171/258 |
| gpt-5.4 | 63.2 | 77.3 | 98.8 | 40.8 | 97.6 | 49.7 | 19.5 | 163/258 |
| gemini-3.1-pro | 65.5 | 76.4 | 97.3 | 36.6 | 92.9 | 49.6 | 20.5 | 169/258 |
| kimi-k2.6 | 64.3 | 76.8 | 92.0 | 41.9 | 93.9 | 49.0 | 28.7 | 166/258 |
| claude-sonnet-4-6 | 61.6 | 77.3 | **99.4** | 43.2 | 95.2 | 48.5 | 39.7 | 159/258 |
| deepseek-v4-pro | 58.9 | 73.9 | 98.5 | 46.3 | 96.5 | 46.4 | **1.7** | 152/258 |
| qwen3.6-27b | 60.9 | 72.5 | 95.7 | 40.7 | 96.2 | 46.4 | 15.0 | 157/258 |
| gemma-4-31b | 56.6 | 79.0 | 97.7 | 37.9 | 95.5 | 43.9 | 3.5 | 146/258 |
| glm-4.7-flash | 34.5 | 22.4 | 85.8 | 11.7 | 57.2 | 15.3 | 0.8 | 89/258 |

<sub>All values in %, twelve models × 41 scenarios in a single evaluation run, sorted by **SMS**. The newly released `glm-5.2` (via the official z.ai API) is the strongest open-weight manager — SMS 50.4, 4th overall — overtaking `kimi-k2.6` to top the open-weight models. **Bold** marks the column-best value (best in each column highlighted independently). Cost ($): per-run main-agent API cost at provider / OpenRouter list rates — lower is better, so it is left unbolded; subagents run on the fixed local pool and are not priced. Rounds: rounds passed out of 258. `claude-fable-5` is evaluated as shipped, with a vendor-recommended refusal → `claude-opus-4-8` fallback.</sub>

> 📥 Submit a result? See [docs/submit-to-leaderboard.md](docs/submit-to-leaderboard.md). Example runs and contributed results live in [`submissions/`](submissions/).

---

## 🔑 Key Findings

Across twelve proprietary, community-hosted, and self-hosted main-agent models, three findings emerge.

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ The bottleneck is *privilege granting*, not perception

The two "easy" axes are nearly saturated — read-only compliance (ROC ≥ 92%) and modality-choice accuracy (MCA ≥ 92%) for every capable model. The discriminating axes are the privilege-precision metrics: **Workspace-Permission Precision (WPP) *never* reaches 50%** for any model. Subagents are routinely granted roughly twice the files they actually touch.

</td>
<td width="33%" valign="top">

### 2️⃣ Cost and management quality are *decoupled*

Main-agent API cost spans **over 100×** (\$0.8 → \$93 per run) while SMS spans **under 4×**. The cheapest open models sit on the Pareto frontier — `deepseek-v4-pro` reaches SMS 46.4 at just \$1.7 — while several high-cost models (`gpt-5.5`, `sonnet-4-6`, `kimi-k2.6`) are *dominated* by mid-cost `gemini-3.5-flash`. The open-weight `glm-5.2` ($22.9) also lands on the frontier as the strongest open model.

</td>
<td width="33%" valign="top">

### 3️⃣ Scores cluster, behaviors diverge

Below the flagship, ten models cluster within a **9.9-point SMS band** (43.9–53.8), yet their orchestration behaviors differ by **more than an order of magnitude**. The per-subagent forbidden-access rate ranges from 0.48 to 5.78 among capable models (~12×), and dynamic-workflow use ranges from 8 to 112 invocations.

</td>
</tr>
</table>

<div align="center">

| Cost vs. management (Finding 2) | Permission violations (Finding 3) |
|:---:|:---:|
| <img src="assets/pareto.png" alt="SMS vs. main-agent API cost, log scale; cheap open models on the Pareto frontier" width="430"> | <img src="assets/forbidden.png" alt="Per-model forbidden-access counts MAF/SAFt/SAFa on a log scale; SAFa diverges ~12x" width="430"> |

</div>

**Modality routing.** Managers overwhelmingly default to the `llm` key and create comparatively few `vlm`/`omni` specialists; when they *do* route by modality they do it correctly (hence the high MCA), but they under-use the multimodal workers.

<div align="center">
<img src="assets/modality.png" alt="Subagent model-key distribution: managers default to the llm key and under-use vlm/omni" width="780">
</div>

---

## 🚀 Quick Start

See [`docs/running-experiments.md`](docs/running-experiments.md) for the full walkthrough (serving the pool, picking targets, resuming runs).

### 1. Install

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

This installs the `clawarena-team` CLI (short aliases: **`cateam`** / **`ca-team`**). The tokenizer and chat template are **bundled in `helper/`** — no download step required.

### 2. Serve the fixed subagent pool (local vLLM)

The subagent pool is held identical across every evaluated main agent, so management is the only variable:

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. Validate, run, and analyze

```bash
# Validate dataset structure (anything that passes check is guaranteed to run)
clawarena-team check -d data/clawarena-team/

# Run the full 41-scenario benchmark (inference + live scoring + report)
clawarena-team run -d data/clawarena-team/ -o results/ --model '<model-json>'

# Or run selected scenarios by id (comma-separated) via -t
clawarena-team run -d data/clawarena-team/ -t s_finance_options_pricing -o results/ --model '<model-json>'

# Resume only the unfinished scenarios into a fresh output dir
clawarena-team resume -d data/clawarena-team/ -O results/old -o results/new --model '<model-json>'

# Dataset statistics (token / file / modality distribution)
clawarena-team stats -d data/clawarena-team/

# Compare two or more runs, ranked by SMS
clawarena-team compare -r results/run_a/report.json -r results/run_b/report.json -o results/diff/
```

> The short aliases `cateam` and `ca-team` are interchangeable with `clawarena-team` everywhere (e.g. `cateam run ...`).

<details>
<summary><b>The <code>--model</code> JSON</b></summary>

```json
{
  "main": {
    "provider": "openai_compat",
    "model_id": "gpt-5.4",
    "api_base": "https://...",
    "api_key": "sk-...",
    "modalities": {"text": true, "image": 4}
  },
  "llm":  {"provider": "...", "model_id": "...", "modalities": {"text": true}},
  "vlm":  {"provider": "...", "model_id": "...", "modalities": {"text": true, "image": 8, "video": 2}},
  "omni": {"provider": "...", "model_id": "...", "modalities": {"text": true, "image": 8, "audio": 4, "video": 2}}
}
```

The same string can be supplied via `CATEAM_MODEL_JSON`. The `main.modalities` field decides what the main agent natively perceives; `Read` degrades out-of-modality files to a textual placeholder and suggests delegation. See [`docs/cli.md`](docs/cli.md) for all flags and `CATEAM_*` variables, [`docs/dataset.md`](docs/dataset.md) for the dataset format, and [`docs/provider.md`](docs/provider.md) for wiring up a provider.
</details>

---

## 🧰 Capability Surface & Tools

ClawArena-Team frames subagent management as a **principal–agent problem**. The main agent's capability surface decomposes into six concrete operations, each forced by the scenario design:

| Operation | What it requires |
|---|---|
| **Creation** | Create a subagent with a system prompt, a model key, a tool subset, and a workspace path whitelist (a subset of its own). |
| **Modality routing** | Route images/video to a `vlm` and audio to an `omni`, since the manager perceives only text. |
| **Least-privilege empowerment** | Grant only the tools and paths a subagent actually needs; over-granting is wasteful and unsafe. |
| **Scheduling** | Run subagents foreground or background, as new or continued (resumed) sessions, and in parallel; background tasks notify the manager on completion. |
| **Dynamic workflows** | Author multi-subagent orchestration (parallel + pipeline stages) at runtime over the same pool. |
| **Integration** | Fuse subagent returns into a correct deliverable — only the integrated answer is scored. |

The main agent is exposed **CapitalCase** tools whose names, descriptions, and parameters mirror real harness conventions for cross-benchmark comparability:

| Tool | Purpose |
|---|---|
| **Read** | Read a file; out-of-modality content degrades to a textual placeholder that suggests delegation. |
| **Write** | Create or overwrite a file in the workspace. |
| **Edit** | Apply a targeted in-place edit to an existing file. |
| **Bash** | Run a shell command in the sandbox (`realpath`-checked paths). |
| **Grep** | Search file contents by pattern. |
| **Glob** | Find files by name pattern. |
| **CreateSubagent** | Define a subagent: system prompt, model key, tool subset, and workspace path whitelist. |
| **RunSubagent** | Invoke a subagent foreground or background, as a new or continued (resumed) session. |
| **ListSubagents** | List the subagents created so far and their status. |
| **InspectSubagent** | Inspect a subagent's configuration, granted privileges, and run history. |
| **Workflow** | JS-style orchestration DSL — `agent()`, `parallel()`, `pipeline()` — to compose multi-subagent runs at runtime. |

System-level signals (environment, token thresholds) are injected via `<system-reminder>` blocks; background-task completions arrive via `<task-notification>` blocks. All path access is `realpath`-checked and symlink escapes are rejected and counted as forbidden accesses.

### Fixed subagent pool (the controlled variable)

| Key | Model | Server | Native modalities |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | local vLLM | text |
| `vlm`  | gemma-4-31b-it | local vLLM | text, image, video |
| `omni` | gemma-4-e4b-it | local vLLM | text, image, audio, video |

Every main agent commands this same team; only the main agent varies across runs.

---

## 📊 Data & Evaluation

Every scenario provides a workspace, a sequence of user questions, and ground-truth checks. Between some rounds the workspace receives **staged updates** (new or replaced files) that change subsequent answers, requiring sustained management of an evolving task rather than a one-shot solution.

<div align="center">
<img src="assets/heatmap.png" alt="Per-scenario SMS heatmap: 12 models x 41 scenarios, difficulty is uneven and model-specific" width="820">
<br/>
<sub>Per-scenario × model SMS heatmap — difficulty is uneven and model-specific.</sub>
</div>

**Scoring components** (all in $[0,1]$, no LLM judge):

| Metric | Meaning |
|---|---|
| **TCR** — Task Completion Rate | Mean pass rate over user questions. |
| **TPP** — Tool-Permission Precision | Per subagent, fraction of granted tool types that are actually used. |
| **ROC** — Read-Only Compliance | Per subagent, 0 if a read-only subagent was granted a mutating tool, else 1. |
| **WPP** — Workspace-Permission Precision | Per subagent, accessed files ÷ granted files. |
| **MCA** — Modality-Choice Accuracy | Per subagent, whether a `vlm` actually reads image/video and an `omni` reads audio (`llm` scores 1). |

Every scenario satisfies **ten hard design constraints (C1–C10)** — unreadable regions, substantive staged updates, full tool-surface use, ≥8 directories with decoys, non-text modality rounds, parallel-required tasks, session-reuse pairs, cross-round dependencies, modality decoys, and machine-checkable answers — each targeting a distinct management failure mode that a single LM could otherwise route around.

### Dataset composition

- **41 scenarios · 258 rounds**, of which 44 (17.1%) are preceded by staged updates.
- **72 update groups over 255 files** (61.1% `new`, 38.9% `replace`, mean 3.54 files/group).
- **170.5 MiB · 28.9 M tokens** — 71.9% workspace content, 27.9% staged updates.
- Modality mix: text dominates files/tokens, while audio and image dominate raw bytes — a substantial non-text payload a text-only manager cannot consume directly.

ClawArena-Team is **built, not collected**: workspace corpora, multimodal assets, ground truth, and execution checks are all procedurally synthesized from the same version-controlled scripts via a **synthesis–verification flywheel** in which a real baseline subagent-management run is the final acceptance gate. The benchmark is, in effect, authored by the very capability it measures. See [`docs/dataset.md`](docs/dataset.md) and the paper appendix for the format and construction methodology.

For finer-grained distributions, see [`docs/data-stats/`](docs/data-stats/): each subset (`demo` / `wave1` / `wave3` / `wave4`) and the full set has its own `STATS.md` plus charts (token / file-size / modality distribution, tag coverage, ...), generated by `clawarena-team stats`.

---

## 🔍 Case Studies

Twelve cases drawn directly from recorded run transcripts and `metadata.json` files — all numbers and quoted strings verbatim — concretely grounding the three findings and the management capability surface.

<details>
<summary><b>Cases 1–4: over-granting under the strongest manager, correct modality routing, the modality-decoy trap, and cost decoupled from quality</b></summary>
<br/>
<div align="center">
<img src="assets/case_study_1.png" alt="Case studies 1-4" width="900">
</div>
</details>

<details>
<summary><b>Cases 5–8: identical scores with divergent forbidden-access, authoring a dynamic workflow (and a fan-out that crashes), logical parallelism without true background scheduling, and true background plus workflow parallelism</b></summary>
<br/>
<div align="center">
<img src="assets/case_study_2.png" alt="Case studies 5-8" width="900">
</div>
</details>

<details>
<summary><b>Cases 9–12: a pending correction that never propagates, a capability cliff the manager cannot operate, the management ceiling (parallel fan-out, adaptive retry, least privilege), and what good management looks like</b></summary>
<br/>
<div align="center">
<img src="assets/case_study_3.png" alt="Case studies 9-12" width="900">
</div>
</details>

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [CLI Reference](docs/cli.md) | All commands, flags, and `CATEAM_*` environment variables |
| [Dataset Format](docs/dataset.md) | Scenario layout, rounds, staged updates, ground-truth checks |
| [Provider Guide](docs/provider.md) | Wiring up main-agent providers (OpenAI-compat, Gemini, OpenRouter, ...) |
| [Running Experiments](docs/running-experiments.md) | Serving the subagent pool and running / resuming a full sweep |
| [Submit to Leaderboard](docs/submit-to-leaderboard.md) | Packaging a run and contributing it to [`submissions/`](submissions/) |

---

## 🏗️ Project Structure

```
ClawArena-Team
├── src/clawarena_team/        # Core package (CLI clawarena-team / cateam)
│   ├── cli.py               # CLI entry point
│   ├── agent/  runner/      # Main-agent loop & scenario/run orchestration
│   ├── tools/  sandbox/     # CapitalCase tools, realpath-checked sandbox
│   ├── provider/            # Provider adapters (OpenAI-compat, Gemini, OpenRouter, ...)
│   ├── scoring/  stats/     # Execution-based scoring + token/structural analysis
│   └── persistence/  prompts.py  tokenizer.py  types.py
├── data/clawarena-team/   # Dataset: 41 scenarios, 258 rounds, full + per-wave tests-*.json
├── configs/                 # default.yaml + variants (global defaults)
├── docs/                    # cli.md, dataset.md, provider.md, running-experiments.md, submit-to-leaderboard.md, i18n/, data-stats/
├── scripts/                 # fetch_helper.py, serve_gemma-*.py, eval runners
├── submissions/             # Example contributed runs (local-gemma-31b, local-qwen3.6-27b)
├── helper/                  # Bundled tokenizer + chat template (no weights)
├── assets/                  # Figures used in this README
└── tests/                   # Unit tests, synced with src/
```

---

## 📚 Citation

```bibtex
@article{xiong2026clawarenateam,
  title   = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author  = {Xiong, Kaiwen and Ji, Haonian and Qiu, Shi and Zheng, Zeyu and Xie, Cihang and Ye, Xinyu and Yao, Huaxiu},
  journal = {arXiv preprint arXiv:2606.31174},
  year    = {2026}
}
```

---

## 📄 License

This project is licensed under the [MIT License](../LICENSE).
</content>
</invoke>
