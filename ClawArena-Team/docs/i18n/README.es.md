<div align="center">

<h1>ClawArena-Team</h1>

### Evaluación comparativa de la orquestación de subagentes y los flujos de trabajo dinámicos en agentes de modelos de lenguaje

<p>
  <a href="../../README.md">English</a> •
  <a href="README.zh-Hans.md">简体中文</a> •
  <a href="README.zh-Hant.md">繁體中文</a> •
  <a href="README.ja.md">日本語</a> •
  <a href="README.ko.md">한국어</a> •
  <a href="README.fr.md">Français</a> •
  <a href="README.de.md">Deutsch</a> •
  <b>Español</b> •
  <a href="README.pt.md">Português</a> •
  <a href="README.ru.md">Русский</a>
</p>

<p>
  <a href="#-citación"><img src="https://img.shields.io/badge/Paper-Preprint-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="Paper" /></a>
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

[🔭 Visión general](#-visión-general) • [📈 Clasificación](#-clasificación) • [🔑 Hallazgos clave](#-hallazgos-clave) • [🚀 Inicio rápido](#-inicio-rápido) • [🧰 Superficie de capacidades y herramientas](#-superficie-de-capacidades-y-herramientas) • [📊 Datos y evaluación](#-datos-y-evaluación) • [🔍 Casos de estudio](#-casos-de-estudio) • [📖 Documentación](#-documentación) • [🏗️ Estructura del proyecto](#️-estructura-del-proyecto) • [📚 Citación](#-citación) • [📄 Licencia](#-licencia)

</div>

---

## 🔭 Visión general

Los agentes de modelos de lenguaje se despliegan cada vez más como **gestores**: un modelo principal crea subagentes especializados, delega trabajo y orquesta sus retornos paralelos y asíncronos mediante flujos de trabajo dinámicos. Las evaluaciones comparativas existentes puntúan la resolución de tareas de la propia política o un sistema multiagente fijo, pero ninguna aísla la **capacidad de gestión** del único modelo de lenguaje que actúa como líder.

**ClawArena-Team** (la variante de gestión de equipos de la serie ClawArena) aísla exactamente esto. Un **agente principal solo de texto** debe completar tareas multironda, multimodales y multidirectorio que no puede realizar por sí solo, creando, empoderando, planificando e integrando subagentes de un **conjunto fijo servido localmente**. Cada gestor comanda a los mismos trabajadores, de modo que las diferencias de puntuación reflejan *habilidad de gestión, no capacidad bruta*.

- **41 escenarios · 258 rondas de evaluación · 72 actualizaciones por etapas**, abarcando **derecho, medicina, ingeniería, negocios y ciencia**.
- **Agente principal solo de texto, parcialmente visible**: percibe de forma nativa únicamente texto y alcanza solo una parte del espacio de trabajo, por lo que la delegación es obligatoria.
- **Conjunto fijo de subagentes** servido localmente mediante vLLM (`llm`/`vlm`/`omni`), mantenido idéntico para todos los gestores evaluados.
- **Puntuación basada en ejecución, sin juez de modelo de lenguaje**: cada ronda incluye un comando de shell cuyo código de salida (con coincidencia de salida opcional) decide el aprobado/suspenso.

---

## 📈 Clasificación

Clasificamos los modelos del agente principal por la puntuación compuesta **Subagent-Management Score (SMS)**, que multiplica la corrección de la tarea por un factor de gestión de privilegio mínimo y enrutamiento por modalidad:

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS ≤ TCR siempre:** la gestión solo puede descontar la corrección de la tarea, nunca inflarla. Un modelo que gestiona a la perfección pero falla la tarea obtiene cero.

| Modelo | TCR | TPP | ROC | WPP | MCA | **SMS** | Coste ($) | Rondas |
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

<sub>Todos los valores en %, doce modelos × 41 escenarios en una única ejecución de evaluación, ordenados por **SMS**. El recién lanzado `glm-5.2` (a través de la API oficial de z.ai) es el gestor de pesos abiertos más potente — SMS 50.4, 4.º en general — superando a `kimi-k2.6` para encabezar los modelos de pesos abiertos. La **negrita** marca el mejor valor de la columna (el mejor de cada columna se resalta de forma independiente). Coste ($): coste de la API del agente principal por ejecución a las tarifas de lista del proveedor / OpenRouter — cuanto más bajo, mejor, por lo que se deja sin negrita; los subagentes se ejecutan en el conjunto local fijo y no tienen coste asignado. Rondas: rondas aprobadas de 258. `claude-fable-5` se evalúa tal como se entrega, con un repliegue de rechazo recomendado por el proveedor → `claude-opus-4-8`.</sub>

> 📥 ¿Quieres enviar un resultado? Consulta [docs/submit-to-leaderboard.md](../../docs/submit-to-leaderboard.md). Las ejecuciones de ejemplo y los resultados contribuidos están en [`submissions/`](../../submissions/).

---

## 🔑 Hallazgos clave

A lo largo de doce modelos de agente principal propietarios, alojados por la comunidad y autoalojados, emergen tres hallazgos.

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ El cuello de botella es la *concesión de privilegios*, no la percepción

Los dos ejes "fáciles" están casi saturados — cumplimiento de solo lectura (ROC ≥ 92%) y precisión de elección de modalidad (MCA ≥ 92%) para todo modelo capaz. Los ejes discriminantes son las métricas de precisión de privilegios: la **Workspace-Permission Precision (WPP) *nunca* alcanza el 50%** para ningún modelo. A los subagentes se les conceden de forma rutinaria aproximadamente el doble de archivos de los que realmente tocan.

</td>
<td width="33%" valign="top">

### 2️⃣ El coste y la calidad de gestión están *desacoplados*

El coste de la API del agente principal abarca **más de 100×** (\$0.8 → \$93 por ejecución) mientras que el SMS abarca **menos de 4×**. Los modelos abiertos más baratos se sitúan en la frontera de Pareto — `deepseek-v4-pro` alcanza un SMS de 46.4 por tan solo \$1.7 — mientras que varios modelos de alto coste (`gpt-5.5`, `sonnet-4-6`, `kimi-k2.6`) son *dominados* por `gemini-3.5-flash`, de coste medio. El `glm-5.2` de pesos abiertos ($22.9) también aterriza en la frontera como el modelo abierto más potente.

</td>
<td width="33%" valign="top">

### 3️⃣ Las puntuaciones se agrupan, los comportamientos divergen

Por debajo del modelo insignia, diez modelos se agrupan dentro de una **banda de SMS de 9.9 puntos** (43.9–53.8), pero sus comportamientos de orquestación difieren en **más de un orden de magnitud**. La tasa de acceso prohibido por subagente varía de 0.48 a 5.78 entre los modelos capaces (~12×), y el uso de flujos de trabajo dinámicos varía de 8 a 112 invocaciones.

</td>
</tr>
</table>

<div align="center">

| Coste vs. gestión (Hallazgo 2) | Violaciones de permisos (Hallazgo 3) |
|:---:|:---:|
| <img src="../../assets/pareto.png" alt="SMS vs. coste de la API del agente principal, escala logarítmica; modelos abiertos baratos en la frontera de Pareto" width="430"> | <img src="../../assets/forbidden.png" alt="Recuentos de acceso prohibido por modelo MAF/SAFt/SAFa en escala logarítmica; SAFa diverge ~12x" width="430"> |

</div>

**Enrutamiento por modalidad.** Los gestores recurren de forma abrumadora por defecto a la clave `llm` y crean comparativamente pocos especialistas `vlm`/`omni`; cuando *sí* enrutan por modalidad lo hacen correctamente (de ahí el alto MCA), pero infrautilizan a los trabajadores multimodales.

<div align="center">
<img src="../../assets/modality.png" alt="Distribución de claves de modelo de subagentes: los gestores recurren por defecto a la clave llm e infrautilizan vlm/omni" width="780">
</div>

---

## 🚀 Inicio rápido

Consulta [`docs/running-experiments.md`](../../docs/running-experiments.md) para el recorrido completo (servir el conjunto, elegir objetivos, reanudar ejecuciones).

### 1. Instalación

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

Esto instala la CLI `clawarena-team` (alias cortos: **`cateam`** / **`ca-team`**). El tokenizador y la plantilla de chat están **incluidos en `helper/`**: no se requiere ningún paso de descarga.

### 2. Servir el conjunto fijo de subagentes (vLLM local)

El conjunto de subagentes se mantiene idéntico para cada agente principal evaluado, de modo que la gestión es la única variable:

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. Validar, ejecutar y analizar

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

> Los alias cortos `cateam` y `ca-team` son intercambiables con `clawarena-team` en todas partes (p. ej. `cateam run ...`).

<details>
<summary><b>El JSON de <code>--model</code></b></summary>

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

La misma cadena puede suministrarse mediante `CATEAM_MODEL_JSON`. El campo `main.modalities` decide qué percibe de forma nativa el agente principal; `Read` degrada los archivos fuera de modalidad a un marcador de posición textual y sugiere la delegación. Consulta [`docs/cli.md`](../../docs/cli.md) para todos los indicadores y las variables `CATEAM_*`, [`docs/dataset.md`](../../docs/dataset.md) para el formato del conjunto de datos y [`docs/provider.md`](../../docs/provider.md) para conectar un proveedor.
</details>

---

## 🧰 Superficie de capacidades y herramientas

ClawArena-Team enmarca la gestión de subagentes como un **problema principal-agente**. La superficie de capacidades del agente principal se descompone en seis operaciones concretas, cada una forzada por el diseño del escenario:

| Operación | Qué requiere |
|---|---|
| **Creación** | Crear un subagente con un prompt de sistema, una clave de modelo, un subconjunto de herramientas y una lista blanca de rutas del espacio de trabajo (un subconjunto de las suyas propias). |
| **Enrutamiento por modalidad** | Enrutar imágenes/vídeo a un `vlm` y audio a un `omni`, ya que el gestor solo percibe texto. |
| **Empoderamiento de privilegio mínimo** | Conceder únicamente las herramientas y rutas que un subagente realmente necesita; conceder de más es derrochador e inseguro. |
| **Planificación** | Ejecutar subagentes en primer o segundo plano, como sesiones nuevas o continuadas (reanudadas), y en paralelo; las tareas en segundo plano notifican al gestor al completarse. |
| **Flujos de trabajo dinámicos** | Crear orquestación multisubagente (etapas en paralelo + tubería) en tiempo de ejecución sobre el mismo conjunto. |
| **Integración** | Fusionar los retornos de los subagentes en un entregable correcto: solo se puntúa la respuesta integrada. |

Al agente principal se le exponen herramientas en **CapitalCase** cuyos nombres, descripciones y parámetros reflejan las convenciones de arneses reales para la comparabilidad entre evaluaciones:

| Herramienta | Propósito |
|---|---|
| **Read** | Leer un archivo; el contenido fuera de modalidad se degrada a un marcador de posición textual que sugiere la delegación. |
| **Write** | Crear o sobrescribir un archivo en el espacio de trabajo. |
| **Edit** | Aplicar una edición específica en el lugar a un archivo existente. |
| **Bash** | Ejecutar un comando de shell en el entorno aislado (rutas verificadas con `realpath`). |
| **Grep** | Buscar contenidos de archivos por patrón. |
| **Glob** | Encontrar archivos por patrón de nombre. |
| **CreateSubagent** | Definir un subagente: prompt de sistema, clave de modelo, subconjunto de herramientas y lista blanca de rutas del espacio de trabajo. |
| **RunSubagent** | Invocar un subagente en primer o segundo plano, como una sesión nueva o continuada (reanudada). |
| **ListSubagents** | Listar los subagentes creados hasta ahora y su estado. |
| **InspectSubagent** | Inspeccionar la configuración de un subagente, los privilegios concedidos y el historial de ejecución. |
| **Workflow** | DSL de orquestación al estilo de JS — `agent()`, `parallel()`, `pipeline()` — para componer ejecuciones multisubagente en tiempo de ejecución. |

Las señales a nivel de sistema (entorno, umbrales de tokens) se inyectan mediante bloques `<system-reminder>`; las finalizaciones de tareas en segundo plano llegan mediante bloques `<task-notification>`. Todo acceso a rutas se verifica con `realpath` y los escapes mediante enlaces simbólicos se rechazan y se contabilizan como accesos prohibidos.

### Conjunto fijo de subagentes (la variable controlada)

| Clave | Modelo | Servidor | Modalidades nativas |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | vLLM local | text |
| `vlm`  | gemma-4-31b-it | vLLM local | text, image, video |
| `omni` | gemma-4-e4b-it | vLLM local | text, image, audio, video |

Cada agente principal comanda este mismo equipo; solo el agente principal varía entre ejecuciones.

---

## 📊 Datos y evaluación

Cada escenario proporciona un espacio de trabajo, una secuencia de preguntas del usuario y comprobaciones de verdad fundamental. Entre algunas rondas, el espacio de trabajo recibe **actualizaciones por etapas** (archivos nuevos o reemplazados) que cambian las respuestas posteriores, requiriendo una gestión sostenida de una tarea en evolución en lugar de una solución de una sola vez.

<div align="center">
<img src="../../assets/heatmap.png" alt="Mapa de calor de SMS por escenario: 12 modelos x 41 escenarios, la dificultad es desigual y específica del modelo" width="820">
<br/>
<sub>Mapa de calor de SMS por escenario × modelo — la dificultad es desigual y específica del modelo.</sub>
</div>

**Componentes de puntuación** (todos en $[0,1]$, sin juez de modelo de lenguaje):

| Métrica | Significado |
|---|---|
| **TCR** — Task Completion Rate | Tasa media de aprobados sobre las preguntas del usuario. |
| **TPP** — Tool-Permission Precision | Por subagente, fracción de los tipos de herramienta concedidos que realmente se usan. |
| **ROC** — Read-Only Compliance | Por subagente, 0 si a un subagente de solo lectura se le concedió una herramienta de mutación, de lo contrario 1. |
| **WPP** — Workspace-Permission Precision | Por subagente, archivos accedidos ÷ archivos concedidos. |
| **MCA** — Modality-Choice Accuracy | Por subagente, si un `vlm` realmente lee imagen/vídeo y un `omni` lee audio (`llm` puntúa 1). |

Cada escenario satisface **diez restricciones de diseño exigentes (C1–C10)** — regiones ilegibles, actualizaciones por etapas sustanciales, uso completo de la superficie de herramientas, ≥8 directorios con señuelos, rondas de modalidad no textual, tareas que requieren paralelismo, pares de reutilización de sesión, dependencias entre rondas, señuelos de modalidad y respuestas verificables por máquina — cada una orientada a un modo de fallo de gestión distinto que de otro modo un único modelo de lenguaje podría sortear.

### Composición del conjunto de datos

- **41 escenarios · 258 rondas**, de las cuales 44 (17.1%) van precedidas de actualizaciones por etapas.
- **72 grupos de actualización sobre 255 archivos** (61.1% `new`, 38.9% `replace`, media de 3.54 archivos/grupo).
- **170.5 MiB · 28.9 M tokens** — 71.9% contenido del espacio de trabajo, 27.9% actualizaciones por etapas.
- Mezcla de modalidades: el texto domina los archivos/tokens, mientras que el audio y la imagen dominan los bytes brutos — una carga útil no textual sustancial que un gestor solo de texto no puede consumir directamente.

ClawArena-Team está **construido, no recopilado**: los corpus del espacio de trabajo, los recursos multimodales, la verdad fundamental y las comprobaciones de ejecución se sintetizan todos procedimentalmente a partir de los mismos scripts versionados mediante un **volante de síntesis-verificación** en el que una ejecución real de referencia de gestión de subagentes es la puerta de aceptación final. La evaluación está, en efecto, creada por la misma capacidad que mide. Consulta [`docs/dataset.md`](../../docs/dataset.md) y el apéndice del artículo para el formato y la metodología de construcción.

Para distribuciones de grano más fino, consulta [`docs/data-stats/`](../../docs/data-stats/): cada subconjunto (`demo` / `wave1` / `wave3` / `wave4`) y el conjunto completo tiene su propio `STATS.md` más gráficos (distribución de tokens / tamaño de archivo / modalidad, cobertura de etiquetas, ...), generados por `clawarena-team stats`.

---

## 🔍 Casos de estudio

Doce casos extraídos directamente de las transcripciones de ejecuciones registradas y de los archivos `metadata.json` — todos los números y cadenas citadas verbatim — que fundamentan de forma concreta los tres hallazgos y la superficie de capacidades de gestión.

<details>
<summary><b>Casos 1–4: concesión excesiva bajo el gestor más potente, enrutamiento de modalidad correcto, la trampa del señuelo de modalidad y el coste desacoplado de la calidad</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_1.png" alt="Casos de estudio 1-4" width="900">
</div>
</details>

<details>
<summary><b>Casos 5–8: puntuaciones idénticas con accesos prohibidos divergentes, creación de un flujo de trabajo dinámico (y un fan-out que falla), paralelismo lógico sin verdadera planificación en segundo plano, y verdadero segundo plano más paralelismo de flujo de trabajo</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_2.png" alt="Casos de estudio 5-8" width="900">
</div>
</details>

<details>
<summary><b>Casos 9–12: una corrección pendiente que nunca se propaga, un precipicio de capacidad que el gestor no puede operar, el techo de gestión (fan-out paralelo, reintento adaptativo, privilegio mínimo) y cómo es una buena gestión</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_3.png" alt="Casos de estudio 9-12" width="900">
</div>
</details>

---

## 📖 Documentación

| Documento | Descripción |
|----------|-------------|
| [Referencia de la CLI](../../docs/cli.md) | Todos los comandos, indicadores y variables de entorno `CATEAM_*` |
| [Formato del conjunto de datos](../../docs/dataset.md) | Disposición de escenarios, rondas, actualizaciones por etapas, comprobaciones de verdad fundamental |
| [Guía de proveedores](../../docs/provider.md) | Conexión de proveedores de agente principal (OpenAI-compat, Gemini, OpenRouter, ...) |
| [Ejecución de experimentos](../../docs/running-experiments.md) | Servir el conjunto de subagentes y ejecutar / reanudar un barrido completo |
| [Enviar a la clasificación](../../docs/submit-to-leaderboard.md) | Empaquetar una ejecución y contribuirla a [`submissions/`](../../submissions/) |

---

## 🏗️ Estructura del proyecto

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

## 📚 Citación

Este trabajo es actualmente un preprint anónimo; el identificador de arXiv y la lista de autores se añadirán más adelante.

```bibtex
@misc{clawarena-team2026,
  title  = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author = {Anonymous Author(s)},
  year   = {2026},
  note   = {Preprint. arXiv identifier and author list to be added.}
}
```

---

## 📄 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](../../../LICENSE).
