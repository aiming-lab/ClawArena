<div align="center">

<h1>ClawArena-Team</h1>

### 評測語言模型代理中的子代理編排與動態工作流程

<p>
  <a href="../../README.md">English</a> •
  <a href="README.zh-Hans.md">简体中文</a> •
  <b>繁體中文</b> •
  <a href="README.ja.md">日本語</a> •
  <a href="README.ko.md">한국어</a> •
  <a href="README.fr.md">Français</a> •
  <a href="README.de.md">Deutsch</a> •
  <a href="README.es.md">Español</a> •
  <a href="README.pt.md">Português</a> •
  <a href="README.ru.md">Русский</a>
</p>

<p>
  <a href="#-引用"><img src="https://img.shields.io/badge/Paper-Preprint-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="論文" /></a>
  <a href="../../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="MIT 授權" /></a>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Version-v1.0.0-blueviolet?style=flat&labelColor=555" alt="v1.0.0" />
</p>
<p>
  <img src="https://img.shields.io/badge/Scenarios-41-orange?style=flat&labelColor=555" alt="41 個情境" />
  <img src="https://img.shields.io/badge/Rounds-258-red?style=flat&labelColor=555" alt="258 回合" />
  <img src="https://img.shields.io/badge/Staged%20Updates-72-yellow?style=flat&labelColor=555" alt="72 次分階段更新" />
  <img src="https://img.shields.io/badge/Models-12-9cf?style=flat&labelColor=555" alt="12 個模型" />
  <img src="https://img.shields.io/badge/Scoring-Execution--based-success?style=flat&labelColor=555" alt="基於執行" />
</p>

<img src="../../assets/hero.png" alt="ClawArena-Team" width="900">

