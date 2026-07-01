# 运维手册 / Operational Runbook

## 概述 / Overview

本手册提供 CI/CD 系统日常运维的标准操作流程（SOP），包括故障排查、配置变更、紧急回滚等场景。

## 故障排查 / Troubleshooting

### Cache Miss 排查 / Cache Miss Investigation

症状：CI 构建时间异常增长，每次运行都重新安装依赖。

排查步骤：
1. 检查 cache key 是否使用了 `hashFiles()` 函数
2. 确认 `actions/cache` 版本不低于 v4.2.0 或 v3.4.0
3. 验证 restore-keys 从最具体到最宽泛排列
4. 检查单仓库缓存用量是否超过 10 GB 上限

正确的 cache 配置示例：
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-build-
      ${{ runner.os }}-
```

### OIDC 认证失败 / OIDC Authentication Failure

症状：`Error: Could not assume role with OIDC: No OpenIDConnect provider found in your account`

根因：缺少 `id-token: write` 权限声明。

修复：在 job 的 `permissions` 块中添加：
```yaml
permissions:
  id-token: write
  contents: read
```

### Workflow Validation Error / 工作流校验错误

症状：`The workflow is not valid. queue and cancel-in-progress cannot be used together.`

根因：`queue: max` 和 `cancel-in-progress: true` 是禁止组合。

修复方案：
- 选项 A：移除 `queue: max`，保留 `cancel-in-progress: true`（适用于短期 job）
- 选项 B：移除 `cancel-in-progress`，保留 `queue: max`（适用于长期运行的 job）

### GitLab CI Pipeline Error / GitLab CI 流水线错误

症状：`'unit_tests' job needs 'compile' job, but 'compile' does not exist in the pipeline`

根因：`needs` 引用了因 `rules` 条件不满足而被排除的 job。

修复：
```yaml
needs:
  - job: compile
    optional: true
```



## 运维场景 1 / Operational Scenario 1

### 场景描述 / Scenario Description

权限变更流程

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 2 / Operational Scenario 2

### 场景描述 / Scenario Description

Job 超时处理

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 3 / Operational Scenario 3

### 场景描述 / Scenario Description

紧急回滚操作

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 4 / Operational Scenario 4

### 场景描述 / Scenario Description

矩阵构建调优

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 5 / Operational Scenario 5

### 场景描述 / Scenario Description

缓存清理与重置

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 6 / Operational Scenario 6

### 场景描述 / Scenario Description

权限变更流程

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 7 / Operational Scenario 7

### 场景描述 / Scenario Description

Job 超时处理

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 8 / Operational Scenario 8

### 场景描述 / Scenario Description

紧急回滚操作

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 9 / Operational Scenario 9

### 场景描述 / Scenario Description

矩阵构建调优

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 10 / Operational Scenario 10

### 场景描述 / Scenario Description

缓存清理与重置

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 11 / Operational Scenario 11

### 场景描述 / Scenario Description

权限变更流程

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 12 / Operational Scenario 12

### 场景描述 / Scenario Description

Job 超时处理

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 13 / Operational Scenario 13

### 场景描述 / Scenario Description

紧急回滚操作

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 14 / Operational Scenario 14

### 场景描述 / Scenario Description

矩阵构建调优

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 15 / Operational Scenario 15

### 场景描述 / Scenario Description

缓存清理与重置

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 16 / Operational Scenario 16

### 场景描述 / Scenario Description

权限变更流程

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 17 / Operational Scenario 17

### 场景描述 / Scenario Description

Job 超时处理

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 18 / Operational Scenario 18

### 场景描述 / Scenario Description

紧急回滚操作

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 19 / Operational Scenario 19

### 场景描述 / Scenario Description

矩阵构建调优

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 20 / Operational Scenario 20

### 场景描述 / Scenario Description

缓存清理与重置

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 21 / Operational Scenario 21

### 场景描述 / Scenario Description

权限变更流程

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 22 / Operational Scenario 22

### 场景描述 / Scenario Description

Job 超时处理

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 23 / Operational Scenario 23

### 场景描述 / Scenario Description

紧急回滚操作

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```



## 运维场景 24 / Operational Scenario 24

### 场景描述 / Scenario Description

矩阵构建调优

### 操作步骤 / Steps

1. 确认当前状态 / Confirm current state
2. 备份配置文件 / Backup configuration files
3. 执行变更 / Apply changes
4. 验证结果 / Verify results
5. 文档化变更 / Document changes

### 注意事项 / Precautions

- 变更前备份所有相关配置文件
- 在 staging 环境验证后再推到 production
- 记录变更时间和变更人

```bash
# 示例命令 / Example commands
git diff HEAD~1 .github/workflows/
python scripts/validate_workflows.py .
```

