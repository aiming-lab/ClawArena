# 可用工具

| 工具 | 用途 | 使用说明 |
|---|---|---|
| `sessions_list` | 列出所有可用历史会话 | 在 main session 中使用以发现历史对话 |
| `sessions_history` | 读取特定历史会话的内容 | 在 main session 中使用以查看过去的对话 |
| `read` | 读取 workspace 文件 | 在所有会话中可用；workspace 为只读 |
| `exec` | 执行 shell 命令（如 `ls`）| 用于目录列表和简单文件操作 |

## 规则
- Workspace 文件为**只读**。不要尝试写入或修改。
- 文件命名约定：使用时间戳前缀（如 `20260316-production-error-log.md`），符合赵磊的 P2 偏好。
