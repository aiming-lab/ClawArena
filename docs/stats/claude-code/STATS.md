# Clawarena-v4 — Stats Report (claude-code)

_Tokenizer: `cl100k_base`_

## 1. Overall Summary

- **Scenarios:** 12
- **Total rounds:** 337
- **Rounds with pref:** 24 (7.1%)
- **Rounds with updates:** 45 (13.4%)
- **Total updates:** 79 (107 files)
- **Total tokens:** 4,733,327

## 2. Token Distribution

| Category | Tokens | % |
|----------|-------:|--:|
| Main Session | 4,170 | 0.1% |
| History Sessions | 167,139 | 3.5% |
| Workspace | 1,472,224 | 31.1% |
| Questions | 101,881 | 2.2% |
| Feedback | 64,271 | 1.4% |
| Pref | 1,709 | 0.0% |
| Update (Session) | 124,800 | 2.6% |
| Update (Workspace) | 2,797,133 | 59.1% |
| **Total** | **4,733,327** | **100.0%** |

![Token Distribution](chart_token_pie.png)

## 3. Question Statistics

### 3.1 Type Distribution

| Type | Count | % |
|------|------:|--:|
| exec_check | 242 | 71.8% |
| multi_choice | 95 | 28.2% |

![Question Type](chart_qtype_pie.png)

### 3.2 MC Shape

| Metric | Mean | Min | Max |
|--------|-----:|----:|----:|
| Options per question | 6.38 | 5 | 10 |
| Answers per question | 4.46 | 2 | 8 |

- **Single-answer rounds:** 0 (0.0%)
- **Multi-answer rounds:** 95 (100.0%)

![MC Options](chart_mc_options_hist.png)

![MC Answers](chart_mc_answers_hist.png)

### 3.3 EC Features

| Feature | Rounds | Coverage |
|---------|-------:|---------:|
| expect_exit | 242 | 100.0% |
| expect_stdout | 1 | 0.4% |
| regex matching | 0 | 0.0% |
| timeout | 242 | 100.0% |

_Timeout (s) — mean 40.2, min 30.0, max 60.0._

![EC Features](chart_ec_features.png)

### 3.4 Pref Coverage

- **Rounds with pref:** 24 (7.1%)

![Pref Coverage](chart_pref_coverage.png)

## 4. Update Statistics

### 4.1 Type Distribution

| Type | Count | % |
|------|------:|--:|
| session | 37 | 46.8% |
| workspace | 42 | 53.2% |

![Update Type](chart_update_type_pie.png)

### 4.3 Files per Update

- **Mean:** 1.35, **Min:** 1, **Max:** 4
- **Total update files:** 107

## 5. Per-Scenario Breakdown

| Scenario | Rounds | MC | EC | w/Pref | w/Upd | Updates | UpdFiles | WSFiles | Tokens |
|----------|-------:|---:|---:|-------:|------:|--------:|---------:|--------:|-------:|
| hil_s1 | 24 | 8 | 16 | 3 | 4 | 8 | 25 | 21 | 4,330,265 |
| hil_f3 | 30 | 8 | 22 | 2 | 4 | 6 | 7 | 8 | 34,443 |
| hil_g3 | 30 | 8 | 22 | 0 | 4 | 6 | 7 | 4 | 28,913 |
| hil_d3 | 30 | 8 | 22 | 2 | 4 | 8 | 10 | 9 | 45,230 |
| hil_i2 | 30 | 8 | 22 | 2 | 4 | 7 | 7 | 7 | 30,854 |
| hil_g1 | 30 | 8 | 22 | 3 | 4 | 7 | 8 | 7 | 36,445 |
| hil_j1 | 30 | 8 | 22 | 2 | 4 | 5 | 6 | 5 | 35,192 |
| hil_f7 | 27 | 8 | 19 | 2 | 4 | 7 | 7 | 7 | 28,765 |
| hil_g4 | 27 | 8 | 19 | 2 | 3 | 7 | 8 | 7 | 38,336 |
| hil_c7 | 28 | 8 | 20 | 2 | 3 | 6 | 9 | 9 | 46,300 |
| hil_h3 | 27 | 8 | 19 | 2 | 4 | 6 | 7 | 7 | 36,792 |
| hil_e4 | 24 | 7 | 17 | 2 | 3 | 6 | 6 | 8 | 41,792 |

