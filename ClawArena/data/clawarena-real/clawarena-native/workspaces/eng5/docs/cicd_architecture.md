# CI/CD 架构文档 / CI/CD Architecture Documentation

## 概述 / Overview

本文档描述公司 CI/CD 体系的整体架构，包含 GitHub Actions（主仓库）和 GitLab CI（基础设施仓库）两套系统的设计原则、配置规范和最佳实践。

This document describes the overall architecture of the company's CI/CD system, covering both GitHub Actions (main repository) and GitLab CI (infrastructure repository) design principles, configuration standards, and best practices.

## GitHub Actions 体系 / GitHub Actions System

### 工作流文件结构 / Workflow File Structure

所有 GitHub Actions 工作流文件位于 `.github/workflows/` 目录下：

```
.github/workflows/
├── ci.yml          # 主 CI 流水线（构建、测试、代码审查）
├── deploy.yml      # 生产环境部署（OIDC 认证）
├── release.yml     # 多平台发版构建（矩阵策略）
└── nightly.yml     # 夜间安全扫描与性能测试
```

### 缓存策略 / Cache Strategy

GitHub Actions 缓存策略遵循官方最佳实践：

**正确的 cache key 格式：**
```yaml
- name: Cache Node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-build-
      ${{ runner.os }}-
```

关键原则：
1. cache key 必须使用 `hashFiles()` 函数，确保依赖变更时缓存自动失效
2. `github.sha` 不适合用作 cache key（每次提交不同，导致永远 cache miss）
3. cache key 最大长度：512 个字符
4. restore-keys 从最具体到最宽泛排列
5. 单仓库默认缓存上限：10 GB
6. 未使用缓存保留期：7 天
7. 上传速率限制：200 次/分钟
8. 下载速率限制：1500 次/分钟

**版本要求：**
- actions/cache v1/v2 已于 2025 年 3 月 1 日停服
- 最低兼容版本：v4.2.0 或 v3.4.0
- Self-hosted runner 最低版本要求：2.320.1

### 并发控制 / Concurrency Control

```yaml
# 正确示例 - 允许的组合
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# 正确示例 - queue: max（不含 cancel-in-progress）
concurrency:
  group: production-deploy
  queue: max

# 错误示例 - 禁止组合
# queue: max + cancel-in-progress: true → 导致 validation error
concurrency:
  group: nightly-build
  cancel-in-progress: true  # FORBIDDEN with queue: max
  queue: max                # FORBIDDEN with cancel-in-progress: true
```

queue: max 的最大 pending runs 数量为 100。

### 权限配置 / Permissions Configuration

OIDC 部署 job 必须配置 `id-token: write` 权限：

```yaml
jobs:
  deploy:
    permissions:
      id-token: write     # 必须：OIDC JWT 生成
      contents: read      # 通常同时需要
      deployments: write  # April 1, 2025 后必须为 write（不再允许 read）
```

完整权限 scope 列表：
actions, attestations, checks, contents, deployments, id-token, issues, packages,
pages, pull-requests, security-events, statuses

未声明的 scope 默认为 `none`。

### 矩阵策略 / Matrix Strategy

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    version: [12, 16, 20]
    exclude:
      # 正确：完整组合对象
      - os: windows-latest
        version: 12
      - os: windows-latest
        version: 14
      # 错误：只指定 os 字段（行为不可预测）
      # - os: windows-latest  ← 不要这样写
