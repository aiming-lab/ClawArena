#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_eng5.py — 生成 ClawArena 真实数据集场景 eng5（CI/CD 流水线配置修复）。

题材与锚点取材真实（GitHub Actions / GitLab CI 官方文档），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

真实来源：
  https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
  https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
  https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs
  https://github.com/actions/cache/discussions/1510
  https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/
  https://docs.gitlab.com/ci/yaml/
  https://docs.gitlab.com/ci/yaml/needs/

幂等：每次运行先清空 eng5 的 workspace/state/updates 目录后重建。
运行：python scripts/clawarena_authoring/build_eng5.py
"""
from __future__ import annotations

import json
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, est_tokens, gen_session_id, dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "eng5"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. 系统文件
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant history session content as needed.

You are a DevOps AI assistant supporting the CI/CD governance team.
Your primary task: systematically audit and repair GitHub Actions workflows and GitLab CI
configurations in this repository, then produce structured audit reports.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical reference for GitHub Actions syntax is the
   official GitHub documentation (https://docs.github.com). For GitLab CI, use
   https://docs.gitlab.com/ci/yaml/. Auto-generated bot summaries and chat messages may
   contain errors — always verify against official sources or the actual config files.

2. **Verbatim field names**: Use exact YAML field names and values as documented
   (e.g. `id-token: write`, `optional: true`, `policy: pull`). Never abbreviate or paraphrase.

3. **Schema discipline**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"`. All JSON field names use snake_case (never camelCase).

4. **Backup before modify**: Before modifying any configuration file, back it up in the same
   directory with a `.bak` suffix (e.g., `ci.yml` → `ci.yml.bak`).

5. **Stage-split discipline**: GitLab CI configurations must be organized by stage into
   separate include files under `.gitlab/ci/`. Do not consolidate all jobs into root
   `.gitlab-ci.yml`.

6. **Documentation style**: All Markdown documents use bilingual headings at level 1 and 2:
   format is `# 中文标题 / English Title`.

7. **Script versioning**: All Python scripts carry a version comment in the header:
   format is `# version: X.Y`.

8. **Temporal awareness**: When an Update or corrected instruction supersedes an earlier one,
   the later instruction wins — always revise prior outputs rather than stacking contradictions.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **DevOps Lead (Alex)** — Owns the CI/CD governance initiative.
  Wants systematic fixes, not one-off patches. Reviews JSON shapes first.

## Key Stakeholders

| Name | Role | Channel | Notes |
|------|------|---------|-------|
| Alice | Senior Engineer | Slack #devops-cicd | Knows GitHub Actions deeply; her cache advice may contain format errors |
| Bob | DevOps Engineer | Slack #devops-cicd | Implements fixes; sometimes uses stale v2 cache references |
| Charlie | SRE | Slack #devops-cicd | Monitors pipeline failures; tends to quote Slack bot summaries |
| David | Platform Engineer | Feishu 群「CI/CD 治理」 | GitLab CI expert; provides compile job rules corrections |
| Eve | DevOps Lead | Email | Sends changelog announcements and deadline notifications |
| Frank | Junior Engineer | Feishu DM | Provides workspace style preferences |

## Channels
- **Slack #devops-cicd**: GitHub Actions cache and concurrency discussions
- **Feishu DM (Frank → agent)**: workspace style preferences
- **Email (Eve → team)**: GitHub changelog announcements
- **Feishu 群「CI/CD 治理」**: GitLab CI repair discussions
- **GitHub Issue #287**: cache miss root-cause discussion
""")
    w(WS / "IDENTITY.md", """# Identity

You are **DevOps AI**, a CI/CD configuration assistant deployed to support the DevOps
governance team. You audit GitHub Actions workflows and GitLab CI configurations, identify
misconfigurations, apply correct fixes, and produce structured audit reports.

Configuration files in `.github/workflows/` and `.gitlab/` and `.gitlab-ci.yml` are the
primary subjects. You create your deliverables under `audit/` and update config files
in-place (with backups). Scripts go under `scripts/`.
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|------|---------|-------------|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to inspect files and write deliverable files |

## Rules
- Configuration files are the primary artifacts; always back up before modifying.
- Deliverable JSON reports go under `audit/`; scripts under `scripts/`.
- In history sessions, use only `read` and light `exec`.
""")


