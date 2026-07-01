<div align="center">

<h1>ClawArena-Team</h1>

### 언어 모델 에이전트의 서브에이전트 오케스트레이션 및 동적 워크플로 벤치마킹

<p>
  <a href="../../README.md">English</a> •
  <a href="README.zh-Hans.md">简体中文</a> •
  <a href="README.zh-Hant.md">繁體中文</a> •
  <a href="README.ja.md">日本語</a> •
  <b>한국어</b> •
  <a href="README.fr.md">Français</a> •
  <a href="README.de.md">Deutsch</a> •
  <a href="README.es.md">Español</a> •
  <a href="README.pt.md">Português</a> •
  <a href="README.ru.md">Русский</a>
</p>

<p>
  <a href="#-인용"><img src="https://img.shields.io/badge/Paper-Preprint-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="Paper" /></a>
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

[🔭 개요](#-개요) • [📈 리더보드](#-리더보드) • [🔑 핵심 발견](#-핵심-발견) • [🚀 빠른 시작](#-빠른-시작) • [🧰 역량 표면 및 도구](#-역량-표면-및-도구) • [📊 데이터 및 평가](#-데이터-및-평가) • [🔍 사례 연구](#-사례-연구) • [📖 문서](#-문서) • [🏗️ 프로젝트 구조](#️-프로젝트-구조) • [📚 인용](#-인용) • [📄 라이선스](#-라이선스)

</div>

---

## 🔭 개요

LM 에이전트는 점점 더 **관리자(manager)** 로 배포되고 있습니다. 하나의 메인 모델이 전문화된 서브에이전트를 생성하고, 작업을 위임하며, 동적 워크플로를 통해 이들의 병렬적·비동기적 반환을 오케스트레이션합니다. 기존 벤치마크는 정책 자체의 작업 해결 능력이나 고정된 멀티 에이전트 시스템을 평가하지만, 리더로서 행동하는 단일 LM의 **관리 능력(management ability)** 을 분리해서 측정하는 것은 없습니다.

**ClawArena-Team** (ClawArena 시리즈의 팀 관리 변형)은 바로 이 능력을 분리합니다. **텍스트 전용 메인 에이전트**는 **고정된, 로컬에서 서빙되는 풀**로부터 서브에이전트를 생성·권한 부여·스케줄링·통합함으로써, 혼자서는 수행할 수 없는 멀티턴·멀티모달·멀티디렉터리 작업을 완수해야 합니다. 모든 관리자가 동일한 워커를 지휘하므로, 점수 차이는 *원시 역량이 아니라 관리 기술* 을 반영합니다.

- **41개 시나리오 · 258개 평가 라운드 · 72개 단계적 업데이트**, **법률, 의료, 공학, 비즈니스, 과학** 분야를 아우릅니다.
- **텍스트 전용, 부분 가시 메인 에이전트** — 메인 에이전트는 텍스트만 네이티브로 인지하고 워크스페이스의 일부에만 접근하므로, 위임이 필수입니다.
- **고정된 서브에이전트 풀** 은 vLLM을 통해 로컬에서 서빙되며(`llm`/`vlm`/`omni`), 평가되는 모든 관리자에 대해 동일하게 유지됩니다.
- **실행 기반 채점, LLM 심판 없음** — 모든 라운드는 종료 코드(선택적 출력 매칭 포함)로 통과/실패를 결정하는 셸 명령을 함께 제공합니다.

---

## 📈 리더보드

메인 에이전트 모델을 복합 지표인 **서브에이전트 관리 점수(Subagent-Management Score, SMS)** 로 순위를 매깁니다. 이 점수는 작업 정확도에 최소 권한(least-privilege) 및 모달리티 라우팅 관리 계수를 곱한 값입니다:

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS ≤ TCR 항상 성립:** 관리는 작업 정확도를 할인할 수만 있을 뿐, 부풀릴 수는 없습니다. 완벽하게 관리하지만 작업에 실패하는 모델은 0점을 받습니다.

| 모델 | TCR | TPP | ROC | WPP | MCA | **SMS** | 비용 ($) | 라운드 |
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

<sub>모든 값은 % 단위이며, 단일 평가 실행에서 12개 모델 × 41개 시나리오를 대상으로 하고 **SMS** 기준으로 정렬되었습니다. 새롭게 출시된 `glm-5.2` (공식 z.ai API 경유)는 가장 강력한 오픈 웨이트 관리자입니다 — SMS 50.4, 전체 4위 — `kimi-k2.6`을 추월하여 오픈 웨이트 모델 중 선두에 올랐습니다. **굵게** 표시된 값은 해당 열의 최고값입니다(각 열에서 독립적으로 최고값을 강조). 비용 ($): 공급자 / OpenRouter 정가 기준 실행당 메인 에이전트 API 비용 — 낮을수록 좋으므로 굵게 표시하지 않았습니다. 서브에이전트는 고정된 로컬 풀에서 실행되며 가격이 책정되지 않습니다. 라운드: 258개 중 통과한 라운드 수. `claude-fable-5`는 출시된 상태 그대로 평가되며, 공급사 권장 거부 → `claude-opus-4-8` 폴백을 사용합니다.</sub>

> 📥 결과를 제출하시나요? [docs/submit-to-leaderboard.md](../../docs/submit-to-leaderboard.md)를 참고하세요. 예시 실행 및 기여된 결과는 [`submissions/`](../../submissions/)에 있습니다.

---

## 🔑 핵심 발견

독점, 커뮤니티 호스팅, 자체 호스팅 메인 에이전트 모델 12종에 걸쳐 세 가지 발견이 나타납니다.

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ 병목은 인지가 아니라 *권한 부여* 다

두 가지 "쉬운" 축은 거의 포화 상태입니다 — 유능한 모든 모델에서 읽기 전용 준수(ROC ≥ 92%)와 모달리티 선택 정확도(MCA ≥ 92%)를 보입니다. 변별력 있는 축은 권한 정밀도 지표입니다: **워크스페이스 권한 정밀도(WPP)는 어떤 모델에서도 *결코* 50%에 도달하지 못합니다**. 서브에이전트는 실제로 접근하는 파일의 대략 두 배에 달하는 권한을 일상적으로 부여받습니다.

</td>
<td width="33%" valign="top">

### 2️⃣ 비용과 관리 품질은 *분리되어 있다*

메인 에이전트 API 비용은 **100배 이상** 차이가 나는 반면(실행당 \$0.8 → \$93), SMS는 **4배 미만** 차이가 납니다. 가장 저렴한 오픈 모델이 파레토 경계에 위치합니다 — `deepseek-v4-pro`는 단 \$1.7로 SMS 46.4를 달성합니다 — 반면 고비용 모델 여러 개(`gpt-5.5`, `sonnet-4-6`, `kimi-k2.6`)는 중간 비용의 `gemini-3.5-flash`에 *지배(dominated)* 당합니다. 오픈 웨이트 `glm-5.2` ($22.9) 또한 가장 강력한 오픈 모델로서 경계 위에 위치합니다.

</td>
<td width="33%" valign="top">

### 3️⃣ 점수는 모이지만, 행동은 갈린다

플래그십 아래로, 10개 모델이 **9.9포인트의 SMS 대역**(43.9–53.8) 안에 모여 있지만, 이들의 오케스트레이션 행동은 **자릿수 이상으로** 차이가 납니다. 서브에이전트당 금지 접근율은 유능한 모델 사이에서 0.48에서 5.78까지 분포하며(~12배), 동적 워크플로 사용은 8회에서 112회까지의 호출 범위에 걸쳐 있습니다.

</td>
</tr>
</table>

<div align="center">

| 비용 대 관리 (발견 2) | 권한 위반 (발견 3) |
|:---:|:---:|
| <img src="../../assets/pareto.png" alt="SMS 대 메인 에이전트 API 비용, 로그 스케일; 저렴한 오픈 모델이 파레토 경계에 위치" width="430"> | <img src="../../assets/forbidden.png" alt="모델별 금지 접근 횟수 MAF/SAFt/SAFa 로그 스케일; SAFa는 약 12배 차이로 갈림" width="430"> |

</div>

**모달리티 라우팅.** 관리자들은 압도적으로 `llm` 키를 기본값으로 사용하며 상대적으로 적은 수의 `vlm`/`omni` 전문가를 생성합니다. 모달리티에 따라 *실제로* 라우팅할 때는 올바르게 수행하지만(따라서 높은 MCA), 멀티모달 워커를 과소 활용합니다.

<div align="center">
<img src="../../assets/modality.png" alt="서브에이전트 모델 키 분포: 관리자는 llm 키를 기본값으로 사용하고 vlm/omni를 과소 활용" width="780">
</div>

---

## 🚀 빠른 시작

전체 절차(풀 서빙, 대상 선택, 실행 재개)는 [`docs/running-experiments.md`](../../docs/running-experiments.md)를 참고하세요.

### 1. 설치

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

이는 `clawarena-team` CLI(짧은 별칭: **`cateam`** / **`ca-team`**)를 설치합니다. 토크나이저와 채팅 템플릿은 **`helper/`에 번들로 포함**되어 있어 — 다운로드 단계가 필요 없습니다.

### 2. 고정 서브에이전트 풀 서빙 (로컬 vLLM)

서브에이전트 풀은 평가되는 모든 메인 에이전트에 대해 동일하게 유지되므로, 관리가 유일한 변수입니다:

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. 검증, 실행, 분석

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

> 짧은 별칭 `cateam`과 `ca-team`은 어디서나 `clawarena-team`과 호환됩니다(예: `cateam run ...`).

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

동일한 문자열을 `CATEAM_MODEL_JSON`을 통해 제공할 수도 있습니다. `main.modalities` 필드는 메인 에이전트가 네이티브로 인지하는 대상을 결정합니다. `Read`는 모달리티를 벗어난 파일을 텍스트 플레이스홀더로 강등시키고 위임을 제안합니다. 모든 플래그와 `CATEAM_*` 변수는 [`docs/cli.md`](../../docs/cli.md), 데이터셋 형식은 [`docs/dataset.md`](../../docs/dataset.md), 공급자 연동은 [`docs/provider.md`](../../docs/provider.md)를 참고하세요.
</details>

---

## 🧰 역량 표면 및 도구

ClawArena-Team은 서브에이전트 관리를 **주인-대리인 문제(principal–agent problem)** 로 구성합니다. 메인 에이전트의 역량 표면은 시나리오 설계에 의해 각각 강제되는 여섯 가지 구체적 작업으로 분해됩니다:

| 작업 | 요구 사항 |
|---|---|
| **생성(Creation)** | 시스템 프롬프트, 모델 키, 도구 부분집합, 워크스페이스 경로 화이트리스트(자신의 부분집합)를 갖춘 서브에이전트를 생성합니다. |
| **모달리티 라우팅(Modality routing)** | 관리자는 텍스트만 인지하므로, 이미지/비디오는 `vlm`으로, 오디오는 `omni`로 라우팅합니다. |
| **최소 권한 부여(Least-privilege empowerment)** | 서브에이전트가 실제로 필요한 도구와 경로만 부여합니다. 과도한 부여는 낭비이자 안전하지 않습니다. |
| **스케줄링(Scheduling)** | 서브에이전트를 포그라운드 또는 백그라운드로, 신규 또는 이어진(재개된) 세션으로, 그리고 병렬로 실행합니다. 백그라운드 작업은 완료 시 관리자에게 알립니다. |
| **동적 워크플로(Dynamic workflows)** | 동일한 풀 위에서 런타임에 다중 서브에이전트 오케스트레이션(병렬 + 파이프라인 단계)을 작성합니다. |
| **통합(Integration)** | 서브에이전트의 반환을 올바른 산출물로 융합합니다 — 통합된 답변만 채점됩니다. |

메인 에이전트는 벤치마크 간 비교 가능성을 위해 이름, 설명, 매개변수가 실제 하니스 관례를 반영하는 **CapitalCase** 도구를 제공받습니다:

| 도구 | 목적 |
|---|---|
| **Read** | 파일을 읽습니다. 모달리티를 벗어난 콘텐츠는 위임을 제안하는 텍스트 플레이스홀더로 강등됩니다. |
| **Write** | 워크스페이스에 파일을 생성하거나 덮어씁니다. |
| **Edit** | 기존 파일에 대상 지정 인플레이스 편집을 적용합니다. |
| **Bash** | 샌드박스에서 셸 명령을 실행합니다(`realpath` 검증 경로). |
| **Grep** | 패턴으로 파일 내용을 검색합니다. |
| **Glob** | 이름 패턴으로 파일을 찾습니다. |
| **CreateSubagent** | 서브에이전트를 정의합니다: 시스템 프롬프트, 모델 키, 도구 부분집합, 워크스페이스 경로 화이트리스트. |
| **RunSubagent** | 서브에이전트를 포그라운드 또는 백그라운드로, 신규 또는 이어진(재개된) 세션으로 호출합니다. |
| **ListSubagents** | 지금까지 생성된 서브에이전트와 그 상태를 나열합니다. |
| **InspectSubagent** | 서브에이전트의 구성, 부여된 권한, 실행 이력을 검사합니다. |
| **Workflow** | JS 스타일 오케스트레이션 DSL — `agent()`, `parallel()`, `pipeline()` — 으로 런타임에 다중 서브에이전트 실행을 구성합니다. |

시스템 수준 신호(환경, 토큰 임계값)는 `<system-reminder>` 블록을 통해 주입되며, 백그라운드 작업 완료는 `<task-notification>` 블록을 통해 도착합니다. 모든 경로 접근은 `realpath`로 검증되며, 심링크 탈출은 거부되고 금지 접근으로 집계됩니다.

### 고정 서브에이전트 풀 (통제 변수)

| 키 | 모델 | 서버 | 네이티브 모달리티 |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | local vLLM | text |
| `vlm`  | gemma-4-31b-it | local vLLM | text, image, video |
| `omni` | gemma-4-e4b-it | local vLLM | text, image, audio, video |

모든 메인 에이전트는 이 동일한 팀을 지휘합니다. 실행 간에 메인 에이전트만 달라집니다.

---

## 📊 데이터 및 평가

모든 시나리오는 워크스페이스, 일련의 사용자 질문, 그리고 정답 검증을 제공합니다. 일부 라운드 사이에는 워크스페이스가 **단계적 업데이트**(신규 또는 교체된 파일)를 받아 이후 답변을 변경시키며, 이는 일회성 해결책이 아니라 진화하는 작업에 대한 지속적 관리를 요구합니다.

<div align="center">
<img src="../../assets/heatmap.png" alt="시나리오별 SMS 히트맵: 12개 모델 x 41개 시나리오, 난이도는 균일하지 않고 모델별로 다름" width="820">
<br/>
<sub>시나리오 × 모델별 SMS 히트맵 — 난이도는 균일하지 않으며 모델별로 다릅니다.</sub>
</div>

**채점 구성요소** (모두 $[0,1]$ 범위, LLM 심판 없음):

| 지표 | 의미 |
|---|---|
| **TCR** — 작업 완료율(Task Completion Rate) | 사용자 질문에 대한 평균 통과율. |
| **TPP** — 도구 권한 정밀도(Tool-Permission Precision) | 서브에이전트당, 부여된 도구 유형 중 실제로 사용된 비율. |
| **ROC** — 읽기 전용 준수(Read-Only Compliance) | 서브에이전트당, 읽기 전용 서브에이전트에 변경 가능 도구가 부여되면 0, 그렇지 않으면 1. |
| **WPP** — 워크스페이스 권한 정밀도(Workspace-Permission Precision) | 서브에이전트당, 접근한 파일 ÷ 부여된 파일. |
| **MCA** — 모달리티 선택 정확도(Modality-Choice Accuracy) | 서브에이전트당, `vlm`이 실제로 이미지/비디오를 읽고 `omni`가 오디오를 읽는지 여부(`llm`은 1점). |

모든 시나리오는 **10가지 엄격한 설계 제약(C1–C10)** 을 충족합니다 — 읽을 수 없는 영역, 실질적인 단계적 업데이트, 전체 도구 표면 사용, 디코이를 포함한 8개 이상의 디렉터리, 비텍스트 모달리티 라운드, 병렬 필수 작업, 세션 재사용 쌍, 라운드 간 의존성, 모달리티 디코이, 기계 검증 가능한 답변 — 각각은 단일 LM이 우회할 수 있는 별개의 관리 실패 모드를 겨냥합니다.

### 데이터셋 구성

- **41개 시나리오 · 258개 라운드**, 그중 44개(17.1%)는 단계적 업데이트가 선행됩니다.
- **255개 파일에 걸친 72개 업데이트 그룹** (61.1% `new`, 38.9% `replace`, 그룹당 평균 3.54개 파일).
- **170.5 MiB · 28.9M 토큰** — 71.9%가 워크스페이스 콘텐츠, 27.9%가 단계적 업데이트.
- 모달리티 구성: 텍스트가 파일/토큰을 지배하는 반면 오디오와 이미지가 원시 바이트를 지배합니다 — 텍스트 전용 관리자가 직접 소비할 수 없는 상당한 비텍스트 페이로드입니다.

ClawArena-Team은 **수집된 것이 아니라 구축된** 것입니다: 워크스페이스 코퍼스, 멀티모달 자산, 정답, 실행 검증은 모두 동일한 버전 관리 스크립트로부터 **합성–검증 플라이휠(synthesis–verification flywheel)** 을 통해 절차적으로 합성되며, 이 플라이휠에서는 실제 베이스라인 서브에이전트 관리 실행이 최종 수용 게이트가 됩니다. 사실상 이 벤치마크는 그것이 측정하는 바로 그 역량에 의해 작성됩니다. 형식과 구축 방법론은 [`docs/dataset.md`](../../docs/dataset.md)와 논문 부록을 참고하세요.

더 세분화된 분포는 [`docs/data-stats/`](../../docs/data-stats/)를 참고하세요: 각 서브셋(`demo` / `wave1` / `wave3` / `wave4`)과 전체 세트는 `clawarena-team stats`로 생성된 자체 `STATS.md`와 차트(토큰 / 파일 크기 / 모달리티 분포, 태그 커버리지, ...)를 가집니다.

---

## 🔍 사례 연구

녹화된 실행 기록과 `metadata.json` 파일에서 직접 추출한 12개 사례 — 모든 수치와 인용 문자열은 그대로입니다 — 로 세 가지 발견과 관리 역량 표면을 구체적으로 뒷받침합니다.

<details>
<summary><b>사례 1–4: 가장 강력한 관리자에서의 과도한 권한 부여, 올바른 모달리티 라우팅, 모달리티 디코이 함정, 품질과 분리된 비용</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_1.png" alt="사례 연구 1-4" width="900">
</div>
</details>

<details>
<summary><b>사례 5–8: 금지 접근이 갈리는 동일 점수, 동적 워크플로 작성(및 크래시를 일으키는 팬아웃), 진정한 백그라운드 스케줄링 없는 논리적 병렬성, 그리고 진정한 백그라운드와 워크플로 병렬성</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_2.png" alt="사례 연구 5-8" width="900">
</div>
</details>

<details>
<summary><b>사례 9–12: 결코 전파되지 않는 보류 중인 수정, 관리자가 운용할 수 없는 역량 절벽, 관리 상한(병렬 팬아웃, 적응형 재시도, 최소 권한), 그리고 좋은 관리란 무엇인가</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_3.png" alt="사례 연구 9-12" width="900">
</div>
</details>

---

## 📖 문서

| 문서 | 설명 |
|----------|-------------|
| [CLI 레퍼런스](../../docs/cli.md) | 모든 명령, 플래그, `CATEAM_*` 환경 변수 |
| [데이터셋 형식](../../docs/dataset.md) | 시나리오 레이아웃, 라운드, 단계적 업데이트, 정답 검증 |
| [공급자 가이드](../../docs/provider.md) | 메인 에이전트 공급자 연동(OpenAI 호환, Gemini, OpenRouter, ...) |
| [실험 실행](../../docs/running-experiments.md) | 서브에이전트 풀 서빙 및 전체 스윕 실행 / 재개 |
| [리더보드 제출](../../docs/submit-to-leaderboard.md) | 실행을 패키징하여 [`submissions/`](../../submissions/)에 기여하기 |

---

## 🏗️ 프로젝트 구조

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

## 📚 인용

본 연구는 현재 익명 프리프린트 상태이며, arXiv 식별자와 저자 목록은 추후 추가될 예정입니다.

```bibtex
@misc{clawarena-team2026,
  title  = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author = {Anonymous Author(s)},
  year   = {2026},
  note   = {Preprint. arXiv identifier and author list to be added.}
}
```

---

## 📄 라이선스

이 프로젝트는 [MIT License](../../../LICENSE) 하에 라이선스가 부여됩니다.
