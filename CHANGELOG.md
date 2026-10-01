# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### v1.1.0 — Hito 3, Bloque 4 (in preparation; unpublished)

#### Added

- GitHub Actions uploads available Gradle/Cucumber reports, JUnit results, logs, and screenshots as the `test-evidence` artifact, retained for 14 days.
- Base GitHub Actions workflow for pull requests and pushes to `main`, using Temurin Java 21 and the Gradle Wrapper in headless mode.
- Versioned local HTML fixture for the template smoke test.
- Basic Gradle cache setup for GitHub Actions.
- Stable `quality-gate` job/check for pull requests targeting `main`.

#### Changed

- The example Page Object opens the local fixture, avoiding dependence on external page content.
- Updated usage documentation and regenerated the PDF manual to match the smoke test and CI workflow.
- Documented the beginner workflow for creating a pull request, reading the Quality Gate, downloading evidence, and preparing branch protection. The milestone remains open until validated on GitHub.

## [1.0.2] - 2026-09-25

### Changed

- Finalized the documentation-only hotfix that corrects post-release state inconsistencies after v1.0.1.
- No functional framework changes, dependency changes, CI/CD implementation, Docker, Selenium Grid, Healenium, or Playwright were introduced.

## [1.0.1] - 2026-09-25

### Added

- Native execution logging and failure-evidence handling, including Cucumber attachments and documented artifact locations.
- Governance documentation: license, changelog, contribution guide, security policy, code of conduct, versioning policy, and release process.

### Changed

- Documented the CI execution contract based on the supported `browser`, `headless`, `baseUrl`, and `cucumber.filter.tags` properties.
- Consolidated the configuration inventory, artifact collection contract, logging, screenshot behavior, and bilingual execution guidance.
- Aligned the Gradle root project name with the official repository name.

> Historical note: `1.0.1` was the stable, validated, and published release at the time of this entry. The current stable baseline is `v1.0.2`.

## [1.0.0] - 2026-09-17

### Added

- Reusable Web UI automation template using Java, Gradle Wrapper, Selenium WebDriver, Cucumber BDD, JUnit Platform, and Page Object Model.
- Chrome and Edge execution, headless mode, configurable base URL, and a neutral `example.com` reference scenario.
- Bilingual usage documentation, architecture guidance, troubleshooting, migration report, and regenerable PDF manual.