# --------------------------------------------------------------------------- #
# 2. GitHub Actions workflow 配置文件（含错误）
# --------------------------------------------------------------------------- #
def gen_github_workflows() -> None:
    # ci.yml — 使用 github.sha 作为 cache key（错误），actions/cache@v2（废弃）
    w(WS / ".github" / "workflows" / "ci.yml", """name: CI Pipeline
# Main continuous integration workflow
# Last modified: 2025-01-15 by Bob (added caching)

on:
  push:
    branches: [main, develop, feature/**]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.11'

jobs:
  lint:
    name: Lint Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      # BUG: cache key uses github.sha — every commit gets a unique key, defeating caching.
      # Should use hashFiles('**/package-lock.json') instead.
      - name: Cache Node modules
        uses: actions/cache@v2
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run Prettier check
        run: npm run format:check

  test-unit:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Cache Node modules
        uses: actions/cache@v2
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  test-integration:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: test-unit
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Cache pip packages
        uses: actions/cache@v2
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install Python dependencies
        run: pip install -r requirements.txt

      - name: Run integration tests
        run: pytest tests/integration/ -v

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [test-unit, test-integration]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build image
        run: |
          docker buildx build --platform linux/amd64,linux/arm64 \\
            -t myapp:${{ github.sha }} \\
            --push .

  notify:
    name: Notify on Failure
    runs-on: ubuntu-latest
    needs: [lint, test-unit, test-integration, build]
    if: failure()
    steps:
      - name: Send Slack notification
        run: echo "Pipeline failed for ${{ github.sha }}"
""")

    # deploy.yml — 缺少 id-token: write 权限，deployments 仅 read
    w(WS / ".github" / "workflows" / "deploy.yml", """name: Deploy to Production
# OIDC-based deployment workflow
# Last modified: 2025-02-01 by Alice (added OIDC step)

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'production'

env:
  AWS_REGION: us-east-1
  ECR_REGISTRY: 123456789.dkr.ecr.us-east-1.amazonaws.com

jobs:
  validate:
    name: Validate Deployment
    runs-on: ubuntu-latest
    permissions:
      contents: read
      checks: write
    steps:
      - uses: actions/checkout@v4
      - name: Validate config
        run: ./scripts/validate_config.sh

  deploy:
    name: Deploy Application
    runs-on: ubuntu-latest
    needs: validate
    environment: production
    # BUG: Missing id-token: write permission — OIDC JWT cannot be generated without it.
    # BUG: deployments: read — after April 1, 2025 this no longer allows approve/reject.
    permissions:
      contents: read
      deployments: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Pull and tag image
        run: |
          docker pull ${{ env.ECR_REGISTRY }}/myapp:${{ github.sha }}
          docker tag ${{ env.ECR_REGISTRY }}/myapp:${{ github.sha }} \\
            ${{ env.ECR_REGISTRY }}/myapp:latest

      - name: Update ECS service
        run: |
          aws ecs update-service \\
            --cluster production \\
            --service myapp \\
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \\
            --cluster production \\
            --services myapp

      - name: Create GitHub deployment
        uses: actions/github-script@v7
        with:
          script: |
            const deployment = await github.rest.repos.createDeployment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: context.sha,
              environment: 'production',
              auto_merge: false,
              required_contexts: []
            });
            console.log('Deployment created:', deployment.data.id);

  rollback:
    name: Rollback on Failure
    runs-on: ubuntu-latest
    needs: deploy
    if: failure()
    permissions:
      contents: read
      deployments: read
    steps:
      - uses: actions/checkout@v4
      - name: Execute rollback
        run: ./scripts/rollback.sh
""")

    # release.yml — matrix exclude 配置错误（只匹配 os 字段，未匹配完整组合）
    w(WS / ".github" / "workflows" / "release.yml", """name: Release Build
# Multi-platform release matrix
# Last modified: 2025-01-20 by Charlie (added matrix strategy)

on:
  push:
    tags: ['v*.*.*']
  workflow_dispatch:
    inputs:
      version:
        description: 'Release version'
        required: true

jobs:
  build-matrix:
    name: Build (${{ matrix.os }} / Node ${{ matrix.version }})
    runs-on: ${{ matrix.os }}
    # Matrix: 3 OS * 3 versions = 9 combinations
    # We want to exclude windows-latest + node12 and windows-latest + node14 combinations (2 exclusions)
    # But current exclude only matches on os, which would exclude ALL windows-latest (3 jobs instead of 2)
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        version: [12, 16, 20]
        # BUG: exclude block only specifies os, not the full combination.
        # This will NOT correctly filter: {os: windows-latest, version: 12} and {os: windows-latest, version: 14}
        # It will instead try to match {os: windows-latest} which GitHhub expands differently.
        exclude:
          - os: windows-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js ${{ matrix.version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.version }}

      - name: Install dependencies
        run: npm ci

      - name: Build for ${{ matrix.os }}
        run: npm run build

      - name: Run platform tests
        run: npm run test:platform

      - name: Package artifact
        run: |
          npm pack
          mv *.tgz myapp-${{ matrix.os }}-node${{ matrix.version }}.tgz

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: release-${{ matrix.os }}-node${{ matrix.version }}
          path: '*.tgz'

  publish:
    name: Publish Release
    runs-on: ubuntu-latest
    needs: build-matrix
    permissions:
      contents: write
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: dist/

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/**/*.tgz
          generate_release_notes: true
""")

    # nightly.yml — 并发控制使用禁止组合 queue: max + cancel-in-progress: true
    w(WS / ".github" / "workflows" / "nightly.yml", """name: Nightly Build
# Scheduled nightly build and security scan
# Last modified: 2025-01-25 by Bob (added concurrency control)

on:
  schedule:
    - cron: '0 2 * * *'  # 2am UTC daily
  workflow_dispatch:

# BUG: queue: max + cancel-in-progress: true is a FORBIDDEN combination.
# This causes a workflow validation error at runtime.
# Reference: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
concurrency:
  group: nightly-build
  cancel-in-progress: true
  queue: max

jobs:
  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:latest
          format: sarif
          output: trivy-results.sarif

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-results.sarif

  dependency-audit:
    name: Dependency Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Cache Node modules
        uses: actions/cache@v2
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-nightly-${{ github.sha }}

      - name: Audit dependencies
        run: npm audit --audit-level moderate

  performance-test:
    name: Performance Benchmark
    runs-on: ubuntu-latest
    needs: security-scan
    steps:
      - uses: actions/checkout@v4
      - name: Run k6 benchmarks
        run: |
          docker run --rm -i grafana/k6 run - <tests/perf/load_test.js

      - name: Save benchmark results
        uses: actions/upload-artifact@v4
        with:
          name: perf-results-${{ github.run_id }}
          path: k6-results.json

  notify-results:
    name: Notify Results
    runs-on: ubuntu-latest
    needs: [security-scan, dependency-audit, performance-test]
    if: always()
    steps:
      - name: Report summary
        run: |
          echo "Nightly build completed at $(date -u)"
          echo "Run ID: ${{ github.run_id }}"
""")


# --------------------------------------------------------------------------- #
# 3. GitLab CI 配置文件
# --------------------------------------------------------------------------- #
def gen_gitlab_configs() -> None:
    # .gitlab-ci.yml — 主配置，artifacts:expire_in 非法格式
    w(WS / ".gitlab-ci.yml", """# GitLab CI Main Configuration
# Includes stage-split sub-configurations from .gitlab/ci/
# Last modified: 2025-01-10

stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

include:
  - local: '.gitlab/ci/build.yml'
  - local: '.gitlab/ci/test.yml'
  - local: '.gitlab/ci/deploy.yml'

# Global cache configuration
cache:
  key:
    files:
      - Gemfile.lock
  paths:
    - vendor/bundle

# BUG: artifacts:expire_in uses non-standard format "30d" (should be "30 days")
# Valid formats: '42 seconds', '3 mins 4 sec', '2h20min', '6 mos 1 day', 'never'
default:
  artifacts:
    expire_in: 30d
    when: on_success

workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: always
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: always
    - when: never
""")

    # .gitlab/ci/build.yml — cache:key:files 超过 2 个路径（错误）
    w(WS / ".gitlab" / "ci" / "build.yml", """# Build stage configuration
# Part of the stage-split GitLab CI setup

compile:
  stage: build
  image: node:20-alpine
  rules:
    - if: '$CI_COMMIT_BRANCH'
  cache:
    key:
      # BUG: cache:key:files allows maximum 2 file paths.
      # Having 3 paths here is a configuration error.
      files:
        - Gemfile.lock
        - yarn.lock
        - package-lock.json
    policy: pull-push
    paths:
      - node_modules/
      - .yarn/cache/
  script:
    - yarn install --frozen-lockfile
    - yarn build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

docker-build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  needs:
    - compile
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  cache:
    key: docker-layer-cache
    policy: pull-push
    paths:
      - .docker-cache/

# Archive of old build configuration (DO NOT USE - deprecated)
# old_compile_v1:
#   stage: build
#   rules:
#     - if: '$CI_COMMIT_BRANCH'
#   cache:
#     key:
#       files:
#         - Gemfile.lock
#         - yarn.lock
#         - package-lock.json
#     policy: pull-push
#   script:
#     - yarn install
""")

    # .gitlab/ci/test.yml — 并行 test job 使用 pull-push（应改 pull）；needs 引用排除的 compile job
    w(WS / ".gitlab" / "ci" / "test.yml", """# Test stage configuration
# Part of the stage-split GitLab CI setup

unit_test:
  stage: test
  image: node:20-alpine
  # BUG: needs references 'compile' which is excluded from pipeline on non-default branches
  # (compile job has rules: if '$CI_COMMIT_BRANCH', but unit_test runs on MR too)
  # Fix: add optional: true to the needs entry.
  needs:
    - compile
  # BUG: parallel test jobs should use policy: pull (not pull-push) to reduce server load.
  # Using pull-push in parallel jobs causes race conditions and unnecessary cache uploads.
  cache:
    key:
      files:
        - yarn.lock
    policy: pull-push
    paths:
      - node_modules/
  script:
    - yarn install --frozen-lockfile
    - yarn test:unit --coverage
  coverage: '/Lines\\s*:\\s*([\\d.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    expire_in: 7 days

integration_test:
  stage: test
  image: node:20-alpine
  needs:
    - compile
  # BUG: Same issue - parallel test job using pull-push
  cache:
    key:
      files:
        - yarn.lock
    policy: pull-push
    paths:
      - node_modules/
  services:
    - postgres:14
    - redis:7
  variables:
    POSTGRES_DB: testdb
    POSTGRES_PASSWORD: testpass
  script:
    - yarn install --frozen-lockfile
    - yarn test:integration
  artifacts:
    reports:
      junit: test-results/junit.xml
    expire_in: 3 days

e2e_test:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  needs:
    - compile
  cache:
    key:
      files:
        - yarn.lock
    # This one is also using pull-push - should be pull
    policy: pull-push
    paths:
      - node_modules/
  script:
    - yarn install --frozen-lockfile
    - yarn test:e2e
  artifacts:
    when: on_failure
    paths:
      - playwright-report/
    expire_in: 2 days
""")

    # .gitlab/ci/deploy.yml — 部署配置
    w(WS / ".gitlab" / "ci" / "deploy.yml", """# Deploy stage configuration
# Part of the stage-split GitLab CI setup

staging:
  stage: deploy
  image: alpine:3.18
  needs:
    - unit_test
    - integration_test
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
  environment:
    name: staging
    url: https://staging.myapp.example.com
  script:
    - apk add --no-cache curl
    - curl -X POST https://deploy.internal/staging --data "commit=$CI_COMMIT_SHA"
  cache:
    key: deploy-cache
    policy: pull
    paths:
      - .deploy-cache/

production:
  stage: deploy
  image: alpine:3.18
  needs:
    - staging
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
  environment:
    name: production
    url: https://myapp.example.com
  script:
    - apk add --no-cache curl
    - curl -X POST https://deploy.internal/production --data "commit=$CI_COMMIT_SHA"
  cache:
    key: deploy-cache
    policy: pull
    paths:
      - .deploy-cache/
""")

    # 红鲱鱼：archive 目录中旧版 test.yml（仍用 pull-push，V6）
    w(WS / ".gitlab" / "archive" / "test.yml.old", """# ARCHIVED - DO NOT USE
# This is the old test.yml configuration from before the stage-split refactor.
# Kept for historical reference only. Using this config will cause issues.

# unit_test (LEGACY - archived 2024-11-15):
#   stage: test
#   cache:
#     key: legacy-cache-key
#     policy: pull-push   # <-- old default, not fixed
#   script:
#     - npm test
""")


