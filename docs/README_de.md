<div align="center">

<img src="../assets/claweval.png" alt="ClawArena" width="500">

<br/>

## Benchmarking von KI-Agenten in sich wandelnden Informationsumgebungen.

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
      <b style="font-size:1.1em">+ Beliebiger Agent</b>
    </td>
  </tr>
  <tr>
    <td align="center"><b>OpenClaw</b></td>
    <td align="center"><b>Claude Code</b></td>
    <td align="center"><b>MetaClaw</b></td>
    <td align="center"><b>PicoClaw</b></td>
    <td align="center"><b>Nanobot</b></td>
    <td align="center">über <a href="plugin.md">Plugin</a></td>
  </tr>
</table>

<br/>

<p>
  <a href="../README.md">English</a> |
  <a href="README_zh.md">中文</a> |
  <a href="README_ja.md">日本語</a> |
  <a href="README_ko.md">한국어</a> |
  <a href="README_es.md">Español</a> |
  <a href="README_fr.md">Français</a> |
  <b>Deutsch</b>
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

[🔭 Überblick](#-überblick) • [📈 Bestenliste](#-bestenliste) • [🆚 Benchmark-Vergleich](#-benchmark-vergleich) • [🚀 Schnellstart](#-schnellstart) • [🤖 Unterstützte Frameworks](#-unterstützte-frameworks) • [📊 Daten und Auswertung](#-daten-und-auswertung) • [🔍 Fallstudien](#-fallstudien) • [📖 Dokumentation](#-dokumentation) • [🏗️ Projektstruktur](#-projektstruktur) • [🙏 Verwandte Projekte](#-verwandte-projekte) • [📚 Zitation](#-zitation) • [📄 Lizenz](#-lizenz)

</div>

---

## 🔭 Überblick

**ClawArena** ist eine Benchmark-Evaluationsplattform für KI-Coding-Agenten. Sie stellt eine einheitliche Pipeline bereit, um Inferenz auszuführen, Ergebnisse zu bewerten und die Leistung verschiedener Agenten-Frameworks anhand desselben Satzes realistischer Mehrsitzungs-Szenarien zu vergleichen.

- **12 Mehrrunden-Szenarien** aus vielfältigen professionellen Kontexten — Einzelhandelsanalytik, Finanzen, Gesundheitswesen, Informationssicherheit, Personalwesen, Bildung, wissenschaftliche Integrität und weitere
- **337 Auswertungsrunden**, die `multi_choice`-Reasoning (95 Runden) und `exec_check`-Ausführungsprüfung (242 Runden) kombinieren
- **45 dynamische Aktualisierungen** — neue Dateien und Chat-Sitzungen werden mitten in der Auswertung eingespeist, um die Revision von Überzeugungen und den Umgang mit Widersprüchen zu prüfen
- **Mehrsitzungs-Kontext** — Agenten schlussfolgern innerhalb jedes Szenarios über Workspace-Dateien und mehrkanalige Chat-Verläufe (IM, E-Mail usw.)
- **Framework-agnostisch** — fünf Frameworks werden im Paper evaluiert (OpenClaw, Claude Code, NanoBot, PicoClaw, MetaClaw); weitere können über das [Plugin-System](plugin.md) hinzugefügt werden
- **[MetaClaw](https://github.com/aiming-lab/MetaClaw)-Integration** — Bewertung von Agenten, die durch Memory, Skills und RL erweitert sind

<div align="center">
<img src="../assets/overview.png" alt="ClawArena Cross-Domain Data Sample Gallery" width="900">
</div>

---

## 📈 Bestenliste

Wir ordnen Agenten anhand des **Composite Reliability Score (CRS)** ein, der reine Korrektheit und Verhaltenskonsistenz gleich gewichtet:

- **TCR** (Task Completion Rate, Aufgabenerfüllungsrate) = $S/N$ — durchschnittliche Korrektheit über alle Runden, zerlegt in MC- und EC-Teilbewertungen.
- **SC** (Success Cohesion, Erfolgskohäsion) = $(S - k)/(N - 1)$ — Konzentration korrekter Runden in lange, ununterbrochene Serien; SC = 1 bei einer einzigen Serie, SC = 0 bei abwechselndem Bestehen/Nichtbestehen.
- **FD** (Failure Dispersion, Fehlerstreuung) = $1 - (S_f - k_f)/(N - 1)$ — bestraft anhaltende Fehlerserien.
- **Robustheit (Robustness)** = SC × FD — multiplikative Form, sodass ein Einbruch in einer der beiden Achsen den Wert deutlich senkt.
- **CRS** = (TCR + Robustness) / 2.

_Alle Zahlen sind makrogemittelt über die 12 Szenarien / 337 Runden und nach CRS sortiert._

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

<sub>Jedes Modell wird unter seinem primären Harness gezeigt: Anthropic-Modelle über Claude Code (inkompatibel mit OpenClaw), alle anderen unter OpenClaw. Den frameworkübergreifenden Vergleich, bei dem das Harness variiert und das Modell festgehalten wird, finden Sie im Paper.</sub>

> 📥 **Ein neues Ergebnis einreichen?** Siehe [submit-to-leaderboard.md](submit-to-leaderboard.md). Referenzlayouts liegen unter [`result_example/`](../result_example/); Community-Einreichungen werden in [`submissions/`](../submissions/) gesammelt.

---

## 🆚 Benchmark-Vergleich

Worin sich ClawArena von anderen harness-nativen Agenten-Benchmarks unterscheidet. Die meisten vorherigen Arbeiten decken höchstens zwei der vier Designachsen ab; ClawArena ist der einzige Benchmark, der alle vier gleichzeitig erfüllt und Ergebnisse über fünf Frameworks hinweg berichtet.

Spaltenlegende — ✅ unterstützt · ❌ nicht unterstützt · 🟡 teilweise (Mechanismus vorhanden, aber abgeschwächt – z. B. Drittpartei-Nachrichten nur als einfache Dateien statt als kanalmarkierte Sitzungen offengelegt, oder Präferenzen als statische Persona kodiert statt in stillen Runden gelernt):

- **MSC** (Multi-Source Conflict): Der Agent muss kanalweise unterschiedene Gespräche zwischen Nutzer und Drittparteien analysieren.
- **DU** (Dynamic Update): Die Umgebung wird zwischen Nutzerzügen überschrieben (Tool-Rückgabedynamik innerhalb einer Schleife zählt nicht).
- **MU** (Multi-User turn): Der Nutzer beteiligt sich über mehrere Runden hinweg mit neuen Anfragen.
- **Pref.** (Implicit personalization): Nutzerpräferenzen werden in stillen Prüfungsrunden angewandt.
- **Frmw.**: Anzahl der evaluierten Agenten-Frameworks.

| Benchmark | Aufgabenquelle | Ausführungsmodus | MSC | DU | MU | Pref. | Verifikation | Frmw. | Umfang (Fragen / Szen.) |
|---|---|---|:---:|:---:|:---:|:---:|---|:---:|---|
| [ClawBench](https://github.com/reacher-z/ClawBench)         | Manueller Pool                | Live-Web                  | ❌ | ❌ | ❌ | ❌ | Regel+LLM   | 8 | 283 / 144 Sites |
| [Claw-Eval](https://github.com/claw-eval/claw-eval)         | Aus Upstream kuratiert        | Sandbox + Mock            | ❌ | ❌ | ✅ | ❌ | Regel+LLM   | 1 | 300 / 9 Kat. |
| [Claw-Eval-Live](https://github.com/Claw-Eval-Live/Claw-Eval-Live)    | Live-Signale (quartalsweise)  | Mock-Dienste              | ❌ | ❌ | ❌ | ❌ | Regel+LLM   | 1 | 105 / 17 Fam. |
| [ClawMark](https://github.com/evolvent-ai/ClawMark)          | Manuell + KI-Synthese         | Gesandboxte Dienste       | ✅ | ✅ | ✅ | ❌ | regelbasiert | 1 | 100 / 13 Szen. |
| [ClawsBench](https://github.com/benchflow-ai/ClawsBench)        | Experten-Entwurf              | Mock-Dienste              | ✅ | ❌ | ❌ | ❌ | regelbasiert | 4 | 44 / 5 Dienste |
| [MetaClaw-Bench](https://github.com/aiming-lab/MetaClaw)     | Synthetisch                   | Workspace-Simulation      | 🟡 | ✅ | ✅ | 🟡 | regelbasiert | 1 | 346 / 30 Tage |
| [PinchBench](https://github.com/pinchbench/skill)        | Manuell (Realwelt)            | Real (OpenClaw)           | ❌ | ❌ | ❌ | ❌ | Regel+LLM   | 1 | 23 / 8 Kat. |
| [QwenClawBench](https://huggingface.co/datasets/skylenage-ai/QwenClawBench)     | Empirisch (angegeben)         | Real (Docker)             | ❌ | ❌ | ❌ | 🟡 | Regel+LLM   | 1 | 100 / 8 Domänen |
| [WildClawBench](https://github.com/InternLM/WildClawBench)     | Manuell (in the wild)         | Real (OpenClaw)           | ✅ | ❌ | ❌ | 🟡 | Regel+LLM   | 1 | 60 / 6 Kat. |
| [ZClawBench](https://huggingface.co/datasets/zai-org/ZClawBench)        | Manuell + synthetisch         | Real + teilweise Mock     | ❌ | ❌ | ❌ | ❌ | Regel+LLM   | 1 | 116 / 6 Kat. |
| **ClawArena (Unsere)** | **Empirische Synthese**  | **Mehrkanal-Simulation**  | ✅ | ✅ | ✅ | ✅ | regelbasiert | **5** | **337 / 12 Szen.** |

---

## 🚀 Schnellstart

### 1. Alles installieren

```bash
bash scripts/setup.sh
```

Dieser Befehl installiert ClawArena (samt Dev-Extras), MetaClaw sowie die Framework-CLIs (OpenClaw, Claude Code, Nanobot, PicoClaw) und Claude Code Router in einem Schritt. Eine manuelle Einrichtung beschreibt der [Installationsleitfaden](installation.md).

### 2. Benchmark ausführen

Konsultieren Sie zunächst [`scripts/env_example.sh`](../scripts/env_example.sh), um die Umgebungsvariablen zu konfigurieren, und führen Sie dann aus:

```bash
python scripts/test_run.py
```

Bearbeiten Sie `scripts/test_run.py`, um Frameworks, Nebenläufigkeit, Timeout und Ausgabepfad einzustellen.

<details>
<summary><b>Oder verwenden Sie die CLI direkt</b></summary>

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

Eine vollständige Übersicht aller Befehle und Optionen finden Sie in der [CLI-Referenz](cli.md).
</details>

<details>
<summary><b>Entwickeln und Tests ausführen</b></summary>

```bash
pip install -e ".[dev]"
pytest
```

</details>

---

## 🤖 Unterstützte Frameworks

| Framework | Typ | Sprache | Anmerkungen |
|-----------|------|----------|-------|
| [OpenClaw](https://github.com/openclaw/openclaw) | CLI-Agent | Node.js | — |
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | LLM-Proxy | Python | Wird ausschließlich innerhalb von [OpenClaw](https://github.com/openclaw/openclaw) und [Nanobot](https://github.com/HKUDS/nanobot) unterstützt |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) | CLI-Agent | Node.js | Unterstützt durch [Claude Code Router](https://github.com/musistudio/claude-code-router) |
| [PicoClaw](https://github.com/sipeed/picoclaw) | CLI-Agent | Go | — |
| [Nanobot](https://github.com/HKUDS/nanobot) | CLI-Agent | Python | — |

Neue Frameworks lassen sich über das Plugin-System hinzufügen, ohne den Kerncode zu verändern — fügen Sie schlicht eine `.py`-Datei hinzu, die einen Adapter registriert, und laden Sie sie zur Laufzeit:

```bash
clawarena infer --data tests.json --framework my_agent --out results/ --plugin my_agent.py
```

Die Adapter-Schnittstelle und die Engine-Round-Hooks beschreibt der [Plugin-Leitfaden](plugin.md).

[MetaClaw](https://github.com/aiming-lab/MetaClaw) ist als transparente Proxy-Schicht eingebunden, um Agenten zu evaluieren, die durch Memory, Skills und RL erweitert sind. Es wird durch Hinzufügen eines `metaclaw`-Felds zu `tests.json` aktiviert; unterstützte Host-Frameworks sind **OpenClaw** und **Nanobot**. Den [MetaClaw-Leitfaden](metaclaw-guide.md) konsultieren Sie für Managed-/Unmanaged-Modi, Trigger-Konfiguration und YAML-Vorlagen.

> **⚠️ Hinweis zu Abrechnung und Richtlinien (4. April 2026):**
Drittanbieter-Tools/-Agenten wie OpenClaw dürfen Datenverkehr möglicherweise nicht mehr über Ihre persönlichen Anmeldedaten eines Claude-Free/Pro/Max-Abonnements leiten. Sämtliche Claude-Integrationen in ClawArena, die Claude.ai-OAuth-Login nutzen, **müssen auf eine offizielle API-Schlüssel-Authentifizierung** über die Claude Console oder unterstützte Cloud-Anbieter umgestellt werden. Solche Drittanbieter-Verbindungen verbrauchen künftig ausschließlich Ihre **kostenpflichtigen zusätzlichen Nutzungsguthaben** und nicht Ihr Abonnement-Kontingent. Vollständige Details zur Richtlinie finden Sie in den [Rechts- und Compliance-Hinweisen von Anthropic](https://code.claude.com/docs/en/legal-and-compliance).

---

## 📊 Daten und Auswertung

Jedes Szenario enthält:

- **Workspace-Dateien** — Dokumente, Tabellen und Code, die der Agent lesen kann
- **Sitzungsverläufe** — mehrkanalige Chat-Logs (IM, E-Mail, Slack usw.)
- **Auswertungsfragen** — `multi_choice` (Reasoning) und `exec_check` (Ausführungsprüfung)
- **Dynamische Aktualisierungen** — neue Sitzungen und Dateien, die zwischen den Runden eingespielt werden

Zwei Fragetypen verteilen sich auf die 337 Runden:

| Typ | Runden | Prüft | Wie |
|------|------:|-------|-----|
| `multi_choice` | 95 (28,2 %) | Reasoning und Verständnis des Agenten | Extrahiert `\bbox{A,B,...}` aus der Antwort und berechnet IoU/F1 gegen die Referenzlösung |
| `exec_check`   | 242 (71,8 %) | Aktionen und Dateiausgaben des Agenten | Führt Shell-Befehle aus, um Exit-Code und stdout zu prüfen |

<details>
<summary><b>Pipeline zur Datenkonstruktion (zum Aufklappen klicken)</b></summary>
<br/>
<div align="center">
<img src="../assets/pipeline_v2.png" alt="ClawArena Construction Pipeline" width="700">
</div>

Die vollständige sechs­schichtige Spezifikationssystematik, die zum Aufbau aller 12 Szenarien verwendet wurde, finden Sie in der [Datenspezifikation](data-spec/).
</details>

Wir haben die vollständigen Spezifikationen zur Datenkonstruktion — einschließlich des sechsschichtigen Szenarien­designs, der Synthese-Richtlinien und der Dokumentation häufiger Fallstricke — unter [`docs/data-spec/`](data-spec/) als Open Source veröffentlicht.

Die vollständige Formatspezifikation finden Sie unter [Datenstruktur](data-structure.md).

---

## 🔍 Fallstudien

Zehn optionsbezogene Fallstudien aus den 12 Szenarien von ClawArena, die die Interaktionskategorien MS-R, DU-R, P-R und `exec_check` über die Bereiche Sicherheit, Klinik, Personalwesen und E-Commerce hinweg abdecken.

<details>
<summary><b>Fall 1–2: NexaFlow-API-Leck (MS-R) und Fehler bei der Schemakonformität (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_01_02.png" alt="Case 1-2" width="900">
</div>
</details>

<details>
<summary><b>Fall 3–4: zusammengesetzte Optionen zur wissenschaftlichen Integrität (MS-R) und autoritätsbeeinflusste Revision (DU-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_03_04.png" alt="Case 3-4" width="900">
</div>
</details>

<details>
<summary><b>Fall 5–6: Dateinamen-Präfix bei ungerechtfertigter Kündigung (P-R + exec_check) und Obergrenze der DSGVO-konformen strukturierten Ausgabe (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_05_06.png" alt="Case 5-6" width="900">
</div>
</details>

<details>
<summary><b>Fall 7–8: aktualisierungsbedingte Fehlschläge beim 618-GPU-Betrug (DU-R) und Einhaltung des JSON-Schemas (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_07_08.png" alt="Case 7-8" width="900">
</div>
</details>

<details>
<summary><b>Fall 9–10: konjunktive Synthese zu ungerechtfertigter Kündigung (MS-R + DU-R) und finale Synthese zur Pipeline-Autorenschaft (exec_check + MS-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_09_10.png" alt="Case 9-10" width="900">
</div>
</details>

---

## 📖 Dokumentation

| Dokument | Beschreibung |
|----------|-------------|
| [Installation](installation.md) | Einrichtungsleitfaden für ClawArena, Frameworks und MetaClaw |
| [CLI-Referenz](cli.md) | Sämtliche Befehle, Optionen und Umgebungsvariablen |
| [Datenstruktur](data-structure.md) | Datensatzformat, Fragetypen, Manifest-Schema |
| [Provider-Leitfaden](provider-usage-guide.md) | Konfiguration der LLM-Provider und Prioritätskette |
| [MetaClaw-Leitfaden](metaclaw-guide.md) | MetaClaw-Integrationsmodi und Trigger-Hooks |
| [Plugin-Leitfaden](plugin.md) | Schreiben und Registrieren externer Framework-Adapter |

---

## 🏗️ Projektstruktur

```
ClawArena
├── src/clawarena/
│   ├── cli.py           # CLI-Einstiegspunkt
│   ├── core/            # Pipeline: infer, score, report, compare, check, run, clean
│   ├── stats/           # Token- und Strukturanalyse mit Layouts pro Framework
│   ├── engines/         # Agenten-Ausführungs-Engines (pro Framework)
│   ├── data_handlers/   # Datenladen, Validierung, Verwaltung von Arbeitskopien
│   ├── adapters/        # Framework-Adapter-Komposition + Registry
│   ├── qtypes/          # Fragetypen: multi_choice, exec_check
│   ├── metaclaw/        # MetaClaw-Proxy-Lebenszyklus und Trigger-Hooks
│   └── plugins/         # Laden externer Adapter (--plugin)
├── data/clawarena/      # Datensatz (12 Szenarien, 337 Runden)
├── docs/                # Dokumentation, einschließlich docs/data-spec/ (sechsschichtige Konstruktionsspezifikation)
├── scripts/             # Setup, Test-Runner, Vergleichsdienstprogramme
├── helpers/             # Framework-spezifische Hilfs-Hooks
└── tests/               # Test-Suite (356 Tests)
```

---

## 🙏 Verwandte Projekte

ClawArena baut auf den folgenden Open-Source-Agenten-Frameworks auf und evaluiert sie:

- [OpenClaw](https://github.com/openclaw/openclaw) — der primär evaluierte CLI-Agent.
- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — Meta-Lern-Proxy, der Agenten um Memory, Skills und RL erweitert.
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropics agentenbasiertes Coding-Werkzeug.
- [Claude Code Router](https://github.com/musistudio/claude-code-router) — leitet Claude-Code-Anfragen an unterschiedliche Modelle weiter.
- [PicoClaw](https://github.com/sipeed/picoclaw) — leichtgewichtiger, Go-basierter CLI-Agent.
- [Nanobot](https://github.com/HKUDS/nanobot) — Python-nativer CLI-Agent mit Unterstützung für die Anthropic-API.

---

## 📚 Zitation

```bibtex
@article{ji2026clawarena,
  title={ClawArena: A Multi-Framework Benchmark for Evaluating AI Coding Agents on Realistic Multi-Session Scenarios},
  author={Ji, Haonian and Xiong, Kaiwen and Han, Siwei and Xia, Peng and Qiu, Shi and Zhou, Yiyang and Liu, Jiaqi and Li, Jinlong and Li, Bingzhou and Zheng, Zeyu and Xie, Cihang and Yao, Huaxiu},
  journal={arXiv preprint arXiv:2604.04202},
  year={2026}
}
```

---

## 📄 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](../LICENSE).
