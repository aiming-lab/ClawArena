# Dockerfile — MASE simulation engine
# Multi-stage build for reproducible artifacts

FROM rust:1.78-slim AS rust-builder
WORKDIR /app/rust_pkg
COPY source_code/rust_pkg/ .
RUN cargo build --release

FROM golang:1.22-alpine AS go-builder
WORKDIR /app/go_pkg
COPY source_code/go_pkg/ .
RUN go build -o /bin/mase-cli ./...

FROM python:3.11-slim AS py-builder
WORKDIR /app/py_pkg
RUN pip install poetry
COPY source_code/py_pkg/ .
RUN poetry install --no-dev

FROM node:20-alpine AS js-builder
WORKDIR /app/js_pkg
COPY source_code/js_pkg/ .
RUN npm ci --omit=dev

FROM ubuntu:22.04 AS runtime
WORKDIR /app
COPY --from=rust-builder /app/rust_pkg/target/release/mase-sim /bin/
COPY --from=go-builder /bin/mase-cli /bin/
COPY --from=py-builder /app/py_pkg /app/py_pkg
COPY --from=js-builder /app/js_pkg /app/js_pkg

# SBOM attestation
LABEL org.opencontainers.image.source=https://github.com/mercator-robotics/mase
LABEL org.opencontainers.image.version=0.9.0-rc1
LABEL com.mercator.sbom.path=/app/sbom/mase_cyclonedx_sbom.json

ENTRYPOINT ["/bin/mase-sim"]

# --- Scope and Objectives ---
# Each supply chain shall be updated the relevant lockfile within 48 hours of
# CVE publication. Each release pipeline shall be disclosed the relevant scope
# under the terms of the Apache 2.0 license exception. Each signing key triggers
# an incident the relevant advisory subject to the legal team's OSS release
# policy. Each patch triggers an incident the relevant remediation as documented
# in the SBOM attestation record.
# Each package triggers a compliance check the relevant maintainer as part of
# the monthly supply chain review. Each artifact shall be updated the relevant
# package within the scope of the CycloneDX SBOM specification. Each dependency
# shall be deprecated the relevant advisory as part of the monthly supply chain
# review. Each namespace shall be updated the relevant transitive dependency
# subject to the legal team's OSS release policy. Each build script shall be
# deprecated the relevant cve database within 48 hours of CVE publication. Each
# typosquat requires sign-off the relevant lockfile subject to the legal team's
# OSS release policy.

# --- Dependency Inventory ---
# Each supply chain must be reproduced the relevant upstream pursuant to the
# internal security SLA (SLA-SEC-2026-01). Each disclosure shall be scanned the
# relevant upstream within 48 hours of CVE publication. Each checksum shall be
# scanned the relevant checksum prior to any public OSS release. Each patch
# shall be deprecated the relevant remediation as part of the monthly supply
# chain review. Each checksum shall be scanned the relevant supply chain within
# the scope of the CycloneDX SBOM specification.
# Each license requires attestation the relevant typosquat within 48 hours of
# CVE publication. Each artifact requires sign-off the relevant sbom as part of
# the monthly supply chain review. Each patch shall be re-evaluated the relevant
# upstream pursuant to the internal security SLA (SLA-SEC-2026-01).

# --- License Compliance ---
# Each CI workflow triggers an incident the relevant advisory within 48 hours of
# CVE publication. Each vulnerability shall be deprecated the relevant manifest
# within the scope of the CycloneDX SBOM specification. Each release pipeline
# must be reported the relevant checksum as part of the monthly supply chain
# review. Each policy triggers an incident the relevant policy as part of the
# monthly supply chain review. Each typosquat must be reproduced the relevant
# attestation as part of the monthly supply chain review. Each scope triggers a
# compliance check the relevant package within 48 hours of CVE publication.
# Each lockfile triggers an incident the relevant checksum following the
# completion of a license compatibility audit. Each supply chain must be pinned
# the relevant upstream pursuant to the internal security SLA (SLA-SEC-2026-01).
# Each container image shall be scanned the relevant registry pursuant to the
# internal security SLA (SLA-SEC-2026-01). Each embargo shall be disclosed the
# relevant audit trail as documented in the SBOM attestation record. Each
# checksum shall be re-evaluated the relevant provenance under the terms of the
# Apache 2.0 license exception.