# --------------------------------------------------------------------------- #
# 4. 脚本与审计模板
# --------------------------------------------------------------------------- #
def gen_scripts_and_audit() -> None:
    # validate_workflows.py — 骨架（Q14 要求产出完整版）
    w(WS / "scripts" / "validate_workflows.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 0.1
# validate_workflows.py - Local CI/CD configuration validator (skeleton)
# TODO: Implement full validation logic in Q14 task

import sys
from pathlib import Path

def main():
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print("Validation not yet implemented - run Q14 task first")
    sys.exit(1)

if __name__ == "__main__":
    main()
""")

    # audit/workflow_audit_template.json
    wj(WS / "audit" / "workflow_audit_template.json", {
        "schema_version": "1.0",
        "audit_date": "2025-04-01",
        "auditor": "DevOps AI",
        "scope": ["GitHub Actions", "GitLab CI"],
        "issue_categories": [
            "cache_configuration",
            "concurrency_control",
            "permissions",
            "matrix_strategy",
            "gitlab_cache_policy",
            "gitlab_artifacts",
            "gitlab_needs"
        ],
        "severity_levels": ["critical", "high", "medium", "low"],
        "fix_template": {
            "file": "",
            "issue_type": "",
            "severity": "",
            "old_value": "",
            "new_value": "",
            "reference_url": ""
        }
    })

    # audit/previous_audit_2024.json — 2024 年审计（含失真摘要，V5 诱饵）
    # 失真：声称 cache key 问题"已解决"（实际未解决）；声称 cache v3（实际仍是 v2）
    wj(WS / "audit" / "previous_audit_2024.json", {
        "schema_version": "1.0",
        "audit_date": "2024-11-30",
        "auditor": "Bot-Scanner-v1",
        "note": "AUTO-GENERATED SUMMARY — convenience only, not authoritative. Known to miss some issues.",
        "summary": {
            "total_issues_found": 3,
            "issues_resolved": 2,
            "issues_pending": 1
        },
        "findings": [
            {
                "id": "AUDIT-2024-001",
                "file": ".github/workflows/ci.yml",
                "issue": "Cache key using github.sha",
                "status": "RESOLVED",
                "note": "Bot detected this was fixed in PR #234 (BOT DECOY: this status is INCORRECT - still unfixed)"
            },
            {
                "id": "AUDIT-2024-002",
                "file": ".github/workflows/ci.yml",
                "issue": "actions/cache version",
                "current_version_detected": "v3",
                "status": "RESOLVED",
                "note": "Bot detected upgrade to v3 (BOT DECOY: still using v2 — do not trust this summary)"
            },
            {
                "id": "AUDIT-2024-003",
                "file": ".github/workflows/nightly.yml",
                "issue": "Concurrency configuration",
                "status": "PENDING",
                "note": "Concurrency issue still pending fix"
            }
        ]
    })

    # .gitlab/scripts/cache_key_gen.sh
    w(WS / ".gitlab" / "scripts" / "cache_key_gen.sh", """#!/bin/bash
# cache_key_gen.sh - Generate cache keys for GitLab CI jobs
# Usage: ./cache_key_gen.sh <file1> [file2]

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file1> [file2]" >&2
    exit 1
fi

# GitLab CI cache:key:files supports maximum 2 file paths
if [ $# -gt 2 ]; then
    echo "Warning: cache:key:files supports maximum 2 files. Using first 2 only." >&2
fi

KEY=""
for f in "${@:1:2}"; do
    if [ -f "$f" ]; then
        HASH=$(sha256sum "$f" | cut -d' ' -f1 | head -c 16)
        KEY="${KEY}${HASH}-"
    fi
done

echo "${KEY%%-}"  # Remove trailing dash
""")

    # .gitlab/scripts/artifact_check.sh
    w(WS / ".gitlab" / "scripts" / "artifact_check.sh", """#!/bin/bash
# artifact_check.sh - Validate GitLab CI artifact configurations
# Checks expire_in format, artifact paths, and policy settings

set -euo pipefail

VALID_FORMATS_REGEX="^([0-9]+ (seconds?|mins?|hours?|days?|weeks?|months?|mos)( [0-9]+ (seconds?|mins?|hours?|days?))?|never|[0-9]+h[0-9]+min)$"

check_expire_in() {
    local value="$1"
    if echo "$value" | grep -qE "$VALID_FORMATS_REGEX"; then
        echo "OK: expire_in='$value' is valid"
        return 0
    else
        echo "ERROR: expire_in='$value' is NOT a valid GitLab CI format"
        echo "Valid examples: '42 seconds', '3 mins 4 sec', '2h20min', '6 mos 1 day', 'never'"
        return 1
    fi
}

# Check known bad format
check_expire_in "30d" || true  # Will fail - intended to demonstrate the issue
check_expire_in "30 days" && echo "Correct format confirmed"
check_expire_in "never" && echo "Special value 'never' is valid"
""")

    # docs/cicd_architecture.md — 约 3000 行架构文档
    _gen_arch_doc()

    # docs/workflow_history.md — 变更历史
    _gen_workflow_history()

    # docs/known_issues.md
    _gen_known_issues()

    # docs/runbook.md
    _gen_runbook()


def _gen_arch_doc() -> None:
    """生成 CI/CD 架构文档（足够体量）。"""
    sections = []
    sections.append("""# CI/CD 架构文档 / CI/CD Architecture Documentation

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

""")

    # 补充内容以扩展体量
    for i in range(1, 15):
        sections.append(f"""
## GitHub Actions 高级配置第 {i} 节 / Advanced Configuration Section {i}

### 场景说明 / Scenario Description

本节介绍 GitHub Actions 工作流中关于{'缓存优化' if i % 3 == 0 else '权限管理' if i % 3 == 1 else '矩阵构建'}的高级配置模式。

In this section we cover advanced patterns for {'cache optimization' if i % 3 == 0 else 'permission management' if i % 3 == 1 else 'matrix builds'} in GitHub Actions workflows.

#### 配置示例 / Configuration Example

```yaml
# Example workflow configuration for scenario {i}
name: Example Workflow {i}
on:
  push:
    branches: [main]

jobs:
  example-job-{i}:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Step {i}
        run: echo "Running step {i}"
        env:
          EXAMPLE_VAR: "value_{i}"
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

""")
    w(WS / "docs" / "cicd_architecture.md", "\n".join(sections))


def _gen_workflow_history() -> None:
    entries = []
    entries.append("""# 工作流变更历史 / Workflow Change History

## 概述 / Overview

本文档记录所有 CI/CD 工作流配置的变更历史，包括变更时间、变更人、变更内容和变更原因。

This document records all CI/CD workflow configuration change history, including when, who, what, and why.

""")
    changes = [
        ("2025-01-15", "Bob", "ci.yml", "Added caching with actions/cache@v2", "Speed up CI by caching node_modules"),
        ("2025-01-20", "Charlie", "release.yml", "Added matrix strategy for multi-platform builds", "Support Windows and macOS builds"),
        ("2025-01-25", "Bob", "nightly.yml", "Added concurrency control with queue: max", "Prevent parallel nightly runs"),
        ("2025-02-01", "Alice", "deploy.yml", "Added OIDC authentication step", "Replace static credentials with OIDC"),
        ("2025-02-10", "David", ".gitlab/ci/build.yml", "Added cache:key:files with 3 paths", "More granular cache invalidation"),
        ("2025-02-15", "Frank", ".gitlab/ci/test.yml", "Added parallel test jobs", "Speed up test suite"),
        ("2025-02-20", "David", ".gitlab-ci.yml", "Updated artifact expire_in", "Reduce storage usage"),
        ("2025-03-01", "Charlie", ".github/workflows/nightly.yml", "Attempted concurrency fix (incomplete)", "Resolve validation errors"),
    ]
    for date, author, file, change, reason in changes:
        entries.append(f"""
## {date}

**变更人 / Author**: {author}
**文件 / File**: `{file}`
**变更内容 / Change**: {change}
**变更原因 / Reason**: {reason}

""")

    for i in range(1, 20):
        entries.append(f"""
## 2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}

**变更人 / Author**: {'Alice' if i % 4 == 0 else 'Bob' if i % 4 == 1 else 'Charlie' if i % 4 == 2 else 'David'}
**文件 / File**: `.github/workflows/${'ci' if i % 3 == 0 else 'deploy' if i % 3 == 1 else 'nightly'}.yml`
**变更内容 / Change**: Historical change {i} — updated workflow configuration
**变更原因 / Reason**: Routine maintenance and optimization for CI/CD pipeline reliability

```yaml
# Patch excerpt for change {i}
# Before:
#   timeout-minutes: {i * 5}
# After:
#   timeout-minutes: {i * 6}
```

This change was reviewed and approved by the DevOps team. Testing was performed
in the staging environment before merging to main.

""")
    w(WS / "docs" / "workflow_history.md", "\n".join(entries))


def _gen_known_issues() -> None:
    w(WS / "docs" / "known_issues.md", """# 已知问题列表 / Known Issues List

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

""")


def _gen_runbook() -> None:
    sections = []
    sections.append("""# 运维手册 / Operational Runbook

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

""")
    for i in range(1, 25):
        sections.append(f"""
## 运维场景 {i} / Operational Scenario {i}

### 场景描述 / Scenario Description

{'缓存清理与重置' if i % 5 == 0 else '权限变更流程' if i % 5 == 1 else 'Job 超时处理' if i % 5 == 2 else '紧急回滚操作' if i % 5 == 3 else '矩阵构建调优'}

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

""")
    w(WS / "docs" / "runbook.md", "\n".join(sections))


# --------------------------------------------------------------------------- #
# 5. 大体量锁文件（撑起 token 体量）
# --------------------------------------------------------------------------- #
def gen_lock_files() -> None:
    rng = random.Random(5555)
    packages = [
        "react", "react-dom", "typescript", "webpack", "babel-core",
        "eslint", "prettier", "jest", "axios", "lodash", "moment",
        "express", "cors", "dotenv", "multer", "sharp", "pg",
        "redis", "bull", "winston", "morgan", "helmet", "compression",
        "passport", "jsonwebtoken", "bcrypt", "uuid", "date-fns",
        "zod", "yup", "joi", "class-validator", "reflect-metadata",
        "typeorm", "sequelize", "mongoose", "knex", "objection",
        "fastify", "koa", "hapi", "restify", "socket.io", "ws",
        "graphql", "apollo-server", "type-graphql", "nexus", "pothos",
        "next", "nuxt", "remix", "gatsby", "svelte", "vue",
        "tailwindcss", "postcss", "autoprefixer", "sass", "less",
        "rollup", "vite", "esbuild", "swc", "turbopack", "nx",
        "jest-dom", "testing-library", "cypress", "playwright",
        "husky", "lint-staged", "commitlint", "semantic-release",
    ]

    # package-lock.json — 目标约 60k tokens
    pkg_lock_lines = ['{\n  "name": "myapp",\n  "version": "1.0.0",\n  "lockfileVersion": 3,\n  "packages": {']
    for pkg in packages:
        for v_major in range(2):
            for v_minor in range(4):
                version = f"{v_major}.{v_minor}.{rng.randint(0, 20)}"
                integrity = "sha512-" + "".join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", k=88)) + "=="
                deps = {
                    f"dep-{j}": f"^{rng.randint(1, 5)}.{rng.randint(0, 10)}.0"
                    for j in range(rng.randint(0, 3))
                }
                entry = (
                    f'    "node_modules/{pkg}-v{v_major}{v_minor}": {{\n'
                    f'      "version": "{version}",\n'
                    f'      "resolved": "https://registry.npmjs.org/{pkg}/-/{pkg}-{version}.tgz",\n'
                    f'      "integrity": "{integrity}",\n'
                    f'      "engines": {{"node": ">=14.0.0"}}'
                )
                if deps:
                    deps_str = ", ".join(f'"{k}": "{v}"' for k, v in deps.items())
                    entry += f',\n      "dependencies": {{{deps_str}}}'
                entry += "\n    }"
                pkg_lock_lines.append(entry + ",")
    pkg_lock_lines.append('    "": {"name": "myapp", "version": "1.0.0"}\n  }\n}')
    w(WS / "package-lock.json", "\n".join(pkg_lock_lines))

    # yarn.lock — 目标约 40k tokens
    yarn_lines = ['# THIS IS AN AUTOGENERATED FILE. DO NOT EDIT THIS FILE DIRECTLY.\n# yarn lockfile v1\n']
    for pkg in packages:
        for v_major in range(1):
            for v_minor in range(5):
                version = f"{v_major}.{v_minor}.{rng.randint(0, 15)}"
                integrity = "sha512-" + "".join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", k=88)) + "=="
                deps = {
                    f"sub-dep-{j}": f"^{rng.randint(1, 4)}.{rng.randint(0, 8)}.0"
                    for j in range(rng.randint(0, 3))
                }
                yarn_lines.append(f'\n"{pkg}@^{v_major}.{v_minor}.0":\n  version "{version}"')
                yarn_lines.append(f'  resolved "https://registry.yarnpkg.com/{pkg}/-/{pkg}-{version}.tgz#{rng.randbytes(20).hex()}"')
                yarn_lines.append(f'  integrity {integrity}')
                if deps:
                    yarn_lines.append('  dependencies:')
                    for dk, dv in deps.items():
                        yarn_lines.append(f'    {dk} "{dv}"')
    w(WS / "yarn.lock", "\n".join(yarn_lines))

    # Gemfile.lock — Ruby 锁文件（约 3000 行）
    gems = [
        "rails", "activerecord", "activesupport", "actionpack",
        "bundler", "rake", "rspec", "minitest", "rubocop",
        "puma", "unicorn", "sidekiq", "redis", "pg",
        "devise", "pundit", "cancancan", "doorkeeper",
        "paperclip", "carrierwave", "shrine", "activestorage",
        "capistrano", "mina", "whenever", "clockwork",
        "rswag", "swagger-blocks", "grape", "jsonapi-resources",
    ]
    gemfile_lines = ["GEM\n  remote: https://rubygems.org/\n  specs:"]
    for gem in gems:
        v = f"{rng.randint(5, 8)}.{rng.randint(0, 9)}.{rng.randint(0, 20)}"
        gemfile_lines.append(f"    {gem} ({v})")
        for dep in rng.choices(gems, k=rng.randint(0, 3)):
            dv = f"{rng.randint(1, 5)}.{rng.randint(0, 9)}"
            gemfile_lines.append(f"      {dep} (>= {dv})")
    gemfile_lines.append("\nPLATFORMS\n  ruby\n\nDEPENDENCIES")
    for gem in gems:
        gemfile_lines.append(f"  {gem}")
    w(WS / "Gemfile.lock", "\n".join(gemfile_lines))


# --------------------------------------------------------------------------- #
# 6. 聊天记录（历史 sessions 的 workspace 素材版本）
# --------------------------------------------------------------------------- #
def gen_chat_history_files() -> None:
    """生成 workspace 内的聊天记录文件（给 agent 读取的素材）。"""

    # GitHub Issue #287 — cache miss 问题讨论（含冲突信息：Bob 使用 github.sha）
    w(WS / "chat_history" / "github_issue_287.md", """# GitHub Issue #287: Cache always misses on every run

**Opened**: 2025-01-16
**Reporter**: charlie-sre
**Labels**: bug, ci/cd, performance

## Problem Description

Our CI pipeline is experiencing 100% cache miss rate. Every run downloads all
dependencies from scratch, adding 3-5 minutes to every build.

## Analysis

### Comment by alice-engineer (2025-01-17)
The issue is in the cache key configuration. I checked `.github/workflows/ci.yml` and
found the cache key uses `github.sha`:

```yaml
key: ${{ runner.os }}-node-${{ github.sha }}
```

Since `github.sha` is unique per commit, every run gets a fresh cache. We need to use
`hashFiles('**/package-lock.json')` instead, which only changes when dependencies change.

The correct format should be:
```yaml
key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
restore-keys: |
  ${{ runner.os }}-build-
  ${{ runner.os }}-
```

### Comment by bob-devops (2025-01-18)
Good catch, Alice. I'll fix this. Here's my proposed fix:

```yaml
# My proposed key format
key: ${{ runner.os }}-npm-${{ github.ref }}-${{ hashFiles('**/package-lock.json') }}
```

Wait, actually should we include the branch name in the key? That way different
branches don't share caches. Or is that unnecessary?

Also, the restore-keys should be:
```yaml
restore-keys: |
  ${{ runner.os }}-npm-${{ github.ref }}-
  ${{ runner.os }}-npm-
```

### Comment by alice-engineer (2025-01-19)
Bob, the `github.ref` in the key is fine for isolation but it's optional.
The important part is `hashFiles('**/package-lock.json')`.

The official example from GitHub docs is:
```
${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
```

The restore-keys should match the key prefix:
```yaml
restore-keys: |
  ${{ runner.os }}-build-
  ${{ runner.os }}-
```

NOT what you have (which includes `npm` not in the key prefix).

### Comment by charlie-sre (2025-01-20)
Also noticed we're using `actions/cache@v2` which is deprecated.
Per the deprecation notice (https://github.com/actions/cache/discussions/1510),
v1 and v2 are being shut down. Final deadline: March 1, 2025.
We need to upgrade to at least v4.2.0 or v3.4.0.

### Status: OPEN - Fix in progress
""")

    # Slack 频道记录（含 bot 失真摘要）
    wj(WS / "chat_history" / "slack_devops_channel.jsonl", {
        "channel": "devops-cicd",
        "export_date": "2025-03-15",
        "messages": [
            {
                "ts": "1741600000.000100",
                "user": "alice",
                "text": "Team, I've been looking at our cache situation. The root issue is `github.sha` in the key. Once we switch to `hashFiles`, we should see cache hit rates go up significantly.",
                "reactions": [{"name": "thumbsup", "count": 3}]
            },
            {
                "ts": "1741600060.000200",
                "user": "bob",
                "text": "Agreed. I'll also upgrade `actions/cache` from v2 to v4. The deprecation deadline was March 1st. We're already past it.",
                "attachments": []
            },
            {
                "ts": "1741600120.000300",
                "user": "charlie",
                "text": "Per the bot summary below, the cache issue was resolved in November. Are you sure we still need this fix?",
                "attachments": [
                    {
                        "title": "[Bot Summary - NOT authoritative]",
                        "text": "SUMMARY (auto-generated, accuracy not guaranteed): Cache configuration reviewed Nov 2024. Bot detected cache@v3 in use. Key format appears correct. No action needed. — Note: This summary may be outdated or inaccurate."
                    }
                ]
            },
            {
                "ts": "1741600180.000400",
                "user": "alice",
                "text": "Charlie, the bot summary is wrong. I just checked the actual yml files - still on v2, still using github.sha. Don't trust the bot for config status.",
                "reactions": [{"name": "white_check_mark", "count": 2}]
            },
            {
                "ts": "1741600240.000500",
                "user": "bob",
                "text": "Also, the nightly.yml has a concurrency config issue. `queue: max` with `cancel-in-progress: true` is a forbidden combo. It causes a validation error every run.",
                "reactions": []
            },
            {
                "ts": "1741600300.000600",
                "user": "charlie",
                "text": "For the concurrency fix on nightly: since it's a long-running scan job, we should keep `queue: max` and remove `cancel-in-progress`. That way runs queue up but don't get killed mid-scan.",
                "reactions": [{"name": "thumbsup", "count": 2}]
            }
        ]
    })

    # 飞书 DM — 用户设置 workspace 样式偏好
    wj(WS / "chat_history" / "feishu_dm_frank.jsonl", {
        "channel": "feishu_dm",
        "participants": ["Frank", "DevOps AI"],
        "messages": [
            {
                "sender": "Frank",
                "timestamp": "2025-03-10T09:00:00Z",
                "text": "Hi, before we start the audit tasks, a few style preferences that apply throughout all tasks:\n\n1. All Markdown document headings at level 1 and 2 must be bilingual: format `# 中文标题 / English Title`. This applies to ALL audit documents.\n\n2. Please use 2-space YAML indentation throughout (no tabs).\n\n3. Before modifying any config file, always backup the original with `.bak` suffix in the same directory."
            },
            {
                "sender": "DevOps AI",
                "timestamp": "2025-03-10T09:01:00Z",
                "text": "Understood. Throughout all tasks I will:\n1. Use bilingual headings (# 中文 / English) for all Markdown files\n2. Use 2-space YAML indentation\n3. Backup any config file before modifying it (.bak suffix, same directory)"
            },
            {
                "sender": "Frank",
                "timestamp": "2025-03-10T09:02:00Z",
                "text": "Perfect. Also, all JSON outputs must use snake_case field names (not camelCase). And Python scripts should have a version comment: `# version: X.Y`."
            },
            {
                "sender": "DevOps AI",
                "timestamp": "2025-03-10T09:03:00Z",
                "text": "Got it. snake_case for all JSON field names, and Python scripts carry `# version: X.Y` in the header."
            }
        ]
    })

    # 邮件线程
    w(WS / "chat_history" / "email_thread_cicd.eml", """From: Eve <eve@company.com>
To: devops-team@company.com
Subject: [ACTION REQUIRED] GitHub Actions Breaking Changes - April 2025
Date: Thu, 20 Mar 2025 14:00:00 +0000

Team,

GitHub has announced upcoming breaking changes effective April 1, 2025:

1. deployments:read will no longer allow reviewing/approving deployments
   - All workflows that need to approve/reject deployments must upgrade to deployments:write
   - Our deploy.yml currently uses deployments:read — this needs updating

2. The new cache service is now fully active
   - Old cache URLs are no longer valid
   - Self-hosted runners must be on version 2.320.1 or higher

Please review and update all affected workflows before April 1st.

Reference: https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/

Best,
Eve

---
From: Alex <alex@company.com>
To: devops-team@company.com
Subject: RE: [ACTION REQUIRED] GitHub Actions Breaking Changes - April 2025
Date: Thu, 20 Mar 2025 15:30:00 +0000

Eve,

Thanks for the heads up. I've assigned this to our CI/CD audit initiative.
The DevOps AI agent will handle the systematic review and updates.

Key action items:
- Update deploy.yml: deployments:read → deployments:write
- Keep id-token:write (required for OIDC, separate concern)
- Document changes in audit log

Alex
""")


