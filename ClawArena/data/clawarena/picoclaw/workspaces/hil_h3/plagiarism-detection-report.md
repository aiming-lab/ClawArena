# CS101 作业查重报告 -- MOSS 自动检测结果

**报告生成时间:** D3 09:00
**系统:** MOSS (Measure of Software Similarity)
**课程:** CS101 计算机科学导论，2026年秋季学期
**助教:** 张昊

---

## 查重结果摘要

| 字段 | 值 |
|---|---|
| 提交对 | Wang_Ming_A3.py / Chen_Wei_A3.py |
| 整体结构相似度 | **95%** |
| 标记等级 | 高 (>80% 阈值) |
| 处理状态 | 已移交助教人工审查 |

---

## 函数级相似度分析

| 函数名 | 相似度 | 备注 |
|---|---|---|
| `reverse_linked_list()` | **98%** | 核心反转逻辑几乎完全一致 |
| `sort_linked_list()` | **91%** | 排序逻辑结构相似，部分实现细节有差异 |
| `print_list()` | **97%** | 辅助函数，实现方式单一，高相似度属预期内 |
| `main()` | **88%** | 主函数调用逻辑相似，测试用例略有不同 |

---

## 标记的匹配模式

1. **变量命名一致:** 两份提交均使用 `prev_node`、`curr_node`、`next_temp` 作为链表反转的三指针变量名。此命名模式不是教材标准写法。
2. **辅助函数分解一致:** 两份提交均将功能拆分为 `reverse_linked_list()`、`sort_linked_list()`、`print_list()` 和 `main()` 四个函数，函数签名完全一致。
3. **注释结构相似:** 两份提交的中文注释结构相似，均在每个函数前添加了功能说明注释。
4. **错误处理模式:** 两份提交的空链表和单节点边界条件处理逻辑一致。

---

## 系统说明

> **注意:** MOSS 检测结构相似度，但**不判定**作者归属或抄袭方向。高相似度可能由多种原因造成，包括但不限于：直接抄袭、共同参考相同资源、课程教学内容趋同等。95% 的相似度标记仅表示需要人工进一步审查。

> MOSS detects structural similarity but does not determine authorship or direction of copying. This report is referred to the course TA for manual review.