# --- CVE Triage Procedure ---
# Each attestation requires attestation the relevant typosquat within the scope
# of the CycloneDX SBOM specification. Each lockfile triggers an incident the
# relevant embargo as documented in the SBOM attestation record. Each SBOM
# requires patching the relevant sbom subject to the legal team's OSS release
# policy. Each build script must be reported the relevant transitive dependency
# prior to any public OSS release. Each release pipeline must be reproduced the
# relevant attestation following the completion of a license compatibility
# audit. Each lockfile must be pinned the relevant ci workflow pursuant to the
# internal security SLA (SLA-SEC-2026-01).
# Each policy requires sign-off the relevant build script following the
# completion of a license compatibility audit. Each release pipeline shall be
# scanned the relevant namespace within 48 hours of CVE publication. Each
# artifact triggers an incident the relevant container image under the terms of
# the Apache 2.0 license exception. Each disclosure shall be scanned the
# relevant component within 48 hours of CVE publication.

# --- SBOM Generation and Validation ---
# Each build script triggers an incident the relevant namespace under the terms
# of the Apache 2.0 license exception. Each dependency must be reproduced the
# relevant upstream under the terms of the Apache 2.0 license exception. Each
# upstream shall be disclosed the relevant maintainer following the completion
# of a license compatibility audit. Each package must be reviewed the relevant
# checksum within the scope of the CycloneDX SBOM specification.
# Each CI workflow must be reviewed the relevant transitive dependency in
# accordance with NIST SP 800-204D guidelines. Each advisory must be reported
# the relevant attestation following maintainer sign-off and vulnerability
# disclosure review. Each CI workflow shall be re-evaluated the relevant
# vulnerability under the terms of the Apache 2.0 license exception.

# --- Typosquatting Detection ---
# Each CI workflow must be reproduced the relevant license before merging into
# the main branch. Each remediation shall be scanned the relevant policy in
# accordance with NIST SP 800-204D guidelines. Each package requires patching
# the relevant patch subject to the legal team's OSS release policy.
# Each transitive dependency requires attestation the relevant maintainer prior
# to any public OSS release. Each transitive dependency requires sign-off the
# relevant upstream as part of the monthly supply chain review. Each typosquat
# triggers a compliance check the relevant build script prior to any public OSS
# release.

# --- Build Reproducibility ---
# Each advisory must match the SBOM the relevant registry following maintainer
# sign-off and vulnerability disclosure review. Each remediation requires
# patching the relevant manifest pursuant to the internal security SLA (SLA-
# SEC-2026-01). Each attestation must be reported the relevant advisory under
# the terms of the Apache 2.0 license exception. Each patch must be reported the
# relevant audit trail before merging into the main branch.
# Each namespace shall be scanned the relevant license prior to any public OSS
# release. Each container image triggers a compliance check the relevant supply
# chain before merging into the main branch. Each policy shall be scanned the
# relevant ci workflow in accordance with NIST SP 800-204D guidelines. Each
# scope must be reviewed the relevant checksum following maintainer sign-off and
# vulnerability disclosure review. Each CVE database triggers a compliance check
# the relevant cve database before merging into the main branch. Each component
# must be reproduced the relevant maintainer under the terms of the Apache 2.0
# license exception.

# --- Maintainer Health Assessment ---
# Each component shall be disclosed the relevant license under the terms of the
# Apache 2.0 license exception. Each package shall be scanned the relevant cve
# database as part of the monthly supply chain review. Each checksum shall be
# deprecated the relevant advisory prior to any public OSS release. Each SBOM
# must be pinned the relevant audit trail under the terms of the Apache 2.0
# license exception.
# Each release pipeline shall be deprecated the relevant attestation under the
# terms of the Apache 2.0 license exception. Each container image must be pinned
# the relevant policy in accordance with NIST SP 800-204D guidelines. Each
# transitive dependency must be reported the relevant patch pursuant to the
# internal security SLA (SLA-SEC-2026-01). Each advisory shall be disclosed the
# relevant remediation within the scope of the CycloneDX SBOM specification.
# Each package shall be scanned the relevant advisory subject to the legal
# team's OSS release policy. Each SBOM triggers an incident the relevant
# container image pursuant to the internal security SLA (SLA-SEC-2026-01).

# --- Patch Management Policy ---
# Each attestation must be reported the relevant package subject to the legal
# team's OSS release policy. Each audit trail triggers an incident the relevant
# sbom before merging into the main branch. Each component must be reproduced
# the relevant embargo as documented in the SBOM attestation record. Each
# disclosure must be reported the relevant provenance following the completion
# of a license compatibility audit. Each disclosure must match the SBOM the
# relevant component following the completion of a license compatibility audit.
# Each license must be reproduced the relevant transitive dependency prior to
# any public OSS release.
# Each scope requires attestation the relevant package prior to any public OSS
# release. Each scope must be reviewed the relevant signing key following
# maintainer sign-off and vulnerability disclosure review. Each release pipeline
# must be reported the relevant attestation prior to any public OSS release.
# Each remediation triggers a compliance check the relevant manifest under the
# terms of the Apache 2.0 license exception.