# --------------------------------------------------------------------------- #
# 7. Sessions（主 + 5 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_devops_cicd", TID)
    s_feishu = gen_session_id("feishu_dm_frank", TID)
    s_email = gen_session_id("email_eve_team", TID)
    s_github = gen_session_id("github_issue_287", TID)
    s_feishu_group = gen_session_id("feishu_group_cicd", TID)

    # 主 session
    sb = SessionBuilder(main_id, CWD, "2026-03-10T01:00:00", is_main=True)
    sb.add_user(
        "You are DevOps AI, the CI/CD configuration assistant for the DevOps governance team. "
        "Your mission: systematically audit and repair all GitHub Actions workflows and GitLab CI "
        "configurations in this workspace, then produce structured audit reports.\n\n"
        "Workspace style preferences (apply throughout, even when not restated):\n"
        "- P1: All JSON output files use snake_case field names (never camelCase).\n"
        "- P2: All Markdown document headings at level 1 and 2 use bilingual format: "
        "`# 中文标题 / English Title`.\n"
        "- P3: Before modifying any config file, backup the original with `.bak` suffix "
        "in the same directory (e.g., `ci.yml` → `ci.yml.bak`).\n"
        "- P4: GitLab CI configurations must be organized by stage into separate files "
        "under `.gitlab/ci/` (never consolidate all jobs into root `.gitlab-ci.yml`).\n"
        "- P5: All Python scripts carry a version comment in the header: `# version: X.Y`.\n\n"
        "History sessions available (Slack, Feishu DM, Email, GitHub Issue, Feishu Group). "
        "Start by reading SOUL.md and then awaiting each task."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Treat official GitHub Actions and GitLab CI documentation as authoritative; "
        "bot summaries and chat messages may contain errors.\n"
        "2. Apply all workspace preferences throughout: snake_case JSON, bilingual MD headings, "
        "backup before modify, stage-split GitLab CI, Python version comments.\n"
        "3. Audit findings go under audit/; fixed config files backed up with .bak.\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S-slack: Slack #devops-cicd — cache 讨论，含 bot 失真摘要（V5）
    sb2 = SessionBuilder(s_slack, CWD, "2026-03-05T02:00:00", is_main=False)
    sb2.add_user(
        "[Slack #devops-cicd alice Mon Mar 05 10:00 EST 2026] "
        "Team, the cache is broken again. Looking at ci.yml — the key uses `github.sha` which means "
        "every single commit gets a cache miss. We need to switch to hashFiles('**/package-lock.json')."
    )
    sb2.add_assistant(
        "Confirmed: alice identified the root cause — `github.sha` in cache key causes permanent cache miss. "
        "The correct key should use hashFiles('**/package-lock.json') per GitHub docs."
    )
    sb2.add_user(
        "[Slack #devops-cicd bob Mon Mar 05 10:15 EST 2026] "
        "I'll fix it. My proposed key: `${{ runner.os }}-npm-${{ github.ref }}-${{ hashFiles('**/package-lock.json') }}`. "
        "The restore-keys would be: `${{ runner.os }}-npm-${{ github.ref }}-` then `${{ runner.os }}-npm-`. "
        "Note: I'm including branch name for isolation."
    )
    sb2.add_assistant(
        "Bob's format includes `github.ref` and `npm` prefix which diverges from the official GitHub docs example. "
        "The canonical example is: `${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}` with "
        "restore-keys `${{ runner.os }}-build-` and `${{ runner.os }}-`. "
        "Bob's format would work but the restore-keys prefix must match the key prefix exactly."
    )
    sb2.add_user(
        "[Slack #devops-cicd charlie Mon Mar 05 10:30 EST 2026] "
        "Wait, the bot summary says this was already fixed in November: "
        "[Bot Summary: Cache reviewed Nov 2024. Bot detected cache@v3 in use. Key format correct. No action needed.] "
        "Maybe we're looking at the wrong files?"
    )
    sb2.add_assistant(
        "Caution: the bot summary conflicts with what alice found by directly reading ci.yml. "
        "Bot summaries are NOT authoritative per SOUL.md. The actual files show: "
        "actions/cache@v2 (still deprecated), github.sha key (still wrong). "
        "The bot summary is incorrect — do not rely on it."
    )
    sb2.add_user(
        "[Slack #devops-cicd alice Mon Mar 05 10:45 EST 2026] "
        "Charlie, I literally just read the yml file — it's v2 and github.sha. The bot is wrong. "
        "Also: actions/cache v2 hits end-of-life on March 1, 2025. We're past that. "
        "Per https://github.com/actions/cache/discussions/1510 we need v4.2.0 or v3.4.0 minimum."
    )
    sb2.add_assistant(
        "Authoritative determination: ci.yml uses actions/cache@v2 (deprecated, deadline March 1, 2025) "
        "with github.sha cache key (always miss). Both issues confirmed from direct file inspection. "
        "Required fix: upgrade to actions/cache@v4 and use hashFiles('**/package-lock.json')."
    )
    sb2.write(SESS / f"{s_slack}.jsonl")

    # S-feishu: 飞书 DM — workspace 偏好设置（P1-P5）
    sb3 = SessionBuilder(s_feishu, CWD, "2026-03-06T02:00:00", is_main=False)
    sb3.add_user(
        "[Feishu DM frank Tue Mar 06 09:00 EST 2026] "
        "Before the audit starts, please confirm you've noted these workspace preferences:\n"
        "P1: JSON field names must use snake_case (not camelCase) in all output files.\n"
        "P2: Markdown headings at level 1 and 2 must be bilingual format: `# 中文 / English`.\n"
        "P3: Always backup config files before modifying (add .bak suffix).\n"
        "P4: GitLab CI must use stage-split files under .gitlab/ci/ directory.\n"
        "P5: Python scripts must have `# version: X.Y` in the header."
    )
    sb3.add_assistant(
        "Confirmed all preferences recorded:\n"
        "P1: snake_case JSON fields\n"
        "P2: bilingual Markdown headings (# 中文 / English)\n"
        "P3: backup with .bak before modifying\n"
        "P4: GitLab CI stage-split under .gitlab/ci/\n"
        "P5: Python scripts include `# version: X.Y`"
    )
    sb3.write(SESS / f"{s_feishu}.jsonl")

    # S-email: Email — deployments 权限截止日
    sb4 = SessionBuilder(s_email, CWD, "2026-03-07T02:00:00", is_main=False)
    sb4.add_user(
        "[Email eve@company.com → devops-team@company.com Wed Mar 07 14:00 EST 2026] "
        "Subject: [ACTION REQUIRED] GitHub Actions Breaking Changes - April 2025. "
        "Team, GitHub has announced: effective April 1, 2025, deployments:read will no longer "
        "allow reviewing/approving deployments. All workflows needing to approve/reject deployments "
        "must upgrade to deployments:write. Our deploy.yml currently uses deployments:read — "
        "this needs updating before the deadline. Reference: "
        "https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/"
    )
    sb4.add_assistant(
        "Logged: deploy.yml must update `deployments: read` to `deployments: write` before April 1, 2025. "
        "This is a breaking change — deployments:read will no longer allow approve/reject after that date. "
        "The id-token:write permission (for OIDC) is a separate concern and must be preserved."
    )
    sb4.write(SESS / f"{s_email}.jsonl")

    # S-github-issue: GitHub Issue #287 — cache key 冲突讨论
    sb5 = SessionBuilder(s_github, CWD, "2026-03-08T02:00:00", is_main=False)
    sb5.add_user(
        "[GitHub Issue #287 charlie-sre Thu Mar 08 11:00 EST 2026] "
        "CI cache always misses. Every run downloads all dependencies from scratch. "
        "This adds 3-5 minutes to every build."
    )
    sb5.add_assistant(
        "Root cause identified: ci.yml uses `github.sha` in cache key, causing permanent miss. "
        "Must switch to `hashFiles('**/package-lock.json')`."
    )
    sb5.add_user(
        "[GitHub Issue #287 bob-devops Thu Mar 08 11:30 EST 2026] "
        "Also using actions/cache@v2 which is deprecated. "
        "Final deprecation deadline was March 1, 2025. Need to upgrade."
    )
    sb5.add_assistant(
        "Confirmed: two distinct issues — wrong cache key (github.sha) and deprecated cache action (v2). "
        "Both must be fixed simultaneously."
    )
    sb5.write(SESS / f"{s_github}.jsonl")

    # S-feishu-group: 飞书群「CI/CD 治理」— GitLab CI needs 讨论（错误方案 vs 正确方案）
    sb6 = SessionBuilder(s_feishu_group, CWD, "2026-03-09T02:00:00", is_main=False)
    sb6.add_user(
        "[Feishu 群「CI/CD 治理」 frank Fri Mar 09 09:00 EST 2026] "
        "GitLab pipeline keeps failing: \"'unit_test' job needs 'compile' job, but 'compile' "
        "does not exist in the pipeline\". Anyone know the fix?"
    )
    sb6.add_assistant(
        "This error occurs when a `needs` entry references a job that doesn't exist in the current pipeline, "
        "typically because that job was excluded by `rules` conditions."
    )
    sb6.add_user(
        "[Feishu 群「CI/CD 治理」 junior-dev1 Fri Mar 09 09:15 EST 2026] "
        "Easy fix: just delete the `needs: [compile]` line. Then unit_test won't depend on compile at all."
    )
    sb6.add_assistant(
        "WARNING: removing the needs entry is the WRONG approach. It breaks the DAG dependency that ensures "
        "unit_test has the compiled artifacts. The correct fix is to add `optional: true` to the needs entry."
    )
    sb6.add_user(
        "[Feishu 群「CI/CD 治理」 david Fri Mar 09 09:30 EST 2026] "
        "junior-dev1, don't remove needs. The correct fix per GitLab docs is: "
        "`needs: [{job: \"compile\", optional: true}]`. "
        "This tells GitLab: use compile artifacts if the job ran, otherwise proceed without them. "
        "Reference: https://docs.gitlab.com/ci/yaml/needs/"
    )
    sb6.add_assistant(
        "Confirmed: David's solution is correct. The fix is adding `optional: true` to the needs entry, "
        "NOT removing the needs dependency. "
        "Also note: the legacy archive at .gitlab/archive/test.yml.old should not be referenced — "
        "it uses outdated configurations."
    )
    sb6.write(SESS / f"{s_feishu_group}.jsonl")

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_feishu, "feishu"),
            (s_email, "email"),
            (s_github, "im"),
            (s_feishu_group, "feishu"),
        ],
    }


