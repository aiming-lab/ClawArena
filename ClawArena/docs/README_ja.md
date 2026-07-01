<div align="center">

<img src="../assets/claweval.png" alt="ClawArena" width="500">

<br/>

## 進化する情報環境における AI エージェントのベンチマーク。

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
      <b style="font-size:1.1em">+ 任意のエージェント</b>
    </td>
  </tr>
  <tr>
    <td align="center"><b>OpenClaw</b></td>
    <td align="center"><b>Claude Code</b></td>
    <td align="center"><b>MetaClaw</b></td>
    <td align="center"><b>PicoClaw</b></td>
    <td align="center"><b>Nanobot</b></td>
    <td align="center"><a href="plugin.md">プラグイン</a> 経由</td>
  </tr>
</table>

<br/>

<p>
  <a href="../README.md">English</a> |
  <a href="README_zh.md">中文</a> |
  <b>日本語</b> |
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
  <a href="../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="License MIT"></a>
  <a href="https://github.com/aiming-lab/ClawArena/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat" alt="PRs welcome" /></a>
</p>
<p>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Scenarios-12-orange?style=flat&labelColor=555" alt="12 Scenarios" />
  <img src="https://img.shields.io/badge/Rounds-337-red?style=flat&labelColor=555" alt="337 Rounds" />
  <img src="https://img.shields.io/badge/Dynamic%20Updates-45-yellow?style=flat&labelColor=555" alt="45 Dynamic Updates" />
  <img src="https://img.shields.io/badge/Frameworks-5-blueviolet?style=flat&labelColor=555" alt="5 Frameworks" />
</p>