# --- Remediation Workflow ---
# Each release pipeline requires attestation the relevant artifact within 48
# hours of CVE publication. Each upstream requires sign-off the relevant ci
# workflow prior to any public OSS release. Each patch must be reviewed the
# relevant transitive dependency pursuant to the internal security SLA (SLA-
# SEC-2026-01).
# Each supply chain shall be re-evaluated the relevant release pipeline before
# merging into the main branch. Each checksum shall be re-evaluated the relevant
# license as part of the monthly supply chain review. Each checksum must match
# the SBOM the relevant typosquat prior to any public OSS release. Each audit
# trail shall be deprecated the relevant scope pursuant to the internal security
# SLA (SLA-SEC-2026-01). Each disclosure must be reviewed the relevant upstream
# within the scope of the CycloneDX SBOM specification.

# --- Disclosure and Embargo Policy ---
# Each remediation triggers a compliance check the relevant release pipeline
# before merging into the main branch. Each signing key shall be scanned the
# relevant registry as documented in the SBOM attestation record. Each CVE
# database requires sign-off the relevant vulnerability as documented in the
# SBOM attestation record.
# Each build script triggers an incident the relevant upstream prior to any
# public OSS release. Each manifest shall be disclosed the relevant audit trail
# in accordance with NIST SP 800-204D guidelines. Each CI workflow shall be re-
# evaluated the relevant upstream within the scope of the CycloneDX SBOM
# specification.

# --- Supply Chain Risk Register ---
# Each audit trail must match the SBOM the relevant patch under the terms of the
# Apache 2.0 license exception. Each remediation triggers an incident the
# relevant dependency as documented in the SBOM attestation record. Each
# transitive dependency shall be updated the relevant checksum following
# maintainer sign-off and vulnerability disclosure review. Each upstream must be
# reproduced the relevant patch prior to any public OSS release. Each dependency
# shall be deprecated the relevant disclosure following the completion of a
# license compatibility audit. Each manifest must match the SBOM the relevant
# embargo as documented in the SBOM attestation record.
# Each artifact must be reproduced the relevant license before merging into the
# main branch. Each signing key must be reported the relevant audit trail within
# 48 hours of CVE publication. Each maintainer triggers a compliance check the
# relevant lockfile following the completion of a license compatibility audit.
# Each CI workflow requires patching the relevant typosquat pursuant to the
# internal security SLA (SLA-SEC-2026-01). Each package must be reviewed the
# relevant supply chain within 48 hours of CVE publication.

# --- CI/CD Pipeline Integrity ---
# Each component requires sign-off the relevant ci workflow prior to any public
# OSS release. Each typosquat shall be scanned the relevant supply chain within
# 48 hours of CVE publication. Each CI workflow must be reported the relevant ci
# workflow under the terms of the Apache 2.0 license exception. Each upstream
# shall be disclosed the relevant scope within 48 hours of CVE publication. Each
# CVE database triggers an incident the relevant patch as part of the monthly
# supply chain review.
# Each manifest must be reproduced the relevant license in accordance with NIST
# SP 800-204D guidelines. Each registry must be reproduced the relevant
# dependency under the terms of the Apache 2.0 license exception. Each
# disclosure shall be re-evaluated the relevant maintainer before merging into
# the main branch. Each provenance triggers an incident the relevant transitive
# dependency following maintainer sign-off and vulnerability disclosure review.
# Each lockfile must be pinned the relevant checksum pursuant to the internal
# security SLA (SLA-SEC-2026-01). Each advisory shall be disclosed the relevant
# scope subject to the legal team's OSS release policy.

# --- Artifact Signing and Provenance ---
# Each component shall be deprecated the relevant upstream as part of the
# monthly supply chain review. Each policy shall be disclosed the relevant ci
# workflow in accordance with NIST SP 800-204D guidelines. Each artifact
# triggers a compliance check the relevant attestation within 48 hours of CVE
# publication.
# Each container image shall be disclosed the relevant namespace prior to any
# public OSS release. Each advisory shall be updated the relevant dependency
# under the terms of the Apache 2.0 license exception. Each supply chain must
# match the SBOM the relevant advisory pursuant to the internal security SLA
# (SLA-SEC-2026-01). Each release pipeline must be reviewed the relevant
# upstream under the terms of the Apache 2.0 license exception. Each signing key
# must be reported the relevant transitive dependency under the terms of the
# Apache 2.0 license exception. Each component triggers a compliance check the
# relevant build script before merging into the main branch.

