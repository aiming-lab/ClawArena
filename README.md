<div align="center">

<img src="assets/claweval.png" alt="ClawArena" width="500">

<br/>

## Benchmarking AI Agents in Evolving Information Environments.

<br/>

<img src="assets/overview2-small.png" alt="ClawArena Overview" width="800">

<br/>

<br/>


<table>
  <tr>
    <td align="center" width="180" height="140">
      <a href="https://github.com/openclaw/openclaw">
        <img src="assets/openclaw-logo.svg" alt="OpenClaw" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/anthropics/claude-code">
        <img src="https://claude.ai/favicon.ico" alt="Claude Code" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/aiming-lab/MetaClaw">
        <img src="assets/metaclaw-logo.png" alt="MetaClaw" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/sipeed/picoclaw">
        <img src="assets/picoclaw-logo.png" alt="PicoClaw" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/HKUDS/nanobot">
        <img src="assets/nanobot-logo.png" alt="Nanobot" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <b style="font-size:1.1em">+ Any Agent</b>
    </td>
  </tr>
  <tr>
    <td align="center"><b>OpenClaw</b></td>
    <td align="center"><b>Claude Code</b></td>
    <td align="center"><b>MetaClaw</b></td>
    <td align="center"><b>PicoClaw</b></td>
    <td align="center"><b>Nanobot</b></td>
    <td align="center">via <a href="docs/plugin.md">Plugin</a></td>
  </tr>
</table>

<br/>

<p>
  🇨🇳 <a href="docs/README_zh.md">中文</a> •
  🇯🇵 <a href="docs/README_ja.md">日本語</a> •
  🇰🇷 <a href="docs/README_ko.md">한국어</a> •
  🇪🇸 <a href="docs/README_es.md">Español</a> •
  🇫🇷 <a href="docs/README_fr.md">Français</a> •
  🇩🇪 <a href="docs/README_de.md">Deutsch</a>
</p>

<br/>

<p>
  <a href="https://arxiv.org/abs/2604.04202"><img src="https://img.shields.io/badge/arXiv-2604.04202-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="arXiv" /></a>
  <a href="https://www.clawarena.cc/"><img src="https://img.shields.io/badge/Website-clawarena.cc-4285F4?style=flat&logo=googlechrome&logoColor=white" alt="Website" /></a>
  <a href="https://github.com/aiming-lab/ClawArena"><img src="https://img.shields.io/badge/GitHub-ClawArena-181717?style=flat&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="License MIT"></a>
  <a href="https://github.com/aiming-lab/ClawArena/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat" alt="PRs welcome" /></a>
</p>
<p>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Scenarios-12-orange?style=flat&labelColor=555" alt="12 Scenarios" />
  <img src="https://img.shields.io/badge/Rounds-337-red?style=flat&labelColor=555" alt="337 Rounds" />
  <img src="https://img.shields.io/badge/Dynamic%20Updates-45-yellow?style=flat&labelColor=555" alt="45 Dynamic Updates" />
  <img src="https://img.shields.io/badge/Frameworks-5-blueviolet?style=flat&labelColor=555" alt="5 Frameworks" />
</p>

