<div align="center">

<h1>ClawArena-Team</h1>

### Benchmarking von Subagenten-Orchestrierung und dynamischen Workflows in Sprachmodell-Agenten

<p>
  <a href="../../README.md">English</a> •
  <a href="README.zh-Hans.md">简体中文</a> •
  <a href="README.zh-Hant.md">繁體中文</a> •
  <a href="README.ja.md">日本語</a> •
  <a href="README.ko.md">한국어</a> •
  <a href="README.fr.md">Français</a> •
  <b>Deutsch</b> •
  <a href="README.es.md">Español</a> •
  <a href="README.pt.md">Português</a> •
  <a href="README.ru.md">Русский</a>
</p>

<p>
  <a href="#-zitation"><img src="https://img.shields.io/badge/Paper-Preprint-b31b1b?style=flat&logo=arxiv&logoColor=white" alt="Paper" /></a>
  <a href="../../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="Lizenz MIT" /></a>
  <img src="https://img.shields.io/badge/Python-≥3.10-blue?style=flat&labelColor=555&logo=python&logoColor=white" alt="Python ≥3.10" />
  <img src="https://img.shields.io/badge/Version-v1.0.0-blueviolet?style=flat&labelColor=555" alt="v1.0.0" />
</p>
<p>
  <img src="https://img.shields.io/badge/Scenarios-41-orange?style=flat&labelColor=555" alt="41 Szenarien" />
  <img src="https://img.shields.io/badge/Rounds-258-red?style=flat&labelColor=555" alt="258 Runden" />
  <img src="https://img.shields.io/badge/Staged%20Updates-72-yellow?style=flat&labelColor=555" alt="72 gestaffelte Aktualisierungen" />
  <img src="https://img.shields.io/badge/Models-12-9cf?style=flat&labelColor=555" alt="12 Modelle" />
  <img src="https://img.shields.io/badge/Scoring-Execution--based-success?style=flat&labelColor=555" alt="Ausführungsbasiert" />
</p>

<img src="../../assets/hero.png" alt="ClawArena-Team" width="900">

