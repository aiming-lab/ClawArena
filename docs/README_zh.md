<div align="center">

<img src="../assets/claweval.png" alt="ClawArena" width="500">

<br/>

## 在不断演化的信息环境中评测 AI 智能体。

<br/>

<img src="../assets/overview2-small.png" alt="ClawArena Overview" width="800">

<br/>

<br/>


<table>
  <tr>
    <td align="center" width="180" height="140">
      <a href="https://github.com/openclaw/openclaw">
        <img src="../assets/openclaw-logo.svg" alt="OpenClaw" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/anthropics/claude-code">
        <img src="https://claude.ai/favicon.ico" alt="Claude Code" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/aiming-lab/MetaClaw">
        <img src="../assets/metaclaw-logo.png" alt="MetaClaw" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/sipeed/picoclaw">
        <img src="../assets/picoclaw-logo.png" alt="PicoClaw" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <a href="https://github.com/HKUDS/nanobot">
        <img src="../assets/nanobot-logo.png" alt="Nanobot" height="70" />
      </a>
    </td>
    <td align="center" width="180" height="140">
      <b style="font-size:1.1em">+ 任意智能体</b>
    </td>
  </tr>
  <tr>
    <td align="center"><b>OpenClaw</b></td>
    <td align="center"><b>Claude Code</b></td>
    <td align="center"><b>MetaClaw</b></td>
    <td align="center"><b>PicoClaw</b></td>
    <td align="center"><b>Nanobot</b></td>
    <td align="center">通过 <a href="plugin.md">插件</a></td>
  </tr>
</table>

<br/>

<p>
  <a href="../README.md">English</a> |
  <b>中文</b> |
  <a href="README_ja.md">日本語</a> |
  <a href="README_ko.md">한국어</a> |
  <a href="README_es.md">Español</a> |
  <a href="README_fr.md">Français</a> |
  <a href="README_de.md">Deutsch</a>
</p>

<br/>

<p>
  <a href="https://arxiv.org/abs/2604.04202"><img src="https://img.shields.io/badge/arXiv-2604.04202-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="arXiv" /></a>
  <a href="https://www.clawarena.cc/"><img src="https://img.shields.io/badge/Website-clawarena.cc-4285F4?style=flat&logo=googlechrome&logoColor=white" alt="Website" /></a>
  <a href="https://github.com/aiming-lab/ClawArena"><img src="https://img.shields.io/badge/GitHub-ClawArena-181717?style=flat&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="License MIT"></a>
  <a href="https://github.com/aiming-lab/ClawArena/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat" alt="PRs welcome" /></a>
</p>
<p>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Scenarios-12-orange?style=flat&labelColor=555" alt="12 Scenarios" />
  <img src="https://img.shields.io/badge/Rounds-337-red?style=flat&labelColor=555" alt="337 Rounds" />
  <img src="https://img.shields.io/badge/Dynamic%20Updates-45-yellow?style=flat&labelColor=555" alt="45 Dynamic Updates" />
  <img src="https://img.shields.io/badge/Frameworks-5-blueviolet?style=flat&labelColor=555" alt="5 Frameworks" />
</p>

