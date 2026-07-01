# Data Augmentation Plan v3

> 基于 v2 的修订。本文为整体性大方向计划，各场景子计划后续单独细化。

---

## 一、核心指标目标

| 指标 | 目标值 | 参照（hil_s1） |
|------|--------|--------------|
| 总轮数 | 30 轮上下浮动（±4） | 66 轮 |
| EC 比例 | ≥ 70% | 71.2%（47/66） |
| MC 轮数 | ~8–10 轮 | 19 轮 |
| Update 间距 | 各 update 间均匀分布，密集 update 之间需插入足够 EC | q13/q26/q40/q53（每段 ≈13 轮） |

---

## 二、题目结构原则

### 2.1 MC 的定位

MC 轮数少而精，集中在三类位置：
1. **场景开篇**（最初 2–3 轮）：建立基线认知，介绍核心矛盾
2. **每个 update 触发轮**（update_ids 非空的那一轮）：认知更新检验
3. **综合收尾**（最后 1–2 轮）：元认知或最终综合判断

其余大量轮次均为 EC，承担主要评测权重。

### 2.2 EC 的布局

- EC 不集中在末尾，与 MC 穿插分布于全流程
- 每个 update 前后均有 EC：update 前的 EC 基于现有信息产出，update 后的 EC 利用新信息深化产出
- 密集 update 区段（如原始 questions.json 中 q4–q9 连续 4 个 update）：重新设计时在各 update 之间插入 1–2 道 EC，拉开间距，避免认知更新过于集中

### 2.3 update_ids 的位置设计

原始 questions.json 的 update 触发位置是按 30 轮 MC-only 设计的，现在重新设计后轮数结构会变化。**重新设计时将 4 个 update 均匀分散在全程**，约每 6–8 轮触发一次（对应 30 轮总体），确保每段都有足够的 EC 空间。

---

## 三、pref 字段使用规范

参照 hil_s1 实际用法：

**前期（update1 前后，约前 1/3 轮）**：部分 EC 题含 `pref` 字段
- pref 里的偏好检查结果**不计入得分**，仅附加反馈文本
- 作用：教学期，让 agent 了解自己的格式是否符合用户偏好

**后期（update3/4 后，约后 1/3 轮）**：不再设 `pref` 字段
- 偏好检查逻辑移入 `eval.command`，**计入得分**
- 评测静默：agent 不再收到额外偏好反馈，表现全凭之前的学习

**边界**：pref 字段仅出现在 EC 题上（MC 无需偏好检查）；全场景 pref 字段约出现 4–6 次，集中在前两个 update 区间内。

---

## 四、评测脚本规范

### 4.1 禁止共享脚本目录

- **禁止** `eval/_shared/` 等跨场景公共目录
- 每个场景的所有评测脚本均放在 `eval/{scene_id}/scripts/` 下
- 若某脚本逻辑两场景雷同，各自复制一份，独立维护

### 4.2 脚本目录结构

```
eval/{scene_id}/
├── questions.json
└── scripts/
    ├── check_*.py          # 评测脚本（验证 agent 产物）
    ├── check_preferences.py # 偏好检查（各场景独立版本）
    ├── validation_utils.py  # 本场景内部工具（如需要）
    ├── schemas/             # JSON schema 文件（如需要）
    └── tests/               # agent 须通过的单元测试（L3 题用）
        └── test_*.py
```

### 4.3 难度分级

- **L2**：调用 `scripts/check_*.py`，验证多文件 + 具体数值 + 结构要求（3+ 个场景内确定数值）；可在 `eval.command` 中用 `&&` 附加 inline 的简单前置检查（如文件存在、非空）作为快速失败条件
- **L3**：agent 须自行创建 Python 脚本文件（从零开始，依据 workspace .md 文档理解后编写），评测运行其脚本输出，或评测运行 `scripts/tests/test_*.py`；agent 须自行创建必要的目录结构

> **注**：所有 EC 题至少达到 L2。纯 L1（只有 `test -f` + `grep` 的 inline command）对现代大模型几乎无难度，不单独作为一道题存在；L1 级检查只能作为 L2 command 的前置 `&&` 短路条件附加使用。

---

## 五、密集 update 场景的处理策略

针对 hil_d3（4 个 update 集中在 q4–q9）、hil_g3（upd1/upd2/upd3 集中在 q5–q7）等密集区段：

