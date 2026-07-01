# 工作流变更历史 / Workflow Change History

## 概述 / Overview

本文档记录所有 CI/CD 工作流配置的变更历史，包括变更时间、变更人、变更内容和变更原因。

This document records all CI/CD workflow configuration change history, including when, who, what, and why.



## 2025-01-15

**变更人 / Author**: Bob
**文件 / File**: `ci.yml`
**变更内容 / Change**: Added caching with actions/cache@v2
**变更原因 / Reason**: Speed up CI by caching node_modules



## 2025-01-20

**变更人 / Author**: Charlie
**文件 / File**: `release.yml`
**变更内容 / Change**: Added matrix strategy for multi-platform builds
**变更原因 / Reason**: Support Windows and macOS builds



## 2025-01-25

**变更人 / Author**: Bob
**文件 / File**: `nightly.yml`
**变更内容 / Change**: Added concurrency control with queue: max
**变更原因 / Reason**: Prevent parallel nightly runs



## 2025-02-01

**变更人 / Author**: Alice
**文件 / File**: `deploy.yml`
**变更内容 / Change**: Added OIDC authentication step
**变更原因 / Reason**: Replace static credentials with OIDC



## 2025-02-10

**变更人 / Author**: David
**文件 / File**: `.gitlab/ci/build.yml`
**变更内容 / Change**: Added cache:key:files with 3 paths
**变更原因 / Reason**: More granular cache invalidation



## 2025-02-15

**变更人 / Author**: Frank
**文件 / File**: `.gitlab/ci/test.yml`
**变更内容 / Change**: Added parallel test jobs
**变更原因 / Reason**: Speed up test suite



## 2025-02-20

**变更人 / Author**: David
**文件 / File**: `.gitlab-ci.yml`
**变更内容 / Change**: Updated artifact expire_in
**变更原因 / Reason**: Reduce storage usage



## 2025-03-01

**变更人 / Author**: Charlie
**文件 / File**: `.github/workflows/nightly.yml`
**变更内容 / Change**: Attempted concurrency fix (incomplete)
**变更原因 / Reason**: Resolve validation errors



## 2024-02-02

**变更人 / Author**: Bob
**文件 / File**: `.github/workflows/$deploy.yml`
**变更内容 / Change**: Historical change 1 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 1
# Before:
#   timeout-minutes: 5
# After:
#   timeout-minutes: 6
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-03-03

**变更人 / Author**: Charlie
**文件 / File**: `.github/workflows/$nightly.yml`
**变更内容 / Change**: Historical change 2 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 2
# Before:
#   timeout-minutes: 10
# After:
#   timeout-minutes: 12
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-04-04

**变更人 / Author**: David
**文件 / File**: `.github/workflows/$ci.yml`
**变更内容 / Change**: Historical change 3 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 3
# Before:
#   timeout-minutes: 15
# After:
#   timeout-minutes: 18
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-05-05

**变更人 / Author**: Alice
**文件 / File**: `.github/workflows/$deploy.yml`
**变更内容 / Change**: Historical change 4 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 4
# Before:
#   timeout-minutes: 20
# After:
#   timeout-minutes: 24
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-06-06

**变更人 / Author**: Bob
**文件 / File**: `.github/workflows/$nightly.yml`
**变更内容 / Change**: Historical change 5 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 5
# Before:
#   timeout-minutes: 25
# After:
#   timeout-minutes: 30
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-07-07

**变更人 / Author**: Charlie
**文件 / File**: `.github/workflows/$ci.yml`
**变更内容 / Change**: Historical change 6 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 6
# Before:
#   timeout-minutes: 30
# After:
#   timeout-minutes: 36
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-08-08

**变更人 / Author**: David
**文件 / File**: `.github/workflows/$deploy.yml`
**变更内容 / Change**: Historical change 7 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 7
# Before:
#   timeout-minutes: 35
# After:
#   timeout-minutes: 42
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-09-09

**变更人 / Author**: Alice
**文件 / File**: `.github/workflows/$nightly.yml`
**变更内容 / Change**: Historical change 8 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 8
# Before:
#   timeout-minutes: 40
# After:
#   timeout-minutes: 48
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-10-10

**变更人 / Author**: Bob
**文件 / File**: `.github/workflows/$ci.yml`
**变更内容 / Change**: Historical change 9 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 9
# Before:
#   timeout-minutes: 45
# After:
#   timeout-minutes: 54
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-11-11

**变更人 / Author**: Charlie
**文件 / File**: `.github/workflows/$deploy.yml`
**变更内容 / Change**: Historical change 10 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 10
# Before:
#   timeout-minutes: 50
# After:
#   timeout-minutes: 60
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-12-12

**变更人 / Author**: David
**文件 / File**: `.github/workflows/$nightly.yml`
**变更内容 / Change**: Historical change 11 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 11
# Before:
#   timeout-minutes: 55
# After:
#   timeout-minutes: 66
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-01-13

**变更人 / Author**: Alice
**文件 / File**: `.github/workflows/$ci.yml`
**变更内容 / Change**: Historical change 12 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 12
# Before:
#   timeout-minutes: 60
# After:
#   timeout-minutes: 72
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-02-14

**变更人 / Author**: Bob
**文件 / File**: `.github/workflows/$deploy.yml`
**变更内容 / Change**: Historical change 13 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 13
# Before:
#   timeout-minutes: 65
# After:
#   timeout-minutes: 78
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-03-15

**变更人 / Author**: Charlie
**文件 / File**: `.github/workflows/$nightly.yml`
**变更内容 / Change**: Historical change 14 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 14
# Before:
#   timeout-minutes: 70
# After:
#   timeout-minutes: 84
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-04-16

**变更人 / Author**: David
**文件 / File**: `.github/workflows/$ci.yml`
**变更内容 / Change**: Historical change 15 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 15
# Before:
#   timeout-minutes: 75
# After:
#   timeout-minutes: 90
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-05-17

**变更人 / Author**: Alice
**文件 / File**: `.github/workflows/$deploy.yml`
**变更内容 / Change**: Historical change 16 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 16
# Before:
#   timeout-minutes: 80
# After:
#   timeout-minutes: 96
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-06-18

**变更人 / Author**: Bob
**文件 / File**: `.github/workflows/$nightly.yml`
**变更内容 / Change**: Historical change 17 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 17
# Before:
#   timeout-minutes: 85
# After:
#   timeout-minutes: 102
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-07-19

**变更人 / Author**: Charlie
**文件 / File**: `.github/workflows/$ci.yml`
**变更内容 / Change**: Historical change 18 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 18
# Before:
#   timeout-minutes: 90
# After:
#   timeout-minutes: 108
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.



## 2024-08-20

**变更人 / Author**: David
**文件 / File**: `.github/workflows/$deploy.yml`
**变更内容 / Change**: Historical change 19 — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change 19
# Before:
#   timeout-minutes: 95
# After:
#   timeout-minutes: 114
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.