[🔭 Overview](#-overview) • [📈 Leaderboard](#-leaderboard) • [🆚 Benchmark Comparison](#-benchmark-comparison) • [🚀 Quick Start](#-quick-start) • [🤖 Supported Frameworks](#-supported-frameworks) • [📊 Data & Evaluation](#-data--evaluation) • [🔍 Case Studies](#-case-studies) • [📖 Documentation](#-documentation) • [🏗️ Project Structure](#-project-structure) • [🙏 Related Projects](#-related-projects) • [📚 Citation](#-citation) • [📄 License](#-license)

</div>

---

## 🔭 Overview

**ClawArena** is a benchmark evaluation platform for AI coding agents. It provides a unified pipeline to run inference, score results, and compare performance across different agent frameworks on the same set of realistic, multi-session scenarios.

- **12 multi-turn scenarios** spanning diverse professional contexts — retail analytics, finance, healthcare, information security, HR, education, research integrity, and others
- **337 evaluation rounds** mixing `multi_choice` reasoning (95 rounds) and `exec_check` execution verification (242 rounds)
- **45 dynamic updates** — new files and chat sessions injected mid-evaluation to probe belief revision and contradiction handling
- **Multi-session context** — agents reason over workspace files and multi-channel chat histories (IM, email, etc.) within each scenario
- **Framework-agnostic** — five frameworks evaluated in the paper (OpenClaw, Claude Code, NanoBot, PicoClaw, MetaClaw); add new ones via the [plugin system](docs/plugin.md)
- **[MetaClaw](https://github.com/aiming-lab/MetaClaw) integration** — evaluate agents enhanced with memory, skills, and RL

<div align="center">
<img src="assets/overview.png" alt="ClawArena Cross-Domain Data Sample Gallery" width="900">
</div>

---

## 📈 Leaderboard

We rank agents with the **Composite Reliability Score (CRS)**, which weighs raw correctness equally against behavioral consistency:

- **TCR** (Task Completion Rate) = $S/N$ — mean correctness across all rounds, decomposed into MC and EC sub-scores.
- **SC** (Success Cohesion) = $(S - k)/(N - 1)$ — concentration of correct rounds into long unbroken runs; SC = 1 for one streak, SC = 0 for pass/fail alternation.
- **FD** (Failure Dispersion) = $1 - (S_f - k_f)/(N - 1)$ — penalises prolonged failure runs.
- **Robustness** = SC × FD — multiplicative form so collapse on either axis hurts the score.
- **CRS** = (TCR + Robustness) / 2.

_All numbers are macro-averaged across the 12 scenarios / 337 rounds and sorted by CRS._

| Rank | Model | Framework | TCR | MC | EC | SC | FD | **CRS** |
|---:|---|---|--:|--:|--:|--:|--:|--:|
| 1  | GPT-5.5            | OpenClaw    | 78.34 | 75.79 | 79.34 | 61.24 | 95.06 | **68.28** |
| 2  | Claude Opus-4.7    | Claude Code | 76.13 | 65.26 | 80.58 | 60.06 | 94.06 | 66.31 |
| 3  | Gemma-4-31B        | OpenClaw    | 75.37 | 81.05 | 73.14 | 56.76 | 91.90 | 63.80 |
| 4  | GPT-5.1            | OpenClaw    | 70.33 | 75.79 | 68.18 | 58.96 | 95.37 | 63.28 |
| 5  | Claude Sonnet-4.6  | Claude Code | 73.36 | 63.16 | 77.69 | 54.80 | 93.02 | 62.16 |
| 6  | Claude Haiku-4.5   | Claude Code | 72.29 | 64.21 | 75.62 | 54.74 | 90.54 | 60.93 |
| 7  | GLM-5.1            | OpenClaw    | 72.70 | 72.63 | 72.73 | 52.74 | 92.07 | 60.63 |
| 8  | Mimo-V2.5-Pro      | OpenClaw    | 71.45 | 66.32 | 73.55 | 52.23 | 91.62 | 59.65 |
| 9  | GPT-5.4            | OpenClaw    | 71.22 | 71.58 | 71.07 | 51.51 | 90.78 | 58.99 |
| 10 | Gemini-3.1-Pro     | OpenClaw    | 69.57 | 66.32 | 71.07 | 50.54 | 90.23 | 57.59 |
| 11 | Kimi-K2.5          | OpenClaw    | 69.44 | 60.00 | 73.14 | 48.86 | 90.02 | 57.24 |
| 12 | Qwen3.6-27B        | OpenClaw    | 66.63 | 65.26 | 68.60 | 48.40 | 93.12 | 55.85 |
| 13 | DeepSeek-V4-Pro    | OpenClaw    | 66.89 | 57.89 | 70.66 | 48.56 | 89.82 | 55.25 |
| 14 | Qwen3.6-Plus       | OpenClaw    | 67.06 | 71.58 | 65.29 | 47.89 | 90.38 | 55.17 |
| 15 | GPT-5.2            | OpenClaw    | 65.88 | 61.05 | 67.77 | 47.21 | 90.01 | 54.18 |
| 16 | Qwen3.6-35B-A3B    | OpenClaw    | 60.24 | 51.58 | 63.64 | 42.17 | 88.93 | 48.86 |
| 17 | Ling-2.6           | OpenClaw    | 55.05 | 66.32 | 50.83 | 37.62 | 87.94 | 44.07 |
| 18 | GLM-4.7-Flash      | OpenClaw    | 54.10 | 42.11 | 57.02 | 30.55 | 77.05 | 38.82 |

<sub>Each model is shown under its primary harness: Anthropic models through Claude Code (incompatible with OpenClaw), all others under OpenClaw. See the paper for the cross-framework comparison that varies the harness while fixing the model.</sub>

---

## 🆚 Benchmark Comparison

How ClawArena differs from other harness-native agent benchmarks. Most prior work covers at most two of the four design axes; ClawArena is the only benchmark to satisfy all four simultaneously while reporting across five frameworks.

Column legend — ✅ supported · ❌ unsupported · 🟡 partial (mechanism present but weakened, e.g., third-party messages exposed only as plain files rather than channel-tagged sessions, or preferences encoded as static persona rather than learned in silent rounds):

- **MSC** (Multi-Source Conflict): agent must analyse user–third-party conversations distinguished by channel.
- **DU** (Dynamic Update): environment is overwritten between user turns (intra-loop tool-return dynamics do not count).
- **MU** (Multi-User turn): user re-engages with new queries across rounds.
- **Pref.** (Implicit personalization): user preferences applied in silent-exam rounds.
- **Frmw.**: number of agent frameworks evaluated.

| Benchmark | Task sourcing | Exec. mode | MSC | DU | MU | Pref. | Verification | Frmw. | Scale (Q / Scen.) |
|---|---|---|:---:|:---:|:---:|:---:|---|:---:|---|
| [ClawBench](https://github.com/reacher-z/ClawBench)         | Manual pool                 | Live web              | ❌ | ❌ | ❌ | ❌ | rule+llm   | 8 | 283 / 144 sites |
| [Claw-Eval](https://github.com/claw-eval/claw-eval)         | Curated from upstream       | Sandbox + mock        | ❌ | ❌ | ✅ | ❌ | rule+llm   | 1 | 300 / 9 cats |
| [Claw-Eval-Live](https://github.com/Claw-Eval-Live/Claw-Eval-Live)    | Live signals (quarterly)    | Mock services         | ❌ | ❌ | ❌ | ❌ | rule+llm   | 1 | 105 / 17 fam. |
| [ClawMark](https://github.com/evolvent-ai/ClawMark)          | Manual + AI synthesis       | Sandboxed services    | ✅ | ✅ | ✅ | ❌ | rule-based | 1 | 100 / 13 scen. |
| [ClawsBench](https://github.com/benchflow-ai/ClawsBench)        | Expert-designed             | Mock services         | ✅ | ❌ | ❌ | ❌ | rule-based | 4 | 44 / 5 svc. |
| [MetaClaw-Bench](https://github.com/aiming-lab/MetaClaw)     | Synthetic                   | Workspace sim         | 🟡 | ✅ | ✅ | 🟡 | rule-based | 1 | 346 / 30 days |
| [PinchBench](https://github.com/pinchbench/skill)        | Manual (real-world)         | Real (OpenClaw)       | ❌ | ❌ | ❌ | ❌ | rule+llm   | 1 | 23 / 8 cats |
| [QwenClawBench](https://huggingface.co/datasets/skylenage-ai/QwenClawBench)     | Empirical (claimed)         | Real (Docker)         | ❌ | ❌ | ❌ | 🟡 | rule+llm   | 1 | 100 / 8 dom. |
| [WildClawBench](https://github.com/InternLM/WildClawBench)     | Manual (in the wild)        | Real (OpenClaw)       | ✅ | ❌ | ❌ | 🟡 | rule+llm   | 1 | 60 / 6 cats |
| [ZClawBench](https://huggingface.co/datasets/zai-org/ZClawBench)        | Manual + synthetic          | Real + part. mock     | ❌ | ❌ | ❌ | ❌ | rule+llm   | 1 | 116 / 6 cats |
| **ClawArena (Ours)** | **Empirical synthesis** | **Multi-channel sim** | ✅ | ✅ | ✅ | ✅ | rule-based | **5** | **337 / 12 scen.** |

---

## 🚀 Quick Start

### 1. Install everything

```bash
bash scripts/setup.sh
```

This installs ClawArena (with dev extras), MetaClaw, and the framework CLIs (OpenClaw, Claude Code, Nanobot, PicoClaw) plus Claude Code Router in one command. See [Installation Guide](docs/installation.md) for manual setup.

### 2. Run the benchmark

First refer to [`scripts/env_example.sh`](scripts/env_example.sh) to configure the environment variables, then run:

```bash
python scripts/test_run.py
```

Edit `scripts/test_run.py` to configure frameworks, concurrency, timeout, and output path.

<details>
<summary><b>Or use the CLI directly</b></summary>

```bash
# Validate data integrity
clawarena check --data data/clawarena/tests.json

# Run inference for a single framework
clawarena infer --data data/clawarena/tests.json --framework openclaw --out results/

# Score results
clawarena score --infer-dir results/

# Generate report
clawarena report --data data/clawarena/tests.json --score-dir results/ --out report/

# Full pipeline (infer + score + report + compare)
clawarena run --data data/clawarena/tests.json --frameworks openclaw,claude-code --out output/
```

See [CLI Reference](docs/cli.md) for all commands and flags.
</details>

<details>
<summary><b>Develop & run tests</b></summary>

```bash
pip install -e ".[dev]"
pytest
```

</details>

---

## 🤖 Supported Frameworks

| Framework | Type | Language | Notes |
|-----------|------|----------|-------|
| [OpenClaw](https://github.com/openclaw/openclaw) | CLI agent | Node.js | — |
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | LLM Proxy | Python | Only supported within [OpenClaw](https://github.com/openclaw/openclaw) and [Nanobot](https://github.com/HKUDS/nanobot) |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) | CLI agent | Node.js | Assisted by [Claude Code Router](https://github.com/musistudio/claude-code-router) |
| [PicoClaw](https://github.com/sipeed/picoclaw) | CLI agent | Go | — |
| [Nanobot](https://github.com/HKUDS/nanobot) | CLI agent | Python | — |

New frameworks can be added via the plugin system without modifying core code — drop in a `.py` file that registers an adapter and load it at run time:

```bash
clawarena infer --data tests.json --framework my_agent --out results/ --plugin my_agent.py
```

See the [Plugin Guide](docs/plugin.md) for the adapter interface and engine round hooks.

[MetaClaw](https://github.com/aiming-lab/MetaClaw) is integrated as a transparent proxy layer for evaluating agents enhanced with memory, skills, and RL. Enable it by adding a `metaclaw` field to `tests.json`; supported host frameworks are **OpenClaw** and **Nanobot**. See the [MetaClaw Guide](docs/metaclaw-guide.md) for managed/unmanaged modes, trigger configuration, and YAML templates.

> **⚠️ Billing & Policy Notice (April 4, 2026):**
Third-party tools/agents like OpenClaw may no longer route traffic via your personal Claude Free/Pro/Max subscription credentials. Any Claude integrations in ClawArena using Claude.ai OAuth login **must switch to official API-key authentication** via the Claude Console or supported cloud providers. Such third-party connections will now consume only your **paid extra usage credits**, not your subscription quota. Refer to [Anthropic's legal and compliance](https://code.claude.com/docs/en/legal-and-compliance) for full policy details.

---

## 📊 Data & Evaluation

Each scenario contains:

- **Workspace files** — documents, spreadsheets, code that the agent can read
- **Session histories** — multi-channel chat logs (IM, email, Slack, etc.)
- **Evaluation questions** — `multi_choice` (reasoning) and `exec_check` (execution verification)
- **Dynamic updates** — new sessions and files injected between rounds

Two question types span the 337 rounds:

| Type | Rounds | Tests | How |
|------|------:|-------|-----|
| `multi_choice` | 95 (28.2%) | Agent's reasoning and comprehension | Extract `\bbox{A,B,...}` from response, compute IoU/F1 against ground truth |
| `exec_check`   | 242 (71.8%) | Agent's actions and file output | Run shell commands to verify exit code and stdout |

<details>
<summary><b>Data construction pipeline (click to expand)</b></summary>
<br/>
<div align="center">
<img src="assets/pipeline_v2.png" alt="ClawArena Construction Pipeline" width="700">
</div>

See [Data Spec](docs/data-spec/) for the full six-layer specification system used to construct all 12 scenarios.
</details>

We have open-sourced the complete data construction specs — including the six-layer scenario design, synthesis guidelines, and pitfall documentation — in [`docs/data-spec/`](docs/data-spec/).

See [Data Structure](docs/data-structure.md) for the full format specification.

---

## 🔍 Case Studies

Ten per-option case studies drawn from ClawArena's 12 scenarios, covering interaction categories MS-R, DU-R, P-R, and `exec_check` across security, clinical, HR, and e-commerce domains.

<details>
<summary><b>Case 1–2: NexaFlow API breach (MS-R) & schema-compliance failure (exec_check)</b></summary>
<br/>
<div align="center">
<img src="assets/case_01_02.png" alt="Case 1-2" width="900">
</div>
</details>

<details>
<summary><b>Case 3–4: Research-integrity compound options (MS-R) & authority-influenced revision (DU-R)</b></summary>
<br/>
<div align="center">
<img src="assets/case_03_04.png" alt="Case 3-4" width="900">
</div>
</details>

<details>
<summary><b>Case 5–6: Wrongful-termination filename prefix (P-R + exec_check) & GDPR structural-output ceiling (exec_check)</b></summary>
<br/>
<div align="center">
<img src="assets/case_05_06.png" alt="Case 5-6" width="900">
</div>
</details>

<details>
<summary><b>Case 7–8: 618 GPU fraud update-specific failures (DU-R) & JSON schema adherence (exec_check)</b></summary>
<br/>
<div align="center">
<img src="assets/case_07_08.png" alt="Case 7-8" width="900">
</div>
</details>

<details>
<summary><b>Case 9–10: Wrongful-termination conjunctive synthesis (MS-R + DU-R) & pipeline authorship final synthesis (exec_check + MS-R)</b></summary>
<br/>
<div align="center">
<img src="assets/case_09_10.png" alt="Case 9-10" width="900">
</div>
</details>

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Installation](docs/installation.md) | Setup guide for ClawArena, frameworks, and MetaClaw |
| [CLI Reference](docs/cli.md) | All commands, flags, and environment variables |
| [Data Structure](docs/data-structure.md) | Dataset format, question types, manifest schema |
| [Provider Guide](docs/provider-usage-guide.md) | LLM provider configuration and priority chain |
| [MetaClaw Guide](docs/metaclaw-guide.md) | MetaClaw integration modes and trigger hooks |
| [Plugin Guide](docs/plugin.md) | Writing and registering external framework adapters |

---

## 🏗️ Project Structure

```
ClawArena
├── src/clawarena/
│   ├── cli.py           # CLI entry point
│   ├── core/            # Pipeline: infer, score, report, compare, check, run, clean
│   ├── stats/           # Token + structural analysis with per-framework layouts
│   ├── engines/         # Agent execution engines (per-framework)
│   ├── data_handlers/   # Data loading, validation, work-copy management
│   ├── adapters/        # Framework adapter composition + registry
│   ├── qtypes/          # Question types: multi_choice, exec_check
│   ├── metaclaw/        # MetaClaw proxy lifecycle and trigger hooks
│   └── plugins/         # External adapter loading (--plugin)
├── data/clawarena/      # Dataset (12 scenarios, 337 rounds)
├── docs/                # Documentation, including docs/data-spec/ (six-layer construction spec)
├── scripts/             # Setup, test runner, comparison utilities
├── helpers/             # Framework-specific helper hooks
└── tests/               # Test suite (356 tests)
```

---

## 🙏 Related Projects

ClawArena builds on and evaluates the following open-source agent frameworks:

- [OpenClaw](https://github.com/openclaw/openclaw) — the primary evaluated CLI agent.
- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — meta-learning proxy that enhances agents with memory, skills, and RL.
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropic's agentic coding tool.
- [Claude Code Router](https://github.com/musistudio/claude-code-router) — route Claude Code requests to different models.
- [PicoClaw](https://github.com/sipeed/picoclaw) — lightweight Go-based CLI agent.
- [Nanobot](https://github.com/HKUDS/nanobot) — Python-native CLI agent with Anthropic API support.

---

## 📚 Citation

```bibtex
@article{ji2026clawarena,
  title={ClawArena: A Multi-Framework Benchmark for Evaluating AI Coding Agents on Realistic Multi-Session Scenarios},
  author={Ji, Haonian and Xiong, Kaiwen and Han, Siwei and Xia, Peng and Qiu, Shi and Zhou, Yiyang and Liu, Jiaqi and Li, Jinlong and Li, Bingzhou and Zheng, Zeyu and Xie, Cihang and Yao, Huaxiu},
  journal={arXiv preprint arXiv:2604.04202},
  year={2026}
}
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