[🔭 概覽](#-概覽) • [📈 排行榜](#-排行榜) • [🔑 主要發現](#-主要發現) • [🚀 快速開始](#-快速開始) • [🧰 能力面向與工具](#-能力面向與工具) • [📊 資料與評測](#-資料與評測) • [🔍 案例研究](#-案例研究) • [📖 文件](#-文件) • [🏗️ 專案結構](#️-專案結構) • [📚 引用](#-引用) • [📄 授權](#-授權)

</div>

---

## 🔭 概覽

LM 代理正越來越多地被部署為 **管理者**——一個主模型建立專門的子代理、委派工作，並透過動態工作流程編排它們平行、非同步的回傳。既有的基準衡量的是某個策略自身的任務求解，或一個固定的多代理系統，卻沒有任何一個能單獨隔離出擔任領導者的單一 LM 的 **管理能力**。

**ClawArena-Team**（ClawArena 系列中的團隊管理變體）正是單獨隔離出這一點。一個 **純文字主代理** 必須透過從 **固定、本地提供服務的集區** 中建立、賦能、排程並整合子代理，來完成它無法獨力完成的多輪、多模態、多目錄任務。每個管理者都指揮同一批工作者，因此分數差異反映的是 *管理技巧，而非原始能力*。

- **41 個情境 · 258 個評測回合 · 72 次分階段更新**，橫跨 **法律、醫學、工程、商業與科學**。
- **純文字、部分可見的主代理**——它原生只能感知文字，且只能觸及工作區的一部分，因此委派是必須的。
- **固定子代理集區** 透過 vLLM 在本地提供服務（`llm`/`vlm`/`omni`），在每個受評測的管理者之間保持完全相同。
- **基於執行的計分，無 LLM 評審**——每個回合都附帶一個 shell 指令，由其退出碼（搭配可選的輸出比對）決定通過／失敗。

---

## 📈 排行榜

我們依綜合性的 **子代理管理分數（Subagent-Management Score, SMS）** 為主代理模型排名，該分數將任務正確性乘上一個最小權限與模態路由的管理因子：

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS ≤ TCR 恆成立：** 管理只能折減任務正確性，永遠無法將其灌大。一個管理得完美卻在任務上失敗的模型，得分為零。

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

<sub>所有數值皆以 % 表示，為十二個模型 × 41 個情境於單一評測執行中的結果，依 **SMS** 排序。新發布的 `glm-5.2`（透過官方 z.ai API）是最強的開放權重管理者——SMS 50.4，總排名第 4——超越 `kimi-k2.6` 登上開放權重模型之首。**粗體** 標示該欄的最佳值（每一欄各自獨立標示最佳值）。成本 ($)：以供應商／OpenRouter 牌價計算的每次執行主代理 API 成本——越低越好，故不以粗體標示；子代理在固定的本地集區上執行，不計價。回合：通過的回合數（共 258）。`claude-fable-5` 以出貨版本評測，並採用廠商建議的拒答 → `claude-opus-4-8` 回退機制。</sub>

> 📥 想提交結果？請見 [docs/submit-to-leaderboard.md](../../docs/submit-to-leaderboard.md)。範例執行與社群貢獻的結果存放於 [`submissions/`](../../submissions/)。

---

## 🔑 主要發現

橫跨十二個專有、社群託管與自行託管的主代理模型，浮現出三項發現。

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ 瓶頸在於 *權限授予*，而非感知

兩個「容易」的面向幾乎已達飽和——對每個具備能力的模型而言，唯讀遵從度（ROC ≥ 92%）與模態選擇準確率（MCA ≥ 92%）皆然。具區辨力的面向是權限精確度指標：**工作區權限精確度（WPP）對任何模型都 *從未* 達到 50%**。子代理被授予的檔案，往往大約是其實際存取數量的兩倍。

</td>
<td width="33%" valign="top">

### 2️⃣ 成本與管理品質彼此 *脫鉤*

主代理 API 成本跨距 **超過 100×**（每次執行 \$0.8 → \$93），而 SMS 跨距 **不到 4×**。最便宜的開放模型位於柏拉圖前緣（Pareto frontier）——`deepseek-v4-pro` 僅以 \$1.7 即達到 SMS 46.4——而數個高成本模型（`gpt-5.5`、`sonnet-4-6`、`kimi-k2.6`）卻被中等成本的 `gemini-3.5-flash` *支配*。開放權重的 `glm-5.2`（$22.9）也落在前緣上，是最強的開放模型。

</td>
<td width="33%" valign="top">

### 3️⃣ 分數聚攏，行為分歧

在旗艦之下，十個模型聚攏在 **9.9 分的 SMS 區間**（43.9–53.8）內，但其編排行為的差異卻 **超過一個數量級**。在具備能力的模型之間，每個子代理的禁止存取率介於 0.48 至 5.78（約 12×），而動態工作流程的使用量介於 8 至 112 次呼叫。

</td>
</tr>
</table>

<div align="center">

| 成本 vs. 管理（發現 2） | 權限違規（發現 3） |
|:---:|:---:|
| <img src="../../assets/pareto.png" alt="SMS 與主代理 API 成本對比，對數刻度；便宜的開放模型位於柏拉圖前緣" width="430"> | <img src="../../assets/forbidden.png" alt="各模型的禁止存取次數 MAF/SAFt/SAFa（對數刻度）；SAFa 分歧約 12×" width="430"> |

</div>

**模態路由。** 管理者絕大多數預設使用 `llm` 鍵，相對而言很少建立 `vlm`/`omni` 專家；當它們 *確實* 依模態進行路由時都做得正確（因此 MCA 很高），但它們未充分運用多模態工作者。

<div align="center">
<img src="../../assets/modality.png" alt="子代理模型鍵分布：管理者預設使用 llm 鍵，且未充分運用 vlm/omni" width="780">
</div>

---

## 🚀 快速開始

完整逐步說明（提供集區服務、挑選目標、續跑執行）請見 [`docs/running-experiments.md`](../../docs/running-experiments.md)。

### 1. 安裝

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

這會安裝 `clawarena-team` CLI（簡短別名：**`cateam`** / **`ca-team`**）。分詞器與對話樣板已 **內建於 `helper/`**——無需下載步驟。

### 2. 提供固定子代理集區服務（本地 vLLM）

子代理集區在每個受評測的主代理之間保持完全相同，因此管理是唯一的變項：

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. 驗證、執行與分析

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

> 簡短別名 `cateam` 與 `ca-team` 在任何地方都可與 `clawarena-team` 互換使用（例如 `cateam run ...`）。

<details>
<summary><b><code>--model</code> JSON 設定</b></summary>

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

同一字串也可透過 `CATEAM_MODEL_JSON` 提供。`main.modalities` 欄位決定主代理原生能感知的內容；`Read` 會將模態之外的檔案降級為文字佔位符並建議委派。所有旗標與 `CATEAM_*` 變數請見 [`docs/cli.md`](../../docs/cli.md)，資料集格式請見 [`docs/dataset.md`](../../docs/dataset.md)，串接供應商請見 [`docs/provider.md`](../../docs/provider.md)。
</details>

---

## 🧰 能力面向與工具

ClawArena-Team 將子代理管理形塑為 **委託—代理問題（principal–agent problem）**。主代理的能力面向可分解為六項具體操作，每一項都由情境設計所強制要求：

| 操作 | 所需條件 |
|---|---|
| **建立** | 以系統提示、模型鍵、工具子集，以及工作區路徑白名單（為其自身的子集）建立一個子代理。 |
| **模態路由** | 由於管理者只能感知文字，須將影像/影片路由至 `vlm`，音訊路由至 `omni`。 |
| **最小權限賦能** | 只授予子代理實際需要的工具與路徑；過度授予既浪費又不安全。 |
| **排程** | 以前景或背景、以新建或續接（恢復）的工作階段，並可平行執行子代理；背景任務完成時會通知管理者。 |
| **動態工作流程** | 在執行期針對同一集區編寫多子代理編排（平行 + 管線階段）。 |
| **整合** | 將子代理的回傳融合為正確的交付成果——只有整合後的答案會被計分。 |

主代理會接觸到 **首字母大寫（CapitalCase）** 的工具，其名稱、描述與參數比照真實 harness 慣例，以利跨基準比較：

| 工具 | 用途 |
|---|---|
| **Read** | 讀取檔案；模態之外的內容會降級為建議委派的文字佔位符。 |
| **Write** | 在工作區建立或覆寫檔案。 |
| **Edit** | 對既有檔案套用就地的針對性編輯。 |
| **Bash** | 在沙箱中執行 shell 指令（路徑經 `realpath` 檢查）。 |
| **Grep** | 依模式搜尋檔案內容。 |
| **Glob** | 依名稱模式尋找檔案。 |
| **CreateSubagent** | 定義子代理：系統提示、模型鍵、工具子集，以及工作區路徑白名單。 |
| **RunSubagent** | 以前景或背景、以新建或續接（恢復）的工作階段呼叫子代理。 |
| **ListSubagents** | 列出目前已建立的子代理及其狀態。 |
| **InspectSubagent** | 檢視子代理的設定、已授予權限與執行歷史。 |
| **Workflow** | JS 風格的編排 DSL——`agent()`、`parallel()`、`pipeline()`——可於執行期組合多子代理執行。 |

系統層級的訊號（環境、token 門檻）會透過 `<system-reminder>` 區塊注入；背景任務的完成則透過 `<task-notification>` 區塊送達。所有路徑存取皆經 `realpath` 檢查，符號連結逃逸會被拒絕並計為禁止存取。

### 固定子代理集區（受控變項）

| 鍵 | 模型 | 伺服器 | 原生模態 |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | 本地 vLLM | 文字 |
| `vlm`  | gemma-4-31b-it | 本地 vLLM | 文字、影像、影片 |
| `omni` | gemma-4-e4b-it | 本地 vLLM | 文字、影像、音訊、影片 |

每個主代理都指揮這支相同的團隊；各次執行之間只有主代理會變動。

---

## 📊 資料與評測

每個情境都提供一個工作區、一連串使用者問題，以及真值（ground-truth）檢查。在某些回合之間，工作區會收到 **分階段更新**（新增或替換的檔案），改變後續的答案，要求對不斷演進的任務進行持續管理，而非一次性的解法。

<div align="center">
<img src="../../assets/heatmap.png" alt="各情境 SMS 熱圖：12 個模型 x 41 個情境，難度不均且因模型而異" width="820">
<br/>
<sub>各情境 × 模型 SMS 熱圖——難度不均且因模型而異。</sub>
</div>

**計分組成**（皆落於 $[0,1]$，無 LLM 評審）：

| 指標 | 意義 |
|---|---|
| **TCR** — 任務完成率 | 在使用者問題上的平均通過率。 |
| **TPP** — 工具權限精確度 | 就每個子代理而言，實際使用的已授予工具類型所佔比例。 |
| **ROC** — 唯讀遵從度 | 就每個子代理而言，若唯讀子代理被授予具變更性的工具則為 0，否則為 1。 |
| **WPP** — 工作區權限精確度 | 就每個子代理而言，存取的檔案數 ÷ 授予的檔案數。 |
| **MCA** — 模態選擇準確率 | 就每個子代理而言，`vlm` 是否確實讀取影像/影片、`omni` 是否確實讀取音訊（`llm` 計為 1）。 |

每個情境都滿足 **十項嚴格的設計約束（C1–C10）**——不可讀區域、實質的分階段更新、完整工具面向的使用、≥8 個含誘餌的目錄、非文字模態回合、必須平行的任務、工作階段重用配對、跨回合相依、模態誘餌，以及機器可檢查的答案——每一項都針對某個單一 LM 原本可能繞過的特定管理失敗模式。

### 資料集組成

- **41 個情境 · 258 回合**，其中 44 個（17.1%）之前有分階段更新。
- **72 個更新群組，涵蓋 255 個檔案**（61.1% 為 `new`，38.9% 為 `replace`，平均每群組 3.54 個檔案）。
- **170.5 MiB · 28.9 M tokens**——71.9% 為工作區內容，27.9% 為分階段更新。
- 模態組合：文字在檔案/token 上佔主導，而音訊與影像在原始位元組上佔主導——這是一份純文字管理者無法直接消化的可觀非文字載荷。

ClawArena-Team 是 **建構而成，而非蒐集而來**：工作區語料、多模態資產、真值與執行檢查，全都透過 **合成—驗證飛輪** 由同一套受版本控管的腳本程序化合成，其中一次真實的基準子代理管理執行是最終的驗收關卡。實際上，這個基準是由它所衡量的那項能力本身所撰寫。格式與建構方法論請見 [`docs/dataset.md`](../../docs/dataset.md) 與論文附錄。

更細緻的分布請見 [`docs/data-stats/`](../../docs/data-stats/)：每個子集（`demo` / `wave1` / `wave3` / `wave4`）與完整集合都各有自己的 `STATS.md` 以及圖表（token / 檔案大小 / 模態分布、標籤涵蓋率……），由 `clawarena-team stats` 生成。

---

## 🔍 案例研究

十二個案例直接取自記錄下的執行逐字稿與 `metadata.json` 檔案——所有數字與引述字串皆為原文照錄——具體佐證這三項發現與管理能力面向。

<details>
<summary><b>案例 1–4：最強管理者下的過度授予、正確的模態路由、模態誘餌陷阱，以及成本與品質脫鉤</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_1.png" alt="案例研究 1-4" width="900">
</div>
</details>

<details>
<summary><b>案例 5–8：分數相同但禁止存取分歧、編寫動態工作流程（以及一個崩潰的扇出）、沒有真正背景排程的邏輯平行，以及真正的背景加上工作流程平行</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_2.png" alt="案例研究 5-8" width="900">
</div>
</details>

<details>
<summary><b>案例 9–12：一個從未傳播出去的待處理修正、管理者無法操作的能力斷崖、管理上限（平行扇出、自適應重試、最小權限），以及優良管理應有的樣貌</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_3.png" alt="案例研究 9-12" width="900">
</div>
</details>

---

## 📖 文件

| 文件 | 說明 |
|----------|-------------|
| [CLI 參考](../../docs/cli.md) | 所有指令、旗標與 `CATEAM_*` 環境變數 |
| [資料集格式](../../docs/dataset.md) | 情境布局、回合、分階段更新、真值檢查 |
| [供應商指南](../../docs/provider.md) | 串接主代理供應商（OpenAI 相容、Gemini、OpenRouter……） |
| [執行實驗](../../docs/running-experiments.md) | 提供子代理集區服務並執行／續跑完整掃描 |
| [提交至排行榜](../../docs/submit-to-leaderboard.md) | 封裝一次執行並貢獻至 [`submissions/`](../../submissions/) |

---

## 🏗️ 專案結構

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

本研究目前為匿名預印本；arXiv 識別碼與作者名單待補。

```bibtex
@misc{clawarena-team2026,
  title  = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author = {Anonymous Author(s)},
  year   = {2026},
  note   = {Preprint. arXiv identifier and author list to be added.}
}
```

---

## 📄 授權

本專案採用 [MIT 授權](../../../LICENSE)。