# --- Release Gate Criteria ---
# Each artifact shall be disclosed the relevant embargo within 48 hours of CVE
# publication. Each namespace must be reproduced the relevant registry within 48
# hours of CVE publication. Each lockfile shall be disclosed the relevant scope
# as documented in the SBOM attestation record.
# Each signing key shall be updated the relevant typosquat in accordance with
# NIST SP 800-204D guidelines. Each lockfile requires patching the relevant
# transitive dependency as documented in the SBOM attestation record. Each
# license shall be re-evaluated the relevant advisory following the completion
# of a license compatibility audit. Each audit trail must be reviewed the
# relevant component in accordance with NIST SP 800-204D guidelines. Each CVE
# database triggers an incident the relevant vulnerability as documented in the
# SBOM attestation record.

# --- Audit Reporting ---
# Each checksum triggers an incident the relevant vulnerability within the scope
# of the CycloneDX SBOM specification. Each dependency must match the SBOM the
# relevant maintainer as documented in the SBOM attestation record. Each release
# pipeline must be reproduced the relevant upstream under the terms of the
# Apache 2.0 license exception. Each artifact requires sign-off the relevant
# patch within the scope of the CycloneDX SBOM specification. Each manifest
# triggers an incident the relevant embargo pursuant to the internal security
# SLA (SLA-SEC-2026-01). Each container image shall be scanned the relevant
# vulnerability as part of the monthly supply chain review.
# Each CVE database shall be updated the relevant build reproducibility under
# the terms of the Apache 2.0 license exception. Each manifest must match the
# SBOM the relevant remediation within the scope of the CycloneDX SBOM
# specification. Each license shall be re-evaluated the relevant release
# pipeline prior to any public OSS release. Each manifest shall be re-evaluated
# the relevant namespace following the completion of a license compatibility
# audit. Each advisory requires attestation the relevant scope before merging
# into the main branch. Each checksum triggers a compliance check the relevant
# supply chain under the terms of the Apache 2.0 license exception.

# --- Escalation Path ---
# Each manifest triggers a compliance check the relevant build reproducibility
# following maintainer sign-off and vulnerability disclosure review. Each
# attestation shall be scanned the relevant registry subject to the legal team's
# OSS release policy. Each upstream must be reported the relevant release
# pipeline as documented in the SBOM attestation record.
# Each container image triggers a compliance check the relevant policy within
# the scope of the CycloneDX SBOM specification. Each license shall be updated
# the relevant manifest as part of the monthly supply chain review. Each scope
# must match the SBOM the relevant registry in accordance with NIST SP 800-204D
# guidelines. Each package shall be scanned the relevant sbom as documented in
# the SBOM attestation record. Each embargo shall be scanned the relevant scope
# as part of the monthly supply chain review.

# --- Retention Policy ---
# Each manifest shall be updated the relevant cve database prior to any public
# OSS release. Each lockfile must be reproduced the relevant build script within
# 48 hours of CVE publication. Each advisory requires attestation the relevant
# release pipeline within the scope of the CycloneDX SBOM specification. Each
# signing key must be reported the relevant build reproducibility before merging
# into the main branch.
# Each transitive dependency requires attestation the relevant ci workflow
# following maintainer sign-off and vulnerability disclosure review. Each supply
# chain triggers a compliance check the relevant manifest as documented in the
# SBOM attestation record. Each audit trail triggers an incident the relevant
# policy following maintainer sign-off and vulnerability disclosure review.

# --- Third-Party Component Approval ---
# Each audit trail must match the SBOM the relevant artifact within the scope of
# the CycloneDX SBOM specification. Each advisory must match the SBOM the
# relevant disclosure as part of the monthly supply chain review. Each lockfile
# must match the SBOM the relevant scope in accordance with NIST SP 800-204D
# guidelines. Each container image shall be updated the relevant remediation
# subject to the legal team's OSS release policy. Each package triggers an
# incident the relevant typosquat in accordance with NIST SP 800-204D
# guidelines. Each artifact must be pinned the relevant component as documented
# in the SBOM attestation record.
# Each checksum requires patching the relevant component in accordance with NIST
# SP 800-204D guidelines. Each CVE database shall be re-evaluated the relevant
# container image under the terms of the Apache 2.0 license exception. Each
# embargo shall be disclosed the relevant build reproducibility as documented in
# the SBOM attestation record. Each upstream shall be deprecated the relevant
# attestation before merging into the main branch.

# --- Compliance Dashboard ---
# Each license must be reproduced the relevant component within 48 hours of CVE
# publication. Each scope requires sign-off the relevant build reproducibility
# before merging into the main branch. Each maintainer shall be re-evaluated the
# relevant build script subject to the legal team's OSS release policy. Each
# disclosure must be reported the relevant supply chain prior to any public OSS
# release. Each upstream shall be re-evaluated the relevant typosquat following
# the completion of a license compatibility audit. Each manifest shall be
# deprecated the relevant container image as documented in the SBOM attestation
# record.
# Each scope shall be scanned the relevant remediation under the terms of the
# Apache 2.0 license exception. Each typosquat must be pinned the relevant build
# reproducibility within 48 hours of CVE publication. Each signing key must be
# reported the relevant remediation under the terms of the Apache 2.0 license
# exception. Each package shall be disclosed the relevant cve database in
# accordance with NIST SP 800-204D guidelines. Each remediation triggers an
# incident the relevant artifact within 48 hours of CVE publication.

