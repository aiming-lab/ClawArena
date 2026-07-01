<div align="center">

<h1>ClawArena-Team</h1>

### 评测语言模型智能体中的子智能体编排与动态工作流

<p>
  <a href="../../README.md">English</a> •
  <b>简体中文</b> •
  <a href="README.zh-Hant.md">繁體中文</a> •
  <a href="README.ja.md">日本語</a> •
  <a href="README.ko.md">한국어</a> •
  <a href="README.fr.md">Français</a> •
  <a href="README.de.md">Deutsch</a> •
  <a href="README.es.md">Español</a> •
  <a href="README.pt.md">Português</a> •
  <a href="README.ru.md">Русский</a>
</p>

<p>
  <a href="#-引用"><img src="https://img.shields.io/badge/Paper-Preprint-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="论文" /></a>
  <a href="../../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="MIT 许可证" /></a>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Version-v1.0.0-blueviolet?style=flat&labelColor=555" alt="v1.0.0" />
</p>
<p>
  <img src="https://img.shields.io/badge/Scenarios-41-orange?style=flat&labelColor=555" alt="41 个场景" />
  <img src="https://img.shields.io/badge/Rounds-258-red?style=flat&labelColor=555" alt="258 个回合" />
  <img src="https://img.shields.io/badge/Staged%20Updates-72-yellow?style=flat&labelColor=555" alt="72 次分阶段更新" />
  <img src="https://img.shields.io/badge/Models-12-9cf?style=flat&labelColor=555" alt="12 个模型" />
  <img src="https://img.shields.io/badge/Scoring-Execution--based-success?style=flat&labelColor=555" alt="基于执行" />
</p>

<img src="../../assets/hero.png" alt="ClawArena-Team" width="900">

