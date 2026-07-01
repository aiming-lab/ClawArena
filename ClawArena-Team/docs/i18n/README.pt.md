<div align="center">

<h1>ClawArena-Team</h1>

### Avaliação de Orquestração de Subagentes e Fluxos de Trabalho Dinâmicos em Agentes de Modelos de Linguagem

<p>
  <a href="../../README.md">English</a> •
  <a href="README.zh-Hans.md">简体中文</a> •
  <a href="README.zh-Hant.md">繁體中文</a> •
  <a href="README.ja.md">日本語</a> •
  <a href="README.ko.md">한국어</a> •
  <a href="README.fr.md">Français</a> •
  <a href="README.de.md">Deutsch</a> •
  <a href="README.es.md">Español</a> •
  <b>Português</b> •
  <a href="README.ru.md">Русский</a>
</p>

<p>
  <a href="#-citação"><img src="https://img.shields.io/badge/Paper-Preprint-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="Artigo" /></a>
  <a href="../../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="Licença MIT" /></a>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Version-v1.0.0-blueviolet?style=flat&labelColor=555" alt="v1.0.0" />
</p>
<p>
  <img src="https://img.shields.io/badge/Scenarios-41-orange?style=flat&labelColor=555" alt="41 Cenários" />
  <img src="https://img.shields.io/badge/Rounds-258-red?style=flat&labelColor=555" alt="258 Rodadas" />
  <img src="https://img.shields.io/badge/Staged%20Updates-72-yellow?style=flat&labelColor=555" alt="72 Atualizações Encenadas" />
  <img src="https://img.shields.io/badge/Models-12-9cf?style=flat&labelColor=555" alt="12 Modelos" />
  <img src="https://img.shields.io/badge/Scoring-Execution--based-success?style=flat&labelColor=555" alt="Baseado em Execução" />
</p>

<img src="../../assets/hero.png" alt="ClawArena-Team" width="900">