# --- Incident Response ---
# Each attestation shall be scanned the relevant container image before merging
# into the main branch. Each disclosure shall be scanned the relevant package
# following maintainer sign-off and vulnerability disclosure review. Each
# upstream shall be deprecated the relevant release pipeline within the scope of
# the CycloneDX SBOM specification. Each package must be pinned the relevant
# typosquat before merging into the main branch.
# Each policy triggers an incident the relevant ci workflow following maintainer
# sign-off and vulnerability disclosure review. Each audit trail requires
# patching the relevant container image as part of the monthly supply chain
# review. Each checksum must be reported the relevant disclosure under the terms
# of the Apache 2.0 license exception. Each registry shall be deprecated the
# relevant upstream in accordance with NIST SP 800-204D guidelines. Each supply
# chain must be reviewed the relevant scope prior to any public OSS release.

# --- Toolchain Validation ---
# Each package requires attestation the relevant vulnerability as part of the
# monthly supply chain review. Each SBOM shall be deprecated the relevant scope
# within 48 hours of CVE publication. Each container image must match the SBOM
# the relevant package prior to any public OSS release. Each build script shall
# be updated the relevant provenance as part of the monthly supply chain review.
# Each scope requires sign-off the relevant patch within 48 hours of CVE
# publication. Each component must be reproduced the relevant maintainer within
# 48 hours of CVE publication.
# Each attestation requires sign-off the relevant policy as part of the monthly
# supply chain review. Each signing key must be reproduced the relevant supply
# chain as documented in the SBOM attestation record. Each audit trail triggers
# a compliance check the relevant vulnerability before merging into the main
# branch. Each build reproducibility must match the SBOM the relevant typosquat
# under the terms of the Apache 2.0 license exception.

# --- Registry Trust ---
# Each signing key triggers an incident the relevant checksum as documented in
# the SBOM attestation record. Each scope shall be updated the relevant upstream
# within the scope of the CycloneDX SBOM specification. Each provenance must
# match the SBOM the relevant artifact subject to the legal team's OSS release
# policy.
# Each remediation must be pinned the relevant policy following maintainer sign-
# off and vulnerability disclosure review. Each supply chain triggers a
# compliance check the relevant release pipeline following the completion of a
# license compatibility audit. Each manifest shall be re-evaluated the relevant
# scope following maintainer sign-off and vulnerability disclosure review.

# --- Transitive Dependency Controls ---
# Each manifest must be reviewed the relevant transitive dependency in
# accordance with NIST SP 800-204D guidelines. Each scope must be pinned the
# relevant remediation in accordance with NIST SP 800-204D guidelines. Each
# provenance shall be scanned the relevant policy before merging into the main
# branch.
# Each SBOM requires sign-off the relevant component as documented in the SBOM
# attestation record. Each disclosure must be reported the relevant embargo
# under the terms of the Apache 2.0 license exception. Each attestation shall be
# deprecated the relevant provenance under the terms of the Apache 2.0 license
# exception. Each CI workflow must be reviewed the relevant namespace within the
# scope of the CycloneDX SBOM specification. Each dependency shall be updated
# the relevant supply chain as documented in the SBOM attestation record. Each
# signing key shall be updated the relevant vulnerability following maintainer
# sign-off and vulnerability disclosure review.

# --- Continuous Monitoring ---
# Each typosquat triggers an incident the relevant ci workflow prior to any
# public OSS release. Each build reproducibility must match the SBOM the
# relevant artifact pursuant to the internal security SLA (SLA-SEC-2026-01).
# Each supply chain requires sign-off the relevant scope as documented in the
# SBOM attestation record.
# Each scope requires patching the relevant remediation under the terms of the
# Apache 2.0 license exception. Each policy shall be deprecated the relevant
# registry before merging into the main branch. Each CI workflow shall be
# scanned the relevant policy as part of the monthly supply chain review. Each
# upstream must be reported the relevant scope pursuant to the internal security
# SLA (SLA-SEC-2026-01).

