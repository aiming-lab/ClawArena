# 已知问题列表 / Known Issues List

## 概述 / Overview

本文档维护 CI/CD 系统的已知问题及其状态。

## 高优先级问题 / High Priority Issues

### GH-001: actions/cache v2 废弃
**状态 / Status**: OPEN
**影响 / Impact**: 所有使用 actions/cache@v2 的 workflow 将在 2025-03-01 后自动失败
**根因 / Root Cause**: GitHub 废弃了 v1/v2 版本，最低要求 v3.4.0 或 v4.2.0
**参考 / Reference**: https://github.com/actions/cache/discussions/1510

### GH-002: Cache key 使用 github.sha
**状态 / Status**: OPEN
**影响 / Impact**: 每次提交都会触发 cache miss，CI 时间增加 3-5 分钟
**根因 / Root Cause**: cache key 应使用 hashFiles() 而非 github.sha
**临时方案 / Workaround**: 暂无，需立即修复

### GH-003: nightly.yml 并发控制配置错误
**状态 / Status**: OPEN
**影响 / Impact**: 工作流每次运行都遇到 validation error
**根因 / Root Cause**: queue: max 与 cancel-in-progress: true 的禁止组合
**参考 / Reference**: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency

### GH-004: deploy.yml 缺少 id-token: write 权限
**状态 / Status**: OPEN
**影响 / Impact**: OIDC JWT 无法生成，AWS credentials 配置失败
**根因 / Root Cause**: OIDC 需要 id-token: write 权限
**参考 / Reference**: https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs

### GH-005: release.yml 矩阵 exclude 配置不完整
**状态 / Status**: OPEN
**影响 / Impact**: windows-latest 的所有版本可能被意外排除或不排除
**根因 / Root Cause**: exclude 规则未指定完整的 {os, version} 组合对象

### GL-001: GitLab CI cache:key:files 超过 2 个路径
**状态 / Status**: OPEN
**影响 / Impact**: 构建失败，cache 配置被拒绝
**根因 / Root Cause**: GitLab CI cache:key:files 最多支持 2 个路径
**参考 / Reference**: https://docs.gitlab.com/ci/yaml/

### GL-002: test.yml 中 cache:policy 应为 pull
**状态 / Status**: OPEN
**影响 / Impact**: 并行测试 job 使用 pull-push 导致缓存竞争和不必要的上传
**参考 / Reference**: https://docs.gitlab.com/ci/caching/

### GL-003: unit_test needs 未加 optional: true
**状态 / Status**: OPEN
**影响 / Impact**: 当 compile job 因 rules 条件不运行时，pipeline 报错
**正确做法 / Fix**: needs: [{job: "compile", optional: true}]
**参考 / Reference**: https://docs.gitlab.com/ci/yaml/needs/

### GL-004: artifacts:expire_in 格式非法
**状态 / Status**: OPEN
**影响 / Impact**: 使用 "30d" 格式不被 GitLab CI 识别
**正确做法 / Fix**: 改为 "30 days"
**参考 / Reference**: https://docs.gitlab.com/ci/yaml/

## 低优先级问题 / Low Priority Issues

### GH-006: nightly.yml 中 dependency-audit job 也使用 v2 cache
**状态 / Status**: OPEN
**影响 / Impact**: 同 GH-001

### GL-005: deploy stage 可进一步优化
**状态 / Status**: PLANNING
**影响 / Impact**: 无紧急影响

