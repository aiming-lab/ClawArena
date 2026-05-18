<div align="center">

<img src="../assets/claweval.png" alt="ClawArena" width="500">

<br/>

## Evaluación comparativa de agentes de IA en entornos de información en evolución.

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
      <b style="font-size:1.1em">+ Cualquier agente</b>
    </td>
  </tr>
  <tr>
    <td align="center"><b>OpenClaw</b></td>
    <td align="center"><b>Claude Code</b></td>
    <td align="center"><b>MetaClaw</b></td>
    <td align="center"><b>PicoClaw</b></td>
    <td align="center"><b>Nanobot</b></td>
    <td align="center">mediante <a href="plugin.md">plugin</a></td>
  </tr>
</table>

<br/>

<p>
  <a href="../README.md">English</a> |
  <a href="README_zh.md">中文</a> |
  <a href="README_ja.md">日本語</a> |
  <a href="README_ko.md">한국어</a> |
  <b>Español</b> |
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

[🔭 Visión general](#-visión-general) • [📈 Tabla de clasificación](#-tabla-de-clasificación) • [🆚 Comparativa Benchmarks](#-comparativa-benchmarks) • [🚀 Inicio rápido](#-inicio-rápido) • [🤖 Frameworks compatibles](#-frameworks-compatibles) • [📊 Datos y evaluación](#-datos-y-evaluación) • [🔍 Estudios de caso](#-estudios-de-caso) • [📖 Documentación](#-documentación) • [🏗️ Estructura del proyecto](#-estructura-del-proyecto) • [🙏 Proyectos relacionados](#-proyectos-relacionados) • [📚 Cita](#-cita) • [📄 Licencia](#-licencia)

</div>

---

## 🔭 Visión general

**ClawArena** es una plataforma de evaluación comparativa para agentes de codificación basados en IA. Proporciona una canalización unificada para ejecutar inferencia, puntuar resultados y comparar el rendimiento de distintos frameworks de agentes sobre el mismo conjunto de escenarios realistas y multisesión.

- **12 escenarios multiturno** que abarcan contextos profesionales diversos: análisis minorista, finanzas, sanidad, seguridad de la información, recursos humanos, educación, integridad académica y otros
- **337 rondas de evaluación** que combinan razonamiento `multi_choice` (95 rondas) y verificación de ejecución `exec_check` (242 rondas)
- **45 actualizaciones dinámicas** — nuevos archivos y sesiones de chat inyectados en mitad de la evaluación para examinar la revisión de creencias y el manejo de contradicciones
- **Contexto multisesión** — los agentes razonan sobre archivos de espacio de trabajo e historiales de chat de múltiples canales (mensajería instantánea, correo electrónico, etc.) en cada escenario
- **Independencia de framework** — en el artículo se evalúan cinco frameworks (OpenClaw, Claude Code, NanoBot, PicoClaw, MetaClaw); pueden añadirse otros mediante el [sistema de plugins](plugin.md)
- **Integración con [MetaClaw](https://github.com/aiming-lab/MetaClaw)** — evaluación de agentes potenciados con memoria, habilidades y aprendizaje por refuerzo

<div align="center">
<img src="../assets/overview.png" alt="ClawArena Cross-Domain Data Sample Gallery" width="900">
</div>

---

## 📈 Tabla de clasificación

Clasificamos a los agentes mediante la **Puntuación Compuesta de Fiabilidad (Composite Reliability Score, CRS)**, que pondera por igual la corrección bruta y la consistencia conductual:

- **TCR** (Task Completion Rate, tasa de finalización de tareas) = $S/N$ — corrección media en todas las rondas, descompuesta en subpuntuaciones MC y EC.
- **SC** (Success Cohesion, cohesión de éxitos) = $(S - k)/(N - 1)$ — concentración de las rondas correctas en rachas largas e ininterrumpidas; SC = 1 para una única racha, SC = 0 para alternancia entre éxito y fracaso.
- **FD** (Failure Dispersion, dispersión de fallos) = $1 - (S_f - k_f)/(N - 1)$ — penaliza las rachas prolongadas de fallo.
- **Robustness** = SC × FD — forma multiplicativa que hace que el colapso en cualquiera de los dos ejes perjudique la puntuación.
- **CRS** = (TCR + Robustness) / 2.

_Todos los números están macropromediados sobre los 12 escenarios / 337 rondas y ordenados por CRS._

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

<sub>Cada modelo se muestra bajo su arnés principal: los modelos de Anthropic a través de Claude Code (incompatibles con OpenClaw), y los demás bajo OpenClaw. Consulte el artículo para la comparación entre frameworks que varía el arnés manteniendo fijo el modelo.</sub>

---

## 🆚 Comparativa Benchmarks

En qué se diferencia ClawArena de otros benchmarks de agentes harness-native. La mayoría de los trabajos previos cubren como máximo dos de los cuatro ejes de diseño; ClawArena es el único benchmark que satisface los cuatro simultáneamente y que reporta resultados en cinco frameworks.

Leyenda de columnas — ✅ admitido · ❌ no admitido · 🟡 parcial (mecanismo presente pero debilitado, p. ej. mensajes de terceros expuestos solo como archivos planos en lugar de sesiones etiquetadas por canal, o preferencias codificadas como persona estática en vez de aprendidas en rondas silenciosas):

- **MSC** (Multi-Source Conflict, conflicto multifuente): el agente debe analizar conversaciones usuario–tercero distinguidas por canal.
- **DU** (Dynamic Update, actualización dinámica): el entorno se sobrescribe entre turnos del usuario (las dinámicas de retorno de herramientas dentro del mismo bucle no cuentan).
- **MU** (Multi-User turn, turno multiusuario): el usuario vuelve a intervenir con nuevas consultas a lo largo de las rondas.
- **Pref.** (Implicit personalization, personalización implícita): preferencias del usuario aplicadas en rondas de examen silencioso.
- **Frmw.**: número de frameworks de agente evaluados.

| Benchmark | Origen de tareas | Modo de ejecución | MSC | DU | MU | Pref. | Verificación | Frmw. | Escala (Preg. / Esc.) |
|---|---|---|:---:|:---:|:---:|:---:|---|:---:|---|
| [ClawBench](https://github.com/reacher-z/ClawBench)         | Conjunto manual               | Web en vivo               | ❌ | ❌ | ❌ | ❌ | regla+LLM   | 8 | 283 / 144 sitios |
| [Claw-Eval](https://github.com/claw-eval/claw-eval)         | Curado desde upstream         | Sandbox + mock            | ❌ | ❌ | ✅ | ❌ | regla+LLM   | 1 | 300 / 9 cat. |
| [Claw-Eval-Live](https://github.com/Claw-Eval-Live/Claw-Eval-Live)    | Señales en vivo (trimestral)  | Servicios mock            | ❌ | ❌ | ❌ | ❌ | regla+LLM   | 1 | 105 / 17 fam. |
| [ClawMark](https://github.com/evolvent-ai/ClawMark)          | Manual + síntesis IA          | Servicios sandboxeados    | ✅ | ✅ | ✅ | ❌ | basado en reglas | 1 | 100 / 13 esc. |
| [ClawsBench](https://github.com/benchflow-ai/ClawsBench)        | Diseñado por expertos         | Servicios mock            | ✅ | ❌ | ❌ | ❌ | basado en reglas | 4 | 44 / 5 serv. |
| [MetaClaw-Bench](https://github.com/aiming-lab/MetaClaw)     | Sintético                     | Simulación de workspace   | 🟡 | ✅ | ✅ | 🟡 | basado en reglas | 1 | 346 / 30 días |
| [PinchBench](https://github.com/pinchbench/skill)        | Manual (mundo real)           | Real (OpenClaw)           | ❌ | ❌ | ❌ | ❌ | regla+LLM   | 1 | 23 / 8 cat. |
| [QwenClawBench](https://huggingface.co/datasets/skylenage-ai/QwenClawBench)     | Empírico (declarado)          | Real (Docker)             | ❌ | ❌ | ❌ | 🟡 | regla+LLM   | 1 | 100 / 8 dom. |
| [WildClawBench](https://github.com/InternLM/WildClawBench)     | Manual (recolección abierta)  | Real (OpenClaw)           | ✅ | ❌ | ❌ | 🟡 | regla+LLM   | 1 | 60 / 6 cat. |
| [ZClawBench](https://huggingface.co/datasets/zai-org/ZClawBench)        | Manual + sintético            | Real + parcialmente mock  | ❌ | ❌ | ❌ | ❌ | regla+LLM   | 1 | 116 / 6 cat. |
| **ClawArena (Ntro.)** | **Síntesis empírica**     | **Sim. multicanal**       | ✅ | ✅ | ✅ | ✅ | basado en reglas | **5** | **337 / 12 esc.** |

---

## 🚀 Inicio rápido

### 1. Instalación completa

```bash
bash scripts/setup.sh
```

Este comando instala ClawArena (con extras de desarrollo), MetaClaw y las CLIs de los frameworks (OpenClaw, Claude Code, Nanobot, PicoClaw) junto con Claude Code Router en una sola operación. Para una configuración manual, consulte la [Guía de instalación](installation.md).

### 2. Ejecutar el benchmark

Primero consulte [`scripts/env_example.sh`](../scripts/env_example.sh) para configurar las variables de entorno, y a continuación ejecute:

```bash
python scripts/test_run.py
```

Edite `scripts/test_run.py` para configurar frameworks, concurrencia, tiempo de espera y ruta de salida.

<details>
<summary><b>O bien utilice la CLI directamente</b></summary>

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

Consulte la [Referencia de la CLI](cli.md) para ver todos los comandos y opciones.
</details>

<details>
<summary><b>Desarrollo y pruebas</b></summary>

```bash
pip install -e ".[dev]"
pytest
```

</details>

---

## 🤖 Frameworks compatibles

| Framework | Tipo | Lenguaje | Notas |
|-----------|------|----------|-------|
| [OpenClaw](https://github.com/openclaw/openclaw) | Agente CLI | Node.js | — |
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | Proxy de LLM | Python | Compatible únicamente dentro de [OpenClaw](https://github.com/openclaw/openclaw) y [Nanobot](https://github.com/HKUDS/nanobot) |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) | Agente CLI | Node.js | Asistido por [Claude Code Router](https://github.com/musistudio/claude-code-router) |
| [PicoClaw](https://github.com/sipeed/picoclaw) | Agente CLI | Go | — |
| [Nanobot](https://github.com/HKUDS/nanobot) | Agente CLI | Python | — |

Pueden añadirse nuevos frameworks mediante el sistema de plugins sin modificar el código central — basta con añadir un archivo `.py` que registre un adaptador y cargarlo en tiempo de ejecución:

```bash
clawarena infer --data tests.json --framework my_agent --out results/ --plugin my_agent.py
```

Consulte la [Guía de plugins](plugin.md) para conocer la interfaz del adaptador y los hooks de ronda del motor.

[MetaClaw](https://github.com/aiming-lab/MetaClaw) se integra como una capa proxy transparente para evaluar agentes potenciados con memoria, habilidades y aprendizaje por refuerzo. Se activa añadiendo un campo `metaclaw` a `tests.json`; los frameworks anfitriones admitidos son **OpenClaw** y **Nanobot**. Consulte la [Guía de MetaClaw](metaclaw-guide.md) para conocer los modos gestionado/no gestionado, la configuración de disparadores y las plantillas YAML.

> **⚠️ Aviso de facturación y políticas (4 de abril de 2026):**
Es posible que herramientas o agentes de terceros como OpenClaw ya no puedan enrutar tráfico mediante sus credenciales personales de suscripción a Claude Free/Pro/Max. Cualquier integración con Claude en ClawArena que utilice el inicio de sesión OAuth de Claude.ai **debe migrar a la autenticación oficial mediante clave de API** a través de la Claude Console o de proveedores de nube compatibles. Estas conexiones de terceros consumirán únicamente sus **créditos de uso adicional de pago** y no su cuota de suscripción. Consulte la documentación [legal y de cumplimiento de Anthropic](https://code.claude.com/docs/en/legal-and-compliance) para conocer todos los detalles de la política.

---

## 📊 Datos y evaluación

Cada escenario contiene:

- **Archivos de espacio de trabajo** — documentos, hojas de cálculo y código que el agente puede leer
- **Historiales de sesión** — registros de chat multicanal (mensajería instantánea, correo, Slack, etc.)
- **Preguntas de evaluación** — `multi_choice` (razonamiento) y `exec_check` (verificación de ejecución)
- **Actualizaciones dinámicas** — nuevas sesiones y archivos inyectados entre rondas

Las 337 rondas combinan dos tipos de pregunta:

| Tipo | Rondas | Pruebas | Cómo |
|------|------:|-------|-----|
| `multi_choice` | 95 (28,2 %) | Razonamiento y comprensión del agente | Extrae `\bbox{A,B,...}` de la respuesta y calcula IoU/F1 frente a la respuesta correcta |
| `exec_check`   | 242 (71,8 %) | Acciones y archivos de salida del agente | Ejecuta comandos de shell para verificar el código de salida y la stdout |

<details>
<summary><b>Canalización de construcción de datos (clic para expandir)</b></summary>
<br/>
<div align="center">
<img src="../assets/pipeline_v2.png" alt="ClawArena Construction Pipeline" width="700">
</div>

Consulte la [especificación de datos](data-spec/) para conocer el sistema completo de seis capas usado para construir los 12 escenarios.
</details>

Hemos liberado las especificaciones completas de construcción de datos — incluido el diseño de escenarios en seis capas, las directrices de síntesis y la documentación de errores comunes — en [`docs/data-spec/`](data-spec/).

Consulte [Estructura de datos](data-structure.md) para la especificación completa del formato.

---

## 🔍 Estudios de caso

Diez estudios de caso por opción extraídos de los 12 escenarios de ClawArena, que cubren las categorías de interacción MS-R, DU-R, P-R y `exec_check` en los dominios de seguridad, clínica, recursos humanos y comercio electrónico.

<details>
<summary><b>Casos 1–2: filtración de la API de NexaFlow (MS-R) y fallo de cumplimiento de esquema (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_01_02.png" alt="Case 1-2" width="900">
</div>
</details>

<details>
<summary><b>Casos 3–4: opciones compuestas de integridad académica (MS-R) y revisión influida por la autoridad (DU-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_03_04.png" alt="Case 3-4" width="900">
</div>
</details>

<details>
<summary><b>Casos 5–6: prefijo de nombre de archivo en despido improcedente (P-R + exec_check) y techo de salida estructurada del RGPD (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_05_06.png" alt="Case 5-6" width="900">
</div>
</details>

<details>
<summary><b>Casos 7–8: fallos específicos de actualización en el fraude de GPU del 618 (DU-R) y adherencia al esquema JSON (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_07_08.png" alt="Case 7-8" width="900">
</div>
</details>

<details>
<summary><b>Casos 9–10: síntesis conjuntiva en despido improcedente (MS-R + DU-R) y síntesis final de autoría en pipeline (exec_check + MS-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_09_10.png" alt="Case 9-10" width="900">
</div>
</details>

---

## 📖 Documentación

| Documento | Descripción |
|----------|-------------|
| [Instalación](installation.md) | Guía de configuración para ClawArena, frameworks y MetaClaw |
| [Referencia de CLI](cli.md) | Todos los comandos, opciones y variables de entorno |
| [Estructura de datos](data-structure.md) | Formato del conjunto de datos, tipos de pregunta, esquema del manifiesto |
| [Guía de proveedores](provider-usage-guide.md) | Configuración de proveedores de LLM y cadena de prioridad |
| [Guía de MetaClaw](metaclaw-guide.md) | Modos de integración de MetaClaw y hooks de disparo |
| [Guía de plugins](plugin.md) | Cómo escribir y registrar adaptadores de framework externos |

---

## 🏗️ Estructura del proyecto

```
ClawArena
├── src/clawarena/
│   ├── cli.py           # Punto de entrada de la CLI
│   ├── core/            # Canalización: infer, score, report, compare, check, run, clean
│   ├── stats/           # Análisis de tokens y estructura con disposiciones por framework
│   ├── engines/         # Motores de ejecución de agentes (por framework)
│   ├── data_handlers/   # Carga de datos, validación, gestión de copias de trabajo
│   ├── adapters/        # Composición de adaptadores de framework + registro
│   ├── qtypes/          # Tipos de pregunta: multi_choice, exec_check
│   ├── metaclaw/        # Ciclo de vida del proxy MetaClaw y hooks de disparo
│   └── plugins/         # Carga de adaptadores externos (--plugin)
├── data/clawarena/      # Conjunto de datos (12 escenarios, 337 rondas)
├── docs/                # Documentación, incluida docs/data-spec/ (especificación de construcción en seis capas)
├── scripts/             # Configuración, ejecutor de pruebas, utilidades de comparación
├── helpers/             # Hooks auxiliares específicos por framework
└── tests/               # Conjunto de pruebas (356 tests)
```

---

## 🙏 Proyectos relacionados

ClawArena se construye sobre y evalúa los siguientes frameworks de agentes de código abierto:

- [OpenClaw](https://github.com/openclaw/openclaw) — el agente CLI principal evaluado.
- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — proxy de metaaprendizaje que potencia a los agentes con memoria, habilidades y aprendizaje por refuerzo.
- [Claude Code](https://github.com/anthropics/claude-code) — herramienta de codificación agéntica de Anthropic.
- [Claude Code Router](https://github.com/musistudio/claude-code-router) — enruta las solicitudes de Claude Code a distintos modelos.
- [PicoClaw](https://github.com/sipeed/picoclaw) — agente CLI ligero basado en Go.
- [Nanobot](https://github.com/HKUDS/nanobot) — agente CLI nativo de Python con soporte para la API de Anthropic.

---

## 📚 Cita

```bibtex
@article{ji2026clawarena,
  title={ClawArena: A Multi-Framework Benchmark for Evaluating AI Coding Agents on Realistic Multi-Session Scenarios},
  author={Ji, Haonian and Xiong, Kaiwen and Han, Siwei and Xia, Peng and Qiu, Shi and Zhou, Yiyang and Liu, Jiaqi and Li, Jinlong and Li, Bingzhou and Zheng, Zeyu and Xie, Cihang and Yao, Huaxiu},
  journal={arXiv preprint arXiv:2604.04202},
  year={2026}
}
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la [Licencia MIT](../LICENSE).