[🔭 概要](#-概要) • [📈 リーダーボード](#-リーダーボード) • [🆚 ベンチマーク比較](#-ベンチマーク比較) • [🚀 クイックスタート](#-クイックスタート) • [🤖 対応フレームワーク](#-対応フレームワーク) • [📊 データと評価](#-データと評価) • [🔍 ケーススタディ](#-ケーススタディ) • [📖 ドキュメント](#-ドキュメント) • [🏗️ プロジェクト構成](#-プロジェクト構成) • [🙏 関連プロジェクト](#-関連プロジェクト) • [📚 引用](#-引用) • [📄 ライセンス](#-ライセンス)

</div>

---

## 🔭 概要

**ClawArena** は AI コーディングエージェントのためのベンチマーク評価プラットフォームです。同一のリアルなマルチセッションシナリオ群において推論を実行し、結果を採点し、異なるエージェントフレームワーク間の性能を比較するための統一されたパイプラインを提供します。

- **12 件のマルチターンシナリオ** — 小売分析、金融、医療、情報セキュリティ、人事、教育、研究公正など多様な専門領域を網羅
- **337 ラウンドの評価** — `multi_choice` 推論（95 ラウンド）と `exec_check` 実行検証（242 ラウンド）を組み合わせ
- **45 件の動的アップデート** — 評価途中で新規ファイルやチャットセッションを注入し、信念の修正と矛盾処理能力を検証
- **マルチセッションコンテキスト** — エージェントは各シナリオ内でワークスペースのファイルとマルチチャネルのチャット履歴（IM、メールなど）を踏まえて推論
- **フレームワーク非依存** — 論文では 5 つのフレームワーク（OpenClaw、Claude Code、NanoBot、PicoClaw、MetaClaw）を評価；新しいフレームワークは[プラグイン機構](plugin.md)で追加可能
- **[MetaClaw](https://github.com/aiming-lab/MetaClaw) 統合** — メモリ、スキル、RL で強化されたエージェントを評価

---

## 📈 リーダーボード

エージェントは **総合信頼性スコア（Composite Reliability Score, CRS）** で順位付けします。これは正答率と挙動の一貫性を等しく重み付けする指標です。_すべての数値は 12 シナリオ / 337 ラウンドにわたるマクロ平均で、CRS によりソートされています。_

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

<sub>各モデルは主要なハーネス上で表示されています：Anthropic 系モデルは Claude Code 経由で実行（OpenClaw とは非互換）、それ以外のモデルはすべて OpenClaw 上で表示しています。モデルを固定しハーネスを変えるクロスフレームワーク比較は論文を参照してください。</sub>

<sub><b>指標定義</b> — <b>TCR</b>（タスク完了率, Task Completion Rate）= S/N、全ラウンドの平均正答率。MC・EC のサブスコアに分解可能 · <b>SC</b>（成功凝集度, Success Cohesion）= (S−k)/(N−1)、正答ラウンドが長い連続区間に集約される度合い（連勝が 1 区間なら SC = 1、合否交互なら SC = 0） · <b>FD</b>（失敗分散度, Failure Dispersion）= 1 − (S_f−k_f)/(N−1)、長期にわたる失敗連続区間にペナルティを課す · <b>頑健性（Robustness）</b> = SC × FD（乗算形式により、いずれかの軸が崩壊するとスコアが大きく低下） · <b>CRS</b> = (TCR + Robustness) / 2。</sub>

> 📥 **新しい結果を投稿しますか？** [submit-to-leaderboard.md](submit-to-leaderboard.md) をご覧ください。参考レイアウトは [`result_example/`](../result_example/) にあり、コミュニティからの投稿は [`submissions/`](../submissions/) に集約します。

---

## 🆚 ベンチマーク比較

ClawArena が他のハーネスネイティブなエージェントベンチマークとどのように異なるかを示します。既存研究の多くは 4 つの設計軸のうち最大 2 つしかカバーしておらず、ClawArena は 4 軸すべてを同時に満たし、かつ 5 つのフレームワーク横断で結果を報告する唯一のベンチマークです。

<table>
<thead>
<tr>
<th align="left"><sub>ベンチマーク</sub></th><th align="left"><sub>タスク収集</sub></th><th align="left"><sub>実行モード</sub></th><th><sub>MSC</sub></th><th><sub>DU</sub></th><th><sub>MU</sub></th><th><sub>Pref.</sub></th><th><sub>検証</sub></th><th><sub>Frmw.</sub></th><th align="left"><sub>規模（問題数 / シナリオ）</sub></th>
</tr>
</thead>
<tbody>
<tr><td><sub><a href="https://github.com/reacher-z/ClawBench">ClawBench</a></sub></td><td><sub>手動プール</sub></td><td><sub>ライブ Web</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td><sub>ルール+LLM</sub></td><td align="center"><sub>8</sub></td><td><sub>283 / 144 サイト</sub></td></tr>
<tr><td><sub><a href="https://github.com/claw-eval/claw-eval">Claw-Eval</a></sub></td><td><sub>上流からキュレーション</sub></td><td><sub>サンドボックス + モック</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>❌</sub></td><td><sub>ルール+LLM</sub></td><td align="center"><sub>1</sub></td><td><sub>300 / 9 カテゴリ</sub></td></tr>
<tr><td><sub><a href="https://github.com/Claw-Eval-Live/Claw-Eval-Live">Claw-Eval-Live</a></sub></td><td><sub>ライブ信号（四半期更新）</sub></td><td><sub>モックサービス</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td><sub>ルール+LLM</sub></td><td align="center"><sub>1</sub></td><td><sub>105 / 17 ファミリ</sub></td></tr>
<tr><td><sub><a href="https://github.com/evolvent-ai/ClawMark">ClawMark</a></sub></td><td><sub>手動 + AI 合成</sub></td><td><sub>サンドボックス化サービス</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>❌</sub></td><td><sub>ルールのみ</sub></td><td align="center"><sub>1</sub></td><td><sub>100 / 13 シナリオ</sub></td></tr>
<tr><td><sub><a href="https://github.com/benchflow-ai/ClawsBench">ClawsBench</a></sub></td><td><sub>専門家設計</sub></td><td><sub>モックサービス</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td><sub>ルールのみ</sub></td><td align="center"><sub>4</sub></td><td><sub>44 / 5 サービス</sub></td></tr>
<tr><td><sub><a href="https://github.com/aiming-lab/MetaClaw">MetaClaw-Bench</a></sub></td><td><sub>合成</sub></td><td><sub>ワークスペース模擬</sub></td><td align="center"><sub>🟡</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>🟡</sub></td><td><sub>ルールのみ</sub></td><td align="center"><sub>1</sub></td><td><sub>346 / 30 日</sub></td></tr>
<tr><td><sub><a href="https://github.com/pinchbench/skill">PinchBench</a></sub></td><td><sub>手動（実世界）</sub></td><td><sub>リアル（OpenClaw）</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td><sub>ルール+LLM</sub></td><td align="center"><sub>1</sub></td><td><sub>23 / 8 カテゴリ</sub></td></tr>
<tr><td><sub><a href="https://huggingface.co/datasets/skylenage-ai/QwenClawBench">QwenClawBench</a></sub></td><td><sub>経験的（主張）</sub></td><td><sub>リアル（Docker）</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>🟡</sub></td><td><sub>ルール+LLM</sub></td><td align="center"><sub>1</sub></td><td><sub>100 / 8 ドメイン</sub></td></tr>
<tr><td><sub><a href="https://github.com/InternLM/WildClawBench">WildClawBench</a></sub></td><td><sub>手動（野外収集）</sub></td><td><sub>リアル（OpenClaw）</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>🟡</sub></td><td><sub>ルール+LLM</sub></td><td align="center"><sub>1</sub></td><td><sub>60 / 6 カテゴリ</sub></td></tr>
<tr><td><sub><a href="https://huggingface.co/datasets/zai-org/ZClawBench">ZClawBench</a></sub></td><td><sub>手動 + 合成</sub></td><td><sub>リアル + 部分モック</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td align="center"><sub>❌</sub></td><td><sub>ルール+LLM</sub></td><td align="center"><sub>1</sub></td><td><sub>116 / 6 カテゴリ</sub></td></tr>
<tr><td><sub><b>ClawArena（本研究）</b></sub></td><td><sub><b>経験的合成</b></sub></td><td><sub><b>マルチチャネル模擬</b></sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>✅</sub></td><td align="center"><sub>✅</sub></td><td><sub>ルールのみ</sub></td><td align="center"><sub><b>5</b></sub></td><td><sub><b>337 / 12 シナリオ</b></sub></td></tr>
</tbody>
</table>

<sub><b>凡例</b> — ✅ サポート · ❌ 非対応 · 🟡 部分対応（仕組みは存在するが弱化されている。例: 第三者メッセージがチャネルタグ付きセッションではなく単なるファイルとして提示される、嗜好が静黙ラウンドで学習されず静的ペルソナとして埋め込まれている、など）。 &nbsp; <b>MSC</b>（Multi-Source Conflict、複数ソース間の矛盾）: チャネルで区別されたユーザーと第三者間の会話を分析 · <b>DU</b>（Dynamic Update、動的更新）: ユーザーターンの間で環境が上書きされる（同一ループ内のツール戻り値の変化は含まれない） · <b>MU</b>（Multi-User turn、マルチユーザーターン）: ユーザーが複数ラウンドにわたって新たなクエリで再関与する · <b>Pref.</b>（Implicit personalization、暗黙的パーソナライゼーション）: ユーザー嗜好を静黙評価ラウンドで適用する · <b>Frmw.</b>: 評価対象のエージェントフレームワーク数。</sub>

---

## 🚀 クイックスタート

### 1. 一括インストール

```bash
bash scripts/setup.sh
```

このコマンドで ClawArena（dev extras 付き）、MetaClaw、フレームワーク CLI（OpenClaw、Claude Code、Nanobot、PicoClaw）、および Claude Code Router を一括導入します。手動セットアップは[インストールガイド](installation.md)を参照してください。

Git から Python パッケージとして（データセットをバンドルして）直接インストールする場合：

```bash
pip install git+https://github.com/aiming-lab/ClawArena.git
```

このコマンドで `clawarena` CLI と `ClawArena` Python SDK の両方が利用できます。データのバンドル方法またはオンデマンド取得については[インストールガイド](installation.md)を参照してください。

### 2. ベンチマーク実行

まず [`scripts/env_example.sh`](../scripts/env_example.sh) を参照して環境変数を設定し、続いて以下を実行します。

```bash
python scripts/test_run.py
```

`scripts/test_run.py` を編集することで、フレームワーク、並列度、タイムアウト、出力先を設定できます。

<details>
<summary><b>あるいは CLI を直接利用する</b></summary>

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

すべてのコマンドおよびオプションは [CLI リファレンス](cli.md) を参照してください。
</details>

<details>
<summary><b>あるいは Python SDK を利用する</b></summary>

```python
from clawarena import ClawArena

ca = ClawArena(data="data/clawarena/tests.json", out="output/", concurrency=8)
ca.check(framework="openclaw")
ca.run(["openclaw", "claude-code"])          # infer + score + report + compare
ca.stats(framework="openclaw", out="stats/")
```

共通設定はコンストラクタに渡し、各メソッドで呼び出しごとに上書き可能です。完全な API については [Python SDK ガイド](sdk.md) を参照してください。
</details>

<details>
<summary><b>開発とテスト</b></summary>

```bash
pip install -e ".[dev]"
pytest
```

</details>

---

## 🤖 対応フレームワーク

| フレームワーク | 種別 | 言語 | 備考 |
|-----------|------|----------|-------|
| [OpenClaw](https://github.com/openclaw/openclaw) | CLI エージェント | Node.js | — |
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | LLM プロキシ | Python | [OpenClaw](https://github.com/openclaw/openclaw) と [Nanobot](https://github.com/HKUDS/nanobot) でのみ対応 |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) | CLI エージェント | Node.js | [Claude Code Router](https://github.com/musistudio/claude-code-router) で支援 |
| [PicoClaw](https://github.com/sipeed/picoclaw) | CLI エージェント | Go | — |
| [Nanobot](https://github.com/HKUDS/nanobot) | CLI エージェント | Python | — |
| ClawArena Native | 組み込みハーネス | Python | ClawArena に同梱；外部インストール不要 |

新しいフレームワークはコア部分を変更せずプラグイン機構で追加可能です — アダプタを登録する `.py` ファイルを配置し、実行時に読み込むだけです。

```bash
clawarena infer --data tests.json --framework my_agent --out results/ --plugin my_agent.py
```

アダプタインターフェースとエンジンのラウンドフックの詳細は[プラグインガイド](plugin.md)を参照してください。

[MetaClaw](https://github.com/aiming-lab/MetaClaw) はメモリ、スキル、RL で強化されたエージェントを評価するための透過的プロキシ層として統合されています。`tests.json` に `metaclaw` フィールドを追加することで有効化でき、対応するホストフレームワークは **OpenClaw** と **Nanobot** です。マネージド／アンマネージドモード、トリガ設定、YAML テンプレートの詳細は [MetaClaw ガイド](metaclaw-guide.md) を参照してください。

**ClawArena Native** は ClawArena に同梱された組み込みエージェントハーネスです。外部フレームワークの CLI をインストールできない環境、あるいは固定バージョンへのピン留めが難しい環境では、この自己完結型の決定論的ハーネスでベンチマークを実行できます。外部インストールは不要で、インプロセスで動作します。`--framework clawarena-native` で選択してください。ツール、マルチセッション設計、データレイアウトの詳細は [ネイティブハーネスガイド](clawarena-native.md) を参照してください。

---

## 📊 データと評価

<div align="center">
<img src="../assets/overview.png" alt="ClawArena Cross-Domain Data Sample Gallery" width="900">
</div>

各シナリオには以下が含まれます：

- **ワークスペースファイル** — エージェントが読み込めるドキュメント、表計算、コード
- **セッション履歴** — マルチチャネルのチャットログ（IM、メール、Slack 等）
- **評価質問** — `multi_choice`（推論）と `exec_check`（実行検証）
- **動的アップデート** — ラウンド間に注入される新規セッションとファイル

337 ラウンドにまたがる 2 種類の質問形式：

| 種別 | ラウンド | 検証対象 | 方法 |
|------|------:|-------|-----|
| `multi_choice` | 95 (28.2%) | エージェントの推論と理解 | 応答から `\bbox{A,B,...}` を抽出し、正解との IoU/F1 を計算 |
| `exec_check`   | 242 (71.8%) | エージェントの動作とファイル出力 | シェルコマンドを実行し終了コードと stdout を検証 |

<details>
<summary><b>データ構築パイプライン（クリックで展開）</b></summary>
<br/>
<div align="center">
<img src="../assets/pipeline_v2.png" alt="ClawArena Construction Pipeline" width="700">
</div>

12 シナリオ全ての構築に用いた六層仕様体系の全容は[データ仕様](data-spec/)を参照してください。
</details>

データ構築仕様一式 — 六層シナリオ設計、合成ガイドライン、落とし穴に関するドキュメントを含む — は [`docs/data-spec/`](data-spec/) に公開しています。

完全なフォーマット仕様は[データ構造](data-structure.md)を参照してください。

---

## 🔍 ケーススタディ

ClawArena の 12 シナリオから抽出した 10 件のオプション別ケーススタディ。MS-R、DU-R、P-R および `exec_check` などのインタラクションカテゴリを、セキュリティ、臨床、人事、E コマースの各領域にわたり収録しています。

<details>
<summary><b>ケース 1–2：NexaFlow API 漏洩（MS-R）とスキーマ準拠失敗（exec_check）</b></summary>
<br/>
<div align="center">
<img src="../assets/case_01_02.png" alt="Case 1-2" width="900">
</div>
</details>

<details>
<summary><b>ケース 3–4：研究公正の複合オプション（MS-R）と権威の影響を受けた修正（DU-R）</b></summary>
<br/>
<div align="center">
<img src="../assets/case_03_04.png" alt="Case 3-4" width="900">
</div>
</details>

<details>
<summary><b>ケース 5–6：不当解雇のファイル名プレフィックス（P-R + exec_check）と GDPR 構造化出力の上限（exec_check）</b></summary>
<br/>
<div align="center">
<img src="../assets/case_05_06.png" alt="Case 5-6" width="900">
</div>
</details>

<details>
<summary><b>ケース 7–8：618 GPU 詐欺のアップデート固有失敗（DU-R）と JSON スキーマ遵守（exec_check）</b></summary>
<br/>
<div align="center">
<img src="../assets/case_07_08.png" alt="Case 7-8" width="900">
</div>
</details>

<details>
<summary><b>ケース 9–10：不当解雇の連言的統合（MS-R + DU-R）とパイプライン著者帰属の最終統合（exec_check + MS-R）</b></summary>
<br/>
<div align="center">
<img src="../assets/case_09_10.png" alt="Case 9-10" width="900">
</div>
</details>

---

## 📖 ドキュメント

| ドキュメント | 説明 |
|----------|-------------|
| [インストール](installation.md) | ClawArena、各フレームワーク、MetaClaw のセットアップガイド |
| [CLI リファレンス](cli.md) | すべてのコマンド、フラグ、環境変数 |
| [Python SDK](sdk.md) | `ClawArena` クラスによるライブラリとしての利用方法 |
| [ネイティブハーネス](clawarena-native.md) | 組み込み `clawarena-native` フレームワーク |
| [データ構造](data-structure.md) | データセット形式、質問形式、マニフェストスキーマ |
| [プロバイダガイド](provider-usage-guide.md) | LLM プロバイダ設定と優先度チェーン |
| [MetaClaw ガイド](metaclaw-guide.md) | MetaClaw 統合モードとトリガフック |
| [プラグインガイド](plugin.md) | 外部フレームワークアダプタの作成と登録 |

---

## 🏗️ プロジェクト構成

```
ClawArena
├── src/clawarena/
│   ├── cli.py           # CLI エントリポイント（SDK へ委譲）
│   ├── sdk.py           # Python SDK: ClawArena クラス
│   ├── _paths.py        # データルート解決（バンドル / 開発ツリー / キャッシュ）
│   ├── datafetch.py     # オンデマンドデータセットダウンローダー（clawarena fetch-data）
│   ├── core/            # パイプライン: infer, score, report, compare, check, run, clean
│   ├── stats/           # トークン＋構造解析（フレームワーク別レイアウト）
│   ├── engines/         # エージェント実行エンジン（フレームワーク別）
│   ├── data_handlers/   # データ読み込み、検証、ワークコピー管理
│   ├── native/          # 組み込み clawarena-native ハーネス（インプロセスエージェントループ）
│   ├── adapters/        # フレームワークアダプタの構成とレジストリ
│   ├── qtypes/          # 質問形式: multi_choice, exec_check
│   ├── metaclaw/        # MetaClaw プロキシのライフサイクルとトリガフック
│   └── plugins/         # 外部アダプタの読み込み（--plugin）
├── data/                # データセット（ホイールに clawarena/_data としてバンドル）
├── docs/                # ドキュメント、docs/data-spec/（六層構築仕様）を含む
├── scripts/             # セットアップ、テストランナー、比較ユーティリティ
├── helpers/             # フレームワーク固有のヘルパーフック
└── tests/               # テストスイート
```

---

## 🙏 関連プロジェクト

ClawArena は以下のオープンソース・エージェントフレームワークの上に構築され、それらを評価対象としています：

- [OpenClaw](https://github.com/openclaw/openclaw) — 主要な評価対象 CLI エージェント。
- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — メモリ、スキル、RL でエージェントを強化するメタ学習プロキシ。
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropic のエージェント型コーディングツール。
- [Claude Code Router](https://github.com/musistudio/claude-code-router) — Claude Code のリクエストを別モデルへルーティング。
- [PicoClaw](https://github.com/sipeed/picoclaw) — Go ベースの軽量 CLI エージェント。
- [Nanobot](https://github.com/HKUDS/nanobot) — Anthropic API に対応した Python ネイティブの CLI エージェント。

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

## 📄 ライセンス

本プロジェクトは [MIT ライセンス](../../LICENSE) の下で公開されています。