[🔭 概览](#-概览) • [📈 排行榜](#-排行榜) • [🔑 关键发现](#-关键发现) • [🚀 快速开始](#-快速开始) • [🧰 能力面与工具](#-能力面与工具) • [📊 数据与评估](#-数据与评估) • [🔍 案例研究](#-案例研究) • [📖 文档](#-文档) • [🏗️ 项目结构](#️-项目结构) • [📚 引用](#-引用) • [📄 许可证](#-许可证)

</div>

---

## 🔭 概览

语言模型智能体正越来越多地被部署为**管理者**——一个主模型创建专门的子智能体、分派工作,并通过动态工作流编排它们并行、异步的返回结果。现有基准要么评测某个策略自身的任务求解能力,要么评测一个固定的多智能体系统,但都没有单独刻画那个充当领导者的单一语言模型的**管理能力**。

**ClawArena-Team**(ClawArena 系列中的团队管理变体)正是要单独刻画这一点。一个**纯文本主智能体**必须完成它无法独立完成的多轮、多模态、多目录任务,方法是从一个**固定的、本地服务的池**中创建、赋权、调度并整合子智能体。每个管理者指挥的都是同一批工人,因此分数差异反映的是*管理技巧,而非原始能力*。

- **41 个场景 · 258 个评测回合 · 72 次分阶段更新**,涵盖**法律、医学、工程、商业与科学**。
- **纯文本、部分可见的主智能体**——它原生只能感知文本,且只能触及工作区的一部分,因此分派是强制性的。
- **固定的子智能体池**,通过 vLLM 在本地服务(`llm`/`vlm`/`omni`),在每个被评测的管理者之间保持完全一致。
- **基于执行的评分,无 LLM 裁判**——每个回合都附带一条 shell 命令,其退出码(可选配合输出匹配)决定通过/失败。

---

## 📈 排行榜

我们以综合**子智能体管理分数(SMS)** 对主智能体模型排名,该分数将任务正确率乘以一个最小权限与模态路由的管理因子:

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS 始终 ≤ TCR:** 管理只能折损任务正确率,绝不会抬高它。一个管理得完美却任务失败的模型得分为零。

| 模型 | TCR | TPP | ROC | WPP | MCA | **SMS** | 成本 ($) | 回合 |
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

<sub>所有数值均为百分比,十二个模型 × 41 个场景在单次评测运行中得出,按 **SMS** 排序。新发布的 `glm-5.2`(通过官方 z.ai API)是最强的开放权重管理者——SMS 50.4,总榜第 4——超越 `kimi-k2.6` 登顶开放权重模型。**加粗**标记每列的最优值(每列各自独立高亮)。成本 ($):每次运行的主智能体 API 成本,按提供方 / OpenRouter 标价计——越低越好,因此不加粗;子智能体运行在固定的本地池上,不计价。回合:在 258 个回合中通过的数量。`claude-fable-5` 按其出厂状态评测,采用厂商推荐的拒答 → `claude-opus-4-8` 回退。</sub>

> 📥 想提交结果?参见 [docs/submit-to-leaderboard.md](../../docs/submit-to-leaderboard.md)。示例运行与贡献结果存放于 [`submissions/`](../../submissions/)。

---

## 🔑 关键发现

在十二个专有、社区托管与自托管的主智能体模型上,浮现出三项发现。

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ 瓶颈在于*赋予权限*,而非感知

两条"容易"的轴几乎已饱和——每个有能力的模型都做到了只读合规(ROC ≥ 92%)与模态选择准确(MCA ≥ 92%)。真正具有区分度的是权限精度类指标:**工作区权限精度(WPP)对任何模型都*从未*达到 50%**。子智能体往往被授予了大约两倍于它们实际触及文件的访问权。

</td>
<td width="33%" valign="top">

### 2️⃣ 成本与管理质量*相互解耦*

主智能体 API 成本跨度**超过 100×**(每次运行 \$0.8 → \$93),而 SMS 跨度**不到 4×**。最便宜的开放模型坐落在帕累托前沿——`deepseek-v4-pro` 仅以 \$1.7 达到 SMS 46.4——而若干高成本模型(`gpt-5.5`、`sonnet-4-6`、`kimi-k2.6`)被中等成本的 `gemini-3.5-flash` *支配*。开放权重的 `glm-5.2`($22.9)同样落在前沿上,是最强的开放模型。

</td>
<td width="33%" valign="top">

### 3️⃣ 分数聚拢,行为发散

在旗舰之下,十个模型聚集在一个**9.9 分的 SMS 带**内(43.9–53.8),然而它们的编排行为相差**超过一个数量级**。在有能力的模型中,每子智能体的禁止访问率从 0.48 到 5.78 不等(约 12×),动态工作流的使用从 8 次到 112 次调用不等。

</td>
</tr>
</table>

<div align="center">

| 成本 vs. 管理(发现 2) | 权限违规(发现 3) |
|:---:|:---:|
| <img src="../../assets/pareto.png" alt="SMS 与主智能体 API 成本的对比,对数刻度;便宜的开放模型位于帕累托前沿" width="430"> | <img src="../../assets/forbidden.png" alt="各模型在对数刻度上的禁止访问计数 MAF/SAFt/SAFa;SAFa 发散约 12 倍" width="430"> |

</div>

**模态路由。** 管理者绝大多数默认使用 `llm` 键,创建的 `vlm`/`omni` 专家相对较少;当它们*确实*按模态路由时是正确的(因此 MCA 很高),但它们对多模态工人使用不足。

<div align="center">
<img src="../../assets/modality.png" alt="子智能体模型键分布:管理者默认使用 llm 键并对 vlm/omni 使用不足" width="780">
</div>

---

## 🚀 快速开始

完整演练(服务子智能体池、选择评测目标、续跑运行)见 [`docs/running-experiments.md`](../../docs/running-experiments.md)。

### 1. 安装

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

这会安装 `clawarena-team` CLI(短别名:**`cateam`** / **`ca-team`**)。分词器与对话模板**已打包在 `helper/` 中**——无需下载步骤。

### 2. 服务固定的子智能体池(本地 vLLM)

子智能体池在每个被评测的主智能体之间保持完全一致,因此管理是唯一变量:

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. 校验、运行与分析

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

> 短别名 `cateam` 与 `ca-team` 在任何地方都可与 `clawarena-team` 互换(例如 `cateam run ...`)。

<details>
<summary><b><code>--model</code> JSON</b></summary>

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

同一个字符串也可通过 `CATEAM_MODEL_JSON` 提供。`main.modalities` 字段决定主智能体原生能感知什么;`Read` 会将超出模态范围的文件降级为一个文本占位符并建议分派。所有标志位与 `CATEAM_*` 变量见 [`docs/cli.md`](../../docs/cli.md),数据集格式见 [`docs/dataset.md`](../../docs/dataset.md),接入某个提供方见 [`docs/provider.md`](../../docs/provider.md)。
</details>

---

## 🧰 能力面与工具

ClawArena-Team 将子智能体管理刻画为一个**委托—代理问题**。主智能体的能力面分解为六项具体操作,每一项都由场景设计强制触发:

| 操作 | 它要求什么 |
|---|---|
| **创建** | 用系统提示、模型键、工具子集与工作区路径白名单(其自身白名单的子集)创建一个子智能体。 |
| **模态路由** | 将图像/视频路由到 `vlm`、将音频路由到 `omni`,因为管理者只能感知文本。 |
| **最小权限赋权** | 仅授予子智能体实际需要的工具和路径;过度授予既浪费又不安全。 |
| **调度** | 以前台或后台、作为新会话或续接(恢复)会话、并行地运行子智能体;后台任务在完成时通知管理者。 |
| **动态工作流** | 在运行时基于同一个池编排多子智能体(并行 + 流水线阶段)。 |
| **整合** | 将子智能体的返回融合为一个正确的交付物——只有整合后的答案才被评分。 |

主智能体被暴露**首字母大写(CapitalCase)** 的工具,其名称、描述与参数都仿照真实 harness 约定,以便跨基准可比较:

| 工具 | 用途 |
|---|---|
| **Read** | 读取一个文件;超出模态范围的内容会降级为一个建议分派的文本占位符。 |
| **Write** | 在工作区中创建或覆写一个文件。 |
| **Edit** | 对一个已有文件施加定向的就地编辑。 |
| **Bash** | 在沙箱中运行一条 shell 命令(路径经 `realpath` 校验)。 |
| **Grep** | 按模式搜索文件内容。 |
| **Glob** | 按名称模式查找文件。 |
| **CreateSubagent** | 定义一个子智能体:系统提示、模型键、工具子集与工作区路径白名单。 |
| **RunSubagent** | 以前台或后台、作为新会话或续接(恢复)会话调用一个子智能体。 |
| **ListSubagents** | 列出迄今创建的子智能体及其状态。 |
| **InspectSubagent** | 检视一个子智能体的配置、被授予的权限与运行历史。 |
| **Workflow** | JS 风格的编排 DSL——`agent()`、`parallel()`、`pipeline()`——在运行时组合多子智能体运行。 |

系统级信号(环境、token 阈值)通过 `<system-reminder>` 块注入;后台任务完成通过 `<task-notification>` 块送达。所有路径访问都经 `realpath` 校验,符号链接逃逸会被拒绝并计为禁止访问。

### 固定的子智能体池(受控变量)

| 键 | 模型 | 服务器 | 原生模态 |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | local vLLM | text |
| `vlm`  | gemma-4-31b-it | local vLLM | text, image, video |
| `omni` | gemma-4-e4b-it | local vLLM | text, image, audio, video |

每个主智能体都指挥这同一支团队;在不同运行间只有主智能体在变化。

---

## 📊 数据与评估

每个场景提供一个工作区、一串用户问题以及真值检查。在某些回合之间,工作区会收到**分阶段更新**(新增或替换的文件),从而改变后续答案,要求对一个演变中的任务进行持续管理,而非一次性求解。

<div align="center">
<img src="../../assets/heatmap.png" alt="逐场景 SMS 热力图:12 个模型 x 41 个场景,难度参差且因模型而异" width="820">
<br/>
<sub>逐场景 × 模型的 SMS 热力图——难度参差且因模型而异。</sub>
</div>

**评分成分**(全部在 $[0,1]$ 内,无 LLM 裁判):

| 指标 | 含义 |
|---|---|
| **TCR** — 任务完成率 | 在用户问题上的平均通过率。 |
| **TPP** — 工具权限精度 | 对每个子智能体,被授予的工具类型中实际被使用的比例。 |
| **ROC** — 只读合规 | 对每个子智能体,若一个只读子智能体被授予了具变更性的工具则为 0,否则为 1。 |
| **WPP** — 工作区权限精度 | 对每个子智能体,被访问的文件数 ÷ 被授予的文件数。 |
| **MCA** — 模态选择准确率 | 对每个子智能体,`vlm` 是否实际读取图像/视频、`omni` 是否读取音频(`llm` 计 1)。 |

每个场景都满足**十条硬性设计约束(C1–C10)**——不可读区域、实质性的分阶段更新、完整的工具面使用、≥8 个带诱饵的目录、非文本模态回合、必须并行的任务、会话复用配对、跨回合依赖、模态诱饵,以及机器可校验的答案——每一条都瞄准一种单一语言模型本可绕过的特定管理失败模式。

### 数据集构成

- **41 个场景 · 258 个回合**,其中 44 个(17.1%)之前有分阶段更新。
- **72 个更新组、共 255 个文件**(61.1% 为 `new`,38.9% 为 `replace`,平均每组 3.54 个文件)。
- **170.5 MiB · 28.9 M tokens**——71.9% 为工作区内容,27.9% 为分阶段更新。
- 模态构成:文本在文件数/token 数上占主导,而音频与图像在原始字节上占主导——这是一份纯文本管理者无法直接消费的可观非文本负载。

ClawArena-Team 是**构建而成,而非采集而来**:工作区语料、多模态资产、真值与执行检查全部由同一批受版本控制的脚本程序化合成,经由一个**合成—验证飞轮**,其中一次真实的基线子智能体管理运行是最终的验收闸门。该基准实际上正是由它所度量的那项能力撰写而成的。格式与构建方法见 [`docs/dataset.md`](../../docs/dataset.md) 与论文附录。

如需更细粒度的分布,见 [`docs/data-stats/`](../../docs/data-stats/):每个子集(`demo` / `wave1` / `wave3` / `wave4`)以及全集都有各自的 `STATS.md` 及图表(token / 文件大小 / 模态分布、标签覆盖率……),由 `clawarena-team stats` 生成。

---

## 🔍 案例研究

直接取自录制的运行记录与 `metadata.json` 文件的十二个案例——所有数字与引用字符串均为原文照录——为三项发现与管理能力面提供具体支撑。

<details>
<summary><b>案例 1–4:最强管理者下的过度授予、正确的模态路由、模态诱饵陷阱,以及成本与质量的解耦</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_1.png" alt="案例研究 1-4" width="900">
</div>
</details>

<details>
<summary><b>案例 5–8:分数相同但禁止访问发散、撰写一个动态工作流(以及一个崩溃的扇出)、没有真正后台调度的逻辑并行,以及真正的后台加工作流并行</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_2.png" alt="案例研究 5-8" width="900">
</div>
</details>

<details>
<summary><b>案例 9–12:一个从未传播开来的待定修正、一处管理者无法驾驭的能力悬崖、管理上限(并行扇出、自适应重试、最小权限),以及优秀管理的样貌</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_3.png" alt="案例研究 9-12" width="900">
</div>
</details>

---

## 📖 文档

| 文档 | 说明 |
|----------|-------------|
| [CLI 参考](../../docs/cli.md) | 所有命令、标志位与 `CATEAM_*` 环境变量 |
| [数据集格式](../../docs/dataset.md) | 场景布局、回合、分阶段更新、真值检查 |
| [提供方指南](../../docs/provider.md) | 接入主智能体提供方(OpenAI-compat、Gemini、OpenRouter……) |
| [运行实验](../../docs/running-experiments.md) | 服务子智能体池并运行 / 续跑一次完整扫描 |
| [提交到排行榜](../../docs/submit-to-leaderboard.md) | 打包一次运行并将其贡献到 [`submissions/`](../../submissions/) |

---

## 🏗️ 项目结构

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

## 📚 引用

本工作目前为匿名预印本;arXiv 标识符与作者名单待补。

```bibtex
@misc{clawarena-team2026,
  title  = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author = {Anonymous Author(s)},
  year   = {2026},
  note   = {Preprint. arXiv identifier and author list to be added.}
}
```

---

## 📄 许可证

本项目采用 [MIT 许可证](../../../LICENSE)授权。
