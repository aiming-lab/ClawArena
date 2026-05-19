<div align="center">

<img src="../assets/claweval.png" alt="ClawArena" width="500">

<br/>

## Évaluation comparative d'agents d'IA dans des environnements informationnels en évolution.

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
      <b style="font-size:1.1em">+ N'importe quel agent</b>
    </td>
  </tr>
  <tr>
    <td align="center"><b>OpenClaw</b></td>
    <td align="center"><b>Claude Code</b></td>
    <td align="center"><b>MetaClaw</b></td>
    <td align="center"><b>PicoClaw</b></td>
    <td align="center"><b>Nanobot</b></td>
    <td align="center">via un <a href="plugin.md">plugin</a></td>
  </tr>
</table>

<br/>

<p>
  <a href="../README.md">English</a> |
  <a href="README_zh.md">中文</a> |
  <a href="README_ja.md">日本語</a> |
  <a href="README_ko.md">한국어</a> |
  <a href="README_es.md">Español</a> |
  <b>Français</b> |
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

[🔭 Vue d'ensemble](#-vue-densemble) • [📈 Classement](#-classement) • [🆚 Comparaison Benchmarks](#-comparaison-benchmarks) • [🚀 Démarrage rapide](#-démarrage-rapide) • [🤖 Frameworks pris en charge](#-frameworks-pris-en-charge) • [📊 Données et évaluation](#-données-et-évaluation) • [🔍 Études de cas](#-études-de-cas) • [📖 Documentation](#-documentation) • [🏗️ Structure du projet](#-structure-du-projet) • [🙏 Projets associés](#-projets-associés) • [📚 Citation](#-citation) • [📄 Licence](#-licence)

</div>

---

## 🔭 Vue d'ensemble

**ClawArena** est une plateforme d'évaluation comparative pour les agents de codage à base d'IA. Elle fournit un pipeline unifié permettant d'exécuter l'inférence, de noter les résultats et de comparer les performances de différents frameworks d'agents sur le même ensemble de scénarios réalistes et multi-sessions.

- **12 scénarios multi-tours** couvrant des contextes professionnels variés — analyse de la distribution, finance, santé, sécurité de l'information, ressources humaines, éducation, intégrité scientifique, et bien d'autres
- **337 manches d'évaluation** combinant le raisonnement `multi_choice` (95 manches) et la vérification d'exécution `exec_check` (242 manches)
- **45 mises à jour dynamiques** — de nouveaux fichiers et sessions de discussion injectés en cours d'évaluation pour sonder la révision des croyances et la gestion des contradictions
- **Contexte multi-sessions** — les agents raisonnent sur les fichiers de l'espace de travail et sur des historiques de conversation multi-canaux (messagerie instantanée, courriel, etc.) au sein de chaque scénario
- **Indépendance vis-à-vis du framework** — cinq frameworks sont évalués dans l'article (OpenClaw, Claude Code, NanoBot, PicoClaw, MetaClaw) ; d'autres peuvent être ajoutés via le [système de plugins](plugin.md)
- **Intégration de [MetaClaw](https://github.com/aiming-lab/MetaClaw)** — évaluation d'agents enrichis par la mémoire, les compétences et l'apprentissage par renforcement

<div align="center">
<img src="../assets/overview.png" alt="ClawArena Cross-Domain Data Sample Gallery" width="900">
</div>

---

## 📈 Classement

Nous classons les agents à l'aide du **score composite de fiabilité (Composite Reliability Score, CRS)**, qui pondère équitablement la justesse brute et la cohérence comportementale :

- **TCR** (Task Completion Rate, taux d'achèvement des tâches) = $S/N$ — justesse moyenne sur l'ensemble des manches, décomposée en sous-scores MC et EC.
- **SC** (Success Cohesion, cohésion des succès) = $(S - k)/(N - 1)$ — concentration des manches correctes en longues séries ininterrompues ; SC = 1 pour une seule série, SC = 0 pour une alternance succès/échec.
- **FD** (Failure Dispersion, dispersion des échecs) = $1 - (S_f - k_f)/(N - 1)$ — pénalise les longues séries d'échecs.
- **Robustness** = SC × FD — forme multiplicative, de sorte que l'effondrement de l'un ou l'autre des axes pénalise le score.
- **CRS** = (TCR + Robustness) / 2.

_Tous les chiffres sont moyennés en macro sur les 12 scénarios / 337 manches et triés par CRS._

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

<sub>Chaque modèle est présenté sous son harnais principal : les modèles d'Anthropic via Claude Code (incompatibles avec OpenClaw), tous les autres sous OpenClaw. Voir l'article pour la comparaison inter-frameworks dans laquelle le harnais varie tandis que le modèle est fixé.</sub>

> 📥 **Vous souhaitez soumettre un nouveau résultat ?** Consultez [submit-to-leaderboard.md](submit-to-leaderboard.md). Les modèles de référence se trouvent dans [`result_example/`](../result_example/) ; les contributions de la communauté sont regroupées dans [`submissions/`](../submissions/).

---

## 🆚 Comparaison Benchmarks

En quoi ClawArena diffère des autres benchmarks d'agents harness-natifs. La plupart des travaux antérieurs ne couvrent que deux des quatre axes de conception au maximum ; ClawArena est le seul benchmark à satisfaire les quatre simultanément tout en rapportant des résultats sur cinq frameworks.

Légende des colonnes — ✅ pris en charge · ❌ non pris en charge · 🟡 partiel (mécanisme présent mais affaibli, p. ex. messages de tiers exposés uniquement sous forme de fichiers plats au lieu de sessions étiquetées par canal, ou préférences encodées comme une persona statique plutôt qu'apprises lors de tours silencieux) :

- **MSC** (Multi-Source Conflict, conflit multi-sources) : l'agent doit analyser les conversations utilisateur–tiers distinguées par canal.
- **DU** (Dynamic Update, mise à jour dynamique) : l'environnement est écrasé entre les tours utilisateur (les dynamiques de retour d'outil au sein d'une boucle ne comptent pas).
- **MU** (Multi-User turn, tour multi-utilisateur) : l'utilisateur intervient à nouveau avec de nouvelles requêtes au fil des tours.
- **Pref.** (Implicit personalization, personnalisation implicite) : préférences utilisateur appliquées lors des tours d'examen silencieux.
- **Frmw.** : nombre de frameworks d'agent évalués.

| Benchmark | Source des tâches | Mode d'exécution | MSC | DU | MU | Pref. | Vérification | Frmw. | Échelle (Q / Scén.) |
|---|---|---|:---:|:---:|:---:|:---:|---|:---:|---|
| [ClawBench](https://github.com/reacher-z/ClawBench)         | Pool manuel                    | Web en direct                | ❌ | ❌ | ❌ | ❌ | règle+LLM   | 8 | 283 / 144 sites |
| [Claw-Eval](https://github.com/claw-eval/claw-eval)         | Curation depuis l'amont        | Sandbox + mock               | ❌ | ❌ | ✅ | ❌ | règle+LLM   | 1 | 300 / 9 cat. |
| [Claw-Eval-Live](https://github.com/Claw-Eval-Live/Claw-Eval-Live)    | Signaux en direct (trimestriels)| Services mock              | ❌ | ❌ | ❌ | ❌ | règle+LLM   | 1 | 105 / 17 fam. |
| [ClawMark](https://github.com/evolvent-ai/ClawMark)          | Manuel + synthèse IA           | Services sandboxés           | ✅ | ✅ | ✅ | ❌ | à base de règles | 1 | 100 / 13 scén. |
| [ClawsBench](https://github.com/benchflow-ai/ClawsBench)        | Conçu par des experts          | Services mock                | ✅ | ❌ | ❌ | ❌ | à base de règles | 4 | 44 / 5 serv. |
| [MetaClaw-Bench](https://github.com/aiming-lab/MetaClaw)     | Synthétique                    | Simulation d'espace de travail | 🟡 | ✅ | ✅ | 🟡 | à base de règles | 1 | 346 / 30 jours |
| [PinchBench](https://github.com/pinchbench/skill)        | Manuel (monde réel)            | Réel (OpenClaw)              | ❌ | ❌ | ❌ | ❌ | règle+LLM   | 1 | 23 / 8 cat. |
| [QwenClawBench](https://huggingface.co/datasets/skylenage-ai/QwenClawBench)     | Empirique (déclaré)            | Réel (Docker)                | ❌ | ❌ | ❌ | 🟡 | règle+LLM   | 1 | 100 / 8 dom. |
| [WildClawBench](https://github.com/InternLM/WildClawBench)     | Manuel (collecte sauvage)      | Réel (OpenClaw)              | ✅ | ❌ | ❌ | 🟡 | règle+LLM   | 1 | 60 / 6 cat. |
| [ZClawBench](https://huggingface.co/datasets/zai-org/ZClawBench)        | Manuel + synthétique           | Réel + mock partiel          | ❌ | ❌ | ❌ | ❌ | règle+LLM   | 1 | 116 / 6 cat. |
| **ClawArena (Notre)** | **Synthèse empirique**     | **Sim. multi-canaux**        | ✅ | ✅ | ✅ | ✅ | à base de règles | **5** | **337 / 12 scén.** |

---

## 🚀 Démarrage rapide

### 1. Tout installer

```bash
bash scripts/setup.sh
```

Cette commande installe ClawArena (avec les extras de développement), MetaClaw ainsi que les CLI des frameworks (OpenClaw, Claude Code, Nanobot, PicoClaw) et Claude Code Router en une seule étape. Pour une installation manuelle, consultez le [Guide d'installation](installation.md).

### 2. Lancer le benchmark

Reportez-vous d'abord à [`scripts/env_example.sh`](../scripts/env_example.sh) pour configurer les variables d'environnement, puis exécutez :

```bash
python scripts/test_run.py
```

Modifiez `scripts/test_run.py` pour configurer les frameworks, la concurrence, le délai d'expiration et le chemin de sortie.

<details>
<summary><b>Ou utilisez la CLI directement</b></summary>

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

Consultez la [Référence de la CLI](cli.md) pour l'ensemble des commandes et des options.
</details>

<details>
<summary><b>Développer et exécuter les tests</b></summary>

```bash
pip install -e ".[dev]"
pytest
```

</details>

---

## 🤖 Frameworks pris en charge

| Framework | Type | Langage | Notes |
|-----------|------|----------|-------|
| [OpenClaw](https://github.com/openclaw/openclaw) | Agent CLI | Node.js | — |
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | Proxy LLM | Python | Pris en charge uniquement au sein d'[OpenClaw](https://github.com/openclaw/openclaw) et de [Nanobot](https://github.com/HKUDS/nanobot) |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) | Agent CLI | Node.js | Assisté par [Claude Code Router](https://github.com/musistudio/claude-code-router) |
| [PicoClaw](https://github.com/sipeed/picoclaw) | Agent CLI | Go | — |
| [Nanobot](https://github.com/HKUDS/nanobot) | Agent CLI | Python | — |

De nouveaux frameworks peuvent être ajoutés via le système de plugins sans modifier le cœur du code — il suffit de fournir un fichier `.py` qui enregistre un adaptateur et de le charger à l'exécution :

```bash
clawarena infer --data tests.json --framework my_agent --out results/ --plugin my_agent.py
```

Consultez le [Guide des plugins](plugin.md) pour l'interface de l'adaptateur et les hooks de manche du moteur.

[MetaClaw](https://github.com/aiming-lab/MetaClaw) est intégré sous forme de couche proxy transparente afin d'évaluer des agents enrichis par la mémoire, les compétences et l'apprentissage par renforcement. Il s'active en ajoutant un champ `metaclaw` à `tests.json` ; les frameworks hôtes pris en charge sont **OpenClaw** et **Nanobot**. Consultez le [Guide MetaClaw](metaclaw-guide.md) pour les modes managed/unmanaged, la configuration des déclencheurs et les modèles YAML.

> **⚠️ Avis de facturation et de politique (4 avril 2026) :**
Les outils ou agents tiers comme OpenClaw pourraient ne plus être autorisés à acheminer le trafic via vos identifiants personnels d'abonnement Claude Free/Pro/Max. Toute intégration Claude présente dans ClawArena utilisant la connexion OAuth de Claude.ai **doit basculer vers une authentification officielle par clé d'API** via la Claude Console ou des fournisseurs cloud pris en charge. Ces connexions tierces ne consommeront désormais que vos **crédits d'utilisation supplémentaires payants**, et non votre quota d'abonnement. Pour l'intégralité de la politique, consultez la documentation [juridique et de conformité d'Anthropic](https://code.claude.com/docs/en/legal-and-compliance).

---

## 📊 Données et évaluation

Chaque scénario contient :

- **Fichiers d'espace de travail** — documents, tableurs et code que l'agent peut lire
- **Historiques de session** — journaux de discussion multi-canaux (messagerie instantanée, courriel, Slack, etc.)
- **Questions d'évaluation** — `multi_choice` (raisonnement) et `exec_check` (vérification d'exécution)
- **Mises à jour dynamiques** — nouvelles sessions et nouveaux fichiers injectés entre les manches

Deux types de questions couvrent les 337 manches :

| Type | Manches | Évalue | Méthode |
|------|------:|-------|-----|
| `multi_choice` | 95 (28,2 %) | Le raisonnement et la compréhension de l'agent | Extrait `\bbox{A,B,...}` de la réponse, calcule l'IoU/F1 par rapport à la vérité terrain |
| `exec_check`   | 242 (71,8 %) | Les actions et les fichiers de sortie de l'agent | Exécute des commandes shell pour vérifier le code de sortie et la stdout |

<details>
<summary><b>Pipeline de construction des données (cliquer pour développer)</b></summary>
<br/>
<div align="center">
<img src="../assets/pipeline_v2.png" alt="ClawArena Construction Pipeline" width="700">
</div>

Consultez la [spécification des données](data-spec/) pour le système complet de spécification à six couches utilisé pour construire les 12 scénarios.
</details>

Nous avons publié en open source l'ensemble des spécifications de construction des données — y compris la conception de scénarios à six couches, les directives de synthèse et la documentation des écueils — dans [`docs/data-spec/`](data-spec/).

Consultez [Structure des données](data-structure.md) pour la spécification complète du format.

---

## 🔍 Études de cas

Dix études de cas par option, tirées des 12 scénarios de ClawArena, couvrant les catégories d'interaction MS-R, DU-R, P-R et `exec_check` à travers les domaines de la sécurité, de la clinique, des ressources humaines et du commerce électronique.

<details>
<summary><b>Cas 1–2 : violation de l'API NexaFlow (MS-R) et défaut de conformité au schéma (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_01_02.png" alt="Case 1-2" width="900">
</div>
</details>

<details>
<summary><b>Cas 3–4 : options composites d'intégrité scientifique (MS-R) et révision sous influence d'autorité (DU-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_03_04.png" alt="Case 3-4" width="900">
</div>
</details>

<details>
<summary><b>Cas 5–6 : préfixe de nom de fichier dans un licenciement abusif (P-R + exec_check) et plafond de sortie structurée du RGPD (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_05_06.png" alt="Case 5-6" width="900">
</div>
</details>

<details>
<summary><b>Cas 7–8 : échecs spécifiques à la mise à jour dans la fraude aux GPU du 618 (DU-R) et respect du schéma JSON (exec_check)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_07_08.png" alt="Case 7-8" width="900">
</div>
</details>

<details>
<summary><b>Cas 9–10 : synthèse conjonctive sur licenciement abusif (MS-R + DU-R) et synthèse finale d'attribution d'autorat de pipeline (exec_check + MS-R)</b></summary>
<br/>
<div align="center">
<img src="../assets/case_09_10.png" alt="Case 9-10" width="900">
</div>
</details>

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Installation](installation.md) | Guide de configuration pour ClawArena, les frameworks et MetaClaw |
| [Référence de la CLI](cli.md) | Toutes les commandes, options et variables d'environnement |
| [Structure des données](data-structure.md) | Format du jeu de données, types de questions, schéma du manifeste |
| [Guide des fournisseurs](provider-usage-guide.md) | Configuration des fournisseurs de LLM et chaîne de priorité |
| [Guide MetaClaw](metaclaw-guide.md) | Modes d'intégration et hooks de déclenchement de MetaClaw |
| [Guide des plugins](plugin.md) | Écrire et enregistrer des adaptateurs de framework externes |

---

## 🏗️ Structure du projet

```
ClawArena
├── src/clawarena/
│   ├── cli.py           # Point d'entrée de la CLI
│   ├── core/            # Pipeline : infer, score, report, compare, check, run, clean
│   ├── stats/           # Analyse des tokens et de la structure avec dispositions par framework
│   ├── engines/         # Moteurs d'exécution d'agents (par framework)
│   ├── data_handlers/   # Chargement, validation des données et gestion des copies de travail
│   ├── adapters/        # Composition des adaptateurs de framework + registre
│   ├── qtypes/          # Types de questions : multi_choice, exec_check
│   ├── metaclaw/        # Cycle de vie du proxy MetaClaw et hooks de déclenchement
│   └── plugins/         # Chargement d'adaptateurs externes (--plugin)
├── data/clawarena/      # Jeu de données (12 scénarios, 337 manches)
├── docs/                # Documentation, y compris docs/data-spec/ (spécification de construction à six couches)
├── scripts/             # Configuration, exécuteur de tests, utilitaires de comparaison
├── helpers/             # Hooks d'aide spécifiques à chaque framework
└── tests/               # Suite de tests (356 tests)
```

---

## 🙏 Projets associés

ClawArena s'appuie sur les frameworks d'agents open source suivants et les évalue :

- [OpenClaw](https://github.com/openclaw/openclaw) — l'agent CLI principal évalué.
- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — proxy de méta-apprentissage qui enrichit les agents par la mémoire, les compétences et l'apprentissage par renforcement.
- [Claude Code](https://github.com/anthropics/claude-code) — l'outil de codage agentique d'Anthropic.
- [Claude Code Router](https://github.com/musistudio/claude-code-router) — route les requêtes Claude Code vers différents modèles.
- [PicoClaw](https://github.com/sipeed/picoclaw) — agent CLI léger basé sur Go.
- [Nanobot](https://github.com/HKUDS/nanobot) — agent CLI Python natif prenant en charge l'API Anthropic.

---

## 📚 Citation

```bibtex
@article{ji2026clawarena,
  title={ClawArena: A Multi-Framework Benchmark for Evaluating AI Coding Agents on Realistic Multi-Session Scenarios},
  author={Ji, Haonian and Xiong, Kaiwen and Han, Siwei and Xia, Peng and Qiu, Shi and Zhou, Yiyang and Liu, Jiaqi and Li, Jinlong and Li, Bingzhou and Zheng, Zeyu and Xie, Cihang and Yao, Huaxiu},
  journal={arXiv preprint arXiv:2604.04202},
  year={2026}
}
```

---

## 📄 Licence

Ce projet est distribué sous la [Licence MIT](../LICENSE).