- **不受原始 update 触发轮次约束**：重新设计 questions.json 时，在 update 前插入若干 EC 题，将密集 update 间距拉开
- 例：原来 upd2@q7、upd3@q8 相邻，重新设计后中间插入 2–3 道 EC，变成 upd2@q8、upd3@q12
- 目标：每两个相邻 update 之间至少有 4–5 轮题目（其中至少 3 轮 EC）

---

## 六、各场景概况

| 场景 | 核心 EC 类型 | Update 密集度 | 偏好风格 |
|------|------------|-------------|---------|
| hil_f3（时区事件） | 代码/脚本创建、JSON 生成、报告写作 | 均匀（每段 ≈6 轮） | 赵磊：表格+JSON，ISO 时间，简洁定量 |
| hil_d3（排班危机） | 统计脚本、数据对比表、合规报告 | 密集（需重新分散） | Tanaka：精确小时数、医学术语、方法论优先 |
| hil_i2（数据重用） | 数据集对比脚本、反驳文档、学术回应 | 均匀 | Lin Yi：结论优先、日期+患者ID命名 |
| hil_g1（背景核查） | GitHub 分析脚本、差异矩阵、评估报告 | 均匀 | Chen Jing：要点+中文命名、执行摘要优先 |
| hil_j1（品牌欺诈） | 夸大率计算脚本、合同分析、证据链 | 前两个 update 紧邻（需分散） | 周芳：emoji 命名、活泼风格、数据优先 |
| hil_g3（薪资泄露） | 日志解析脚本、跨渠道审计、概率报告 | 密集（需重新分散） | Chen Jing：中文命名、执行摘要、专业温暖 |

---

## 七、实施顺序

每个场景的子计划由用户逐步指导细化，执行时按以下顺序推进：

1. **hil_f3**：代码/脚本创建类 EC 最典型，建立评测脚本范式
2. **hil_g3**：日志解析类，workspace 文件较少，脚本逻辑清晰
3. **hil_d3**：统计类，update 密集，验证分散策略是否有效
4. **hil_i2**：数据科学类
5. **hil_g1**：报告生成类
6. **hil_j1**：偏好风格最特殊（周芳 emoji），最后处理

每个场景执行步骤：
1. 细化子计划（题目序列 + update 重新定位 + 脚本清单）
2. 编写 `scripts/` 下的评测脚本与 schema
3. 编写 `eval/{scene_id}/questions.json`
4. `clawarena check` 验证
5. 提交 `data-augment/` 供审阅
6. 审阅通过后迁移至 `data/extended/`

---

## 八、data-augment 目录结构规划

```
data-augment/
├── plan/                          # 计划文档（本目录）
│   ├── v1-plan.md
│   ├── v2-plan.md
│   ├── v3-plan.md                 # 当前版本
│   ├── pre_inject-cleanup.md
│   └── {scene_id}-plan.md        # 各场景子计划（逐步新增）
│
├── eval/                          # 新生成的 questions.json 及评测脚本
│   │                              # 结构与 data/extended/eval/ 完全对应，
│   │                              # 审阅通过后整体迁移
│   ├── hil_f3/
│   │   ├── questions.json
│   │   └── scripts/
│   │       ├── check_*.py
│   │       ├── check_preferences.py
│   │       ├── validation_utils.py
│   │       ├── schemas/
│   │       │   └── *.json
│   │       └── tests/
│   │           └── test_*.py
│   ├── hil_d3/
│   │   └── ...（同上结构）
│   ├── hil_i2/
│   ├── hil_g1/
│   ├── hil_j1/
│   └── hil_g3/
│
└── scratch/                       # 造数据过程中的临时文件
    ├── {scene_id}/                # 各场景独立子目录，互不干扰
    │   ├── notes.md               # 设计笔记、数值核查、草稿
    │   ├── workspace_snapshot.md  # workspace 文件内容摘录（供出题时快速查阅）
    │   └── *.py / *.json          # 辅助脚本、数值计算、schema 草稿
    └── ...
```

**规则说明**：
- `plan/` 只放计划与决策文档，不放任何数据文件
- `eval/` 是最终产物目录，结构与 `data/extended/eval/` 严格对应，迁移时直接 `cp -r`
- `scratch/` 是过程性临时目录，内容不会迁移到正式数据；场景完成后可保留作为造数据记录，也可清理
- 各场景子计划文档命名为 `plan/{scene_id}-plan.md`（如 `plan/hil_f3-plan.md`），内容包含：题目序列设计、update 重新定位、脚本功能清单、关键数值来源