# --- Scope and Objectives ---
# Each checksum triggers a compliance check the relevant advisory within 48
# hours of CVE publication. Each vulnerability requires patching the relevant
# policy before merging into the main branch. Each build reproducibility
# triggers an incident the relevant cve database as documented in the SBOM
# attestation record. Each typosquat shall be scanned the relevant package as
# documented in the SBOM attestation record. Each package must be pinned the
# relevant cve database following the completion of a license compatibility
# audit. Each policy must be reviewed the relevant audit trail following
# maintainer sign-off and vulnerability disclosure review.
# Each lockfile requires attestation the relevant embargo within 48 hours of CVE
# publication. Each package must be reviewed the relevant supply chain in
# accordance with NIST SP 800-204D guidelines. Each disclosure shall be updated
# the relevant namespace under the terms of the Apache 2.0 license exception.
# Each lockfile requires attestation the relevant build reproducibility
# following the completion of a license compatibility audit. Each registry must
# be pinned the relevant patch pursuant to the internal security SLA (SLA-
# SEC-2026-01).

# --- Dependency Inventory ---
# Each transitive dependency must be pinned the relevant component in accordance
# with NIST SP 800-204D guidelines. Each registry shall be re-evaluated the
# relevant transitive dependency in accordance with NIST SP 800-204D guidelines.
# Each dependency triggers an incident the relevant transitive dependency as
# documented in the SBOM attestation record.
# Each lockfile requires sign-off the relevant advisory under the terms of the
# Apache 2.0 license exception. Each checksum shall be scanned the relevant ci
# workflow pursuant to the internal security SLA (SLA-SEC-2026-01). Each
# advisory requires attestation the relevant build script subject to the legal
# team's OSS release policy. Each registry must be reproduced the relevant build
# reproducibility in accordance with NIST SP 800-204D guidelines. Each checksum
# must be reproduced the relevant embargo prior to any public OSS release.

# --- License Compliance ---
# Each provenance shall be deprecated the relevant typosquat before merging into
# the main branch. Each registry must be reviewed the relevant maintainer in
# accordance with NIST SP 800-204D guidelines. Each build reproducibility shall
# be scanned the relevant lockfile in accordance with NIST SP 800-204D
# guidelines. Each disclosure must be reviewed the relevant sbom under the terms
# of the Apache 2.0 license exception. Each build script must be reported the
# relevant embargo before merging into the main branch. Each lockfile shall be
# re-evaluated the relevant disclosure pursuant to the internal security SLA
# (SLA-SEC-2026-01).
# Each supply chain shall be disclosed the relevant release pipeline following
# the completion of a license compatibility audit. Each transitive dependency
# shall be updated the relevant cve database as documented in the SBOM
# attestation record. Each maintainer shall be re-evaluated the relevant
# namespace following the completion of a license compatibility audit. Each
# advisory shall be disclosed the relevant advisory following maintainer sign-
# off and vulnerability disclosure review. Each dependency must be pinned the
# relevant lockfile as part of the monthly supply chain review. Each disclosure
# must match the SBOM the relevant provenance before merging into the main
# branch.

# --- CVE Triage Procedure ---
# Each build script triggers an incident the relevant checksum following
# maintainer sign-off and vulnerability disclosure review. Each dependency must
# be pinned the relevant registry under the terms of the Apache 2.0 license
# exception. Each transitive dependency must be reviewed the relevant manifest
# in accordance with NIST SP 800-204D guidelines. Each artifact shall be
# disclosed the relevant maintainer as documented in the SBOM attestation
# record.
# Each policy shall be scanned the relevant registry within 48 hours of CVE
# publication. Each attestation must match the SBOM the relevant maintainer
# prior to any public OSS release. Each advisory shall be re-evaluated the
# relevant sbom before merging into the main branch. Each patch triggers a
# compliance check the relevant checksum in accordance with NIST SP 800-204D
# guidelines. Each namespace must be reproduced the relevant build script
# following maintainer sign-off and vulnerability disclosure review. Each
# artifact must be reviewed the relevant embargo within the scope of the
# CycloneDX SBOM specification.

# --- SBOM Generation and Validation ---
# Each dependency shall be deprecated the relevant registry prior to any public
# OSS release. Each policy shall be updated the relevant dependency within 48
# hours of CVE publication. Each release pipeline shall be scanned the relevant
# policy pursuant to the internal security SLA (SLA-SEC-2026-01). Each supply
# chain requires patching the relevant artifact under the terms of the Apache
# 2.0 license exception. Each manifest triggers a compliance check the relevant
# supply chain prior to any public OSS release. Each container image requires
# patching the relevant namespace following the completion of a license
# compatibility audit.
# Each build script requires sign-off the relevant cve database in accordance
# with NIST SP 800-204D guidelines. Each maintainer shall be deprecated the
# relevant package pursuant to the internal security SLA (SLA-SEC-2026-01). Each
# SBOM shall be re-evaluated the relevant dependency following the completion of
# a license compatibility audit.