[🔭 Überblick](#-überblick) • [📈 Bestenliste](#-bestenliste) • [🔑 Zentrale Erkenntnisse](#-zentrale-erkenntnisse) • [🚀 Schnellstart](#-schnellstart) • [🧰 Fähigkeitsspektrum & Werkzeuge](#-fähigkeitsspektrum--werkzeuge) • [📊 Daten & Evaluation](#-daten--evaluation) • [🔍 Fallstudien](#-fallstudien) • [📖 Dokumentation](#-dokumentation) • [🏗️ Projektstruktur](#️-projektstruktur) • [📚 Zitation](#-zitation) • [📄 Lizenz](#-lizenz)

</div>

---

## 🔭 Überblick

LM-Agenten werden zunehmend als **Manager** eingesetzt – ein Hauptmodell erstellt spezialisierte Subagenten, delegiert Aufgaben und orchestriert ihre parallelen, asynchronen Rückgaben über dynamische Workflows. Bestehende Benchmarks bewerten die eigene Aufgabenlösung einer Policy oder ein festes Multi-Agenten-System, aber keiner isoliert die **Managementfähigkeit** des einzelnen LM, das als Leiter agiert.

**ClawArena-Team** (die Team-Management-Variante in der ClawArena-Reihe) isoliert genau dies. Ein **rein textbasierter Hauptagent** muss mehrstufige, multimodale Aufgaben über mehrere Verzeichnisse bewältigen, die er nicht allein erledigen kann, indem er Subagenten aus einem **festen, lokal bereitgestellten Pool** erstellt, bevollmächtigt, einplant und integriert. Jeder Manager befehligt dieselben Worker, sodass Score-Unterschiede *Managementkompetenz, nicht rohe Leistungsfähigkeit* widerspiegeln.

- **41 Szenarien · 258 Evaluationsrunden · 72 gestaffelte Aktualisierungen**, die **Recht, Medizin, Ingenieurwesen, Wirtschaft und Wissenschaft** abdecken.
- **Rein textbasierter, teilweise sichtbarer Hauptagent** – er nimmt nativ nur Text wahr und erreicht nur einen Teil des Workspace, sodass Delegation zwingend erforderlich ist.
- **Fester Subagenten-Pool**, lokal über vLLM bereitgestellt (`llm`/`vlm`/`omni`), für jeden bewerteten Manager identisch gehalten.
- **Ausführungsbasierte Bewertung, kein LLM-Judge** – jede Runde liefert einen Shell-Befehl, dessen Exit-Code (mit optionalem Output-Matching) über Bestehen/Nichtbestehen entscheidet.

---

## 📈 Bestenliste

Wir ordnen die Hauptagenten-Modelle anhand des zusammengesetzten **Subagent-Management Score (SMS)**, der die Aufgabenkorrektheit mit einem Management-Faktor aus Least-Privilege und Modalitäts-Routing multipliziert:

$$\mathrm{SMS} = \mathrm{TCR} \times \frac{\mathrm{TPP} + \mathrm{ROC} + \mathrm{WPP} + \mathrm{MCA}}{4}$$

**SMS ≤ TCR gilt immer:** Management kann die Aufgabenkorrektheit nur mindern, niemals erhöhen. Ein Modell, das perfekt managt, aber die Aufgabe nicht löst, erhält null Punkte.

| Modell | TCR | TPP | ROC | WPP | MCA | **SMS** | Kosten ($) | Runden |
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

<sub>Alle Werte in %, zwölf Modelle × 41 Szenarien in einem einzigen Evaluationslauf, sortiert nach **SMS**. Das neu veröffentlichte `glm-5.2` (über die offizielle z.ai-API) ist der stärkste Open-Weight-Manager – SMS 50.4, Platz 4 insgesamt – und überholt `kimi-k2.6` an der Spitze der Open-Weight-Modelle. **Fett** markiert den spaltenbesten Wert (der Beste jeder Spalte ist unabhängig hervorgehoben). Kosten ($): Hauptagenten-API-Kosten pro Lauf zu Listenpreisen des Anbieters / von OpenRouter – niedriger ist besser, daher nicht fett gesetzt; Subagenten laufen auf dem festen lokalen Pool und werden nicht bepreist. Runden: bestandene Runden von 258. `claude-fable-5` wird im Auslieferungszustand evaluiert, mit einem vom Anbieter empfohlenen Fallback bei Verweigerung → `claude-opus-4-8`.</sub>

> 📥 Ein Ergebnis einreichen? Siehe [docs/submit-to-leaderboard.md](../../docs/submit-to-leaderboard.md). Beispielläufe und beigetragene Ergebnisse liegen in [`submissions/`](../../submissions/).

---

## 🔑 Zentrale Erkenntnisse

Über zwölf proprietäre, community-gehostete und selbst gehostete Hauptagenten-Modelle hinweg ergeben sich drei Erkenntnisse.

<table>
<tr>
<td width="33%" valign="top">

### 1️⃣ Der Engpass ist die *Privilegienvergabe*, nicht die Wahrnehmung

Die beiden „einfachen" Achsen sind nahezu gesättigt – Read-Only-Compliance (ROC ≥ 92 %) und Modalitäts-Wahl-Genauigkeit (MCA ≥ 92 %) für jedes leistungsfähige Modell. Die unterscheidenden Achsen sind die Privilegien-Präzisionsmetriken: **Workspace-Permission Precision (WPP) erreicht *niemals* 50 %** für irgendein Modell. Subagenten erhalten routinemäßig etwa doppelt so viele Dateien, wie sie tatsächlich anfassen.

</td>
<td width="33%" valign="top">

### 2️⃣ Kosten und Managementqualität sind *entkoppelt*

Die Hauptagenten-API-Kosten umspannen **über 100×** (\$0.8 → \$93 pro Lauf), während SMS **unter 4×** umspannt. Die günstigsten offenen Modelle liegen auf der Pareto-Front – `deepseek-v4-pro` erreicht SMS 46.4 bei nur \$1.7 –, während mehrere kostenintensive Modelle (`gpt-5.5`, `sonnet-4-6`, `kimi-k2.6`) vom mittelteuren `gemini-3.5-flash` *dominiert* werden. Das Open-Weight-Modell `glm-5.2` ($22.9) landet ebenfalls als stärkstes offenes Modell auf der Front.

</td>
<td width="33%" valign="top">

### 3️⃣ Scores clustern, Verhalten divergiert

Unterhalb des Flaggschiffs clustern zehn Modelle innerhalb eines **9,9-Punkte-SMS-Bands** (43.9–53.8), doch ihr Orchestrierungsverhalten unterscheidet sich um **mehr als eine Größenordnung**. Die Rate verbotener Zugriffe pro Subagent reicht bei leistungsfähigen Modellen von 0,48 bis 5,78 (~12×), und die Nutzung dynamischer Workflows reicht von 8 bis 112 Aufrufen.

</td>
</tr>
</table>

<div align="center">

| Kosten vs. Management (Erkenntnis 2) | Berechtigungsverletzungen (Erkenntnis 3) |
|:---:|:---:|
| <img src="../../assets/pareto.png" alt="SMS vs. Hauptagenten-API-Kosten, logarithmische Skala; günstige offene Modelle auf der Pareto-Front" width="430"> | <img src="../../assets/forbidden.png" alt="Anzahl verbotener Zugriffe pro Modell MAF/SAFt/SAFa auf logarithmischer Skala; SAFa divergiert ~12×" width="430"> |

</div>

**Modalitäts-Routing.** Manager greifen überwiegend standardmäßig auf den `llm`-Schlüssel zurück und erstellen vergleichsweise wenige `vlm`/`omni`-Spezialisten; wenn sie *tatsächlich* nach Modalität routen, tun sie es korrekt (daher das hohe MCA), aber sie nutzen die multimodalen Worker zu wenig.

<div align="center">
<img src="../../assets/modality.png" alt="Verteilung der Subagenten-Modellschlüssel: Manager greifen standardmäßig auf den llm-Schlüssel zurück und nutzen vlm/omni zu wenig" width="780">
</div>

---

## 🚀 Schnellstart

Die vollständige Anleitung (Bereitstellung des Pools, Auswahl der Ziele, Fortsetzen von Läufen) finden Sie unter [`docs/running-experiments.md`](../../docs/running-experiments.md).

### 1. Installation

```bash
pip install -e ".[dev]"           # core + dev extras (pytest, hf_hub, reportlab)
# pip install -e ".[dev,video]"   # add to run the real-video multimodal tests
```

Dies installiert die `clawarena-team`-CLI (Kurzaliase: **`cateam`** / **`ca-team`**). Der Tokenizer und das Chat-Template sind **in `helper/` mitgeliefert** – kein Download-Schritt erforderlich.

### 2. Den festen Subagenten-Pool bereitstellen (lokales vLLM)

Der Subagenten-Pool wird für jeden bewerteten Hauptagenten identisch gehalten, sodass Management die einzige Variable ist:

```bash
python scripts/serve_gemma-4-31b.py     # serves the llm / vlm keys (gemma-4-31b-it)
python scripts/serve_gemma-4-omni.py    # serves the omni key   (gemma-4-e4b-it)
```

### 3. Validieren, ausführen und analysieren

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

> Die Kurzaliase `cateam` und `ca-team` sind überall mit `clawarena-team` austauschbar (z. B. `cateam run ...`).

<details>
<summary><b>Das <code>--model</code>-JSON</b></summary>

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

Derselbe String kann über `CATEAM_MODEL_JSON` bereitgestellt werden. Das Feld `main.modalities` entscheidet, was der Hauptagent nativ wahrnimmt; `Read` reduziert Dateien außerhalb der Modalität auf einen textuellen Platzhalter und schlägt Delegation vor. Siehe [`docs/cli.md`](../../docs/cli.md) für alle Flags und `CATEAM_*`-Variablen, [`docs/dataset.md`](../../docs/dataset.md) für das Datensatzformat und [`docs/provider.md`](../../docs/provider.md) für die Anbindung eines Anbieters.
</details>

---

## 🧰 Fähigkeitsspektrum & Werkzeuge

ClawArena-Team fasst Subagenten-Management als **Prinzipal-Agent-Problem** auf. Das Fähigkeitsspektrum des Hauptagenten zerfällt in sechs konkrete Operationen, die jeweils durch das Szenariodesign erzwungen werden:

| Operation | Was sie erfordert |
|---|---|
| **Erstellung** | Einen Subagenten mit einem System-Prompt, einem Modellschlüssel, einer Werkzeug-Teilmenge und einer Workspace-Pfad-Whitelist (eine Teilmenge der eigenen) erstellen. |
| **Modalitäts-Routing** | Bilder/Video an ein `vlm` und Audio an ein `omni` weiterleiten, da der Manager nur Text wahrnimmt. |
| **Least-Privilege-Bevollmächtigung** | Nur die Werkzeuge und Pfade gewähren, die ein Subagent tatsächlich benötigt; Übervergabe ist verschwenderisch und unsicher. |
| **Einplanung** | Subagenten im Vorder- oder Hintergrund ausführen, als neue oder fortgesetzte (wiederaufgenommene) Sitzungen und parallel; Hintergrundaufgaben benachrichtigen den Manager bei Abschluss. |
| **Dynamische Workflows** | Multi-Subagenten-Orchestrierung (parallele + Pipeline-Stufen) zur Laufzeit über denselben Pool verfassen. |
| **Integration** | Subagenten-Rückgaben zu einem korrekten Ergebnis zusammenführen – nur die integrierte Antwort wird bewertet. |

Dem Hauptagenten werden **CapitalCase**-Werkzeuge bereitgestellt, deren Namen, Beschreibungen und Parameter reale Harness-Konventionen widerspiegeln, um die Vergleichbarkeit über Benchmarks hinweg zu gewährleisten:

| Werkzeug | Zweck |
|---|---|
| **Read** | Eine Datei lesen; Inhalt außerhalb der Modalität wird auf einen textuellen Platzhalter reduziert, der Delegation vorschlägt. |
| **Write** | Eine Datei im Workspace erstellen oder überschreiben. |
| **Edit** | Eine gezielte In-Place-Bearbeitung an einer vorhandenen Datei vornehmen. |
| **Bash** | Einen Shell-Befehl in der Sandbox ausführen (`realpath`-geprüfte Pfade). |
| **Grep** | Dateiinhalte nach Muster durchsuchen. |
| **Glob** | Dateien nach Namensmuster finden. |
| **CreateSubagent** | Einen Subagenten definieren: System-Prompt, Modellschlüssel, Werkzeug-Teilmenge und Workspace-Pfad-Whitelist. |
| **RunSubagent** | Einen Subagenten im Vorder- oder Hintergrund aufrufen, als neue oder fortgesetzte (wiederaufgenommene) Sitzung. |
| **ListSubagents** | Die bisher erstellten Subagenten und ihren Status auflisten. |
| **InspectSubagent** | Konfiguration, gewährte Privilegien und Laufhistorie eines Subagenten inspizieren. |
| **Workflow** | Orchestrierungs-DSL im JS-Stil – `agent()`, `parallel()`, `pipeline()` – zum Komponieren von Multi-Subagenten-Läufen zur Laufzeit. |

Systemebene-Signale (Umgebung, Token-Schwellenwerte) werden über `<system-reminder>`-Blöcke injiziert; Abschlüsse von Hintergrundaufgaben treffen über `<task-notification>`-Blöcke ein. Jeder Pfadzugriff wird `realpath`-geprüft, und Symlink-Ausbrüche werden abgelehnt und als verbotene Zugriffe gezählt.

### Fester Subagenten-Pool (die kontrollierte Variable)

| Schlüssel | Modell | Server | Native Modalitäten |
|---|---|---|---|
| `llm`  | gemma-4-31b-it | lokales vLLM | Text |
| `vlm`  | gemma-4-31b-it | lokales vLLM | Text, Bild, Video |
| `omni` | gemma-4-e4b-it | lokales vLLM | Text, Bild, Audio, Video |

Jeder Hauptagent befehligt dasselbe Team; nur der Hauptagent variiert zwischen den Läufen.

---

## 📊 Daten & Evaluation

Jedes Szenario stellt einen Workspace, eine Folge von Benutzerfragen und Ground-Truth-Prüfungen bereit. Zwischen einigen Runden erhält der Workspace **gestaffelte Aktualisierungen** (neue oder ersetzte Dateien), die nachfolgende Antworten verändern und ein anhaltendes Management einer sich entwickelnden Aufgabe statt einer einmaligen Lösung erfordern.

<div align="center">
<img src="../../assets/heatmap.png" alt="SMS-Heatmap pro Szenario: 12 Modelle × 41 Szenarien, der Schwierigkeitsgrad ist ungleichmäßig und modellspezifisch" width="820">
<br/>
<sub>SMS-Heatmap pro Szenario × Modell – der Schwierigkeitsgrad ist ungleichmäßig und modellspezifisch.</sub>
</div>

**Bewertungskomponenten** (alle in $[0,1]$, kein LLM-Judge):

| Metrik | Bedeutung |
|---|---|
| **TCR** – Task Completion Rate | Durchschnittliche Bestehensrate über die Benutzerfragen. |
| **TPP** – Tool-Permission Precision | Pro Subagent der Anteil der gewährten Werkzeugtypen, die tatsächlich genutzt werden. |
| **ROC** – Read-Only Compliance | Pro Subagent 0, wenn einem Read-Only-Subagenten ein veränderndes Werkzeug gewährt wurde, sonst 1. |
| **WPP** – Workspace-Permission Precision | Pro Subagent zugegriffene Dateien ÷ gewährte Dateien. |
| **MCA** – Modality-Choice Accuracy | Pro Subagent, ob ein `vlm` tatsächlich Bild/Video liest und ein `omni` Audio liest (`llm` erhält 1). |

Jedes Szenario erfüllt **zehn harte Designvorgaben (C1–C10)** – unlesbare Bereiche, substanzielle gestaffelte Aktualisierungen, vollständige Nutzung des Werkzeugspektrums, ≥8 Verzeichnisse mit Ködern, Runden mit Nicht-Text-Modalität, parallelitätspflichtige Aufgaben, Session-Wiederverwendungspaare, rundenübergreifende Abhängigkeiten, Modalitäts-Köder und maschinell prüfbare Antworten –, die jeweils auf einen eigenständigen Management-Fehlermodus abzielen, den ein einzelnes LM sonst umgehen könnte.

### Datensatzzusammensetzung

- **41 Szenarien · 258 Runden**, von denen 44 (17,1 %) gestaffelte Aktualisierungen vorausgehen.
- **72 Aktualisierungsgruppen über 255 Dateien** (61,1 % `new`, 38,9 % `replace`, im Mittel 3,54 Dateien/Gruppe).
- **170,5 MiB · 28,9 M Tokens** – 71,9 % Workspace-Inhalt, 27,9 % gestaffelte Aktualisierungen.
- Modalitätsmix: Text dominiert Dateien/Tokens, während Audio und Bild die Rohbytes dominieren – eine erhebliche Nicht-Text-Nutzlast, die ein rein textbasierter Manager nicht direkt konsumieren kann.

ClawArena-Team wird **erstellt, nicht gesammelt**: Workspace-Korpora, multimodale Assets, Ground Truth und Ausführungsprüfungen werden allesamt prozedural aus denselben versionskontrollierten Skripten synthetisiert, über ein **Synthese-Verifikations-Schwungrad**, in dem ein realer Baseline-Subagenten-Management-Lauf das finale Akzeptanzkriterium ist. Der Benchmark wird gewissermaßen von genau der Fähigkeit verfasst, die er misst. Siehe [`docs/dataset.md`](../../docs/dataset.md) und den Anhang des Papers für das Format und die Konstruktionsmethodik.

Für feinere Verteilungen siehe [`docs/data-stats/`](../../docs/data-stats/): Jede Teilmenge (`demo` / `wave1` / `wave3` / `wave4`) und der vollständige Satz haben ein eigenes `STATS.md` plus Diagramme (Token-/Dateigrößen-/Modalitätsverteilung, Tag-Abdeckung, ...), erzeugt von `clawarena-team stats`.

---

## 🔍 Fallstudien

Zwölf Fälle, direkt aus aufgezeichneten Lauf-Transkripten und `metadata.json`-Dateien entnommen – alle Zahlen und zitierten Zeichenketten wortgetreu –, die die drei Erkenntnisse und das Management-Fähigkeitsspektrum konkret untermauern.

<details>
<summary><b>Fälle 1–4: Übervergabe beim stärksten Manager, korrektes Modalitäts-Routing, die Modalitäts-Köder-Falle und Kosten entkoppelt von Qualität</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_1.png" alt="Fallstudien 1–4" width="900">
</div>
</details>

<details>
<summary><b>Fälle 5–8: identische Scores bei divergierenden verbotenen Zugriffen, Verfassen eines dynamischen Workflows (und ein Fan-out, der abstürzt), logische Parallelität ohne echte Hintergrund-Einplanung sowie echter Hintergrund plus Workflow-Parallelität</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_2.png" alt="Fallstudien 5–8" width="900">
</div>
</details>

<details>
<summary><b>Fälle 9–12: eine ausstehende Korrektur, die sich nie fortpflanzt, eine Fähigkeitsklippe, die der Manager nicht bedienen kann, die Management-Obergrenze (paralleles Fan-out, adaptiver Retry, Least Privilege) und wie gutes Management aussieht</b></summary>
<br/>
<div align="center">
<img src="../../assets/case_study_3.png" alt="Fallstudien 9–12" width="900">
</div>
</details>

---

## 📖 Dokumentation

| Dokument | Beschreibung |
|----------|-------------|
| [CLI-Referenz](../../docs/cli.md) | Alle Befehle, Flags und `CATEAM_*`-Umgebungsvariablen |
| [Datensatzformat](../../docs/dataset.md) | Szenario-Layout, Runden, gestaffelte Aktualisierungen, Ground-Truth-Prüfungen |
| [Anbieter-Leitfaden](../../docs/provider.md) | Anbindung von Hauptagenten-Anbietern (OpenAI-compat, Gemini, OpenRouter, ...) |
| [Experimente ausführen](../../docs/running-experiments.md) | Bereitstellung des Subagenten-Pools und Ausführen / Fortsetzen eines vollständigen Sweeps |
| [An die Bestenliste einreichen](../../docs/submit-to-leaderboard.md) | Einen Lauf paketieren und zu [`submissions/`](../../submissions/) beitragen |

---

## 🏗️ Projektstruktur

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

## 📚 Zitation

Diese Arbeit ist derzeit ein anonymes Preprint; der arXiv-Bezeichner und die Autorenliste werden noch ergänzt.

```bibtex
@misc{clawarena-team2026,
  title  = {ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents},
  author = {Anonymous Author(s)},
  year   = {2026},
  note   = {Preprint. arXiv identifier and author list to be added.}
}
```

---

## 📄 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](../../../LICENSE).