[🔭 Visão Geral](#-visão-geral) • [📈 Placar](#-placar) • [🔑 Principais Descobertas](#-principais-descobertas) • [🚀 Início Rápido](#-início-rápido) • [🧰 Superfície de Capacidades e Ferramentas](#-superfície-de-capacidades-e-ferramentas) • [📊 Dados e Avaliação](#-dados-e-avaliação) • [🔍 Estudos de Caso](#-estudos-de-caso) • [📖 Documentação](#-documentação) • [🏗️ Estrutura do Projeto](#️-estrutura-do-projeto) • [📚 Citação](#-citação) • [📄 Licença](#-licença)

</div>

---

## 🔭 Visão Geral

Agentes de LM são cada vez mais implantados como **gerentes** — um modelo principal cria subagentes especializados, delega trabalho e orquestra seus retornos paralelos e assíncronos por meio de fluxos de trabalho dinâmicos. Os benchmarks existentes pontuam a resolução de tarefas da própria política ou um sistema multiagente fixo, mas nenhum isola a **capacidade de gestão** do único LM que atua como líder.

**ClawArena-Team** (a variante de gestão de equipe da série ClawArena) isola exatamente isso. Um **agente principal somente de texto** deve concluir tarefas multietapa, multimodais e de múltiplos diretórios que não consegue realizar sozinho, criando, empoderando, agendando e integrando subagentes de um **pool fixo, servido localmente**. Todo gerente comanda os mesmos trabalhadores, de modo que as diferenças de pontuação refletem *habilidade de gestão, não capacidade bruta*.

- **41 cenários · 258 rodadas de avaliação · 72 atualizações encenadas**, abrangendo **direito, medicina, engenharia, negócios e ciência**.
- **Agente principal somente de texto, parcialmente visível** — ele percebe nativamente apenas texto e alcança apenas parte do espaço de trabalho, então a delegação é obrigatória.
- **Pool fixo de subagentes** servido localmente via vLLM (`llm`/`vlm`/`omni`), mantido idêntico em todos os gerentes avaliados.
- **Pontuação baseada em execução, sem juiz LLM** — cada rodada inclui um comando de shell cujo código de saída (com correspondência de saída opcional) decide aprovação/reprovação.

---

## 📈 Placar

Classificamos os modelos de agente principal pelo **Subagent-Management Score (SMS)** composto, que multiplica a correção da tarefa por um fator de gestão de privilégio mínimo e roteamento de modalidade:

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS ≤ TCR sempre:** a gestão só pode descontar a correção da tarefa, nunca inflá-la. Um modelo que gerencia perfeitamente, mas falha na tarefa, pontua zero.

| Modelo | TCR | TPP | ROC | WPP | MCA | **SMS** | Custo ($) | Rodadas |
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

<sub>Todos os valores em %, doze modelos × 41 cenários em uma única execução de avaliação, ordenados por **SMS**. O recém-lançado `glm-5.2` (via a API oficial da z.ai) é o gerente de peso aberto mais forte — SMS 50.4, 4º no geral — superando `kimi-k2.6` para liderar os modelos de peso aberto. O **negrito** marca o melhor valor da coluna (o melhor de cada coluna é destacado independentemente). Custo ($): custo de API do agente principal por execução às tarifas de tabela do provedor / OpenRouter — menor é melhor, portanto não está em negrito; os subagentes rodam no pool local fixo e não têm preço. Rodadas: rodadas aprovadas de 258. `claude-fable-5` é avaliado tal como distribuído, com um fallback recomendado pelo fornecedor de recusa → `claude-opus-4-8`.</sub>

> 📥 Enviar um resultado? Consulte [docs/submit-to-leaderboard.md](../../docs/submit-to-leaderboard.md). Execuções de exemplo e resultados contribuídos ficam em [`submissions/`](../../submissions/).

---

## 🔑 Principais Descobertas

Entre doze modelos de agente principal proprietários, hospedados pela comunidade e auto-hospedados, surgem três descobertas.

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ O gargalo é a *concessão de privilégios*, não a percepção

Os dois eixos "fáceis" estão quase saturados — conformidade somente leitura (ROC ≥ 92%) e precisão de escolha de modalidade (MCA ≥ 92%) para todo modelo capaz. Os eixos discriminantes são as métricas de precisão de privilégio: a **Workspace-Permission Precision (WPP) *nunca* atinge 50%** para nenhum modelo. Rotineiramente, os subagentes recebem cerca de duas vezes os arquivos que realmente acessam.

</td>
<td width="33%" valign="top">

### 2️⃣ Custo e qualidade de gestão estão *desacoplados*

O custo de API do agente principal varia **mais de 100×** (\$0.8 → \$93 por execução), enquanto o SMS varia **menos de 4×**. Os modelos abertos mais baratos ficam na fronteira de Pareto — `deepseek-v4-pro` atinge SMS 46.4 por apenas \$1.7 — enquanto vários modelos de alto custo (`gpt-5.5`, `sonnet-4-6`, `kimi-k2.6`) são *dominados* pelo `gemini-3.5-flash` de custo médio. O `glm-5.2` de peso aberto ($22.9) também chega à fronteira como o modelo aberto mais forte.

</td>
<td width="33%" valign="top">

### 3️⃣ As pontuações se agrupam, os comportamentos divergem

Abaixo do modelo principal, dez modelos se agrupam em uma **faixa de SMS de 9,9 pontos** (43.9–53.8), mas seus comportamentos de orquestração diferem em **mais de uma ordem de magnitude**. A taxa de acesso proibido por subagente varia de 0.48 a 5.78 entre os modelos capazes (~12×), e o uso de fluxo de trabalho dinâmico varia de 8 a 112 invocações.

</td>
</tr>
</table>

<div align="center">

| Custo vs. gestão (Descoberta 2) | Violações de permissão (Descoberta 3) |
|:---:|:---:|
| <img src="../../assets/pareto.png" alt="SMS vs. custo de API do agente principal, escala logarítmica; modelos abertos baratos na fronteira de Pareto" width="430"> | <img src="../../assets/forbidden.png" alt="Contagens de acesso proibido por modelo MAF/SAFt/SAFa em escala logarítmica; SAFa diverge ~12x" width="430"> |

</div>

**Roteamento de modalidade.** Os gerentes recorrem majoritariamente à chave `llm` e criam comparativamente poucos especialistas `vlm`/`omni`; quando *de fato* roteiam por modalidade, fazem-no corretamente (daí o alto MCA), mas subutilizam os trabalhadores multimodais.

<div align="center">
<img src="../../assets/modality.png" alt="Distribuição de chave de modelo dos subagentes: os gerentes recorrem à chave llm e subutilizam vlm/omni" width="780">
</div>

---

## 🚀 Início Rápido

Consulte [`docs/running-experiments.md`](../../docs/running-experiments.md) para o passo a passo completo (servir o pool, escolher alvos, retomar execuções).

### 1. Instalação

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

Isso instala a CLI `clawarena-team` (aliases curtos: **`cateam`** / **`ca-team`**). O tokenizador e o template de chat estão **incluídos em `helper/`** — nenhuma etapa de download é necessária.

### 2. Servir o pool fixo de subagentes (vLLM local)

O pool de subagentes é mantido idêntico em todos os agentes principais avaliados, de modo que a gestão é a única variável:

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. Validar, executar e analisar

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

> Os aliases curtos `cateam` e `ca-team` são intercambiáveis com `clawarena-team` em todos os lugares (ex.: `cateam run ...`).

<details>
<summary><b>O JSON <code>--model</code></b></summary>

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

A mesma string pode ser fornecida via `CATEAM_MODEL_JSON`. O campo `main.modalities` decide o que o agente principal percebe nativamente; `Read` rebaixa arquivos fora de modalidade para um marcador de posição textual e sugere delegação. Consulte [`docs/cli.md`](../../docs/cli.md) para todas as flags e variáveis `CATEAM_*`, [`docs/dataset.md`](../../docs/dataset.md) para o formato do conjunto de dados e [`docs/provider.md`](../../docs/provider.md) para configurar um provedor.
</details>

---

## 🧰 Superfície de Capacidades e Ferramentas

O ClawArena-Team enquadra a gestão de subagentes como um **problema principal–agente**. A superfície de capacidades do agente principal decompõe-se em seis operações concretas, cada uma imposta pelo design do cenário:

| Operação | O que exige |
|---|---|
| **Criação** | Criar um subagente com um prompt de sistema, uma chave de modelo, um subconjunto de ferramentas e uma lista de permissões de caminhos do espaço de trabalho (um subconjunto do seu próprio). |
| **Roteamento de modalidade** | Rotear imagens/vídeo para um `vlm` e áudio para um `omni`, já que o gerente percebe apenas texto. |
| **Empoderamento de privilégio mínimo** | Conceder apenas as ferramentas e caminhos que um subagente realmente precisa; conceder em excesso é um desperdício e inseguro. |
| **Agendamento** | Executar subagentes em primeiro ou segundo plano, como sessões novas ou continuadas (retomadas), e em paralelo; tarefas em segundo plano notificam o gerente ao concluir. |
| **Fluxos de trabalho dinâmicos** | Criar orquestração de múltiplos subagentes (estágios paralelos + pipeline) em tempo de execução sobre o mesmo pool. |
| **Integração** | Fundir os retornos dos subagentes em um entregável correto — apenas a resposta integrada é pontuada. |

O agente principal recebe ferramentas em **CapitalCase** cujos nomes, descrições e parâmetros espelham convenções reais de harness para comparabilidade entre benchmarks:

| Ferramenta | Finalidade |
|---|---|
| **Read** | Lê um arquivo; conteúdo fora de modalidade é rebaixado a um marcador de posição textual que sugere delegação. |
| **Write** | Cria ou sobrescreve um arquivo no espaço de trabalho. |
| **Edit** | Aplica uma edição direcionada in loco a um arquivo existente. |
| **Bash** | Executa um comando de shell no sandbox (caminhos verificados com `realpath`). |
| **Grep** | Pesquisa o conteúdo de arquivos por padrão. |
| **Glob** | Encontra arquivos por padrão de nome. |
| **CreateSubagent** | Define um subagente: prompt de sistema, chave de modelo, subconjunto de ferramentas e lista de permissões de caminhos do espaço de trabalho. |
| **RunSubagent** | Invoca um subagente em primeiro ou segundo plano, como uma sessão nova ou continuada (retomada). |
| **ListSubagents** | Lista os subagentes criados até o momento e seu status. |
| **InspectSubagent** | Inspeciona a configuração de um subagente, os privilégios concedidos e o histórico de execução. |
| **Workflow** | DSL de orquestração estilo JS — `agent()`, `parallel()`, `pipeline()` — para compor execuções de múltiplos subagentes em tempo de execução. |

Sinais de nível de sistema (ambiente, limites de tokens) são injetados via blocos `<system-reminder>`; conclusões de tarefas em segundo plano chegam via blocos `<task-notification>`. Todo acesso a caminho é verificado com `realpath` e escapes por symlink são rejeitados e contabilizados como acessos proibidos.

### Pool fixo de subagentes (a variável controlada)

| Chave | Modelo | Servidor | Modalidades nativas |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | local vLLM | texto |
| `vlm`  | gemma-4-31b-it | local vLLM | texto, imagem, vídeo |
| `omni` | gemma-4-e4b-it | local vLLM | texto, imagem, áudio, vídeo |

Todo agente principal comanda esta mesma equipe; apenas o agente principal varia entre as execuções.

---

## 📊 Dados e Avaliação

Cada cenário fornece um espaço de trabalho, uma sequência de perguntas do usuário e verificações de ground-truth. Entre algumas rodadas, o espaço de trabalho recebe **atualizações encenadas** (arquivos novos ou substituídos) que alteram as respostas subsequentes, exigindo uma gestão sustentada de uma tarefa em evolução em vez de uma solução única.

<div align="center">
<img src="../../assets/heatmap.png" alt="Mapa de calor de SMS por cenário: 12 modelos x 41 cenários, a dificuldade é irregular e específica de cada modelo" width="820">
<br/>
<sub>Mapa de calor de SMS por cenário × modelo — a dificuldade é irregular e específica de cada modelo.</sub>
</div>

**Componentes de pontuação** (todos em $[0,1]$, sem juiz LLM):

| Métrica | Significado |
|---|---|
| **TCR** — Taxa de Conclusão de Tarefas | Taxa média de aprovação nas perguntas do usuário. |
| **TPP** — Precisão de Permissão de Ferramentas | Por subagente, fração dos tipos de ferramenta concedidos que são de fato usados. |
| **ROC** — Conformidade Somente Leitura | Por subagente, 0 se um subagente somente leitura recebeu uma ferramenta mutadora, caso contrário 1. |
| **WPP** — Precisão de Permissão do Espaço de Trabalho | Por subagente, arquivos acessados ÷ arquivos concedidos. |
| **MCA** — Precisão de Escolha de Modalidade | Por subagente, se um `vlm` de fato lê imagem/vídeo e um `omni` lê áudio (`llm` pontua 1). |

Cada cenário satisfaz **dez restrições rígidas de design (C1–C10)** — regiões ilegíveis, atualizações encenadas substanciais, uso completo da superfície de ferramentas, ≥8 diretórios com chamarizes, rodadas de modalidade não textual, tarefas que exigem paralelismo, pares de reuso de sessão, dependências entre rodadas, chamarizes de modalidade e respostas verificáveis por máquina — cada uma visando um modo distinto de falha de gestão que um único LM poderia, de outra forma, contornar.

### Composição do conjunto de dados

- **41 cenários · 258 rodadas**, das quais 44 (17,1%) são precedidas por atualizações encenadas.
- **72 grupos de atualização sobre 255 arquivos** (61,1% `new`, 38,9% `replace`, média de 3,54 arquivos/grupo).
- **170,5 MiB · 28,9 M tokens** — 71,9% conteúdo do espaço de trabalho, 27,9% atualizações encenadas.
- Mistura de modalidades: o texto domina arquivos/tokens, enquanto áudio e imagem dominam os bytes brutos — uma carga não textual substancial que um gerente somente de texto não consegue consumir diretamente.

O ClawArena-Team é **construído, não coletado**: corpora de espaço de trabalho, ativos multimodais, ground truth e verificações de execução são todos sintetizados proceduralmente a partir dos mesmos scripts versionados por meio de um **flywheel de síntese–verificação** no qual uma execução real de gestão de subagentes de referência é o portão de aceitação final. O benchmark é, com efeito, criado pela própria capacidade que mede. Consulte [`docs/dataset.md`](../../docs/dataset.md) e o apêndice do artigo para o formato e a metodologia de construção.

Para distribuições mais granulares, consulte [`docs/data-stats/`](../../docs/data-stats/): cada subconjunto (`demo` / `wave1` / `wave3` / `wave4`) e o conjunto completo têm seu próprio `STATS.md` mais gráficos (distribuição de tokens / tamanho de arquivo / modalidade, cobertura de tags, ...), gerados por `clawarena-team stats`.

---

## 🔍 Estudos de Caso

Doze casos extraídos diretamente de transcrições de execução registradas e arquivos `metadata.json` — todos os números e strings citadas literais — fundamentando concretamente as três descobertas e a superfície de capacidades de gestão.

<details>
<summary><b>Casos 1–4: concessão excessiva sob o gerente mais forte, roteamento correto de modalidade, a armadilha do chamariz de modalidade e o custo desacoplado da qualidade</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_1.png" alt="Estudos de caso 1-4" width="900">
</div>
</details>

<details>
<summary><b>Casos 5–8: pontuações idênticas com acesso proibido divergente, criação de um fluxo de trabalho dinâmico (e um fan-out que trava), paralelismo lógico sem agendamento real em segundo plano, e segundo plano real mais paralelismo de fluxo de trabalho</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_2.png" alt="Estudos de caso 5-8" width="900">
</div>
</details>

<details>
<summary><b>Casos 9–12: uma correção pendente que nunca se propaga, um precipício de capacidade que o gerente não consegue operar, o teto de gestão (fan-out paralelo, retentativa adaptativa, privilégio mínimo) e como é uma boa gestão</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_3.png" alt="Estudos de caso 9-12" width="900">
</div>
</details>

---

## 📖 Documentação

| Documento | Descrição |
|----------|-------------|
| [Referência da CLI](../../docs/cli.md) | Todos os comandos, flags e variáveis de ambiente `CATEAM_*` |
| [Formato do Conjunto de Dados](../../docs/dataset.md) | Layout do cenário, rodadas, atualizações encenadas, verificações de ground-truth |
| [Guia de Provedores](../../docs/provider.md) | Configuração de provedores de agente principal (OpenAI-compat, Gemini, OpenRouter, ...) |
| [Executando Experimentos](../../docs/running-experiments.md) | Servir o pool de subagentes e executar / retomar uma varredura completa |
| [Enviar para o Placar](../../docs/submit-to-leaderboard.md) | Empacotar uma execução e contribuí-la para [`submissions/`](../../submissions/) |

---

## 🏗️ Estrutura do Projeto

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

## 📚 Citação

Este trabalho é atualmente um preprint anônimo; o identificador arXiv e a lista de autores serão adicionados.

```bibtex
@misc{clawarena-team2026,
  title  = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author = {Anonymous Author(s)},
  year   = {2026},
  note   = {Preprint. arXiv identifier and author list to be added.}
}
```

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](../../../LICENSE).