![Question Type Stacked](chart_qtype_stacked.png)

![Updates Stacked](chart_update_stacked.png)

## 6. Per-Scenario Token Detail

| Scenario | Main Session | History Sessions | Workspace | Questions | Feedback | Pref | Update (Session) | Update (Workspace) | Total |
|----------|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| hil_s1 | 432 | 58,861 | 1,410,594 | 4,200 | 3,327 | 326 | 86,003 | 2,766,522 | 4,330,265 |
| hil_f3 | 0 | 6,514 | 8,144 | 9,855 | 4,678 | 97 | 2,951 | 2,204 | 34,443 |
| hil_g3 | 0 | 4,564 | 3,302 | 10,846 | 6,551 | 0 | 1,515 | 2,135 | 28,913 |
| hil_d3 | 0 | 12,552 | 6,889 | 9,692 | 6,186 | 191 | 5,103 | 4,617 | 45,230 |
| hil_i2 | 0 | 5,667 | 6,394 | 7,124 | 5,228 | 194 | 3,024 | 3,223 | 30,854 |
| hil_g1 | 0 | 11,485 | 5,134 | 6,105 | 4,933 | 196 | 5,275 | 3,317 | 36,445 |
| hil_j1 | 0 | 6,523 | 4,227 | 10,912 | 8,510 | 179 | 3,187 | 1,654 | 35,192 |
| hil_f7 | 816 | 5,540 | 5,126 | 8,622 | 5,675 | 111 | 1,211 | 1,664 | 28,765 |
| hil_g4 | 742 | 7,531 | 6,251 | 10,349 | 4,940 | 121 | 5,318 | 3,084 | 38,336 |
| hil_c7 | 640 | 20,277 | 5,898 | 7,220 | 4,870 | 92 | 4,008 | 3,295 | 46,300 |
| hil_h3 | 835 | 9,894 | 4,073 | 11,206 | 4,866 | 102 | 3,750 | 2,066 | 36,792 |
| hil_e4 | 705 | 17,731 | 6,192 | 5,750 | 4,507 | 100 | 3,455 | 3,352 | 41,792 |

![Token Stacked](chart_token_stacked.png)

## 7. Top-N Rankings

### Top 10 by Tokens

| Rank | Scenario | Tokens |
|-----:|----------|------:|
| 1 | hil_s1 | 4,330,265 |
| 2 | hil_c7 | 46,300 |
| 3 | hil_d3 | 45,230 |
| 4 | hil_e4 | 41,792 |
| 5 | hil_g4 | 38,336 |
| 6 | hil_h3 | 36,792 |
| 7 | hil_g1 | 36,445 |
| 8 | hil_j1 | 35,192 |
| 9 | hil_f3 | 34,443 |
| 10 | hil_i2 | 30,854 |

### Top 10 by Rounds

| Rank | Scenario | Rounds |
|-----:|----------|------:|
| 1 | hil_f3 | 30 |
| 2 | hil_g3 | 30 |
| 3 | hil_d3 | 30 |
| 4 | hil_i2 | 30 |
| 5 | hil_g1 | 30 |
| 6 | hil_j1 | 30 |
| 7 | hil_c7 | 28 |
| 8 | hil_f7 | 27 |
| 9 | hil_g4 | 27 |
| 10 | hil_h3 | 27 |

### Top 10 by Updates

| Rank | Scenario | Updates |
|-----:|----------|------:|
| 1 | hil_s1 | 8 |
| 2 | hil_d3 | 8 |
| 3 | hil_i2 | 7 |
| 4 | hil_g1 | 7 |
| 5 | hil_f7 | 7 |
| 6 | hil_g4 | 7 |
| 7 | hil_f3 | 6 |
| 8 | hil_g3 | 6 |
| 9 | hil_c7 | 6 |
| 10 | hil_h3 | 6 |

![Top by Tokens](chart_top_tokens.png)

![Complexity](chart_complexity_scatter.png)