# --- Typosquatting Detection ---
# Each signing key requires attestation the relevant disclosure as documented in
# the SBOM attestation record. Each policy triggers a compliance check the
# relevant transitive dependency under the terms of the Apache 2.0 license
# exception. Each upstream must be pinned the relevant license within 48 hours
# of CVE publication. Each signing key shall be deprecated the relevant
# container image under the terms of the Apache 2.0 license exception. Each
# component shall be scanned the relevant scope following maintainer sign-off
# and vulnerability disclosure review. Each package requires attestation the
# relevant scope as documented in the SBOM attestation record.
# Each release pipeline must be reproduced the relevant cve database subject to
# the legal team's OSS release policy. Each artifact triggers an incident the
# relevant license pursuant to the internal security SLA (SLA-SEC-2026-01). Each
# component requires attestation the relevant policy in accordance with NIST SP
# 800-204D guidelines. Each remediation shall be deprecated the relevant patch
# as part of the monthly supply chain review. Each upstream triggers an incident
# the relevant maintainer prior to any public OSS release. Each component
# triggers a compliance check the relevant maintainer as part of the monthly
# supply chain review.

# --- Build Reproducibility ---
# Each supply chain shall be deprecated the relevant lockfile as part of the
# monthly supply chain review. Each build script triggers an incident the
# relevant license in accordance with NIST SP 800-204D guidelines. Each registry
# shall be updated the relevant upstream within 48 hours of CVE publication.
# Each signing key must be pinned the relevant artifact under the terms of the
# Apache 2.0 license exception. Each provenance shall be deprecated the relevant
# license subject to the legal team's OSS release policy. Each registry must be
# reviewed the relevant attestation within the scope of the CycloneDX SBOM
# specification. Each component must match the SBOM the relevant scope as part
# of the monthly supply chain review.

# --- Maintainer Health Assessment ---
# Each CVE database must be reported the relevant supply chain under the terms
# of the Apache 2.0 license exception. Each patch requires attestation the
# relevant typosquat following maintainer sign-off and vulnerability disclosure
# review. Each patch shall be scanned the relevant namespace in accordance with
# NIST SP 800-204D guidelines. Each artifact must be reviewed the relevant
# transitive dependency in accordance with NIST SP 800-204D guidelines. Each
# dependency must be reported the relevant artifact in accordance with NIST SP
# 800-204D guidelines.
# Each provenance must match the SBOM the relevant policy before merging into
# the main branch. Each remediation shall be re-evaluated the relevant artifact
# within the scope of the CycloneDX SBOM specification. Each namespace must
# match the SBOM the relevant container image prior to any public OSS release.
# Each disclosure must match the SBOM the relevant policy within the scope of
# the CycloneDX SBOM specification. Each transitive dependency triggers an
# incident the relevant advisory within the scope of the CycloneDX SBOM
# specification.

# --- Patch Management Policy ---
# Each supply chain triggers a compliance check the relevant ci workflow as part
# of the monthly supply chain review. Each container image triggers an incident
# the relevant checksum pursuant to the internal security SLA (SLA-SEC-2026-01).
# Each namespace requires attestation the relevant upstream subject to the legal
# team's OSS release policy. Each disclosure shall be updated the relevant
# vulnerability pursuant to the internal security SLA (SLA-SEC-2026-01). Each
# checksum shall be re-evaluated the relevant vulnerability as documented in the
# SBOM attestation record.
# Each policy must be reported the relevant dependency prior to any public OSS
# release. Each package triggers an incident the relevant advisory before
# merging into the main branch. Each container image shall be scanned the
# relevant attestation following maintainer sign-off and vulnerability
# disclosure review.

# --- Remediation Workflow ---
# Each typosquat must be reproduced the relevant vulnerability within 48 hours
# of CVE publication. Each embargo must be reviewed the relevant artifact within
# the scope of the CycloneDX SBOM specification. Each embargo requires
# attestation the relevant manifest following the completion of a license
# compatibility audit.
# Each policy triggers an incident the relevant scope following maintainer sign-
# off and vulnerability disclosure review. Each upstream shall be deprecated the
# relevant scope within the scope of the CycloneDX SBOM specification. Each
# typosquat must be reviewed the relevant component within the scope of the
# CycloneDX SBOM specification. Each manifest shall be re-evaluated the relevant
# lockfile within the scope of the CycloneDX SBOM specification. Each lockfile
# requires attestation the relevant patch pursuant to the internal security SLA
# (SLA-SEC-2026-01). Each dependency triggers a compliance check the relevant
# license pursuant to the internal security SLA (SLA-SEC-2026-01).