```

`fail-fast` 默认值为 `true`（任意 job 失败即取消其余）。



## GitHub Actions 高级配置第 1 节 / Advanced Configuration Section 1

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于权限管理的高级配置模式。

In this section we cover advanced patterns for permission management in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 1
name: Example Workflow 1
on:
  push:
    branches: [main]

jobs:
  example-job-1:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 1
        run: echo "Running step 1"
        env:
          EXAMPLE_VAR: "value_1"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 2 节 / Advanced Configuration Section 2

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于矩阵构建的高级配置模式。

In this section we cover advanced patterns for matrix builds in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 2
name: Example Workflow 2
on:
  push:
    branches: [main]

jobs:
  example-job-2:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 2
        run: echo "Running step 2"
        env:
          EXAMPLE_VAR: "value_2"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 3 节 / Advanced Configuration Section 3

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于缓存优化的高级配置模式。

In this section we cover advanced patterns for cache optimization in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 3
name: Example Workflow 3
on:
  push:
    branches: [main]

jobs:
  example-job-3:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 3
        run: echo "Running step 3"
        env:
          EXAMPLE_VAR: "value_3"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 4 节 / Advanced Configuration Section 4

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于权限管理的高级配置模式。

In this section we cover advanced patterns for permission management in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 4
name: Example Workflow 4
on:
  push:
    branches: [main]

jobs:
  example-job-4:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 4
        run: echo "Running step 4"
        env:
          EXAMPLE_VAR: "value_4"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 5 节 / Advanced Configuration Section 5

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于矩阵构建的高级配置模式。

In this section we cover advanced patterns for matrix builds in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 5
name: Example Workflow 5
on:
  push:
    branches: [main]

jobs:
  example-job-5:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 5
        run: echo "Running step 5"
        env:
          EXAMPLE_VAR: "value_5"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 6 节 / Advanced Configuration Section 6

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于缓存优化的高级配置模式。

In this section we cover advanced patterns for cache optimization in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 6
name: Example Workflow 6
on:
  push:
    branches: [main]

jobs:
  example-job-6:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 6
        run: echo "Running step 6"
        env:
          EXAMPLE_VAR: "value_6"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 7 节 / Advanced Configuration Section 7

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于权限管理的高级配置模式。

In this section we cover advanced patterns for permission management in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 7
name: Example Workflow 7
on:
  push:
    branches: [main]

jobs:
  example-job-7:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 7
        run: echo "Running step 7"
        env:
          EXAMPLE_VAR: "value_7"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 8 节 / Advanced Configuration Section 8

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于矩阵构建的高级配置模式。

In this section we cover advanced patterns for matrix builds in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 8
name: Example Workflow 8
on:
  push:
    branches: [main]

jobs:
  example-job-8:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 8
        run: echo "Running step 8"
        env:
          EXAMPLE_VAR: "value_8"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 9 节 / Advanced Configuration Section 9

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于缓存优化的高级配置模式。

In this section we cover advanced patterns for cache optimization in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 9
name: Example Workflow 9
on:
  push:
    branches: [main]

jobs:
  example-job-9:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 9
        run: echo "Running step 9"
        env:
          EXAMPLE_VAR: "value_9"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 10 节 / Advanced Configuration Section 10

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于权限管理的高级配置模式。

In this section we cover advanced patterns for permission management in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 10
name: Example Workflow 10
on:
  push:
    branches: [main]

jobs:
  example-job-10:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 10
        run: echo "Running step 10"
        env:
          EXAMPLE_VAR: "value_10"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 11 节 / Advanced Configuration Section 11

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于矩阵构建的高级配置模式。

In this section we cover advanced patterns for matrix builds in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 11
name: Example Workflow 11
on:
  push:
    branches: [main]

jobs:
  example-job-11:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 11
        run: echo "Running step 11"
        env:
          EXAMPLE_VAR: "value_11"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 12 节 / Advanced Configuration Section 12

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于缓存优化的高级配置模式。

In this section we cover advanced patterns for cache optimization in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 12
name: Example Workflow 12
on:
  push:
    branches: [main]

jobs:
  example-job-12:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 12
        run: echo "Running step 12"
        env:
          EXAMPLE_VAR: "value_12"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 13 节 / Advanced Configuration Section 13

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于权限管理的高级配置模式。

In this section we cover advanced patterns for permission management in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 13
name: Example Workflow 13
on:
  push:
    branches: [main]

jobs:
  example-job-13:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 13
        run: echo "Running step 13"
        env:
          EXAMPLE_VAR: "value_13"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）



## GitHub Actions 高级配置第 14 节 / Advanced Configuration Section 14

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于矩阵构建的高级配置模式。

In this section we cover advanced patterns for matrix builds in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario 14
name: Example Workflow 14
on:
  push:
    branches: [main]

jobs:
  example-job-14:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step 14
        run: echo "Running step 14"
        env:
          EXAMPLE_VAR: "value_14"
```

#### 注意事项 / Important Notes

1. 确保所有权限声明完整且最小化 / Ensure all permission declarations are complete and minimal
2. 使用 hashFiles() 生成稳定的 cache key / Use hashFiles() for stable cache keys
3. 避免在 restore-keys 中过度指定 / Avoid over-specification in restore-keys
4. 测试环境中使用 workflow_dispatch 触发器 / Use workflow_dispatch trigger in test environments

#### 常见错误 / Common Mistakes

- 使用 `github.sha` 作为 cache key（导致每次 miss）
- 忘记 `id-token: write` 权限（OIDC 失败）
- 使用已废弃的 `actions/cache@v2`（2025-03-01 后失败）
- 矩阵 exclude 只指定部分字段（行为不明确）

