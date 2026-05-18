# Clawarena-v4 — Stats Report (openclaw)

_Tokenizer: `cl100k_base`_

## 1. Overall Summary

- **Scenarios:** 12
- **Total rounds:** 337
- **Rounds with pref:** 24 (7.1%)
- **Rounds with updates:** 45 (13.4%)
- **Total updates:** 83 (107 files)
- **Total tokens:** 4,739,550

## 2. Token Distribution

| Category | Tokens | % |
|----------|-------:|--:|
| Main Session | 10,457 | 0.2% |
| History Sessions | 158,090 | 3.3% |
| Workspace | 1,483,834 | 31.3% |
| Questions | 101,881 | 2.1% |
| Feedback | 64,271 | 1.4% |
| Pref | 1,709 | 0.0% |
| Update (Session) | 122,271 | 2.6% |
| Update (Workspace) | 2,797,037 | 59.0% |
| **Total** | **4,739,550** | **100.0%** |

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
| group | 4 | 4.8% |
| session | 37 | 44.6% |
| workspace | 42 | 50.6% |

![Update Type](chart_update_type_pie.png)

### 4.2 Action Distribution

| Action | Files | % |
|--------|------:|--:|
| append | 14 | 56.0% |
| new | 11 | 44.0% |

![Update Action](chart_update_action_pie.png)

### 4.3 Files per Update

- **Mean:** 1.29, **Min:** 0, **Max:** 4
- **Total update files:** 107

## 5. Per-Scenario Breakdown

| Scenario | Rounds | MC | EC | w/Pref | w/Upd | Updates | UpdFiles | WSFiles | Tokens |
|----------|-------:|---:|---:|-------:|------:|--------:|---------:|--------:|-------:|
| hil_s1 | 24 | 8 | 16 | 3 | 4 | 8 | 25 | 24 | 4,344,165 |
| hil_f3 | 30 | 8 | 22 | 2 | 4 | 6 | 7 | 11 | 34,061 |
| hil_g3 | 30 | 8 | 22 | 0 | 4 | 6 | 7 | 7 | 30,474 |
| hil_d3 | 30 | 8 | 22 | 2 | 4 | 8 | 10 | 12 | 44,137 |
| hil_i2 | 30 | 8 | 22 | 2 | 4 | 7 | 7 | 10 | 30,940 |
| hil_g1 | 30 | 8 | 22 | 3 | 4 | 7 | 8 | 10 | 36,077 |
| hil_j1 | 30 | 8 | 22 | 2 | 4 | 5 | 6 | 8 | 34,823 |
| hil_f7 | 27 | 8 | 19 | 2 | 4 | 11 | 7 | 10 | 28,084 |
| hil_g4 | 27 | 8 | 19 | 2 | 3 | 7 | 8 | 10 | 37,429 |
| hil_c7 | 28 | 8 | 20 | 2 | 3 | 6 | 9 | 12 | 44,210 |
| hil_h3 | 27 | 8 | 19 | 2 | 4 | 6 | 7 | 10 | 35,038 |
| hil_e4 | 24 | 7 | 17 | 2 | 3 | 6 | 6 | 11 | 40,112 |

![Question Type Stacked](chart_qtype_stacked.png)

![Updates Stacked](chart_update_stacked.png)

## 6. Per-Scenario Token Detail

| Scenario | Main Session | History Sessions | Workspace | Questions | Feedback | Pref | Update (Session) | Update (Workspace) | Total |
|----------|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| hil_s1 | 432 | 60,236 | 1,422,316 | 4,200 | 3,327 | 326 | 86,806 | 2,766,522 | 4,344,165 |
| hil_f3 | 914 | 5,616 | 8,097 | 9,855 | 4,678 | 97 | 2,600 | 2,204 | 34,061 |
| hil_g3 | 2,354 | 4,014 | 3,186 | 10,846 | 6,551 | 0 | 1,388 | 2,135 | 30,474 |
| hil_d3 | 737 | 11,305 | 6,928 | 9,692 | 6,186 | 191 | 4,577 | 4,521 | 44,137 |
| hil_i2 | 1,021 | 5,133 | 6,247 | 7,124 | 5,228 | 194 | 2,770 | 3,223 | 30,940 |
| hil_g1 | 593 | 10,768 | 5,174 | 6,105 | 4,933 | 196 | 4,991 | 3,317 | 36,077 |
| hil_j1 | 668 | 5,777 | 4,222 | 10,912 | 8,510 | 179 | 2,901 | 1,654 | 34,823 |
| hil_f7 | 816 | 4,937 | 5,124 | 8,622 | 5,675 | 111 | 1,135 | 1,664 | 28,084 |
| hil_g4 | 742 | 6,900 | 6,256 | 10,349 | 4,940 | 121 | 5,037 | 3,084 | 37,429 |
| hil_c7 | 640 | 18,625 | 5,930 | 7,220 | 4,870 | 92 | 3,538 | 3,295 | 44,210 |
| hil_h3 | 835 | 8,568 | 4,124 | 11,206 | 4,866 | 102 | 3,271 | 2,066 | 35,038 |
| hil_e4 | 705 | 16,211 | 6,230 | 5,750 | 4,507 | 100 | 3,257 | 3,352 | 40,112 |

![Token Stacked](chart_token_stacked.png)

## 7. Top-N Rankings

### Top 10 by Tokens

| Rank | Scenario | Tokens |
|-----:|----------|------:|
| 1 | hil_s1 | 4,344,165 |
| 2 | hil_c7 | 44,210 |
| 3 | hil_d3 | 44,137 |
| 4 | hil_e4 | 40,112 |
| 5 | hil_g4 | 37,429 |
| 6 | hil_g1 | 36,077 |
| 7 | hil_h3 | 35,038 |
| 8 | hil_j1 | 34,823 |
| 9 | hil_f3 | 34,061 |
| 10 | hil_i2 | 30,940 |

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
| 1 | hil_f7 | 11 |
| 2 | hil_s1 | 8 |
| 3 | hil_d3 | 8 |
| 4 | hil_i2 | 7 |
| 5 | hil_g1 | 7 |
| 6 | hil_g4 | 7 |
| 7 | hil_f3 | 6 |
| 8 | hil_g3 | 6 |
| 9 | hil_c7 | 6 |
| 10 | hil_h3 | 6 |

![Top by Tokens](chart_top_tokens.png)

![Complexity](chart_complexity_scatter.png)

