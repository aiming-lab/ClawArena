# Git Commit History -- Chen Wei (陈伟) UESTC GitLab + GitHub

**导出来源:**
1. UESTC GitLab: `chenwei/cs101-hw` (私有仓库)
2. GitHub: `chenwei-dev/algorithm-practice` (公开仓库，创建于3个月前)

**作业:** CS101 Assignment 3 -- 链表反转与排序

---

## GitLab Commit 记录 (3 commits, D-1 至 D2)

```
f1a2b3c  D-1 20:00:44 +0800  initial commit: linked list assignment
g4c5d6e  D1  19:22:11 +0800  refactor: clean up variable names
h7e8f9a  D2  00:55:38 +0800  final: add header comments for submission
```

---

## GitLab Commit 详情

### Commit f1a2b3c (D-1 20:00)
- **一次性提交完整实现**: 链表反转 + 排序 + 辅助函数 + main
- 包含 `reverse_linked_list()` 使用 `prev_node`/`curr_node`/`next_temp`
- 包含 `sort_linked_list()` 使用插入排序
- 包含 `print_list()` 和 `main()`

### Commit g4c5d6e (D1 19:22)
- 小幅变量重命名和格式调整
- 无实质性功能变更

### Commit h7e8f9a (D2 00:55)
- 添加头部注释准备提交
- 最终提交时间: D2 01:15 (通过课程提交系统)

---

## GitHub 记录

| 字段 | 值 |
|---|---|
| 仓库 | `chenwei-dev/algorithm-practice` |
| 权限 | **公开** |
| 创建时间 | 3个月前 |
| 相关 Push | D1 22:30:15 +0800 |
| Commit Message | "add linked list reversal assignment solution" |
| 说明 | GitHub push 为 GitLab 代码的副本，非独立开发线 |

---

## 时间线对比

| 事件 | Wang Ming | Chen Wei |
|---|---|---|
| 第一个 GitLab commit | **D-2 14:22** | D-1 20:00 |
| GitHub push | 无 (私有仓库) | D1 22:30 |
| 最后一个 commit | D1 23:30 | D2 00:55 |
| 课程系统提交 | D1 23:50 | D2 01:15 |

**时间差:** Wang Ming 的第一个 commit (D-2 14:22) 比 Chen Wei 的第一个 GitLab commit (D-1 20:00) 早约 **30 小时**，比 Chen Wei 的 GitHub push (D1 22:30) 早约 **56 小时**。

---

## 开发模式分析

- **Chen Wei GitLab:** 3 次提交，首次提交即为完整实现（非增量开发模式）
- **Chen Wei GitHub:** 为 GitLab 代码的复制推送，非独立开发
- **仓库权限:** GitLab 私有，GitHub **公开** (任何人可查看)
