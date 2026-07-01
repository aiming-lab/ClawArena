<div align="center">

<h1>ClawArena-Team</h1>

### 言語モデルエージェントにおけるサブエージェントのオーケストレーションと動的ワークフローのベンチマーク

<p>
  <a href="../../README.md">English</a> •
  <a href="README.zh-Hans.md">简体中文</a> •
  <a href="README.zh-Hant.md">繁體中文</a> •
  <b>日本語</b> •
  <a href="README.ko.md">한국어</a> •
  <a href="README.fr.md">Français</a> •
  <a href="README.de.md">Deutsch</a> •
  <a href="README.es.md">Español</a> •
  <a href="README.pt.md">Português</a> •
  <a href="README.ru.md">Русский</a>
</p>

<p>
  <a href="#-引用"><img src="https://img.shields.io/badge/Paper-Preprint-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="Paper" /></a>
  <a href="../../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="License MIT" /></a>
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

<img src="../../assets/hero.png" alt="ClawArena-Team" width="900">

[🔭 概要](#-概要) • [📈 リーダーボード](#-リーダーボード) • [🔑 主要な発見](#-主要な発見) • [🚀 クイックスタート](#-クイックスタート) • [🧰 機能サーフェスとツール](#-機能サーフェスとツール) • [📊 データと評価](#-データと評価) • [🔍 ケーススタディ](#-ケーススタディ) • [📖 ドキュメント](#-ドキュメント) • [🏗️ プロジェクト構成](#-プロジェクト構成) • [📚 引用](#-引用) • [📄 ライセンス](#-ライセンス)

</div>

---

## 🔭 概要

言語モデルエージェントは、ますます **マネージャー** として運用されるようになっています。1 つのメインモデルが専門的なサブエージェントを作成し、作業を委譲し、それらの並列・非同期な返答を動的ワークフローを通じてオーケストレーションします。既存のベンチマークは、ポリシー自身のタスク解決能力や固定的なマルチエージェントシステムを評価しますが、リーダーとして振る舞う単一の言語モデルの **管理能力** を切り分けて評価するものはありません。

**ClawArena-Team**（ClawArena シリーズにおけるチーム管理バリアント）は、まさにこれを切り分けます。**テキストのみのメインエージェント** は、単独では実行できないマルチターン・マルチモーダル・マルチディレクトリのタスクを、**固定されローカルで提供されるプール** からサブエージェントを作成・権限付与・スケジューリング・統合することで完了しなければなりません。すべてのマネージャーが同じワーカーを指揮するため、スコアの差は *素の能力ではなく管理スキル* を反映します。

- **41 シナリオ・258 評価ラウンド・72 段階的更新** にわたり、**法律・医療・工学・ビジネス・科学** を網羅します。
- **テキストのみ・部分可視のメインエージェント** — ネイティブにはテキストのみを知覚し、ワークスペースの一部にしか到達できないため、委譲が必須となります。
- **固定されたサブエージェントプール** は vLLM 経由でローカルに提供され（`llm`/`vlm`/`omni`）、評価されるすべてのマネージャー間で同一に保たれます。
- **実行ベースのスコアリング、LLM ジャッジなし** — すべてのラウンドはシェルコマンドを伴い、その終了コード（オプションで出力マッチング）が合否を決定します。

---

## 📈 リーダーボード

メインエージェントのモデルを、タスク正答率に最小権限・モダリティルーティングの管理係数を掛け合わせた複合指標 **Subagent-Management Score (SMS)** でランク付けします。

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS は常に TCR 以下です。** 管理はタスク正答率を割り引くことしかできず、決して水増しすることはありません。完璧に管理してもタスクに失敗するモデルはスコアがゼロになります。

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

<sub>すべての値は % 単位、12 モデル × 41 シナリオを単一の評価実行で測定し、**SMS** でソートしています。新たにリリースされた `glm-5.2`（公式 z.ai API 経由）は最強のオープンウェイトマネージャーであり — SMS 50.4、総合 4 位 — `kimi-k2.6` を上回ってオープンウェイトモデルの首位に立ちました。**太字** は各列の最良値を示します（各列で独立に最良値をハイライト）。Cost ($)：プロバイダー / OpenRouter のリスト料金における実行あたりのメインエージェント API コスト — 低いほど良いため太字にしていません。サブエージェントは固定されたローカルプール上で実行され、価格は計上されません。Rounds：258 ラウンド中の合格ラウンド数。`claude-fable-5` は出荷時の状態で評価され、ベンダー推奨の拒否 → `claude-opus-4-8` フォールバックを伴います。</sub>

> 📥 結果を投稿しますか？ [docs/submit-to-leaderboard.md](../../docs/submit-to-leaderboard.md) を参照してください。実行例と寄稿された結果は [`submissions/`](../../submissions/) にあります。

---

## 🔑 主要な発見

12 のプロプライエタリ、コミュニティホスト、セルフホストのメインエージェントモデルにわたって、3 つの発見が浮かび上がりました。

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ ボトルネックは知覚ではなく *権限付与* にある

2 つの「容易な」軸はほぼ飽和しています — すべての有能なモデルにおいて読み取り専用遵守（ROC ≥ 92%）とモダリティ選択精度（MCA ≥ 92%）が高い値を示します。識別力のある軸は権限の精度に関する指標です：**Workspace-Permission Precision (WPP) はどのモデルでも 50% に *到達しません*。** サブエージェントには、実際にアクセスするファイルのおよそ 2 倍が日常的に付与されています。

</td>
<td width="33%" valign="top">

### 2️⃣ コストと管理品質は *分離している*

メインエージェントの API コストは **100 倍以上**（実行あたり \$0.8 → \$93）に及ぶ一方、SMS は **4 倍未満** にとどまります。最も安価なオープンモデルはパレートフロンティア上に位置し — `deepseek-v4-pro` はわずか \$1.7 で SMS 46.4 に到達します — 一方でいくつかの高コストモデル（`gpt-5.5`、`sonnet-4-6`、`kimi-k2.6`）は中コストの `gemini-3.5-flash` に *支配されています*。オープンウェイトの `glm-5.2`（$22.9）も最強のオープンモデルとしてフロンティア上に位置します。

</td>
<td width="33%" valign="top">

### 3️⃣ スコアは集中し、振る舞いは分岐する

フラッグシップを下回る 10 モデルは **9.9 ポイントの SMS 帯**（43.9〜53.8）に集中していますが、それらのオーケストレーション挙動は **1 桁以上** 異なります。サブエージェントあたりの禁止アクセス率は、有能なモデル間で 0.48 から 5.78（約 12 倍）に及び、動的ワークフローの利用は 8 から 112 回の呼び出しに及びます。

</td>
</tr>
</table>

<div align="center">

| コスト対管理（発見 2） | 権限違反（発見 3） |
|:---:|:---:|
| <img src="../../assets/pareto.png" alt="SMS vs. main-agent API cost, log scale; cheap open models on the Pareto frontier" width="430"> | <img src="../../assets/forbidden.png" alt="Per-model forbidden-access counts MAF/SAFt/SAFa on a log scale; SAFa diverges ~12x" width="430"> |

</div>

**モダリティルーティング。** マネージャーは圧倒的に `llm` キーをデフォルトとして使用し、比較的少数の `vlm`/`omni` スペシャリストしか作成しません。モダリティでルーティングを *行う* 場合には正しく行いますが（ゆえに MCA が高い）、マルチモーダルワーカーを過少利用しています。

<div align="center">
<img src="../../assets/modality.png" alt="Subagent model-key distribution: managers default to the llm key and under-use vlm/omni" width="780">
</div>

---

## 🚀 クイックスタート

完全なウォークスルー（プールの提供、ターゲットの選択、実行の再開）については [`docs/running-experiments.md`](../../docs/running-experiments.md) を参照してください。

### 1. インストール

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

これにより `clawarena-team` CLI がインストールされます（短いエイリアス：**`cateam`** / **`ca-team`**）。トークナイザーとチャットテンプレートは **`helper/` にバンドルされており** — ダウンロードのステップは不要です。

### 2. 固定されたサブエージェントプールを提供する（ローカル vLLM）

サブエージェントプールは、評価されるすべてのメインエージェント間で同一に保たれるため、管理だけが唯一の変数となります。

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. 検証、実行、分析

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

> 短いエイリアス `cateam` と `ca-team` は、あらゆる場所で `clawarena-team` と互換的に使用できます（例：`cateam run ...`）。

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

同じ文字列は `CATEAM_MODEL_JSON` 経由でも指定できます。`main.modalities` フィールドはメインエージェントがネイティブに知覚する内容を決定します。`Read` はモダリティ外のファイルをテキストのプレースホルダーに劣化させ、委譲を提案します。すべてのフラグと `CATEAM_*` 変数については [`docs/cli.md`](../../docs/cli.md)、データセット形式については [`docs/dataset.md`](../../docs/dataset.md)、プロバイダーの接続については [`docs/provider.md`](../../docs/provider.md) を参照してください。
</details>

---

## 🧰 機能サーフェスとツール

ClawArena-Team はサブエージェント管理を **プリンシパル–エージェント問題** として枠組み化します。メインエージェントの機能サーフェスは 6 つの具体的な操作に分解され、それぞれがシナリオ設計によって強制されます。

| Operation | What it requires |
|---|---|
| **作成** | システムプロンプト、モデルキー、ツールのサブセット、ワークスペースパスのホワイトリスト（自身のサブセット）を備えたサブエージェントを作成する。 |
| **モダリティルーティング** | マネージャーはテキストしか知覚しないため、画像/動画を `vlm` に、音声を `omni` にルーティングする。 |
| **最小権限の付与** | サブエージェントが実際に必要とするツールとパスのみを付与する。過剰な付与は無駄であり安全でない。 |
| **スケジューリング** | サブエージェントをフォアグラウンドまたはバックグラウンドで、新規または継続（再開）セッションとして、並列に実行する。バックグラウンドタスクは完了時にマネージャーに通知する。 |
| **動的ワークフロー** | 同一プール上で実行時にマルチサブエージェントのオーケストレーション（並列 + パイプラインステージ）を構成する。 |
| **統合** | サブエージェントの返答を正しい成果物に融合する。統合された回答のみが採点される。 |

メインエージェントには、クロスベンチマークの比較可能性のために実際のハーネス慣習を反映した名前・説明・パラメータを持つ **CapitalCase** ツールが公開されます。

| Tool | Purpose |
|---|---|
| **Read** | ファイルを読む。モダリティ外のコンテンツは委譲を提案するテキストのプレースホルダーに劣化する。 |
| **Write** | ワークスペース内にファイルを作成または上書きする。 |
| **Edit** | 既存ファイルに対象を絞ったインプレース編集を適用する。 |
| **Bash** | サンドボックス内でシェルコマンドを実行する（`realpath` チェック済みのパス）。 |
| **Grep** | パターンによってファイル内容を検索する。 |
| **Glob** | 名前パターンによってファイルを検索する。 |
| **CreateSubagent** | サブエージェントを定義する：システムプロンプト、モデルキー、ツールのサブセット、ワークスペースパスのホワイトリスト。 |
| **RunSubagent** | サブエージェントをフォアグラウンドまたはバックグラウンドで、新規または継続（再開）セッションとして呼び出す。 |
| **ListSubagents** | これまでに作成されたサブエージェントとそのステータスを一覧表示する。 |
| **InspectSubagent** | サブエージェントの設定、付与された権限、実行履歴を検査する。 |
| **Workflow** | JS スタイルのオーケストレーション DSL — `agent()`、`parallel()`、`pipeline()` — を用いて実行時にマルチサブエージェント実行を構成する。 |

システムレベルのシグナル（環境、トークンしきい値）は `<system-reminder>` ブロック経由で注入され、バックグラウンドタスクの完了は `<task-notification>` ブロック経由で届きます。すべてのパスアクセスは `realpath` でチェックされ、シンボリックリンクによる脱出は拒否され禁止アクセスとしてカウントされます。

### 固定されたサブエージェントプール（制御された変数）

| Key | Model | Server | Native modalities |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | local vLLM | text |
| `vlm`  | gemma-4-31b-it | local vLLM | text, image, video |
| `omni` | gemma-4-e4b-it | local vLLM | text, image, audio, video |

すべてのメインエージェントがこの同じチームを指揮します。実行間で変化するのはメインエージェントだけです。

---

## 📊 データと評価

すべてのシナリオは、ワークスペース、一連のユーザー質問、グラウンドトゥルースチェックを提供します。一部のラウンドの間に、ワークスペースは後続の回答を変化させる **段階的更新**（新規または置換されたファイル）を受け取り、一回限りの解決ではなく、進化するタスクの継続的な管理を要求します。

<div align="center">
<img src="../../assets/heatmap.png" alt="Per-scenario SMS heatmap: 12 models x 41 scenarios, difficulty is uneven and model-specific" width="820">
<br/>
<sub>シナリオ × モデルごとの SMS ヒートマップ — 難易度は不均一であり、モデル固有である。</sub>
</div>

**スコアリングコンポーネント**（すべて $[0,1]$、LLM ジャッジなし）：

| Metric | Meaning |
|---|---|
| **TCR** — Task Completion Rate | ユーザー質問に対する平均合格率。 |
| **TPP** — Tool-Permission Precision | サブエージェントごとに、付与されたツールタイプのうち実際に使用された割合。 |
| **ROC** — Read-Only Compliance | サブエージェントごとに、読み取り専用サブエージェントに変更ツールが付与された場合は 0、そうでなければ 1。 |
| **WPP** — Workspace-Permission Precision | サブエージェントごとに、アクセスされたファイル ÷ 付与されたファイル。 |
| **MCA** — Modality-Choice Accuracy | サブエージェントごとに、`vlm` が実際に画像/動画を読み、`omni` が音声を読むかどうか（`llm` は 1 となる）。 |

すべてのシナリオは **10 個の厳格な設計制約（C1–C10）** を満たします — 読み取り不能な領域、実質的な段階的更新、フルツールサーフェスの使用、デコイを含む 8 つ以上のディレクトリ、非テキストモダリティのラウンド、並列が必須のタスク、セッション再利用ペア、ラウンド間の依存関係、モダリティデコイ、機械検証可能な回答 — それぞれが、単一の言語モデルなら迂回できてしまう個別の管理失敗モードを標的としています。

### データセットの構成

- **41 シナリオ・258 ラウンド**、そのうち 44（17.1%）は段階的更新が先行します。
- **72 更新グループ、255 ファイル**（61.1% が `new`、38.9% が `replace`、平均 3.54 ファイル/グループ）。
- **170.5 MiB・28.9 M トークン** — 71.9% がワークスペースコンテンツ、27.9% が段階的更新。
- モダリティの内訳：ファイル/トークンではテキストが支配的である一方、生バイト数では音声と画像が支配的です — テキストのみのマネージャーが直接消費できない、かなりの非テキストペイロードです。

ClawArena-Team は **収集されたものではなく構築されたもの** です：ワークスペースコーパス、マルチモーダルアセット、グラウンドトゥルース、実行チェックはすべて、同じバージョン管理されたスクリプトから **合成–検証フライホイール** を通じて手続き的に合成されており、その中で実際のベースラインのサブエージェント管理実行が最終的な受け入れゲートとなります。このベンチマークは、実質的に、それが測定するまさにその能力によって作成されています。形式と構築方法論については [`docs/dataset.md`](../../docs/dataset.md) と論文の付録を参照してください。

より細かい分布については [`docs/data-stats/`](../../docs/data-stats/) を参照してください：各サブセット（`demo` / `wave1` / `wave3` / `wave4`）と全体セットは、それぞれ独自の `STATS.md` とチャート（トークン / ファイルサイズ / モダリティの分布、タグカバレッジ、...）を持ち、`clawarena-team stats` によって生成されます。

---

## 🔍 ケーススタディ

記録された実行トランスクリプトと `metadata.json` ファイルから直接抽出した 12 のケース — すべての数値と引用文字列はそのまま — が、3 つの発見と管理機能サーフェスを具体的に裏付けます。

<details>
<summary><b>ケース 1〜4：最強のマネージャーにおける過剰付与、正しいモダリティルーティング、モダリティデコイの罠、品質から分離したコスト</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_1.png" alt="Case studies 1-4" width="900">
</div>
</details>

<details>
<summary><b>ケース 5〜8：禁止アクセスが分岐しているのに同一スコア、動的ワークフローの作成（およびクラッシュするファンアウト）、真のバックグラウンドスケジューリングなしの論理的並列性、真のバックグラウンドとワークフロー並列性</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_2.png" alt="Case studies 5-8" width="900">
</div>
</details>

<details>
<summary><b>ケース 9〜12：決して伝播しない保留中の修正、マネージャーが操作できない能力の崖、管理の天井（並列ファンアウト、適応的リトライ、最小権限）、優れた管理とはどのようなものか</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_3.png" alt="Case studies 9-12" width="900">
</div>
</details>

---

## 📖 ドキュメント

| Document | Description |
|----------|-------------|
| [CLI リファレンス](../../docs/cli.md) | すべてのコマンド、フラグ、`CATEAM_*` 環境変数 |
| [データセット形式](../../docs/dataset.md) | シナリオレイアウト、ラウンド、段階的更新、グラウンドトゥルースチェック |
| [プロバイダーガイド](../../docs/provider.md) | メインエージェントプロバイダーの接続（OpenAI-compat、Gemini、OpenRouter、...） |
| [実験の実行](../../docs/running-experiments.md) | サブエージェントプールの提供とフルスイープの実行 / 再開 |
| [リーダーボードへの投稿](../../docs/submit-to-leaderboard.md) | 実行のパッケージ化と [`submissions/`](../../submissions/) への寄稿 |

---

## 🏗️ プロジェクト構成

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

本研究は現在、匿名のプレプリントです。arXiv 識別子と著者リストは後日追加予定です。

```bibtex
@misc{clawarena-team2026,
  title  = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author = {Anonymous Author(s)},
  year   = {2026},
  note   = {Preprint. arXiv identifier and author list to be added.}
}
```

---

## 📄 ライセンス

本プロジェクトは [MIT License](../../../LICENSE) の下でライセンスされています。