[🔭 概览](#-概览) • [📈 排行榜](#-排行榜) • [🆚 Benchmark 对比](#-benchmark-对比) • [🚀 快速开始](#-快速开始) • [🤖 支持的框架](#-支持的框架) • [📊 数据与评测](#-数据与评测) • [🔍 案例研究](#-案例研究) • [📖 文档](#-文档) • [🏗️ 项目结构](#-项目结构) • [🙏 相关项目](#-相关项目) • [📚 引用](#-引用) • [📄 许可证](#-许可证)

</div>

---

## 🔭 概览

**ClawArena** 是一个面向 AI 编码智能体的基准评测平台。它提供统一的流水线，用于在同一组真实的多会话场景上执行推理、对结果评分，并比较不同智能体框架的表现。

- **12 个多轮场景** — 覆盖零售分析、金融、医疗、信息安全、人力资源、教育、科研诚信等多种专业语境
- **337 个评测轮次** — 混合 `multi_choice` 推理（95 轮）与 `exec_check` 执行验证（242 轮）
- **45 次动态更新** — 在评测中途注入新文件与新会话，用以考察信念修正与矛盾处理能力
- **多会话上下文** — 智能体需在每个场景内对工作区文件以及多渠道聊天历史（IM、邮件等）进行推理
- **框架无关** — 论文中评测了五种框架（OpenClaw、Claude Code、NanoBot、PicoClaw、MetaClaw）；可通过[插件系统](plugin.md)添加新框架
- **集成 [MetaClaw](https://github.com/aiming-lab/MetaClaw)** — 评测在记忆、技能与强化学习增强之下的智能体

<div align="center">
<img src="../assets/overview.png" alt="ClawArena Cross-Domain Data Sample Gallery" width="900">
</div>

---

## 📈 排行榜

我们使用 **综合可靠性得分（Composite Reliability Score, CRS）** 对智能体进行排序，该指标对原始正确率与行为一致性赋予同等权重：

- **TCR**（任务完成率，Task Completion Rate）= $S/N$ — 所有轮次的平均正确率，可分解为 MC 与 EC 子分。
- **SC**（成功内聚度，Success Cohesion）= $(S - k)/(N - 1)$ — 衡量正确轮次集中为长连续段的程度；单一连胜时 SC = 1，通过/失败交替时 SC = 0。
- **FD**（失败分散度，Failure Dispersion）= $1 - (S_f - k_f)/(N - 1)$ — 对长失败连段进行惩罚。
- **鲁棒性（Robustness）** = SC × FD — 采用乘法形式，使任一维度的崩溃都会拉低得分。
- **CRS** = (TCR + Robustness) / 2。

_所有数值均在 12 个场景 / 337 轮次上做宏平均，并按 CRS 排序。_

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

<sub>每个模型在其主要承载框架下展示：Anthropic 模型通过 Claude Code 运行（与 OpenClaw 不兼容），其余模型均在 OpenClaw 下展示。固定模型而切换框架的跨框架对比详见论文。</sub>

---

## 🆚 Benchmark 对比

ClawArena 与其他 harness-native 智能体 benchmark 的差异。已有工作至多覆盖四个设计维度中的两个；ClawArena 是唯一同时满足全部四个维度，并跨五种框架报告结果的 benchmark。

列标记 — ✅ 支持 · ❌ 不支持 · 🟡 部分支持（机制存在但被削弱，例如第三方消息仅以普通文件暴露而非按渠道标签化的会话，或偏好以静态人设编码而非通过静默回合学习得到）：

- **MSC**（Multi-Source Conflict，多源冲突）：智能体必须分析按渠道区分的"用户—第三方"对话。
- **DU**（Dynamic Update，动态更新）：环境在用户回合之间被覆盖（单次循环内工具返回值的变化不计入）。
- **MU**（Multi-User turn，多用户回合）：用户在多个回合中以新查询再次介入。
- **Pref.**（Implicit personalization，隐式个性化）：用户偏好在静默考查回合中得到应用。
- **Frmw.**：被评测的智能体框架数量。

| Benchmark | 任务来源 | 执行方式 | MSC | DU | MU | Pref. | 验证方式 | Frmw. | 规模（题量 / 场景） |
|---|---|---|:---:|:---:|:---:|:---:|---|:---:|---|
| [ClawBench](https://github.com/reacher-z/ClawBench)         | 人工题库            | 真实网页          | ❌ | ❌ | ❌ | ❌ | 规则+LLM  | 8 | 283 / 144 站点 |
| [Claw-Eval](https://github.com/claw-eval/claw-eval)         | 上游数据筛选        | 沙箱 + Mock       | ❌ | ❌ | ✅ | ❌ | 规则+LLM  | 1 | 300 / 9 类 |
| [Claw-Eval-Live](https://github.com/Claw-Eval-Live/Claw-Eval-Live)    | 实时信号（季度更新）| Mock 服务         | ❌ | ❌ | ❌ | ❌ | 规则+LLM  | 1 | 105 / 17 族 |
| [ClawMark](https://github.com/evolvent-ai/ClawMark)          | 人工 + AI 合成      | 沙箱化服务        | ✅ | ✅ | ✅ | ❌ | 纯规则    | 1 | 100 / 13 场景 |
| [ClawsBench](https://github.com/benchflow-ai/ClawsBench)        | 专家设计            | Mock 服务         | ✅ | ❌ | ❌ | ❌ | 纯规则    | 4 | 44 / 5 服务 |
| [MetaClaw-Bench](https://github.com/aiming-lab/MetaClaw)     | 合成                | 工作区仿真        | 🟡 | ✅ | ✅ | 🟡 | 纯规则    | 1 | 346 / 30 天 |
| [PinchBench](https://github.com/pinchbench/skill)        | 人工（真实世界）    | 真实（OpenClaw）  | ❌ | ❌ | ❌ | ❌ | 规则+LLM  | 1 | 23 / 8 类 |
| [QwenClawBench](https://huggingface.co/datasets/skylenage-ai/QwenClawBench)     | 经验性（声称）      | 真实（Docker）    | ❌ | ❌ | ❌ | 🟡 | 规则+LLM  | 1 | 100 / 8 领域 |
| [WildClawBench](https://github.com/InternLM/WildClawBench)     | 人工（野外采集）    | 真实（OpenClaw）  | ✅ | ❌ | ❌ | 🟡 | 规则+LLM  | 1 | 60 / 6 类 |
| [ZClawBench](https://huggingface.co/datasets/zai-org/ZClawBench)        | 人工 + 合成         | 真实 + 部分 Mock  | ❌ | ❌ | ❌ | ❌ | 规则+LLM  | 1 | 116 / 6 类 |
| **ClawArena（本文）** | **经验性合成**  | **多渠道仿真**    | ✅ | ✅ | ✅ | ✅ | 纯规则    | **5** | **337 / 12 场景** |

---

## 🚀 快速开始

### 1. 一键安装

```bash
bash scripts/setup.sh
```

该命令会一并安装 ClawArena（含开发依赖）、MetaClaw，以及框架 CLI（OpenClaw、Claude Code、Nanobot、PicoClaw）和 Claude Code Router。手动安装请参考[安装指南](installation.md)。

### 2. 运行基准测试

首先参考 [`scripts/env_example.sh`](../scripts/env_example.sh) 配置环境变量，然后运行：

```bash
python scripts/test_run.py
```

编辑 `scripts/test_run.py` 即可配置框架、并发度、超时与输出路径。

<details>
<summary><b>或直接使用 CLI</b></summary>

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

完整命令与参数详见 [CLI 参考文档](cli.md)。
</details>

<details>
<summary><b>开发与测试</b></summary>

```bash
pip install -e ".[dev]"
pytest
```

</details>

---

## 🤖 支持的框架

| 框架 | 类型 | 语言 | 说明 |
|-----------|------|----------|-------|
| [OpenClaw](https://github.com/openclaw/openclaw) | CLI 智能体 | Node.js | — |
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | LLM 代理层 | Python | 仅在 [OpenClaw](https://github.com/openclaw/openclaw) 与 [Nanobot](https://github.com/HKUDS/nanobot) 中受支持 |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) | CLI 智能体 | Node.js | 借助 [Claude Code Router](https://github.com/musistudio/claude-code-router) |
| [PicoClaw](https://github.com/sipeed/picoclaw) | CLI 智能体 | Go | — |
| [Nanobot](https://github.com/HKUDS/nanobot) | CLI 智能体 | Python | — |

新框架可通过插件系统接入，无需修改核心代码 — 只需提供一个注册适配器的 `.py` 文件并在运行时加载：

```bash
clawarena infer --data tests.json --framework my_agent --out results/ --plugin my_agent.py
```

适配器接口与引擎轮次钩子的细节参见[插件指南](plugin.md)。

[MetaClaw](https://github.com/aiming-lab/MetaClaw) 以透明代理层的形式集成，用于评测在记忆、技能与强化学习增强之下的智能体。在 `tests.json` 中添加 `metaclaw` 字段即可启用；当前支持的承载框架为 **OpenClaw** 与 **Nanobot**。托管/非托管模式、触发器配置与 YAML 模板详见 [MetaClaw 指南](metaclaw-guide.md)。

> **⚠️ 计费与政策提示（2026 年 4 月 4 日）：**
OpenClaw 等第三方工具/智能体可能不再被允许使用您的 Claude Free/Pro/Max 个人订阅凭据中转流量。ClawArena 中所有通过 Claude.ai OAuth 登录接入的 Claude 集成 **必须改用通过 Claude Console 或受支持的云厂商签发的官方 API Key 进行鉴权**。此类第三方接入将仅消耗您的 **付费追加额度**，而不会占用订阅配额。完整政策详情请参见 [Anthropic 法律与合规说明](https://code.claude.com/docs/en/legal-and-compliance)。

---

## 📊 数据与评测

每个场景包含：

- **工作区文件** — 智能体可读取的文档、电子表格与代码
- **会话历史** — 多渠道聊天记录（IM、邮件、Slack 等）
- **评测题目** — `multi_choice`（推理）与 `exec_check`（执行验证）
- **动态更新** — 在轮次之间注入的新会话与新文件

337 个轮次包含两种题型：

| 类型 | 轮次 | 测试 | 方式 |
|------|------:|-------|-----|
| `multi_choice` | 95 (28.2%) | 智能体的推理与理解 | 从回复中提取 `\bbox{A,B,...}`，与标准答案计算 IoU/F1 |
| `exec_check`   | 242 (71.8%) | 智能体的动作与文件输出 | 运行 shell 命令以验证退出码与 stdout |

<details>
<summary><b>数据构建流水线（点击展开）</b></summary>
<br/>
<div align="center">
<img src="../assets/pipeline_v2.png" alt="ClawArena Construction Pipeline" width="700">
</div>

构建全部 12 个场景所用的完整六层规范体系详见[数据规范](data-spec/)。
</details>

我们已开源完整的数据构建规范 — 包括六层场景设计、合成准则与陷阱文档 — 见 [`docs/data-spec/`](data-spec/)。

完整格式说明详见[数据结构](data-structure.md)。

---

## 🔍 案例研究

从 ClawArena 的 12 个场景中精选的十个分选项案例研究，覆盖 MS-R、DU-R、P-R 与 `exec_check` 等交互类别，跨安全、临床、人力资源与电商领域。

<details>
<summary><b>案例 1–2：NexaFlow API 泄露 (MS-R) 与模式合规失败 (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_01_02.png" alt="Case 1-2" width="900">
</div>
</details>

<details>
<summary><b>案例 3–4：科研诚信复合选项 (MS-R) 与权威影响下的修订 (DU-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_03_04.png" alt="Case 3-4" width="900">
</div>
</details>

<details>
<summary><b>案例 5–6：违规解雇文件名前缀 (P-R + exec_check) 与 GDPR 结构化输出上限 (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_05_06.png" alt="Case 5-6" width="900">
</div>
</details>

<details>
<summary><b>案例 7–8：618 GPU 欺诈更新特定型失败 (DU-R) 与 JSON 模式遵循 (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_07_08.png" alt="Case 7-8" width="900">
</div>
</details>

<details>
<summary><b>案例 9–10：违规解雇合取式综合 (MS-R + DU-R) 与流水线作者归属最终综合 (exec_check + MS-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_09_10.png" alt="Case 9-10" width="900">
</div>
</details>

---

## 📖 文档

| 文档 | 说明 |
|----------|-------------|
| [安装指南](installation.md) | ClawArena、各框架与 MetaClaw 的安装指引 |
| [CLI 参考](cli.md) | 全部命令、参数与环境变量 |
| [数据结构](data-structure.md) | 数据集格式、题型与清单结构 |
| [Provider 指南](provider-usage-guide.md) | LLM Provider 配置与优先级链 |
| [MetaClaw 指南](metaclaw-guide.md) | MetaClaw 集成模式与触发钩子 |
| [插件指南](plugin.md) | 编写并注册外部框架适配器 |

---

## 🏗️ 项目结构

```
ClawArena
├── src/clawarena/
│   ├── cli.py           # CLI 入口
│   ├── core/            # 流水线：infer、score、report、compare、check、run、clean
│   ├── stats/           # Token 与结构化分析，按框架布局
│   ├── engines/         # 智能体执行引擎（按框架）
│   ├── data_handlers/   # 数据加载、校验与工作副本管理
│   ├── adapters/        # 框架适配器组合与注册表
│   ├── qtypes/          # 题型：multi_choice、exec_check
│   ├── metaclaw/        # MetaClaw 代理生命周期与触发钩子
│   └── plugins/         # 外部适配器加载（--plugin）
├── data/clawarena/      # 数据集（12 个场景，337 轮次）
├── docs/                # 文档，含 docs/data-spec/（六层构建规范）
├── scripts/             # 安装、测试运行器、对比工具
├── helpers/             # 框架专属辅助钩子
└── tests/               # 测试套件（356 个测试）
```

---

## 🙏 相关项目

ClawArena 在以下开源智能体框架之上构建并对其进行评测：

- [OpenClaw](https://github.com/openclaw/openclaw) — 主要被评测的 CLI 智能体。
- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — 元学习代理层，以记忆、技能与强化学习增强智能体。
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropic 的智能体式编码工具。
- [Claude Code Router](https://github.com/musistudio/claude-code-router) — 将 Claude Code 请求路由到不同模型。
- [PicoClaw](https://github.com/sipeed/picoclaw) — 基于 Go 的轻量级 CLI 智能体。
- [Nanobot](https://github.com/HKUDS/nanobot) — 原生 Python 实现、支持 Anthropic API 的 CLI 智能体。

---

## 📚 引用

```bibtex
@article{ji2026clawarena,
  title={ClawArena: A Multi-Framework Benchmark for Evaluating AI Coding Agents on Realistic Multi-Session Scenarios},
  author={Ji, Haonian and Xiong, Kaiwen and Han, Siwei and Xia, Peng and Qiu, Shi and Zhou, Yiyang and Liu, Jiaqi and Li, Jinlong and Li, Bingzhou and Zheng, Zeyu and Xie, Cihang and Yao, Huaxiu},
  journal={arXiv preprint arXiv:2604.04202},
  year={2026}
}
```

---

## 📄 许可证

本项目基于 [MIT 许可证](../LICENSE) 发布。