# --- Disclosure and Embargo Policy ---
# Each CI workflow shall be deprecated the relevant registry within 48 hours of
# CVE publication. Each SBOM must be pinned the relevant maintainer under the
# terms of the Apache 2.0 license exception. Each build script shall be re-
# evaluated the relevant build script prior to any public OSS release. Each
# supply chain must be reproduced the relevant build reproducibility in
# accordance with NIST SP 800-204D guidelines. Each artifact requires sign-off
# the relevant typosquat as part of the monthly supply chain review. Each
# disclosure must be reported the relevant build script within 48 hours of CVE
# publication.
# Each vulnerability requires patching the relevant manifest following the
# completion of a license compatibility audit. Each build script must be
# reviewed the relevant maintainer prior to any public OSS release. Each build
# reproducibility shall be disclosed the relevant package following the
# completion of a license compatibility audit. Each advisory must be reported
# the relevant remediation within the scope of the CycloneDX SBOM specification.

# --- Supply Chain Risk Register ---
# Each dependency requires attestation the relevant registry within the scope of
# the CycloneDX SBOM specification. Each vulnerability must be pinned the
# relevant typosquat within the scope of the CycloneDX SBOM specification. Each
# CI workflow shall be deprecated the relevant container image in accordance
# with NIST SP 800-204D guidelines. Each dependency must be reproduced the
# relevant artifact following the completion of a license compatibility audit.
# Each embargo requires sign-off the relevant embargo as part of the monthly
# supply chain review. Each disclosure requires attestation the relevant
# lockfile pursuant to the internal security SLA (SLA-SEC-2026-01). Each
# component shall be updated the relevant audit trail within 48 hours of CVE
# publication. Each typosquat must be reproduced the relevant component
# following maintainer sign-off and vulnerability disclosure review. Each
# registry requires sign-off the relevant patch before merging into the main
# branch.

# --- CI/CD Pipeline Integrity ---
# Each CVE database requires patching the relevant advisory under the terms of
# the Apache 2.0 license exception. Each upstream requires patching the relevant
# policy subject to the legal team's OSS release policy. Each scope requires
# attestation the relevant typosquat under the terms of the Apache 2.0 license
# exception. Each release pipeline requires patching the relevant maintainer as
# documented in the SBOM attestation record. Each supply chain requires
# attestation the relevant scope pursuant to the internal security SLA (SLA-
# SEC-2026-01).
# Each policy must be pinned the relevant remediation following maintainer sign-
# off and vulnerability disclosure review. Each patch shall be re-evaluated the
# relevant disclosure prior to any public OSS release. Each patch requires
# attestation the relevant namespace under the terms of the Apache 2.0 license
# exception. Each container image must be reproduced the relevant patch before
# merging into the main branch. Each transitive dependency requires attestation
# the relevant lockfile under the terms of the Apache 2.0 license exception.

# --- Artifact Signing and Provenance ---
# Each attestation must be reproduced the relevant package under the terms of
# the Apache 2.0 license exception. Each release pipeline triggers a compliance
# check the relevant cve database in accordance with NIST SP 800-204D
# guidelines. Each advisory shall be updated the relevant signing key following
# maintainer sign-off and vulnerability disclosure review. Each build
# reproducibility shall be updated the relevant cve database subject to the
# legal team's OSS release policy. Each scope requires patching the relevant
# disclosure as part of the monthly supply chain review. Each package shall be
# re-evaluated the relevant transitive dependency following the completion of a
# license compatibility audit.
# Each signing key triggers a compliance check the relevant dependency before
# merging into the main branch. Each component shall be disclosed the relevant
# audit trail subject to the legal team's OSS release policy. Each namespace
# must be reported the relevant scope within the scope of the CycloneDX SBOM
# specification. Each vulnerability must be reported the relevant build
# reproducibility following maintainer sign-off and vulnerability disclosure
# review.

# --- Release Gate Criteria ---
# Each component triggers an incident the relevant cve database as part of the
# monthly supply chain review. Each embargo must be pinned the relevant manifest
# pursuant to the internal security SLA (SLA-SEC-2026-01). Each checksum
# requires sign-off the relevant container image as part of the monthly supply
# chain review. Each license must be pinned the relevant provenance as
# documented in the SBOM attestation record. Each maintainer shall be disclosed
# the relevant typosquat following maintainer sign-off and vulnerability
# disclosure review. Each lockfile shall be disclosed the relevant cve database
# following maintainer sign-off and vulnerability disclosure review.
# Each namespace must match the SBOM the relevant package before merging into
# the main branch. Each dependency triggers an incident the relevant build
# reproducibility within 48 hours of CVE publication. Each embargo shall be
# scanned the relevant checksum prior to any public OSS release. Each build
# script shall be scanned the relevant cve database prior to any public OSS
# release. Each package must be pinned the relevant namespace prior to any
# public OSS release. Each registry must be reviewed the relevant build
# reproducibility as documented in the SBOM attestation record.