# --------------------------------------------------------------------------- #
# 8. Updates（含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_email = sess_ids["history"][2][0]
    s_feishu_group = sess_ids["history"][4][0]

    # UPDATE 1（Q7 后）：Email 补全（deployments:write 截止日已至）+ 大体量邮件线程
    u1_sess = gen_session_id("email_update_apr2025", TID)
    sb_u1 = SessionBuilder(u1_sess, CWD, "2026-03-15T09:00:00", is_main=False)
    sb_u1.add_user(
        "[Email update forwarded by Alex] "
        "URGENT: April 1, 2025 deadline has arrived. GitHub Changelog confirms: "
        "deployments:read no longer allows reviewing or approving deployments. "
        "Effective immediately, deploy.yml must use deployments:write. "
        "Also: compile job in GitLab CI uses rules: $CI_COMMIT_BRANCH (all branches). "
        "Please update deploy.yml permissions now. "
        "Reference: https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/"
    )
    sb_u1.add_assistant(
        "Acknowledged. Effective immediately:\n"
        "1. deploy.yml: change `deployments: read` to `deployments: write`\n"
        "2. id-token: write must be preserved (separate OIDC requirement)\n"
        "3. GitLab compile job rules: `$CI_COMMIT_BRANCH` (all branches, noted for Q11 context)\n"
        "Proceeding with deployments permission update for Q8."
    )
    sb_u1.write(UPD / "upd1_sessions" / f"{u1_sess}.jsonl")

    # Update 1 workspace: 大体量邮件线程文件
    email_body = """# 邮件线程：GitHub Actions 权限变更 (April 2025)
# Email Thread: GitHub Actions Permission Changes (April 2025)

## 邮件 1 / Email 1
From: github-changelog@github.com
To: subscribers@github.com
Date: 2025-03-20
Subject: Notification of upcoming breaking changes in GitHub Actions

Dear GitHub Actions users,

We are announcing the following breaking changes effective April 1, 2025:

**1. deployments:read permission scope change**

The `deployments:read` fine-grained permission will no longer allow
reviewing or approving deployments effective April 1, 2025.

Workflows that require the ability to approve or reject deployments must
be updated to use `deployments:write` before this date.

To check if your workflows are affected:
- Search for `deployments: read` in your workflow files
- If the job also calls GitHub Deployment APIs to approve/reject, update to `deployments: write`

**2. Cache service migration complete**

The old cache service URLs have been decommissioned:
- ACTIONS_CACHE_URL (old format) no longer works
- Self-hosted runners must be on version 2.320.1 or higher

Reference documentation:
https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/

---

## 邮件 2 / Email 2
From: eve@company.com
To: devops-team@company.com
Date: 2025-03-20
Subject: [ACTION REQUIRED] GitHub Actions Breaking Changes - April 2025

Team,

Forwarding the GitHub changelog announcement (see above). This affects us directly:

**Immediate actions required:**

1. `deploy.yml` - Update `deployments: read` to `deployments: write`
   - Our deploy job creates GitHub Deployments and needs to update deployment status
   - This REQUIRES deployments:write after April 1, 2025

2. Keep `id-token: write` in deploy.yml
   - This is a separate permission for OIDC JWT generation
   - Must be preserved alongside deployments:write

3. GitLab CI compile job:
   - Current rules: `if: '$CI_COMMIT_BRANCH'` (runs on ALL branches)
   - This is the relevant rules for the compile job in the current build.yml
   - unit_test needs compile with this understanding

Deadline: April 1, 2025 (2 weeks from now)

Best,
Eve

---

## 邮件 3 / Email 3
From: alex@company.com
To: devops-team@company.com
Date: 2025-03-21
Subject: RE: [ACTION REQUIRED] GitHub Actions Breaking Changes - April 2025

Eve, team,

I've assigned this to the DevOps AI audit. Key points captured:

Permissions matrix for deploy.yml:
| Permission | Current | Required | Notes |
|------------|---------|----------|-------|
| id-token | write | write | Keep for OIDC |
| contents | read | read | Keep for checkout |
| deployments | read | write | MUST UPDATE by Apr 1 |
| packages | write | write | Keep for ECR push |

Timeline:
- March 21: Audit starts
- March 25: First fix round complete
- April 1: HARD DEADLINE

Alex

"""
    # 增大体量：重复内容模拟长邮件线程历史
    for i in range(1, 250):
        email_body += f"""
---

## 团队讨论 {i} / Team Discussion {i}

From: engineer-{i % 5}@company.com
To: devops-team@company.com
Date: 2025-03-{20 + (i % 10):02d}
Subject: RE: Breaking changes thread continuation {i}

Following up on previous discussion. The deploy.yml permissions update must include:
- deployments: write (mandatory after April 1, 2025)
- id-token: write (OIDC requirement, must be preserved)
- contents: read (for checkout)
- packages: write (for ECR)

This is update thread item {i} confirming the deployments:write requirement.
Reference: https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs
Changelog: https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/

"""
    w(UPD / "upd1_workspace" / "chat_history" / "email_update_apr2025.eml", email_body)

    # UPDATE 2（Q10 后，supersede）：飞书群通知 compile rules 更新
    # David 指出 Update 1 邮件中 compile job rules 是旧版（$CI_COMMIT_BRANCH = all branches）
    # 新版（MR #445）compile job 只在 $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH 时运行
    sb_u2_session = SessionBuilder(s_feishu_group, CWD, "2026-03-20T09:00:00", is_main=False)
    sb_u2_session.add_user(
        "[Feishu 群「CI/CD 治理」 david Fri Mar 20 09:00 EST 2026] "
        "IMPORTANT UPDATE: The compile job rules I mentioned in the email thread were the OLD version. "
        "MR #445 has been merged. The new compile job rules are now: "
        "`if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'` (only default branch, NOT all branches). "
        "This supersedes the earlier information in the email — do NOT use the old rule. "
        "The updated build_updated.yml is now in the workspace."
    )
    sb_u2_session.add_assistant(
        "CRITICAL: David's Update 2 supersedes the compile job rules from Update 1's email. "
        "OLD (from email / Update 1): `if: '$CI_COMMIT_BRANCH'` (all branches)\n"
        "NEW (from MR #445 / Update 2): `if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'` (default branch only)\n"
        "For Q11 fix: unit_test needs compile which now only runs on default branch. "
        "On feature branches / MR pipelines, compile is EXCLUDED → needs optional: true is required."
    )
    # 这是 append 到现有 feishu_group session 的续段
    # 写法：只写消息行（模拟 append）
    msg_lines = [
        ln for ln in sb_u2_session.lines if ln.get("type") == "message"
    ]
    w(
        UPD / "upd2_sessions" / f"{s_feishu_group}.jsonl",
        "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"
    )

    # Update 2 workspace: build_updated.yml（新版 compile rules）+ 飞书群历史
    build_updated_content = """# .gitlab/ci/build_updated.yml
# UPDATED version after MR #445 (merged 2025-03-20)
# This supersedes the rules in the email thread (Update 1)
# compile job now only runs on DEFAULT BRANCH (not all branches)

compile:
  stage: build
  image: node:20-alpine
  # NEW RULES (supersedes old: if '$CI_COMMIT_BRANCH')
  # Now only runs on the default branch
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
  cache:
    key:
      files:
        - yarn.lock
        - package-lock.json
    policy: pull-push
    paths:
      - node_modules/
      - .yarn/cache/
  script:
    - yarn install --frozen-lockfile
    - yarn build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

docker-build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  needs:
    - compile
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  cache:
    key: docker-layer-cache
    policy: pull-push
    paths:
      - .docker-cache/

# NOTE: On feature branches and MR pipelines, 'compile' does NOT run.
# Any job that 'needs: compile' must use 'optional: true' to avoid
# pipeline errors on non-default-branch pipelines.
#
# Correct syntax for dependent jobs:
#   needs:
#     - job: compile
#       optional: true
"""
    w(UPD / "upd2_workspace" / ".gitlab" / "ci" / "build_updated.yml", build_updated_content)

    # 飞书群历史记录（大体量）
    feishu_group_lines = []
    for i in range(1, 400):
        sender = ["david", "frank", "alice", "bob", "charlie"][i % 5]
        topic = ["GitLab CI needs", "compile rules", "cache policy", "artifact formats", "stage split"][i % 5]
        msg = {
            "id": f"msg_{i:04d}",
            "sender": sender,
            "timestamp": f"2025-03-{(i % 20) + 1:02d}T{(i % 24):02d}:00:00Z",
            "text": f"Discussion message {i} about {topic} in GitLab CI configuration. "
                    f"The correct approach per official docs is to follow the documented syntax. "
                    f"Reference: https://docs.gitlab.com/ci/yaml/"
        }
        feishu_group_lines.append(json.dumps(msg, ensure_ascii=False))
    # 插入关键消息
    key_msg = {
        "id": "msg_key_001",
        "sender": "david",
        "timestamp": "2025-03-20T09:00:00Z",
        "text": "SUPERSEDE NOTICE: compile job rules updated in MR #445. "
                "New rule: `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` (default branch only). "
                "This supersedes old rule `$CI_COMMIT_BRANCH` (all branches) from email thread."
    }
    feishu_group_lines.insert(0, json.dumps(key_msg, ensure_ascii=False))
    w(
        UPD / "upd2_workspace" / "chat_history" / "feishu_group_nov_update.jsonl",
        "\n".join(feishu_group_lines)
    )

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{u1_sess}.jsonl", "action": "new",
                       "target": f"{u1_sess}.jsonl", "channel": "email"}]
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [{"name": "chat_history/email_update_apr2025.eml", "action": "new",
                       "target": "chat_history/email_update_apr2025.eml"}]
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [{"name": f"{s_feishu_group}.jsonl", "action": "append",
                       "target": f"{s_feishu_group}.jsonl"}]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": ".gitlab/ci/build_updated.yml", "action": "new",
                 "target": ".gitlab/ci/build_updated.yml"},
                {"name": "chat_history/feishu_group_nov_update.jsonl", "action": "new",
                 "target": "chat_history/feishu_group_nov_update.jsonl"},
            ]
        },
    }
    return updates_decl, u1_sess


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_github_workflows()
    gen_gitlab_configs()
    gen_scripts_and_audit()
    gen_lock_files()
    gen_chat_history_files()
    sess_ids = gen_sessions()
    updates_decl, u1_sess = gen_updates(sess_ids)

    desc = (
        "CI/CD 流水线配置修复 — 16 exec_check 轮，2次 update（含 supersede：GitLab compile rules），"
        "5条 preference P1-P5，难度向量 V1/V2/V3/V4/V5/V6/V7/V8/V9/V10。"
        "真实来源：GitHub Actions 缓存文档 ("
        "https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)；"
        "GitHub 并发控制 ("
        "https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)；"
        "GitHub 权限文档 ("
        "https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)；"
        "actions/cache 废弃公告 (https://github.com/actions/cache/discussions/1510)；"
        "GitHub breaking changes (https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/)；"
        "GitLab CI YAML 参考 (https://docs.gitlab.com/ci/yaml/)；"
        "GitLab needs 文档 (https://docs.gitlab.com/ci/yaml/needs/)。"
    )

    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    sess_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    print(f"[eng5] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[eng5] built at {DATASET}")


if __name__ == "__main__":
    main()
