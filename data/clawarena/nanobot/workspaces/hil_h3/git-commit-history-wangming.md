# Git Commit History -- Wang Ming (王明) UESTC GitLab

**仓库:** `wangming/cs101-assignments` (私有仓库)
**平台:** UESTC GitLab
**导出命令:** `git log --oneline --format="%H %ai %s"`
**作业:** CS101 Assignment 3 -- 链表反转与排序

---

## Commit 记录 (5 commits, D-2 至 D1)

```
a3f2c1d  D-2 14:22:08 +0800  init: add linked list node struct and basic test
b7e4a2f  D-2 21:15:33 +0800  feat: implement reverse_linked_list with three-pointer
c9d1b3e  D-1 10:45:12 +0800  feat: add sort_linked_list using insertion sort
d2f5c4a  D1  16:30:47 +0800  fix: edge case for empty list and single node
e8a3d5b  D1  23:30:22 +0800  cleanup: add comments and format code for submission
```

---

## Commit 详情

### Commit a3f2c1d (D-2 14:22)
- 初始化项目骨架
- 定义 `Node` 类和基本测试用例
- 创建空的 `reverse_linked_list()`、`sort_linked_list()` 函数桩
- 添加 `print_list()` 辅助函数

### Commit b7e4a2f (D-2 21:15)
- 实现核心反转逻辑
- 使用三指针技术: `prev_node`, `curr_node`, `next_temp`
- 添加基本的反转测试用例

### Commit c9d1b3e (D-1 10:45)
- 实现 `sort_linked_list()` 使用插入排序
- 这部分是独立实现，非来自反转参考

### Commit d2f5c4a (D1 16:30)
- 修复空链表和单节点的边界条件
- 添加错误处理逻辑

### Commit e8a3d5b (D1 23:30)
- 添加中文注释
- 格式化代码准备提交
- 最终提交时间: D1 23:50 (通过课程提交系统)

---

## 开发模式分析

- **增量开发:** 5 次提交跨 3 天，每次提交添加不同功能
- **逐步构建:** 骨架 -> 核心功能 -> 排序 -> Bug修复 -> 清理
- **时间分布:** D-2 (2次), D-1 (1次), D1 (2次)
- **仓库权限:** 私有 (仅 Wang Ming 可访问)
